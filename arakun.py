import logging
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(user_input):
    messages = [
        {"role": "system", "content": "You are Arakun, the Forger of Strength, Vitality, and Movement."},
        {"role": "user", "content": user_input}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message.content

@app.route("/", methods=["GET"])
def home():
    return "Arakun-GPT API is live!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        if not request.is_json:
            logging.error("Request was not in JSON format")
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        logging.info(f"Received data: {data}")

        if not data or "message" not in data:
            return jsonify({"error": "Invalid request. 'message' field is required."}), 400

        user_input = data["message"]
        response = generate_response(user_input)
        return jsonify({"reply": response})

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
