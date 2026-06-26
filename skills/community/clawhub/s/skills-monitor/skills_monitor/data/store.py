"""
数据存储层 — SQLite 本地数据库
存储 skill 运行记录、指标、隐性对话反馈等
"""

import json
import os
import sqlite3
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_DB_DIR = os.path.expanduser(os.environ.get("SKILLS_MONITOR_HOME", "~/.skills_monitor"))
DB_NAME = "skills_monitor.db"


class DataStore:
    """SQLite 数据存储"""

    def __init__(self, db_dir: str = DEFAULT_DB_DIR):
        Path(db_dir).mkdir(parents=True, exist_ok=True)
        self.db_path = os.path.join(db_dir, DB_NAME)
        self._local = threading.local()
        self._init_tables()

    @property
    def _conn(self) -> sqlite3.Connection:
        """每个线程一个连接"""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_path)
            self._local.conn.row_factory = sqlite3.Row
            self._local.conn.execute("PRAGMA journal_mode=WAL")
        return self._local.conn

    def _init_tables(self):
        """初始化表结构"""
        conn = self._conn
        conn.executescript("""
            -- skill 运行记录
            CREATE TABLE IF NOT EXISTS skill_runs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id      TEXT NOT NULL UNIQUE,
                agent_id    TEXT NOT NULL,
                skill_id    TEXT NOT NULL,
                task_name   TEXT,
                status      TEXT NOT NULL DEFAULT 'running',  -- running / success / error
                start_time  TEXT NOT NULL,
                end_time    TEXT,
                duration_ms REAL,
                input_data  TEXT,   -- JSON
                output_data TEXT,   -- JSON (truncated)
                error_msg   TEXT,
                metadata    TEXT,   -- JSON
                created_at  TEXT NOT NULL DEFAULT (datetime('now'))
            );

            -- 聚合指标（按 skill_id 汇总）
            CREATE TABLE IF NOT EXISTS skill_metrics (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id        TEXT NOT NULL,
                skill_id        TEXT NOT NULL,
                date            TEXT NOT NULL,            -- YYYY-MM-DD
                total_runs      INTEGER NOT NULL DEFAULT 0,
                success_count   INTEGER NOT NULL DEFAULT 0,
                error_count     INTEGER NOT NULL DEFAULT 0,
                avg_duration_ms REAL,
                p95_duration_ms REAL,
                min_duration_ms REAL,
                max_duration_ms REAL,
                updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
                UNIQUE(agent_id, skill_id, date)
            );

            -- 旧版用户反馈表（已废弃，保留兼容）
            CREATE TABLE IF NOT EXISTS user_feedback (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id    TEXT NOT NULL,
                skill_id    TEXT NOT NULL,
                rating      INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
                comment     TEXT,
                sentiment   TEXT,
                run_id      TEXT,
                created_at  TEXT NOT NULL DEFAULT (datetime('now'))
            );

            -- 隐性对话反馈（取代人工评分）
            CREATE TABLE IF NOT EXISTS implicit_feedback (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id          TEXT NOT NULL,
                skill_id          TEXT NOT NULL,
                run_id            TEXT,
                implicit_rating   REAL NOT NULL,         -- 1.0-5.0 推断评分
                confidence        REAL NOT NULL,          -- 0.0-1.0 置信度
                sentiment_label   TEXT,                   -- positive/neutral/negative
                dimensions        TEXT,                   -- JSON: 5维度详细分数
                evidence          TEXT,                   -- JSON: 支撑证据列表
                source            TEXT DEFAULT 'conversation', -- 来源标识
                user_messages_count INTEGER DEFAULT 0,
                run_status        TEXT,                   -- success/error
                retry_count       INTEGER DEFAULT 0,
                created_at        TEXT NOT NULL DEFAULT (datetime('now'))
            );

            -- 索引
            CREATE INDEX IF NOT EXISTS idx_runs_skill ON skill_runs(skill_id, start_time);
            CREATE INDEX IF NOT EXISTS idx_runs_agent ON skill_runs(agent_id, start_time);
            CREATE INDEX IF NOT EXISTS idx_metrics_skill ON skill_metrics(skill_id, date);
            CREATE INDEX IF NOT EXISTS idx_feedback_skill ON user_feedback(skill_id, created_at);
            CREATE INDEX IF NOT EXISTS idx_implicit_fb_skill ON implicit_feedback(skill_id, created_at);
            CREATE INDEX IF NOT EXISTS idx_implicit_fb_agent ON implicit_feedback(agent_id, skill_id);
        """)
        conn.commit()

    # ──────── 写入 ────────

    def insert_run(self, run: Dict[str, Any]) -> None:
        """插入一条运行记录"""
        self._conn.execute(
            """INSERT INTO skill_runs 
               (run_id, agent_id, skill_id, task_name, status,
                start_time, end_time, duration_ms,
                input_data, output_data, error_msg, metadata)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                run["run_id"],
                run["agent_id"],
                run["skill_id"],
                run.get("task_name", ""),
                run["status"],
                run["start_time"],
                run.get("end_time"),
                run.get("duration_ms"),
                json.dumps(run.get("input_data"), ensure_ascii=False) if run.get("input_data") else None,
                _truncate_json(run.get("output_data")),
                run.get("error_msg"),
                json.dumps(run.get("metadata"), ensure_ascii=False) if run.get("metadata") else None,
            ),
        )
        self._conn.commit()

    def update_run(self, run_id: str, **kwargs) -> None:
        """更新运行记录"""
        allowed = {"status", "end_time", "duration_ms", "output_data", "error_msg"}
        updates = {k: v for k, v in kwargs.items() if k in allowed}
        if not updates:
            return
        if "output_data" in updates:
            updates["output_data"] = _truncate_json(updates["output_data"])

        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [run_id]
        self._conn.execute(
            f"UPDATE skill_runs SET {set_clause} WHERE run_id = ?",
            values,
        )
        self._conn.commit()

    def insert_feedback(self, feedback: Dict[str, Any]) -> None:
        """[已废弃] 插入旧版用户反馈 — 保留向后兼容"""
        self._conn.execute(
            """INSERT INTO user_feedback 
               (agent_id, skill_id, rating, comment, sentiment, run_id)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                feedback["agent_id"],
                feedback["skill_id"],
                feedback["rating"],
                feedback.get("comment", ""),
                feedback.get("sentiment", "neutral"),
                feedback.get("run_id"),
            ),
        )
        self._conn.commit()

    def insert_implicit_feedback(self, feedback: Dict[str, Any]) -> None:
        """插入隐性对话反馈"""
        self._conn.execute(
            """INSERT INTO implicit_feedback
               (agent_id, skill_id, run_id, implicit_rating, confidence,
                sentiment_label, dimensions, evidence, source,
                user_messages_count, run_status, retry_count)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                feedback["agent_id"],
                feedback["skill_id"],
                feedback.get("run_id"),
                feedback["implicit_rating"],
                feedback["confidence"],
                feedback.get("sentiment_label", "neutral"),
                json.dumps(feedback.get("dimensions", {}), ensure_ascii=False),
                json.dumps(feedback.get("evidence", []), ensure_ascii=False),
                feedback.get("source", "conversation"),
                feedback.get("user_messages_count", 0),
                feedback.get("run_status"),
                feedback.get("retry_count", 0),
            ),
        )
        self._conn.commit()

    def upsert_daily_metrics(self, agent_id: str, skill_id: str, date: str) -> None:
        """重新计算并更新某天的聚合指标"""
        rows = self._conn.execute(
            """SELECT duration_ms, status FROM skill_runs
               WHERE agent_id = ? AND skill_id = ? 
               AND date(start_time) = ?""",
            (agent_id, skill_id, date),
        ).fetchall()

        if not rows:
            return

        durations = [r["duration_ms"] for r in rows if r["duration_ms"] is not None]
        total = len(rows)
        success = sum(1 for r in rows if r["status"] == "success")
        errors = sum(1 for r in rows if r["status"] == "error")

        avg_d = sum(durations) / len(durations) if durations else None
        sorted_d = sorted(durations) if durations else []
        p95_d = sorted_d[int(len(sorted_d) * 0.95)] if sorted_d else None
        min_d = min(sorted_d) if sorted_d else None
        max_d = max(sorted_d) if sorted_d else None

        self._conn.execute(
            """INSERT INTO skill_metrics 
               (agent_id, skill_id, date, total_runs, success_count, error_count,
                avg_duration_ms, p95_duration_ms, min_duration_ms, max_duration_ms, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
               ON CONFLICT(agent_id, skill_id, date) DO UPDATE SET
                total_runs = excluded.total_runs,
                success_count = excluded.success_count,
                error_count = excluded.error_count,
                avg_duration_ms = excluded.avg_duration_ms,
                p95_duration_ms = excluded.p95_duration_ms,
                min_duration_ms = excluded.min_duration_ms,
                max_duration_ms = excluded.max_duration_ms,
                updated_at = excluded.updated_at""",
            (agent_id, skill_id, date, total, success, errors, avg_d, p95_d, min_d, max_d),
        )
        self._conn.commit()

    # ──────── 查询 ────────

    def get_runs(
        self,
        skill_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 50,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """查询运行记录"""
        conditions = []
        params: list = []
        if skill_id:
            conditions.append("skill_id = ?")
            params.append(skill_id)
        if agent_id:
            conditions.append("agent_id = ?")
            params.append(agent_id)
        if status:
            conditions.append("status = ?")
            params.append(status)

        where = "WHERE " + " AND ".join(conditions) if conditions else ""
        rows = self._conn.execute(
            f"SELECT * FROM skill_runs {where} ORDER BY start_time DESC LIMIT ?",
            params + [limit],
        ).fetchall()
        return [dict(r) for r in rows]

    def get_metrics(
        self,
        skill_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        days: int = 7,
    ) -> List[Dict[str, Any]]:
        """查询聚合指标"""
        conditions = ["date >= date('now', ?)"]
        params: list = [f"-{days} days"]
        if skill_id:
            conditions.append("skill_id = ?")
            params.append(skill_id)
        if agent_id:
            conditions.append("agent_id = ?")
            params.append(agent_id)

        where = "WHERE " + " AND ".join(conditions)
        rows = self._conn.execute(
            f"SELECT * FROM skill_metrics {where} ORDER BY date DESC",
            params,
        ).fetchall()
        return [dict(r) for r in rows]

    def get_feedback(
        self,
        skill_id: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """[已废弃] 查询旧版用户反馈 — 保留向后兼容"""
        if skill_id:
            rows = self._conn.execute(
                "SELECT * FROM user_feedback WHERE skill_id = ? ORDER BY created_at DESC LIMIT ?",
                (skill_id, limit),
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM user_feedback ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]

    def get_implicit_feedback(
        self,
        skill_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """查询隐性对话反馈"""
        conditions = []
        params: list = []
        if skill_id:
            conditions.append("skill_id = ?")
            params.append(skill_id)
        if agent_id:
            conditions.append("agent_id = ?")
            params.append(agent_id)

        where = "WHERE " + " AND ".join(conditions) if conditions else ""
        rows = self._conn.execute(
            f"SELECT * FROM implicit_feedback {where} ORDER BY created_at DESC LIMIT ?",
            params + [limit],
        ).fetchall()

        results = []
        for r in rows:
            d = dict(r)
            # 反序列化 JSON 字段
            if d.get("dimensions"):
                try:
                    d["dimensions"] = json.loads(d["dimensions"])
                except (json.JSONDecodeError, TypeError):
                    pass
            if d.get("evidence"):
                try:
                    d["evidence"] = json.loads(d["evidence"])
                except (json.JSONDecodeError, TypeError):
                    pass
            results.append(d)
        return results

    def get_skill_summary(self, skill_id: str, agent_id: str) -> Dict[str, Any]:
        """获取某个 skill 的汇总信息（使用隐性评分替代人工评分）"""
        total = self._conn.execute(
            "SELECT COUNT(*) as cnt FROM skill_runs WHERE skill_id=? AND agent_id=?",
            (skill_id, agent_id),
        ).fetchone()["cnt"]

        success = self._conn.execute(
            "SELECT COUNT(*) as cnt FROM skill_runs WHERE skill_id=? AND agent_id=? AND status='success'",
            (skill_id, agent_id),
        ).fetchone()["cnt"]

        avg_dur = self._conn.execute(
            "SELECT AVG(duration_ms) as avg_d FROM skill_runs WHERE skill_id=? AND agent_id=? AND status='success'",
            (skill_id, agent_id),
        ).fetchone()["avg_d"]

        # 隐性评分：置信度加权平均
        implicit_row = self._conn.execute(
            """SELECT 
                SUM(implicit_rating * confidence) as weighted_sum,
                SUM(confidence) as weight_total,
                COUNT(*) as fb_count,
                AVG(confidence) as avg_conf
               FROM implicit_feedback 
               WHERE skill_id=? AND agent_id=?""",
            (skill_id, agent_id),
        ).fetchone()

        avg_implicit_rating = None
        implicit_feedback_count = 0
        avg_confidence = None

        if implicit_row and implicit_row["weight_total"] and implicit_row["weight_total"] > 0:
            avg_implicit_rating = round(
                implicit_row["weighted_sum"] / implicit_row["weight_total"], 2
            )
            implicit_feedback_count = implicit_row["fb_count"]
            avg_confidence = round(implicit_row["avg_conf"], 3) if implicit_row["avg_conf"] else None

        return {
            "skill_id": skill_id,
            "total_runs": total,
            "success_count": success,
            "success_rate": round(success / total * 100, 1) if total > 0 else 0,
            "avg_duration_ms": round(avg_dur, 1) if avg_dur else None,
            "avg_rating": avg_implicit_rating,         # 现在来自隐性评分
            "implicit_feedback_count": implicit_feedback_count,
            "avg_confidence": avg_confidence,
        }

    def close(self):
        if hasattr(self._local, "conn") and self._local.conn:
            self._local.conn.close()
            self._local.conn = None


def _truncate_json(data: Any, max_len: int = 2000) -> Optional[str]:
    """将数据转 JSON 并截断"""
    if data is None:
        return None
    text = json.dumps(data, ensure_ascii=False, default=str)
    if len(text) > max_len:
        return text[:max_len] + "...(truncated)"
    return text
