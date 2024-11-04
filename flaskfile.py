from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Database sederhana
def read_db():
    with open("db.json", "r") as file:
        return json.load(file)

def write_db(data):
    with open("db.json", "w") as file:
        json.dump(data, file)

# Read - Endpoint untuk mendapatkan semua data
@app.route('/items', methods=['GET'])
def get_items():
    data = read_db()
    return jsonify(data), 200

# Create - Endpoint untuk menambah item baru
@app.route('/items', methods=['POST'])
def create_item():
    data = read_db()
    new_item = request.json
    new_item["id"] = len(data) + 1
    data.append(new_item)
    write_db(data)
    return jsonify(new_item), 201

# Read - Endpoint untuk mendapatkan item berdasarkan ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    data = read_db()
    item = next((i for i in data if i["id"] == item_id), None)
    if item is not None:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

# Update - Endpoint untuk memperbarui item berdasarkan ID
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = read_db()
    item = next((i for i in data if i["id"] == item_id), None)
    if item is not None:
        update_data = request.json
        item.update(update_data)
        write_db(data)
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

# Delete - Endpoint untuk menghapus item berdasarkan ID
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    data = read_db()
    item = next((i for i in data if i["id"] == item_id), None)
    if item is not None:
        data.remove(item)
        write_db(data)
        return jsonify({"message": "Item deleted"}), 200
    return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
