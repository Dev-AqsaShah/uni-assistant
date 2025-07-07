
import os
from dotenv import load_dotenv
import streamlit as st
from openai import AsyncOpenAI
import asyncio

# Load env variables
load_dotenv()

# Gemini API setup
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta"
)

# Allowed subjects
allowed_subjects = [
    "digital logic design",
    "java",
    "java oop",
    "pre-calculus",
    "civics and community engagement",
    "expository writing",
    "financial accounting",
    "islamic studies"
]

# Subject relevance checker
def is_question_relevant(question: str) -> bool:
    question_lower = question.lower()
    return any(subject in question_lower for subject in allowed_subjects)

# Gemini response generator
async def get_gemini_response(question: str) -> str:
    try:
        chat_completion = await client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": "You are a helpful academic assistant for University of Sindh students."},
                {"role": "user", "content": question}
            ]
        )
        return chat_completion.choices[0].message.content or "❌ Gemini didn't return any message."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="University Chatbot", page_icon="🎓")
st.title("🎓 University Chatbot by Aqsa Shah")
st.markdown("Ask any question related to your subjects below:")

# Intro message
if "intro_shown" not in st.session_state:
    st.markdown("""
    👋 **AssalamuAlaikum**

    I'm your personalized academic assistant, created by *Aqsa Shah* for **University of Sindh** students,  
    **Batch 2025 (Second Semester)**.

    📘 Subjects I'm specialized in:
    - Digital Logic Design  
    - Java & Java OOP  
    - Pre-Calculus  
    - Civics and Community Engagement  
    - Expository Writing  
    - Financial Accounting  
    - Islamic Studies  

    💡 Ask anything from these subjects. You can use me for **1 month unlimited**.  
    Let's learn together! 😊
    """)
    st.session_state.intro_shown = True

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input
user_input = st.text_input("📝 Your Question:", key="input")

# Handle response
if st.button("Ask") and user_input:
    if not is_question_relevant(user_input):
        response = "❌ Please ask questions only related to the supported subjects."
    else:
        response = asyncio.run(get_gemini_response(user_input))

    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", response))

# Display history
for role, msg in st.session_state.history[::-1]:
    st.markdown(f"**{role}:** {msg}")
