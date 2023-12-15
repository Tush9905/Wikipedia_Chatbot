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
ans = "Welcome, Please ask your Query!"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input
if user_query := st.chat_input("Enter Your Query Here"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_query)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})
    docs = retriever.get_relevant_documents(user_query)
    if docs != []:
         prompt = f"<|im_start|>system {docs[0]} <|im_end|> <|im_start|>user {user_query} <|im_end|> <|im_start|>assistant"
         output = query({
         	"inputs": prompt,
         })

         system_output = output[0]["generated_text"]
         ans = system_output[len(prompt):]
    else:
         ans = "There is no info about it on Wikipedia as of now."

response = f"Assistant: {ans}"
# Display assistant response in chat message container
with st.chat_message("assistant"):
    st.markdown(response)
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})