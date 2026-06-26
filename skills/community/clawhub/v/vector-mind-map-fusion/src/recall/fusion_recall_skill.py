#!/usr/bin/env python3
"""
Fusion Recall Skill
供 OpenClaw agent 在对话中调用 fusion_recall。

用法示例：
  results = fusion_recall("dxiaofeng 的项目", top_k=10, tier="warm")
  for r in results:
      print(r["content"], r["activation_score"])
"""

import sys
import json
from pathlib import Path

# 确保 fusion 模块可导入
sys.path.insert(0, str(Path(__file__).parent))

from recall import fusion_recall as _fusion_recall


def fusion_recall(
    query: str,
    top_k: int = 10,
    tier: str = None,
    memory_type: str = None,
    min_score: float = 0.3,
) -> list[dict]:
    """
    Fusion 记忆召回。

    参数：
        query: 搜索查询文本
        top_k: 返回结果数量（默认 10）
        tier: 过滤 tier（cold/warm/hot），可选
        memory_type: 过滤 memory_type（context/reference/decision 等），可选
        min_score: 最低激活分数（默认 0.3）

    返回：
        list[dict]，每条包含 id, content, memory_type, priority, tier,
        abstraction_level, activation_score
    """
    return _fusion_recall(
        query=query,
        top_k=top_k,
        tier=tier,
        memory_type=memory_type,
        min_score=min_score,
    )


if __name__ == "__main__":
    # CLI 测试
    import argparse
    parser = argparse.ArgumentParser(description="Fusion Recall CLI")
    parser.add_argument("query", help="搜索查询")
    parser.add_argument("--top-k", type=int, default=10, help="返回数量")
    parser.add_argument("--tier", help="tier 过滤 (cold/warm/hot)")
    parser.add_argument("--type", dest="memory_type", help="memory_type 过滤")
    parser.add_argument("--min-score", type=float, default=0.3, help="最低分数")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    results = fusion_recall(
        query=args.query,
        top_k=args.top_k,
        tier=args.tier,
        memory_type=args.memory_type,
        min_score=args.min_score,
    )

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"\n返回 {len(results)} 条结果：\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. [{r['activation_score']:.4f}] {r['memory_type']} | tier={r['tier']} | priority={r['priority']}")
            print(f"   {r['content'][:100]}...")
            print()