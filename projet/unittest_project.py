import unittest
from unittest.mock import MagicMock
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from projet import scrapping, intoMontgo, streamlit_part
import pandas as pd
import streamlit as st


class TestScrapping(unittest.TestCase):
    def setUp(self):
        s = Service('./chromedriver.exe')
        options = ChromeOptions()
        options.add_argument("--headless")
        self.browser = ChromeDriver(service=s, options=options)

    def test_scrapping(self):
        array = scrapping(self.browser)
        self.assertIsInstance(array, list)
        self.assertGreater(len(array), 0)
        self.assertIsInstance(array[0], dict)
        self.assertIn('nom', array[0])
        self.assertIn('prix', array[0])
        self.assertIn('vendeur', array[0])
        self.assertIn('vendeur_type', array[0])

    def tearDown(self):
        self.browser.quit()


class TestInsertMany(unittest.TestCase):
    def setUp(self):
        CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.2"
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client['test_db']
        self.collection = self.db['test_collection']
        self.data = [{'nom': 'Peinture 1', 'prix': '10', 'vendeur': 'Vendeur 1', 'vendeur_type': 'pro'},
                     {'nom': 'Peinture 2', 'prix': '20', 'vendeur': 'Vendeur 2', 'vendeur_type': 'particulier'}]
        print(len(self.data))

    def test_insert_many(self):
        intoMontgo(self.collection, self.data)
        self.assertEqual(self.collection.count_documents({}), len(self.data))
        for d in self.data:
            self.assertIsNotNone(self.collection.find_one(d))

    def tearDown(self):
        self.client.drop_database('test_db')


def test_streamlit_part(self):
    # Mock data
    data = [{'nom': 'Tableau', 'prix': '50', 'vendeur': 'Alice', 'vendeur_type': 'Pro'},
            {'nom': 'Peinture', 'prix': '20', 'vendeur': 'Bob',
                'vendeur_type': 'Particulier'},
            {'nom': 'Cadre', 'prix': '30', 'vendeur': 'Alice', 'vendeur_type': 'Pro'}]
    df = pd.DataFrame(data)

    # Mock collection
    myCollection = MagicMock()
    myCollection.find.return_value = data

    # Patch the st functions used in streamlit_part
    with unittest.mock.patch.object(st, 'write') as mock_write, \
            unittest.mock.patch.object(st, 'pyplot') as mock_pyplot, \
            unittest.mock.patch.object(st, 'text_input') as mock_text_input, \
            unittest.mock.patch.object(st, 'selectbox') as mock_selectbox:

        # Set the input for the mocked functions
        mock_pyplot.subplots.return_value = (None, None)
        mock_text_input.return_value = 'Alice'
        mock_selectbox.return_value = 'Pro'

        # Call the function being tested
        streamlit_part(myCollection)

        # Check that the expected functions were called with the expected arguments
        mock_write.assert_any_call('My First Streamlit Web App')
        mock_write.assert_any_call(df)
        mock_pyplot.assert_called_with((None, None))
        mock_text_input.assert_called_with('Entrez le nom du vendeur :')
        mock_write.assert_any_call(df[df['vendeur'] == 'Alice'])
        mock_selectbox.assert_called_with(
            'Sélectionnez le type de vendeur :', ['Pro', 'Particulier'])
        mock_write.assert_any_call(df[df['vendeur_type'] == 'Pro'])


if __name__ == '__main__':
    unittest.main()
