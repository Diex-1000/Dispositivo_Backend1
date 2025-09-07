from flask import Flask
import os 
from dotenv import load_dotenv
from config.db import init_db, mysql
from routes.tareas import tareas_bp
from routes.usuarios import usuarios_bp, jwt

#Cargar las variables de entorno
load_dotenv()

#Funcion para crear la app
def create_app(): 

    #Instancia de la app
    app = Flask(__name__)
    jwt.init_app(app=app)

    #Configurar la DB
    init_db(app)

    #Registrar el blueprint
    app.register_blueprint(tareas_bp, url_prefix='/tareas')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')

    return app
# Crear la app 
app = create_app()

if __name__ == "__main__":
    #Obtener el puerto
    port = int(os.getenv("PORT",8080))

    #Corremos la app
    app.run(host="0.0.0.0", port=port, debug=True)