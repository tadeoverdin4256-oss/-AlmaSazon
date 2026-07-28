import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- CONFIGURACIÓN DE CONTRASEÑA ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "Abuelita2026": # <--- CAMBIA ESTA CONTRASEÑA SI QUIERES
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("🔒 Contraseña para entrar a AlmaSazón", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("🔒 Contraseña", type="password", on_change=password_entered, key="password")
        st.error("😡 Contraseña incorrecta. Intenta de nuevo")
        return False
    else:
        return True

# --- CONFIGURACIÓN DE GEMINI ---
@st.cache_resource
def get_model():
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")

model = get_model()

# --- INICIA LA APP ---
if check_password():
    st.set_page_config(page_title="AlmaSazón 👵🏽", layout="centered")
    st.title("AlmaSazón 👵🏽 Tu Abuela IA")
    st.write("Sube una foto de tu refri o dime qué tienes y te doy 3 recetas")

    # CEREBRO 1: ESCÁNER DE FOTOS
    st.header("1. Escáner de Fotos 📸")
    uploaded_file = st.file_uploader("Sube una foto de tus ingredientes", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Analizando...")
        if st.button("¿Qué puedo cocinar con esto?"):
            with st.spinner("AlmaSazón está viendo tu refri..."):
                prompt = "Eres una abuela mexicana. Mira esta foto de ingredientes y dame 3 recetas sencillas. Sé cariñosa."
                response = model.generate_content([prompt, image])
                st.write(response.text)

    # CEREBRO 2: QUÉ TENGO HOY
    st.header("2. ¿Qué tengo hoy? 🥕")
    ingredientes = st.text_input("Escribe lo que tienes, separado por comas:")
    if st.button("Dame 3 recetas"):
        if ingredientes:
            with st.spinner("Pensando recetas..."):
                prompt = f"Eres una abuela mexicana. Con estos ingredientes: {ingredientes}. Dame 3 recetas. Sé práctica y cariñosa."
                response = model.generate_content(prompt)
                st.write(response.text)

    # CEREBRO 3: MENÚ SEMANAL
    st.header("3. Menú Semanal 🗓️")
    if st.button("Generar menú para la semana"):
        with st.spinner("Planeando tu semana..."):
            prompt = "Eres una abuela mexicana. Crea un menú de 7 días, barato, sano y mexicano. Desayuno, comida y cena."
            response = model.generate_content(prompt)
            st.write(response.text)
