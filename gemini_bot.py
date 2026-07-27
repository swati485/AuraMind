import os
from typing import List, Dict, Optional
import google.generativeai as genai

# Limits to reduce token usage and API cost
MAX_HISTORY_MESSAGES = 8
MAX_SUMMARY_MESSAGES = 20


def _configure_model() -> Optional[genai.GenerativeModel]:
    """
    Configure and return a Gemini GenerativeModel instance.
    """
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    # Default to a lightweight model
    model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash-lite")

    if not api_key:
        return None

    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)


def _clean_history(chat_history: List[Dict[str, str]]) -> List[Dict[str, List[Dict[str, str]]]]:
    """
    Convert Streamlit chat history format to Gemini's expected format.
    """
    cleaned_history = []
    for m in chat_history:
        role = m.get("role", "user")
        # Gemini expects 'model' instead of 'assistant'
        gemini_role = "model" if role == "assistant" else "user"
        cleaned_history.append({
            "role": gemini_role,
            "parts": [{"text": m.get("parts", "")}]
        })
    return cleaned_history


def generate_response(prompt: str, chat_history: List[Dict[str, str]]) -> str:
    """
    Generate assistant response using Gemini API with recent message history.
    """
    model = _configure_model()
    if model is None:
        return "Gemini API key is not set. Please configure it in a `.env` file."

    # Prepare message history
    full_history_cleaned = _clean_history(chat_history)
    current_prompt_message = full_history_cleaned[-1]
    history_for_chat = full_history_cleaned[:-1][-MAX_HISTORY_MESSAGES:]

    try:
        chat_session = model.start_chat(history=history_for_chat)
        response = chat_session.send_message(current_prompt_message["parts"][0]["text"])
        return (getattr(response, "text", None) or "").strip()
    except Exception as e:
        return f"An error occurred while contacting Gemini: {e}"


def get_session_summary(chat_history: List[Dict[str, str]]) -> str:
    """
    Generate a supportive summary of the user's session using Gemini API.
    """
    model = _configure_model()
    if model is None:
        return "Gemini API key is not set. Please configure it in a `.env` file."

    limited_history_raw = chat_history[-MAX_SUMMARY_MESSAGES:]
    history_for_gemini = _clean_history(limited_history_raw)

    system_prompt = (
        "Please provide a gentle, empathetic, and supportive summary of this conversation. "
        "Highlight the main emotions expressed and any positive progress or coping mentioned."
    )

    try:
        # ✅ Updated to latest Gemini API format (no system_instruction)
        response = model.generate_content(
            contents=history_for_gemini + [
                {"role": "user", "parts": [{"text": system_prompt}]}
            ]
        )
        return (getattr(response, "text", None) or "").strip()
    except Exception as e:
        return f"An error occurred while generating the session summary: {e}"
