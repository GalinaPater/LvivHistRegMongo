import streamlit as st
import pymongo

def create_client():
    username = st.secrets["connection"]["username"]
    password = st.secrets["connection"]["password"]
    cluster_name = st.secrets["connection"]["cluster_name"]
    uri = "mongodb+srv://" + username + ":" + password + "@" + cluster_name + ".mongodb.net/?retryWrites=true&w=majority"

    client = pymongo.MongoClient(uri)
    return client
    
def use_collection(client):
    db = client.ArcLviv
    collection = db.HistReg
    return collection