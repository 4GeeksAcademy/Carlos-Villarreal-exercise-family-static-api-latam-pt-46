"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

Jack = {
    "first_name": "Jack",
    "age": "23",
    "lucky_numbers": [2, 17, 23]
}

Janet = {
    "first_name": "Janet",
    "age": "28",
    "lucky_numbers": [9, 16, 26]
}

Jill = {
    "firs_name": "Jill",
    "age": "19",
    "lucky_numbers": [10, 17, 29]
}

jackson_family.add_member(Jack)
jackson_family.add_member(Janet)
jackson_family.add_member(Jill)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_list_family():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/members', methods=['POST'])
def post_member():
    member = request.json
    print("añadido", member)
    jackson_family.add_member(member)
    return member, 200

@app.route('/members/<int:id>', methods=['GET'])
def get_only_member(id):
    member = jackson_family.get_member(id)
    if member is None:
        return jsonify({"Error": "Miembro no encontrado"}), 404
    return jsonify(member)

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_only_member(id):
    member = jackson_family.delete_member(id)
    if member is None:
        return jsonify({"Error": "Miembro no encontrado"}), 404
    return jsonify({"done": True, "Delete_member": member}), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)