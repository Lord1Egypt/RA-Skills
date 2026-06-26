"""
数据库模型定义

使用 SQLite 存储技能使用日志、健康度评分和用户反馈
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class SkillUsage:
    """技能使用记录"""
    id: Optional[int] = None
    skill_name: str = ""
    action: str = ""
    status: str = ""  # success, failed, timeout
    duration_ms: int = 0
    timestamp: Optional[datetime] = None
    context: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


@dataclass
class HealthScore:
    """技能健康度评分"""
    id: Optional[int] = None
    skill_name: str = ""
    success_rate: float = 0.0  # 0-100
    avg_duration_ms: float = 0.0
    usage_count: int = 0
    last_check: Optional[datetime] = None
    score: int = 0  # 综合评分 0-100
    issues: Optional[str] = None  # JSON 格式的问题列表


@dataclass
class Feedback:
    """用户反馈"""
    id: Optional[int] = None
    skill_name: str = ""
    rating: int = 0  # 1-5
    comment: Optional[str] = None
    timestamp: Optional[datetime] = None
    user_id: Optional[str] = None


class Database:
    """SQLite 数据库管理类"""
    
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            # 默认存储在用户目录下
            home = Path.home()
            db_dir = home / ".openclaw" / "skill-evolver"
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = db_dir / "skill_evolver.db"
        
        self.db_path = str(db_path)
        self._init_db()
    
    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_db(self):
        """初始化数据库表"""
        with self._get_connection() as conn:
            # 技能使用日志表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS skill_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_name TEXT NOT NULL,
                    action TEXT NOT NULL,
                    status TEXT NOT NULL,
                    duration_ms INTEGER DEFAULT 0,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    context TEXT,
                    error_message TEXT
                )
            """)
            
            # 健康度评分表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS health_score (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_name TEXT NOT NULL UNIQUE,
                    success_rate REAL DEFAULT 0,
                    avg_duration_ms REAL DEFAULT 0,
                    usage_count INTEGER DEFAULT 0,
                    last_check DATETIME,
                    score INTEGER DEFAULT 0,
                    issues TEXT
                )
            """)
            
            # 用户反馈表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_name TEXT NOT NULL,
                    rating INTEGER DEFAULT 0,
                    comment TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_id TEXT
                )
            """)
            
            # 创建索引
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_usage_skill_name 
                ON skill_usage(skill_name)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_usage_timestamp 
                ON skill_usage(timestamp)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_feedback_skill_name 
                ON feedback(skill_name)
            """)
            
            conn.commit()
    
    # ===== SkillUsage 操作 =====
    
    def log_usage(self, usage: SkillUsage) -> int:
        """记录技能使用"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO skill_usage 
                (skill_name, action, status, duration_ms, timestamp, context, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                usage.skill_name,
                usage.action,
                usage.status,
                usage.duration_ms,
                usage.timestamp or datetime.now(),
                json.dumps(usage.context) if usage.context else None,
                usage.error_message
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_usage_stats(self, skill_name: str, days: int = 30) -> Dict[str, Any]:
        """获取技能使用统计"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success,
                    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                    AVG(duration_ms) as avg_duration,
                    MAX(duration_ms) as max_duration,
                    MIN(duration_ms) as min_duration
                FROM skill_usage
                WHERE skill_name = ? 
                AND timestamp >= datetime('now', '-{} days')
            """.format(days), (skill_name,))
            
            row = cursor.fetchone()
            return {
                "total": row["total"] or 0,
                "success": row["success"] or 0,
                "failed": row["failed"] or 0,
                "avg_duration_ms": round(row["avg_duration"] or 0, 2),
                "max_duration_ms": row["max_duration"] or 0,
                "min_duration_ms": row["min_duration"] or 0,
            }
    
    def get_recent_usage(self, skill_name: str, limit: int = 100) -> List[SkillUsage]:
        """获取最近的技能使用记录"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM skill_usage
                WHERE skill_name = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (skill_name, limit))
            
            return [
                SkillUsage(
                    id=row["id"],
                    skill_name=row["skill_name"],
                    action=row["action"],
                    status=row["status"],
                    duration_ms=row["duration_ms"],
                    timestamp=datetime.fromisoformat(row["timestamp"]),
                    context=json.loads(row["context"]) if row["context"] else None,
                    error_message=row["error_message"]
                )
                for row in cursor.fetchall()
            ]
    
    # ===== HealthScore 操作 =====
    
    def update_health_score(self, score: HealthScore) -> int:
        """更新健康度评分"""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO health_score
                (skill_name, success_rate, avg_duration_ms, usage_count, last_check, score, issues)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                score.skill_name,
                score.success_rate,
                score.avg_duration_ms,
                score.usage_count,
                score.last_check or datetime.now(),
                score.score,
                json.dumps(score.issues) if isinstance(score.issues, list) else score.issues
            ))
            conn.commit()
            return conn.execute(
                "SELECT id FROM health_score WHERE skill_name = ?", 
                (score.skill_name,)
            ).fetchone()["id"]
    
    def get_health_score(self, skill_name: str) -> Optional[HealthScore]:
        """获取技能健康度评分"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM health_score WHERE skill_name = ?", 
                (skill_name,)
            )
            row = cursor.fetchone()
            
            if row:
                return HealthScore(
                    id=row["id"],
                    skill_name=row["skill_name"],
                    success_rate=row["success_rate"],
                    avg_duration_ms=row["avg_duration_ms"],
                    usage_count=row["usage_count"],
                    last_check=datetime.fromisoformat(row["last_check"]) if row["last_check"] else None,
                    score=row["score"],
                    issues=json.loads(row["issues"]) if row["issues"] else []
                )
            return None
    
    def get_all_health_scores(self) -> List[HealthScore]:
        """获取所有技能的健康度评分"""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM health_score ORDER BY score DESC")
            
            return [
                HealthScore(
                    id=row["id"],
                    skill_name=row["skill_name"],
                    success_rate=row["success_rate"],
                    avg_duration_ms=row["avg_duration_ms"],
                    usage_count=row["usage_count"],
                    last_check=datetime.fromisoformat(row["last_check"]) if row["last_check"] else None,
                    score=row["score"],
                    issues=json.loads(row["issues"]) if row["issues"] else []
                )
                for row in cursor.fetchall()
            ]
    
    # ===== Feedback 操作 =====
    
    def add_feedback(self, feedback: Feedback) -> int:
        """添加用户反馈"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO feedback
                (skill_name, rating, comment, timestamp, user_id)
                VALUES (?, ?, ?, ?, ?)
            """, (
                feedback.skill_name,
                feedback.rating,
                feedback.comment,
                feedback.timestamp or datetime.now(),
                feedback.user_id
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_feedback_stats(self, skill_name: str) -> Dict[str, Any]:
        """获取技能反馈统计"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total,
                    AVG(rating) as avg_rating,
                    SUM(CASE WHEN rating = 5 THEN 1 ELSE 0 END) as five_star,
                    SUM(CASE WHEN rating = 4 THEN 1 ELSE 0 END) as four_star,
                    SUM(CASE WHEN rating = 3 THEN 1 ELSE 0 END) as three_star,
                    SUM(CASE WHEN rating = 2 THEN 1 ELSE 0 END) as two_star,
                    SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END) as one_star
                FROM feedback
                WHERE skill_name = ?
            """, (skill_name,))
            
            row = cursor.fetchone()
            return {
                "total": row["total"] or 0,
                "avg_rating": round(row["avg_rating"] or 0, 2),
                "distribution": {
                    5: row["five_star"] or 0,
                    4: row["four_star"] or 0,
                    3: row["three_star"] or 0,
                    2: row["two_star"] or 0,
                    1: row["one_star"] or 0,
                }
            }
    
    def get_recent_feedback(self, skill_name: str, limit: int = 50) -> List[Feedback]:
        """获取最近的反馈"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM feedback
                WHERE skill_name = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (skill_name, limit))
            
            return [
                Feedback(
                    id=row["id"],
                    skill_name=row["skill_name"],
                    rating=row["rating"],
                    comment=row["comment"],
                    timestamp=datetime.fromisoformat(row["timestamp"]),
                    user_id=row["user_id"]
                )
                for row in cursor.fetchall()
            ]
    
    # ===== 通用操作 =====
    
    def get_all_skills(self) -> List[str]:
        """获取所有已记录的技能名称"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT DISTINCT skill_name FROM skill_usage
                UNION
                SELECT DISTINCT skill_name FROM health_score
                UNION
                SELECT DISTINCT skill_name FROM feedback
                ORDER BY skill_name
            """)
            return [row["skill_name"] for row in cursor.fetchall()]
    
    def clear_old_data(self, days: int = 90):
        """清理旧数据"""
        with self._get_connection() as conn:
            conn.execute("""
                DELETE FROM skill_usage
                WHERE timestamp < datetime('now', '-{} days')
            """.format(days))
            conn.execute("""
                DELETE FROM feedback
                WHERE timestamp < datetime('now', '-{} days')
            """.format(days))
            conn.commit()
