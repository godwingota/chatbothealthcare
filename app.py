import os
from flask import Flask, render_template, request, jsonify
import traceback  # For detailed error traceback
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai
from datetime import datetime

# Configure the API key for Google's Gemini
genai.configure(api_key="AIDvU")  # Replace with your actual API key

# Initialize the generative model
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

# Gmail Configuration (Update these with your email and app password)
GMAIL_USER = "your_email@gmail.com"  # Replace with your Gmail address
GMAIL_PASSWORD = "your_app_password"  # Replace with your Gmail app password

def send_email(to_email, subject, body):
    """
    Function to send email using Gmail's SMTP server.
    """
    try:
        # Set up the MIME
        message = MIMEMultipart()
        message['From'] = GMAIL_USER
        message['To'] = to_email
        message['Subject'] = subject

        # Attach the email body
        message.attach(MIMEText(body, 'plain'))

        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)

        # Send the email
        server.sendmail(GMAIL_USER, to_email, message.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Route for the homepage
@app.route('/')
def index():
    return render_template('ccc.html')  # Ensure your HTML file is named 'index.html' and placed in the 'templates' folder

# Route to handle chat responses
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("user_input")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        # Customize the prompt for concise responses
        prompt = (
            "You are Dr. Dome, an AI healthcare chatbot. Provide short, accurate, and professional responses "
            "to healthcare-related questions. Keep your answers concise and to the point while maintaining a polite tone. "
            "Also provide the contact details of the suitable doctor or specialist if required.\n"
            f"User's question: {user_input}\n"
            "Your brief answer:"
        )

        # Use the GenerativeModel to generate content
        response = model.generate_content(prompt)
        chat_response = response.text.strip()  # Accessing and cleaning up the generated text

        return jsonify({"response": chat_response})

    except Exception as e:
        # Log detailed errors for troubleshooting
        app.logger.error(f"Unexpected error: {str(e)}")
        app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Route to handle setting a reminder
@app.route('/set-reminder', methods=['POST'])
def set_reminder():
    data = request.json
    email = data.get("email")
    time = data.get("time")
    message = data.get("message")

    if not all([email, time, message]):
        return jsonify({"error": "Email, time, and message are required"}), 400

    try:
        # Here we would save the reminder to a database or schedule it
        reminder_time = datetime.strptime(time, "%H:%M").time()  # convert string time to datetime object

        # Send email with the reminder message
        subject = "Your Reminder"
        body = f"Reminder for {message} at {reminder_time.strftime('%I:%M %p')}"
        send_email(email, subject, body)

        return jsonify({"message": "Reminder set and email sent successfully!"}), 200

    except Exception as e:
        app.logger.error(f"Failed to set reminder: {str(e)}")
        return jsonify({"error": f"Failed to set reminder: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
