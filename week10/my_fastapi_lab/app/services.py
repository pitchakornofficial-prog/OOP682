# app/services.py
from __future__ import annotations

from typing import List

from fastapi import HTTPException
from .repositories import ITaskRepository
from .models import TaskCreate
from .models_orm import TaskORM


class TaskService:
    def __init__(self, repo: ITaskRepository):
        self.repo = repo

    def get_tasks(self) -> List[TaskORM]:
        return self.repo.list_tasks()

    def create_task(self, task_create: TaskCreate) -> TaskORM:
        # ✅ Validation Logic: ห้าม title ซ้ำ (ทำใน Service เท่านั้น)
        title = (task_create.title or "").strip()
        if not title:
            raise HTTPException(status_code=400, detail="Title is required")

        existing = self.repo.get_by_title(title)
        if existing:
            raise HTTPException(status_code=409, detail="Task title already exists")

        task = TaskORM(
            title=title,
            description=task_create.description,
            completed=task_create.completed,
        )
        return self.repo.create_task(task)

    def mark_complete(self, task_id: int) -> TaskORM | None:
        task = self.repo.get_task(task_id)
        if not task:
            return None
        task.completed = True
        return self.repo.update(task)
