from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key_here"  

MESSAGES_FILE = "messages.json"
ADMIN_PASSWORD = "YuNa081522!" 


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    msg = data.get("message")

    if not msg:
        return jsonify(success=False, error="Empty message")

    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r") as f:
            messages = json.load(f)
    else:
        messages = []

    messages.append({
        "text": msg,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f)

    return jsonify(success=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()  
        password = data.get("password")
        if password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return jsonify(success=True)
        else:
            return jsonify(success=False)
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))


@app.route("/admin")
def admin():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r") as f:
            messages = json.load(f)
    else:
        messages = []

    return render_template("yuyu.html", messages=messages)

@app.route("/messages")
def get_messages():
    if not session.get("logged_in"):
        return jsonify([])  
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r") as f:
            messages = json.load(f)
    else:
        messages = []

    return jsonify(messages)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        message = request.form['message']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('messages.txt', 'a') as file:
            file.write(f"{timestamp}|||{message}\n")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
