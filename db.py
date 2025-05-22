import sqlite3
from colorama import Fore

# from db import conectar


def conectar():
    """
    Establece una conexión con la base de datos 'inventario.db'.

    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos si es exitosa.
        None: Si ocurre un error al conectar.
    """
    try:
        return sqlite3.connect("inventario.db")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error de conexión a la base de datos: {e}")
        return None


def crear_tabla():
    """
    Crea la tabla 'productos' en la base de datos 'inventario.db' si no existe.

    La tabla 'productos' se define con los siguientes campos:
        - id (INTEGER PRIMARY KEY AUTOINCREMENT): Identificador único del producto.
        - nombre (TEXT NOT NULL): Nombre del producto.
        - descripcion (TEXT): Descripción detallada del producto.
        - cantidad (INTEGER NOT NULL): Cantidad en stock del producto.
        - precio (REAL NOT NULL): Precio unitario del producto.
        - categoria (TEXT): Categoría a la que pertenece el producto.

    Side Effects:
        - Imprime mensajes en la consola sobre el estado de la operación.
        - Puede crear una tabla en la base de datos si esta no existe.
    """
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
