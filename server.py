from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# 🌐 ГЛАВНАЯ СТРАНИЦА (ТО ЧТО ТЫ НЕ ВИДЕЛ)
@app.route("/")
def home():
    return render_template("index.html")


# 🤖 CHAT API
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])

    api_key = os.getenv("OPENROUTER_API_KEY")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": messages
        }
    )

    return jsonify(response.json())


# 🚀 RAILWAY PORT
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
