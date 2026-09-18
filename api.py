from flask import Flask, jsonify

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

if __name__ == '__main__':
    app.run(debug=True)