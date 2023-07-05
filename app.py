from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
api = Api(app)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
users_collection = db['users']

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = users_collection.find_one({'_id': ObjectId(user_id)}, {'_id': False})
            if user:
                return jsonify(user)
            else:
                return {'error': 'User not found'}, 404
        else:
            users = list(users_collection.find({}, {'_id': False}))
            return jsonify(users)

    def post(self):
        data = request.get_json()
        user_id = users_collection.insert_one(data).inserted_id
        return {'id': str(user_id)}, 201

    def put(self, user_id):
        data = request.get_json()
        result = users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': data})
        if result.modified_count > 0:
            return {'message': 'User updated successfully'}
        else:
            return {'error': 'User not found'}, 404

    def delete(self, user_id):
        result = users_collection.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count > 0:
            return {'message': 'User deleted successfully'}
        else:
            return {'error': 'User not found'}, 404

api.add_resource(UserResource, '/users', '/users/<user_id>')

if __name__ == '__main__':
    app.run(debug=True)
