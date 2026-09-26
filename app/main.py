from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task Hub API")

class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool=False

tasks = []

@app.get("/")

def health_check():
    return {"status": "ok"}

@app.post("/tasks", status_code=201)

def create_task(task: TaskCreate):
    new_task = {
        "id": len(tasks)+1,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
      }
    tasks.append(new_task)

    return new_task


@app.get("/tasks")

def get_tasks():    
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(
        status_code=404, 
        detail="Task not found"
        )


