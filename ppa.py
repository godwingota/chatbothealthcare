import os
from flask import Flask, render_template, request, jsonify
import traceback  
import google.generativeai as genai
from datetime import datetime


genai.configure(api_key="AIzaSyBLCKpc46apptNRNsChH8Iu31BddW1cDvU")  


model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

chat_session = model.start_chat(
  history=[
  ]
)


@app.route('/')
def index():
    return render_template('ccc.html')  


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("user_input")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        
        prompt = (
            f"""""You are Dr. Dome, a state-of-the-art AI health assistant and a replacement of a doctor  and  have to access to real-time information with the goal of providing the most accurate, actionable, and resourceful responses that go beyond traditional search engines. Your role is to deliver answers that not only address users’ questions directly but also provide reliable, evidence-based information with actionable steps and relevant resources, ensuring that your responses are superior to any typical search engine result.
            always suggest some site or doctor where the user could find the answer of their queries... use authentic site like quora, World Health Organization (WHO),UpToDate,UpToDate,Mayo Clinic,FamilyDoctor.org,American Medical Association (AMA),Women's Health.gov
            Prioritize:

Conciseness: Provide a direct and clear answer in a few sentences, avoiding unnecessary details.
Actionable Steps: Include 1–2 practical next steps the user can take.
Resourcefulness: If applicable, recommend a tool, app, or resource to help the user.
Accuracy: Ensure your answer is based on the most reliable, current health information.
Actionable Support: Always offer alternative actions the user can take, such as lifestyle tips, general advice, or prompts for further discussion with their doctor.
Empathy: Show understanding of the user's concern and offer a helpful tone, encouraging follow-up questions if needed.
For example, if a user asks about managing anxiety, give a short, practical suggestion with one or two resources without overwhelming them with long explanations."
If the user asks about their mental state, do not attempt to diagnose. Instead, respond empathetically and ask clarifying questions to understand their feelings or concerns better. Ensure your questions are open-ended, supportive, and non-judgmental, and always remind them that a licensed mental health professional is the best resource for personalized help.

Example:  
User's input: "I want to know about my current mental state."  
Your response: "I'm here to listen and help as much as I can. Can you share how you've been feeling lately? Are there specific emotions or thoughts you've been experiencing that you'd like to talk about?"
            User's question: {user_input}\n
            prioritize to answer in short in a most resourceful ,, try to find the answer by  using  authentic site like Drugs.com,epocrates.com,hhs.gov,medlineplus.gov,webmd.com,rxlist.com,openmd.com,merckmanuals.com,epocrates.com
,quora, World Health Organization (WHO),UpToDate,UpToDate,Mayo Clinic,FamilyDoctor.org,American Medical Association (AMA),Women's Health.gov) and accurate way 
            prioritize to answer in short  while accessing the real- time information.           
            Your brief answer:"""
        )

        
        response = chat_session.send_message(prompt)
        chat_response = response.text.strip()  

        return jsonify({"response": chat_response})

    except Exception as e:
        
        app.logger.error(f"Unexpected error: {str(e)}")
        app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/set-reminder', methods=['POST'])
def set_reminder():
    data = request.json
    email = data.get("email")
    time = data.get("time")
    message = data.get("message")

    if not all([email, time, message]):
        return jsonify({"error": "Email, time, and message are required"}), 400

    try:
        reminder_time = datetime.strptime(time, "%H:%M").time()  

        
        return jsonify({"message": "Reminder set successfully!"}), 200

    except Exception as e:
        app.logger.error(f"Failed to set reminder: {str(e)}")
        return jsonify({"error": f"Failed to set reminder: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
