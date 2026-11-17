#!/usr/bin/env python3
"""
性能基准测试脚本
=================
测试 BM25 检索的性能随文档数增长的变化。

运行：
    python scripts/benchmark_retrieval.py --docs 1000

输出：
    打印检索耗时、内存占用和吞吐率
"""
import json
import sys
import time
import random
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

from bm25_retriever import BM25Retriever


def generate_corpus(doc_count: int) -> list:
    """生成合成语料"""
    topics = [
        "RAG检索增强生成是一种结合信息检索和生成模型的技术",
        "由小到大检索是RAG优化的核心策略用小块检索返回大块上下文",
        "重排序使用Cross-Encoder对粗筛结果精排可将准确率从05提升到07",
        "混合检索结合向量语义与BM25关键词匹配适合短查询和长查询",
        "语义分块基于段落和句子边界动态聚合避免切断语义完整性",
    ]
    corpus = []
    for i in range(doc_count):
        topic = topics[i % len(topics)]
        text = f"文档{i+1}：{topic}。这是关于第{i+1}篇文档的详细内容，包含技术细节和背景信息。"
        corpus.append({"id": f"doc_{i}", "text": text})
    return corpus


def main():
    doc_counts = [100, 500, 1000, 5000, 10000]
    if "--docs" in sys.argv:
        idx = sys.argv.index("--docs")
        doc_counts = [int(sys.argv[idx + 1])]

    results = []
    for n in doc_counts:
        print(f"\n{'='*50}")
        print(f"文档数: {n}")
        print(f"{'='*50}")

        corpus = generate_corpus(n)

        retriever = BM25Retriever()

        # 索引性能
        t0 = time.perf_counter()
        retriever.index_documents(corpus)
        index_time = time.perf_counter() - t0

        # 检索性能（平均10次）
        queries = ["RAG优化的核心策略", "重排序是什么", "如何提升召回率",
                   "语义分块的方法", "检索增强生成的定义"]
        total_retrieve = 0.0
        for q in queries:
            t0 = time.perf_counter()
            retriever.retrieve(q, top_k=5, strategy="bm25")
            total_retrieve += time.perf_counter() - t0

        avg_retrieve = total_retrieve / len(queries)
        throughput = 1.0 / avg_retrieve if avg_retrieve > 0 else 0

        print(f"  索引耗时:     {index_time:.3f}s")
        print(f"  单次检索耗时: {avg_retrieve*1000:.2f}ms")
        print(f"  吞吐率:       {throughput:.0f} queries/s")

        results.append({
            "doc_count": n,
            "index_time_sec": round(index_time, 3),
            "avg_retrieve_ms": round(avg_retrieve * 1000, 2),
            "throughput_qps": round(throughput, 0)
        })

    # 保存报告
    print(f"\n\n{'='*50}")
    print("汇总报告：")
    for r in results:
        print(f"  文档 {r['doc_count']:>6d}: 索引={r['index_time_sec']}s, "
              f"检索={r['avg_retrieve_ms']}ms, 吞吐={r['throughput_qps']}qps")


if __name__ == "__main__":
    main()
