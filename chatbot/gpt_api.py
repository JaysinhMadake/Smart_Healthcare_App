import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GPT_API_KEY")
if not API_KEY:
    print("❌ ERROR: GPT_API_KEY not found in .env file")

def get_gpt_reply(message):
    """
    Sends the user message to the OpenRouter GPT API and returns the response.
    """
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful medical assistant chatbot."},
                {"role": "user", "content": message},
            ],
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 headers=headers, json=data)

        # Debugging info
        print("🛰️ API Response Status:", response.status_code)
        print("📦 Raw Response:", response.text)

        if response.status_code == 200:
            json_response = response.json()
            reply = json_response["choices"][0]["message"]["content"]
            return reply
        else:
            return f"⚠️ Error from API: {response.status_code} - {response.text}"

    except Exception as e:
        print("❌ Exception:", e)
        return "Sorry, something went wrong while connecting to GPT API."
