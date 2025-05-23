from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")  # From .env
jwt = JWTManager(app)

# Mock user database
users = {
    "sanskriti@intern.com": {
        "password": "securepassword123",
        "role": "intern"
    }
}

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    if email not in users or users[email]["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=email)
    return jsonify({
        "access_token": access_token,
        "user": email,
        "role": users[email]["role"]
    })

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({
        "message": f"Hello {current_user}!",
        "secret_data": "For interns only: API_KEY_XYZ123"
    })

if __name__ == "__main__":
    app.run(debug=True)