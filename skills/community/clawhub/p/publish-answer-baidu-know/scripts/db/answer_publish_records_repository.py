"""answer_publish_records 表读写。

百度知道回答发布记录仓储：记录每次发布的幂等键、账号、问题 URL、文稿路径、
状态与平台反馈。支持幂等预检（按 idempotency_key 查重）。
"""

from __future__ import annotations

from typing import Any, List, Optional, Tuple

from db.connection import get_conn, init_db
from util.timeutil import now_unix


def find_by_idempotency_key(idempotency_key: str) -> Optional[Tuple[Any, ...]]:
    """按幂等键查询已有记录，用于幂等预检。返回 None 表示无重复。"""
    key = (idempotency_key or "").strip()
    if not key:
        return None
    init_db()
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, idempotency_key, account_id, question_url, answer_path,
                   status, platform_message, published_at, created_at, updated_at
            FROM answer_publish_records
            WHERE idempotency_key = ?
            LIMIT 1
            """,
            (key,),
        )
        return cur.fetchone()
    finally:
        conn.close()


def save_publish_record(
    *,
    idempotency_key: Optional[str] = None,
    account_id: str,
    question_url: str,
    answer_path: str,
    status: str,
    platform_message: Optional[str] = None,
    published_at: Optional[int] = None,
) -> Tuple[int, bool]:
    """
    插入一条发布记录。

    返回 (record_id, is_duplicate)：
      - 若 idempotency_key 已存在，返回已有记录的 (id, True)
      - 否则插入新记录，返回 (new_id, False)
    """
    init_db()
    key = (idempotency_key or "").strip() or None

    # 幂等预检
    if key:
        existing = find_by_idempotency_key(key)
        if existing is not None:
            return int(existing[0]), True

    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO answer_publish_records
                (idempotency_key, account_id, question_url, answer_path,
                 status, platform_message, published_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                key,
                str(account_id),
                str(question_url),
                str(answer_path),
                str(status),
                platform_message,
                published_at if published_at is not None else now_unix(),
            ),
        )
        new_id = int(cur.lastrowid)
        conn.commit()
        return new_id, False
    finally:
        conn.close()


def list_publish_records(
    limit: int = 20,
    status: Optional[str] = None,
    account_id: Optional[str] = None,
) -> List[Tuple[Any, ...]]:
    init_db()
    conn = get_conn()
    try:
        cur = conn.cursor()
        sql = (
            "SELECT id, idempotency_key, account_id, question_url, answer_path, "
            "status, platform_message, published_at, created_at, updated_at "
            "FROM answer_publish_records WHERE 1=1 "
        )
        params: List[Any] = []
        if status:
            sql += "AND status = ? "
            params.append(status)
        if account_id:
            sql += "AND account_id = ? "
            params.append(str(account_id))
        sql += "ORDER BY created_at DESC, id DESC LIMIT ?"
        params.append(int(limit))
        cur.execute(sql, tuple(params))
        return list(cur.fetchall())
    finally:
        conn.close()


def get_publish_record_by_id(record_id: int) -> Optional[Tuple[Any, ...]]:
    init_db()
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, idempotency_key, account_id, question_url, answer_path,
                   status, platform_message, published_at, created_at, updated_at
            FROM answer_publish_records
            WHERE id = ?
            """,
            (int(record_id),),
        )
        return cur.fetchone()
    finally:
        conn.close()
