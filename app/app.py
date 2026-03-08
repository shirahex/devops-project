from flask import Flask, jsonify, request
import os
import datetime

app = Flask(__name__)

# In-memory store for demo purposes
tasks = [
    {"id": 1, "title": "Setup Kubernetes", "done": False},
    {"id": 2, "title": "Configure CI/CD", "done": True},
]

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "DevOps API v2 - Auto Depoloyed",
        "version": APP_VERSION,
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "version": APP_VERSION}), 200

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks, "count": len(tasks)})

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400
    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "done": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json()
    task["done"] = data.get("done", task["done"])
    task["title"] = data.get("title", task["title"])
    return jsonify(task)

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": f"Task {task_id} deleted"}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
