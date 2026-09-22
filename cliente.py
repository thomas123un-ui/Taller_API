import requests

BASE_URL = "http://127.0.0.1:5001/productos"

def mostrar_menu():
    print("\n=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*")
    print("   MENÚ CLIENTE - INVENTARIO  ")
    print("=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*")
    print("1. Listar productos")
    print("2. Consultar producto por ID")
    print("3. Agregar producto")
    print("4. Modificar producto")
    print("5. Eliminar producto")
    print("6. Buscar producto por nombre")
    print("7. Consultar productos con bajo stock")
    print("8. Consultar productos por categoría")
    print("9. Consultar valor total del inventario") 
    print("10. Salir") 

def listar_productos():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            productos = response.json()
            print("\n--- LISTA DE PRODUCTOS ---")
            if not productos:
                print("No hay productos registrados.")
            for p in productos:
                print(f"ID: {p['id']} | Nombre: {p['nombre']} | Precio: ${p['precio']} | Cantidad: {p['cantidad']} | Categoría: {p['categoria']}")
        else:
            print(f"Error al listar: {response.json().get('error', 'Desconocido')}")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar con la API. Asegúrate de que api.py esté ejecutándose.")

def consultar_por_id():
    id_prod = input("Ingrese el ID del producto a consultar: ")
    try:
        response = requests.get(f"{BASE_URL}/{id_prod}")
        if response.status_code == 200:
            p = response.json()
            print("\n--- PRODUCTO ENCONTRADO ---")
            print(f"ID: {p['id']} | Nombre: {p['nombre']} | Precio: ${p['precio']} | Cantidad: {p['cantidad']} | Categoría: {p['categoria']}")
        elif response.status_code == 404:
            print(f"Error: {response.json().get('error', 'Producto no encontrado')}")
        else:
            print("Ocurrió un error inesperado.")
    except requests.exceptions.ConnectionError:
        print("Error de conexión con la API.")

def agregar_producto():
    print("\n--- AGREGAR NUEVO PRODUCTO ---")
    nombre = input("Nombre: ")
    try:
        precio = float(input("Precio: "))
        cantidad = int(input("Cantidad: "))
    except ValueError:
        print("Error: El precio debe ser un número y la cantidad un número entero.")
        return

    categoria = input("Categoría: ")

    data = {
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad,
        "categoria": categoria
    }

    try:
        response = requests.post(BASE_URL, json=data)
        if response.status_code == 201:
            p = response.json()
            print(f"¡Producto creado con éxito! (ID asignado: {p['id']})")
        elif response.status_code == 400:
            print(f"Error de validación: {response.json().get('error', 'Datos inválidos')}")
        else:
            print("Ocurrió un error inesperado.")
    except requests.exceptions.ConnectionError:
        print("Error de conexión con la API.")

def modificar_producto():
    id_prod = input("Ingrese el ID del producto que desea modificar: ")
    print("\n--- MODIFICAR PRODUCTO (Deje en blanco si no desea cambiar el campo) ---")
    
    nombre = input("Nuevo nombre: ")
    precio_str = input("Nuevo precio: ")
    cantidad_str = input("Nueva cantidad: ")
    categoria = input("Nueva categoría: ")

    data = {}
    if nombre.strip():
        data["nombre"] = nombre
    if precio_str.strip():
        try:
            data["precio"] = float(precio_str)
        except ValueError:
            print("Error: El precio debe ser un número.")
            return
    if cantidad_str.strip():
        try:
            data["cantidad"] = int(cantidad_str)
        except ValueError:
            print("Error: La cantidad debe ser un entero.")
            return
    if categoria.strip():
        data["categoria"] = categoria

    try:
        response = requests.put(f"{BASE_URL}/{id_prod}", json=data)
        if response.status_code == 200:
            print("¡Producto modificado exitosamente!")
        elif response.status_code == 404:
            print(f"Error: {response.json().get('error', 'Producto no encontrado')}")
        elif response.status_code == 400:
            print(f"Error de validación: {response.json().get('error', 'Datos inválidos')}")
        else:
            print("Ocurrió un error inesperado.")
    except requests.exceptions.ConnectionError:
        print("Error de conexión con la API.")

def eliminar_producto():
    id_prod = input("Ingrese el ID del producto a eliminar: ")
    try:
        response = requests.delete(f"{BASE_URL}/{id_prod}")
        if response.status_code == 200:
            print("Producto eliminado correctamente.")
        elif response.status_code == 404:
            print(f"Error: {response.json().get('error', 'Producto no encontrado')}")
        else:
            print("Ocurrió un error inesperado.")
    except requests.exceptions.ConnectionError:
        print("Error de conexión con la API.")

def buscar_por_nombre():
    nombre = input("Ingrese el nombre (o parte del nombre) a buscar: ")
    try:
        response = requests.get(f"{BASE_URL}/buscar/{nombre}")
        if response.status_code == 200:
            productos = response.json()
            print(f"\n--- RESULTADOS DE BÚSQUEDA ('{nombre}') ---")
            if not productos:
                print("No se encontraron productos con ese nombre.")
            for p in productos:
                print(f"ID: {p['id']} | Nombre: {p['nombre']} | Precio: ${p['precio']} | Cantidad: {p['cantidad']} | Categoría: {p['categoria']}")
        else:
            print("Error al realizar la búsqueda.")
    except requests.exceptions.ConnectionError:
        print("Error de conexión con la API.")

def consultar_bajo_stock():
    try:
        response = requests.get(f"{BASE_URL}/bajo-stock")
        if response.status_code == 200:
            productos = response.json()
            print("\n--- PRODUCTOS CON BAJO STOCK (<= 5) ---")
            if not productos:
                print("No hay productos con bajo stock.")
            for p in productos:
                print(f"ID: {p['id']} | Nombre: {p['nombre']} | Cantidad: {p['cantidad']} | Categoría: {p['categoria']}")
        else:
            print("Error al consultar bajo stock.")
    except requests.exceptions.ConnectionError:
        print("Error de conexión con la API.")

def consultar_por_categoria():
    categoria = input("Ingrese la categoría a buscar: ")
    try:
        response = requests.get(f"{BASE_URL}/categoria/{categoria}")
        if response.status_code == 200:
            productos = response.json()
            print(f"\n--- PRODUCTOS EN LA CATEGORÍA '{categoria.upper()}' ---")
            if not productos:
                print("No se encontraron productos en esta categoría.")
            for p in productos:
                print(f"ID: {p['id']} | Nombre: {p['nombre']} | Precio: ${p['precio']} | Cantidad: {p['cantidad']}")
        else:
            print("Error al consultar la categoría.")
    except requests.exceptions.ConnectionError:
        print("Error de conexión con la API.")

def consultar_valor_total():
    try:
        response = requests.get(f"{BASE_URL}/valor-total")
        if response.status_code == 200:
            data = response.json()
            print(f"\n--- VALOR TOTAL DEL INVENTARIO ---")
            print(f"El valor total es: ${data['valor_total']:.2f}")
        else:
            print("Error al calcular el valor total.")
    except requests.exceptions.ConnectionError:
        print("Error de conexión con la API.")

def main():
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-10): ")

        if opcion == "1":
            listar_productos()
        elif opcion == "2":
            consultar_por_id()
        elif opcion == "3":
            agregar_producto()
        elif opcion == "4":
            modificar_producto()
        elif opcion == "5":
            eliminar_producto()
        elif opcion == "6":
            buscar_por_nombre()
        elif opcion == "7":
            consultar_bajo_stock()
        elif opcion == "8":
            consultar_por_categoria()
        elif opcion == "9":
            consultar_valor_total()
        elif opcion == "10":
            print("\n¡Saliendo del sistema de inventario. Hasta luego! :/")
            break
        else:
            print("Opción inválida. Por favor, ingrese un número del 1 al 10.")
if __name__ == "__main__":
    main()