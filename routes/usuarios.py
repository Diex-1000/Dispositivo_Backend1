from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from flask_bcrypt import Bcrypt, check_password_hash

from config.db import get_db_connection

import os
from dotenv import load_dotenv

jwt = JWTManager()

# Cargamos las variables de entorno
load_dotenv()

# Creamos el blueprint
usuarios_bp = Blueprint('usuarios', __name__)

# Inicializamos a Bcrypt
bcrypt = Bcrypt()


@usuarios_bp.route('/registrar', methods=['POST'])
def registrar():
    # Obtener del body los datos
    data = request.get_json()

    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    # Validacion
    if not nombre or not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    # Obtener el cursor de la bd
    cursor = get_db_connection()

    try:
        # Verificamos que el usuario no exista
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({"error": "Ese usuario ya existe"}), 400

        # Hacemos hash al password
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')

        # Insertar el registro del nuevo usuario en la base de datos
        cursor.execute('''INSERT INTO usuarios (nombre, email, password) values (%s,%s,%s)''',
               (nombre, email, hashed_password))


        # Guardadmos el nuevo registro
        cursor.connection.commit()
    except Exception as e:
        return jsonify({"error": f"Error al registrar al usuario: {str(e)}"}), 500
    finally:
        # Nos aseguramos de cerrar el cursor
        cursor.close()

    return jsonify({"mensaje": "EL usuario se creo correctamente"}), 200

@usuarios_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    cursor = get_db_connection()

    try:
        cursor.execute("SELECT id_usuario, password FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        user_id, hashed_password = user

        if not bcrypt.check_password_hash(hashed_password, password):
            return jsonify({"error": "Contraseña incorrecta"}), 401

      
        access_token = create_access_token(identity=user_id)
        return jsonify({"token": access_token}), 200

    except Exception as e:
        return jsonify({"error": f"Error al iniciar sesión: {str(e)}"}), 500
    finally:
        cursor.close()
    
