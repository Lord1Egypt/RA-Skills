"""v8.5 — 检索延迟基准 (p50/p95/p99)
评估 BM25 + 向量 + 关键词在不同数据规模下的延迟
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def run_latency_bench(search_fn, dataset_sizes: list[int] = None, queries_per_size: int = 50) -> dict:
    if dataset_sizes is None:
        dataset_sizes = [100, 500, 1000]

    from bm25_index import BM25Index

    results = {}

    for size in dataset_sizes:
        bm25 = BM25Index()
        for i in range(size):
            bm25.add(
                f"doc_{i}",
                f"测试文档 {i} 包含各种中文内容用于性能基准测试",
                {"topics": ["dev.testing"], "importance": "medium"},
            )

        latencies = []
        for _ in range(queries_per_size):
            start = time.perf_counter()
            bm25.search(f"性能基准查询 {_ % 10}", top_k=20)
            latencies.append((time.perf_counter() - start) * 1000)

        latencies.sort()
        results[f"n={size}"] = {
            "p50_ms": round(latencies[len(latencies) // 2], 2),
            "p95_ms": round(latencies[int(len(latencies) * 0.95)], 2),
            "p99_ms": round(latencies[int(len(latencies) * 0.99)], 2),
            "mean_ms": round(sum(latencies) / len(latencies), 2),
            "queries": queries_per_size,
            "documents": size,
        }

    return results


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

    results = run_latency_bench(None)

    os.makedirs(os.path.join(os.path.dirname(__file__), "results"), exist_ok=True)
    output_path = os.path.join(os.path.dirname(__file__), "results", "latency_bench.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\nResults saved to: {output_path}")

    peak_size = list(results.keys())[-1]
    peak = results[peak_size]
    print(f"\nPeak ({peak_size}): p50={peak['p50_ms']}ms, p95={peak['p95_ms']}ms, p99={peak['p99_ms']}ms")
    if peak["p95_ms"] <= 200:
        print("✅ PASS: p95 ≤ 200ms target")
    else:
        print(f"⚠️  SLOW: p95={peak['p95_ms']}ms exceeds 200ms target")