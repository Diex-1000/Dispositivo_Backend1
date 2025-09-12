from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

# Cargar de .env las variables de entorno
load_dotenv()

# Crear una instanccia de MySQL
mysql = MySQL()

# Funcion para conectarme a la BD


def init_db(app):
    '''Configuramos la base de datos con la instancia de Flask'''
    app.config['MYSQL_HOST'] = os.getenv("DB_HOST")
    app.config['MYSQL_USER'] = os.getenv("DB_USER")
    app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASSWORD")
    app.config['MYSQL_DB'] = os.getenv("DB_NAME")
    app.config['MYSQL_PORT'] = int(os.getenv("DB_PORT"))
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET")

    # Inicializamos la conexion
    mysql.init_app(app)

# Definimos el cursor


def get_db_connection():
    '''Devuelve un cursor para interactuar con la bd'''
    try:
        connection = mysql.connection
        return connection.cursor()
    except Exception as e:
        raise RuntimeError(f"Error al conectar a la base de datos: {e}")