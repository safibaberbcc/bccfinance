@echo off
echo Création de l'arborescence du projet...

REM Création des dossiers principaux
mkdir mon-projet
cd mon-projet

REM Création du dossier frontend
mkdir frontend
cd frontend
mkdir public
mkdir public\images
echo. > public\favicon.ico
echo. > public\index.html
mkdir src
mkdir src\assets
echo. > src\assets\styles.css
mkdir src\components
mkdir src\pages
mkdir src\services
echo. > src\App.js
echo. > src\index.js
echo. > package.json
echo. > README.md
cd ..

REM Création du dossier backend
mkdir backend
cd backend
mkdir src
mkdir src\controllers
mkdir src\models
mkdir src\routes
mkdir src\services
mkdir src\utils
echo. > src\app.js
echo. > src\server.js
mkdir config
echo. > package.json
echo. > README.md
cd ..

REM Création des fichiers globaux
echo. > .gitignore
echo. > README.md
echo. > docker-compose.yml

echo Arborescence créée avec succès !
pause