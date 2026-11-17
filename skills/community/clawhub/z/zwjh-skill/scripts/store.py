# -*- coding: utf-8 -*-
"""
存储层 —— 基于标准库 sqlite3 的轻量「记忆底座」。

表结构：
  memories   长期记忆条目（来自每日日志 / 对话 / 文件沉淀）
  entities   知识图谱实体（人/项目/任务/事件/文档…）
  relations  实体间关系
  facts      关于实体的「事实」（带有效期，支持冲突消解）
  diary      日记（自由记录）

所有写入兼容「只追加 / 可修正」，不删原始数据，符合记忆安全约定。
"""

from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime, date
from pathlib import Path

from . import config

_lock = threading.Lock()


def _connect() -> sqlite3.Connection:
    config.ensure_dirs()
    db = str(config.DB_PATH)
    conn = sqlite3.connect(db, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")          # 写前日志，降低写入阻塞
    conn.execute("PRAGMA synchronous=NORMAL")         # 性能优先，WAL 足够安全
    conn.execute("PRAGMA foreign_keys=ON")
    _init_schema(conn)
    return conn


def _init_schema(conn: sqlite3.Connection) -> None:
    # Check if memories table already exists and lacks new columns
    has_namespace = False
    try:
        cols = [row[1] for row in conn.execute("PRAGMA table_info(memories)")]
        has_namespace = "namespace" in cols
    except Exception:
        pass

    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS memories (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            day           TEXT NOT NULL,                -- 关联每日日志日期
            source        TEXT NOT NULL DEFAULT 'conversation',
            raw_text      TEXT NOT NULL,
            norm_hash     TEXT NOT NULL,                -- 去重指纹
            tokens_json   TEXT NOT NULL DEFAULT '[]',   -- 中文 char n-gram + 词 token
            created_at    TEXT NOT NULL,
            last_accessed TEXT NOT NULL,
            access_count  INTEGER NOT NULL DEFAULT 0,
            quality       REAL   NOT NULL DEFAULT 1.0,  -- 健康度质量分
            importance    REAL   NOT NULL DEFAULT 0.5,
            version       INTEGER NOT NULL DEFAULT 1,   -- 乐观锁版本号
            namespace     TEXT NOT NULL DEFAULT 'public' -- 命名空间隔离
        );
        CREATE INDEX IF NOT EXISTS idx_mem_day ON memories(day);
        CREATE INDEX IF NOT EXISTS idx_mem_hash ON memories(norm_hash);
        CREATE INDEX IF NOT EXISTS idx_mem_access ON memories(last_accessed);
        -- idx_mem_namespace created below after migration check

        -- 归档表（forget 软删除后的恢复用）
        CREATE TABLE IF NOT EXISTS memories_archive (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            original_id   INTEGER NOT NULL,
            day           TEXT NOT NULL,
            source        TEXT NOT NULL,
            raw_text      TEXT NOT NULL,
            norm_hash     TEXT NOT NULL,
            tokens_json   TEXT NOT NULL,
            importance    REAL NOT NULL DEFAULT 0.5,
            namespace     TEXT NOT NULL DEFAULT 'public',
            archived_at   TEXT NOT NULL,
            reason        TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_arch_original ON memories_archive(original_id);
        CREATE INDEX IF NOT EXISTS idx_arch_day ON memories_archive(day);
        """
    )
    # Migration: add columns if missing (for existing DBs that pre-date v2.6.0)
    if not has_namespace:
        try:
            cols = [row[1] for row in conn.execute("PRAGMA table_info(memories)")]
            if "version" not in cols:
                conn.execute("ALTER TABLE memories ADD COLUMN version INTEGER NOT NULL DEFAULT 1")
            if "namespace" not in cols:
                conn.execute("ALTER TABLE memories ADD COLUMN namespace TEXT NOT NULL DEFAULT 'public'")
        except Exception:
            pass
    # Create namespace index (safe after migration)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_mem_namespace ON memories(namespace)")
    conn.commit()

    # Migration: add columns if missing (for existing DBs that pre-date v2.6.0)
    try:
        cols = [row[1] for row in conn.execute("PRAGMA table_info(memories)")]
        if "version" not in cols:
            conn.execute("ALTER TABLE memories ADD COLUMN version INTEGER NOT NULL DEFAULT 1")
        if "namespace" not in cols:
            conn.execute("ALTER TABLE memories ADD COLUMN namespace TEXT NOT NULL DEFAULT 'public'")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_mem_namespace ON memories(namespace)")
        conn.commit()
    except Exception:
        pass

    # Continue creating remaining tables
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS entities (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            type       TEXT NOT NULL DEFAULT 'concept',
            name       TEXT NOT NULL,
            aliases_json TEXT NOT NULL DEFAULT '[]',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            importance REAL NOT NULL DEFAULT 0.5,
            UNIQUE(type, name)
        );
        CREATE INDEX IF NOT EXISTS idx_ent_name ON entities(name);

        CREATE TABLE IF NOT EXISTS relations (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            from_id    INTEGER NOT NULL,
            to_id      INTEGER NOT NULL,
            relation   TEXT NOT NULL,
            weight     REAL NOT NULL DEFAULT 1.0,
            confidence REAL NOT NULL DEFAULT 1.0,
            created_at TEXT NOT NULL,
            FOREIGN KEY(from_id) REFERENCES entities(id) ON DELETE CASCADE,
            FOREIGN KEY(to_id)   REFERENCES entities(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_rel_from ON relations(from_id);
        CREATE INDEX IF NOT EXISTS idx_rel_to   ON relations(to_id);

        CREATE TABLE IF NOT EXISTS facts (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_id     INTEGER NOT NULL,
            predicate     TEXT NOT NULL,                -- 谓词，如「职位」「状态」
            value         TEXT NOT NULL,
            valid_from    TEXT NOT NULL,
            valid_to      TEXT,                         -- 被取代时填时间
            superseded    INTEGER NOT NULL DEFAULT 0,
            source_memory_id INTEGER,
            created_at    TEXT NOT NULL,
            FOREIGN KEY(entity_id) REFERENCES entities(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_fact_ent ON facts(entity_id, predicate);

        CREATE TABLE IF NOT EXISTS diary (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            day        TEXT NOT NULL,
            text       TEXT NOT NULL,
            mood       TEXT,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_diary_day ON diary(day);
        """
    )
    conn.commit()


def get_conn() -> sqlite3.Connection:
    # 简单连接池：每个线程复用同一条连接
    local = _conn_local()
    conn = getattr(local, "conn", None)
    if conn is None:
        conn = _connect()
        local.conn = conn
    return conn


def _conn_local():
    t = threading.current_thread()
    if not hasattr(t, "_zwjh_conn"):
        t._zwjh_conn = type("L", (), {})()
    return t._zwjh_conn


# ── 记忆 ──────────────────────────────────────────────────────────────────
def add_memory(day: str, source: str, raw_text: str, norm_hash: str,
               tokens: list[str], importance: float = 0.5,
               namespace: str = "public") -> int:
    now = datetime.now().isoformat(timespec="seconds")
    with _lock:
        conn = get_conn()
        cur = conn.execute(
            """INSERT INTO memories(day, source, raw_text, norm_hash, tokens_json,
                                    created_at, last_accessed, access_count, importance,
                                    namespace)
               VALUES(?,?,?,?,?,?,?,?,?,?)""",
            (day, source, raw_text, norm_hash, json.dumps(tokens, ensure_ascii=False),
             now, now, 0, importance, namespace),
        )
        conn.commit()
        return int(cur.lastrowid)


def find_by_hash(norm_hash: str):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM memories WHERE norm_hash=?", (norm_hash,)
    ).fetchone()
    return dict(row) if row else None


def get_memory_version(memory_id: int) -> int | None:
    """获取记忆当前版本号（乐观锁）。"""
    conn = get_conn()
    row = conn.execute(
        "SELECT version FROM memories WHERE id=?", (memory_id,)
    ).fetchone()
    return row["version"] if row else None


def update_memory_with_lock(memory_id: int, fields: dict) -> dict:
    """
    带乐观锁的记忆更新。

    Args:
        memory_id: 记忆 ID
        fields: 要更新的字段 dict，必须包含 'version' 键表示期望的当前版本

    Returns:
        {"ok": True} 或 {"ok": False, "error": "WRITE_CONFLICT", "current_version": int}
    """
    with _lock:
        conn = get_conn()
        row = conn.execute(
            "SELECT version FROM memories WHERE id=?", (memory_id,)
        ).fetchone()
        if not row:
            return {"ok": False, "error": "NOT_FOUND"}
        current_ver = row["version"]
        expected_ver = fields.get("version", current_ver)
        if current_ver != expected_ver:
            return {"ok": False, "error": "WRITE_CONFLICT",
                    "current_version": current_ver,
                    "expected_version": expected_ver}
        # 构建 SET 子句
        allowed = {"raw_text", "importance", "quality", "namespace", "source"}
        updates = {k: v for k, v in fields.items() if k in allowed}
        if not updates:
            return {"ok": True, "version": current_ver}
        updates["version"] = current_ver + 1
        set_clause = ", ".join("%s=?" % k for k in updates)
        values = list(updates.values()) + [memory_id, current_ver]
        conn.execute(
            "UPDATE memories SET %s WHERE id=? AND version=?" % set_clause,
            values)
        conn.commit()
        return {"ok": True, "version": current_ver + 1}


def get_daily_log(day: str):
    """返回某天是否已作为 daily_log 索引（用于幂等补录）。"""
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM memories WHERE source='daily_log' AND day=?", (day,)
    ).fetchone()
    return dict(row) if row else None


def update_access(memory_id: int) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    with _lock:
        conn = get_conn()
        conn.execute(
            "UPDATE memories SET last_accessed=?, access_count=access_count+1 WHERE id=?",
            (now, memory_id),
        )
        conn.commit()


def list_memories(day_from: str | None = None, day_to: str | None = None,
                  limit: int = 200, offset: int = 0) -> list[dict]:
    conn = get_conn()
    sql = "SELECT * FROM memories WHERE 1=1"
    args: list = []
    if day_from:
        sql += " AND day>=?"
        args.append(day_from)
    if day_to:
        sql += " AND day<=?"
        args.append(day_to)
    sql += " ORDER BY day DESC, id DESC LIMIT ? OFFSET ?"
    args += [limit, offset]
    rows = conn.execute(sql, args).fetchall()
    return [dict(r) for r in rows]


def all_memory_tokens() -> list[tuple[int, list[str]]]:
    """返回全部记忆 (id, tokens)，用于离线重建 IDF / 语义检索。"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, tokens_json FROM memories"
    ).fetchall()
    out = []
    for r in rows:
        try:
            toks = json.loads(r["tokens_json"])
        except Exception:
            toks = []
        out.append((r["id"], toks))
    return out


def count_memories() -> int:
    conn = get_conn()
    return conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]


def has_digest_for_day(day: str) -> bool:
    """某天是否已有 digest（压缩）记忆，避免重复摘要。"""
    conn = get_conn()
    row = conn.execute(
        "SELECT id FROM memories WHERE source='digest' AND day=?", (day,)
    ).fetchone()
    return row is not None


def dump_memories(limit: int = 200000) -> list[dict]:
    """导出全部记忆（供快照/备份/恢复）。"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT day, source, raw_text, norm_hash, tokens_json, importance "
        "FROM memories ORDER BY id LIMIT ?",
        (limit,),
    ).fetchall()
    return [dict(r) for r in rows]


# ── 实体 ──────────────────────────────────────────────────────────────────
def upsert_entity(type_: str, name: str, aliases: list[str] | None = None,
                  importance: float = 0.5):
    now = datetime.now().isoformat(timespec="seconds")
    with _lock:
        conn = get_conn()
        row = conn.execute(
            "SELECT * FROM entities WHERE type=? AND name=?", (type_, name)
        ).fetchone()
        if row:
            conn.execute(
                "UPDATE entities SET updated_at=?, importance=? WHERE id=?",
                (now, max(row["importance"], importance), row["id"]),
            )
            conn.commit()
            return int(row["id"])
        cur = conn.execute(
            "INSERT INTO entities(type, name, aliases_json, created_at, updated_at, importance) "
            "VALUES(?,?,?,?,?,?)",
            (type_, name, json.dumps(aliases or [], ensure_ascii=False), now, now, importance),
        )
        conn.commit()
        return int(cur.lastrowid)


def find_entity(type_: str | None, name: str):
    conn = get_conn()
    if type_:
        row = conn.execute(
            "SELECT * FROM entities WHERE type=? AND name=?", (type_, name)
        ).fetchone()
    else:
        row = conn.execute(
            "SELECT * FROM entities WHERE name=?", (name,)
        ).fetchone()
    return dict(row) if row else None


def search_entities_by_name(substr: str, limit: int = 20) -> list[dict]:
    conn = get_conn()
    like = f"%{substr}%"
    rows = conn.execute(
        "SELECT * FROM entities WHERE name LIKE ? ORDER BY importance DESC LIMIT ?",
        (like, limit),
    ).fetchall()
    return [dict(r) for r in rows]


def list_entities(limit: int = 500) -> list[dict]:
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM entities ORDER BY importance DESC, id LIMIT ?", (limit,)
    ).fetchall()
    return [dict(r) for r in rows]


def count_entities() -> int:
    conn = get_conn()
    return conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]


# ── 关系 ──────────────────────────────────────────────────────────────────
def add_relation(from_id: int, to_id: int, relation: str,
                 weight: float = 1.0, confidence: float = 1.0) -> int | None:
    now = datetime.now().isoformat(timespec="seconds")
    with _lock:
        conn = get_conn()
        # 避免完全重复的关系
        existing = conn.execute(
            "SELECT id FROM relations WHERE from_id=? AND to_id=? AND relation=?",
            (from_id, to_id, relation),
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE relations SET weight=weight+?, confidence=? WHERE id=?",
                (weight, max(confidence, 0.5), existing["id"]),
            )
            conn.commit()
            return int(existing["id"])
        cur = conn.execute(
            "INSERT INTO relations(from_id, to_id, relation, weight, confidence, created_at) "
            "VALUES(?,?,?,?,?,?)",
            (from_id, to_id, relation, weight, confidence, now),
        )
        conn.commit()
        return int(cur.lastrowid)


def relations_of(entity_id: int, direction: str = "both") -> list[dict]:
    conn = get_conn()
    out = []
    if direction in ("out", "both"):
        rows = conn.execute(
            "SELECT r.*, e.name AS to_name, e.type AS to_type FROM relations r "
            "JOIN entities e ON e.id=r.to_id WHERE r.from_id=?", (entity_id,)
        ).fetchall()
        out += [dict(r) for r in rows]
    if direction in ("in", "both"):
        rows = conn.execute(
            "SELECT r.*, e.name AS from_name, e.type AS from_type FROM relations r "
            "JOIN entities e ON e.id=r.from_id WHERE r.to_id=?", (entity_id,)
        ).fetchall()
        out += [dict(r) for r in rows]
    return out


def count_relations() -> int:
    conn = get_conn()
    return conn.execute("SELECT COUNT(*) FROM relations").fetchone()[0]


# ── 事实（冲突消解） ───────────────────────────────────────────────────────
def add_fact(entity_id: int, predicate: str, value: str,
             source_memory_id: int | None = None) -> dict:
    """写入事实；若同谓词存在未废止的旧值且不同，则把旧值标记为 superseded。"""
    now = datetime.now().isoformat(timespec="seconds")
    with _lock:
        conn = get_conn()
        old = conn.execute(
            "SELECT * FROM facts WHERE entity_id=? AND predicate=? AND superseded=0",
            (entity_id, predicate),
        ).fetchone()
        conflict = False
        if old and old["value"] != value:
            conn.execute(
                "UPDATE facts SET superseded=1, valid_to=? WHERE id=?",
                (now, old["id"]),
            )
            conflict = True
        cur = conn.execute(
            "INSERT INTO facts(entity_id, predicate, value, valid_from, source_memory_id, created_at) "
            "VALUES(?,?,?,?,?,?)",
            (entity_id, predicate, value, now, source_memory_id, now),
        )
        conn.commit()
        return {"fact_id": int(cur.lastrowid), "conflict": conflict,
                "old_value": old["value"] if old else None}


def current_facts(entity_id: int) -> list[dict]:
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM facts WHERE entity_id=? AND superseded=0 ORDER BY created_at DESC",
        (entity_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def all_facts_with_conflict() -> list[dict]:
    """返回所有被取代（存在冲突）的事实，供健康度审计。"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT f.*, e.name AS entity_name FROM facts f "
        "JOIN entities e ON e.id=f.entity_id WHERE f.superseded=1"
    ).fetchall()
    return [dict(r) for r in rows]


# ── 日记 ──────────────────────────────────────────────────────────────────
def add_diary(day: str, text: str, mood: str | None = None) -> int:
    now = datetime.now().isoformat(timespec="seconds")
    with _lock:
        conn = get_conn()
        cur = conn.execute(
            "INSERT INTO diary(day, text, mood, created_at) VALUES(?,?,?,?)",
            (day, text, mood, now),
        )
        conn.commit()
        return int(cur.lastrowid)


def list_diary(day_from: str | None = None, day_to: str | None = None,
               limit: int = 100) -> list[dict]:
    conn = get_conn()
    sql = "SELECT * FROM diary WHERE 1=1"
    args: list = []
    if day_from:
        sql += " AND day>=?"
        args.append(day_from)
    if day_to:
        sql += " AND day<=?"
        args.append(day_to)
    sql += " ORDER BY day DESC, id DESC LIMIT ?"
    args.append(limit)
    rows = conn.execute(sql, args).fetchall()
    return [dict(r) for r in rows]


# ── 维护 ──────────────────────────────────────────────────────────────────
def vacuum() -> None:
    """压缩数据库（在健康度/快照流程中调用，释放空间）。"""
    with _lock:
        conn = get_conn()
        conn.execute("VACUUM")
        conn.commit()


def wipe_memories_only() -> int:
    """仅清空派生索引（记忆/图谱/事实），保留每日日志原文。用于重索引。"""
    with _lock:
        conn = get_conn()
        conn.execute("DELETE FROM memories")
        conn.execute("DELETE FROM relations")
        conn.execute("DELETE FROM facts")
        conn.execute("DELETE FROM entities")
        conn.commit()
        return 1


# ── 归档（forget 软删除）────────────────────────────────────────────────
def list_archive(limit: int = 200, offset: int = 0) -> list[dict]:
    """列出归档的记忆（forget 后可恢复）。"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM memories_archive ORDER BY archived_at DESC LIMIT ? OFFSET ?",
        (limit, offset)
    ).fetchall()
    return [dict(r) for r in rows]


def restore_from_archive(archive_id: int) -> dict:
    """从归档表恢复一条记忆。"""
    with _lock:
        conn = get_conn()
        row = conn.execute(
            "SELECT * FROM memories_archive WHERE id=?", (archive_id,)
        ).fetchone()
        if not row:
            return {"ok": False, "error": "NOT_FOUND"}
        d = dict(row)
        # 检查是否已恢复
        existing = conn.execute(
            "SELECT id FROM memories WHERE id=?", (d["original_id"],)
        ).fetchone()
        if existing:
            return {"ok": False, "error": "ALREADY_EXISTS"}
        cur = conn.execute(
            """INSERT INTO memories(id, day, source, raw_text, norm_hash, tokens_json,
                                    created_at, last_accessed, access_count, importance,
                                    version, namespace)
               VALUES(?,?,?,?,?,?,?,?,
                       COALESCE((SELECT access_count FROM memories WHERE id=?),0),
                       ?,1,?)""",
            (d["original_id"], d["day"], d["source"], d["raw_text"], d["norm_hash"],
             d["tokens_json"], d["day"] + "T00:00:00", d["day"] + "T00:00:00",
             d["original_id"], d["importance"], d["namespace"]),
        )
        conn.execute("DELETE FROM memories_archive WHERE id=?", (archive_id,))
        conn.commit()
        return {"ok": True, "restored_id": d["original_id"]}


def archive_count() -> int:
    """统计归档记忆数。"""
    conn = get_conn()
    return conn.execute("SELECT COUNT(*) FROM memories_archive").fetchone()[0]


if __name__ == "__main__":
    print("DB:", config.DB_PATH)
    print("memories:", count_memories(), "entities:", count_entities(),
          "relations:", count_relations())
