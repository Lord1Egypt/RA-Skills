from typing import Dict, List, Optional
"""查询历史学习 - 记录高频查询，优化缓存"""
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class QueryHistory:
    def __init__(self, history_dir: str):
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = self.history_dir / "query_history.json"
        self.history = self._load()
    
    def _load(self) -> Dict:
        if self.history_file.exists():
            try:
                return json.loads(self.history_file.read_text())
            except:
                pass
        return {"queries": {}, "stats": {"total": 0, "unique": 0}}
    
    def _save(self):
        self.history_file.write_text(json.dumps(self.history, ensure_ascii=False))
    
    def record(self, query: str, mode: str, elapsed_ms: float, result_count: int):
        """记录查询"""
        query_key = self._hash_query(query)
        
        if query_key not in self.history["queries"]:
            self.history["queries"][query_key] = {
                "query": query,
                "count": 0,
                "first_seen": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "avg_elapsed_ms": 0,
                "modes": {},
                "result_counts": []
            }
            self.history["stats"]["unique"] += 1
        
        entry = self.history["queries"][query_key]
        entry["count"] += 1
        entry["last_seen"] = datetime.now().isoformat()
        
        # 更新平均耗时
        old_avg = entry["avg_elapsed_ms"]
        entry["avg_elapsed_ms"] = (old_avg * (entry["count"] - 1) + elapsed_ms) / entry["count"]
        
        # 记录模式使用
        if mode not in entry["modes"]:
            entry["modes"][mode] = 0
        entry["modes"][mode] += 1
        
        # 记录结果数量
        entry["result_counts"].append(result_count)
        if len(entry["result_counts"]) > 10:
            entry["result_counts"] = entry["result_counts"][-10:]
        
        self.history["stats"]["total"] += 1
        self._save()
    
    def get_hot_queries(self, limit: int = 10) -> List[Dict]:
        """获取热门查询"""
        queries = list(self.history["queries"].values())
        queries.sort(key=lambda x: x["count"], reverse=True)
        return queries[:limit]
    
    def get_recommended_mode(self, query: str) -> Optional[str]:
        """根据历史推荐模式"""
        query_key = self._hash_query(query)
        
        if query_key in self.history["queries"]:
            entry = self.history["queries"][query_key]
            modes = entry.get("modes", {})
            if modes:
                # 返回最常用的模式
                return max(modes, key=modes.get)
        
        return None
    
    def is_hot_query(self, query: str, threshold: int = 3) -> bool:
        """判断是否为热门查询"""
        query_key = self._hash_query(query)
        
        if query_key in self.history["queries"]:
            return self.history["queries"][query_key]["count"] >= threshold
        
        return False
    
    @staticmethod
    def _hash_query(query: str) -> str:
        import hashlib
        normalized = query.lower().strip()
        return hashlib.md5(normalized.encode()).hexdigest()[:16]
