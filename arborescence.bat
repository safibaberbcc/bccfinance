@echo off
echo Création de l'arborescence du projet...

REM Création des dossiers principaux
mkdir finance-app
cd finance-app

REM Création du dossier frontend
mkdir frontend
cd frontend
npx create-react-app finance-app-frontend
cd finance-app-frontend
npm install axios
cd ..\..

REM Création du dossier backend
mkdir backend
cd backend
mkdir app
cd app
mkdir controllers
mkdir models
mkdir routes
mkdir utils
echo. > __init__.py
echo. > main.py
cd ..
echo. > requirements.txt
echo. > .env
cd ..

REM Création des fichiers globaux
echo. > .gitignore
echo. > README.md

echo Arborescence créée avec succès !
pause