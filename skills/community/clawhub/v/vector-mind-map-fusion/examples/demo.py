#!/usr/bin/env python3
"""
Vector-Mind Map-Fusion 快速演示

演示 L1→L2→L3 完整链路的基本功能。
"""

import sys
import os

# 添加项目根目录到 path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.l1.l1_cron import main as l1_main
from src.l2.l2_cron import main as l2_main
from src.l3.l3_cron import main as l3_main
from src.recall.recall import VectorMindRecall


def demo_l1_extract():
    """演示 L1 提取"""
    print("\n" + "=" * 50)
    print("演示 L1 提取层")
    print("=" * 50)

    print("""
    L1 负责从 OpenClaw session 中提取用户内容：

    1. ByteOffsetScanner: 扫描 session JSONL，断点续扫
    2. Stage1 过滤: 噪音/UUID/cron/metadata
    3. Classifier: 去噪→质量检查→分类→分块→向量
    4. 输出到 L2A 目录

    触发条件: "记住 XXX"、"存入记忆"
    """)

    # 实际运行 L1（注释掉以避免在 demo 中触发）
    # l1_main()

    print("[完成] L1 演示")


def demo_l2_consolidate():
    """演示 L2 整理"""
    print("\n" + "=" * 50)
    print("演示 L2 整理层")
    print("=" * 50)

    print("""
    L2 负责整理 L1 的输出：

    1. 加载 L2A: 扫描所有日期文件
    2. session 分组 + 滑动窗口
    3. 四级去重: content_hash → cosine → simhash → hnsw
    4. session graph: N-gram 中文分词
    5. transitive closure: 关系补全
    6. 输出到 L2 目录

    触发条件: "整理一下"、"归类"
    """)

    print("[完成] L2 演示")


def demo_l3_retrieve():
    """演示 L3 检索"""
    print("\n" + "=" * 50)
    print("演示 L3 检索层")
    print("=" * 50)

    print("""
    L3 负责检索记忆：

    1. 加载 L2: Brain.db 写入
    2. SCHEMA 生成: session≥5 → TF-IDF 摘要
    3. InfinityDB 同步: brain.graph + brain.vec + hnsw

    召回方式：
    - Vector Search: 暴力向量搜索
    - Adjacency BFS: 图遍历
    - Combined Recall: HNSW + BFS 组合召回

    触发条件: "搜索记忆"、"之前有没有"
    """)

    print("[完成] L3 演示")


def demo_recall():
    """演示召回功能"""
    print("\n" + "=" * 50)
    print("演示召回功能")
    print("=" * 50)

    print("""
    from recall.recall import VectorMindRecall

    recall = VectorMindRecall()

    # 语义搜索
    results = recall.search("查询内容", top_k=10)

    # 按 session 搜索
    bfs = recall.search_by_session("session_id", max_hops=3)

    # 精确 ID 查找
    neuron = recall.get_neuron("chunk_id")
    """)

    print("[完成] 召回演示")


def main():
    print("=" * 50)
    print("Vector-Mind Map-Fusion 快速演示")
    print("=" * 50)

    demos = [
        ("L1 提取", demo_l1_extract),
        ("L2 整理", demo_l2_consolidate),
        ("L3 检索", demo_l3_retrieve),
        ("召回功能", demo_recall),
    ]

    for name, func in demos:
        func()

    print("\n" + "=" * 50)
    print("演示完成")
    print("=" * 50)
    print("""
    快速开始：

    1. 运行全部层:
       python main.py run --all

    2. 搜索记忆:
       python main.py search "查询内容"

    3. 查看状态:
       python main.py stats

    4. 查看帮助:
       python main.py --help
    """)


if __name__ == "__main__":
    main()