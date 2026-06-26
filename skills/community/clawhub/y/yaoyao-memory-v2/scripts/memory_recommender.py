#!/usr/bin/env python3
"""
记忆推荐模块 - v1.0.0
基于用户行为主动推荐相关记忆

功能：
1. 基于搜索历史的推荐
2. 基于当前对话上下文的推荐
3. 基于时间规律的推荐
4. 基于关联记忆的推荐
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Optional
from collections import Counter, defaultdict

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
HISTORY_FILE = MEMORY_DIR / ".search_history.json"

class MemoryRecommender:
    """记忆推荐器"""
    
    def __init__(self):
        self.memory_dir = MEMORY_DIR
        self.history_file = HISTORY_FILE
        self._load_history()
    
    def _load_history(self):
        """加载搜索历史"""
        if self.history_file.exists():
            try:
                self.history = json.loads(self.history_file.read_text(encoding="utf-8"))
            except:
                self.history = {"searches": [], "accesses": []}
        else:
            self.history = {"searches": [], "accesses": []}
    
    def _save_history(self):
        """保存搜索历史"""
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            self.history_file.write_text(json.dumps(self.history, ensure_ascii=False), encoding="utf-8")
        except:
            pass
    
    def record_search(self, query: str, results: List[str]):
        """记录搜索行为"""
        self.history["searches"].append({
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "results_count": len(results)
        })
        # 只保留最近100条
        self.history["searches"] = self.history["searches"][-100:]
        self._save_history()
    
    def record_access(self, memory_id: str):
        """记录访问行为"""
        self.history["accesses"].append({
            "memory_id": memory_id,
            "timestamp": datetime.now().isoformat()
        })
        # 只保留最近100条
        self.history["accesses"] = self.history["accesses"][-100:]
        self._save_history()
    
    def _extract_context_keywords(self, context: str) -> Set[str]:
        """从上下文提取关键词"""
        # 分词
        words = re.findall(r'[\w]{2,}', context.lower())
        
        # 过滤停用词
        stopwords = {"的", "了", "是", "在", "我", "你", "他", "这", "那", "和", "与", "或", "以及", "关于", "一个", "一些", "什么", "怎么", "如何", "为什么", "现在", "今天", "昨天", "这个", "那个"}
        
        return set(w for w in words if w not in stopwords and len(w) >= 2)
    
    def recommend_by_context(self, context: str, limit: int = 3) -> List[Dict]:
        """
        基于当前上下文推荐记忆
        """
        keywords = self._extract_context_keywords(context)
        
        memories = []
        for f in self.memory_dir.glob("*.md"):
            if f.name.startswith(".") or "合并版" in f.name:
                continue
            
            try:
                content = f.read_text(encoding="utf-8").lower()
                
                # 计算关键词匹配数
                matches = sum(1 for kw in keywords if kw in content)
                
                if matches > 0:
                    memories.append({
                        "filename": f.name,
                        "title": f.stem,
                        "match_count": matches,
                        "match_keywords": [kw for kw in keywords if kw in content],
                        "score": matches / len(keywords) if keywords else 0
                    })
            except:
                pass
        
        # 排序
        memories.sort(key=lambda x: (x["score"], x["match_count"]), reverse=True)
        
        return memories[:limit]
    
    def recommend_by_history(self, limit: int = 3) -> List[Dict]:
        """
        基于搜索历史推荐
        - 推荐用户之前搜索过但没访问的记忆
        """
        # 获取最近的搜索查询
        recent_queries = [s["query"] for s in self.history["searches"][-10:]]
        
        # 已经被访问的
        accessed = set(a["memory_id"] for a in self.history["accesses"][-50:])
        
        # 推荐
        recommendations = []
        
        for query in recent_queries:
            query_lower = query.lower()
            
            for f in self.memory_dir.glob("*.md"):
                if f.name in accessed or f.name.startswith("."):
                    continue
                
                try:
                    content = f.read_text(encoding="utf-8").lower()
                    
                    if query_lower in content:
                        recommendations.append({
                            "filename": f.name,
                            "title": f.stem,
                            "reason": f"与之前搜索「{query}」相关",
                            "query": query
                        })
                except:
                    pass
        
        # 去重
        seen = set()
        unique = []
        for r in recommendations:
            if r["filename"] not in seen:
                seen.add(r["filename"])
                unique.append(r)
        
        return unique[:limit]
    
    def recommend_by_time(self, limit: int = 3) -> List[Dict]:
        """
        基于时间规律推荐
        - 推荐用户通常在这个时候会看的内容类型
        """
        now = datetime.now()
        hour = now.hour
        
        # 分析历史访问时间
        access_hours = []
        for a in self.history["accesses"]:
            try:
                t = datetime.fromisoformat(a["timestamp"])
                access_hours.append(t.hour)
            except:
                pass
        
        # 如果这个小时没有历史访问记录，推荐今天的日记
        recent_access = [
            a for a in self.history["accesses"]
            if datetime.fromisoformat(a["timestamp"]).date() == now.date()
        ]
        
        today_memories = []
        for f in self.memory_dir.glob("*.md"):
            if f.name.startswith(".") or "合并版" in f.name:
                continue
            
            # 推荐今天的记忆
            if str(now.date()) in f.name:
                today_memories.append({
                    "filename": f.name,
                    "title": f.stem,
                    "reason": "今日记忆",
                    "access_today": True
                })
        
        return today_memories[:limit]
    
    def recommend_by_related(self, current_memory: str, limit: int = 3) -> List[Dict]:
        """
        基于关联记忆推荐
        - 推荐与当前记忆相关的其他记忆
        """
        # 简单实现：通过关键词匹配
        current_path = self.memory_dir / current_memory
        if not current_path.exists():
            return []
        
        try:
            current_content = current_path.read_text(encoding="utf-8").lower()
            
            # 提取当前记忆的关键词
            keywords = set(re.findall(r'[\w]{2,}', current_content)) - {"的", "了", "是", "在", "我", "你"}
            
            related = []
            for f in self.memory_dir.glob("*.md"):
                if f.name == current_memory or f.name.startswith("."):
                    continue
                
                try:
                    content = f.read_text(encoding="utf-8").lower()
                    matches = sum(1 for kw in keywords if kw in content)
                    
                    if matches >= 2:  # 至少2个共同关键词
                        related.append({
                            "filename": f.name,
                            "title": f.stem,
                            "reason": f"{matches}个共同关键词",
                            "match_count": matches
                        })
                except:
                    pass
            
            related.sort(key=lambda x: x["match_count"], reverse=True)
            return related[:limit]
        except:
            return []
    
    def get_recommendations(self, context: str = "", current_memory: str = "", limit: int = 5) -> List[Dict]:
        """
        综合推荐接口
        """
        all_recs = []
        seen = set()
        
        # 1. 上下文推荐
        for r in self.recommend_by_context(context, limit):
            if r["filename"] not in seen:
                seen.add(r["filename"])
                all_recs.append({**r, "source": "context"})
        
        # 2. 历史推荐
        for r in self.recommend_by_history(limit):
            if r["filename"] not in seen:
                seen.add(r["filename"])
                all_recs.append({**r, "source": "history"})
        
        # 3. 时间推荐
        for r in self.recommend_by_time(limit):
            if r["filename"] not in seen:
                seen.add(r["filename"])
                all_recs.append({**r, "source": "time"})
        
        # 4. 关联推荐
        if current_memory:
            for r in self.recommend_by_related(current_memory, limit):
                if r["filename"] not in seen:
                    seen.add(r["filename"])
                    all_recs.append({**r, "source": "related"})
        
        return all_recs[:limit]
    
    def report(self) -> str:
        """生成推荐报告"""
        history_size = len(self.history.get("searches", []))
        access_size = len(self.history.get("accesses", []))
        
        recs = self.get_recommendations(limit=5)
        
        lines = [
            "🎯 记忆推荐报告",
            "=" * 40,
            f"搜索历史: {history_size}条",
            f"访问历史: {access_size}条",
            "",
            f"当前推荐: {len(recs)}条",
        ]
        
        for i, r in enumerate(recs[:5], 1):
            lines.append(f"{i}. {r['title']}")
            lines.append(f"   来源: {r.get('source', 'unknown')} | {r.get('reason', '')}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    recommender = MemoryRecommender()
    print(recommender.report())
