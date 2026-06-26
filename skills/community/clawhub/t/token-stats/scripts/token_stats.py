#!/usr/bin/env python3
"""
OpenClaw Token Statistics — scan all session JSONL files and report usage.

Usage:
    python token_stats.py [OPTIONS]

Options:
    --agent AGENT_ID    Agent to scan (default: main)
    --include-deleted   Include .deleted and .bak files
    --daily             Show per-day breakdown
    --sessions          Show per-session breakdown
    --top N             Show top N sessions by token usage (default: 10)
    --format FORMAT     Output format: text (default) or json
    --since DATE        Only include data from this date (YYYY-MM-DD)
    --until DATE        Only include data until this date (YYYY-MM-DD)
"""

import json
import glob
import os
import sys
import argparse
from datetime import datetime
from collections import defaultdict


def parse_args():
    p = argparse.ArgumentParser(description="OpenClaw Token Statistics")
    p.add_argument("--agent", default="main", help="Agent ID (default: main)")
    p.add_argument("--include-deleted", action="store_true", help="Include .deleted and .bak files")
    p.add_argument("--daily", action="store_true", help="Show per-day breakdown")
    p.add_argument("--sessions", action="store_true", help="Show per-session breakdown")
    p.add_argument("--top", type=int, default=10, help="Top N sessions (default: 10)")
    p.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    p.add_argument("--since", default=None, help="Start date (YYYY-MM-DD)")
    p.add_argument("--until", default=None, help="End date (YYYY-MM-DD)")
    return p.parse_args()


def find_session_files(agent_id, include_deleted):
    base = os.path.expanduser("~/.openclaw/agents/%s/sessions/" % agent_id)
    patterns = [base + "*.jsonl"]
    if include_deleted:
        patterns.append(base + "*.jsonl.deleted*")
        patterns.append(base + "*.jsonl.bak*")
    files = []
    for pat in patterns:
        files.extend(glob.glob(pat))
    return sorted(set(files), key=os.path.getmtime, reverse=True)


def load_labels(agent_id):
    """Load session labels from sessions.json."""
    sj_path = os.path.expanduser(
        "~/.openclaw/agents/%s/sessions/sessions.json" % agent_id
    )
    labels = {}
    if os.path.exists(sj_path):
        try:
            with open(sj_path) as f:
                sj = json.load(f)
            for key, val in sj.items():
                sid = val.get("sessionId", "")
                lbl = val.get("label", key)
                labels[sid] = lbl
        except Exception:
            pass
    return labels


def scan_file(fpath, date_filter_start=None, date_filter_end=None):
    """
    Scan a single JSONL file and return stats.

    Token calculation methodology:
    - usage is at entry["message"]["usage"], only on assistant messages
    - Fields: input, output, cacheRead, cacheWrite, totalTokens, cost
    - "input" = API's prompt_tokens - cacheRead - cacheWrite
      This can be NEGATIVE when provider reports prompt_tokens as uncached-only
      (double subtraction bug via New-API proxy)
    - Correct prompt calculation: cacheRead + max(input, 0)
      This recovers the real prompt token count
    - totalTokens field is unreliable (arithmetic sum including negative input)
    - output includes thinking tokens (no separate breakdown)
    - cacheWrite is always 0 through New-API proxy (not passed through)
    - cost is always 0 through New-API proxy (calculated on proxy side)
    """
    stats = {
        "calls": 0,
        "errors": 0,
        "compactions": 0,
        "prompt": 0,        # cacheRead + max(input, 0)
        "cache_read": 0,
        "new_input": 0,     # max(input, 0)
        "output": 0,
        "first_ts": None,
        "last_ts": None,
        "daily": defaultdict(lambda: {
            "calls": 0, "prompt": 0, "cache_read": 0, "new_input": 0, "output": 0
        }),
    }

    try:
        with open(fpath) as f:
            for line in f:
                try:
                    e = json.loads(line)
                except Exception:
                    continue

                if e.get("type") == "compaction":
                    stats["compactions"] += 1
                    continue

                if e.get("type") != "message":
                    continue

                msg = e.get("message", {})
                if msg.get("role") != "assistant" or "usage" not in msg:
                    continue

                # Date filtering
                ts = e.get("timestamp", "")
                day = ts[:10] if ts else None

                if date_filter_start and day and day < date_filter_start:
                    continue
                if date_filter_end and day and day > date_filter_end:
                    continue

                # Track time range
                if ts:
                    if stats["first_ts"] is None:
                        stats["first_ts"] = ts
                    stats["last_ts"] = ts

                # Skip errors
                if msg.get("stopReason") == "error":
                    stats["errors"] += 1
                    continue

                u = msg["usage"]
                inp = u.get("input", 0)
                output = u.get("output", 0)
                cache_read = u.get("cacheRead", 0)

                # Core formula: real prompt = cacheRead + max(input, 0)
                fresh_input = max(inp, 0)
                prompt = cache_read + fresh_input

                stats["calls"] += 1
                stats["prompt"] += prompt
                stats["cache_read"] += cache_read
                stats["new_input"] += fresh_input
                stats["output"] += output

                if day:
                    d = stats["daily"][day]
                    d["calls"] += 1
                    d["prompt"] += prompt
                    d["cache_read"] += cache_read
                    d["new_input"] += fresh_input
                    d["output"] += output

    except Exception as ex:
        sys.stderr.write("Error reading %s: %s\n" % (fpath, ex))

    return stats


def format_number(n):
    return "{:,}".format(n)


def format_yi(n):
    """Format large numbers in 亿 (hundred millions)."""
    if n >= 100_000_000:
        return "%.2f 亿" % (n / 100_000_000)
    elif n >= 10_000:
        return "%.1f 万" % (n / 10_000)
    else:
        return format_number(n)


def main():
    args = parse_args()
    files = find_session_files(args.agent, args.include_deleted)
    labels = load_labels(args.agent)

    if not files:
        print("No session files found for agent: %s" % args.agent)
        sys.exit(1)

    # Scan all files
    session_stats = []
    grand = {
        "calls": 0, "errors": 0, "compactions": 0,
        "prompt": 0, "cache_read": 0, "new_input": 0, "output": 0,
    }
    grand_daily = defaultdict(lambda: {
        "calls": 0, "prompt": 0, "cache_read": 0, "new_input": 0, "output": 0
    })

    for fpath in files:
        sid = os.path.basename(fpath).split(".")[0]
        label = labels.get(sid, sid[:16])
        st = scan_file(fpath, args.since, args.until)

        if st["calls"] == 0 and st["errors"] == 0:
            continue

        st["label"] = label
        st["sid"] = sid
        session_stats.append(st)

        for key in ("calls", "errors", "compactions", "prompt", "cache_read", "new_input", "output"):
            grand[key] += st[key]

        for day, d in st["daily"].items():
            for key in ("calls", "prompt", "cache_read", "new_input", "output"):
                grand_daily[day][key] += d[key]

    # Determine time range
    all_ts = [s["first_ts"] for s in session_stats if s["first_ts"]]
    earliest = min(all_ts)[:10] if all_ts else "?"
    all_ts_last = [s["last_ts"] for s in session_stats if s["last_ts"]]
    latest = max(all_ts_last)[:10] if all_ts_last else "?"

    # JSON output
    if args.format == "json":
        result = {
            "range": {"from": earliest, "to": latest},
            "files": len(files),
            "sessions_with_data": len(session_stats),
            "grand": grand,
            "total_tokens": grand["prompt"] + grand["output"],
            "cache_rate": round(grand["cache_read"] / grand["prompt"] * 100, 1) if grand["prompt"] > 0 else 0,
        }
        if args.daily:
            result["daily"] = dict(sorted(grand_daily.items()))
        if args.sessions:
            result["sessions"] = [
                {"label": s["label"], "calls": s["calls"], "prompt": s["prompt"],
                 "cache_read": s["cache_read"], "new_input": s["new_input"],
                 "output": s["output"]}
                for s in sorted(session_stats, key=lambda x: x["prompt"], reverse=True)[:args.top]
            ]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # Text output
    total_tokens = grand["prompt"] + grand["output"]
    cache_rate = grand["cache_read"] / grand["prompt"] * 100 if grand["prompt"] > 0 else 0

    print("=" * 60)
    print("  OpenClaw Token 统计报告")
    print("=" * 60)
    print()
    print("  统计范围:       %s ~ %s" % (earliest, latest))
    print("  扫描文件:       %d 个" % len(files))
    print("  有数据的会话:   %d 个" % len(session_stats))
    print("  有效 API 调用:  %s 次" % format_number(grand["calls"]))
    print("  错误调用:       %s 次" % format_number(grand["errors"]))
    print("  Compaction:     %s 次" % format_number(grand["compactions"]))
    print()
    print("  --- Token 用量 ---")
    print("  Prompt (含缓存):  %s" % format_yi(grand["prompt"]))
    print("    缓存命中:       %s  (%.1f%%)" % (format_yi(grand["cache_read"]), cache_rate))
    print("    新增输入:       %s  (%.1f%%)" % (
        format_yi(grand["new_input"]),
        grand["new_input"] / grand["prompt"] * 100 if grand["prompt"] > 0 else 0
    ))
    print("  输出:             %s" % format_yi(grand["output"]))
    print()
    print("  --- 汇总 ---")
    print("  Token 总量:       %s" % format_yi(total_tokens))
    print()

    # Per-day breakdown
    if args.daily:
        print("=" * 60)
        print("  每日明细")
        print("=" * 60)
        print("%12s  %6s  %14s  %14s  %7s  %10s" % (
            "日期", "调用", "Prompt", "缓存命中", "缓存率", "输出"
        ))
        print("-" * 70)
        for day in sorted(grand_daily.keys()):
            d = grand_daily[day]
            rate = d["cache_read"] / d["prompt"] * 100 if d["prompt"] > 0 else 0
            print("%12s  %6s  %14s  %14s  %6.1f%%  %10s" % (
                day,
                format_number(d["calls"]),
                format_number(d["prompt"]),
                format_number(d["cache_read"]),
                rate,
                format_number(d["output"])
            ))
        print()

    # Per-session breakdown
    if args.sessions:
        print("=" * 60)
        print("  Top %d 会话 (按 Prompt 排序)" % args.top)
        print("=" * 60)
        sorted_sessions = sorted(session_stats, key=lambda x: x["prompt"], reverse=True)
        for s in sorted_sessions[:args.top]:
            rate = s["cache_read"] / s["prompt"] * 100 if s["prompt"] > 0 else 0
            time_range = ""
            if s["first_ts"] and s["last_ts"]:
                time_range = " (%s ~ %s)" % (s["first_ts"][:10], s["last_ts"][:10])
            print("  %s%s" % (s["label"], time_range))
            print("    调用: %s  Prompt: %s  缓存: %.1f%%  输出: %s" % (
                format_number(s["calls"]),
                format_yi(s["prompt"]),
                rate,
                format_number(s["output"])
            ))
        print()


if __name__ == "__main__":
    main()
