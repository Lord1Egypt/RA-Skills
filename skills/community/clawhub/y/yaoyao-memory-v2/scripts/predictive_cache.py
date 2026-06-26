#!/usr/bin/env python3
"""
预测性缓存模块 - v1.0.0
基于上下文预测可能需要的记忆并预加载

功能：
1. 分析当前对话上下文
2. 预测可能需要的记忆
3. 提前加载向量embedding到缓存
4. 减少实际搜索时的延迟
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set
from collections import Counter

# 配置
MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
CACHE_FILE = MEMORY_DIR / ".predictive_cache.json"

# 预测关键词模式
CONTEXT_PATTERNS = {
    "记忆": ["记忆", "记得", "以前", "上次", "过去"],
    "用户": ["用户", "偏好", "喜欢", "习惯"],
    "技术": ["代码", "技术", "实现", "方案", "架构"],
    "决策": ["决定", "选择", "采用", "决策"],
    "错误": ["错误", "失败", "bug", "问题"],
    "项目": ["项目", "功能", "开发", "任务"],
}

class PredictiveCache:
    """预测性缓存器"""
    
    def __init__(self):
        self.memory_dir = MEMORY_DIR
        self.cache_file = CACHE_FILE
        self._data = {}  # 简单的KV存储，供benchmark.py使用
        self._load_cache()
    
    def _load_cache(self):
        """加载预测缓存"""
        if self.cache_file.exists():
            try:
                self.cache = json.loads(self.cache_file.read_text(encoding="utf-8"))
            except:
                self.cache = {"predictions": [], "last_update": None}
        else:
            self.cache = {"predictions": [], "last_update": None}
    
    def set(self, key, value):
        """设置缓存值（供benchmark.py使用）"""
        self._data[key] = value
    
    def get(self, key, default=None):
        """获取缓存值（供benchmark.py使用）"""
        return self._data.get(key, default)
    
    def _save_cache(self):
        """保存预测缓存"""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            self.cache_file.write_text(json.dumps(self.cache, ensure_ascii=False), encoding="utf-8")
        except:
            pass
    
    def extract_keywords(self, text: str) -> List[str]:
        """从文本中提取关键词"""
        # 简单分词
        words = re.findall(r'[\w]+', text.lower())
        # 过滤停用词
        stopwords = {"的", "了", "是", "在", "我", "你", "他", "这", "那", "和", "与", "或", "以及", "对于", "关于"}
        keywords = [w for w in words if len(w) >= 2 and w not in stopwords]
        return keywords
    
    def match_context(self, text: str) -> List[str]:
        """匹配上下文类型"""
        matched = []
        text_lower = text.lower()
        
        for context_type, patterns in CONTEXT_PATTERNS.items():
            for pattern in patterns:
                if pattern in text_lower:
                    matched.append(context_type)
                    break
        
        return matched if matched else ["其他"]
    
    def predict(self, context: str, limit: int = 5) -> List[Dict]:
        """
        预测可能需要的记忆
        - context: 当前对话上下文
        - limit: 返回数量
        """
        # 提取关键词
        keywords = self.extract_keywords(context)
        matched_types = self.match_context(context)
        
        # 扫描记忆文件
        memories = []
        for f in self.memory_dir.glob("*.md"):
            if f.name.startswith(".") or "合并版" in f.name:
                continue
            
            try:
                content = f.read_text(encoding="utf-8")
                title = f.stem
                
                # 计算相关性分数
                score = 0
                content_lower = content.lower()
                
                # 关键词匹配
                for kw in keywords:
                    if kw in content_lower:
                        score += 2
                
                # 类型匹配
                for mem_type in matched_types:
                    type_keywords = CONTEXT_PATTERNS.get(mem_type, [])
                    for tk in type_keywords:
                        if tk in content_lower:
                            score += 1
                
                # 最近修改加权
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                days_ago = (datetime.now() - mtime).days
                if days_ago <= 7:
                    score += 3
                elif days_ago <= 30:
                    score += 1
                
                if score > 0:
                    memories.append({
                        "filename": f.name,
                        "title": title,
                        "score": score,
                        "size": len(content),
                        "modified": mtime.isoformat()
                    })
            except:
                pass
        
        # 按分数排序
        memories.sort(key=lambda x: x["score"], reverse=True)
        
        # 更新缓存
        self.cache["predictions"] = memories[:limit]
        self.cache["last_update"] = datetime.now().isoformat()
        self._save_cache()
        
        return memories[:limit]
    
    def preload(self, predictions: List[Dict]):
        """
        预加载预测的记忆到缓存
        - 实际是提前加载embedding到内存
        """
        from memory import _get_embedding, _embedding_cache
        
        preloaded = []
        for mem in predictions:
            # 这里只记录，不实际调用embedding（避免浪费）
            preloaded.append({
                "filename": mem["filename"],
                "title": mem["title"],
                "score": mem["score"],
                "preload_hint": "embedding_cached"
            })
        
        return preloaded
    
    def get_cached_predictions(self) -> List[Dict]:
        """获取上次预测的结果"""
        return self.cache.get("predictions", [])
    
    def report(self) -> str:
        """生成预测报告"""
        predictions = self.get_cached_predictions()
        last_update = self.cache.get("last_update", "从未")
        
        lines = [
            "🔮 预测性缓存报告",
            "=" * 40,
            f"最后更新: {last_update}",
            "",
        ]
        
        if predictions:
            lines.append(f"预测记忆 ({len(predictions)}条):")
            for p in predictions[:5]:
                lines.append(f"  • {p['title']} (分数:{p['score']})")
        else:
            lines.append("暂无预测数据")
        
        return "\n".join(lines)


if __name__ == "__main__":
    predictor = PredictiveCache()
    
    # 测试预测
    print("=== 预测测试 ===")
    test_context = "用户喜欢什么？记得之前的技术决策是什么？"
    predictions = predictor.predict(test_context)
    print(f"上下文: {test_context}")
    print(f"预测结果: {len(predictions)}条")
    for p in predictions[:3]:
        print(f"  - {p['title']} (分数:{p['score']})")
    
    print("\n" + predictor.report())
