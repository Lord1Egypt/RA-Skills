#!/usr/bin/env python3
"""
Vector-Mind Map-Fusion 项目入口
L1 提取 → L2 整理 → L3 检索

Usage:
    python main.py run --all          # 运行全部层
    python main.py run --layer l1    # 只运行 L1
    python main.py run --layer l2    # 只运行 L2
    python main.py run --layer l3    # 只运行 L3
    python main.py search "内容"      # 搜索记忆
    python main.py stats             # 查看状态
"""

import sys
import os
import argparse
from datetime import datetime

# 添加项目根目录到 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def check_ollama():
    """检查 Ollama 是否可用"""
    import httpx
    try:
        resp = httpx.get("http://localhost:11434/api/tags", timeout=5)
        if resp.status_code != 200:
            raise RuntimeError(f"Ollama 返回状态码 {resp.status_code}")
        models = resp.json().get("models", [])
        model_names = [m.get("name", "") for m in models]
        if "bge-m3" not in " ".join(model_names):
            print("[警告] 未检测到 bge-m3 模型，请运行: ollama pull bge-m3")
            print(f"[警告] 当前已安装模型: {model_names}")
    except Exception as e:
        print(f"[错误] Ollama 不可用: {e}")
        print("[错误] 请确保已启动 ollama serve")
        raise SystemExit(1)


def run_l1():
    """运行 L1 提取层"""
    check_ollama()
    from src.l1.l1_cron import main as l1_main
    print(f"[Main] 运行 L1 提取层: {datetime.now().isoformat()}")
    l1_main()
    print("[Main] L1 完成")


def run_l2():
    """运行 L2 整理层"""
    from src.l2.l2_cron import main as l2_main
    print(f"[Main] 运行 L2 整理层: {datetime.now().isoformat()}")
    l2_main()
    print("[Main] L2 完成")


def run_l3():
    """运行 L3 检索层"""
    from src.l3.l3_cron import main as l3_main
    print(f"[Main] 运行 L3 检索层: {datetime.now().isoformat()}")
    l3_main()
    print("[Main] L3 完成")


def run_all():
    """运行全部层"""
    print(f"[Main] 运行全部层: {datetime.now().isoformat()}")
    run_l1()
    run_l2()
    run_l3()
    print(f"[Main] 全部完成: {datetime.now().isoformat()}")


def search(query: str, top_k: int = 10):
    """搜索记忆"""
    from src.recall.recall import VectorMindRecall

    print(f"[Main] 搜索记忆: {query}")
    recall = VectorMindRecall()
    results = recall.search(query, top_k=top_k)

    print(f"\n找到 {len(results)} 条结果:")
    for i, r in enumerate(results, 1):
        print(f"  [{i}] {r.get('content', '')[:60]}...")
        print(f"      score={r.get('score', 0):.4f} type={r.get('memory_type', 'unknown')}")

    return results


def stats():
    """查看系统状态"""
    import sqlite3
    from pathlib import Path

    print("[Main] 系统状态")
    print("=" * 50)

    # L2A 数据
    l2a_dir = Path(__file__).parent / "memory" / "layers" / "l2a"
    l2a_count = len(list(l2a_dir.glob("*.jsonl"))) if l2a_dir.exists() else 0

    # L2 数据
    l2_dir = Path(__file__).parent / "memory" / "layers" / "l2"
    l2_count = len(list(l2_dir.glob("*.jsonl"))) if l2_dir.exists() else 0

    # InfinityDB 数据
    infinity_dir = Path(__file__).parent / "memory" / "layers" / "infinitydb"
    graph_file = infinity_dir / "brain.graph.json" if infinity_dir.exists() else None
    infinity_nodes = 0
    if graph_file and graph_file.exists():
        import json
        with open(graph_file) as f:
            data = json.load(f)
            infinity_nodes = len(data)

    # Brain.db 数据
    brain_db = Path.home() / ".local" / "share" / "neural-memory" / "brains.db"
    brain_neurons = 0
    if brain_db.exists():
        conn = sqlite3.connect(str(brain_db))
        cursor = conn.execute("SELECT COUNT(*) FROM neurons WHERE brain_id='default'")
        brain_neurons = cursor.fetchone()[0]
        conn.close()

    print(f"  L2A 文件数: {l2a_count}")
    print(f"  L2 文件数: {l2_count}")
    print(f"  InfinityDB nodes: {infinity_nodes}")
    print(f"  Brain.db neurons: {brain_neurons}")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="Vector-Mind Map-Fusion")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # run 命令
    run_parser = subparsers.add_parser("run", help="运行指定层")
    run_parser.add_argument("--layer", choices=["l1", "l2", "l3", "all"], default="all",
                           help="运行哪一层 (默认: all)")
    run_parser.add_argument("--date", default=None, help="指定日期 (YYYY-MM-DD)")

    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索记忆")
    search_parser.add_argument("query", help="搜索内容")
    search_parser.add_argument("--top-k", type=int, default=10, help="返回数量")

    # stats 命令
    subparsers.add_parser("stats", help="查看状态")

    args = parser.parse_args()

    if args.command == "run":
        if args.layer == "l1":
            run_l1()
        elif args.layer == "l2":
            run_l2()
        elif args.layer == "l3":
            run_l3()
        else:
            run_all()
    elif args.command == "search":
        search(args.query, args.top_k)
    elif args.command == "stats":
        stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()