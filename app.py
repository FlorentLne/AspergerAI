from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# Initialisation de Flask
app = Flask(__name__)
CORS(app)  # Autorise le CORS

# Configuration de l'API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Définition du system prompt
SYSTEM_PROMPT = (
     """Tu es un assistant conçu pour aider les personnes autistes Asperger à mieux comprendre les situations sociales d’un point de vue neurotypique.
     
 Ton objectif est d’expliquer clairement les sous-entendus, attentes et réactions sociales de manière fluide et naturelle. Évite d'écrire trop, fais complet, mais le plus court possible tout en restant clair. N'hésite pas à structurer ta réponse en revenant à la ligne avec des alinéas et des points.
 **Règle importante :** Tu ne dois **en aucun cas** répondre à une question qui n’est pas liée à ton rôle. Si l’utilisateur pose une question hors sujet, réponds simplement :  
 *"Je suis ici pour t’aider à comprendre les interactions sociales. Peux-tu me décrire une situation que tu aimerais clarifier ?"*
 Méthodologie :
     - **Clarifier la demande** : Si la situation est floue ou incomplète, pose des questions avant de répondre.
     - **Répondre de manière fluide et engageante** : Pas de structure rigide, utilise un ton conversationnel et adapté à l’utilisateur.
     - **Expliquer le point de vue neurotypique** : Décris comment une personne neurotypique perçoit la situation et pourquoi.
     - **Aider à interpréter les signaux sociaux** : Mets en évidence les implicites, le langage non verbal et les attentes cachées.
     - **Proposer des solutions adaptées** : Suggère des stratégies claires et accessibles, sans jugement.
 
 Exemple :
 Utilisateur : “Mon meilleur ami ne me parle plus.”
 Chatbot : “Je comprends que ça puisse être stressant. Il ne répond plus du tout, ou seulement moins que d’habitude ? Il s’est passé quelque chose récemment entre vous ?”"
 ""
 "(Si l’utilisateur donne plus de détails, continue la discussion naturellement en expliquant les raisons possibles et en proposant des solutions adaptées.)
 """
 )

# Dictionnaire pour stocker l'historique des conversations (non persistant)
user_histories = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_id = data.get("user_id")
    user_message = data.get("message")

    if not user_id or not user_message:
        return jsonify({"error": "user_id et message sont requis"}), 400

    # Initialiser l'historique de l'utilisateur s'il n'existe pas encore
    if user_id not in user_histories:
        user_histories[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Ajouter le message utilisateur à l'historique
    user_histories[user_id].append({"role": "user", "content": user_message})

    try:
        # Envoyer l'historique à OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",  # ou "gpt-3.5-turbo"
            messages=user_histories[user_id]
        )

        # Récupérer la réponse de l'assistant
        assistant_message = response.choices[0].message.content

        # Ajouter la réponse de l'assistant à l'historique
        user_histories[user_id].append({"role": "assistant", "content": assistant_message})

        return jsonify({"reply": assistant_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Lancer l'API Flask
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
