#!/usr/bin/env python3
"""
搜索引擎 v2.0 - 全面优化版
集成所有优化：连接池、缓存、日志、异步、监控
"""

import sqlite3
import struct
import re
import asyncio
from pathlib import Path
from typing import List, Optional, AsyncGenerator
from concurrent.futures import ThreadPoolExecutor

# 导入所有优化模块
from connection_pool import get_connection
from query_cache import get_cache
from unified_logger import get_logger
from performance_monitor import get_monitor

logger = get_logger("search_engine_v2")
cache = get_cache("search_v2")
monitor = get_monitor()

class SearchEngineV2:
    """搜索引擎 v2.0（全面优化版）"""
    
    def __init__(self, db_path: str, vec_ext: str):
        self.db_path = db_path
        self.vec_ext = vec_ext
        logger.info(f"搜索引擎 v2.0 初始化: {db_path}")
    
    def _get_connection(self):
        """获取数据库连接（使用连接池）"""
        return get_connection(self.db_path)
    
    def vector_search(self, embedding: List[float], top_k: int = 20, max_distance: float = 0.8) -> List[dict]:
        """向量搜索（全面优化版）"""
        import time
        start_time = time.time()
        
        if not embedding:
            return []
        
        # 验证 top_k
        if not isinstance(top_k, int) or top_k < 1 or top_k > 100:
            top_k = 20
        
        # 检查缓存
        cache_key = f"vec_{hash(tuple(embedding))}_{top_k}"
        cached = cache.get(cache_key)
        if cached is not None:
            latency = (time.time() - start_time) * 1000
            monitor.record_query("vector_search", latency, cache_hit=True)
            logger.debug("向量搜索命中缓存")
            return cached
        
        vec_hex = struct.pack(f'{len(embedding)}f', *embedding).hex()
        
        with self._get_connection() as conn:
            try:
                conn.enable_load_extension(True)
                conn.load_extension(self.vec_ext)
                cursor = conn.cursor()
                
                # 使用参数化查询
                sql = """
                    SELECT v.record_id, r.content, r.type, r.scene_name, v.distance 
                    FROM l1_vec v 
                    JOIN l1_records r ON v.record_id = r.record_id 
                    WHERE v.embedding MATCH ? AND k = ? 
                    ORDER BY v.distance ASC
                """
                cursor.execute(sql, (f"X'{vec_hex}'", top_k))
                results = cursor.fetchall()
                
                parsed = self._parse_vector_results_safe(results, max_distance)
                
                # 存入缓存
                cache.set(cache_key, None, parsed)
                
                # 记录监控
                latency = (time.time() - start_time) * 1000
                monitor.record_query("vector_search", latency, cache_hit=False)
                
                logger.info(f"向量搜索完成: {len(parsed)} 条结果, 耗时: {latency:.2f}ms")
                return parsed
                
            except Exception as e:
                monitor.record_error("vector_search")
                logger.error(f"向量搜索失败: {e}")
                return []
    
    def fts_search(self, query: str, top_k: int = 10) -> List[dict]:
        """FTS 搜索（全面优化版）"""
        import time
        start_time = time.time()
        
        # 输入验证
        query = re.sub(r'[^\w\u4e00-\u9fff\s]', '', query)
        
        if not isinstance(top_k, int) or top_k < 1 or top_k > 100:
            top_k = 10
        
        tokens = query.replace('，', ' ').replace('、', ' ').split()
        tokens = [t for t in tokens if len(t) > 0]
        
        if not tokens:
            return []
        
        # 检查缓存
        cache_key = f"fts_{hash(query)}_{top_k}"
        cached = cache.get(cache_key)
        if cached is not None:
            latency = (time.time() - start_time) * 1000
            monitor.record_query("fts_search", latency, cache_hit=True)
            logger.debug("FTS 搜索命中缓存")
            return cached
        
        fts_query = " OR ".join(tokens)
        
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                
                # 使用参数化查询
                sql = """
                    SELECT record_id, content, type, scene_name 
                    FROM l1_fts 
                    WHERE l1_fts MATCH ? 
                    ORDER BY rank 
                    LIMIT ?
                """
                cursor.execute(sql, (fts_query, top_k))
                results = cursor.fetchall()
                
                parsed = self._parse_fts_results_safe(results)
                
                # 存入缓存
                cache.set(cache_key, None, parsed)
                
                # 记录监控
                latency = (time.time() - start_time) * 1000
                monitor.record_query("fts_search", latency, cache_hit=False)
                
                logger.info(f"FTS 搜索完成: {len(parsed)} 条结果, 耗时: {latency:.2f}ms")
                return parsed
                
            except Exception as e:
                monitor.record_error("fts_search")
                logger.error(f"FTS 搜索失败: {e}")
                return []
    
    def parallel_search(self, embedding: List[float], query: str) -> tuple:
        """并行搜索"""
        with ThreadPoolExecutor(max_workers=2) as executor:
            f1 = executor.submit(self.vector_search, embedding)
            f2 = executor.submit(self.fts_search, query)
            return f1.result(), f2.result()
    
    def _parse_vector_results_safe(self, results: List[tuple], max_distance: float = 0.8) -> List[dict]:
        """解析向量结果"""
        parsed = []
        for row in results:
            if len(row) >= 5:
                try:
                    dist = float(row[4])
                    if dist < max_distance:
                        parsed.append({
                            "record_id": str(row[0]),
                            "content": str(row[1]),
                            "type": str(row[2]),
                            "scene": str(row[3]),
                            "distance": dist,
                            "score": 1.0 - dist,
                            "source": "vector"
                        })
                except (ValueError, TypeError):
                    pass
        return parsed
    
    def _parse_fts_results_safe(self, results: List[tuple]) -> List[dict]:
        """解析 FTS 结果"""
        parsed = []
        for row in results:
            if len(row) >= 4:
                parsed.append({
                    "record_id": str(row[0]),
                    "content": str(row[1]),
                    "type": str(row[2]),
                    "scene": str(row[3]),
                    "source": "fts"
                })
        return parsed
    
    @staticmethod
    def merge(vector_results: List[dict], fts_results: List[dict]) -> List[dict]:
        """合并去重"""
        seen = set()
        merged = []
        
        for r in vector_results:
            if r["record_id"] not in seen:
                merged.append(r)
                seen.add(r["record_id"])
        
        for r in fts_results:
            if r["record_id"] not in seen:
                merged.append(r)
                seen.add(r["record_id"])
        
        merged.sort(key=lambda x: x.get("score", 0), reverse=True)
        return merged
    
    @staticmethod
    def get_cache_stats() -> dict:
        """获取缓存统计"""
        return cache.get_stats()
    
    @staticmethod
    def get_monitor_stats() -> dict:
        """获取监控统计"""
        return monitor.get_summary()
