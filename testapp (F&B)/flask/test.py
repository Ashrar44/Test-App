from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)  # Permits your mobile app to access the API

# Update with your MySQL credentials
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "user_db"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username, password = data.get('username'), data.get('password')
    hashed_pw = generate_password_hash(password)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
        return jsonify({"message": "User registered"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username, password = data.get('username'), data.get('password')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result and check_password_hash(result[0], password):
        return jsonify({"message": "Login successful", "username": username}), 200
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    # Listen on all network interfaces for mobile access
    app.run(host='0.0.0.0', port=5000, debug=True)