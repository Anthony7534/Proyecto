from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Simulación de base de datos en memoria
conversiones_db = []

@app.route('/')
def index():
    """Página principal del conversor"""
    return render_template('index.html')

@app.route('/api/conversiones/temperatura', methods=['POST'])
def convertir_temperatura():
    """Endpoint para guardar conversiones de temperatura"""
    try:
        data = request.get_json()
        
        # Validar datos recibidos
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400
            
        if 'resultado' not in data:
            return jsonify({'error': 'Falta el campo resultado'}), 400
            
        # Crear registro de conversión
        conversion = {
            'id': len(conversiones_db) + 1,
            'resultado': float(data['resultado']),
            'tipo': data.get('tipo', 'Celsius a Fahrenheit'),
            'registro': data.get('registro', datetime.now().isoformat())
        }
        
        # Guardar en "base de datos"
        conversiones_db.append(conversion)
        
        logger.info(f"Nueva conversión guardada: {conversion}")
        
        return jsonify(conversion), 201
        
    except ValueError as e:
        logger.error(f"Error de valor: {e}")
        return jsonify({'error': 'Valor numérico inválido'}), 400
    except Exception as e:
        logger.error(f"Error interno: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
