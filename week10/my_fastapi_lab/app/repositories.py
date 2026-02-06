# app/repositories.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.orm import Session
from .models_orm import TaskORM as Task


class ITaskRepository(ABC):
    @abstractmethod
    def list_tasks(self) -> List[Task]:
        ...

    @abstractmethod
    def get_task(self, task_id: int) -> Optional[Task]:
        ...

    @abstractmethod
    def create_task(self, task: Task) -> Task:
        ...

    @abstractmethod
    def update(self, task: Task) -> Task:
        ...

    # ✅ เพิ่มตามโจทย์: ใช้เช็กชื่อซ้ำ
    @abstractmethod
    def get_by_title(self, title: str) -> Optional[Task]:
        ...


class InMemoryTaskRepository(ITaskRepository):
    def __init__(self):
        self._data: List[Task] = []

    def list_tasks(self) -> List[Task]:
        return self._data

    def get_task(self, task_id: int) -> Optional[Task]:
        return next((t for t in self._data if t.id == task_id), None)

    def create_task(self, task: Task) -> Task:
        self._data.append(task)
        return task

    def update(self, task: Task) -> Task:
        for i, t in enumerate(self._data):
            if t.id == task.id:
                self._data[i] = task
                return task
        return task

    # ✅ Implement get_by_title
    def get_by_title(self, title: str) -> Optional[Task]:
        title_norm = title.strip().lower()
        return next((t for t in self._data if (t.title or "").strip().lower() == title_norm), None)


class SqlTaskRepository(ITaskRepository):
    def __init__(self, db: Session):
        self.db = db

    def list_tasks(self) -> List[Task]:
        return self.db.query(Task).all()

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def create_task(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    # ✅ Implement get_by_title
    def get_by_title(self, title: str) -> Optional[Task]:
        # เลือกเช็กแบบ exact match (ถ้าต้องการ ignore case ค่อยปรับด้วย func.lower)
        return self.db.query(Task).filter(Task.title == title).first()
