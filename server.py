from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "test"

# проверка что сервер жив
@app.route("/")
def home():
    return "Nova server работает"

# основной чат-эндпоинт
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        messages = data.get("messages", [])

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": messages
            }
        )

        result = response.json()

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)