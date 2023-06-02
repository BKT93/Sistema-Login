# SISTEMA DE INICIO DE SESIÓN
# --- Desarrollado con Streamlit
# --- Conexión a base de datos Sqlite3
# --- Librería bcrypt para realizar el encriptado
# --- Función para generar usuario/contraseña > "def insert_user(username, password):"
# --- Base de datos contenedora de Usuario + Hash
# --- En "def show_app():" incluiremos el código a mostrar si las credenciales son correctas


import bcrypt
import streamlit as st
import sqlite3

def main():
    if not is_authenticated():
        show_login()
    else:
        show_app()

def is_authenticated():
    return st.session_state.get("authenticated", False)


# Pantalla de Login
def show_login():
    st.title("Inicio de sesión")

    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            redirect_to_app()
        else:
            st.error("Nombre de usuario o contraseña incorrectos")

# Conexión con la base de datos donde se registran los Usuarios/Contraseñas (hashed)
def create_connection():
    conn = sqlite3.connect("D:/ussers.db") # Colocar ruta de la base de datos
    return conn

# Auntenticación de Usuario. Consulta a base de datos.
def authenticate(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT password FROM usuarios WHERE username = ?"
    cursor.execute(query, (username,))

    result = cursor.fetchone()

    if result:
        stored_password = result[0]  # Obtener la contraseña almacenada en la base de datos
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):  # Verificar la contraseña ingresada
            return True

    cursor.close()
    conn.close()

    return False

# Con esta función quitamos separamos el Inicio de sesión del resto de código
def redirect_to_app():
    st.experimental_set_query_params(authenticated="true")

def show_app():
    # --- Contenedora del código. Respetar identación
    pass

#Función para realizar el encriptado de las contraseñas
def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

# Función para la creación de nuevos usuarios/contraseñas
def insert_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password) #Llamamos la función para realizar el encriptado

    query = "INSERT INTO usuarios (username, password) VALUES (?, ?)"
    cursor.execute(query, (username, hashed_password))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":


# FUNCIÓN:
    #--- Función para insertar los Usuarios/Contraseñas dentro del Dataset
    #--- Guardar código + guardar cambios en base de dato o la función no impactará
    #--- Creado el usuario comentar la función para no generar mas usuarios y hash


    #insert_user("gvaldes", "129899")
    

    main()