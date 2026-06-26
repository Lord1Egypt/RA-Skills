#!/usr/bin/env python3
"""
Smart Cache Manager - 本地智能缓存管理工具
用于管理L1精确缓存和L2语义缓存
"""

import os
import sys
import json
import hashlib
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any
import sqlite3
import threading

# 配置默认路径
CACHE_DIR = Path.home() / ".qclaw" / "smart-cache" / "data"
CONFIG_FILE = Path.home() / ".qclaw" / "smart-cache" / "config.json"
DB_FILE = CACHE_DIR / "cache.db"

# 默认配置
DEFAULT_CONFIG = {
    "cache_dir": str(CACHE_DIR),
    "l1_max_size": 10000,
    "l2_max_size": 5000,
    "ttl_hours": 168,
    "similarity_threshold": 0.85,
    "enable_cost_tracking": True,
    "cost_per_1k_tokens": 0.002
}


class CacheConfig:
    """缓存配置管理"""
    
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        return DEFAULT_CONFIG
    
    def save_config(self):
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)


class CacheDB:
    """SQLite缓存数据库"""
    
    def __init__(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(DB_FILE), check_same_thread=False)
        self.lock = threading.Lock()
        self._init_tables()
    
    def _init_tables(self):
        with self.lock:
            cursor = self.conn.cursor()
            
            # L1精确缓存表
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
            
            # L2语义缓存表
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
    
    def close(self):
        self.conn.close()


class SmartCache:
    """智能缓存主类"""
    
    def __init__(self, config: Optional[CacheConfig] = None):
        self.config = config or CacheConfig()
        self.db = CacheDB()
    
    @staticmethod
    def _hash_query(query: str) -> str:
        """生成查询的SHA256哈希"""
        normalized = query.strip().lower()
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()
    
    def query_l1(self, query: str) -> Optional[Dict[str, Any]]:
        """L1精确缓存查询"""
        query_hash = self._hash_query(query)
        
        with self.db.lock:
            cursor = self.db.conn.cursor()
            cursor.execute('''
                SELECT response, created_at, hit_count, tokens_saved 
                FROM l1_cache 
                WHERE query_hash = ? AND (expires_at IS NULL OR expires_at > datetime('now'))
            ''', (query_hash,))
            
            result = cursor.fetchone()
            
            if result:
                # 更新命中次数
                cursor.execute('''
                    UPDATE l1_cache SET hit_count = hit_count + 1 WHERE query_hash = ?
                ''', (query_hash,))
                self.db.conn.commit()
                
                return {
                    'response': result[0],
                    'created_at': result[1],
                    'hit_count': result[2] + 1,
                    'tokens_saved': result[3],
                    'similarity': 1.0,
                    'cache_type': 'L1'
                }
        
        return None
    
    def store_l1(self, query: str, response: str, tokens: int = 0) -> bool:
        """存储到L1缓存"""
        query_hash = self._hash_query(query)
        ttl_hours = self.config.config.get('ttl_hours', 168)
        expires_at = datetime.now() + timedelta(hours=ttl_hours)
        
        with self.db.lock:
            cursor = self.db.conn.cursor()
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO l1_cache 
                    (query_hash, query, response, expires_at, tokens_saved)
                    VALUES (?, ?, ?, ?, ?)
                ''', (query_hash, query, response, expires_at.isoformat(), tokens))
                self.db.conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"存储L1缓存失败: {e}")
                return False
    
    def query_l2(self, query: str, threshold: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """L2语义缓存查询（简化版，基于关键词匹配）"""
        threshold = threshold or self.config.config.get('similarity_threshold', 0.85)
        query_words = set(query.lower().split())
        
        with self.db.lock:
            cursor = self.db.conn.cursor()
            cursor.execute('''
                SELECT query, response, created_at, hit_count, tokens_saved 
                FROM l2_cache 
                WHERE expires_at IS NULL OR expires_at > datetime('now')
            ''')
            
            best_match = None
            best_similarity = 0.0
            
            for row in cursor.fetchall():
                cached_query = row[0]
                cached_words = set(cached_query.lower().split())
                
                # 计算字符级bigram相似度（支持中文）
                def get_ngrams(text, n=2):
                    text = text.strip().lower()
                    return set(text[i:i+n] for i in range(len(text) - n + 1))
                
                ngrams1 = get_ngrams(query)
                ngrams2 = get_ngrams(cached_query)
                
                if ngrams1 and ngrams2:
                    intersection = len(ngrams1 & ngrams2)
                    union = len(ngrams1 | ngrams2)
                    similarity = intersection / union if union > 0 else 0
                    
                    if similarity >= threshold and similarity > best_similarity:
                        best_similarity = similarity
                        best_match = {
                            'response': row[1],
                            'created_at': row[2],
                            'hit_count': row[3],
                            'tokens_saved': row[4],
                            'similarity': similarity,
                            'cache_type': 'L2',
                            'matched_query': cached_query
                        }
            
            if best_match:
                # 更新命中次数
                cursor.execute('''
                    UPDATE l2_cache SET hit_count = hit_count + 1 
                    WHERE query = ?
                ''', (best_match['matched_query'],))
                self.db.conn.commit()
            
            return best_match
    
    def store_l2(self, query: str, response: str, tokens: int = 0) -> bool:
        """存储到L2缓存"""
        ttl_hours = self.config.config.get('ttl_hours', 168)
        expires_at = datetime.now() + timedelta(hours=ttl_hours)
        
        with self.db.lock:
            cursor = self.db.conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO l2_cache 
                    (query, response, expires_at, tokens_saved)
                    VALUES (?, ?, ?, ?)
                ''', (query, response, expires_at.isoformat(), tokens))
                self.db.conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"存储L2缓存失败: {e}")
                return False
    
    def query(self, query: str, threshold: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """智能查询（先L1后L2）"""
        # 先尝试L1精确匹配
        result = self.query_l1(query)
        if result:
            return result
        
        # 再尝试L2语义匹配
        return self.query_l2(query, threshold)
    
    def store(self, query: str, response: str, tokens: int = 0) -> bool:
        """存储到缓存（同时存L1和L2）"""
        success_l1 = self.store_l1(query, response, tokens)
        success_l2 = self.store_l2(query, response, tokens)
        return success_l1 or success_l2
    
    def clean_expired(self) -> int:
        """清理过期缓存"""
        count = 0
        with self.db.lock:
            cursor = self.db.conn.cursor()
            cursor.execute("DELETE FROM l1_cache WHERE expires_at < datetime('now')")
            count += cursor.rowcount
            cursor.execute("DELETE FROM l2_cache WHERE expires_at < datetime('now')")
            count += cursor.rowcount
            self.db.conn.commit()
        return count
    
    def clean_all(self) -> int:
        """清理所有缓存"""
        count = 0
        with self.db.lock:
            cursor = self.db.conn.cursor()
            cursor.execute("DELETE FROM l1_cache")
            count += cursor.rowcount
            cursor.execute("DELETE FROM l2_cache")
            count += cursor.rowcount
            self.db.conn.commit()
        return count
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        with self.db.lock:
            cursor = self.db.conn.cursor()
            
            # L1统计
            cursor.execute("SELECT COUNT(*), SUM(hit_count), SUM(tokens_saved) FROM l1_cache")
            l1_stats = cursor.fetchone()
            
            # L2统计
            cursor.execute("SELECT COUNT(*), SUM(hit_count), SUM(tokens_saved) FROM l2_cache")
            l2_stats = cursor.fetchone()
            
            # 总统计
            cursor.execute('''
                SELECT 
                    SUM(total_requests),
                    SUM(l1_hits),
                    SUM(l2_hits),
                    SUM(misses),
                    SUM(tokens_saved),
                    SUM(cost_saved)
                FROM stats
            ''')
            total_stats = cursor.fetchone()
        
        return {
            'l1_entries': l1_stats[0] or 0,
            'l1_hits': l1_stats[1] or 0,
            'l1_tokens_saved': l1_stats[2] or 0,
            'l2_entries': l2_stats[0] or 0,
            'l2_hits': l2_stats[1] or 0,
            'l2_tokens_saved': l2_stats[2] or 0,
            'total_requests': total_stats[0] or 0,
            'total_l1_hits': total_stats[1] or 0,
            'total_l2_hits': total_stats[2] or 0,
            'total_misses': total_stats[3] or 0,
            'total_tokens_saved': total_stats[4] or 0,
            'total_cost_saved': total_stats[5] or 0.0
        }
    
    def close(self):
        self.db.close()


def print_status():
    """打印缓存状态"""
    cache = SmartCache()
    stats = cache.get_stats()
    cache.close()
    
    print("\n📊 智能缓存状态")
    print("━" * 40)
    print(f"L1缓存条目: {stats['l1_entries']}")
    print(f"L2缓存条目: {stats['l2_entries']}")
    print(f"L1命中次数: {stats['l1_hits']}")
    print(f"L2命中次数: {stats['l2_hits']}")
    print()
    print(f"累计节省Token: {stats['total_tokens_saved']}")
    print(f"累计节省费用: ${stats['total_cost_saved']:.4f}")
    print()


def print_stats():
    """打印详细统计"""
    cache = SmartCache()
    stats = cache.get_stats()
    cache.close()
    
    total = stats['total_requests'] or 1
    
    print("\n📊 缓存统计详情")
    print("━" * 40)
    print(f"总请求数: {stats['total_requests']}")
    print(f"L1命中: {stats['total_l1_hits']} ({stats['total_l1_hits']/total*100:.1f}%)")
    print(f"L2命中: {stats['total_l2_hits']} ({stats['total_l2_hits']/total*100:.1f}%)")
    print(f"缓存未命中: {stats['total_misses']} ({stats['total_misses']/total*100:.1f}%)")
    print()
    print("💰 成本节省")
    print("━" * 40)
    print(f"节省Token: {stats['total_tokens_saved']}")
    print(f"估算节省: ${stats['total_cost_saved']:.4f}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='Smart Cache Manager - 本地智能缓存管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # status命令
    subparsers.add_parser('status', help='查看缓存状态')
    
    # stats命令
    subparsers.add_parser('stats', help='查看详细统计')
    
    # query命令
    query_parser = subparsers.add_parser('query', help='精确查询缓存')
    query_parser.add_argument('text', help='查询文本')
    
    # query-semantic命令
    semantic_parser = subparsers.add_parser('query-semantic', help='语义查询缓存')
    semantic_parser.add_argument('text', help='查询文本')
    semantic_parser.add_argument('--threshold', type=float, default=0.85, help='相似度阈值')
    
    # add命令
    add_parser = subparsers.add_parser('add', help='添加缓存')
    add_parser.add_argument('query', help='查询文本')
    add_parser.add_argument('response', help='响应文本')
    add_parser.add_argument('--tokens', type=int, default=0, help='Token数量')
    
    # clean命令
    clean_parser = subparsers.add_parser('clean', help='清理缓存')
    clean_group = clean_parser.add_mutually_exclusive_group(required=True)
    clean_group.add_argument('--expired', action='store_true', help='清理过期缓存')
    clean_group.add_argument('--all', action='store_true', help='清理所有缓存')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cache = SmartCache()
    
    try:
        if args.command == 'status':
            print_status()
        
        elif args.command == 'stats':
            print_stats()
        
        elif args.command == 'query':
            result = cache.query_l1(args.text)
            if result:
                print(f"\n✅ L1缓存命中")
                print(f"响应: {result['response'][:200]}...")
                print(f"相似度: {result['similarity']}")
            else:
                print("\n❌ 缓存未命中")
        
        elif args.command == 'query-semantic':
            result = cache.query(args.text, args.threshold)
            if result:
                print(f"\n✅ {result['cache_type']}缓存命中")
                print(f"响应: {result['response'][:200]}...")
                print(f"相似度: {result['similarity']:.2f}")
                if result.get('matched_query'):
                    print(f"匹配查询: {result['matched_query']}")
            else:
                print("\n❌ 缓存未命中")
        
        elif args.command == 'add':
            success = cache.store(args.query, args.response, args.tokens)
            if success:
                print(f"\n✅ 缓存已添加")
            else:
                print("\n❌ 添加失败")
        
        elif args.command == 'clean':
            if args.expired:
                count = cache.clean_expired()
                print(f"\n✅ 已清理 {count} 条过期缓存")
            elif args.all:
                count = cache.clean_all()
                print(f"\n✅ 已清理 {count} 条缓存")
    
    finally:
        cache.close()


if __name__ == '__main__':
    main()
