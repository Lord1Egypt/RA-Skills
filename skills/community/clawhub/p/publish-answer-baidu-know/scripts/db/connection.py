"""SQLite 连接与业务表迁移。"""

from __future__ import annotations

import sqlite3

from db.display_metadata import init_display_metadata
from db.timestamp_columns import (
    init_answer_publish_records_timestamp_maintenance,
    init_task_logs_timestamp_maintenance,
)
from util.runtime_paths import get_db_path


def get_conn() -> sqlite3.Connection:
    return sqlite3.connect(get_db_path())


def init_db() -> None:
    conn = get_conn()
    try:
        cur = conn.cursor()
        # 通用任务日志表
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS task_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_type TEXT NOT NULL,
                target_id TEXT,
                input_id TEXT,
                input_title TEXT,
                status TEXT NOT NULL,
                error_msg TEXT,
                result_summary TEXT,
                created_at INTEGER NOT NULL DEFAULT (unixepoch()),
                updated_at INTEGER NOT NULL DEFAULT (unixepoch())
            )
            """
        )
        # 百度知道回答发布记录表（REQUIREMENTS §5）
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_publish_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idempotency_key TEXT,
                account_id TEXT NOT NULL,
                question_url TEXT NOT NULL,
                answer_path TEXT NOT NULL,
                status TEXT NOT NULL,
                platform_message TEXT,
                published_at INTEGER,
                created_at INTEGER NOT NULL DEFAULT (unixepoch()),
                updated_at INTEGER NOT NULL DEFAULT (unixepoch())
            )
            """
        )
        # 幂等键唯一索引（同一 idempotency_key 只能产生一条记录）
        cur.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_answer_publish_idempotency
            ON answer_publish_records(idempotency_key)
            WHERE idempotency_key IS NOT NULL
            """
        )
        init_task_logs_timestamp_maintenance(cur)
        init_answer_publish_records_timestamp_maintenance(cur)
        init_display_metadata(cur)
        conn.commit()
    finally:
        conn.close()
