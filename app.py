from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
MEMORY_FILE = 'memory.json'

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_memory(data):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    memory = load_memory()
    if request.method == "POST":
        entry = request.form.get("entry", "")
        if entry:
            memory.append(entry)
            save_memory(memory)
    return render_template("index.html", memory=memory)

@app.route("/memory", methods=["GET", "POST"])
def memory():
    if request.method == "GET":
        return jsonify(load_memory())
    elif request.method == "POST":
        new_entry = request.json.get('entry')
        memory = load_memory()
        memory.append(new_entry)
        save_memory(memory)
        return jsonify({'status': 'success', 'entry_added': new_entry})

if __name__ == "__main__":
    app.run()
