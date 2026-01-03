# server/app.py
from flask import Flask, request, jsonify, session, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, User  # Make sure models.py has User model
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "supersecretkey")

CORS(app, supports_credentials=True)
migrate = Migrate(app, db)
db.init_app(app)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    session["user_id"] = user.id
    return jsonify(user.to_dict()), 200


@app.route("/logout", methods=["DELETE"])
def logout():
    session.pop("user_id", None)
    return "", 204


@app.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")
    if not user_id:
        return "", 401

    user = User.query.get(user_id)
    if not user:
        return "", 401

    return jsonify(user.to_dict()), 200

# -------------------
if __name__ == "__main__":
    app.run(port=5555, debug=True)
