# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from .models import Task, TaskCreate
from .repositories import SqlTaskRepository
from .services import TaskService
from .database import get_db, engine, Base

app = FastAPI()

# สร้างตารางใน DB ตอนเริ่มรัน
Base.metadata.create_all(bind=engine)


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    repo = SqlTaskRepository(db)
    return TaskService(repo)


@app.get("/tasks", response_model=List[Task])
def read_tasks(service: TaskService = Depends(get_task_service)):
    return service.get_tasks()


@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate, service: TaskService = Depends(get_task_service)):
    return service.create_task(task)


# ✅ Route ใหม่ตามโจทย์: Mark as Complete
@app.put("/tasks/{id}/complete", response_model=Task)
def mark_task_complete(id: int, service: TaskService = Depends(get_task_service)):
    updated = service.mark_complete(id)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated
