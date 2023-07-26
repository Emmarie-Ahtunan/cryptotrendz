import streamlit as st
import requests
import pymongo
from pymongo import MongoClient
from datetime import datetime

import pymongo
from urllib.parse import quote_plus


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://username:<password>@cluster0.romp4mt.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

username = quote_plus('<username>')
password = quote_plus('<password>')
cluster = '<clusterName>'
authSource = '<authSource>'
authMechanism = '<authMechanism>'

uri = 'mongodb+srv://' + username + ':' + password + '@' + cluster + '/?authSource=' + authSource + '&authMechanism=' + authMechanism

client = pymongo.MongoClient(uri)

result = client["<dbName"]["<collName>"].find()

# print results
for i in result:
    print(i)


# Function to connect to MongoDB
def connect_to_mongodb():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['cryptocurrency']
    collection = db['prices']
    return collection

# Streamlit web application
def main():
    st.title('Cryptocurrency Price Dashboard')

    # Connect to MongoDB
    collection = connect_to_mongodb()

    # Display data from MongoDB
    data = collection.find().sort('_id', pymongo.DESCENDING).limit(10)
    for entry in data:
        st.write(f"Timestamp: {entry['timestamp']}, Price: ${entry['price']}")


# Function to fetch cryptocurrency data from the API
def fetch_cryptocurrency_data():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {'ids': 'bitcoin', 'vs_currencies': 'usd'}
    response = requests.get(url, params=params)
    data = response.json()
    return data['bitcoin']['usd']

# Function to store cryptocurrency data in MongoDB
def store_in_mongodb(price):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['cryptocurrency']
    collection = db['prices']
    timestamp = datetime.now()
    document = {'timestamp': timestamp, 'price': price}
    collection.insert_one(document)
    client.close()

# Fetch data and store it in MongoDB every 5 minutes (for demonstration purposes)
while True:
    price = fetch_cryptocurrency_data()
    store_in_mongodb(price)
    time.sleep(300)  # Wait for 5 minutes

if __name__ == '__main__':
    main()