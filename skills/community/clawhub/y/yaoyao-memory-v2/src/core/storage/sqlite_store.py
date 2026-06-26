#!/usr/bin/env python3
"""
SQLite Store - 统一存储层
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class SQLiteStore:
    """SQLite 存储"""
    
    def __init__(self):
        self.db_path = Path.home() / ".openclaw" / "workspace" / "memory" / "memory.db"
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        if not self.db_path.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.db_path.touch()
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # 创建表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                type TEXT DEFAULT 'info',
                importance TEXT DEFAULT 'normal',
                tags TEXT DEFAULT '[]'
            )
        """)
        
        # FTS5 索引
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                content,
                content=memory,
                content_rowid=id
            )
        """)
        
        conn.commit()
        conn.close()
    
    def insert(self, content: str, metadata: Optional[Dict] = None) -> int:
        """插入记忆"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        meta = metadata or {}
        cursor.execute("""
            INSERT INTO memory (content, timestamp, type, importance, tags)
            VALUES (?, ?, ?, ?, ?)
        """, (
            content,
            datetime.now().isoformat(),
            meta.get("type", "info"),
            meta.get("importance", "normal"),
            json.dumps(meta.get("tags", []))
        ))
        
        row_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return row_id
    
    def query(self, sql: str, params: tuple = ()) -> List[Dict]:
        """查询"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(sql, params)
        results = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def health(self) -> Dict:
        """健康状态"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM memory")
            count = cursor.fetchone()[0]
            conn.close()
            return {"status": "ok", "records": count}
        except:
            return {"status": "error", "records": 0}


import json
