#!/usr/bin/env python3
"""yaoyao-memory CLI - 命令行工具
用法：
  python3 cli.py search <query>
  python3 cli.py stats
  python3 cli.py health
  python3 cli.py benchmark
  python3 cli.py optimize
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def cmd_search(query: str, limit: int = 3):
    """搜索记忆"""
    from memory import Memory
    m = Memory()
    result = m.search(query, limit=limit)
    print(f"查询: {query}")
    print(f"方法: {result['method']}")
    print(f"结果数: {result['total']}")
    for r in result.get('results', []):
        print(f"  - {r.get('s', 'N/A')}")

def cmd_stats():
    """显示统计"""
    from memory import Memory
    m = Memory()
    stats = m.stats()
    print(f"记忆总数: {stats['total']}")
    print(f"按类型:")
    for t, c in stats['by_type'].items():
        print(f"  {t}: {c}")

def cmd_health():
    """健康检查"""
    from health_check import run_health_check
    result = run_health_check()
    print(f"健康度: {result.get('health_score', 'N/A')}")
    print(f"模块完整: {result.get('module_integrity', 'N/A')}")

def cmd_benchmark():
    """运行基准测试"""
    from benchmark import run_all_benchmarks
    run_all_benchmarks()

def cmd_optimize():
    """执行优化"""
    from self_improver import SelfImprover
    improver = SelfImprover()
    suggestions = improver.get_optimization_suggestions()
    print(f"发现 {len(suggestions)} 条优化建议")
    for s in suggestions:
        print(f"  [{s['priority']}] {s['description']}")

def main():
    parser = argparse.ArgumentParser(description="yaoyao-memory CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    # search
    p_search = subparsers.add_parser("search", help="搜索记忆")
    p_search.add_argument("query", help="搜索词")
    p_search.add_argument("-n", "--limit", type=int, default=3, help="结果数量")
    
    # stats
    subparsers.add_parser("stats", help="显示统计")
    
    # health
    subparsers.add_parser("health", help="健康检查")
    
    # benchmark
    subparsers.add_parser("benchmark", help="运行基准测试")
    
    # optimize
    subparsers.add_parser("optimize", help="执行优化")
    
    args = parser.parse_args()
    
    if args.command == "search":
        cmd_search(args.query, args.limit)
    elif args.command == "stats":
        cmd_stats()
    elif args.command == "health":
        cmd_health()
    elif args.command == "benchmark":
        cmd_benchmark()
    elif args.command == "optimize":
        cmd_optimize()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
