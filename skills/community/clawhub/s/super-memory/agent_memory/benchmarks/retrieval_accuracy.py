"""v8.5 — 检索准确性基准 (Precision@k, Recall@k, MRR, NDCG)
对标 BEIR 简化版，评估 BM25 + Vector + Keyword 三路融合效果
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _load_test_set():
    path = os.path.join(os.path.dirname(__file__), "test_queries.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "queries": [
            {"query": "Python编程", "relevant_ids": ["d1", "d3"]},
            {"query": "数据库设计", "relevant_ids": ["d2"]},
            {"query": "异步编程", "relevant_ids": ["d1"]},
            {"query": "测试框架", "relevant_ids": ["d3", "d4"]},
            {"query": "机器学习", "relevant_ids": []},
        ]
    }


def precision_at_k(predicted: list[str], relevant: set[str], k: int) -> float:
    if not predicted:
        return 0.0
    hits = sum(1 for p in predicted[:k] if p in relevant)
    return hits / min(k, len(predicted))


def recall_at_k(predicted: list[str], relevant: set[str], k: int) -> float:
    if not relevant:
        return 0.0
    hits = sum(1 for p in predicted[:k] if p in relevant)
    return hits / len(relevant)


def mrr(predicted: list[str], relevant: set[str]) -> float:
    for i, p in enumerate(predicted, 1):
        if p in relevant:
            return 1.0 / i
    return 0.0


def ndcg_at_k(predicted: list[str], relevant: set[str], k: int) -> float:
    ideal = [1.0] * min(len(relevant), k)
    dcg = sum((1.0 / math.log2(i + 2)) for i, p in enumerate(predicted[:k]) if p in relevant)
    idcg = sum((ideal[r] / math.log2(r + 2)) for r in range(len(ideal)))
    return dcg / idcg if idcg > 0 else 0.0


def run_benchmark(search_fn, test_data: dict) -> dict:
    queries = test_data.get("queries", [])
    results = {"k_values": [1, 3, 5, 10], "queries": [], "summary": {}}

    for k in results["k_values"]:
        precision_sum, recall_sum, ndcg_sum = 0.0, 0.0, 0.0
        mrr_sum = 0.0
        count = 0

        for item in queries:
            query = item["query"]
            relevant = set(item.get("relevant_ids", []))
            retrieved = search_fn(query, limit=k)
            pred_ids = [r.get("id", "") for r in retrieved]

            prec = precision_at_k(pred_ids, relevant, k)
            rec = recall_at_k(pred_ids, relevant, k)
            ndcg = ndcg_at_k(pred_ids, relevant, k)
            mr = mrr(pred_ids, relevant)

            precision_sum += prec
            recall_sum += rec
            ndcg_sum += ndcg
            mrr_sum += mr
            count += 1

        if count > 0:
            results["summary"][f"P@{k}"] = round(precision_sum / count, 4)
            results["summary"][f"R@{k}"] = round(recall_sum / count, 4)
            results["summary"][f"NDCG@{k}"] = round(ndcg_sum / count, 4)
        if k == results["k_values"][-1]:
            results["summary"]["MRR"] = round(mrr_sum / count, 4) if count > 0 else 0.0

    return results


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from bm25_index import BM25Index

    bm25 = BM25Index()
    bm25.add("d1", "Python编程语言异步编程与协程", {"topics": ["dev.python"]})
    bm25.add("d2", "数据库设计与 PostgreSQL 优化", {"topics": ["data.sql"]})
    bm25.add("d3", "Python测试框架 pytest 与覆盖率", {"topics": ["dev.python", "dev.testing"]})
    bm25.add("d4", "单元测试与集成测试的最佳实践", {"topics": ["dev.testing"]})

    def search(query, limit=10):
        return bm25.search(query, top_k=limit)

    test_data = _load_test_set()
    metrics = run_benchmark(search, test_data)

    output_path = os.path.join(os.path.dirname(__file__), "results", "retrieval_accuracy.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    print(json.dumps(metrics["summary"], indent=2, ensure_ascii=False))
    print(f"\nResults saved to: {output_path}")