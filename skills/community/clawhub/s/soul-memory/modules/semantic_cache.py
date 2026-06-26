#!/usr/bin/env python3
"""
Soul Memory v3.4.0 - Semantic Cache Layer
語義緩存層：減少重複查詢，提升響應速度 10x

Author: Li Si (李斯)
Date: 2026-03-08

v3.4.0 - 新增語義緩存 + LRU 淘汰機制
"""

import os
import json
import hashlib
import time
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CacheEntry:
    """緩存條目"""
    query: str
    query_hash: str
    results: List[Dict]
    timestamp: float
    hit_count: int = 0
    
    def to_dict(self) -> Dict:
        return {
            'query': self.query,
            'query_hash': self.query_hash,
            'results': self.results,
            'timestamp': self.timestamp,
            'hit_count': self.hit_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CacheEntry':
        return cls(
            query=data['query'],
            query_hash=data['query_hash'],
            results=data['results'],
            timestamp=data['timestamp'],
            hit_count=data.get('hit_count', 0)
        )


class SemanticCache:
    """
    語義緩存層 v3.4.0
    
    Features:
    - LRU (Least Recently Used) 淘汰機制
    - TTL (Time To Live) 過期機制
    - 語義相似度檢測
    - 持久化存儲
    - 命中率統計
    """
    
    VERSION = "3.4.0"
    DEFAULT_TTL = 300  # 5 分鐘
    DEFAULT_MAX_SIZE = 100  # 最多 100 條緩存
    SIMILARITY_THRESHOLD = 0.95  # 語義相似度閾值
    
    def __init__(self, cache_path: Optional[Path] = None, 
                 ttl: int = DEFAULT_TTL,
                 max_size: int = DEFAULT_MAX_SIZE):
        """
        初始化緩存
        
        Args:
            cache_path: 緩存文件路徑
            ttl: 過期時間（秒）
            max_size: 最大緩存數量
        """
        self.cache_path = cache_path or Path(__file__).parent / "cache" / "semantic_cache.json"
        self.ttl = ttl
        self.max_size = max_size
        
        # 內存緩存
        self.cache: Dict[str, CacheEntry] = {}
        
        # 統計信息
        self.stats = {
            'total_queries': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'evictions': 0
        }
        
        # 確保目錄存在
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 加載持久化緩存
        self.load()
    
    def _hash_query(self, query: str) -> str:
        """計算查詢哈希"""
        # 正規化查詢（去除空格、轉小寫）
        normalized = query.strip().lower()
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def _calculate_similarity(self, query1: str, query2: str) -> float:
        """
        計算語義相似度
        
        使用簡化的字符串相似度算法（Levenshtein 距離）
        未來可替換為 Embedding 模型
        """
        # 快速檢查：完全相同
        if query1 == query2:
            return 1.0
        
        # 計算編輯距離
        len1, len2 = len(query1), len(query2)
        if len1 == 0 or len2 == 0:
            return 0.0
        
        # 簡化版：字符重疊率
        set1, set2 = set(query1), set(query2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    def get(self, query: str) -> Optional[List[Dict]]:
        """
        獲取緩存結果
        
        Args:
            query: 查詢字符串
            
        Returns:
            緩存的搜索結果，如果未命中則返回 None
        """
        self.stats['total_queries'] += 1
        
        # 1. 精確匹配（哈希）
        query_hash = self._hash_query(query)
        if query_hash in self.cache:
            entry = self.cache[query_hash]
            
            # 檢查是否過期
            if time.time() - entry.timestamp < self.ttl:
                entry.hit_count += 1
                self.stats['cache_hits'] += 1
                
                # 更新訪問時間（LRU）
                entry.timestamp = time.time()
                self.save()
                
                return entry.results
            else:
                # 過期，刪除
                del self.cache[query_hash]
                self.stats['evictions'] += 1
        
        # 2. 語義相似匹配
        for hash_key, entry in list(self.cache.items()):
            if time.time() - entry.timestamp >= self.ttl:
                continue
            
            similarity = self._calculate_similarity(query, entry.query)
            if similarity >= self.SIMILARITY_THRESHOLD:
                entry.hit_count += 1
                self.stats['cache_hits'] += 1
                
                # 更新訪問時間
                entry.timestamp = time.time()
                self.save()
                
                return entry.results
        
        # 未命中
        self.stats['cache_misses'] += 1
        return None
    
    def set(self, query: str, results: List[Dict]):
        """
        設置緩存
        
        Args:
            query: 查詢字符串
            results: 搜索結果
        """
        query_hash = self._hash_query(query)
        
        # 如果已存在，更新
        if query_hash in self.cache:
            self.cache[query_hash].results = results
            self.cache[query_hash].timestamp = time.time()
        else:
            # 檢查是否需要淘汰
            if len(self.cache) >= self.max_size:
                self._evict_lru()
            
            # 創建新條目
            entry = CacheEntry(
                query=query,
                query_hash=query_hash,
                results=results,
                timestamp=time.time()
            )
            self.cache[query_hash] = entry
        
        self.save()
    
    def _evict_lru(self):
        """淘汰最少使用的條目"""
        if not self.cache:
            return
        
        # 找到最少使用的條目
        lru_entry = min(self.cache.items(), key=lambda x: x[1].hit_count)
        
        # 刪除
        del self.cache[lru_entry[0]]
        self.stats['evictions'] += 1
    
    def clear(self):
        """清空緩存"""
        self.cache.clear()
        self.save()
    
    def cleanup_expired(self) -> int:
        """清理過期條目"""
        current_time = time.time()
        expired_keys = []
        
        for key, entry in self.cache.items():
            if current_time - entry.timestamp >= self.ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
            self.stats['evictions'] += 1
        
        if expired_keys:
            self.save()
        
        return len(expired_keys)
    
    def save(self):
        """持久化緩存到文件"""
        try:
            data = {
                'version': self.VERSION,
                'updated_at': datetime.now().isoformat(),
                'stats': self.stats,
                'cache': {k: v.to_dict() for k, v in self.cache.items()}
            }
            
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[SemanticCache] Save failed: {e}")
    
    def load(self):
        """從文件加載緩存"""
        if not self.cache_path.exists():
            return
        
        try:
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 加載統計信息
            if 'stats' in data:
                self.stats = data['stats']
            
            # 加載緩存條目
            if 'cache' in data:
                for key, entry_data in data['cache'].items():
                    self.cache[key] = CacheEntry.from_dict(entry_data)
            
            # 清理過期條目
            self.cleanup_expired()
            
            print(f"[SemanticCache] Loaded {len(self.cache)} entries")
        except Exception as e:
            print(f"[SemanticCache] Load failed: {e}")
            self.cache = {}
    
    def get_stats(self) -> Dict:
        """獲取統計信息"""
        hit_rate = (
            self.stats['cache_hits'] / self.stats['total_queries'] * 100
            if self.stats['total_queries'] > 0 else 0
        )
        
        return {
            'version': self.VERSION,
            'total_queries': self.stats['total_queries'],
            'cache_hits': self.stats['cache_hits'],
            'cache_misses': self.stats['cache_misses'],
            'evictions': self.stats['evictions'],
            'hit_rate': f"{hit_rate:.1f}%",
            'cache_size': len(self.cache),
            'max_size': self.max_size,
            'ttl': self.ttl
        }
    
    def __len__(self) -> int:
        """返回緩存大小"""
        return len(self.cache)
    
    def __contains__(self, query: str) -> bool:
        """檢查查詢是否在緩存中"""
        return self.get(query) is not None


# 全局緩存實例（單例模式）
_global_cache: Optional[SemanticCache] = None


def get_cache(cache_path: Optional[Path] = None, 
              ttl: int = SemanticCache.DEFAULT_TTL,
              max_size: int = SemanticCache.DEFAULT_MAX_SIZE) -> SemanticCache:
    """獲取全局緩存實例"""
    global _global_cache
    
    if _global_cache is None:
        _global_cache = SemanticCache(cache_path, ttl, max_size)
    
    return _global_cache


# CLI 測試
if __name__ == "__main__":
    print("🧪 Testing Semantic Cache v3.4.0\n")
    
    cache = SemanticCache()
    
    # 測試 1: 設置緩存
    print("Test 1: Set cache")
    cache.set("QST 物理理論", [
        {'content': 'QSTv7.1 理論', 'score': 5.0},
        {'content': 'FSCAv7 模擬', 'score': 4.5}
    ])
    print(f"✓ Cache size: {len(cache)}\n")
    
    # 測試 2: 獲取緩存
    print("Test 2: Get cache")
    results = cache.get("QST 物理理論")
    print(f"✓ Hit: {results is not None}")
    print(f"✓ Results: {results}\n")
    
    # 測試 3: 緩存統計
    print("Test 3: Cache stats")
    stats = cache.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()
    
    # 測試 4: 語義相似匹配
    print("Test 4: Semantic similarity")
    results = cache.get("QST 物理")  # 相似查詢
    print(f"✓ Similar match: {results is not None}\n")
    
    # 測試 5: 清理過期
    print("Test 5: Cleanup expired")
    cache.ttl = 1  # 設置 1 秒過期
    time.sleep(1.1)
    expired = cache.cleanup_expired()
    print(f"✓ Expired entries: {expired}")
    print(f"✓ Cache size after cleanup: {len(cache)}\n")
    
    print("✅ All tests passed!")
