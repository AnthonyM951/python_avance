import time
from matplotlib import pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from pymongo import MongoClient
import streamlit as st


def scrapping(browser):
    s = Service('./chromedriver.exe')

    browser = ChromeDriver(service=s)
    dataset = {}
    browser.maximize_window()
    browser.get(
        'https://www.ebay.fr/sch/i.html?_nkw=peinture&rt=nc&_dcat=128482&_sacat=-1&vbn_id=7006312012&Type=Huile&mag=1&_fsrp=1')
    time.sleep(2)
    tableaux = browser.find_elements(
        By.CLASS_NAME, 's-item__pl-on-bottom')
    i = 2
    array = []
    for tableau in tableaux:
        if i < 60:
            if '<span class="LIGHT_HIGHLIGHT">Nouvelle annonce</span>' in tableau.find_element(
                    'xpath', f'//*[@id="srp-river-results"]/ul/li[{i}]/div/div[2]/a/div/span').get_attribute('innerHTML'):
                dataset['nom'] = tableau.find_element(
                    'xpath', f'//*[@id="srp-river-results"]/ul/li[{i}]/div/div[2]/a/div/span').get_attribute('innerHTML').split('<span class="LIGHT_HIGHLIGHT">Nouvelle annonce</span>')[1]
            else:
                dataset['nom'] = tableau.find_element(
                    'xpath', f'//*[@id="srp-river-results"]/ul/li[{i}]/div/div[2]/a/div/span').get_attribute('innerHTML')
            dataset['prix'] = tableau.find_element(
                By.CLASS_NAME, 's-item__price').text.split(' EUR')[0]
            dataset['vendeur'] = tableau.find_elements(
                'xpath', '//span[@class="s-item__seller-info-text"]')[i].text.split(' (')[0]
            if len(tableau.find_elements(By.CLASS_NAME, 's-item__subtitle')) < 2:
                dataset['vendeur_type'] = tableau.find_element(
                    By.CLASS_NAME, 's-item__subtitle').text
            else:
                dataset['vendeur_type'] = tableau.find_elements(
                    By.CLASS_NAME, 's-item__subtitle')[1].text
            i += 1

        array.append(dataset)
        dataset = {}
    time.sleep(3)
    print(array)

    return array


def create_Db():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.2"
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)
    return client['End_projet']


# mydb = create_Db()
# myCollection = mydb['data_']

mydb = create_Db()
myCollection = mydb['data_']
def intoMontgo():
    
    data = scrapping()
    # print(data)

    #     if d != data[0]:
    #         myCollection.insert_one(d)
    myCollection.insert_many(data)


def streamlit_part():

    df = pd.DataFrame(list(myCollection.find({}, {'_id': 0})))
    st.write('My First Streamlit Web App')
    st.write(df)
    fig, ax = plt.subplots()
    vendeur_type = df[['vendeur_type']].value_counts()
    print(vendeur_type)
    vendeur_type.plot(kind='pie')
    # st.bar_chart(chart_data['grp_sanguin'].value_counts())

    # man = chart_data[['grp_sanguin', 'sex']].loc[chart_data['sex'] == 'M']
    # fig = plt.subplot()
    # fig1 = pd.crosstab(df['grp_sanguin'], df['sex']).plot.bar()
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


# streamlit_part()
# print(data[1])
