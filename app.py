from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
users_collection = db['users']

class UserResource:
    def get_all_users(self):
        users = list(users_collection.find({}, {'_id': False}))
        return jsonify(users)

    def get_user(self, user_id):
        user = users_collection.find_one({'_id': ObjectId(user_id)}, {'_id': False})
        if user:
            return jsonify(user)
        else:
            return jsonify({'error': 'User not found'}), 404

    def create_user(self):
        data = request.get_json()
        user_id = users_collection.insert_one(data).inserted_id
        return jsonify({'id': str(user_id)}), 201

    def update_user(self, user_id):
        data = request.get_json()
        result = users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': data})
        if result.modified_count > 0:
            return jsonify({'message': 'User updated successfully'})
        else:
            return jsonify({'error': 'User not found'}), 404

    def delete_user(self, user_id):
        result = users_collection.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count > 0:
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'error': 'User not found'}), 404

user_resource = UserResource()

app.route('/users', methods=['GET'])(user_resource.get_all_users)
app.route('/users/<user_id>', methods=['GET'])(user_resource.get_user)
app.route('/users', methods=['POST'])(user_resource.create_user)
app.route('/users/<user_id>', methods=['PUT'])(user_resource.update_user)
app.route('/users/<user_id>', methods=['DELETE'])(user_resource.delete_user)

if __name__ == '__main__':
    app.run(debug=True)
