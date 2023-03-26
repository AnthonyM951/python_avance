# python_avance

Ce repository contient plusieurs scripts Python pour effectuer du web scraping et afficher les données collectées sur une application Streamlit.

# Prérequis
Python 3.7 ou supérieur
pip
Les bibliothèques Python suivantes : pandas, pymongo, selenium, matplotlib et streamlit.

# Installation
Clonez ce repository ou téléchargez-le sous forme de fichier zip.
Ouvrez un terminal et accédez au répertoire contenant les fichiers téléchargés.

# Les dfférents scripts
## script_1_scraping.py
Ce script utilise la bibliothèque Selenium pour effectuer du web scraping sur le site eBay.fr. Il récupère le nom, le prix, le vendeur et le type de vendeur de chaque produit de la première page de résultats de recherche pour une recherche spécifiée (ici, "peinture"). Les données sont stockées dans une liste de dictionnaires, puis insérées dans une base de données MongoDB.

## streamlit_project.py
Ce script utilise la bibliothèque Streamlit pour afficher les données stockées dans la base de données MongoDB dans un tableau. Il permet également de filtrer les données selon le nom du vendeur et le type de vendeur (professionnel ou particulier), ainsi que de générer des graphiques à partir des données.

# Tests unitaires
Ils se trouvent dans le fichier unittest_project.py

## class TestScrapping
Cette classe contient des tests unitaires pour la fonction scrapping.

## class TestInsertMany
Cette classe contient des tests unitaires pour la fonction streamlit_part.

## test_streamlit_part
Cette fonction contient des tests unitaires pour la fonction intoMontgo qui insère les données dans la base de données MongoDB.

# Utilisation
Exécutez le script projet.py pour collecter des données à partir du site eBay.fr et les stocker dans la base de données MongoDB.
Exécutez le streamlit_project.py pour afficher les données stockées dans le tableau et filtrer les données selon vos besoins.
(Optionnel) Exécutez les scripts de test (unittest_project.py) pour vous assurer que les fonctions fonctionnent correctement.

# Auteur
Ce projet a été réalisé par Anthony dans le cadre d'un cours de programmation.
