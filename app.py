#python3 -m venv venv
#source venv/bin/activate
#pip install Flask Flask-Mail
#pip install flask-cors

from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import random
import os


app = Flask(__name__)
CORS(app)

# Email Configurationvenv
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sarthakmishra080803@gmail.com'       # Replace with your email
app.config['MAIL_PASSWORD'] = 'pwnq rlqf tknh jytl'        # Replace with your password (preferably an app password)

mail = Mail(app)

# Temporary OTP storage
otp_store = {}

@app.route('/')
def home():
    return 'OTP Authentication Server is Running! 🚀'

# Route to Send OTP
@app.route('/send-otp', methods=['POST'])
def send_otp():
    email = request.json.get('email')
    otp = random.randint(100000, 999999)  # Generate 6-digit OTP
    otp_store[email] = otp                # Store OTP temporarily

    # Send OTP via Email
    msg = Message('Your OTP Code', sender='sarthakmishra080803@gmail.com', recipients=[email])
    msg.body = f'Your OTP is {otp}'
    mail.send(msg)

    return jsonify({"message": "OTP sent successfully."}), 200

# Route to Verify OTP
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    email = request.json.get('email')
    otp = request.json.get('otp')

    if otp_store.get(email) == int(otp):
        del otp_store[email]  # Clear OTP after successful verification
        return jsonify({"message": "OTP verified successfully."}), 200
    else:
        return jsonify({"message": "Invalid OTP."}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable
    app.run(host='0.0.0.0', port=port)    
