from colorama import Fore, Style, init
from db import crear_tabla
from productos import (
    registrar_producto,
    mostrar_productos,
    buscar_producto,
    actualizar_producto,
    eliminar_producto,
    reporte_bajo_stock,
)

init(autoreset=True)


def main():
    """
    Inicia el menú interactivo principal del sistema de gestión de inventario.

    Esta función crea la tabla de la base de datos si no existe y luego entra
    en un bucle que presenta al usuario opciones para gestionar productos:
    agregar, mostrar, buscar, actualizar, eliminar y generar reportes de stock.
    El usuario puede escribir 'volver' en cualquier solicitud de datos para
    regresar al menú principal. El bucle termina cuando el usuario elige salir.
    """
    crear_tabla()
    while True:
        print(Style.BRIGHT + Fore.BLUE + "\n===== Menú de Inventario =====")
        print(Fore.YELLOW + "1. Agregar producto")
        print(Fore.YELLOW + "2. Mostrar/Listar productos")
        print(Fore.YELLOW + "3. Buscar producto")
        print(Fore.YELLOW + "4. Actualizar producto por ID")
        print(Fore.YELLOW + "5. Eliminar producto por ID")
        print(Fore.YELLOW + "6. Reporte de bajo stock")
        print(Fore.YELLOW + "7. Salir")
        print(
            Fore.CYAN
            + "(En cualquier opción donde se solicite un dato, escriba 'volver' para regresar al menú)"
        )
        print(Style.RESET_ALL)
        opcion = input(Fore.CYAN + "Seleccione una opción (1-7): ").strip()

        if not opcion.isdigit() or not (1 <= int(opcion) <= 7):
            print(Fore.RED + "Opción no válida. Intente nuevamente.")
            continue

        try:
            if opcion == "1":
                registrar_producto()
            elif opcion == "2":
                mostrar_productos()
            elif opcion == "3":
                buscar_producto()
            elif opcion == "4":
                actualizar_producto()
            elif opcion == "5":
                eliminar_producto()
            elif opcion == "6":
                reporte_bajo_stock()
            elif opcion == "7":
                print(Fore.BLUE + "Saliendo del sistema. ¡Hasta luego!")
                break
            else:
                print(Fore.RED + "Opción no válida. Intente nuevamente.")
        except Exception as e:
            print(Fore.RED + f"Ocurrió un error: {e}")


if __name__ == "__main__":
    """
    Punto de entrada del programa. Llama a la función principal para iniciar el menú.
    """
    main()
