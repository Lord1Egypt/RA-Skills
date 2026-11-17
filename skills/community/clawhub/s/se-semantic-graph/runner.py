#!/usr/bin/env python3
"""se-semantic-graph runner — 软件工程语义图谱 CLI。

把软件工程全知识域（客户画像/需求/成本/架构/分层/模块/运行逻辑/历史决策）
落进 axolotl 图库，支持：
- init: 初始化项目图
- add: 录入语义节点（字段级摘要）
- connect: 加跨域语义边（正反成对，双向可遍历）
- trace: 定向遍历查询（修 bug/加功能/重构时取精确上下文）
- list: 列出节点
- stats: 统计

用法示例见 SKILL.md。所有路径可经环境变量覆盖：
  SE_SEMANTIC_ENGINE  引擎目录（默认 ~/.workbuddy/skills/lobster-memory）
  SE_SEMANTIC_DIR     图文件目录（默认 ~/.workbuddy/se-semantic-graph）
"""
import argparse
import json
import os
import sys

_SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
if _SKILL_DIR not in sys.path:
    sys.path.insert(0, _SKILL_DIR)

from graph_api import SEManticGraph, DEFAULT_GRAPH_FILE  # noqa: E402
from schema import NODE_TYPES, EDGE_KINDS  # noqa: E402

GRAPH_DIR = os.environ.get(
    "SE_SEMANTIC_DIR", os.path.expanduser("~/.workbuddy/se-semantic-graph")
)


def _graph():
    os.makedirs(GRAPH_DIR, exist_ok=True)
    return SEManticGraph(os.path.join(GRAPH_DIR, DEFAULT_GRAPH_FILE))


def cmd_init(args):
    g = _graph()
    try:
        st = g.stats()
        g.close()
    except Exception as e:
        sys.stderr.write(f"[se-semantic-graph] init 失败: {e}\n")
        sys.exit(1)
    print(f"已初始化项目语义图谱: {GRAPH_DIR}")
    print(f"  当前: {st['vertices']} 节点 | {st['edges']} 边")


def cmd_add(args):
    g = _graph()
    try:
        r = g.upsert_node(
            id_str=args.id,
            label=args.label,
            node_type=args.type,
            summary=args.summary or "",
            detail_ref=args.detail_ref or "",
            source=args.source or "",
        )
        g.close()
    except Exception as e:
        sys.stderr.write(f"[se-semantic-graph] add 失败（未落盘）: {e}\n")
        sys.exit(1)
    print(f"节点已写入: {r['id']} ({r['type']}) {r['label']}")


def cmd_connect(args):
    g = _graph()
    try:
        r = g.connect(args.from_id, args.to_id, args.kind, note=args.note or "")
        g.close()
    except Exception as e:
        sys.stderr.write(f"[se-semantic-graph] connect 失败（未落盘）: {e}\n")
        sys.exit(1)
    print(f"边已建立: {r['from']} --{r['kind']}--> {r['to']} [{r['status']}]")


def cmd_trace(args):
    g = _graph()
    try:
        r = g.trace(
            start_id=args.start,
            direction=args.direction,
            max_depth=args.depth,
            max_results=args.limit,
            kind_filter=args.kind,
            node_type_filter=args.type,
        )
        g.close()
    except Exception as e:
        sys.stderr.write(f"[se-semantic-graph] trace 失败: {e}\n")
        sys.exit(1)

    if "error" in r:
        print(r["error"])
        sys.exit(1)

    print(f"[追踪] 起点: {r['start']} | 方向: {r['direction']} | 命中 {r['total_nodes']} 节点")
    for n in r["nodes"]:
        depth = n.get("depth", 0)
        indent = "  " * depth
        summ = n.get("summary", "")
        summ = summ[:60] + ("…" if len(summ) > 60 else "")
        print(f"{indent}- [{n.get('type')}] {n.get('label')}"
              + (f" | {summ}" if summ else ""))
    if r["paths"] and args.verbose:
        print("\n[路径]")
        for (d, frm, to, kind) in r["paths"]:
            print(f"  {'  ' * d}{frm} --{kind}--> {to}")


def cmd_list(args):
    g = _graph()
    try:
        nodes = g.list_nodes(node_type=args.type, limit=args.limit)
        g.close()
    except Exception as e:
        sys.stderr.write(f"[se-semantic-graph] list 失败: {e}\n")
        sys.exit(1)
    print(f"[节点清单] {len(nodes)} 条")
    for n in nodes:
        summ = (n.get("summary") or "")[:50]
        print(f"- [{n.get('type')}] {n.get('id')} | {n.get('label')}"
              + (f" | {summ}" if summ else ""))


def cmd_stats(args):
    g = _graph()
    try:
        st = g.stats()
        g.close()
    except Exception as e:
        sys.stderr.write(f"[se-semantic-graph] stats 失败: {e}\n")
        sys.exit(1)
    print(f"[图谱统计] 节点 {st['vertices']} | 边 {st['edges']} | 文件 {st['path']}")
    if st["by_type"]:
        print("[按类型]")
        for t, c in sorted(st["by_type"].items(), key=lambda x: -x[1]):
            print(f"  {NODE_TYPES.get(t, t)} ({t}): {c}")


def cmd_types(args):
    print("[节点类型]")
    for t, zh in NODE_TYPES.items():
        print(f"  {t} = {zh}")
    print("\n[边类型]")
    for k, zh in EDGE_KINDS.items():
        print(f"  {k} = {zh}")


def main():
    p = argparse.ArgumentParser(description="软件工程语义图谱 CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("init", help="初始化项目图")
    sp.set_defaults(fn=cmd_init)

    sp = sub.add_parser("add", help="录入语义节点")
    sp.add_argument("--id", required=True, help="稳定标识符（英文/拼音，无空格）")
    sp.add_argument("--label", required=True, help="可读名称")
    sp.add_argument("--type", required=True, choices=NODE_TYPES.keys(), help="节点类型")
    sp.add_argument("--summary", default="", help="一句话摘要（≤200字）")
    sp.add_argument("--detail-ref", default="", help="详细文档/源码位置引用")
    sp.add_argument("--source", default="", help="来源（需求文档/issue/PR/会议）")
    sp.set_defaults(fn=cmd_add)

    sp = sub.add_parser("connect", help="加跨域语义边")
    sp.add_argument("--from", dest="from_id", required=True)
    sp.add_argument("--to", dest="to_id", required=True)
    sp.add_argument("--kind", required=True, choices=EDGE_KINDS.keys())
    sp.add_argument("--note", default="")
    sp.set_defaults(fn=cmd_connect)

    sp = sub.add_parser("trace", help="定向遍历查询（核心）")
    sp.add_argument("--start", required=True, help="起点节点 id")
    sp.add_argument("--direction", default="up", choices=["up", "down", "both"],
                    help="up=反向追溯(为什么做) down=正向展开(影响什么) both=双向")
    sp.add_argument("--depth", type=int, default=4)
    sp.add_argument("--limit", type=int, default=50)
    sp.add_argument("--kind", default=None, help="只走指定边类型")
    sp.add_argument("--type", dest="type", default=None, help="只保留指定节点类型")
    sp.add_argument("--verbose", action="store_true", help="显示完整路径")
    sp.set_defaults(fn=cmd_trace)

    sp = sub.add_parser("list", help="列出节点")
    sp.add_argument("--type", default=None, choices=list(NODE_TYPES) + [None])
    sp.add_argument("--limit", type=int, default=500)
    sp.set_defaults(fn=cmd_list)

    sp = sub.add_parser("stats", help="图谱统计")
    sp.set_defaults(fn=cmd_stats)

    sp = sub.add_parser("types", help="列出节点/边类型")
    sp.set_defaults(fn=cmd_types)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
