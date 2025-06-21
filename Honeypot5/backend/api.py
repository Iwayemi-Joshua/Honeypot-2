from flask import Flask, request, session, redirect, jsonify, send_from_directory
from functools import wraps
import json
from pathlib import Path
import threading
import time
from logger import log_attack  # Import log simulation
app = Flask(__name__)

app = Flask(__name__)
app.secret_key = "super_secret_key"

FRONTEND_PATH = "../frontend"
EVENTS_FILE = Path("../static/json/events.json")
ATTACK_LOGS_FILE = Path("attack_logs.json")
USERS_FILE = Path("users.json")

# Load or initialize users from file
if USERS_FILE.exists():
    with USERS_FILE.open("r") as f:
        USERS = json.load(f)
else:
    USERS = {"admin": "password123"}  # Default admin
    USERS_FILE.write_text(json.dumps(USERS))


# Save users back to file
def save_users():
    with USERS_FILE.open("w") as f:
        json.dump(USERS, f)


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect("/login.html")
        return f(*args, **kwargs)
    return decorated


@app.route("/")
@login_required
def home():
    return send_from_directory(FRONTEND_PATH, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_PATH, filename)


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if USERS.get(username) == password:
            session["user"] = username
            return jsonify({"message": "Login successful"}), 200
        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"message": "Server error", "error": str(e)}), 500


@app.route("/register", methods=["POST"])
def register():
    try:
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Username and password are required.", 400

        if username in USERS:
            return "Username already exists. Please choose another.", 409

        USERS[username] = password
        save_users()
        return redirect("/login.html")
    except Exception as e:
        return f"Registration failed: {str(e)}", 500


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"message": "Logged out"}), 200


@app.route("/events")
@login_required
def get_events():
    if ATTACK_LOGS_FILE.exists():
        with open(ATTACK_LOGS_FILE) as f:
            logs = json.load(f)
        return jsonify({"events": logs})
    return jsonify({"events": []})


@app.route("/api/clear-logs", methods=["POST"])
@login_required
def clear_logs():
    try:
        with open(ATTACK_LOGS_FILE, "w") as f:
            json.dump([], f)
        return {"status": "success"}, 200
    except Exception as e:
        return {"error": str(e)}, 500


# ===========================
# Simulate attacks in real time
# ===========================
def simulate_attacks():
    types = ["Port Scan", "SQL Injection", "Brute Force", "DDoS"]
    count = 0
    while True:
        ip = f"192.168.0.{count % 255}"
        attack = types[count % len(types)]
        log_attack(ip, attack)
        count += 1
        time.sleep(10)  # Add a log every 10 seconds


# Run simulation in background
threading.Thread(target=simulate_attacks, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True)
