from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app import db, bcrypt
from app.models import User
from sqlalchemy.exc import IntegrityError


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Auth blueprint is working!"})


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    # --- Validation ---
    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters"}), 400

    if '@' not in email or '.' not in email:
        return jsonify({"error": "Invalid email format"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    # --- Check for existing user ---
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    # --- Hash password ---
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # --- Create user ---
    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        role='user'
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 409

    return jsonify({
        "message": "User registered successfully",
        "user": new_user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # --- Find user (allow login via username OR email) ---
    user = User.query.filter(
        (User.username == username) | (User.email == username.lower())
    ).first()

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    # --- Check password ---
    if not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid username or password"}), 401

    # --- Create JWT token, embedding role as a custom claim ---
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role, "username": user.username}
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user": user.to_dict()}), 200


@auth_bp.route('/admin-only', methods=['GET'])
@jwt_required()
def admin_only():
    claims = get_jwt()

    if claims.get('role') != 'admin':
        return jsonify({"error": "Admin access required"}), 403

    return jsonify({"message": "Welcome, admin! This is protected admin data."}), 200