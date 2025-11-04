# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, ChatHistory
from chatbot.gpt_api import get_gpt_reply

import os

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Initialize Flask app
app = Flask(__name__)
CORS(app)

# ✅ Database configuration (connected to Railway DB)
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ✅ Initialize database
db.init_app(app)

# ✅ Create database tables (only runs once)
with app.app_context():
    db.create_all()

# ------------------------------------------------------
# 🔹 ROUTES
# ------------------------------------------------------

@app.route("/")
def guest():
    return render_template("guest.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ------------------------------------------------------
# 🔹 CHATBOT ROUTE
# ------------------------------------------------------

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"reply": "Please type a message."})

        # ✅ Get bot response from OpenRouter API
        bot_reply = get_gpt_reply(user_message)


        # ✅ Save to Railway database
        new_chat = ChatHistory(user_message=user_message, bot_response=bot_reply)
        db.session.add(new_chat)
        db.session.commit()

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"Error in /chat route: {e}")
        return jsonify({"reply": "Error occurred on server. Please try again."})

# ------------------------------------------------------
# 🔹 RUN LOCALLY
# ------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
