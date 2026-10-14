from __future__ import annotations

import json
import os
from pathlib import Path

from .models import Task, _now


def default_path() -> Path:
    base = os.environ.get("XDG_DATA_HOME") or (Path.home() / ".local" / "share")
    return Path(base) / "tasky" / "tasks.json"


class TaskNotFound(Exception):
    def __init__(self, task_id: int) -> None:
        super().__init__(f"task {task_id} not found")
        self.task_id = task_id


class Store:
    """JSON-backed task store. Reads and writes on every call for simplicity."""

    def __init__(self, path: str | os.PathLike | None = None) -> None:
        self.path = Path(path) if path is not None else default_path()

    def _load(self) -> list[Task]:
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [Task.from_dict(item) for item in raw]

    def _save(self, tasks: list[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [t.to_dict() for t in tasks]
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        tmp.replace(self.path)

    def _next_id(self, tasks: list[Task]) -> int:
        return max((t.id for t in tasks), default=0) + 1

    def add(self, title: str) -> Task:
        tasks = self._load()
        task = Task(id=self._next_id(tasks), title=title)
        tasks.append(task)
        self._save(tasks)
        return task

    def all(self, include_done: bool = True) -> list[Task]:
        tasks = self._load()
        if not include_done:
            tasks = [t for t in tasks if not t.done]
        return tasks

    def get(self, task_id: int) -> Task:
        for task in self._load():
            if task.id == task_id:
                return task
        raise TaskNotFound(task_id)

    def complete(self, task_id: int) -> Task:
        tasks = self._load()
        for task in tasks:
            if task.id == task_id:
                task.done = True
                task.done_at = _now()
                self._save(tasks)
                return task
        raise TaskNotFound(task_id)

    def remove(self, task_id: int) -> Task:
        tasks = self._load()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                removed = tasks.pop(i)
                self._save(tasks)
                return removed
        raise TaskNotFound(task_id)

    def clear_done(self) -> int:
        tasks = self._load()
        remaining = [t for t in tasks if not t.done]
        removed = len(tasks) - len(remaining)
        if removed:
            self._save(remaining)
        return removed
