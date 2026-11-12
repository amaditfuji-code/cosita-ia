import streamlit as st
from google import genai
from google.genai import types

# Configuración de la página
st.set_page_config(
    page_title="Cosita IA",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Cosita IA")
st.caption("Tu asistente personal inteligente creada por mí.")

# Cliente de Google GenAI (la clave se lee de secrets)
try:
    if "client" not in st.session_state:
        st.session_state.client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    client = st.session_state.client
except Exception:
    st.error("⚠️ No se detectó la API Key. Revisa los Secrets.")
    st.stop()

# Chat con personalidad (no gasta ninguna llamada al abrir la página)
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-3.8-flash",
        config=types.GenerateContentConfig(
            system_instruction=(
                "Te llamas Cosita IA. Eres un asistente virtual personal, "
                "amigable, cercano y servicial en español. Preséntate "
                "brevemente diciendo tu nombre la primera vez que el "
                "usuario hable."
            )
        ),
    )

# Mostrar los mensajes anteriores
for message in st.session_state.chat.get_history():
    texto = message.parts[0].text if message.parts else None
    if not texto:
        continue
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(texto)

# Caja de texto para los mensajes
if prompt := st.chat_input("Escribe lo que quieras preguntarle a Cosita IA..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            st.write_stream(
                chunk.text
                for chunk in st.session_state.chat.send_message_stream(prompt)
                if chunk.text
            )
    except Exception as e:
        st.error(f"Ocurrió un error al conectar con la IA: {e}")