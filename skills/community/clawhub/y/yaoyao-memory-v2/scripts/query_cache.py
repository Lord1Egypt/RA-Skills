#!/usr/bin/env python3
"""
查询缓存模块
支持 LRU 缓存，提升重复查询性能
"""

import time
import hashlib
import threading
from typing import Any, Optional, Dict, Tuple
from collections import OrderedDict

class QueryCache:
    """LRU 查询缓存"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 300):
        """
        初始化缓存
        
        Args:
            max_size: 最大缓存条目数
            ttl: 缓存有效期（秒）
        """
        self.max_size = max_size
        self.ttl = ttl
        self._cache: OrderedDict = OrderedDict()
        self._lock = threading.Lock()
        
        # 统计信息
        self.hits = 0
        self.misses = 0
    
    def _make_key(self, query: str, params: tuple = None) -> str:
        """生成缓存键"""
        content = f"{query}:{params or ()}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, query: str, params: tuple = None) -> Optional[Any]:
        """获取缓存"""
        key = self._make_key(query, params)
        
        with self._lock:
            if key not in self._cache:
                self.misses += 1
                return None
            
            result, timestamp = self._cache[key]
            
            # 检查是否过期
            if time.time() - timestamp > self.ttl:
                del self._cache[key]
                self.misses += 1
                return None
            
            # 移动到末尾（LRU）
            self._cache.move_to_end(key)
            self.hits += 1
            return result
    
    def set(self, query: str, params: tuple, result: Any):
        """设置缓存"""
        key = self._make_key(query, params)
        
        with self._lock:
            # 如果已存在，更新
            if key in self._cache:
                del self._cache[key]
            
            # 添加新条目
            self._cache[key] = (result, time.time())
            
            # LRU 淘汰
            while len(self._cache) > self.max_size:
                self._cache.popitem(last=False)
    
    def clear(self):
        """清空缓存"""
        with self._lock:
            self._cache.clear()
            self.hits = 0
            self.misses = 0
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        with self._lock:
            total = self.hits + self.misses
            hit_rate = self.hits / total if total > 0 else 0
            
            return {
                "size": len(self._cache),
                "max_size": self.max_size,
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate": f"{hit_rate:.2%}"
            }

# 全局缓存实例
_cache_instances = {}

def get_cache(name: str = "default") -> QueryCache:
    """获取或创建缓存实例"""
    if name not in _cache_instances:
        _cache_instances[name] = QueryCache()
    return _cache_instances[name]
