import sqlite3
from colorama import Fore

# from db import conectar


def conectar():
    try:
        return sqlite3.connect("inventario.db")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error de conexión a la base de datos: {e}")
        return None


def crear_tabla():
    con = conectar()
    if con is not None:
        try:
            with con:
                cur = con.cursor()
                cur.execute(
                    """
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    categoria TEXT
)
"""
                )
            print(Fore.GREEN + "Base de datos y tabla listas para usar.")
        except sqlite3.Error as e:
            print(Fore.RED + f"Error al crear la tabla: {e}")
    else:
        print(Fore.RED + "No se pudo inicializar la base de datos.")
