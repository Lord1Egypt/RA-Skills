"""反馈学习 - 记录用户点击，优化排序"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class FeedbackLearner:
    def __init__(self, feedback_dir: str):
        self.feedback_dir = Path(feedback_dir)
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
        self.feedback_file = self.feedback_dir / "feedback.json"
        self.feedback = self._load()
    
    def _load(self) -> Dict:
        if self.feedback_file.exists():
            try:
                return json.loads(self.feedback_file.read_text())
            except:
                pass
        return {"clicks": {}, "preferences": {}}
    
    def _save(self):
        self.feedback_file.write_text(json.dumps(self.feedback, ensure_ascii=False))
    
    def record_click(self, query: str, result_id: str, position: int):
        """记录点击"""
        query_key = self._hash(query)
        
        if query_key not in self.feedback["clicks"]:
            self.feedback["clicks"][query_key] = {
                "query": query,
                "clicks": []
            }
        
        self.feedback["clicks"][query_key]["clicks"].append({
            "result_id": result_id,
            "position": position,
            "time": datetime.now().isoformat()
        })
        
        self._save()
    
    def record_preference(self, query: str, good_result_ids: List[str], bad_result_ids: List[str] = None):
        """记录偏好"""
        query_key = self._hash(query)
        
        self.feedback["preferences"][query_key] = {
            "query": query,
            "good": good_result_ids,
            "bad": bad_result_ids or [],
            "time": datetime.now().isoformat()
        }
        
        self._save()
    
    def get_boosted_ids(self, query: str) -> List[str]:
        """获取应提升的结果ID"""
        query_key = self._hash(query)
        
        if query_key in self.feedback["clicks"]:
            clicks = self.feedback["clicks"][query_key]["clicks"]
            # 统计点击次数
            click_counts = {}
            for c in clicks:
                rid = c["result_id"]
                click_counts[rid] = click_counts.get(rid, 0) + 1
            
            # 返回点击次数最多的
            sorted_ids = sorted(click_counts.keys(), key=lambda x: click_counts[x], reverse=True)
            return sorted_ids
        
        return []
    
    def get_penalty_ids(self, query: str) -> List[str]:
        """获取应降权的结果ID"""
        query_key = self._hash(query)
        
        if query_key in self.feedback["preferences"]:
            return self.feedback["preferences"][query_key].get("bad", [])
        
        return []
    
    def apply_feedback(self, query: str, results: List[Dict]) -> List[Dict]:
        """应用反馈到结果"""
        boosted = self.get_boosted_ids(query)
        penalized = self.get_penalty_ids(query)
        
        for r in results:
            rid = r.get("record_id", "")
            
            # 提升被点击的结果
            if rid in boosted:
                r["feedback_boost"] = 0.1
            
            # 降权被标记为差的结果
            if rid in penalized:
                r["feedback_penalty"] = -0.1
        
        # 重新排序
        results.sort(key=lambda x: (
            x.get("feedback_boost", 0),
            x.get("weighted_score", x.get("score", 0)),
            -x.get("feedback_penalty", 0)
        ), reverse=True)
        
        return results
    
    @staticmethod
    def _hash(text: str) -> str:
        import hashlib
        return hashlib.md5(text.lower().encode()).hexdigest()[:16]
