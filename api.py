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

@app.route('/productos', methods=['GET'])
def obtener_productos():
    return jsonify(productos)

@app.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):

    for producto in productos:
        if producto["id"] == id:
            return jsonify(producto)

    return jsonify({"error": "Producto no encontrado"}), 404

@app.route('/productos', methods=['POST'])
def crear_producto():

    datos = request.get_json()

    if len(productos) > 0:
        nuevo_id = max(p["id"] for p in productos) + 1
    else:
        nuevo_id = 1

        nuevo_producto = {
        "id": nuevo_id,
        "nombre": datos["nombre"],
        "precio": datos["precio"],
        "cantidad": datos["cantidad"],
        "categoria": datos["categoria"]

    }

    productos.append(nuevo_producto)

    return jsonify(nuevo_producto), 201

@app.route('/productos/<int:id>', methods=['PUT'])
def modificar_producto(id):
    datos = request.get_json()

    for producto in productos:
        if producto["id"] == id:

            producto["nombre"] = datos.get("nombre", producto["nombre"])
            producto["precio"] = datos.get("precio", producto["precio"])
            producto["cantidad"] = datos.get("cantidad", producto["cantidad"])
            producto["categoria"] = datos.get("categoria", producto["categoria"])

            return jsonify(producto)
        
        return jsonify({"error": "Producto no encontrado"}), 404
    
@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    for producto in productos:
        if producto["id"] == id:
            productos.remove(producto)
            return jsonify({"mensaje": "Producto eliminado exitosamente"})
        
    return jsonify({"error": "Producto no encontrado"}), 404


if __name__ == '__main__':
    app.run(debug=True)