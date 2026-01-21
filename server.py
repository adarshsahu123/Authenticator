from flask import Flask, render_template, request, redirect, session
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your-secret-key-change-in-production"

# OTP validity time in seconds
OTP_EXPIRY = 120

# Debug mode: Print OTP to console instead of sending email (set to False when SendGrid works)
DEBUG_MODE = False

# ==================== ROUTES ====================

@app.route('/')
def home():
    # Redirect to signup page
    return redirect('/signup')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Handle user signup and OTP generation
    if request.method == 'POST':
        email = request.form['email']
        session['email'] = email
        
        # Generate random 6-digit OTP
        otp = random.randint(100000, 999999)
        session['otp'] = otp
        
        # Set OTP expiry time
        session['otp_expiry'] = (datetime.now() + timedelta(seconds=OTP_EXPIRY)).isoformat()
        
        # Send OTP to email
        if send_otp_email(email, otp):
            return redirect('/verify')
        else:
            return "Failed to send OTP. Please try again."
    
    return render_template('signup.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    # Verify OTP entered by user
    if request.method == 'POST':
        user_otp = request.form['otp']
        correct_otp = session.get('otp')
        expiry = session.get('otp_expiry')
        
        # Check if OTP exists
        if not correct_otp:
            return "No OTP generated. Go to signup."
        
        # Check if OTP is expired
        if datetime.fromisoformat(expiry) < datetime.now():
            return "OTP expired! Please resend."
        
        # Check if OTP matches
        if str(correct_otp) == str(user_otp):
            return redirect('/dashboard')
        else:
            return "Invalid OTP. Try again."
    
    return render_template('verify.html')

@app.route('/resend')
def resend():
    # Resend OTP to user's email
    if 'email' in session:
        email = session['email']
        otp = random.randint(100000, 999999)
        session['otp'] = otp
        session['otp_expiry'] = (datetime.now() + timedelta(seconds=OTP_EXPIRY)).isoformat()
        
        if send_otp_email(email, otp):
            return redirect('/verify')
        else:
            return "Failed to resend OTP."
    
    return redirect('/signup')

@app.route('/dashboard')
def dashboard():
    # Show success page after verification
    if 'email' not in session:
        return redirect('/signup')
    return render_template('dashboard.html', email=session['email'])

@app.route('/logout', methods=['POST'])
def logout():
    # Clear session and logout user
    session.clear()
    return redirect('/signup')

@app.route('/test-sendgrid')
def test_sendgrid():
    api_key = os.environ.get('SENDGRID_API_KEY')
    if not api_key:
        return "❌ SENDGRID_API_KEY not found"
    result = send_otp_email("adarshsahu371@gmail.com", 123456)
    return "✅ Test email sent!" if result else "❌ Failed"



def send_otp_email(to_email, otp_code):
    # Send OTP via SendGrid or console (if DEBUG_MODE)
    if DEBUG_MODE:
        print(f"\n{'='*60}")
        print(f"📧 DEBUG MODE - OTP Generated (Not Sent via Email)")
        print(f"{'='*60}")
        print(f"To: {to_email}")
        print(f"OTP Code: {otp_code}")
        print(f"Expires in: {OTP_EXPIRY} seconds")
        print(f"{'='*60}\n")
        return True
    
    try:
        api_key = os.environ.get('SENDGRID_API_KEY')
        if not api_key:
            print("❌ ERROR: SENDGRID_API_KEY not found")
            return False
        
        message = Mail(
            from_email='adarshsahu371@gmail.com',
            to_emails=to_email,
            subject='Your OTP Verification Code',
            html_content=f'<div style="background:#0f172a;padding:20px;border-radius:10px;color:white;font-family:Arial;"><h2 style="color:#38bdf8;">Verify Your Email</h2><p>Your OTP: <h1 style="font-size:32px;letter-spacing:4px;">{otp_code}</h1></p><p>Expires in <b>120 seconds</b>.</p></div>'
        )
        
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        
        if response.status_code == 202:
            print(f"✅ OTP sent to {to_email}")
            return True
        else:
            print(f"❌ Failed - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == '__main__':
    print("🚀 Starting OTP Email Verification App...")
    print(f"📍 Access at: http://127.0.0.1:5000/")
    if DEBUG_MODE:
        print(f"🔧 DEBUG MODE: ON - OTP will be printed to console")
    else:
        print(f"📧 PRODUCTION MODE: Using SendGrid for emails")
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
