import sqlite3
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional


class StateStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    status TEXT,
                    payload TEXT,
                    result TEXT,
                    created_at REAL,
                    updated_at REAL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS workers (
                    worker_id TEXT PRIMARY KEY,
                    status TEXT,
                    last_heartbeat REAL,
                    metadata TEXT
                )
            """)

    def save_task(
        self, task_id: str, status: str, payload: Optional[Dict] = None, result: Optional[Dict] = None
    ):
        now = time.time()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO tasks
                   (task_id, status, payload, result, updated_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    task_id,
                    status,
                    json.dumps(payload) if payload else None,
                    json.dumps(result) if result else None,
                    now,
                ),
            )

    def get_task(self, task_id: str) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT task_id, status, payload, result FROM tasks WHERE task_id=?",
                (task_id,),
            )
            row = cur.fetchone()
            if row:
                return {
                    "task_id": row[0],
                    "status": row[1],
                    "payload": json.loads(row[2]) if row[2] else None,
                    "result": json.loads(row[3]) if row[3] else None,
                }
        return None

    def save_worker(self, worker_id: str, status: str, metadata: Optional[Dict] = None):
        now = time.time()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO workers
                   (worker_id, status, last_heartbeat, metadata)
                   VALUES (?, ?, ?, ?)""",
                (worker_id, status, now, json.dumps(metadata) if metadata else None),
            )

    def get_worker(self, worker_id: str) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT worker_id, status, last_heartbeat, metadata FROM workers WHERE worker_id=?",
                (worker_id,),
            )
            row = cur.fetchone()
            if row:
                return {
                    "worker_id": row[0],
                    "status": row[1],
                    "last_heartbeat": row[2],
                    "metadata": json.loads(row[3]) if row[3] else None,
                }
        return None
