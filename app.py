from flask import Flask
import psycopg2

app = Flask(__name__)
VERSION = "3.0.0"  # ¡Cambiamos a la versión 3.0.0 de una vez!

@app.route("/")
def inicio():
    try:
        # Conexión a la base de datos de PostgreSQL
        conexion = psycopg2.connect(
            host="db",
            database="empresa",
            user="admin",
            password="admin123"
        )
        cursor = conexion.cursor()

        # Intentamos obtener los clientes de la tabla (Actividad 5)
        try:
            cursor.execute("SELECT id, nombre FROM clientes;")
            clientes = cursor.fetchall()
            lista_clientes = "".join([f"<li>ID: {c[0]} - Nombre: {c[1]}</li>" for c in clientes])
            if not lista_clientes:
                lista_clientes = "<li>No hay clientes registrados aún.</li>"
        except Exception:
            lista_clientes = "<li>La tabla 'clientes' no existe todavía. ¡Créala en pgAdmin!</li>"

        # Obtenemos la versión de PostgreSQL para el entregable
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        cursor.close()
        conexion.close()

        return f"""
        <h1>Aplicación Flask</h1>
        <h2>Versión {VERSION}</h2>
        <p style="color: green; font-weight: bold;">✔ Conexión exitosa a PostgreSQL</p>
        <p><strong>Versión DB:</strong> {db_version[0]}</p>
        <hr>
        <h3>Actividad 5: Lista de Clientes en la Base de Datos</h3>
        <ul>
            {lista_clientes}
        </ul>
        """
    except Exception as e:
        return f"<h1>Error de Conexión</h1><p>{str(e)}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)