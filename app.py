import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Import your existing backend functions
from gemini_bot import generate_response, get_session_summary
from utils import analyze_sentiment, provide_coping_strategy

# --- Page Configuration and Styling ---

st.set_page_config(
    page_title="AuraMind – Mental Health Support Chatbot",
    page_icon="🧠",
    layout="wide"
)

# Load environment variables
load_dotenv()

def load_css(file_name):
    """Load an external CSS file."""
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}. Make sure it's in the same directory as the app.")

 


# Disclaimer regarding data privacy
def display_disclaimer():
    st.sidebar.markdown(
        "<h2 style='color: #FF5733;'>Data Privacy Disclaimer</h2>",
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        "<span style='color: #FF5733;'>This application stores your session data, including your messages and "
        "sentiment analysis results, in temporary storage during your session. "
        "This data is not stored permanently and is used solely to improve your interaction with the chatbot. "
        "Please avoid sharing personal or sensitive information during your conversation.</span>",
        unsafe_allow_html=True
    )

def display_header():
    """Render the main header section."""
    st.markdown(
        """
        <div class="header">
            <h1>AuraMind</h1>
            <p class="subheader">A safe, supportive space powered by AI.</p>
            <div class="disclaimer">
                <strong>Disclaimer:</strong> This assistant is not a substitute for professional care. 
                If you are in crisis, please call your local emergency number immediately.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def display_sidebar():
    """Render the sidebar with navigation and resources."""
    with st.sidebar:
        st.markdown("<h2>🆘 Support Hub</h2>", unsafe_allow_html=True)

     
        st.divider()
        
        st.markdown("<h3>Crisis Resources (India)</h3>", unsafe_allow_html=True)
        st.write("If you need immediate help, please reach out:")

        # 🇮🇳 Verified Indian Helplines
        st.markdown("- **Tele MANAS (Govt. of India, 24x7):** 14416")
        st.markdown("- **AASRA (24x7):** +91-22-27546669")
        st.markdown("- **Snehi (Emotional Support):** +91-9582208181")
        st.markdown("- **iCALL (TISS):** 022-25521111 (Mon–Sat, 10 AM–8 PM)")
        st.markdown("- **Vandrevala Foundation Helpline:** +91-9999 666 555 (24x7)")

        st.info(
            "If you or someone you know is in emotional distress or crisis, "
            "please reach out to these helplines for free and confidential support."
        )

        st.divider()

        with st.expander("📝 Show Session Summary"):
            if st.button("Generate Summary", use_container_width=True, key="summarize"):
                if st.session_state["messages"]:
                    summary = get_session_summary(st.session_state["messages"])  # type: ignore[arg-type]
                    st.write(summary)
                else:
                    st.write("No conversation yet to summarize.")
        
        st.markdown(
            """
            <div class="sidebar-footer">
                v1.0 • You are not alone 💚
            </div>
            """,
            unsafe_allow_html=True,
        )

# ✅ Function properly closed here — nothing should be indented below this line


def display_prompt_suggestions():
    """Display clickable prompt suggestions."""
    suggestions = [
        "I feel anxious and overwhelmed.",
        "Guide me through a breathing exercise.",
        "Help me reframe a negative thought.",
        "Share coping strategies for stress.",
    ]
    
    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        if cols[i].button(suggestion, use_container_width=True):
            return suggestion
    return None

def display_mood_tracker():
    """Render the mood tracker and recent entries card."""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h2>💖 Mood Tracker</h2>", unsafe_allow_html=True)
    st.write("**How are you feeling right now?**")

    # Initialize state for mood selection
    if "selected_mood" not in st.session_state:
        st.session_state["selected_mood"] = None

    # Mood buttons with unique keys
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("😊 Good", key="mood_good"):
            st.session_state["selected_mood"] = "Positive"
    with col2:
        if st.button("😐 Okay", key="mood_okay"):
            st.session_state["selected_mood"] = "Neutral"
    with col3:
        if st.button("😔 Low", key="mood_low"):
            st.session_state["selected_mood"] = "Negative"

    # Show which mood is currently selected
    if st.session_state["selected_mood"]:
        st.info(f"Selected Mood: {st.session_state['selected_mood']}")

    # Note input
    note = st.text_area("Add a short note (optional):", placeholder="e.g., Stressed about work...")

    # Save entry button
    if st.button("Save Entry", key="save_mood", use_container_width=True):
        mood = st.session_state["selected_mood"]
        if mood:
            polarity = {"Positive": 0.5, "Neutral": 0, "Negative": -0.5}.get(mood, 0)
            entry_text = f"Mood log: {mood}. Note: {note}" if note else f"Mood log: {mood}"
            if "mood_tracker" not in st.session_state:
                st.session_state["mood_tracker"] = []
            st.session_state["mood_tracker"].append((entry_text, mood, polarity))
            st.toast(f"Saved your '{mood}' mood entry!", icon="✅")
            st.session_state["selected_mood"] = None  # reset after saving
        else:
            st.warning("Please select a mood before saving your entry.")

    st.markdown("</div>", unsafe_allow_html=True)


def display_mood_journey_chart():
    """Render the mood journey line chart."""
    with st.container(border=False):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h2>📈 My Mood Journey</h2>", unsafe_allow_html=True)
        if st.session_state["mood_tracker"]:
            mood_data = pd.DataFrame(
                st.session_state["mood_tracker"], columns=["Message", "Sentiment", "Polarity"]
            )
            # Add a time index for better plotting
            mood_data['Time'] = range(len(mood_data))
            st.line_chart(mood_data.set_index('Time')['Polarity'])
        else:
            st.info("Your mood entries and chat sentiments will appear here once you start interacting.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- Main Application ---

# 1. Setup & Initialization
load_css("style.css") # Load the external CSS file

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "mood_tracker" not in st.session_state:
    st.session_state["mood_tracker"] = []

if not (os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")):
    st.warning("Your GOOGLE_API_KEY is not set. The bot may not respond. Please add it to a `.env` file.")

# 2. Render UI Components
display_sidebar()
display_header()

# Main layout with two columns
col1, col2 = st.columns([2, 1])

with col1: # Main chat and interaction area
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h2 id=\"chat\">💬 Compassionate Chat</h2>", unsafe_allow_html=True)
    
    # Initialize with a welcome message if the chat is empty
    if not st.session_state["messages"]:
        st.session_state["messages"].append({
            "role": "assistant",
            "parts": "Hello! I'm here to listen and offer support. How are you feeling today?"
        })

    # Render chat history (scrollable)
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-scroll">', unsafe_allow_html=True)
        for msg in st.session_state["messages"]:
            role = msg.get("role")
            avatar = "🤖" if role == "assistant" else "👤"
            with st.chat_message(role, avatar=avatar):
                st.markdown(msg.get("parts", ""))
        st.markdown('</div>', unsafe_allow_html=True)

    # Handle user input (from both chat input and prompt buttons)
    user_message = st.chat_input("Type how you’re feeling or ask for a technique...")
    suggested_prompt = display_prompt_suggestions()
    
    if suggested_prompt:
        user_message = suggested_prompt

    if user_message:
        # Append user message and analyze mood
        st.session_state["messages"].append({"role": "user", "parts": user_message})
        sentiment, polarity = analyze_sentiment(user_message)
        st.session_state["mood_tracker"].append((user_message, sentiment, polarity))

        # Get assistant response and append it
        with st.spinner("Thinking..."):
            response_text = generate_response(user_message, st.session_state["messages"])  # type: ignore[arg-type]
        st.session_state["messages"].append({"role": "assistant", "parts": response_text})
        
        # Rerun to display the new messages immediately
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


with col2: # Side cards for mood tracking and charts
    display_mood_tracker()
    display_mood_journey_chart()