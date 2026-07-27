🌿 AuraMind – AI-Powered Mental Health Support Chatbot

A supportive, empathetic mental wellness companion built using Streamlit, Google Gemini API, and NLP (DistilBERT).
Developed as part of my MCA Final Semester Project at Graphic Era Hill University.

💡 Overview

AuraMind is a conversational mental health support system designed to provide a safe, calming, and emotionally intelligent experience.
It enables users to express their feelings, understand their emotional patterns, and receive supportive responses — all in a private, non-clinical environment.

The system includes:

🧠 Gemini-powered conversational AI

💬 Compassionate chat interface

🌈 Sentiment analysis using DistilBERT

📊 Mood tracking & mood journey visualization

📄 AI-generated session summaries

🆘 Crisis support resources for India

✨ Key Features
💬 Compassionate AI Chat

Empathetic responses powered by Google Gemini API

Maintains conversation context

Supportive, safe, non-judgmental tone

🧠 Real-Time Sentiment Analysis

Built with DistilBERT (Transformers)

Detects emotions: Very Positive → Very Negative

Generates a polarity score for mood tracking

💖 Mood Tracker

Select mood: 😊 Good | 😐 Okay | 😔 Low

Add optional notes

Stored in Streamlit session_state

📈 Mood Journey Graph

Line graph showing emotional polarity over time

Updated automatically after:

Chat messages

Manual mood logs

📄 Session Summary Report

AI-generated reflective summary

Highlights emotional trends and positive progress

Powered by get_session_summary() in gemini_bot.py

🆘 Crisis Resource Hub (India)

Provides verified emergency helplines:

Tele MANAS (Govt. of India): 14416 / 1-800-891-4416

AASRA (24×7): +91-22-27546669

Vandrevala Foundation: +91-9999 666 555

🛠️ Tech Stack
Component	Technology
Frontend	Streamlit
Backend	Python 3.x
NLP	HuggingFace Transformers (DistilBERT)
AI Model	Google Gemini API
Styling	Custom CSS (Dark Mode)
Data Handling	Pandas
📁 Folder Structure
AuraMind/
│── app.py
│── gemini_bot.py
│── utils.py
│── style.css
│── requirements.txt
│── .env               ← (You must create this)
│── README.md
│── /screenshots       ← (Add your images here)

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/swati485/AuraMind-Chatbot.git
cd AuraMind-Chatbot

2️⃣ Create & Activate Virtual Environment
Windows
python -m venv env
env\Scripts\activate

Mac/Linux
python3 -m venv env
source env/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure API Keys

Create a .env file in the root folder:

GOOGLE_API_KEY="your_gemini_api_key"
GEMINI_MODEL_NAME="gemini-2.5-flash-lite"

5️⃣ Run the Application
streamlit run app.py


Open the app at:
👉 http://localhost:8501

📸 Screenshots

(Upload your real screenshots here inside /screenshots)

/screenshots
 ├── ui_home.png
 ├── chat_view.png
 ├── mood_graph.png
 └── session_summary.png

🚀 Future Enhancements

✔ User login + cloud mood history
✔ Mobile app (Flutter / React Native)
✔ Voice input + text-to-speech
✔ AI-guided exercises (breathing, grounding, journaling)
✔ Multilingual support (Hindi, Bengali, Marathi…)
✔ Advanced crisis-detection algorithm


