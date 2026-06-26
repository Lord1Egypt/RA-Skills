#!/usr/bin/env python3
"""批量搜索优化器
功能：
1. 批量搜索 - 一次查询多个关键词
2. 结果缓存 - 避免重复搜索
3. 智能合并 - 去重+排序
"""
import time
from typing import List, Dict, Optional

class BatchSearchOptimizer:
    """批量搜索优化器"""
    
    def __init__(self, memory_instance):
        self.m = memory_instance
        self._result_cache = {}
        self._cache_ttl = 60
    
    def batch_search(self, queries: List[str], limit: int = 3) -> Dict[str, List]:
        """批量搜索"""
        results = {}
        queries_to_search = []
        
        now = time.time()
        for q in queries:
            cache_key = f"{q}:{limit}"
            if cache_key in self._result_cache:
                cached_result, cached_time = self._result_cache[cache_key]
                if now - cached_time < self._cache_ttl:
                    results[q] = cached_result
                else:
                    queries_to_search.append(q)
            else:
                queries_to_search.append(q)
        
        if queries_to_search:
            search_results = self._execute_batch(queries_to_search, limit)
            results.update(search_results)
        
        return results
    
    def _execute_batch(self, queries: List[str], limit: int) -> Dict[str, List]:
        """执行批量搜索"""
        all_results = {}
        
        for q in queries:
            start = time.time()
            result = self.m.search(q, limit=limit)
            elapsed = (time.time() - start) * 1000
            
            all_results[q] = {
                'items': result.get('results', []),
                'method': result.get('method', 'unknown'),
                'elapsed_ms': elapsed,
                'count': result.get('total', 0)
            }
            
            cache_key = f"{q}:{limit}"
            self._result_cache[cache_key] = (all_results[q], time.time())
        
        return all_results
    
    def search_with_dedup(self, queries: List[str], limit: int = 3) -> List[Dict]:
        """搜索并智能合并去重"""
        results = self.batch_search(queries, limit)
        
        seen = set()
        merged = []
        
        for q, result in results.items():
            for item in result.get('items', []):
                title = item.get('s', '')
                if title and title not in seen:
                    seen.add(title)
                    item['query'] = q
                    merged.append(item)
        
        return merged
    
    def invalidate_cache(self, query: Optional[str] = None):
        """清除缓存"""
        if query is None:
            self._result_cache.clear()
        else:
            keys_to_remove = [k for k in self._result_cache if k.startswith(query)]
            for k in keys_to_remove:
                del self._result_cache[k]


class QueryRouter:
    """智能查询路由"""
    
    FAST_PATH_KEYWORDS = {'记忆', '状态', '统计', '帮助', '搜索', '查询'}
    
    @classmethod
    def route(cls, query: str) -> str:
        """路由决策"""
        q = query.strip().lower()
        
        if q in cls.FAST_PATH_KEYWORDS or any(kw in q for kw in cls.FAST_PATH_KEYWORDS):
            return 'fast'
        
        if len(q.split()) <= 2:
            return 'fts'
        
        return 'hybrid'


if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/home/tiamo/.openclaw/workspace/skills/yaoyao-memory/scripts')
    from memory import Memory
    
    m = Memory()
    optimizer = BatchSearchOptimizer(m)
    
    print('=== 批量搜索测试 ===')
    
    queries = ['记忆', '配置', '系统', '性能']
    start = time.time()
    results = optimizer.batch_search(queries, limit=3)
    elapsed = (time.time() - start) * 1000
    
    print(f'批量搜索 {len(queries)} 个查询: {elapsed:.0f}ms\n')
    
    for q, r in results.items():
        print(f'{q}: {r["count"]} results ({r["method"]}, {r["elapsed_ms"]:.0f}ms)')
    
    print('\n=== 去重合并测试 ===')
    dedup = optimizer.search_with_dedup(['记忆', '系统', '用户'], limit=3)
    print(f'合并后: {len(dedup)} 条唯一结果')
    
    print('\n=== 查询路由测试 ===')
    for q in ['记忆', '系统配置', '用户偏好设置']:
        route = QueryRouter.route(q)
        print(f'{q!r} -> {route}')
