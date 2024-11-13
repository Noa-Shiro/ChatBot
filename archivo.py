import streamlit as st
from groq import Groq as gq

st.set_page_config(page_title = "Mi chat de IA", page_icon ="☀️")
st.title("Mi 1ra apk con Streamlit")
nombre = st.text_input("¿Cuál es tu nombre?")
if st.button("Bienvenida"):
    st.write(f"Hola {nombre} gracias por ingresar")

Modelo = ['llama3-8b-8192', 'llama3-70b-8192','mixtral-9x7b-32768 ']

def crear_usuario_groq():
    clave_secreta = st.secrets["clave_api"]
    return gq(api_key = clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo, #indica el modelo de la ia
        messages = [{"role": "user","content": mensajeDeEntrada}],
        stream = True
    ) #devuelve la respuesta de la IA
    

def inicializar_estado():
    if "mensaje" not in st.session_state:
        st.session_state.mensaje = [] #historial vacio

def configurar_pagina():
    st.title("Mi chat de IA")
    st.sidebar.title("Configuración")
    elegirModelo = st.sidebar.selectbox(
        "Elegí un modelo", #titulo
        Modelo, #opciones
        index = 0 #valor defecto
    )
    return elegirModelo

def actualizar_historial(rol, contenido, avatar):
    #agrega datos a la lista el append()
    st.session_state.mensaje.append(
        {"role": rol , "content": contenido, "avatar": avatar}
        #      usuario             mensajes            icono
    )

def mostrar_historial(): #sector del chat de web
    for mensaje in st.session_state.mensaje:
        with st.chat_message(mensaje["role"], avatar = mensaje ["avatar"]):
            st.markdown(mensaje["content"])
            

def area_chat():
    contenedorDelChat = st.container(height=400, border = True)
    with contenedorDelChat : mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = "" #variable vacia
    for frase in chat_completo:
        if frase.choices[0].delta.content: #el [0].delta.content se encargan de separar info
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa #se lee cuando termina el for

def main():
    #funciones del chatbot
    modelo = configurar_pagina() 
    clienteUsuario = crear_usuario_groq() #conecta a la Api a través de un usuario
    inicializar_estado() #llama al historial vacio
    area_chat() #pone en la web el contenedor del chat

    mensaje = st.chat_input("Escríba su mensaje...")

    if mensaje:
        actualizar_historial("user", mensaje, "😊") #muestra el mensaje del usuario
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🕶️")
                st.rerun() #actualizar
        #borrar lo demas

if __name__ == "__main__":
    main() #una función principal y siempre se invoca
    