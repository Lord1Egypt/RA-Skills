"""
SQLite 数据库存储
"""
import aiosqlite
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path


class Database:
    """SQLite 数据库"""
    
    def __init__(self, db_path: str = "workswith_claw.db"):
        self.db_path = db_path
        self._conn: Optional[aiosqlite.Connection] = None
    
    async def init_db(self):
        """初始化数据库"""
        self._conn = await aiosqlite.connect(self.db_path)
        
        # 创表
        await self._conn.execute("""
            CREATE TABLE IF NOT EXISTS device_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_id TEXT NOT NULL,
                state TEXT,
                attributes TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await self._conn.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                utterance TEXT NOT NULL,
                intent TEXT,
                result TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await self._conn.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_id TEXT NOT NULL UNIQUE,
                typical_on_time TEXT,
                typical_off_time TEXT,
                confidence REAL DEFAULT 0,
                sample_count INTEGER DEFAULT 0,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await self._conn.execute("""
            CREATE TABLE IF NOT EXISTS suggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_id TEXT NOT NULL,
                suggestion_type TEXT,
                trigger_time TEXT,
                action TEXT,
                message TEXT,
                confidence REAL,
                status TEXT DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await self._conn.commit()
    
    async def close(self):
        """关闭连接"""
        if self._conn:
            await self._conn.close()
    
    # ========== Device States ==========
    
    async def insert_state(self, entity_id: str, state: str, attributes: dict = None):
        """插入设备状态"""
        await self._conn.execute(
            "INSERT INTO device_states (entity_id, state, attributes) VALUES (?, ?, ?)",
            (entity_id, state, json.dumps(attributes) if attributes else None)
        )
        await self._conn.commit()
    
    async def get_states(self, entity_id: str = None, limit: int = 100) -> List[Dict]:
        """获取设备状态"""
        if entity_id:
            cursor = await self._conn.execute(
                "SELECT entity_id, state, attributes, timestamp FROM device_states WHERE entity_id = ? ORDER BY timestamp DESC LIMIT ?",
                (entity_id, limit)
            )
        else:
            cursor = await self._conn.execute(
                "SELECT entity_id, state, attributes, timestamp FROM device_states ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
        
        rows = await cursor.fetchall()
        return [
            {
                "entity_id": r[0],
                "state": r[1],
                "attributes": json.loads(r[2]) if r[2] else None,
                "timestamp": r[3]
            }
            for r in rows
        ]
    
    # ========== Interactions ==========
    
    async def insert_interaction(self, utterance: str, intent: str, result: str):
        """记录交互"""
        await self._conn.execute(
            "INSERT INTO interactions (utterance, intent, result) VALUES (?, ?, ?)",
            (utterance, intent, result)
        )
        await self._conn.commit()
    
    async def get_interactions(self, limit: int = 100) -> List[Dict]:
        """获取交互历史"""
        cursor = await self._conn.execute(
            "SELECT utterance, intent, result, timestamp FROM interactions ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        rows = await cursor.fetchall()
        return [
            {"utterance": r[0], "intent": r[1], "result": r[2], "timestamp": r[3]}
            for r in rows
        ]
    
    # ========== Habits ==========
    
    async def upsert_habit(
        self, 
        entity_id: str, 
        typical_on_time: str = None,
        typical_off_time: str = None,
        confidence: float = 0,
        sample_count: int = 0
    ):
        """更新习惯"""
        await self._conn.execute("""
            INSERT INTO habits (entity_id, typical_on_time, typical_off_time, confidence, sample_count, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(entity_id) DO UPDATE SET
                typical_on_time = excluded.typical_on_time,
                typical_off_time = excluded.typical_off_time,
                confidence = excluded.confidence,
                sample_count = excluded.sample_count,
                updated_at = CURRENT_TIMESTAMP
        """, (entity_id, typical_on_time, typical_off_time, confidence, sample_count))
        await self._conn.commit()
    
    async def get_habits(self) -> List[Dict]:
        """获取所有习惯"""
        cursor = await self._conn.execute(
            "SELECT entity_id, typical_on_time, typical_off_time, confidence, sample_count, updated_at FROM habits"
        )
        rows = await cursor.fetchall()
        return [
            {
                "entity_id": r[0],
                "typical_on_time": r[1],
                "typical_off_time": r[2],
                "confidence": r[3],
                "sample_count": r[4],
                "updated_at": r[5]
            }
            for r in rows
        ]
    
    # ========== Suggestions ==========
    
    async def insert_suggestion(
        self,
        entity_id: str,
        suggestion_type: str,
        trigger_time: str,
        action: dict,
        message: str,
        confidence: float
    ):
        """插入建议"""
        await self._conn.execute("""
            INSERT INTO suggestions (entity_id, suggestion_type, trigger_time, action, message, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (entity_id, suggestion_type, trigger_time, json.dumps(action), message, confidence))
        await self._conn.commit()
    
    async def update_suggestion_status(self, entity_id: str, status: str):
        """更新建议状态"""
        await self._conn.execute(
            "UPDATE suggestions SET status = ? WHERE entity_id = ?",
            (status, entity_id)
        )
        await self._conn.commit()
    
    async def get_pending_suggestions(self) -> List[Dict]:
        """获取待确认的建议"""
        cursor = await self._conn.execute(
            "SELECT entity_id, suggestion_type, trigger_time, action, message, confidence, status FROM suggestions WHERE status = 'pending'"
        )
        rows = await cursor.fetchall()
        return [
            {
                "entity_id": r[0],
                "suggestion_type": r[1],
                "trigger_time": r[2],
                "action": json.loads(r[3]) if r[3] else {},
                "message": r[4],
                "confidence": r[5],
                "status": r[6]
            }
            for r in rows
        ]


# 全局数据库实例
db = Database()
