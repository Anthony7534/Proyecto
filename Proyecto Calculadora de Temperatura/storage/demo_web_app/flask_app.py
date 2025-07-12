from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_cors import CORS
from datetime import datetime
import os
import logging
import requests

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'semestral'
CORS(app)  # Habilitar CORS para todas las rutas

# Simulación de base de datos en memoria
conversiones_db = []

@app.route('/')
def index():
    """Página principal del conversor"""
    return render_template('conver.html')

@app.route('/api/conversiones', methods=['GET'])
def obtener_conversiones():
    """Obtener todas las conversiones"""
    return jsonify({
        'conversiones': conversiones_db,
        'total': len(conversiones_db)
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de salud para verificar que la API funciona"""
    return jsonify({
        'status': 'OK',
        'message': 'API funcionando correctamente',
        'timestamp': datetime.now().isoformat(),
        'conversiones_guardadas': len(conversiones_db)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500
    
 #Render de la página de login
@app.route('/login', methods=['GET'])
def loginp():
    return render_template('index.html')
        #username = request.form['username']
        #password = request.form['passsword']
        #if username in users and users [username] == password:
            #session['username'] = username 
            #return redirect(url_for('conver'))
        #else:
            #flash('Credenciales erroneas')
            
@app.route('/api/login', methods=['POST'])
def login():
    url = 'http://172.30.0.20/api/user'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    
    try:
        response = requests.get(url, headers)

        return jsonify({
            'status': 'OK',
            'isSuccess': True,
            'message': 'login ok',
            'timestamp': datetime.now().isoformat()
        }), 200

    except requests.exceptions.RequestException as e:
        print("Excepción de red:", e)
        return jsonify({
            'status': 'ERROR',
            'isSuccess': False,
            'message': 'No se pudo contactar con el servidor de usuarios',
            'timestamp': datetime.now().isoformat()
        }), 500
        
@app.route('/api/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
