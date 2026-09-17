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

if __name__ == '__main__':
    app.run(debug=True)