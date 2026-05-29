import os
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_session import Session
import mysql.connector
from dotenv import load_dotenv
from email_service import sendMail

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY',
    'bella_piel_secret'
)

app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

CORS( app, supports_credentials=True, origins=[ "http://localhost:5173", "https://fronted-web.vercel.app" ] )

def obtener_conexion():

    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT', 3306),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

@app.route('/')

def inicio():

    return jsonify({
        'mensaje': 'Backend Bella Piel funcionando'
    })

@app.route('/login', methods=['POST'])

def login():

    data = request.json
    usuario = data.get('usuario')
    password = data.get('password')

    if not usuario or not password:
        return jsonify({
            'success': False,
            'mensaje': 'Todos los campos son obligatorios'
        }), 400

    if usuario == 'admin' and password == 'admin123':
        session['usuario'] = usuario
        session['logged_in'] = True

        return jsonify({
            'success': True,
            'usuario': usuario,
            'mensaje': 'Inicio de sesión correcto'
        })

    try:
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT *
            FROM usuarios
            WHERE usuario = %s
            AND password = %s
            """,
            (usuario, password)
        )

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['usuario'] = user['usuario']
            session['logged_in'] = True

            return jsonify({
                'success': True,
                'usuario': user['usuario'],
                'mensaje': 'Inicio de sesión correcto'
            })

        else:

            return jsonify({
                'success': False,
                'mensaje': 'Credenciales inválidas'
            }), 401

    except Exception as e:

        return jsonify({
            'success': False,
            'mensaje': f'Error de base de datos: {str(e)}'
        }), 500

@app.route('/session', methods=['GET'])

def verificar_sesion():

    if session.get('logged_in'):
        return jsonify({
            'logged_in': True,
            'usuario': session.get('usuario')
        })

    return jsonify({
        'logged_in': False
    }), 200

@app.route('/logout', methods=['POST'])

def logout():

    session.clear()

    return jsonify({
        'success': True,
        'mensaje': 'Sesión cerrada correctamente'
    })

@app.route('/pacientes', methods=['GET'])

def obtener_pacientes():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT
            nombre,
            telefono,
            correo
        FROM pacientes
        ORDER BY id DESC
        """
    )

    resultado = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(resultado)

@app.route('/pacientes', methods=['POST'])

def agregar_paciente():

    data = request.json

    if (
        not data.get('nombre') or
        not data.get('telefono') or
        not data.get('correo')
    ):

        return jsonify({
            'error': 'Todos los campos son obligatorios'
        }), 400

    nuevo_paciente = {
        'nombre': data['nombre'],
        'telefono': data['telefono'],
        'correo': data['correo']
    }

    try:

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO pacientes
            (nombre, telefono, correo)
            VALUES (%s, %s, %s)
            """,
            (
                nuevo_paciente['nombre'],
                nuevo_paciente['telefono'],
                nuevo_paciente['correo']
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'mensaje': 'Paciente agregada correctamente',
            'paciente': nuevo_paciente
        }), 201

    except mysql.connector.Error as err:

        return jsonify({
            'error': f'Error al guardar paciente: {err}'
        }), 400

@app.route('/citas', methods=['GET'])

def obtener_citas():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT
            id,
            paciente,
            telefono,
            area,
            DATE_FORMAT(fecha, '%Y-%m-%d') as fecha,
            TIME_FORMAT(hora, '%H:%i') as hora,
            estado
        FROM citas
        ORDER BY fecha ASC
        """
    )

    resultado = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(resultado)

@app.route('/citas', methods=['POST'])

def agregar_cita():

    data = request.json

    if (
        not data.get('paciente') or
        not data.get('telefono') or
        not data.get('area') or
        not data.get('fecha') or
        not data.get('hora')
    ):
        return jsonify({
            'error': 'Todos los campos son obligatorios'
        }), 400

    try:
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            INSERT INTO citas
            (paciente, telefono, area, fecha, hora, estado)
            VALUES (%s, %s, %s, %s, %s, 'Pendiente')
            """,
            (
                data['paciente'],
                data['telefono'],
                data['area'],
                data['fecha'],
                data['hora']
            )
        )

        conn.commit()
        cursor.execute(
            """
            SELECT correo
            FROM pacientes
            WHERE nombre = %s
            """,
            (data['paciente'],)
        )

        paciente = cursor.fetchone()

        if paciente and paciente['correo']:

            sendMail(
                paciente['correo'],
                data['paciente'],
                data['area'],
                data['fecha'],
                data['hora']
            )

        cursor.close()
        conn.close()

        return jsonify({
            'mensaje': 'Cita agregada correctamente'
        }), 201

    except Exception as e:

        return jsonify({
            'error': str(e)
        }), 500

@app.route('/citas/actualizar-estado', methods=['POST'])

def actualizar_estado():

    data = request.json
    id_cita = data.get('id')
    nuevo_estado = data.get('estado')

    if not id_cita or not nuevo_estado:
        return jsonify({
            'error': 'Id y Estado son requeridos'
        }), 400

    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE citas
        SET estado = %s
        WHERE id = %s
        """,
        (nuevo_estado, id_cita)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        'mensaje': 'Estado actualizado correctamente'
    })

@app.route('/citas/eliminar', methods=['POST'])

def eliminar_cita():

    data = request.json
    id_cita = data.get('id')

    if not id_cita:

        return jsonify({
            'error': 'Id de la cita requerido'
        }), 400

    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM citas
        WHERE id = %s
        """,
        (id_cita,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        'mensaje': 'Cita eliminada correctamente'
    })

if __name__ == '__main__':
    app.run(debug=True)
