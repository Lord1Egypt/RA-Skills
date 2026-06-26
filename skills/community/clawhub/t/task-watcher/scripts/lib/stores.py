"""TaskStore interface and implementations for persisting callback tasks."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import json
import os
import fcntl
from datetime import datetime

try:
    from .models import CallbackTask
except ImportError:
    from models import CallbackTask


def task_state_hash(task_dict: Dict[str, Any]) -> str:
    """
    Compute a hash representing task state for change detection.

    Compatible with monitor_task_registry.py pattern.
    """
    fields = [
        str(task_dict.get("current_state", "")),
        str(task_dict.get("target_object_id", "")),
        str(task_dict.get("lookup_title", "")),
        str(task_dict.get("terminal", False)),
    ]
    return "|".join(fields)


class TaskStore(ABC):
    """
    Abstract interface for task persistence.

    All task storage implementations must conform to this interface.
    """

    @abstractmethod
    def create(self, task: CallbackTask) -> CallbackTask:
        """Create a new task record."""
        pass

    @abstractmethod
    def get(self, task_id: str) -> Optional[CallbackTask]:
        """Get task by ID."""
        pass

    @abstractmethod
    def list_active(self, limit: Optional[int] = None) -> List[CallbackTask]:
        """
        List all non-terminal active tasks.

        Args:
            limit: Maximum number of tasks to return (None = no limit)
        """
        pass

    @abstractmethod
    def list_by_owner(self, owner_agent: str, limit: Optional[int] = None) -> List[CallbackTask]:
        """List tasks by owner agent."""
        pass

    @abstractmethod
    def list_by_adapter(self, adapter: str, limit: Optional[int] = None) -> List[CallbackTask]:
        """List tasks by adapter type."""
        pass

    @abstractmethod
    def update(self, task_id: str, patch: Dict[str, Any]) -> Optional[CallbackTask]:
        """
        Update task fields.

        Args:
            task_id: Task ID to update
            patch: Dictionary of fields to update
        """
        pass

    @abstractmethod
    def close(self, task_id: str, final_state: str) -> Optional[CallbackTask]:
        """
        Close a task with final state.

        This marks the task as terminal.
        """
        pass

    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """Delete a task permanently."""
        pass

    @abstractmethod
    def count_active(self) -> int:
        """Count number of active (non-terminal) tasks."""
        pass


class JsonlTaskStore(TaskStore):
    """
    JSONL-based task storage.

    Each line is a JSON object representing a task.
    Latest version of a task is kept; older versions are marked as stale.

    File format: one JSON object per line
    - No array wrapper
    - Append-only for writes
    - Read loads all and returns latest version of each task
    """

    def __init__(self, file_path: str):
        """
        Initialize JSONL task store.

        Args:
            file_path: Path to the .jsonl file
        """
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Create file and directory if they don't exist."""
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.file_path):
            # Create empty file
            with open(self.file_path, 'w', encoding='utf-8') as f:
                pass

    def _lock_file(self, f, exclusive: bool = False) -> None:
        """Acquire file lock."""
        if exclusive:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        else:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)

    def _unlock_file(self, f) -> None:
        """Release file lock."""
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    def _read_all_tasks(self) -> Dict[str, CallbackTask]:
        """
        Read all tasks from file, keeping latest version of each.

        Returns:
            Dictionary mapping task_id -> latest CallbackTask
        """
        tasks = {}

        if not os.path.exists(self.file_path):
            return tasks

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self._lock_file(f, exclusive=False)
                try:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            task = CallbackTask.from_dict(data)
                            # Keep latest version by task_id
                            if task.task_id not in tasks:
                                tasks[task.task_id] = task
                            else:
                                # Compare updated_at timestamps
                                existing = tasks[task.task_id]
                                try:
                                    existing_time = datetime.fromisoformat(existing.updated_at)
                                    new_time = datetime.fromisoformat(task.updated_at)
                                    if new_time > existing_time:
                                        tasks[task.task_id] = task
                                except (ValueError, TypeError):
                                    # If timestamp parsing fails, keep newer line (later in file)
                                    tasks[task.task_id] = task
                        except (json.JSONDecodeError, KeyError, TypeError):
                            # Skip malformed lines
                            continue
                finally:
                    self._unlock_file(f)
        except FileNotFoundError:
            pass

        return tasks

    def _append_task(self, task: CallbackTask) -> None:
        """Append task to file."""
        with open(self.file_path, 'a', encoding='utf-8') as f:
            self._lock_file(f, exclusive=True)
            try:
                f.write(task.to_json() + '\n')
                f.flush()
                os.fsync(f.fileno())
            finally:
                self._unlock_file(f)

    def create(self, task: CallbackTask) -> CallbackTask:
        """
        Create a new task.

        Args:
            task: Task to create (task_id must be unique)

        Returns:
            The created task

        Raises:
            ValueError: If task_id already exists
        """
        tasks = self._read_all_tasks()
        if task.task_id in tasks:
            raise ValueError(f"Task with ID '{task.task_id}' already exists")

        task.created_at = datetime.now().isoformat()
        task.updated_at = task.created_at

        self._append_task(task)
        return task

    def get(self, task_id: str) -> Optional[CallbackTask]:
        """Get task by ID."""
        tasks = self._read_all_tasks()
        return tasks.get(task_id)

    def list_active(self, limit: Optional[int] = None) -> List[CallbackTask]:
        """List all non-terminal active tasks."""
        tasks = self._read_all_tasks()
        active = [t for t in tasks.values() if not t.terminal]

        # Sort by priority and creation time
        priority_order = {"critical": 0, "high": 1, "normal": 2, "low": 3}
        active.sort(key=lambda t: (
            priority_order.get(t.priority, 2),
            t.created_at
        ))

        if limit is not None:
            active = active[:limit]
        return active

    def list_by_owner(self, owner_agent: str, limit: Optional[int] = None) -> List[CallbackTask]:
        """List tasks by owner agent."""
        tasks = self._read_all_tasks()
        filtered = [t for t in tasks.values() if t.owner_agent == owner_agent and not t.terminal]
        filtered.sort(key=lambda t: t.created_at)
        if limit is not None:
            filtered = filtered[:limit]
        return filtered

    def list_by_adapter(self, adapter: str, limit: Optional[int] = None) -> List[CallbackTask]:
        """List tasks by adapter type."""
        tasks = self._read_all_tasks()
        filtered = [t for t in tasks.values() if t.adapter == adapter and not t.terminal]
        filtered.sort(key=lambda t: t.created_at)
        if limit is not None:
            filtered = filtered[:limit]
        return filtered

    def update(self, task_id: str, patch: Dict[str, Any]) -> Optional[CallbackTask]:
        """
        Update task fields.

        Args:
            task_id: Task ID to update
            patch: Dictionary of fields to update

        Returns:
            Updated task or None if not found
        """
        existing = self.get(task_id)
        if not existing:
            return None

        # Apply patch
        task_dict = existing.to_dict()
        for key, value in patch.items():
            if key in task_dict and key != 'task_id':  # Don't allow changing task_id
                task_dict[key] = value

        task_dict['updated_at'] = datetime.now().isoformat()

        updated_task = CallbackTask.from_dict(task_dict)
        self._append_task(updated_task)
        return updated_task

    def close(self, task_id: str, final_state: str) -> Optional[CallbackTask]:
        """
        Close a task with final state.

        Args:
            task_id: Task ID to close
            final_state: Final state to set

        Returns:
            Closed task or None if not found
        """
        patch = {
            'current_state': final_state,
            'terminal': True,
            'updated_at': datetime.now().isoformat()
        }
        return self.update(task_id, patch)

    def delete(self, task_id: str) -> bool:
        """
        Delete a task permanently.

        Note: In JSONL format, we mark for deletion and compact later.
        For now, we rewrite the file without the deleted task.

        Args:
            task_id: Task ID to delete

        Returns:
            True if deleted, False if not found
        """
        tasks = self._read_all_tasks()
        if task_id not in tasks:
            return False

        del tasks[task_id]

        # Rewrite file
        with open(self.file_path, 'w', encoding='utf-8') as f:
            self._lock_file(f, exclusive=True)
            try:
                for task in tasks.values():
                    f.write(task.to_json() + '\n')
                f.flush()
                os.fsync(f.fileno())
            finally:
                self._unlock_file(f)

        return True

    def count_active(self) -> int:
        """Count number of active (non-terminal) tasks."""
        tasks = self._read_all_tasks()
        return sum(1 for t in tasks.values() if not t.terminal)

    def compact(self) -> int:
        """
        Compact the JSONL file by removing stale entries.

        Returns:
            Number of lines removed
        """
        tasks = self._read_all_tasks()
        original_size = os.path.getsize(self.file_path) if os.path.exists(self.file_path) else 0

        # Rewrite file with only latest versions
        with open(self.file_path, 'w', encoding='utf-8') as f:
            self._lock_file(f, exclusive=True)
            try:
                for task in tasks.values():
                    f.write(task.to_json() + '\n')
                f.flush()
                os.fsync(f.fileno())
            finally:
                self._unlock_file(f)

        new_size = os.path.getsize(self.file_path) if os.path.exists(self.file_path) else 0
        # Approximate lines removed
        avg_line_size = original_size / (len(tasks) + 1) if tasks else 1
        lines_removed = int((original_size - new_size) / avg_line_size) if avg_line_size > 0 else 0

        return max(0, lines_removed)

    def get_raw(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get task as raw dict (for monitor script compatibility).

        Args:
            task_id: Task ID to retrieve

        Returns:
            Task dict or None if not found
        """
        task = self.get(task_id)
        if task:
            return task.to_dict()
        return None

    def update_raw(self, task_id: str, patch: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update task with raw dict and return updated dict.

        Compatible with monitor_task_registry.py update pattern.
        Automatically updates last_state_hash if relevant fields change.

        Args:
            task_id: Task ID to update
            patch: Dictionary of fields to update

        Returns:
            Updated task dict or None if not found
        """
        existing = self.get(task_id)
        if not existing:
            return None

        # Apply patch
        task_dict = existing.to_dict()
        for key, value in patch.items():
            if key in task_dict and key != 'task_id':
                task_dict[key] = value

        # Auto-update state hash if relevant fields changed
        if any(k in patch for k in ['current_state', 'target_object_id', 'lookup_title', 'terminal']):
            task_dict['last_state_hash'] = task_state_hash(task_dict)

        task_dict['updated_at'] = datetime.now().isoformat()

        updated_task = CallbackTask.from_dict(task_dict)
        self._append_task(updated_task)
        return task_dict

    def list_active_raw(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        List active tasks as raw dicts (for monitor script compatibility).

        Args:
            limit: Maximum number of tasks to return

        Returns:
            List of task dicts
        """
        tasks = self.list_active(limit=limit)
        return [t.to_dict() for t in tasks]
