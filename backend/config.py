# config.py
import os

class Config:
    # Configuration MongoDB
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/finbcc")

    # Configuration Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'  # Exemple : smtp.gmail.com
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")    # à définir dans vos variables d'environnement
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "no-reply@votre-domaine.com")
    
    # Autres configurations...
    SECRET_KEY = os.environ.get("SECRET_KEY", "votre_cle_secrete")
