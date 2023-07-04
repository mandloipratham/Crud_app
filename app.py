from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
port = 5000
client = MongoClient('mongodb://localhost:27017/')
db = client['users_db']
collection = db['users']



@app.route('/users', methods=['GET'])
def get_all_users():
    users = []
    for user in collection.find():
        users.append({
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
        })
    return jsonify(users)


@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    user = {
        'name': user_data['name'],
        'email': user_data['email'],
        'password': user_data['password']
    }
    result = collection.insert_one(user)
    return jsonify(str(result.inserted_id))


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = collection.find_one({'_id': ObjectId(user_id)})
    if user:
        return jsonify({
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
        })
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    updated_user = {
        'name': user_data['name'],
        'email': user_data['email'],
        'password': user_data['password']
    }
    result = collection.update_one({'_id': ObjectId(user_id)}, {'$set': updated_user})
    if result.modified_count > 0:
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = collection.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port ,debug=True)
    
