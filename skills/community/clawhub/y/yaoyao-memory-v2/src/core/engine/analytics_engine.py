#!/usr/bin/env python3
"""Analytics Engine - 分析引擎"""

import sqlite3
from pathlib import Path
from typing import Dict, List
from collections import Counter


class AnalyticsEngine:
    """分析引擎 - 记忆统计分析"""
    
    def __init__(self):
        self.db_path = Path.home() / ".openclaw" / "workspace" / "memory" / "memory.db"
    
    def run(self) -> Dict:
        """执行分析"""
        if not self.db_path.exists():
            return {"status": "error", "message": "Database not found"}
        
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # 总数
            cursor.execute("SELECT COUNT(*) FROM memory")
            total = cursor.fetchone()[0]
            
            # 类型分布
            cursor.execute("SELECT type, COUNT(*) FROM memory GROUP BY type")
            types = dict(cursor.fetchall())
            
            # 重要性分布
            cursor.execute("SELECT importance, COUNT(*) FROM memory GROUP BY importance")
            importance = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                "status": "ok",
                "total": total,
                "types": types,
                "importance": importance,
                "health_score": self._calc_health_score(total, types, importance),
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _calc_health_score(self, total: int, types: Dict, importance: Dict) -> int:
        """计算健康分数"""
        score = 60  # 基础分
        
        if total >= 50:
            score += 20
        elif total >= 20:
            score += 10
        
        if types.get("decision", 0) >= 3:
            score += 10
        
        if importance.get("high", 0) + importance.get("critical", 0) >= 5:
            score += 10
        
        return min(score, 100)
