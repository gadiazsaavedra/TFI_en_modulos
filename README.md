# TFI_en_modulos
TFI de Com25006 separados en 4 archivos (db.py, inventario.db, menu.py y productos.py
# Sistema de Inventario en Python

Este proyecto es un sistema de inventario sencillo desarrollado en Python, que permite gestionar productos utilizando una base de datos SQLite. El sistema es modular y está compuesto por cuatro archivos principales:

- **db.py**: Maneja la conexión y la creación de la base de datos.
- **inventario.db**: Archivo de base de datos SQLite donde se almacenan los productos.
- **menu.py**: Proporciona la interfaz de menú principal para interactuar con el sistema.
- **productos.py**: Contiene todas las funciones relacionadas con la gestión de productos (agregar, mostrar, buscar, actualizar, eliminar y reportar bajo stock).

---

## Descripción de los archivos

### 1. db.py
Este archivo contiene funciones para conectar con la base de datos SQLite y crear la tabla de productos si no existe.  
- `conectar()`: Devuelve una conexión a la base de datos `inventario.db`.
- `crear_tabla()`: Crea la tabla `productos` con los campos necesarios (id, nombre, descripción, cantidad, precio, categoría).

### 2. inventario.db
Es el archivo de base de datos SQLite generado automáticamente al ejecutar el programa. Aquí se almacenan todos los productos y sus datos.

### 3. menu.py
Este archivo es el punto de entrada del programa.  
- Muestra un menú interactivo en la consola usando la librería `colorama` para mejorar la visualización.
- Permite al usuario seleccionar opciones para agregar, mostrar, buscar, actualizar, eliminar productos o ver un reporte de bajo stock.
- Llama a las funciones correspondientes de `productos.py` según la opción elegida.
- Al iniciar, se asegura de que la tabla de productos exista llamando a `crear_tabla()`.

### 4. productos.py
Contiene todas las funciones para gestionar los productos:
- **Agregar producto**: Solicita datos al usuario, valida la entrada y guarda el producto en la base de datos.
- **Mostrar productos**: Lista todos los productos almacenados.
- **Buscar producto**: Permite buscar por ID, nombre o categoría.
- **Actualizar producto**: Permite modificar los datos de un producto existente.
- **Eliminar producto**: Borra un producto por su ID.
- **Reporte bajo stock**: Muestra productos cuya cantidad está por debajo de un umbral definido.

Incluye validaciones para asegurar que los datos ingresados sean correctos y seguros.

---

## ¿Cómo funciona el sistema?

1. **Al iniciar el programa (`menu.py`)**, se crea la tabla de productos si no existe.
2. **El usuario ve un menú** con opciones para gestionar el inventario.
3. **Cada opción del menú** llama a una función de `productos.py` que interactúa con la base de datos a través de las funciones de `db.py`.
4. **Todos los datos** se almacenan y consultan en el archivo `inventario.db`.

---

## Requisitos

- Python 3.x
- Paquete `colorama` (instalar con `pip install colorama`)

---

## Ejecución

Para iniciar el sistema, ejecuta en la terminal:

```
python menu.py
```

---

## Notas

- El sistema es modular y fácil de mantener.
- Todos los mensajes y menús están en español.
- El archivo `inventario.db` se crea automáticamente en la primera ejecución.
