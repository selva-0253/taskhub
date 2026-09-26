from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Task Hub API")

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None= None
    completed: bool=False

class TaskUpdate(BaseModel):
    title: str= Field(min_length=1, max_length=200)
    description: str | None= None
    completed: bool=False

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None= None
    completed: bool

tasks = []

@app.get("/")

def health_check():
    return {"status": "ok"}

@app.post("/tasks", response_model=TaskResponse, status_code=201)

def create_task(task: TaskCreate):
    new_task = {
        "id": len(tasks)+1,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
      }
    tasks.append(new_task)

    return new_task


@app.get("/tasks", response_model=list[TaskResponse])

def get_tasks():    
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(
        status_code=404, 
        detail="Task not found"
        )

@app.put("/tasks/{task_id}", response_model=TaskResponse)

def update_task(task_id: int, update_task: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = update_task.title
            task["description"] = update_task.description
            task["completed"] = update_task.completed
            return task
    raise HTTPException(
            status_code=404, 
            detail="Task not found"
        )

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return
    raise HTTPException(
            status_code=404, 
            detail="Task not found"
        )
    
      