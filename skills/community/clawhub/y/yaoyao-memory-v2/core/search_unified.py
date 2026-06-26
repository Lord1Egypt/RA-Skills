#!/usr/bin/env python3
"""
统一搜索模块 - 整合 search.py + search_optimized.py + search_v2.py
"""
import time
import sqlite3
import struct
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor

from .embedding import EmbeddingEngine
from .router import QueryRouter, QueryIntent


class SearchMode(Enum):
    """搜索模式"""
    FAST = "fast"         # 快速搜索（缓存优先）
    BALANCED = "balanced" # 平衡模式
    FULL = "full"         # 完整模式（混合搜索）


class UnifiedSearch:
    """
    统一搜索接口
    整合了基础搜索、优化搜索、v2搜索的所有功能
    """
    
    def __init__(
        self,
        db_path: str,
        vec_ext: str,
        embedding_engine: EmbeddingEngine,
        cache_dir: str = None
    ):
        self.db_path = db_path
        self.vec_ext = vec_ext
        self.embedding_engine = embedding_engine
        self.cache_dir = cache_dir or str(Path.home() / ".openclaw" / "memory-tdai" / ".cache")
        
        # 连接池（简单实现）
        self._connections = []
        self._max_connections = 5
        
        # 查询缓存
        self._query_cache = {}
        self._cache_ttl = 300  # 5分钟
        
        # 并行搜索器
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接（带连接池）"""
        if self._connections:
            conn = self._connections.pop()
            return conn
        
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.enable_load_extension(True)
        try:
            conn.load_extension(self.vec_ext)
        except:
            pass  # Extension may not be available
        return conn
    
    def _return_connection(self, conn: sqlite3.Connection):
        """归还连接到池中"""
        if len(self._connections) < self._max_connections:
            self._connections.append(conn)
        else:
            conn.close()
    
    def search(
        self,
        query: str,
        mode: str = "auto",
        top_k: int = 20,
        use_cache: bool = True,
        intent_hints: Dict = None
    ) -> Dict:
        """
        统一搜索接口
        
        Args:
            query: 查询文本
            mode: 搜索模式 (auto/fast/balanced/full)
            top_k: 返回结果数
            use_cache: 是否使用缓存
            intent_hints: 意图提示（来自 QueryRouter）
        
        Returns:
            {
                "results": [...],
                "method": "vector/fts/hybrid",
                "latency_ms": 12,
                "cached": False
            }
        """
        start = time.time()
        
        # 1. 分析查询意图（如果未提供）
        if intent_hints is None:
            intent = QueryRouter.detect_intent(query)
            complexity = QueryRouter.analyze(query)
            intent_hints = QueryRouter.get_search_hints(query)
        else:
            intent = QueryIntent(intent_hints.get("intent", "unknown"))
            complexity = intent_hints.get("complexity", "balanced")
        
        # 2. 确定搜索模式
        if mode == "auto":
            if complexity == "fast":
                mode = "fast"
            elif complexity == "full":
                mode = "full"
            else:
                mode = "balanced"
        
        # 3. 执行搜索
        cache_key = f"{query}_{mode}_{top_k}"
        
        if use_cache and cache_key in self._query_cache:
            cached_result, cached_time = self._query_cache[cache_key]
            if time.time() - cached_time < self._cache_ttl:
                cached_result["cached"] = True
                return cached_result
        
        # 根据模式执行搜索
        if mode == "fast":
            results = self._fast_search(query, top_k)
            method = "fts"
        elif mode == "full":
            results = self._hybrid_search(query, top_k, intent_hints)
            method = "hybrid"
        else:
            results = self._balanced_search(query, top_k, intent_hints)
            method = "vector" if results else "fts"
        
        # 4. 构建返回
        result = {
            "results": results,
            "method": method,
            "latency_ms": int((time.time() - start) * 1000),
            "cached": False,
            "intent": intent.value,
            "complexity": complexity
        }
        
        # 缓存结果
        if use_cache:
            self._query_cache[cache_key] = (result, time.time())
        
        return result
    
    def _fast_search(self, query: str, top_k: int) -> List[Dict]:
        """快速FTS搜索"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, content, type, scene_name, updated_at
                FROM memory_index
                WHERE content LIKE ?
                ORDER BY updated_at DESC
                LIMIT ?
            """, (f"%{query}%", top_k))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "content": row[1],
                    "type": row[2],
                    "scene_name": row[3],
                    "updated_at": row[4],
                    "score": 1.0  # FTS doesn't have distance
                })
            return results
        finally:
            self._return_connection(conn)
    
    def _balanced_search(self, query: str, top_k: int, intent_hints: Dict) -> List[Dict]:
        """平衡模式：向量搜索 + 可选FTS补充"""
        # 获取查询向量
        embedding = self.embedding_engine.get(query)
        if not embedding:
            return self._fast_search(query, top_k)
        
        # 向量搜索
        vec_results = self._vector_search(embedding, top_k)
        
        if not vec_results or intent_hints.get("require_rerank"):
            # 如果向量结果不足，补充FTS结果
            fts_results = self._fast_search(query, top_k // 2)
            return self._merge_results(vec_results, fts_results)
        
        return vec_results
    
    def _hybrid_search(self, query: str, top_k: int, intent_hints: Dict) -> List[Dict]:
        """混合搜索：向量 + FTS + RRF融合"""
        # 获取查询向量
        embedding = self.embedding_engine.get(query)
        
        # 并行执行向量和FTS搜索
        with ThreadPoolExecutor(max_workers=2) as executor:
            vec_future = executor.submit(self._vector_search, embedding, top_k * 2 if embedding else 0)
            fts_future = executor.submit(self._fast_search, query, top_k * 2)
            
            vec_results = vec_future.result() if embedding else []
            fts_results = fts_future.result()
        
        # RRF融合
        return self._rrf_fusion(vec_results, fts_results, top_k)
    
    def _vector_search(self, embedding: List[float], top_k: int) -> List[Dict]:
        """向量搜索"""
        if not embedding:
            return []
        
        conn = self._get_connection()
        try:
            vec_hex = struct.pack(f'{len(embedding)}f', *embedding).hex()
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.record_id, r.content, r.type, r.scene_name, v.distance
                FROM vectors v
                JOIN memory_index r ON v.record_id = r.id
                WHERE v.embedding = ?
                ORDER BY v.distance ASC
                LIMIT ?
            """, (vec_hex, top_k))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "content": row[1],
                    "type": row[2],
                    "scene_name": row[3],
                    "distance": row[4],
                    "score": 1 - row[4] if row[4] <= 1 else 0
                })
            return results
        except Exception as e:
            print(f"Vector search error: {e}")
            return []
        finally:
            self._return_connection(conn)
    
    def _merge_results(self, vec_results: List[Dict], fts_results: List[Dict]) -> List[Dict]:
        """合并向量和FTS结果"""
        seen = set()
        merged = []
        
        # 优先添加向量结果
        for r in vec_results:
            if r["id"] not in seen:
                seen.add(r["id"])
                merged.append(r)
        
        # 补充FTS结果
        for r in fts_results:
            if r["id"] not in seen:
                seen.add(r["id"])
                merged.append(r)
        
        return merged[:20]
    
    def _rrf_fusion(
        self,
        vec_results: List[Dict],
        fts_results: List[Dict],
        top_k: int,
        k: int = 60
    ) -> List[Dict]:
        """
        RRF (Reciprocal Rank Fusion) 融合
        
        RRF score = Σ (1 / (k + rank))
        """
        scores = {}
        
        # 向量结果评分
        for i, r in enumerate(vec_results):
            rrf_score = 1 / (k + i + 1)
            scores[r["id"]] = scores.get(r["id"], 0) + rrf_score * 0.6
            r["rrf_score"] = rrf_score * 0.6
        
        # FTS结果评分
        for i, r in enumerate(fts_results):
            rrf_score = 1 / (k + i + 1)
            if r["id"] in scores:
                scores[r["id"]] += rrf_score * 0.4
                # 合并类型
                if r["type"] not in [x.get("type") for x in vec_results if x["id"] == r["id"]]:
                    pass  # Type already set
            else:
                scores[r["id"]] = rrf_score * 0.4
                r["rrf_score"] = rrf_score * 0.4
                vec_results.append(r)  # Add to vec_results for final sort
        
        # 按RRF分数排序
        for r in vec_results:
            r["score"] = scores.get(r["id"], r.get("score", 0))
        
        vec_results.sort(key=lambda x: -x["score"])
        
        return vec_results[:top_k]
    
    def close(self):
        """关闭搜索器，释放资源"""
        self._executor.shutdown(wait=True)
        for conn in self._connections:
            conn.close()
        self._connections.clear()


# 导出
from enum import Enum
__all__ = ["UnifiedSearch", "SearchMode"]
