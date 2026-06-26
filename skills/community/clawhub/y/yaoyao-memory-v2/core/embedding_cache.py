#!/usr/bin/env python3
"""
embedding_cache.py - 强化 Embedding 缓存管理器

功能：
- LRU 缓存（内存）
- 持久化缓存（磁盘）
- 缓存预热
- 缓存统计

性能优化：
- 内存缓存：无网络延迟，< 0.1ms
- 持久化缓存：避免进程重启后重新计算
- 批量预热：启动时预加载常用查询
"""

import hashlib
import json
import os
import time
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class EmbeddingCache:
    """强化 Embedding 缓存管理器"""
    
    def __init__(self, cache_dir: Optional[Path] = None, max_memory_items: int = 500):
        self.cache_dir = cache_dir or Path.home() / ".openclaw" / "memory-tdai" / ".cache" / "embeddings"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 内存缓存（LRU）
        self._memory_cache: OrderedDict = OrderedDict()
        self._max_memory_items = max_memory_items
        
        # 持久化缓存路径
        self._disk_cache_file = self.cache_dir / "embedding_cache.json"
        self._disk_cache: Dict[str, dict] = {}
        
        # 统计
        self._stats = {
            "memory_hits": 0,
            "disk_hits": 0,
            "misses": 0,
            "total_requests": 0,
        }
        
        # 加载持久化缓存
        self._load_disk_cache()
    
    def _hash(self, text: str) -> str:
        """计算文本的哈希值"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def _load_disk_cache(self):
        """加载磁盘缓存到内存"""
        if self._disk_cache_file.exists():
            try:
                with open(self._disk_cache_file, 'r', encoding='utf-8') as f:
                    self._disk_cache = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._disk_cache = {}
    
    def _save_disk_cache(self):
        """保存磁盘缓存"""
        try:
            with open(self._disk_cache_file, 'w', encoding='utf-8') as f:
                json.dump(self._disk_cache, f, ensure_ascii=False)
        except IOError as e:
            print(f"警告：缓存保存失败: {e}")
    
    def get(self, text: str) -> Optional[List[float]]:
        """获取缓存的 embedding"""
        self._stats["total_requests"] += 1
        key = self._hash(text)
        
        # 1. 检查内存缓存
        if key in self._memory_cache:
            # 移到末尾（LRU）
            self._memory_cache.move_to_end(key)
            self._stats["memory_hits"] += 1
            return self._memory_cache[key]["embedding"]
        
        # 2. 检查磁盘缓存
        if key in self._disk_cache:
            embedding = self._disk_cache[key]["embedding"]
            # 升级到内存缓存
            self._add_to_memory(key, embedding)
            self._stats["disk_hits"] += 1
            return embedding
        
        # 3. 未命中
        self._stats["misses"] += 1
        return None
    
    def _add_to_memory(self, key: str, embedding: List[float]):
        """添加到内存缓存"""
        # 如果已存在，移到末尾
        if key in self._memory_cache:
            self._memory_cache.move_to_end(key)
            return
        
        # 如果缓存已满，删除最旧的
        if len(self._memory_cache) >= self._max_memory_items:
            self._memory_cache.popitem(last=False)
        
        self._memory_cache[key] = {
            "embedding": embedding,
            "cached_at": time.time(),
        }
    
    def set(self, text: str, embedding: List[float], persist: bool = True):
        """设置缓存"""
        key = self._hash(text)
        
        # 添加到内存缓存
        self._add_to_memory(key, embedding)
        
        # 添加到磁盘缓存
        if persist:
            self._disk_cache[key] = {
                "embedding": embedding,
                "text": text[:100],  # 只存前100字符用于调试
                "cached_at": time.time(),
            }
            self._save_disk_cache()
    
    def batch_get(self, texts: List[str]) -> Tuple[List[Optional[List[float]]], List[int]]:
        """
        批量获取缓存
        
        Returns:
            (results, uncached_indices) - 结果列表和未缓存的索引
        """
        results = []
        uncached_indices = []
        
        for i, text in enumerate(texts):
            embedding = self.get(text)
            if embedding is not None:
                results.append(embedding)
            else:
                results.append(None)
                uncached_indices.append(i)
        
        return results, uncached_indices
    
    def batch_set(self, texts: List[str], embeddings: List[List[float]], persist: bool = True):
        """批量设置缓存"""
        for text, embedding in zip(texts, embeddings):
            self.set(text, embedding, persist=persist)
    
    def get_stats(self) -> dict:
        """获取缓存统计"""
        total = self._stats["total_requests"]
        if total == 0:
            hit_rate = 0
        else:
            hit_rate = (self._stats["memory_hits"] + self._stats["disk_hits"]) / total * 100
        
        return {
            "memory_items": len(self._memory_cache),
            "disk_items": len(self._disk_cache),
            "memory_hits": self._stats["memory_hits"],
            "disk_hits": self._stats["disk_hits"],
            "misses": self._stats["misses"],
            "total_requests": total,
            "hit_rate": f"{hit_rate:.1f}%",
        }
    
    def warm_up(self, common_queries: List[str]):
        """预热缓存"""
        print(f"开始预热 {len(common_queries)} 个查询...")
        
        # 只从磁盘缓存加载，不调用 API
        loaded = 0
        for query in common_queries:
            key = self._hash(query)
            if key in self._disk_cache:
                embedding = self._disk_cache[key]["embedding"]
                self._add_to_memory(key, embedding)
                loaded += 1
        
        print(f"预热完成：从磁盘缓存加载 {loaded} 个 embeddings")
        return loaded
    
    def clear(self, clear_disk: bool = False):
        """清空缓存"""
        self._memory_cache.clear()
        if clear_disk:
            self._disk_cache.clear()
            if self._disk_cache_file.exists():
                self._disk_cache_file.unlink()
        self._stats = {
            "memory_hits": 0,
            "disk_hits": 0,
            "misses": 0,
            "total_requests": 0,
        }


# 全局缓存实例
_global_cache: Optional[EmbeddingCache] = None


def get_embedding_cache() -> EmbeddingCache:
    """获取全局缓存实例"""
    global _global_cache
    if _global_cache is None:
        _global_cache = EmbeddingCache()
    return _global_cache
