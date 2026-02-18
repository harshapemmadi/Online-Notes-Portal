from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize database
def init_db():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        subject TEXT,
                        content TEXT,
                        uploadedBy TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/notes/upload', methods=['POST'])
def upload_note():
    data = request.json
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (subject, content, uploadedBy) VALUES (?, ?, ?)",
                   (data['subject'], data['content'], data['uploadedBy']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Note uploaded successfully!"})

@app.route('/api/notes/get', methods=['GET'])
def get_notes():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT subject, content, uploadedBy FROM notes")
    notes = cursor.fetchall()
    conn.close()
    return jsonify([{"subject": n[0], "content": n[1], "uploadedBy": n[2]} for n in notes])

if __name__ == '__main__':
    app.run(port=5000, debug=True)