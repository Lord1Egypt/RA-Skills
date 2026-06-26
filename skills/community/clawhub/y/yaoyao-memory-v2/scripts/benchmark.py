#!/usr/bin/env python3
"""性能基准测试工具
功能：
1. 搜索性能基准
2. 内存占用测试
3. 缓存效率测试
4. 批量操作测试
"""
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def benchmark_search(memory, queries, iterations=10):
    """搜索基准测试"""
    results = []
    
    for q in queries:
        times = []
        for _ in range(iterations):
            start = time.time()
            memory.search(q, limit=3)
            times.append((time.time() - start) * 1000)
        
        avg = sum(times) / len(times)
        min_t = min(times)
        max_t = max(times)
        results.append({
            "query": q,
            "avg_ms": round(avg, 2),
            "min_ms": round(min_t, 2),
            "max_ms": round(max_t, 2)
        })
    
    return results

def benchmark_memory():
    """内存占用测试"""
    import tracemalloc
    from memory import Memory
    
    tracemalloc.start()
    
    m = Memory()
    current, peak = tracemalloc.get_traced_memory()
    
    tracemalloc.stop()
    
    return {
        "current_kb": round(current / 1024, 1),
        "peak_kb": round(peak / 1024, 1)
    }

def benchmark_batch(memory, queries):
    """批量操作测试"""
    from batch_search import BatchSearchOptimizer
    
    optimizer = BatchSearchOptimizer(memory)
    
    start = time.time()
    results = optimizer.batch_search(queries, limit=3)
    elapsed = (time.time() - start) * 1000
    
    return {
        "queries": len(queries),
        "total_ms": round(elapsed, 2),
        "avg_ms": round(elapsed / len(queries), 2)
    }

def benchmark_cache(memory):
    """缓存效率测试"""
    from predictive_cache import PredictiveCache
    
    cache = PredictiveCache()
    
    # 模拟访问
    keys = ["记忆", "配置", "系统", "用户", "决策"]
    for key in keys * 3:
        cache.set(key, f"value_{key}")
    
    # 测试缓存命中
    hits = 0
    for key in keys:
        if cache.get(key):
            hits += 1
    
    return {
        "total_keys": len(keys),
        "cache_hits": hits,
        "hit_rate": f"{hits/len(keys)*100:.0f}%"
    }

def run_all_benchmarks():
    """运行所有基准测试"""
    from memory import Memory
    
    print("=== yaoyao-memory 性能基准测试 ===\n")
    
    m = Memory()
    
    # 1. 搜索性能
    print("【搜索性能测试】")
    queries = ["记忆", "配置", "系统", "用户", "决策", "性能"]
    results = benchmark_search(m, queries)
    for r in results:
        print(f"  {r['query']}: avg={r['avg_ms']}ms min={r['min_ms']}ms max={r['max_ms']}ms")
    
    # 2. 内存占用
    print("\n【内存占用测试】")
    mem = benchmark_memory()
    print(f"  当前: {mem['current_kb']} KB")
    print(f"  峰值: {mem['peak_kb']} KB")
    
    # 3. 批量操作
    print("\n【批量操作测试】")
    batch = benchmark_batch(m, queries)
    print(f"  {batch['queries']} 查询: {batch['total_ms']}ms (平均 {batch['avg_ms']}ms/查询)")
    
    # 4. 缓存效率
    print("\n【缓存效率测试】")
    cache = benchmark_cache(m)
    print(f"  命中率: {cache['hit_rate']} ({cache['cache_hits']}/{cache['total_keys']})")
    
    print("\n=== 基准测试完成 ===")

if __name__ == "__main__":
    run_all_benchmarks()
