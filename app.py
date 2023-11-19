import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

# Configure your OpenAI API key from environment variables for better security

app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv('FLASK_SECRET_KEY')  # Set a secret key for session management

# Dummy way to store user data - replace with a proper database in production
users = {
    "TobiasG": generate_password_hash("paco")
}

@app.route('/')
def home():
    return render_template('login.html')  # Render the login page initially

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user_hash = users.get(username)
    
    if user_hash and check_password_hash(user_hash, password):
        session['user'] = username  # Store the username in the session
        return redirect(url_for('voice_assistant'))  # Redirect to the voice assistant page
    else:
        return "Login Failed", 401

@app.route('/voice-assistant')
def voice_assistant():
    if 'user' in session:
        return render_template('voice_assistant.html')  # Render the voice assistant page
    else:
        return redirect(url_for('home'))  # Redirect back to login if not authenticated

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json['message']
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "system", "content": "You are a helpful assistant"}, {"role": "user", "content": user_message}]
        )
        ai_message = response.choices[0].message.content
        return jsonify({'message': ai_message})
    except Exception as e:
        print(e)  # Print the exception to the console
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
