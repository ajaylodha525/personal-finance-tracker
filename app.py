from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import os

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

FILE = "finance_data.csv"

def init():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            csv.writer(f).writerow(["id","date","type","category","amount","note"])

def read():
    init()
    rows = []
    with open(FILE, newline="") as f:
        for r in csv.DictReader(f):
            r["amount"] = float(r["amount"])
            rows.append(r)
    return rows

def write(rows):
    with open(FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id","date","type","category","amount","note"])
        w.writeheader()
        w.writerows(rows)

@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/transactions", methods=["GET"])
def get_all():
    return jsonify(read())

@app.route("/transactions", methods=["POST"])
def add():
    d = request.json
    rows = read()
    new = {
        "id":       str(len(rows) + 1),
        "date":     d.get("date", ""),
        "type":     d["type"],
        "category": d["category"],
        "amount":   float(d["amount"]),
        "note":     d.get("note", "")
    }
    rows.append(new)
    write(rows)
    return jsonify(new), 201

@app.route("/transactions/<id>", methods=["DELETE"])
def delete(id):
    rows = [r for r in read() if r["id"] != id]
    write(rows)
    return jsonify({"ok": True})

if __name__ == "__main__":
    print("App chal raha hai → http://localhost:5000")
    app.run(debug=True)