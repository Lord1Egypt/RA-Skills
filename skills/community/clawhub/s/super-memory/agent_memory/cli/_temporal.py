"""Time travel: snapshot, snapshots, diff, blame, timeline-stats."""

from __future__ import annotations

import json
from argparse import Namespace
from datetime import datetime

from agent_memory.cli._utils import get_memory


def cmd_snapshot(args):
    """创建记忆快照"""
    mem = get_memory()
    at_ts = None
    if args.at:
        from timeline import parse_date_to_ts
        try:
            at_ts = parse_date_to_ts(args.at)
        except ValueError as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
            mem.close()
            return
    result = mem.take_snapshot(
        label=args.label,
        at_ts=at_ts,
        description=args.description,
    )
    label = args.label or result.get("snapshot_id", "")
    print(f"📸 快照已创建: {label}")
    mem.close()


def cmd_snapshots(args):
    """列出所有快照"""
    mem = get_memory()
    snapshots = mem.list_snapshots(limit=args.limit)
    if not snapshots:
        print("📭 还没有快照 — 使用 snapshot 创建你的第一个快照，保存此刻的认知状态")
    else:
        output = []
        for s in snapshots:
            output.append({
                "id": s["snapshot_id"],
                "label": s["label"],
                "at": datetime.fromtimestamp(s["at_ts"]).strftime("%Y-%m-%d %H:%M"),
                "memories": s["memory_count"],
                "high": s["high_count"],
            })
        print(json.dumps(output, ensure_ascii=False, indent=2))
    mem.close()


def cmd_diff(args):
    """对比两个时间点的记忆差异"""
    mem = get_memory()
    from timeline import parse_date_to_ts

    from_ts = None
    to_ts = None

    # 解析时间
    if not args.from_snapshot:
        try:
            from_ts = parse_date_to_ts(args.from_date)
        except ValueError as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
            mem.close()
            return

    if not args.to_snapshot and args.to_date:
        try:
            to_ts = parse_date_to_ts(args.to_date)
        except ValueError as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
            mem.close()
            return

    if args.natural:
        output = mem.diff_natural(
            from_ts=from_ts, to_ts=to_ts,
            from_snapshot=args.from_snapshot, to_snapshot=args.to_snapshot,
        )
        print(output)
    else:
        result = mem.diff_memories(
            from_ts=from_ts, to_ts=to_ts,
            from_snapshot=args.from_snapshot, to_snapshot=args.to_snapshot,
            topic=args.topic,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    mem.close()


def cmd_blame(args):
    """追溯记忆来源"""
    mem = get_memory()
    if args.natural:
        output = mem.blame_natural(args.memory_id)
        print(output)
    else:
        result = mem.blame_memory(args.memory_id)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    mem.close()


def cmd_timeline_stats(args):
    """时间旅行系统统计"""
    mem = get_memory()
    stats = mem.get_timeline_stats()
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    mem.close()
