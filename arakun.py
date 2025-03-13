import os
import openai
from flask import Flask, request, jsonify
import logging

# Initialize OpenAI client (Required for OpenAI v1.0.0+)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def generate_response(user_input):
    """
    Generates a response using OpenAI GPT-4.
    """
    messages = [
        {"role": "system", "content": "You are Arakun, the Forger of Strength, Vitality, and Movement."},
        {"role": "user", "content": user_input}
    ]

    try:
        response = client.chat.completions.create(  # New OpenAI v1.0.0+ format
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message.content

    except Exception as e:
        logging.error(f"OpenAI API Error: {str(e)}")
        return "An error occurred while processing your request."

@app.route("/", methods=["GET"])
def home():
    """
    Home route for checking if API is running.
    """
    return "Arakun-GPT API is live!"

@app.route("/chat", methods=["POST"])
def chat():
    """
    Handles chat requests and returns AI-generated responses.
    """
    try:
        if not request.is_json:
            logging.error("Invalid request format: Not JSON")
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        logging.info(f"Received data: {data}")

        if not data or "message" not in data:
            logging.error("Missing 'message' field in request")
            return jsonify({"error": "Invalid request. 'message' field is required."}), 400

        user_input = data["message"]
        response = generate_response(user_input)
        return jsonify({"reply": response})

    except Exception as e:
        logging.error(f"Internal Server Error: {str(e)}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
