from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# 🌐 ГЛАВНАЯ СТРАНИЦА
@app.route("/")
def home():
    return render_template("index.html")


# 🤖 CHAT API
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        messages = data.get("messages", [])

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return jsonify({"error": "No API key"}), 500

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": messages
            },
            timeout=30
        )

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🚀 START (RAILWAY SAFE)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
