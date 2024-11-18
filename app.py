import os
from flask import Flask, render_template, request, jsonify
import traceback  # For detailed error traceback

# Assuming you have installed google-generativeai using pip
try:
    import google.generativeai as genai
except ModuleNotFoundError:
    print("Error: Please install the 'google-generativeai' library using pip install google-generativeai")
    exit(1)

# Configure the API key (replace with your actual key)
genai.configure(api_key="AIzaSyBLCKpc46apptNRNsChH8Iu31BddW1cDvU")

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle chat responses
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("user_input")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        # Specify the actual model name
        response = genai.generate_text(
            prompt=user_input,
            model="gemini-1.5-flash",
            temperature=0.7,
            max_output_tokens=100
        )

        chat_response = response.result.text  # Assuming the response is in this structure
        return jsonify({"response": chat_response})

    except Exception as e:
        # Log detailed errors for troubleshooting
        app.logger.error(f"Unexpected error: {str(e)}")
        app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)