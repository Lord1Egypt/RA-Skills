#!/usr/bin/env python3
"""
语义缓存模块 - 基于语义的智能缓存

功能：
- 语义相似度缓存
- 查询改写缓存
- 上下文感知缓存
- 缓存预热
- 缓存淘汰策略（LRU/TTL/语义相似度）
"""

import sys
import json
import hashlib
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from collections import OrderedDict
import re

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_memory_base


class SemanticCache:
    """语义缓存"""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache_dir = get_memory_base() / ".cache" / "semantic"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self._memory_cache: OrderedDict = OrderedDict()
        self._access_times: Dict[str, float] = {}
        self._load_disk_cache()
    
    def _load_disk_cache(self):
        """从磁盘加载缓存"""
        cache_file = self.cache_dir / "semantic_cache.json"
        if cache_file.exists():
            try:
                with open(cache_file) as f:
                    data = json.load(f)
                
                # 清理过期条目
                now = time.time()
                for key, item in list(data.items()):
                    if now - item.get('timestamp', 0) > self.ttl_seconds:
                        del data[key]
                
                self._memory_cache = OrderedDict(
                    (k, v) for k, v in data.items()
                    if now - v.get('timestamp', 0) <= self.ttl_seconds
                )
            except:
                pass
    
    def _save_disk_cache(self):
        """保存缓存到磁盘"""
        cache_file = self.cache_dir / "semantic_cache.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(dict(self._memory_cache), f, ensure_ascii=False)
        except:
            pass
    
    def _generate_key(self, query: str, context: Optional[Dict] = None) -> str:
        """生成缓存键"""
        key_data = {
            'query': query,
            'context': context or {}
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _is_similar(self, text1: str, text2: str, threshold: float = 0.85) -> bool:
        """简单语义相似度检测"""
        # 去除标点、转小写
        t1 = re.sub(r'[^\w]', '', text1.lower())
        t2 = re.sub(r'[^\w]', '', text2.lower())
        
        # 简单词集合相似度
        words1 = set(t1)
        words2 = set(t2)
        
        if not words1 or not words2:
            return False
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        similarity = intersection / union if union > 0 else 0
        return similarity >= threshold
    
    def get(self, query: str, context: Optional[Dict] = None) -> Optional[Any]:
        """获取缓存"""
        key = self._generate_key(query, context)
        
        # 检查精确键
        if key in self._memory_cache:
            item = self._memory_cache[key]
            if time.time() - item.get('timestamp', 0) <= self.ttl_seconds:
                self._memory_cache.move_to_end(key)
                self._access_times[key] = time.time()
                return item.get('result')
            else:
                del self._memory_cache[key]
        
        # 检查语义相似键
        for cached_key, item in self._memory_cache.items():
            if time.time() - item.get('timestamp', 0) <= self.ttl_seconds:
                if self._is_similar(query, item.get('query', '')):
                    self._memory_cache.move_to_end(cached_key)
                    self._access_times[key] = time.time()
                    return item.get('result')
        
        return None
    
    def set(self, query: str, result: Any, context: Optional[Dict] = None):
        """设置缓存"""
        key = self._generate_key(query, context)
        
        # LRU 淘汰
        if len(self._memory_cache) >= self.max_size:
            oldest_key = next(iter(self._memory_cache))
            del self._memory_cache[oldest_key]
        
        self._memory_cache[key] = {
            'query': query,
            'context': context,
            'result': result,
            'timestamp': time.time()
        }
        self._access_times[key] = time.time()
        
        # 定期保存
        if len(self._memory_cache) % 10 == 0:
            self._save_disk_cache()
    
    def invalidate(self, pattern: Optional[str] = None):
        """使缓存失效"""
        if pattern is None:
            self._memory_cache.clear()
            self._access_times.clear()
        else:
            for key in list(self._memory_cache.keys()):
                if pattern in self._memory_cache[key].get('query', ''):
                    del self._memory_cache[key]
        
        self._save_disk_cache()
    
    def get_stats(self) -> Dict:
        """获取缓存统计"""
        now = time.time()
        valid_entries = [
            k for k, v in self._memory_cache.items()
            if now - v.get('timestamp', 0) <= self.ttl_seconds
        ]
        
        return {
            'size': len(valid_entries),
            'max_size': self.max_size,
            'ttl_seconds': self.ttl_seconds,
            'hit_rate_estimate': len(self._access_times) / max(len(valid_entries), 1)
        }
    
    def warmup(self, queries: List[Tuple[str, Any, Optional[Dict]]]):
        """预热缓存"""
        for query, result, context in queries:
            self.set(query, result, context)
        self._save_disk_cache()
    
    def cleanup_expired(self):
        """清理过期条目"""
        now = time.time()
        expired_keys = [
            k for k, v in self._memory_cache.items()
            if now - v.get('timestamp', 0) > self.ttl_seconds
        ]
        
        for key in expired_keys:
            del self._memory_cache[key]
        
        if expired_keys:
            self._save_disk_cache()
        
        return len(expired_keys)


class QueryRewriteCache:
    """查询改写缓存"""
    
    def __init__(self):
        self.cache_dir = get_memory_base() / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._rewrites: Dict[str, str] = {}
        self._load()
    
    def _load(self):
        """加载缓存"""
        cache_file = self.cache_dir / "query_rewrites.json"
        if cache_file.exists():
            try:
                with open(cache_file) as f:
                    self._rewrites = json.load(f)
            except:
                pass
    
    def _save(self):
        """保存缓存"""
        cache_file = self.cache_dir / "query_rewrites.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(self._rewrites, f, ensure_ascii=False)
        except:
            pass
    
    def get_rewrite(self, original: str) -> Optional[str]:
        """获取改写后的查询"""
        return self._rewrites.get(original)
    
    def add_rewrite(self, original: str, rewritten: str):
        """添加改写规则"""
        self._rewrites[original] = rewritten
        self._save()
    
    def remove_rewrite(self, original: str):
        """移除改写规则"""
        if original in self._rewrites:
            del self._rewrites[original]
            self._save()
    
    def get_all_rewrites(self) -> Dict[str, str]:
        """获取所有改写规则"""
        return dict(self._rewrites)


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='语义缓存')
    parser.add_argument('--stats', '-s', action='store_true', help='显示统计')
    parser.add_argument('--clear', '-c', action='store_true', help='清空缓存')
    parser.add_argument('--cleanup', action='store_true', help='清理过期')
    args = parser.parse_args()
    
    cache = SemanticCache()
    
    if args.clear:
        cache.invalidate()
        print("✅ 缓存已清空")
    elif args.cleanup:
        count = cache.cleanup_expired()
        print(f"✅ 已清理 {count} 个过期条目")
    elif args.stats:
        stats = cache.get_stats()
        print("# 💾 语义缓存统计")
        for k, v in stats.items():
            print(f"- {k}: {v}")
    else:
        stats = cache.get_stats()
        print(f"# 💾 缓存状态：{stats['size']}/{stats['max_size']}")
    
    cache._save_disk_cache()


if __name__ == '__main__':
    main()
