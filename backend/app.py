# app.py
from flask import Flask, request, jsonify, url_for
from flask_pymongo import PyMongo
from flask_mail import Mail, Message
from email_validator import validate_email, EmailNotValidError
import re
from config import Config
from bson.objectid import ObjectId

app = Flask(__name__)
app.config.from_object(Config)

# Initialisation de PyMongo et Mail
mongo = PyMongo(app)
mail = Mail(app)

# Fonction de validation du mot de passe
def is_valid_password(password):
    if len(password) < 8:
        return False
    # Au moins 1 majuscule, 1 minuscule, 1 chiffre et 1 caractère spécial
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

# Route d'inscription
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    nom = data.get('nom')
    prenom = data.get('prenom')
    pays = data.get('pays')
    devise = data.get('devise')

    # Validation des champs
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError as e:
        return jsonify({'message': 'Adresse email invalide', 'error': str(e)}), 400

    if not nom or not prenom:
        return jsonify({'message': 'Le nom et le prénom ne doivent pas être vides'}), 400

    if not is_valid_password(password):
        return jsonify({'message': 'Le mot de passe ne respecte pas les critères requis'}), 400

    # Vérifier si l'email existe déjà
    if mongo.db.users.find_one({'email': email}):
        return jsonify({'message': 'Cette adresse email est déjà utilisée'}), 400

    # Enregistrer l'utilisateur dans la base de données
    user = {
        'email': email,
        'password': password,  # Pour un vrai projet, pensez à hasher le mot de passe !
        'nom': nom,
        'prenom': prenom,
        'pays': pays,
        'devise': devise,
        'etat': 'attente'  # État par défaut : en attente de validation
    }
    user_id = mongo.db.users.insert_one(user).inserted_id

    # Envoyer l'email de vérification
    token = str(user_id)  # Pour simplifier, nous utilisons l'ID de l'utilisateur comme token.
    verification_url = url_for('verify_email', token=token, _external=True)
    
    msg = Message("Vérifiez votre adresse email", recipients=[email])
    msg.body = f"Bonjour {prenom},\n\nCliquez sur le lien suivant pour vérifier votre email :\n{verification_url}"
    
    try:
        mail.send(msg)
    except Exception as e:
        # En cas d'erreur d'envoi, vous pouvez choisir de supprimer l'utilisateur ou enregistrer une erreur
        return jsonify({'message': 'Erreur lors de l\'envoi de l\'email de vérification', 'error': str(e)}), 500

    return jsonify({'message': 'Inscription réussie, veuillez vérifier votre email'}), 201

# Route de vérification de l'email
@app.route('/api/verify/<token>', methods=['GET'])
def verify_email(token):
    # Ici, token est l'ID de l'utilisateur
    user = mongo.db.users.find_one({'_id': ObjectId(token)})
    if not user:
        return jsonify({'message': 'Token invalide'}), 400

    # Mettre à jour l'état de l'utilisateur
    mongo.db.users.update_one({'_id': ObjectId(token)}, {'$set': {'etat': 'valide'}})
    return jsonify({'message': 'Email vérifié avec succès'}), 200

if __name__ == '__main__':
    app.run(debug=True)
