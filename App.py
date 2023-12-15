import streamlit as st 
import requests
from langchain.retrievers import WikipediaRetriever
import os 
import dotenv

dotenv.load_dotenv()
token = os.environ["HUGGINGFACE_TOKEN"]
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {token}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

st.title("Wikipedia Chatbot")

retriever = WikipediaRetriever()

with st.form("my_fourm"):
    user_query = st.text_input("Please enter your query")
    submit = st.form_submit_button("Submit")

    if submit:
        docs = retriever.get_relevant_documents(user_query)
        prompt = f"<|system|> {docs[0]} <|user|> {user_query} <|assistant|>"
        output = query({
        	"inputs": prompt,
        })

        system_output = output[0]["generated_text"]
        ans = system_output[len(prompt):]
        st.write(ans)

