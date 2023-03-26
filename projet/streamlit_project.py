import pandas as pd
from pymongo import MongoClient
import streamlit as st
from projet import create_Db
from matplotlib import pyplot as plt

mydb = create_Db()
myCollection = mydb['data_']

def streamlit_part(myCollection):

    df = pd.DataFrame(list(myCollection.find({}, {'_id': 0})))
    st.write('My First Streamlit Web App')
    st.write(df)
    fig, ax = plt.subplots()
    vendeur_type = df[['vendeur_type']].value_counts()
    print(vendeur_type)
    vendeur_type.plot(kind='pie')
    st.pyplot(fig)
    fig2, ax2 = fig, ax = plt.subplots()
    # Obtenir l'entrée de l'utilisateur pour le vendeur
    vendeur_input = st.text_input('Entrez le nom du vendeur :')
    if vendeur_input != '':
        # Filtrer le DataFrame en fonction du vendeur
        df_vendeur = df[df['vendeur'] == vendeur_input]

        # Afficher le DataFrame filtré dans Streamlit
        st.write(df_vendeur)
    # Obtenir l'entrée de l'utilisateur pour le type de vendeur
    vendeur_type_input = st.selectbox(
        'Sélectionnez le type de vendeur :', ['Pro', 'Particulier'])

    # Filtrer le DataFrame en fonction du type de vendeur
    df_vendeur_type = df[df['vendeur_type'] == vendeur_type_input]

    # Afficher le DataFrame filtré dans Streamlit
    st.write(df_vendeur_type)

streamlit_part(myCollection)