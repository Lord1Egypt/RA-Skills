"""task_logs 表读写模板。

通用业务日志仓储：记录每次任务执行的 task_type / target / input / 状态 / 结果摘要。
不假设任何特定业务（发布、对账、审核等都可复用）。
"""

from __future__ import annotations

from typing import Any, List, Optional, Tuple

from db.connection import get_conn, init_db


def save_task_log(
    task_type: str,
    target_id: Optional[str] = None,
    input_id: Optional[str] = None,
    input_title: Optional[str] = None,
    status: str = "success",
    error_msg: Optional[str] = None,
    result_summary: Optional[str] = None,
) -> int:
    init_db()
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO task_logs
                (task_type, target_id, input_id, input_title, status, error_msg, result_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (task_type, target_id, input_id, input_title or "", status, error_msg, result_summary),
        )
        new_id = int(cur.lastrowid)
        conn.commit()
    finally:
        conn.close()
    return new_id


def list_task_logs(
    limit: int,
    status: Optional[str] = None,
    task_type: Optional[str] = None,
    target_id: Optional[str] = None,
) -> List[Tuple[Any, ...]]:
    init_db()
    conn = get_conn()
    try:
        cur = conn.cursor()
        sql = (
            "SELECT id, task_type, target_id, input_id, input_title, status, error_msg, result_summary, "
            "created_at, updated_at FROM task_logs WHERE 1=1 "
        )
        params: List[Any] = []
        if status:
            sql += "AND status = ? "
            params.append(status)
        if task_type:
            sql += "AND task_type = ? "
            params.append(task_type)
        if target_id:
            sql += "AND target_id = ? "
            params.append(target_id)
        sql += "ORDER BY created_at DESC, id DESC LIMIT ?"
        params.append(int(limit))
        cur.execute(sql, tuple(params))
        return list(cur.fetchall())
    finally:
        conn.close()


def get_task_log_by_id(log_id: int) -> Optional[Tuple[Any, ...]]:
    init_db()
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, task_type, target_id, input_id, input_title, status, error_msg, result_summary, "
            "created_at, updated_at FROM task_logs WHERE id = ?",
            (int(log_id),),
        )
        return cur.fetchone()
    finally:
        conn.close()
