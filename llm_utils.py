import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

#Intent detection logic
def detect_intent(user_input, history=""):
    prompt = f"""
You are an intent classification system

Classify the user's intent inot EXACTLY one of these categories:
- greeting
- inquiry
- high_intent
- irrelevant

Conversation so far:
{history}

User Message:
"{user_input}"

Rules:
- Greeting → hello, hi, hey
- Inquiry → asking about pricing, features, plans
- High_intent → wants to buy, subscribe, try, sign up
- Irrelevant → rejection, "don't", "not interested", or unrelated

Return ONLY one word from the list above
"""
    response = model.generate_content(prompt)
    return response.text.strip().lower()