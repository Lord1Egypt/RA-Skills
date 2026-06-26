#!/usr/bin/env python3
"""
Smart Cache API - Python编程接口
用于在其他Python代码中集成智能缓存功能
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import sqlite3
import threading


@dataclass
class CacheEntry:
    """缓存条目"""
    query: str
    response: str
    similarity: float = 1.0
    cache_type: str = 'L1'
    created_at: Optional[str] = None
    hit_count: int = 0
    tokens_saved: int = 0


@dataclass
class CacheStats:
    """缓存统计"""
    total_requests: int = 0
    l1_hits: int = 0
    l2_hits: int = 0
    misses: int = 0
    l1_entries: int = 0
    l2_entries: int = 0
    tokens_saved: int = 0
    cost_saved: float = 0.0


class SmartCache:
    """
    智能缓存主类
    
    使用示例:
    ```python
    from cache_api import SmartCache
    
    cache = SmartCache()
    
    # 查询缓存
    result = cache.query("你好")
    if result:
        print(f"命中缓存: {result.response}")
    else:
        # 调用API
        response = call_your_llm("你好")
        # 存入缓存
        cache.store("你好", response)
    ```
    """
    
    def __init__(
        self,
        cache_dir: Optional[str] = None,
        l1_max_size: int = 10000,
        l2_max_size: int = 5000,
        ttl_hours: int = 168,
        similarity_threshold: float = 0.85
    ):
        """
        初始化智能缓存
        
        Args:
            cache_dir: 缓存目录路径，默认 ~/.qclaw/smart-cache/data
            l1_max_size: L1缓存最大条目数
            l2_max_size: L2缓存最大条目数
            ttl_hours: 缓存过期时间（小时）
            similarity_threshold: L2语义匹配阈值
        """
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".qclaw" / "smart-cache" / "data"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_path = self.cache_dir / "cache.db"
        self.l1_max_size = l1_max_size
        self.l2_max_size = l2_max_size
        self.ttl_hours = ttl_hours
        self.similarity_threshold = similarity_threshold
        
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.lock = threading.RLock()  # 可重入锁，允许同一线程重复获取
        
        cursor = self.conn.cursor()
        
        # L1缓存表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS l1_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_hash TEXT UNIQUE NOT NULL,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                hit_count INTEGER DEFAULT 0,
                tokens_saved INTEGER DEFAULT 0
            )
        ''')
        
        # L2缓存表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS l2_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                query_embedding BLOB,
                response TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                hit_count INTEGER DEFAULT 0,
                tokens_saved INTEGER DEFAULT 0
            )
        ''')
        
        # 统计表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total_requests INTEGER DEFAULT 0,
                l1_hits INTEGER DEFAULT 0,
                l2_hits INTEGER DEFAULT 0,
                misses INTEGER DEFAULT 0,
                tokens_saved INTEGER DEFAULT 0,
                cost_saved REAL DEFAULT 0.0
            )
        ''')
        
        self.conn.commit()
    
    def _hash_query(self, query: str) -> str:
        """生成查询哈希"""
        normalized = query.strip().lower()
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度（字符级Jaccard，支持中文）"""
        # 字符级 n-gram（bigram），对中文友好
        def get_ngrams(text, n=2):
            text = text.strip().lower()
            return set(text[i:i+n] for i in range(len(text) - n + 1))
        
        ngrams1 = get_ngrams(text1)
        ngrams2 = get_ngrams(text2)
        
        if not ngrams1 or not ngrams2:
            return 0.0
        
        intersection = len(ngrams1 & ngrams2)
        union = len(ngrams1 | ngrams2)
        
        return intersection / union if union > 0 else 0.0
    
    def _update_stats(self, cache_type: Optional[str], tokens: int = 0):
        """更新统计"""
        cost_per_token = 0.0001  # 假设每token成本
        cost_saved = tokens * cost_per_token
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT id FROM stats WHERE date = ?",
                (today,)
            )
            row = cursor.fetchone()
            
            if row:
                if cache_type == 'L1':
                    cursor.execute('''
                        UPDATE stats SET 
                            total_requests = total_requests + 1,
                            l1_hits = l1_hits + 1,
                            tokens_saved = tokens_saved + ?,
                            cost_saved = cost_saved + ?
                        WHERE date = ?
                    ''', (tokens, cost_saved, today))
                elif cache_type == 'L2':
                    cursor.execute('''
                        UPDATE stats SET 
                            total_requests = total_requests + 1,
                            l2_hits = l2_hits + 1,
                            tokens_saved = tokens_saved + ?,
                            cost_saved = cost_saved + ?
                        WHERE date = ?
                    ''', (tokens, cost_saved, today))
                else:
                    cursor.execute('''
                        UPDATE stats SET 
                            total_requests = total_requests + 1,
                            misses = misses + 1
                        WHERE date = ?
                    ''', (today,))
            else:
                if cache_type == 'L1':
                    l1_hits, l2_hits, misses = 1, 0, 0
                elif cache_type == 'L2':
                    l1_hits, l2_hits, misses = 0, 1, 0
                else:
                    l1_hits, l2_hits, misses = 0, 0, 1
                
                cursor.execute('''
                    INSERT INTO stats 
                    (date, total_requests, l1_hits, l2_hits, misses, tokens_saved, cost_saved)
                    VALUES (?, 1, ?, ?, ?, ?, ?)
                ''', (today, l1_hits, l2_hits, misses, tokens, cost_saved))
            
            self.conn.commit()
    
    def query_l1(self, query: str) -> Optional[CacheEntry]:
        """
        L1精确缓存查询
        
        Args:
            query: 查询文本
            
        Returns:
            CacheEntry对象如果命中，否则None
        """
        query_hash = self._hash_query(query)
        
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT response, created_at, hit_count, tokens_saved 
                FROM l1_cache 
                WHERE query_hash = ? AND (expires_at IS NULL OR expires_at > datetime('now'))
            ''', (query_hash,))
            
            result = cursor.fetchone()
            
            if result:
                cursor.execute(
                    'UPDATE l1_cache SET hit_count = hit_count + 1 WHERE query_hash = ?',
                    (query_hash,)
                )
                self.conn.commit()
                
                self._update_stats('L1', result[3] or 0)
                
                return CacheEntry(
                    query=query,
                    response=result[0],
                    similarity=1.0,
                    cache_type='L1',
                    created_at=result[1],
                    hit_count=result[2] + 1,
                    tokens_saved=result[3] or 0
                )
        
        self._update_stats(None)
        return None
    
    def query_l2(self, query: str, threshold: Optional[float] = None) -> Optional[CacheEntry]:
        """
        L2语义缓存查询
        
        Args:
            query: 查询文本
            threshold: 相似度阈值，默认使用初始化时设置的值
            
        Returns:
            CacheEntry对象如果命中，否则None
        """
        threshold = threshold or self.similarity_threshold
        
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, query, response, created_at, hit_count, tokens_saved 
                FROM l2_cache 
                WHERE expires_at IS NULL OR expires_at > datetime('now')
            ''')
            
            best_match = None
            best_similarity = 0.0
            
            for row in cursor.fetchall():
                similarity = self._calculate_similarity(query, row[1])
                
                if similarity >= threshold and similarity > best_similarity:
                    best_similarity = similarity
                    best_match = CacheEntry(
                        query=query,
                        response=row[2],
                        similarity=similarity,
                        cache_type='L2',
                        created_at=row[3],
                        hit_count=row[4],
                        tokens_saved=row[5] or 0
                    )
                    best_match._id = row[0]
            
            if best_match:
                cursor.execute(
                    'UPDATE l2_cache SET hit_count = hit_count + 1 WHERE id = ?',
                    (best_match._id,)
                )
                self.conn.commit()
                
                self._update_stats('L2', best_match.tokens_saved)
            
            return best_match
    
    def query(self, query: str, threshold: Optional[float] = None) -> Optional[CacheEntry]:
        """
        智能查询（先L1后L2）
        
        Args:
            query: 查询文本
            threshold: L2相似度阈值
            
        Returns:
            CacheEntry对象如果命中，否则None
        """
        # 先尝试L1精确匹配
        result = self.query_l1(query)
        if result:
            return result
        
        # 再尝试L2语义匹配
        return self.query_l2(query, threshold)
    
    def store_l1(self, query: str, response: str, tokens: int = 0) -> bool:
        """
        存储到L1缓存
        
        Args:
            query: 查询文本
            response: 响应文本
            tokens: 节省的token数量
            
        Returns:
            是否成功
        """
        query_hash = self._hash_query(query)
        expires_at = datetime.now() + timedelta(hours=self.ttl_hours)
        
        with self.lock:
            cursor = self.conn.cursor()
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO l1_cache 
                    (query_hash, query, response, expires_at, tokens_saved)
                    VALUES (?, ?, ?, ?, ?)
                ''', (query_hash, query, response, expires_at.isoformat(), tokens))
                self.conn.commit()
                
                # 检查容量限制
                cursor.execute("SELECT COUNT(*) FROM l1_cache")
                count = cursor.fetchone()[0]
                if count > self.l1_max_size:
                    # 删除最老的条目
                    cursor.execute('''
                        DELETE FROM l1_cache WHERE id IN (
                            SELECT id FROM l1_cache ORDER BY created_at ASC LIMIT ?
                        )
                    ''', (count - self.l1_max_size,))
                    self.conn.commit()
                
                return True
            except sqlite3.Error as e:
                print(f"L1存储失败: {e}")
                return False
    
    def store_l2(self, query: str, response: str, tokens: int = 0) -> bool:
        """
        存储到L2缓存
        
        Args:
            query: 查询文本
            response: 响应文本
            tokens: 节省的token数量
            
        Returns:
            是否成功
        """
        expires_at = datetime.now() + timedelta(hours=self.ttl_hours)
        
        with self.lock:
            cursor = self.conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO l2_cache 
                    (query, response, expires_at, tokens_saved)
                    VALUES (?, ?, ?, ?)
                ''', (query, response, expires_at.isoformat(), tokens))
                self.conn.commit()
                
                # 检查容量限制
                cursor.execute("SELECT COUNT(*) FROM l2_cache")
                count = cursor.fetchone()[0]
                if count > self.l2_max_size:
                    # 删除最老的条目
                    cursor.execute('''
                        DELETE FROM l2_cache WHERE id IN (
                            SELECT id FROM l2_cache ORDER BY created_at ASC LIMIT ?
                        )
                    ''', (count - self.l2_max_size,))
                    self.conn.commit()
                
                return True
            except sqlite3.Error as e:
                print(f"L2存储失败: {e}")
                return False
    
    def store(self, query: str, response: str, tokens: int = 0, cache_type: str = 'both') -> bool:
        """
        存储到缓存
        
        Args:
            query: 查询文本
            response: 响应文本
            tokens: 节省的token数量
            cache_type: 'l1', 'l2', 或 'both'
            
        Returns:
            是否成功
        """
        success = True
        
        if cache_type in ('l1', 'both'):
            success = self.store_l1(query, response, tokens) and success
        
        if cache_type in ('l2', 'both'):
            success = self.store_l2(query, response, tokens) and success
        
        return success
    
    def clean_expired(self) -> int:
        """清理过期缓存"""
        count = 0
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM l1_cache WHERE expires_at < datetime('now')")
            count += cursor.rowcount
            cursor.execute("DELETE FROM l2_cache WHERE expires_at < datetime('now')")
            count += cursor.rowcount
            self.conn.commit()
        return count
    
    def clean_all(self) -> int:
        """清理所有缓存"""
        count = 0
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM l1_cache")
            count += cursor.rowcount
            cursor.execute("DELETE FROM l2_cache")
            count += cursor.rowcount
            self.conn.commit()
        return count
    
    def get_stats(self) -> CacheStats:
        """获取缓存统计"""
        with self.lock:
            cursor = self.conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM l1_cache")
            l1_entries = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM l2_cache")
            l2_entries = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT 
                    COALESCE(SUM(total_requests), 0),
                    COALESCE(SUM(l1_hits), 0),
                    COALESCE(SUM(l2_hits), 0),
                    COALESCE(SUM(misses), 0),
                    COALESCE(SUM(tokens_saved), 0),
                    COALESCE(SUM(cost_saved), 0.0)
                FROM stats
            ''')
            stats = cursor.fetchone()
            
            return CacheStats(
                total_requests=stats[0],
                l1_hits=stats[1],
                l2_hits=stats[2],
                misses=stats[3],
                l1_entries=l1_entries,
                l2_entries=l2_entries,
                tokens_saved=stats[4],
                cost_saved=stats[5]
            )
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 便捷函数
def create_cache(
    cache_dir: Optional[str] = None,
    l1_max_size: int = 10000,
    l2_max_size: int = 5000,
    ttl_hours: int = 168,
    similarity_threshold: float = 0.85
) -> SmartCache:
    """创建智能缓存实例"""
    return SmartCache(
        cache_dir=cache_dir,
        l1_max_size=l1_max_size,
        l2_max_size=l2_max_size,
        ttl_hours=ttl_hours,
        similarity_threshold=similarity_threshold
    )


# 示例用法
if __name__ == '__main__':
    # 创建缓存实例
    cache = SmartCache()
    
    # 存储示例
    cache.store(
        "你好，今天天气怎么样？",
        "今天天气晴朗，气温25度，适合外出活动。"
    )
    
    # 查询示例
    result = cache.query("今天天气怎么样？")
    if result:
        print(f"缓存命中 ({result.cache_type})!")
        print(f"相似度: {result.similarity:.2f}")
        print(f"响应: {result.response}")
    else:
        print("缓存未命中")
    
    # 统计
    stats = cache.get_stats()
    print(f"\n缓存统计: {stats.l1_entries} L1条目, {stats.l2_entries} L2条目")
    
    cache.close()
