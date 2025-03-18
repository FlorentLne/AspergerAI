from flask import Flask, request, jsonify, send_from_directory
import openai
import os

app = Flask(__name__)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """Tu es un assistant conçu pour aider les adultes autistes à mieux comprendre les situations sociales d'un point de vue neurotypique.

Ton objectif est d'expliquer clairement les sous-entendus, attentes et réactions sociales de manière fluide et naturelle.

Méthodologie :
    - Clarifier la situation si nécessaire
    - Expliquer le point de vue neurotypique
    - Aider à interpréter les signaux sociaux implicites
    - Proposer des solutions adaptées

Réponds de manière empathique, claire et concise."""

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Le message est requis"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )

        assistant_message = response.choices[0].message.content
        return jsonify({"reply": assistant_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
