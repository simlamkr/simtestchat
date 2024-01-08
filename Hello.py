
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

# Initialize Gemini-Pro 
load_dotenv()
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key=GOOGLE_API_KEY)
#model = genai.GenerativeModel('gemini-pro')

model = genai.GenerativeModel(model_name = "gemini-pro")

# Gemini uses 'model' for assistant; Streamlit uses 'assistant'
def role_to_streamlit(role):
  if role == "model":
    return "assistant"
  else:
    return role

def run():
# Add a Gemini Chat history object to Streamlit session state
  if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history = [])

  if 'chat' not in st.session_state:
    st.session_state.chat = {}  # Initialize it to an empty dictionary

  #st.session_state.chat['history'] = ""  # Now you can safely set 'history'

  # Display Form Title
  st.title("Chat with Google Gemini-Pro!")

  #st.session_state.chat.history =""

  # Display chat messages from history above current input box
  for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

  # Accept user's next message, add to context, resubmit context to Gemini
  if prompt := st.chat_input("I possess a well of knowledge. What would you like to know?"):
    # Display user's last message
    st.chat_message("user").markdown(prompt)
    
    # Send user entry to Gemini and read the response
    response = st.session_state.chat.send_message(prompt) 
    
    # Display last 
    with st.chat_message("assistant"):
        st.markdown(response.text)

if __name__ == "__main__":
    run()

