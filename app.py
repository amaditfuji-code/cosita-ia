import os
import streamlit as st
from google import genai

# Configuración de la página web de la app
st.set_page_config(
    page_title="Cosita IA", 
    page_icon="🤖", 
    layout="centered"
)

st.title("🤖 Cosita IA")
st.caption("Tu asistente personal inteligente creada por mi.")

# Configurar el cliente de Google GenAI
try:
    if "client" not in st.session_state:
        st.session_state.client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    client = st.session_state.client
except Exception as e:
    st.error("⚠️ No se detectó la API Key. Asegúrate de configurarla en tu sistema.")
    st.stop()

# Mantener el historial del chat en la sesión de Streamlit
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(model="gemini-3.8-flash")
    
    # Personalidad y nombre oficial
    st.session_state.chat.send_message(
        "Te llamas Cosita IA. Eres un asistente virtual personal, amigable, cercano y servicial en español. "
        "Preséntate brevemente diciendo tu nombre cuando el usuario comience a hablar por primera vez."
    )

# Mostrar los mensajes anteriores en la pantalla del chat
for message in st.session_state.chat.get_history():
    if message.parts[0].text.startswith("Te llamas Cosita IA"):
        continue
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Caja de texto para tus mensajes
if prompt := st.chat_input("Escribe lo que quieras preguntarle a Cosita IA..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Ocurrió un error al conectar con la IA: {e}")