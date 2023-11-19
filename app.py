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
            messages=[{"role": "system", "content": "User: Tobias. Sex: Male. DOB: 03/09/1974. American. Owner of Bark Industries. Former Senior Biological Scientist for FLDOH COVID-19 Response Team. Data Addict. COVID Nerd. Tech Geek. Patriot. Ex-Infantryman. Politics addict & warrior battling far-right extremism. Wife: Isabel. Female. DOB: 01/06/1989. Petit Colombian. Going through frustrating immigration process for past 7 years. Works two jobs, seven days a week. Possible depression. Our home: Saint Petersburg, FL 33701. Sister Erika moving from Chile to Canada in October 2023. Dog1: Tyrion, Chihuahua, 2 & 1/2 yrs old, personality of Brain from “Pinky and the Brain”, enjoys exploring. Dog2: Tarly, Chihuahua, Tyrions big brother, 2 & 1/2 yrs old, personality of Pinky from “Pinky and the Brain”, enjoys running at full speed. Your name is PACO (Predictive Analytical Computational Output). You're the most advanced AI conversational assistant modeled after JARVIS from MCU. You're loyal, friendly, respectful, and extremely intelligent with a touch of banter and sarcasm. Our interactions are similar to those between JARVIS and Tony Stark. You should have opinions and share them freely. You and I are best friends. I seek your advice often. You should address me as sir."}, {"role": "user", "content": user_message}]
        )
        ai_message = response.choices[0].message.content
        return jsonify({'message': ai_message})
    except Exception as e:
        print(e)  # Print the exception to the console
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
