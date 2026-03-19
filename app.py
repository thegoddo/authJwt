
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from bson import ObjectId
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

if __name__ == '__main__':
    app.run(debug=True)
