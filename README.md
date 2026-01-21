# OTP Email Verification System

A simple Flask application that generates and verifies One-Time Passwords (OTP) via email.

---

## 🚀 Quick Start

### 1. Run the Server

```bash
python server.py
```

### 2. Open in Browser

Visit: **http://127.0.0.1:5000/**

### 3. Test the Flow

- Enter your email
- Check console for OTP (DEBUG_MODE) or check email (SendGrid)
- Enter OTP on verify page
- Success! ✅

---

## 📋 How It Works

1. **User enters email** → OTP generated (6 digits)
2. **OTP sent via email** (SendGrid) or printed to console (DEBUG_MODE)
3. **User enters OTP** → System verifies
4. **Success page** shows verified email
5. **Logout** clears session

---

## ⚙️ Configuration

### .env File

```
SENDGRID_API_KEY=SG.your_api_key_here
```

### server.py Settings

```python
DEBUG_MODE = True   # Print OTP to console (testing)
DEBUG_MODE = False  # Send real emails via SendGrid
OTP_EXPIRY = 120    # OTP valid for 120 seconds
```

---

## 📂 Project Structure

```
otp-auth/
├── server.py              # Main Flask application
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
├── templates/
│   ├── signup.html       # Email form
│   ├── verify.html       # OTP form
│   └── dashboard.html    # Success page
└── static/
    ├── style.css         # Styling
    ├── script.js         # Client logic
    └── particles-config.json
```

---

## 🎯 Routes

| Route        | Purpose          |
| ------------ | ---------------- |
| `/signup`    | Email signup     |
| `/verify`    | OTP verification |
| `/resend`    | Resend OTP       |
| `/dashboard` | Success page     |
| `/logout`    | Clear session    |

---

## 📧 Using SendGrid (Real Emails)

1. Create free account: https://sendgrid.com/
2. Get API key from Settings → API Keys
3. Verify sender email in Settings → Sender Authentication
4. Add API key to `.env` file
5. Set `DEBUG_MODE = False` in server.py
6. Restart server

---

## 📦 Dependencies

```
Flask
SendGrid
python-dotenv
```

Install:

```bash
pip install -r requirements.txt
```

---

## ❓ Troubleshooting

| Issue                | Solution                               |
| -------------------- | -------------------------------------- |
| OTP not arriving     | Check spam folder, verify sender email |
| "Failed to send OTP" | Check DEBUG_MODE, verify API key       |
| Connection refused   | Make sure server is running            |

---

**Status: ✅ Production Ready**
