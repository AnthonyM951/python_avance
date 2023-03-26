import unittest
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from projet import scrapping,intoMontgo

class TestScrapping(unittest.TestCase):
    def setUp(self):
        s = Service('./chromedriver.exe')
        options = ChromeOptions()
        options.add_argument("--headless")
        self.browser = ChromeDriver(service=s,options=options)
    
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
    
    def test_insert_many(self):
        intoMontgo(self.collection, self.data)
        self.assertEqual(self.collection.count_documents({}), len(self.data))
        for d in self.data:
            self.assertIsNotNone(self.collection.find_one(d))
    
    def tearDown(self):
        self.client.drop_database('test_db')

if __name__ == '__main__':
    unittest.main()
