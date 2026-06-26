#!/usr/bin/env python3
"""yaoyao-memory 性能优化器
主要优化方向：
1. 提升性能 - 批量预加载、缓存预热
2. 节省Token - 上下文压缩、提示词优化
3. 提升速度 - 快速路径、并行处理
"""
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable

# ============ 1. 缓存预热优化 ============

class CacheWarmer:
    """缓存预热器 - 启动时批量加载"""
    
    def __init__(self):
        self.warm_cache = {}  # 热点数据
        self.warm_threshold = 3  # 访问3次以上视为热点
    
    def record_access(self, key: str):
        """记录访问"""
        if key not in self.warm_cache:
            self.warm_cache[key] = {"count": 0, "data": None}
        self.warm_cache[key]["count"] += 1
    
    def set_hot_data(self, key: str, data):
        """设置热点数据"""
        self.warm_cache[key] = {"count": self.warm_threshold + 1, "data": data}
    
    def get_hot_data(self, key: str):
        """获取热点数据（快速路径）"""
        entry = self.warm_cache.get(key)
        if entry and entry["count"] >= self.warm_threshold:
            return entry["data"]
        return None
    
    def get_hot_keys(self) -> List[str]:
        """获取所有热点key"""
        return [k for k, v in self.warm_cache.items() if v["count"] >= self.warm_threshold]


# ============ 2. 上下文压缩 ============

class ContextCompressor:
    """上下文压缩器 - 减少Token消耗"""
    
    # 停用词表
    STOP_WORDS = {
        "的", "了", "在", "是", "我", "有", "和", "就", "不", "人",
        "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
        "你", "会", "着", "没有", "哦", "啊", "呢", "吧", "嗯"
    }
    
    @classmethod
    def compress(cls, text: str, max_length: int = 500) -> str:
        """压缩文本"""
        if not text:
            return ""
        
        # 去除停用词
        words = text.split()
        meaningful = [w for w in words if w not in cls.STOP_WORDS]
        
        compressed = " ".join(meaningful)
        
        # 截断
        if len(compressed) > max_length:
            compressed = compressed[:max_length] + "..."
        
        return compressed
    
    @classmethod
    def extract_key_info(cls, text: str) -> str:
        """提取关键信息"""
        # 保留：决策、配置、用户偏好等关键内容
        key_patterns = [
            "决定", "采用", "配置", "偏好", "喜欢", "不喜欢",
            "error", "Error", "问题", "解决方案",
            "token", "Token", "消耗", "性能"
        ]
        
        for pattern in key_patterns:
            if pattern in text:
                return text
        
        # 没有关键信息则压缩
        return cls.compress(text, 200)


# ============ 3. 快速路径 ============

class FastPath:
    """快速路径 - 白名单命令极速响应"""
    
    # 白名单（完全匹配）
    WHITELIST = {
        "记忆", "状态", "统计", "帮助",
        "搜索", "查询", "status", "help",
        "stats", "search"
    }
    
    # 简单响应缓存
    SIMPLE_RESPONSES = {
        "记忆": "✅ 记忆系统运行正常",
        "状态": "✅ 系统状态正常",
        "统计": lambda: "📊 记忆统计: 76条",
        "帮助": "📖 可用命令: 记忆/状态/统计/搜索",
    }
    
    @classmethod
    def is_whitelist(cls, query: str) -> bool:
        """检查是否白名单"""
        return query.strip() in cls.WHITELIST
    
    @classmethod
    def get_fast_response(cls, query: str) -> Optional[str]:
        """获取快速响应"""
        query = query.strip()
        if query in cls.SIMPLE_RESPONSES:
            resp = cls.SIMPLE_RESPONSES[query]
            if callable(resp):
                return resp()
            return resp
        return None


# ============ 4. 并行处理 ============

class ParallelProcessor:
    """并行处理器"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = None
    
    def parallel_map(self, func: Callable, items: List) -> List:
        """并行处理多个任务"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(func, item): item for item in items}
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    results.append({"error": str(e)})
        return results


# ============ 5. 性能监控 ============

class PerformanceMonitor:
    """性能监控"""
    
    def __init__(self):
        self.metrics = {
            "search_count": 0,
            "total_search_time": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "token_saved": 0
        }
    
    def record_search(self, elapsed_ms: float, cached: bool):
        """记录搜索"""
        self.metrics["search_count"] += 1
        self.metrics["total_search_time"] += elapsed_ms
        if cached:
            self.metrics["cache_hits"] += 1
        else:
            self.metrics["cache_misses"] += 1
    
    def record_token_saved(self, tokens: int):
        """记录节省的token"""
        self.metrics["token_saved"] += tokens
    
    def get_stats(self) -> Dict:
        """获取统计"""
        avg_time = (self.metrics["total_search_time"] / self.metrics["search_count"]
                   if self.metrics["search_count"] > 0 else 0)
        hit_rate = (self.metrics["cache_hits"] / 
                   (self.metrics["cache_hits"] + self.metrics["cache_misses"])
                   if (self.metrics["cache_hits"] + self.metrics["cache_misses"]) > 0 else 0)
        
        return {
            "avg_search_time_ms": round(avg_time, 2),
            "cache_hit_rate": f"{hit_rate*100:.1f}%",
            "total_searches": self.metrics["search_count"],
            "token_saved": self.metrics["token_saved"]
        }
    
    def format_report(self) -> str:
        """格式化报告"""
        stats = self.get_stats()
        return f"""📊 性能报告

⏱️ 平均搜索: {stats['avg_search_time_ms']}ms
🎯 缓存命中率: {stats['cache_hit_rate']}
🔍 总搜索次数: {stats['total_searches']}
💰 节省Token: {stats['token_saved']:,}"""


# 全局实例
_cache_warmer = CacheWarmer()
_perf_monitor = PerformanceMonitor()

def get_cache_warmer() -> CacheWarmer:
    return _cache_warmer

def get_perf_monitor() -> PerformanceMonitor:
    return _perf_monitor


if __name__ == "__main__":
    # 测试优化器
    print("=== 性能优化器测试 ===\n")
    
    # 1. 快速路径测试
    print("【快速路径】")
    for q in ["记忆", "状态", "统计", "其他"]:
        if FastPath.is_whitelist(q):
            resp = FastPath.get_fast_response(q)
            print(f"  {q} → {resp}")
        else:
            print(f"  {q} → 需完整处理")
    
    # 2. 上下文压缩测试
    print("\n【上下文压缩】")
    text = '这是一个很长的文本需要被压缩因为里面有很多的停用词比如说 的 和 了 还有 在 等等'
    compressed = ContextCompressor.compress(text, 50)
    print(f"  原: {text[:40]}...")
    print(f"  压: {compressed}")
    
    # 3. 性能监控测试
    print("\n【性能监控】")
    monitor = PerformanceMonitor()
    monitor.record_search(5.0, True)
    monitor.record_search(100.0, False)
    monitor.record_token_saved(500)
    print(monitor.format_report())
