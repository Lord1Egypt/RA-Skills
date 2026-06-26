"""Task management for memory-related TODOs."""

from __future__ import annotations

import hashlib
import time
import logging

logger = logging.getLogger(__name__)


class TaskManager:
    """Manages memory-related tasks (TODOs, reminders)."""

    def __init__(self, conn_getter, transaction_provider, cache_invalidator):
        """
        Args:
            conn_getter: Callable that returns a sqlite3.Connection
            transaction_provider: Context manager for transactions
            cache_invalidator: Callable to invalidate cache after writes
        """
        self._get_conn = conn_getter
        self._transaction = transaction_provider
        self._invalidate_cache = cache_invalidator

    @property
    def conn(self):
        return self._get_conn()

    def add_task(self, memory_id: str, title: str, assignee: str = "ai", deadline: int = None, topic_code: str = None) -> str:
        raw = f"{memory_id}_{title}_{time.time()}"
        task_id = "task_" + hashlib.sha256(raw.encode()).hexdigest()[:12]
        with self._transaction() as conn:
            conn.execute(
                """INSERT INTO tasks (task_id, memory_id, title, status, assignee, deadline, topic_code)
                   VALUES (?, ?, ?, 'pending', ?, ?, ?)""",
                (task_id, memory_id, title, assignee, deadline, topic_code),
            )
        self._invalidate_cache()
        return task_id

    def update_task_status(self, task_id: str, status: str) -> bool:
        valid = {"pending", "in_progress", "done", "overdue"}
        if status not in valid:
            raise ValueError(f"无效状态: {status}，可选: {valid}")

        now = int(time.time())
        params = [status, now]
        sql = "UPDATE tasks SET status = ?, updated_at = ?"
        if status == "done":
            sql += ", completed_at = ?"
            params.append(now)
        sql += " WHERE task_id = ?"
        params.append(task_id)

        with self._transaction() as conn:
            cur = conn.execute(sql, params)
        self._invalidate_cache()
        return cur.rowcount > 0

    def get_tasks(self, status: str = None, assignee: str = None, topic_code: str = None, overdue_only: bool = False, limit: int = 50) -> list[dict]:
        conditions = []
        params = []
        if status:
            conditions.append("t.status = ?")
            params.append(status)
        if assignee:
            conditions.append("t.assignee = ?")
            params.append(assignee)
        if topic_code:
            conditions.append("t.topic_code LIKE ?")
            params.append(topic_code + "%")
        if overdue_only:
            conditions.append("t.deadline < ? AND t.status NOT IN ('done', 'overdue')")
            params.append(int(time.time()))

        where = " AND ".join(conditions) if conditions else "1=1"

        rows = self.conn.execute(
            f"""SELECT t.*, m.content as memory_content
                FROM tasks t
                LEFT JOIN memories m ON t.memory_id = m.memory_id AND m.deleted=0
                WHERE {where}
                ORDER BY
                    CASE t.status
                        WHEN 'overdue' THEN 0
                        WHEN 'pending' THEN 1
                        WHEN 'in_progress' THEN 2
                        WHEN 'done' THEN 3
                    END,
                    t.created_at DESC
                LIMIT ?""",
            params + [limit],
        ).fetchall()
        return [dict(r) for r in rows]

    def check_overdue(self) -> list[dict]:
        now = int(time.time())
        with self._transaction() as conn:
            conn.execute(
                "UPDATE tasks SET status = 'overdue', updated_at = ? WHERE deadline < ? AND status IN ('pending', 'in_progress')",
                (now, now),
            )
        rows = self.conn.execute(
            "SELECT * FROM tasks WHERE status = 'overdue' AND deadline < ?",
            (now,),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_task_stats(self) -> dict:
        rows = self.conn.execute("SELECT status, COUNT(*) as cnt FROM tasks GROUP BY status").fetchall()
        stats = {r["status"]: r["cnt"] for r in rows}
        stats["total"] = sum(stats.values())
        return stats
