from typing import Optional
from transformers import pipeline, logging
import torch

# Hide distracting warning messages from the transformers library
logging.set_verbosity_error()

# This global variable will hold the model so it's only loaded once
_sentiment_pipeline: Optional[object] = None

def _get_sentiment_pipeline():
    """
    Loads the sentiment analysis model only once to save memory and time.
    """
    global _sentiment_pipeline
    if _sentiment_pipeline is not None:
        return _sentiment_pipeline

    # Use GPU if available, otherwise CPU
    device = 0 if torch.cuda.is_available() else -1

    # Create the pipeline with our specific model and device
    _sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=device
    )
    return _sentiment_pipeline

def analyze_sentiment(text: str):
    """
    Analyzes the sentiment of text using the Hugging Face model.
    Returns a descriptive label and a numerical polarity score.
    """
    try:
        # Get the singleton pipeline instance
        pipe = _get_sentiment_pipeline()
        
        # Run the analysis
        result = pipe(text)[0]
        raw_label = str(result.get("label", "")).upper()
        score = float(result.get("score", 0.0))

        # Convert the model's output ('POSITIVE' or 'NEGATIVE') into a numerical score
        polarity = score if "POS" in raw_label else -score

        # Map the numerical score to a descriptive 5-point scale
        if polarity >= 0.7:
            label = "Very Positive"
        elif 0.3 <= polarity < 0.7:
            label = "Positive"
        elif -0.3 < polarity < 0.3:
            label = "Neutral"
        elif -0.7 < polarity <= -0.3:
            label = "Negative"
        else:
            label = "Very Negative"

        return label, polarity
        
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return "Neutral", 0.0

def provide_coping_strategy(sentiment: str) -> str:
    """
    Returns a brief coping suggestion based on the sentiment label.
    """
    strategies = {
        "Very Positive": "That's fantastic! Keep embracing that positive energy.",
        "Positive": "It's great to hear you're feeling positive. Keep up with what you're doing!",
        "Neutral": "Feeling neutral is perfectly okay. Maybe try engaging in a hobby you enjoy.",
        "Negative": "It sounds like things are tough right now. Remember to be kind to yourself. Taking a short break might help.",
        "Very Negative": "I'm really sorry you're feeling this way. Please consider reaching out to a friend, family member, or a professional for support. You don't have to go through this alone.",
    }
    return strategies.get(sentiment, "Keep going, you're doing great!")


