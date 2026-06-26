#!/usr/bin/env python3
"""Recall Engine - 记忆召回引擎"""

from typing import Dict, List, Optional


class RecallEngine:
    """召回引擎 - 根据上下文召回相关记忆"""
    
    def run(self, query: str, context: Optional[Dict] = None) -> List[Dict]:
        """执行召回"""
        from .search_engine import SearchEngine
        
        search = SearchEngine()
        results = search.query(query, limit=10)
        
        # 上下文过滤
        if context:
            results = self._filter_by_context(results, context)
        
        return results
    
    def _filter_by_context(self, results: List[Dict], context: Dict) -> List[Dict]:
        """根据上下文过滤"""
        # 简单实现：按类型过滤
        ctx_type = context.get("type")
        if ctx_type:
            return [r for r in results if r.get("type") == ctx_type]
        return results
