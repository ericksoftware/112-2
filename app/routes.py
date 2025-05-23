from flask import Flask, render_template
import requests as pyrequests

BACKEND_URL = "http://127.0.0.1:5000/"  # Using root endpoint

app = Flask(__name__)

@app.get("/tasks")
def list_tasks():
    response = pyrequests.get(BACKEND_URL)
    if response.status_code == 200:
        backend_data = response.json()
        tasks = [
            {
                "id": item["id"],
                "name": item["name"],  # Keep original field name
                "summary": item["summary"],
                "description": item["description"]
            }
            for item in backend_data.get("task", [])
        ]
        return render_template("list.html", tasks=tasks)
    else:
        return render_template("error.html", error="Failed to fetch tasks"), 500

@app.get("/task/<int:id>")
def task(id):  # Changed function name to match endpoint
    response = pyrequests.get(f"http://127.0.0.1:5000/task/{id}/")
    if response.status_code == 200:
        task_data = response.json().get("task")
        return render_template("task_detail.html", task=task_data)
    else:
        return render_template("error.html", error="Task not found"), 404