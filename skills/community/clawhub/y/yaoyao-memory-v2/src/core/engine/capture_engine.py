#!/usr/bin/env python3
"""Capture Engine - 记忆捕获引擎"""

from typing import Dict, Optional
from datetime import datetime


class CaptureEngine:
    """捕获引擎 - 从对话中捕获记忆"""
    
    def run(self, content: str, metadata: Optional[Dict] = None) -> Dict:
        """执行捕获"""
        meta = metadata or {}
        
        # 提取关键信息
        extracted = self._extract(content)
        
        # 存储
        from .sqlite_store import SQLiteStore
        store = SQLiteStore()
        row_id = store.insert(content, {**meta, **extracted})
        
        return {
            "status": "captured",
            "id": row_id,
            "extracted": extracted,
            "timestamp": datetime.now().isoformat(),
        }
    
    def _extract(self, content: str) -> Dict:
        """提取元数据"""
        # 简单关键词提取
        keywords = []
        important_markers = ["重要", "关键", "记住", "不要", "必须", "决策"]
        
        for marker in important_markers:
            if marker in content:
                keywords.append(marker)
        
        return {
            "keywords": keywords[:5],
            "auto_tags": ["captured"] + keywords,
        }
