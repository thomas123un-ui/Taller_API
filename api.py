from flask import Flask, jsonify, request

app = Flask(__name__)

productos = [
    {
        "id": 1,
        "nombre": "Teclado Mecánico",
        "precio": 45.99,
        "cantidad": 15,
        "categoria": "Periféricos"
    }
]

# Consultar Productos

@app.route('/productos', methods=['GET'])
def obtener_productos():
    return jsonify(productos)

@app.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):

    for producto in productos:
        if producto["id"] == id:
            return jsonify(producto)

    return jsonify({"error": "Producto no encontrado"}), 404

#Validacion De Datos

def validar_datos(datos, es_modificacion=False):
    if not request.is_json or not datos:
        return "Los datos deben recibirse en formato JSON."
        
    if not es_modificacion:
        campos_requeridos = ["nombre", "precio", "cantidad", "categoria"]
        for campo in campos_requeridos:
            if campo not in datos:
                return f"Falta el campo requerido: {campo}"

    if "nombre" in datos and not str(datos["nombre"]).strip():
        return "El nombre no puede estar vacío."
        
    if "precio" in datos and (not isinstance(datos["precio"], (int, float)) or datos["precio"] <= 0):
        return "El precio debe ser mayor que cero."
        
    if "cantidad" in datos and (not isinstance(datos["cantidad"], int) or datos["cantidad"] < 0):
        return "La cantidad no puede ser negativa."
        
    if "categoria" in datos and not str(datos["categoria"]).strip():
        return "La categoría no puede estar vacía."
        
    return None

#Crear Producto

@app.route('/productos', methods=['POST'])
def crear_producto():
    datos = request.get_json(silent=True)

    error = validar_datos(datos, es_modificacion=False)
    if error:
        return jsonify({"error": error}), 400
    
    nuevo_id = max(p["id"] for p in productos) + 1 if productos else 1
        
    nuevo_producto = {
        "id": nuevo_id,
        "nombre": datos["nombre"],
        "precio": datos["precio"],
        "cantidad": datos["cantidad"],
        "categoria": datos["categoria"]
    }
    
    productos.append(nuevo_producto)
    return jsonify(nuevo_producto), 201

#Modificar Producto

@app.route('/productos/<int:id>', methods=['PUT'])
def modificar_producto(id):
    datos = request.get_json(silent=True)
    
    error = validar_datos(datos, es_modificacion=True)
    if error:
        return jsonify({"error": error}), 400
    
    for producto in productos:
        if producto["id"] == id:
            producto["nombre"] = datos.get("nombre", producto["nombre"])
            producto["precio"] = datos.get("precio", producto["precio"])
            producto["cantidad"] = datos.get("cantidad", producto["cantidad"])
            producto["categoria"] = datos.get("categoria", producto["categoria"])
            
            return jsonify(producto)
            
    return jsonify({"error": "Producto no encontrado"}), 404
    
#Eliminar Producto

@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    for producto in productos:
        if producto["id"] == id:
            productos.remove(producto)
            return jsonify({"mensaje": "Producto eliminado exitosamente"})
        
    return jsonify({"error": "Producto no encontrado"}), 404

#Buscar Producto por Nombre

@app.route('/productos/buscar/<string:nombre>', methods=['GET'])
def buscar_producto_por_nombre(nombre):

    resultados = [p for p in productos if nombre.lower() in p["nombre"].lower()]
    return jsonify(resultados)

#Buscar Productos Bajo Stock

@app.route('/productos/bajo-stock', methods=['GET'])
def buscar_bajo_stock():

    resultados = [p for p in productos if p["cantidad"] <= 5]
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True, port=5001)