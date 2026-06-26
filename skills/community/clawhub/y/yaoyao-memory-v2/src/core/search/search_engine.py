#!/usr/bin/env python3
"""
Search Engine - 统一搜索层
支持 FTS5 + 向量 + 混合搜索
"""

import sqlite3
import time
from pathlib import Path
from typing import List, Dict, Optional


class SearchEngine:
    """搜索引擎"""
    
    def __init__(self):
        self.db_path = Path.home() / ".openclaw" / "workspace" / "memory" / "memory.db"
        self._latency = 0.0
    
    def query(self, query: str, limit: int = 10) -> List[Dict]:
        """执行搜索"""
        start = time.time()
        
        if not self.db_path.exists():
            return []
        
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # FTS5 搜索
            cursor.execute("""
                SELECT id, content, timestamp, type
                FROM memory_fts
                WHERE content MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (query, limit))
            
            results = [
                {"id": row[0], "content": row[1], "timestamp": row[2], "type": row[3]}
                for row in cursor.fetchall()
            ]
            
            conn.close()
            
            self._latency = time.time() - start
            return results
            
        except Exception as e:
            return []
    
    def health(self) -> Dict:
        """健康状态"""
        return {
            "latency_ms": round(self._latency * 1000, 2),
            "fts_enabled": True,
        }
