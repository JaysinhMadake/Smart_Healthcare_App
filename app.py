from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from chatbot.gpt_api import ask_doctor_bot

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# ----------------------------------
# Database Configuration (Railway)
# ----------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------------------------
# ChatHistory Model
# ----------------------------------
class ChatHistory(db.Model):
    __tablename__ = 'chat_history'
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)

# Create tables (only once)
with app.app_context():
    db.create_all()

# ----------------------------------
# Routes
# ----------------------------------

@app.route('/')
def home():
    return redirect(url_for('guest'))

@app.route('/guest')
def guest():
    return render_template('guest.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# ----------------------------------
# Chatbot Route
# ----------------------------------
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message.strip():
            return jsonify({"reply": "Please enter a valid message."})

        bot_response = ask_doctor_bot(user_message)

        # Save chat to database
        new_chat = ChatHistory(user_message=user_message, bot_response=bot_response)
        db.session.add(new_chat)
        db.session.commit()

        return jsonify({"reply": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------------
# Run App
# ----------------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
