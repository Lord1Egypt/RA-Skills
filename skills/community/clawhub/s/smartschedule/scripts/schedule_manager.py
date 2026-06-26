#!/usr/bin/env python3
"""
智能日程管理系统 - 核心模块
提供 SQLite 持久化的 CRUD 操作、时间冲突检测、替代时间建议。
"""

import sqlite3
import json
import os
import sys
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schedules.db")
DATE_FMT = "%Y-%m-%d %H:%M"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT DEFAULT '',
            start_time  TEXT NOT NULL,
            end_time    TEXT NOT NULL,
            location    TEXT DEFAULT '',
            remind_sent INTEGER DEFAULT 0,
            created_at  TEXT NOT NULL,
            updated_at  TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_start ON schedules(start_time)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_end ON schedules(end_time)
    """)
    conn.commit()
    conn.close()


def _row_to_dict(row):
    return dict(row) if row else None


def _now_str():
    return datetime.now().strftime(DATE_FMT)


# ── CRUD ─────────────────────────────────────────────────────────────

def add_schedule(title, start_time, end_time, description="", location=""):
    """添加日程，返回新日程 dict 和可能的冲突列表。"""
    conflicts = check_conflict(start_time, end_time)
    conn = get_conn()
    now = _now_str()
    cur = conn.execute(
        "INSERT INTO schedules (title, description, start_time, end_time, location, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (title, description, start_time, end_time, location, now, now),
    )
    conn.commit()
    new_id = cur.lastrowid
    row = conn.execute("SELECT * FROM schedules WHERE id = ?", (new_id,)).fetchone()
    conn.close()
    return {"schedule": _row_to_dict(row), "conflicts": conflicts}


def get_schedule(schedule_id):
    """按 ID 查询单条日程。"""
    conn = get_conn()
    row = conn.execute("SELECT * FROM schedules WHERE id = ?", (schedule_id,)).fetchone()
    conn.close()
    return _row_to_dict(row)


def list_schedules(start_after=None, start_before=None):
    """列出日程，可按时间范围筛选。"""
    conn = get_conn()
    query = "SELECT * FROM schedules WHERE 1=1"
    params = []
    if start_after:
        query += " AND start_time >= ?"
        params.append(start_after)
    if start_before:
        query += " AND start_time <= ?"
        params.append(start_before)
    query += " ORDER BY start_time ASC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def update_schedule(schedule_id, **kwargs):
    """更新日程字段（title / description / start_time / end_time / location）。"""
    allowed = {"title", "description", "start_time", "end_time", "location"}
    fields = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
    if not fields:
        return {"error": "没有可更新的字段"}

    new_start = fields.get("start_time")
    new_end = fields.get("end_time")

    if new_start or new_end:
        old = get_schedule(schedule_id)
        if not old:
            return {"error": f"日程 #{schedule_id} 不存在"}
        s = new_start or old["start_time"]
        e = new_end or old["end_time"]
        conflicts = check_conflict(s, e, exclude_id=schedule_id)
    else:
        conflicts = []

    fields["updated_at"] = _now_str()
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    vals = list(fields.values()) + [schedule_id]
    conn = get_conn()
    conn.execute(f"UPDATE schedules SET {set_clause} WHERE id = ?", vals)
    conn.commit()
    row = conn.execute("SELECT * FROM schedules WHERE id = ?", (schedule_id,)).fetchone()
    conn.close()
    return {"schedule": _row_to_dict(row), "conflicts": conflicts}


def delete_schedule(schedule_id):
    """删除日程。"""
    conn = get_conn()
    old = conn.execute("SELECT * FROM schedules WHERE id = ?", (schedule_id,)).fetchone()
    if not old:
        conn.close()
        return {"error": f"日程 #{schedule_id} 不存在"}
    conn.execute("DELETE FROM schedules WHERE id = ?", (schedule_id,))
    conn.commit()
    conn.close()
    return {"deleted": _row_to_dict(old)}


def search_schedules(keyword):
    """按关键词模糊搜索日程标题和描述。"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM schedules WHERE title LIKE ? OR description LIKE ? ORDER BY start_time ASC",
        (f"%{keyword}%", f"%{keyword}%"),
    ).fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


# ── 冲突检测 ─────────────────────────────────────────────────────────

def check_conflict(start_time, end_time, exclude_id=None):
    """检测与给定时间段冲突的已有日程。"""
    conn = get_conn()
    query = "SELECT * FROM schedules WHERE start_time < ? AND end_time > ?"
    params = [end_time, start_time]
    if exclude_id is not None:
        query += " AND id != ?"
        params.append(exclude_id)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def suggest_alternative(start_time, end_time, exclude_id=None):
    """为冲突的日程建议最近的可用时间段。向前后各搜索一个空闲窗口。"""
    s = datetime.strptime(start_time, DATE_FMT)
    e = datetime.strptime(end_time, DATE_FMT)
    duration = e - s

    conn = get_conn()
    exclude_clause = "AND id != ?" if exclude_id else ""
    params_base = [exclude_id] if exclude_id else []

    suggestions = []

    # 向后搜索：从原始结束时间开始找空闲
    rows_after = conn.execute(
        f"SELECT * FROM schedules WHERE start_time >= ? {exclude_clause} ORDER BY start_time ASC LIMIT 10",
        [start_time] + params_base,
    ).fetchall()

    candidate = e
    for row in rows_after:
        row_start = datetime.strptime(row["start_time"], DATE_FMT)
        row_end = datetime.strptime(row["end_time"], DATE_FMT)
        if candidate + duration <= row_start:
            break
        candidate = max(candidate, row_end)
    suggestions.append({
        "direction": "后移",
        "start_time": candidate.strftime(DATE_FMT),
        "end_time": (candidate + duration).strftime(DATE_FMT),
    })

    # 向前搜索：在原始开始时间之前找空闲
    rows_before = conn.execute(
        f"SELECT * FROM schedules WHERE end_time <= ? {exclude_clause} ORDER BY end_time DESC LIMIT 10",
        [end_time] + params_base,
    ).fetchall()

    candidate = s - duration
    for row in rows_before:
        row_start = datetime.strptime(row["start_time"], DATE_FMT)
        row_end = datetime.strptime(row["end_time"], DATE_FMT)
        if row_end <= candidate:
            break
        candidate = min(candidate, row_start - duration)
    if candidate >= datetime.now():
        suggestions.append({
            "direction": "前移",
            "start_time": candidate.strftime(DATE_FMT),
            "end_time": (candidate + duration).strftime(DATE_FMT),
        })

    conn.close()
    return suggestions


# ── 提醒相关查询 ─────────────────────────────────────────────────────

def get_upcoming(hours=24):
    """获取未来 N 小时内的日程。"""
    now = datetime.now()
    cutoff = now + timedelta(hours=hours)
    return list_schedules(
        start_after=now.strftime(DATE_FMT),
        start_before=cutoff.strftime(DATE_FMT),
    )


def get_due_soon(minutes=20):
    """获取即将在 N 分钟内开始且未发送提醒的日程。"""
    now = datetime.now()
    cutoff = now + timedelta(minutes=minutes)
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM schedules WHERE start_time >= ? AND start_time <= ? AND remind_sent = 0 "
        "ORDER BY start_time ASC",
        (now.strftime(DATE_FMT), cutoff.strftime(DATE_FMT)),
    ).fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def mark_reminded(schedule_id):
    """标记日程已发送提醒。"""
    conn = get_conn()
    conn.execute("UPDATE schedules SET remind_sent = 1 WHERE id = ?", (schedule_id,))
    conn.commit()
    conn.close()


# ── CLI 入口 ─────────────────────────────────────────────────────────

def main():
    init_db()

    if len(sys.argv) < 2:
        print(json.dumps({"error": "用法: schedule_manager.py <command> [args_json]"}, ensure_ascii=False))
        return

    cmd = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    handlers = {
        "add": lambda: add_schedule(**args),
        "get": lambda: get_schedule(args["id"]),
        "list": lambda: list_schedules(args.get("start_after"), args.get("start_before")),
        "update": lambda: update_schedule(args.pop("id"), **args),
        "delete": lambda: delete_schedule(args["id"]),
        "search": lambda: search_schedules(args["keyword"]),
        "conflict": lambda: check_conflict(args["start_time"], args["end_time"]),
        "suggest": lambda: suggest_alternative(args["start_time"], args["end_time"]),
        "upcoming": lambda: get_upcoming(args.get("hours", 24)),
        "due_soon": lambda: get_due_soon(args.get("minutes", 20)),
        "mark_reminded": lambda: mark_reminded(args["id"]),
        "init": lambda: "数据库已初始化",
    }

    if cmd not in handlers:
        print(json.dumps({"error": f"未知命令: {cmd}", "available": list(handlers.keys())}, ensure_ascii=False))
        return

    result = handlers[cmd]()
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
