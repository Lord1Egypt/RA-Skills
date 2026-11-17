from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


@app.post("/notes")
def add_note():
    db = sqlite3.connect("notes.db")
    db.execute("create table if not exists notes (body text)")
    db.execute("insert into notes (body) values (?)", (request.json["body"],))
    db.commit()
    return jsonify(ok=True)
