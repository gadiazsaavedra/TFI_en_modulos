from colorama import Fore
from db import conectar
import re
import sqlite3


def es_texto_valido(texto, max_len=50):
    """
    Valida que el texto solo contenga caracteres permitidos y no exceda la longitud máxima.
    Args:
        texto (str): Texto a validar.
        max_len (int): Longitud máxima permitida.
    Returns:
        bool: True si es válido, False en caso contrario.
    """
    return bool(re.match(r"^[\w\sáéíóúÁÉÍÓÚüÜñÑ.,-]{1," + str(max_len) + "}$", texto))


def input_con_volver(mensaje):
    """
    Solicita un input al usuario y permite cancelar la operación escribiendo 'volver'.
    Args:
        mensaje (str): Mensaje a mostrar al usuario.
    Returns:
        str or None: Valor ingresado o None si el usuario escribe 'volver'.
    """
    valor = input(mensaje).strip()
    if valor.lower() == "volver":
        return None
    return valor


# Función para registrar un nuevo producto
def registrar_producto():
    """
    Solicita los datos de un nuevo producto, los valida y los registra en la base de datos.
    Permite cancelar la operación escribiendo 'volver' en cualquier campo.
    """
    print(Fore.CYAN + "\n--- Registrar Nuevo Producto ---")
    # Validar nombre no vacío y longitud/carácteres
    while True:
        nombre = input_con_volver("Nombre: ")
        if nombre is None:
            print(Fore.BLUE + "Registro cancelado. Volviendo al menú principal.")
            return
        if not nombre:
            print(Fore.RED + "El nombre no puede estar vacío.")
        elif not es_texto_valido(nombre, 50):
            print(
                Fore.RED
                + "El nombre contiene caracteres no permitidos o es demasiado largo (máx 50)."
            )
        else:
            break
    # Validar descripción no vacía y longitud/carácteres
    while True:
        descripcion = input_con_volver("Descripción: ")
        if descripcion is None:
            print(Fore.BLUE + "Registro cancelado. Volviendo al menú principal.")
            return
        if not descripcion:
            print(Fore.RED + "La descripción no puede estar vacía.")
        elif not es_texto_valido(descripcion, 100):
            print(
                Fore.RED
                + "La descripción contiene caracteres no permitidos o es demasiado larga (máx 100)."
            )
        else:
            break
    # Validar cantidad (no permitir valores negativos)
    while True:
        cantidad = input_con_volver("Cantidad: ")
        if cantidad is None:
            print(Fore.BLUE + "Registro cancelado. Volviendo al menú principal.")
            return
        if cantidad.isdigit() and int(cantidad) >= 0:
            cantidad = int(cantidad)
            break
        print(Fore.RED + "Cantidad inválida. Debe ser un número entero no negativo.")
    # Validar precio no negativo
    while True:
        precio = input_con_volver("Precio: ")
        if precio is None:
            print(Fore.BLUE + "Registro cancelado. Volviendo al menú principal.")
            return
        try:
            precio = float(precio)
            if precio < 0:
                print(Fore.RED + "El precio no puede ser negativo.")
            else:
                break
        except ValueError:
            print(Fore.RED + "Precio inválido. Debe ser un número.")
    # Validar categoría no vacía y longitud/carácteres
    while True:
        categoria = input_con_volver("Categoría: ")
        if categoria is None:
            print(Fore.BLUE + "Registro cancelado. Volviendo al menú principal.")
            return
        if not categoria:
            print(Fore.RED + "La categoría no puede estar vacía.")
        elif not es_texto_valido(categoria, 30):
            print(
                Fore.RED
                + "La categoría contiene caracteres no permitidos o es demasiado larga (máx 30)."
            )
        else:
            break
    con = conectar()
    if con is None:
        return
    try:
        with con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
                (nombre, descripcion, cantidad, precio, categoria),
            )
            print(Fore.GREEN + "Producto registrado exitosamente.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al registrar producto: {e}")


# Función para mostrar todos los productos
def mostrar_productos():
    """
    Muestra todos los productos registrados en la base de datos.
    Si no hay productos, informa al usuario.
    """
    print(Fore.CYAN + "\n--- Lista de Productos ---")
    con = conectar()
    if con is None:
        return
    try:
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM productos")
            productos = cur.fetchall()
            if productos:
                for p in productos:
                    print(
                        Fore.YELLOW
                        + f"ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}"
                    )
            else:
                print(Fore.RED + "No hay productos registrados.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al mostrar productos: {e}")


# Función para buscar productos por ID, nombre o categoría
def buscar_producto():
    """
    Permite buscar productos por ID, nombre o categoría.
    Solicita el criterio de búsqueda y muestra los resultados encontrados.
    """
    print(Fore.CYAN + "\n--- Buscar Producto ---")
    print("1. Buscar por ID")
    print("2. Buscar por nombre")
    print("3. Buscar por categoría")
    opcion_busqueda = input("Seleccione una opción de búsqueda (1-3): ").strip()

    con = conectar()
    if con is None:
        return
    try:
        with con:
            cur = con.cursor()
            if opcion_busqueda == "1":
                id_buscar = input("Ingrese el ID del producto a buscar: ").strip()
                if not id_buscar.isdigit():
                    print(Fore.RED + "ID inválido.")
                    return
                cur.execute("SELECT * FROM productos WHERE id = ?", (int(id_buscar),))
                p = cur.fetchone()
                if p:
                    print(
                        Fore.YELLOW
                        + f"ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}"
                    )
                else:
                    print(Fore.RED + "No se encontró un producto con ese ID.")

            elif opcion_busqueda == "2":
                nombre_buscar = input(
                    "Ingrese el nombre (o parte) del producto a buscar: "
                ).strip()
                if not nombre_buscar:
                    print(Fore.RED + "Debe ingresar un nombre.")
                    return
                cur.execute(
                    "SELECT * FROM productos WHERE LOWER(nombre) LIKE ?",
                    ("%" + nombre_buscar.lower() + "%",),
                )
                productos = cur.fetchall()
                if productos:
                    print(Fore.CYAN + "\n--- Resultados de la búsqueda por nombre ---")
                    for p in productos:
                        print(
                            Fore.YELLOW
                            + f"ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}"
                        )
                else:
                    print(Fore.RED + "No se encontraron productos con ese nombre.")

            elif opcion_busqueda == "3":
                categoria_buscar = input(
                    "Ingrese la categoría (o parte) a buscar: "
                ).strip()
                if not categoria_buscar:
                    print(Fore.RED + "Debe ingresar una categoría.")
                    return
                cur.execute(
                    "SELECT * FROM productos WHERE LOWER(categoria) LIKE ?",
                    ("%" + categoria_buscar.lower() + "%",),
                )
                productos = cur.fetchall()
                if productos:
                    print(
                        Fore.CYAN + "\n--- Resultados de la búsqueda por categoría ---"
                    )
                    for p in productos:
                        print(
                            Fore.YELLOW
                            + f"ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}"
                        )
                else:
                    print(Fore.RED + "No se encontraron productos en esa categoría.")
            else:
                print(Fore.RED + "Opción de búsqueda no válida.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al buscar productos: {e}")


# Función para actualizar un producto por ID
def actualizar_producto():
    """
    Permite actualizar los datos de un producto existente por su ID.
    Solicita los nuevos valores y valida cada campo antes de actualizar.
    """
    print(Fore.CYAN + "\n--- Actualizar Producto ---")
    id_actualizar = input("Ingrese el ID del producto a actualizar: ").strip()
    if not id_actualizar.isdigit():
        print(Fore.RED + "ID inválido.")
        return
    con = conectar()
    if con is None:
        return
    try:
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM productos WHERE id = ?", (int(id_actualizar),))
            p = cur.fetchone()
            if not p:
                print(Fore.RED + "No se encontró un producto con ese ID.")
                return
            print(
                Fore.YELLOW
                + f"Producto actual: Nombre: {p[1]}, Descripción: {p[2]}, Cantidad: {p[3]}, Precio: {p[4]}, Categoría: {p[5]}"
            )
            # Validar nombre no vacío y longitud/carácteres
            while True:
                nombre = input("Nuevo nombre (Enter para mantener): ").strip()
                if nombre == "":
                    nombre = p[1]
                if not nombre:
                    print(Fore.RED + "El nombre no puede estar vacío.")
                elif not es_texto_valido(nombre, 50):
                    print(
                        Fore.RED
                        + "El nombre contiene caracteres no permitidos o es demasiado largo (máx 50)."
                    )
                else:
                    break
            # Validar descripción no vacía y longitud/carácteres
            while True:
                descripcion = input("Nueva descripción (Enter para mantener): ").strip()
                if descripcion == "":
                    descripcion = p[2]
                if not descripcion:
                    print(Fore.RED + "La descripción no puede estar vacía.")
                elif not es_texto_valido(descripcion, 100):
                    print(
                        Fore.RED
                        + "La descripción contiene caracteres no permitidos o es demasiado larga (máx 100)."
                    )
                else:
                    break
            # Validación para cantidad (no permitir valores negativos)
            while True:
                cantidad = input("Nueva cantidad (Enter para mantener): ").strip()
                if cantidad == "":
                    cantidad = p[3]
                    break
                elif cantidad.isdigit() and int(cantidad) >= 0:
                    cantidad = int(cantidad)
                    break
                else:
                    print(
                        Fore.RED
                        + "Cantidad inválida. Debe ser un número entero no negativo."
                    )
            # Validación para precio no negativo
            while True:
                precio = input("Nuevo precio (Enter para mantener): ").strip()
                if precio == "":
                    precio = p[4]
                    break
                try:
                    precio = float(precio)
                    if precio < 0:
                        print(Fore.RED + "El precio no puede ser negativo.")
                    else:
                        break
                except ValueError:
                    print(Fore.RED + "Precio inválido. Debe ser un número.")
            # Validar categoría no vacía y longitud/carácteres
            while True:
                categoria = input("Nueva categoría (Enter para mantener): ").strip()
                if categoria == "":
                    categoria = p[5]
                if not categoria:
                    print(Fore.RED + "La categoría no puede estar vacía.")
                elif not es_texto_valido(categoria, 30):
                    print(
                        Fore.RED
                        + "La categoría contiene caracteres no permitidos o es demasiado larga (máx 30)."
                    )
                else:
                    break
            cur.execute(
                "UPDATE productos SET nombre=?, descripcion=?, cantidad=?, precio=?, categoria=? WHERE id=?",
                (nombre, descripcion, cantidad, precio, categoria, int(id_actualizar)),
            )
            print(Fore.GREEN + "Producto actualizado exitosamente.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al actualizar producto: {e}")


# Función para eliminar un producto por ID
def eliminar_producto():
    """
    Elimina un producto de la base de datos por su ID, previa confirmación del usuario.
    """
    print(Fore.CYAN + "\n--- Eliminar Producto ---")
    id_eliminar = input("Ingrese el ID del producto a eliminar: ").strip()
    if not id_eliminar.isdigit():
        print(Fore.RED + "ID inválido.")
        return
    con = conectar()
    if con is None:
        return
    try:
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM productos WHERE id = ?", (int(id_eliminar),))
            p = cur.fetchone()
            if not p:
                print(Fore.RED + "No se encontró un producto con ese ID.")
                return
            print(
                Fore.YELLOW
                + f"¿Está seguro que desea eliminar el producto?\nID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}"
            )
            confirm = (
                input(Fore.RED + "Escriba 'SI' para confirmar la eliminación: ")
                .strip()
                .upper()
            )
            if confirm != "SI":
                print(Fore.BLUE + "Eliminación cancelada.")
                return
            cur.execute("DELETE FROM productos WHERE id = ?", (int(id_eliminar),))
            if cur.rowcount:
                print(Fore.GREEN + "Producto eliminado exitosamente.")
            else:
                print(Fore.RED + "No se encontró un producto con ese ID.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al eliminar producto: {e}")


# Función para mostrar productos con bajo stock
def reporte_bajo_stock():
    """
    Muestra un reporte de productos cuyo stock es igual o menor al valor indicado por el usuario.
    """
    print(Fore.CYAN + "\n--- Reporte de Bajo Stock ---")
    limite = input("Mostrar productos con cantidad igual o menor a: ").strip()
    if not limite.isdigit():
        print(Fore.RED + "Límite inválido.")
        return
    con = conectar()
    if con is None:
        return
    try:
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM productos WHERE cantidad <= ?", (int(limite),))
            productos = cur.fetchall()
            if productos:
                for p in productos:
                    print(Fore.YELLOW + f"ID: {p[0]}, Nombre: {p[1]}, Cantidad: {p[3]}")
            else:
                print(Fore.RED + "No hay productos con bajo stock.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al generar el reporte: {e}")


# Fin de funciones
