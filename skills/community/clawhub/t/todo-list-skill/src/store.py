#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TODO 数据访问层（单例模式 + WAL 并发安全）。

本模块提供 :class:`TodosStore` 类，用于通过 SQLite WAL（Write-Ahead
Logging，预写日志）模式实现线程安全的 TODO 数据持久化。Store 采用
单例模式避免重复初始化，并对写操作使用指数退避重试。

线程安全：
    SQLite WAL 模式允许多读单写并发。写操作在
    ``OperationalError: locked`` 时最多重试 3 次。

技术决策：
    - 单例：避免重复创建连接（DB_PATH 单值）
    - WAL：读写并发 + 减少锁等待
    - 重试：指数退避（0.1s → 0.2s → 0.4s）
    - from __future__ import annotations：解决 def list() 遮蔽 built-in

参见：
    - DESIGN.md §4.1（数据层设计）
    - SOUL.md 规则 15（数据源统一原则）
    - SQLite WAL 文档：https://www.sqlite.org/wal.html

License:
    MIT

Version:
    1.4.0

Author:
    月海巫师 (Chen Qing)
"""
from __future__ import annotations  # PEP 563：延后求值类型注解

import json
import os
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .exceptions import (
    TodoAmbiguousError,
    TodoDatabaseError,
    TodoNotFoundError,
    TodoValidationError,
)

# 数据库路径（相对于 src/ 目录）
# 支持 TODOS_DB_PATH 环境变量覆盖（测试隔离用）
DB_DIR = Path(__file__).parent.parent
DB_PATH = os.environ.get("TODOS_DB_PATH") or str(DB_DIR / "todos.db")
SCHEMA_PATH = str(DB_DIR / "schema" / "init_todos.sql")

# 并发重试配置
MAX_RETRIES = 3
RETRY_DELAY_BASE = 0.1  # 秒，指数退避

# 业务常量（参考 DESIGN.md §十 §10.1）
VALID_PRIORITIES = {"high", "medium", "low"}
VALID_STATUSES = {"pending", "in_progress", "completed", "cancelled", "overdue"}
DUE_AT_MAX_DAYS = 365  # due_at 距今最大天数（DESIGN.md §十 §10.1）


class TodosStore:
    """
    TODO 数据访问层（单例模式，线程安全 via WAL）

    业界参考：
    - SOUL.md 规则15：数据源统一原则（SQLite 持久化）
    - 12-Factor App §XI：日志写到 stdout
    """

    _instance: "TodosStore | None" = None

    def __new__(cls) -> "TodosStore":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # 单例模式：避免重复初始化
        pass

    # ── 私有工具 ────────────────────────────────────────────────

    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接（WAL 模式）"""
        conn = sqlite3.connect(DB_PATH, timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.row_factory = sqlite3.Row
        return conn

    def _execute_with_retry(
        self, sql: str, params: tuple = ()
    ) -> sqlite3.Cursor:
        """带重试的写操作（WAL 模式）"""
        for attempt in range(MAX_RETRIES):
            conn = self._get_connection()
            try:
                cursor = conn.execute(sql, params)
                conn.commit()
                return cursor
            except sqlite3.OperationalError as e:
                if "locked" in str(e) and attempt < MAX_RETRIES - 1:
                    delay = RETRY_DELAY_BASE * (2 ** attempt)
                    time.sleep(delay)
                    conn.close()
                    continue
                raise TodoDatabaseError(f"数据库写入失败: {e}")
            finally:
                conn.close()

    def _log_audit(
        self,
        action: str,
        todo_id: int | None = None,
        actor: str = "agent",
        details: dict | None = None,
    ) -> None:
        """写入审计日志"""
        details_json = json.dumps(details, ensure_ascii=False) if details else None
        try:
            conn = self._get_connection()
            conn.execute(
                "INSERT INTO audit_log (action, todo_id, actor, details) VALUES (?, ?, ?, ?)",
                (action, todo_id, actor, details_json),
            )
            conn.commit()
            conn.close()
        except Exception:
            # 审计日志失败不阻塞主操作
            pass

    def _row_to_dict(self, row: sqlite3.Row) -> dict:
        """sqlite3.Row → dict"""
        return dict(row)

    def _is_overdue(self, due_at: str | None) -> bool:
        """检查是否已过期"""
        if not due_at:
            return False
        try:
            due = datetime.fromisoformat(due_at.replace("Z", "+00:00"))
            # 只比较日期部分（忽略时区）
            return due.replace(tzinfo=None) < datetime.now().replace(tzinfo=None)
        except ValueError:
            return False

    # ── 初始化 ──────────────────────────────────────────────────

    def init_db(self) -> None:
        """创建 schema（幂等，多次调用安全）"""
        schema_sql = Path(SCHEMA_PATH).read_text(encoding="utf-8")
        conn = self._get_connection()
        try:
            conn.executescript(schema_sql)
            conn.commit()
            print("✅ 数据库初始化完成")
            print(f"   Schema 版本：v1.0")
        finally:
            conn.close()

    # ── CRUD ────────────────────────────────────────────────────

    def add(
        self,
        content: str,
        active_form: str | None = None,
        due_at: str | None = None,
        priority: str = "medium",
        tags: list[str] | None = None,
        source: str = "chat",
        raw_input: str | None = None,
    ) -> dict:
        """
        添加 TODO

        Raises:
            TodoValidationError: 参数校验失败（content 空/超长、priority/status 非法、due_at 距今>1年）
        """
        # 验证 content
        if not content or not content.strip():
            raise TodoValidationError("content 不能为空")
        if len(content) > 500:
            raise TodoValidationError(f"content 超过 500 字符（当前 {len(content)}）")

        # 验证 priority（DESIGN.md §十 §10.1 白名单）
        if priority not in VALID_PRIORITIES:
            raise TodoValidationError(
                f"priority 必须是 {VALID_PRIORITIES} 之一，当前: {priority!r}"
            )

        # 验证 due_at 范围（DESIGN.md §十 §10.1：距今 ≤ 1 年）
        if due_at:
            try:
                due_dt = datetime.fromisoformat(due_at.replace("Z", "+00:00"))
            except ValueError:
                raise TodoValidationError(f"due_at 格式不合法: {due_at!r}")
            if due_dt < datetime.now() - timedelta(days=DUE_AT_MAX_DAYS):
                raise TodoValidationError(
                    f"due_at 距今超过 {DUE_AT_MAX_DAYS} 天"
                )
            if due_dt > datetime.now() + timedelta(days=DUE_AT_MAX_DAYS):
                raise TodoValidationError(
                    f"due_at 距今超过 {DUE_AT_MAX_DAYS} 天（未来）"
                )

        # active_form 默认值
        if active_form is None:
            active_form = _to_active_form(content)

        # tags 序列化为 JSON
        tags_json = json.dumps(tags or [], ensure_ascii=False)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor = self._execute_with_retry(
            """INSERT INTO todos
                (content, active_form, status, priority, due_at, tags, created_at, updated_at, source, raw_input)
               VALUES (?, ?, 'pending', ?, ?, ?, ?, ?, ?, ?)""",
            (content.strip(), active_form, priority, due_at, tags_json, now, now, source, raw_input),
        )

        todo_id = cursor.lastrowid
        self._log_audit("add", todo_id, details={"content": content, "priority": priority})

        # 返回新建的 TODO
        conn = self._get_connection()
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
        conn.close()
        return self._row_to_dict(row) if row else {}

    def list(
        self,
        status: str | None = None,
        tag: str | None = None,
        priority: str | None = None,
        overdue: bool = False,
        all: bool = False,
    ) -> list[dict]:
        """
        查询 TODO

        - 默认（all=False）：只返回 pending + in_progress
        - all=True：返回所有状态
        - overdue=True：返回所有已过期（不管 status）
        - tag 过滤：JSON 数组包含该标签
        """
        conditions = []
        params: list[Any] = []

        # status 过滤
        if status:
            conditions.append("status = ?")
            params.append(status)
        elif not all and not overdue:
            # 默认：只返 pending + in_progress
            conditions.append("status IN ('pending', 'in_progress')")

        # priority 过滤
        if priority:
            conditions.append("priority = ?")
            params.append(priority)

        # tag 过滤（JSON 数组包含）
        if tag:
            conditions.append("tags LIKE ?")
            params.append(f'%"{tag}"%')

        # overdue 过滤
        if overdue:
            conditions.append("due_at IS NOT NULL")
            conditions.append("due_at < ?")
            params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        order = "ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END, created_at DESC"

        conn = self._get_connection()
        rows = conn.execute(f"SELECT * FROM todos {where} {order}", params).fetchall()
        conn.close()

        return [self._row_to_dict(row) for row in rows]

    def done(self, id_or_content: str) -> dict:
        """
        完成 TODO（按 ID 或 content 模糊匹配）

        Raises:
            TodoNotFoundError: 无匹配 todo
            TodoAmbiguousError: 多个匹配，需要用户确认
        """
        conn = self._get_connection()

        # 先按 ID 精确匹配
        if id_or_content.isdigit():
            row = conn.execute(
                "SELECT * FROM todos WHERE id = ? AND status IN ('pending', 'in_progress')",
                (int(id_or_content),),
            ).fetchone()
            if row:
                conn.close()
                return self._complete_todo(row["id"])

        # 按 content 模糊匹配
        rows = conn.execute(
            """SELECT * FROM todos
               WHERE status IN ('pending', 'in_progress')
                 AND content LIKE ?""",
            (f"%{id_or_content}%",),
        ).fetchall()
        conn.close()

        if not rows:
            raise TodoNotFoundError(f"未找到匹配的 TODO: {id_or_content}")
        if len(rows) > 1:
            raise TodoAmbiguousError([self._row_to_dict(r) for r in rows])

        return self._complete_todo(rows[0]["id"])

    def _complete_todo(self, todo_id: int) -> dict:
        """内部方法：完成指定 TODO"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = self._get_connection()
        conn.execute(
            """UPDATE todos
               SET status = 'completed', completed_at = ?, updated_at = ?
               WHERE id = ?""",
            (now, now, todo_id),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
        conn.close()
        self._log_audit("done", todo_id)
        return self._row_to_dict(row) if row else {}

    def delete(self, id_or_content: str) -> dict:
        """
        软删除：移入 archive，状态改为 cancelled

        Raises:
            TodoNotFoundError: 无匹配 todo
            TodoAmbiguousError: 多个匹配，需要用户确认
        """
        conn = self._get_connection()

        # 按 ID 精确匹配
        if id_or_content.isdigit():
            row = conn.execute("SELECT * FROM todos WHERE id = ?", (int(id_or_content),)).fetchone()
            if row:
                conn.close()
                return self._archive_todo(row["id"], "cancelled")

        # 按 content 模糊匹配
        rows = conn.execute(
            "SELECT * FROM todos WHERE content LIKE ?",
            (f"%{id_or_content}%",),
        ).fetchall()

        if not rows:
            raise TodoNotFoundError(f"未找到匹配的 TODO: {id_or_content}")
        if len(rows) > 1:
            raise TodoAmbiguousError([self._row_to_dict(r) for r in rows])

        conn.close()
        return self._archive_todo(rows[0]["id"], "cancelled")

    def _archive_todo(self, todo_id: int, status: str) -> dict:
        """内部方法：移入 archive"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = self._get_connection()
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
        if not row:
            conn.close()
            raise TodoNotFoundError(f"TODO {todo_id} 不存在")

        conn.execute(
            """INSERT INTO todos_archive
                (id, content, active_form, status, priority, due_at, tags,
                 created_at, updated_at, completed_at, archived_at, source, raw_input)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                row["id"], row["content"], row["active_form"], status, row["priority"],
                row["due_at"], row["tags"], row["created_at"], row["updated_at"],
                row["completed_at"], now, row["source"], row["raw_input"],
            ),
        )
        conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
        conn.close()
        self._log_audit("del", todo_id, details={"status": status})
        return self._row_to_dict(row)

    def update(self, id: int, **kwargs) -> dict:
        """
        更新字段（priority/due_at/tags/content/status）
        任意字段更新后同步 updated_at

        Raises:
            TodoNotFoundError: TODO 不存在
            TodoValidationError: 参数校验失败
        """
        allowed_fields = {"content", "active_form", "priority", "due_at", "tags", "status"}
        invalid_fields = set(kwargs.keys()) - allowed_fields
        if invalid_fields:
            raise TodoValidationError(f"不允许的字段: {invalid_fields}")

        conn = self._get_connection()
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (id,)).fetchone()
        if not row:
            conn.close()
            raise TodoNotFoundError(f"TODO {id} 不存在")

        # 验证 content
        if "content" in kwargs:
            c = kwargs["content"]
            if not c or not c.strip():
                conn.close()
                raise TodoValidationError("content 不能为空")
            if len(c) > 500:
                conn.close()
                raise TodoValidationError(f"content 超过 500 字符")

        # 验证 priority 白名单
        if "priority" in kwargs and kwargs["priority"] not in VALID_PRIORITIES:
            conn.close()
            raise TodoValidationError(
                f"priority 必须是 {VALID_PRIORITIES} 之一，当前: {kwargs['priority']!r}"
            )

        # 验证 status 白名单
        if "status" in kwargs and kwargs["status"] not in VALID_STATUSES:
            conn.close()
            raise TodoValidationError(
                f"status 必须是 {VALID_STATUSES} 之一，当前: {kwargs['status']!r}"
            )

        # 验证 due_at 范围
        if "due_at" in kwargs and kwargs["due_at"]:
            try:
                due_dt = datetime.fromisoformat(kwargs["due_at"].replace("Z", "+00:00"))
            except ValueError:
                conn.close()
                raise TodoValidationError(f"due_at 格式不合法: {kwargs['due_at']!r}")
            now = datetime.now()
            if due_dt < now - timedelta(days=DUE_AT_MAX_DAYS) or due_dt > now + timedelta(days=DUE_AT_MAX_DAYS):
                conn.close()
                raise TodoValidationError(
                    f"due_at 距今超过 {DUE_AT_MAX_DAYS} 天"
                )

        # 构建更新 SQL
        sets = []
        params = []
        for field in allowed_fields:
            if field in kwargs:
                if field == "tags" and isinstance(kwargs[field], list):
                    sets.append(f"{field} = ?")
                    params.append(json.dumps(kwargs[field], ensure_ascii=False))
                else:
                    sets.append(f"{field} = ?")
                    params.append(kwargs[field])

        sets.append("updated_at = ?")
        params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        params.append(id)

        conn.execute(f"UPDATE todos SET {', '.join(sets)} WHERE id = ?", params)
        conn.commit()
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (id,)).fetchone()
        conn.close()
        self._log_audit("update", id, details=kwargs)
        return self._row_to_dict(row) if row else {}

    def restore(self, archive_id: int) -> dict:
        """
        从 archive 恢复到 todos

        Raises:
            TodoNotFoundError: archive 中不存在
        """
        conn = self._get_connection()
        row = conn.execute("SELECT * FROM todos_archive WHERE id = ?", (archive_id,)).fetchone()
        if not row:
            conn.close()
            raise TodoNotFoundError(f"Archive {archive_id} 不存在")

        conn.execute(
            """INSERT INTO todos
                (id, content, active_form, status, priority, due_at, tags,
                 created_at, updated_at, completed_at, source, raw_input)
               VALUES (?, ?, ?, 'pending', ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                row["id"], row["content"], row["active_form"], row["priority"],
                row["due_at"], row["tags"], row["created_at"], row["updated_at"],
                row["completed_at"], row["source"], row["raw_input"],
            ),
        )
        conn.execute("DELETE FROM todos_archive WHERE id = ?", (archive_id,))
        conn.commit()
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (archive_id,)).fetchone()
        conn.close()
        self._log_audit("restore", archive_id)
        return self._row_to_dict(row) if row else {}

    # ── 工具 ────────────────────────────────────────────────────

    def stats(self) -> dict:
        """统计：总数/各状态数/高优数/本周到期数/逾期数"""
        conn = self._get_connection()

        total = conn.execute("SELECT COUNT(*) FROM todos").fetchone()[0]
        pending = conn.execute("SELECT COUNT(*) FROM todos WHERE status='pending'").fetchone()[0]
        in_progress = conn.execute("SELECT COUNT(*) FROM todos WHERE status='in_progress'").fetchone()[0]
        completed = conn.execute("SELECT COUNT(*) FROM todos WHERE status='completed'").fetchone()[0]
        cancelled = conn.execute("SELECT COUNT(*) FROM todos WHERE status='cancelled'").fetchone()[0]
        overdue = conn.execute(
            """SELECT COUNT(*) FROM todos
               WHERE due_at IS NOT NULL AND due_at < ?""",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),),
        ).fetchone()[0]

        high_priority = conn.execute("SELECT COUNT(*) FROM todos WHERE priority='high'").fetchone()[0]
        medium_priority = conn.execute("SELECT COUNT(*) FROM todos WHERE priority='medium'").fetchone()[0]
        low_priority = conn.execute("SELECT COUNT(*) FROM todos WHERE priority='low'").fetchone()[0]

        # 本周到期
        week_end = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        week_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        this_week = conn.execute(
            """SELECT COUNT(*) FROM todos
               WHERE due_at IS NOT NULL
                 AND due_at >= ? AND due_at <= ?""",
            (week_start, week_end),
        ).fetchone()[0]

        conn.close()
        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed,
            "cancelled": cancelled,
            "overdue": overdue,
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "low_priority": low_priority,
            "this_week": this_week,
        }

    def check_overdue(self) -> list[dict]:
        """批量标记 overdue（每天 00:05 调用）"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = self._get_connection()
        conn.execute(
            """UPDATE todos
               SET status = 'overdue', updated_at = ?
               WHERE status IN ('pending', 'in_progress')
                 AND due_at IS NOT NULL
                 AND due_at < ?""",
            (now, now),
        )
        conn.commit()
        rows = conn.execute(
            """SELECT * FROM todos
               WHERE status = 'overdue'
                 AND updated_at = ?""",
            (now,),
        ).fetchall()
        conn.close()
        for row in rows:
            self._log_audit("overdue", row["id"])
        return [self._row_to_dict(r) for r in rows]

    def archive_cleanup(self, days: int = 30) -> int:
        """
        清理 30 天前 archive（返回清理数量）
        由 cron 每月调用一次
        """
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        conn = self._get_connection()
        cursor = conn.execute(
            "DELETE FROM todos_archive WHERE archived_at < ?",
            (cutoff,),
        )
        conn.commit()
        count = cursor.rowcount
        conn.close()
        if count > 0:
            self._log_audit("archive_cleanup", details={"deleted": count, "cutoff": cutoff})
        return count

    def get_by_id(self, id: int) -> dict | None:
        """按 ID 获取 TODO"""
        conn = self._get_connection()
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (id,)).fetchone()
        conn.close()
        return self._row_to_dict(row) if row else None

    def get_by_raw_input(self, raw_input: str) -> list[dict]:
        """按 raw_input 查找 TODO"""
        conn = self._get_connection()
        rows = conn.execute(
            "SELECT * FROM todos WHERE raw_input LIKE ?",
            (f"%{raw_input}%",),
        ).fetchall()
        conn.close()
        return [self._row_to_dict(r) for r in rows]


# ── 工具函数 ─────────────────────────────────────────────────────

def _to_active_form(content: str) -> str:
    """命令式 → 进行时（简单规则）"""
    content = content.strip()
    # 去除末尾标点
    content = content.rstrip("。！？.,!?")
    # 常见前缀
    for prefix in ["提醒我", "提醒", "记一下", "加个待办", "待办", "任务", "todo"]:
        if content.startswith(prefix):
            content = content[len(prefix):].strip()
    # 加"进行中"后缀
    if not content.endswith("中") and not content.endswith("进行"):
        return content + "进行中"
    return content


# 导出异常（方便调用方 import）
__all__ = [
    "TodosStore",
    "TodoNotFoundError",
    "TodoAmbiguousError",
    "TodoValidationError",
    "TodoDatabaseError",
    "_to_active_form",
]