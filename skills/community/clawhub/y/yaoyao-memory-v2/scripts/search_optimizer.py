#!/usr/bin/env python3
"""
搜索优化模块 - v1.0.0
提升记忆搜索的相关性算法

功能：
1. 语义相似度优化（考虑词向量）
2. 关键词权重调整
3. 搜索结果重排序（Rerank）
4. 搜索历史学习
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import Counter

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"

# 停用词
STOPWORDS = {"的", "了", "是", "在", "我", "你", "他", "这", "那", "和", "与", "或", "以及", "对于", "关于", "一个", "一些", "什么", "怎么", "如何", "为什么"}

# 关键词重要性权重
KEYWORD_WEIGHTS = {
    "决策": 3.0,
    "决定": 3.0,
    "重要": 2.5,
    "优先": 2.5,
    "关键": 2.5,
    "错误": 2.0,
    "失败": 2.0,
    "问题": 1.5,
    "完成": 1.5,
    "新增": 1.5,
    "优化": 1.5,
    "修复": 1.5,
    "学习": 1.2,
    "了解": 1.0,
}

class SearchOptimizer:
    """搜索优化器"""
    
    def __init__(self):
        self.memory_dir = MEMORY_DIR
    
    def extract_keywords(self, text: str) -> List[Tuple[str, float]]:
        """提取关键词及其权重"""
        # 分词
        words = re.findall(r'[\w]+', text.lower())
        
        keywords = []
        for w in words:
            if len(w) >= 2 and w not in STOPWORDS:
                weight = KEYWORD_WEIGHTS.get(w, 1.0)
                keywords.append((w, weight))
        
        return keywords
    
    def calculate_relevance(self, query: str, content: str, title: str = "") -> float:
        """
        计算内容与查询的相关性分数
        """
        query_lower = query.lower()
        content_lower = content.lower()
        title_lower = title.lower()
        
        # 基础分
        score = 0.0
        
        # 提取查询关键词
        query_keywords = self.extract_keywords(query)
        
        # 计算标题匹配（标题权重更高）
        title_matches = 0
        for kw, weight in query_keywords:
            if kw in title_lower:
                title_matches += weight * 2  # 标题双倍权重
        
        score += title_matches
        
        # 计算内容匹配
        content_matches = 0
        for kw, weight in query_keywords:
            count = content_lower.count(kw)
            if count > 0:
                # 位置权重（前面的匹配更重要）
                first_pos = content_lower.find(kw)
                position_weight = max(0.5, 1.0 - first_pos / len(content) * 0.5)
                content_matches += weight * count * position_weight
        
        score += content_matches * 0.5
        
        # 计算查询词完整匹配（整个查询在内容中）
        if query_lower in content_lower:
            score += 5.0
        
        if query_lower in title_lower:
            score += 10.0
        
        # 归一化
        return round(score, 2)
    
    def rerank_results(self, query: str, results: List[Dict], top_k: int = 5) -> List[Dict]:
        """
        重排序搜索结果
        - query: 搜索查询
        - results: 原始搜索结果（来自向量搜索）
        - top_k: 返回数量
        """
        reranked = []
        
        for r in results:
            content = r.get("content", "")
            title = r.get("title", r.get("filename", ""))
            
            # 计算新的相关性分数
            relevance = self.calculate_relevance(query, content, title)
            
            # 结合原始分数（如果有）
            original_score = r.get("score", 0.5)
            
            # 综合分数 = 语义分数 * 0.6 + 关键词分数 * 0.4
            combined_score = original_score * 0.6 + (relevance / 100) * 0.4
            
            reranked.append({
                **r,
                "relevance": relevance,
                "combined_score": round(combined_score, 4),
                "rerank_reason": self._explain_score(relevance, title, content, query)
            })
        
        # 按综合分数排序
        reranked.sort(key=lambda x: x["combined_score"], reverse=True)
        
        return reranked[:top_k]
    
    def _explain_score(self, relevance: float, title: str, content: str, query: str) -> str:
        """解释分数来源"""
        reasons = []
        
        query_lower = query.lower()
        title_lower = title.lower()
        content_lower = content.lower()
        
        if query_lower in title_lower:
            reasons.append("标题精确匹配")
        elif any(kw in title_lower for kw in query_lower.split()):
            reasons.append("标题部分匹配")
        
        if relevance > 50:
            reasons.append("高关键词密度")
        elif relevance > 20:
            reasons.append("中关键词密度")
        
        return "; ".join(reasons) if reasons else "基础匹配"
    
    def search_with_boost(self, query: str, memory_contents: List[Dict], top_k: int = 5) -> List[Dict]:
        """
        带权重提升的搜索
        """
        scored = []
        
        for mem in memory_contents:
            content = mem.get("content", "")
            title = mem.get("title", mem.get("filename", ""))
            filename = mem.get("filename", "")
            
            score = self.calculate_relevance(query, content, title)
            
            # 时间权重：新记忆略微提升
            if "mtime" in mem:
                mtime = datetime.fromisoformat(mem["mtime"]) if isinstance(mem["mtime"], str) else mem["mtime"]
                days_ago = (datetime.now() - mtime).days
                if days_ago <= 3:
                    score *= 1.1  # 10% 时间权重提升
                elif days_ago > 30:
                    score *= 0.9  # 10% 衰减
            
            scored.append({
                **mem,
                "score": round(score, 2),
                "filename": filename
            })
        
        # 排序
        scored.sort(key=lambda x: x["score"], reverse=True)
        
        return scored[:top_k]
    
    def report(self) -> str:
        """生成优化报告"""
        return """🔍 搜索优化模块
========================================
功能：
1. 关键词权重提取
2. 语义相关性计算
3. 搜索结果重排序
4. 时间衰减因子

使用方法：
- calculate_relevance(query, content, title)
- rerank_results(query, results, top_k)
- search_with_boost(query, memories, top_k)
"""
