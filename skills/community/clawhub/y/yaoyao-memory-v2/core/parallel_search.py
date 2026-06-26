#!/usr/bin/env python3
"""
并行搜索 - 多策略并行执行，结果智能合并
"""
import time
from typing import List, Dict, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum


class SearchStrategy(Enum):
    """搜索策略枚举"""
    VECTOR = "vector"       # 向量搜索
    FTS = "fts"             # 全文搜索
    HYBRID = "hybrid"       # 混合搜索
    FAST = "fast"           # 快速搜索（缓存优先）


@dataclass
class SearchResult:
    """搜索结果"""
    strategy: SearchStrategy
    results: List[Dict]
    latency_ms: float
    cached: bool = False


@dataclass
class MergedResult:
    """合并后的搜索结果"""
    id: str
    content: str
    score: float
    strategies: List[SearchStrategy]
    types: List[str]


class ParallelSearcher:
    """并行搜索器"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
    
    def search_parallel(
        self,
        query: str,
        vector_func,  # 向量搜索函数
        fts_func,     # FTS搜索函数
        embedding: Optional[List[float]] = None,
        top_k: int = 10
    ) -> Tuple[List[MergedResult], Dict[str, any]]:
        """
        并行执行多个搜索策略并合并结果
        
        Args:
            query: 查询文本
            vector_func: 向量搜索函数
            fts_func: FTS搜索函数
            embedding: 查询向量
            top_k: 返回结果数
        
        Returns:
            (合并结果, 统计信息)
        """
        start_time = time.time()
        results: Dict[str, MergedResult] = {}
        stats = {
            "strategies_used": [],
            "total_latency_ms": 0,
            "results_from_cache": 0,
        }
        
        # 准备搜索任务
        tasks = []
        
        # FTS搜索（总是执行）
        tasks.append(("fts", lambda: fts_func(query, limit=top_k * 2)))
        
        # 向量搜索（如果有embedding）
        if embedding:
            tasks.append(("vector", lambda: vector_func(embedding, top_k=top_k * 2)))
        
        # 并行执行
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(task[1]): task[0] for task in tasks}
            
            for future in as_completed(futures):
                strategy_name = futures[future]
                try:
                    search_results = future.result()
                    stats["strategies_used"].append(strategy_name)
                    
                    # 处理结果
                    for i, r in enumerate(search_results):
                        result_id = r.get("id", f"{strategy_name}_{i}")
                        
                        if result_id in results:
                            # 已存在，合并策略
                            existing = results[result_id]
                            existing.strategies.append(SearchStrategy(strategy_name))
                            existing.score = max(existing.score, r.get("score", 0))
                            if r.get("type") and r["type"] not in existing.types:
                                existing.types.append(r["type"])
                        else:
                            # 新结果
                            results[result_id] = MergedResult(
                                id=result_id,
                                content=r.get("content", r.get("s", "")),
                                score=r.get("score", 0),
                                strategies=[SearchStrategy(strategy_name)],
                                types=[r.get("type", "info")] if r.get("type") else ["info"]
                            )
                except Exception as e:
                    print(f"Strategy {strategy_name} failed: {e}")
        
        # 按分数排序并截取
        sorted_results = sorted(results.values(), key=lambda x: -x.score)[:top_k]
        
        stats["total_latency_ms"] = int((time.time() - start_time) * 1000)
        stats["strategies_count"] = len(stats["strategies_used"])
        stats["results_merged"] = len(results)
        
        return sorted_results, stats
    
    def rerank_by_intent(
        self,
        results: List[MergedResult],
        intent_boost: Dict[str, float],
        top_k: int = 10
    ) -> List[MergedResult]:
        """
        根据意图重排序结果
        
        Args:
            results: 搜索结果
            intent_boost: 类型权重（如 {"error": 1.5, "decision": 1.2}）
            top_k: 返回数
        
        Returns:
            重排序后的结果
        """
        for r in results:
            type_boost = 1.0
            for t in r.types:
                type_boost *= intent_boost.get(t, 1.0)
            
            # 策略多样性奖励
            strategy_boost = 1.0 + 0.05 * len(r.strategies)
            
            r.score = r.score * type_boost * strategy_boost
        
        return sorted(results, key=lambda x: -x.score)[:top_k]


def parallel_search(
    query: str,
    vector_func,
    fts_func,
    embedding: Optional[List[float]] = None,
    top_k: int = 10,
    intent_boost: Optional[Dict[str, float]] = None
) -> Tuple[List[Dict], Dict[str, any]]:
    """
    并行搜索快捷函数
    """
    searcher = ParallelSearcher()
    
    # 执行并行搜索
    merged_results, stats = searcher.search_parallel(
        query, vector_func, fts_func, embedding, top_k
    )
    
    # 根据意图重排序
    if intent_boost:
        merged_results = searcher.rerank_by_intent(merged_results, intent_boost, top_k)
    
    # 转换为字典格式
    output = []
    for r in merged_results:
        output.append({
            "id": r.id,
            "content": r.content,
            "score": r.score,
            "types": r.types,
            "strategies": [s.value for s in r.strategies],
        })
    
    return output, stats
