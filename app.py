from flask import Flask, render_template, request, jsonify, session
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or "clave_super_secreta"
# Apuntamos directo al archivo que acabamos de arreglar
DB_PATH = "keystore.db"

# ---------- Crear BD si no existe ----------
def inicializar_bd():
    if not os.path.exists("database"):
        os.makedirs("database")

    if not os.path.exists(DB_PATH):
        print("⚙ Creando base de datos...")
        conn = sqlite3.connect(DB_PATH)
        with open("database/schema.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.close()
        print("✅ Base creada correctamente.")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Rutas ----------
@app.route("/")
def index():
    conn = get_db()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()
    return render_template("index.html", productos=productos)

@app.route("/agregar", methods=["POST"])
def agregar():
    data = request.json
    producto_id = data.get("id")
    if "carrito" not in session:
        session["carrito"] = []
    session["carrito"].append(producto_id)
    session.modified = True
    return jsonify({"status": "ok"})

@app.route("/carrito")
def ver_carrito():
    if "carrito" not in session or len(session["carrito"]) == 0:
        return jsonify([])
    ids = tuple(session["carrito"])
    conn = get_db()
    query = f"SELECT * FROM productos WHERE id IN ({','.join('?' * len(ids))})"
    productos = conn.execute(query, ids).fetchall()
    conn.close()
    return jsonify([dict(p) for p in productos])

@app.route("/comprar", methods=["POST"])
def comprar():
    datos = request.json
    nombre = datos.get("nombre")
    correo = datos.get("correo")
    metodo = datos.get("metodo")
    conn = get_db()
    conn.execute(
        "INSERT INTO ventas (nombre, correo, metodo) VALUES (?, ?, ?)",
        (nombre, correo, metodo),
    )
    conn.commit()
    conn.close()
    session.pop("carrito", None)
    return jsonify({"status": "compra_exitosa"})

# ---------- Login y Registro (CON BASE DE DATOS) ----------

@app.route("/login", methods=["POST"])
def login():
    datos = request.json
    usuario = datos.get("usuario")
    password = datos.get("password")
    
    conn = get_db()
    # Buscamos si existe un usuario con ese nombre y contraseña
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", 
        (usuario, password)
    ).fetchone()
    conn.close()
    
    if user:
        # ¡Encontrado! Guardamos la sesión
        session["usuario"] = user["username"]
        # Opcional: Guardar también el nombre real para mostrarlo
        session["nombre_real"] = user["nombre"] 
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error", "msg": "Usuario o contraseña incorrectos"})

@app.route("/register", methods=["POST"])
def register():
    datos = request.json
    usuario = datos.get("usuario")
    password = datos.get("password")
    nombre = datos.get("nombre")
    correo = datos.get("correo")
    telefono = datos.get("telefono")
    direccion = datos.get("direccion")
    
    conn = get_db()
    try:
        # Intentamos guardar en la base de datos
        conn.execute(
            """INSERT INTO users (username, password, nombre, correo, telefono, direccion) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (usuario, password, nombre, correo, telefono, direccion)
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "ok"})
        
    except sqlite3.IntegrityError:
        # Esto pasa si el 'username' ya existe (porque pusimos UNIQUE en la base de datos)
        conn.close()
        return jsonify({"status": "error", "msg": "El nombre de usuario ya está ocupado"})
    except Exception as e:
        conn.close()
        return jsonify({"status": "error", "msg": f"Error al registrar: {e}"})

# ---------- Inicialización ----------
if __name__ == "__main__":
    inicializar_bd()
    app.run(host="0.0.0.0", port=5000, debug=True)