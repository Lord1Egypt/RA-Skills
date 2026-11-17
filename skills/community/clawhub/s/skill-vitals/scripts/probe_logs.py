#!/usr/bin/env python3
"""
探测本机 Agent 会话日志的结构，判断能否从中挖出 skill 触发与标注信号。

隐私优先：只输出字段名、类型、计数和长度，**不输出任何业务内容**。
唯一的例外是 --sample-keys，也只打印键名。

用法:
    python3 probe_logs.py
    python3 probe_logs.py --path ~/some/other/logs
    python3 probe_logs.py --skill-name my-skill   # 看该名字在日志里出现几次
"""

import argparse
import json
import os
import re
from collections import Counter
from pathlib import Path

CANDIDATE_DIRS = {
    "claude-code": ["~/.claude/projects", "~/.claude/history"],
    "codex": ["~/.codex/sessions", "~/.codex/history"],
    "openclaw": ["~/.openclaw/agents"],
    "cc-switch": ["~/.cc-switch/sessions"],
}


def observed_skill_reads(obj, out, event_prefix):
    """Collect indirect evidence: tool reads whose arguments name SKILL.md."""
    if isinstance(obj, dict):
        name = obj.get("name")
        args = obj.get("arguments", obj.get("input"))
        if isinstance(name, str) and name.lower() in ("read", "read_file") and args is not None:
            blob = args if isinstance(args, str) else json.dumps(args, ensure_ascii=False)
            for raw in re.findall(r"[^\"'\s,}\]]*SKILL\.md", blob, re.I):
                path = raw.replace("\\\\", "/").replace("\\", "/")
                call_id = obj.get("id") or obj.get("toolCallId") or obj.get("tool_call_id")
                out.add((str(call_id or event_prefix), path))
        for value in obj.values():
            observed_skill_reads(value, out, event_prefix)
    elif isinstance(obj, list):
        for value in obj:
            observed_skill_reads(value, out, event_prefix)


def walk_json_lines(path: Path, limit=4000):
    """逐行读 jsonl；非 json 行跳过。"""
    n = 0
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
                n += 1
                if n >= limit:
                    return
    except OSError:
        return


def flatten_keys(obj, prefix="", out=None, depth=0):
    if out is None:
        out = set()
    if depth > 4:
        return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else k
            out.add(key)
            flatten_keys(v, key, out, depth + 1)
    elif isinstance(obj, list) and obj:
        flatten_keys(obj[0], prefix + "[]", out, depth + 1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", action="append", default=[])
    ap.add_argument("--host", choices=("all", *CANDIDATE_DIRS), default="all",
                    help="只探测一个宿主；默认探测全部已知日志目录")
    ap.add_argument("--skill-name", help="检查该 skill 名在日志中出现的次数")
    ap.add_argument("--max-files", type=int, default=40)
    ap.add_argument("--deep", action="store_true",
                    help="统计去重后的 SKILL.md read 观测；这是间接证据，不是触发次数")
    args = ap.parse_args()

    defaults = (sum(CANDIDATE_DIRS.values(), []) if args.host == "all"
                else CANDIDATE_DIRS[args.host])
    dirs = [Path(os.path.expanduser(d)) for d in defaults + args.path]
    found_dirs, seen_dirs = [], set()
    for directory in dirs:
        if not directory.is_dir():
            continue
        resolved = directory.resolve()
        if resolved in seen_dirs:
            continue
        seen_dirs.add(resolved)
        found_dirs.append(directory)

    print("=== 日志目录 ===")
    if not found_dirs:
        print("未找到。用 --path 指定，或告诉我你的宿主把会话存在哪。")
        return
    for d in found_dirs:
        files = list(d.rglob("*.jsonl")) + list(d.rglob("*.json"))
        print(f"  {d}  ({len(files)} 个文件)")

    all_files = []
    for d in found_dirs:
        all_files += sorted(d.rglob("*.jsonl"), key=lambda p: -p.stat().st_mtime)
        all_files += sorted(d.rglob("*.json"), key=lambda p: -p.stat().st_mtime)
    # trajectory 通常复制同一会话的工具事件；有主 transcript 时不要双计。
    primary_names = {p.name for p in all_files
                     if p.suffix == ".jsonl" and ".trajectory" not in p.name}
    all_files = [p for p in all_files
                 if not (p.name.endswith(".trajectory.jsonl") and
                         p.name.replace(".trajectory.jsonl", ".jsonl") in primary_names)]
    all_files = all_files[: args.max_files]

    if not all_files:
        print("\n目录存在但没有 json/jsonl 文件。")
        return

    keys = Counter()
    roles = Counter()
    types = Counter()
    records = 0
    skill_hits = 0
    skill_word_hits = 0
    read_events = set()

    for fp in all_files:
        for record_index, rec in enumerate(walk_json_lines(fp)):
            records += 1
            for k in flatten_keys(rec):
                keys[k] += 1
            if isinstance(rec, dict):
                for field in ("role", "type", "event"):
                    v = rec.get(field)
                    if isinstance(v, str):
                        (roles if field == "role" else types)[f"{field}={v}"] += 1
            blob = json.dumps(rec, ensure_ascii=False)
            if "skill" in blob.lower():
                skill_word_hits += 1
            if args.skill_name and args.skill_name in blob:
                skill_hits += 1
            if args.deep:
                observed_skill_reads(rec, read_events,
                                     f"{fp.name}:{record_index}")

    print(f"\n=== 概览 ===")
    print(f"  扫描文件 {len(all_files)} 个，记录 {records} 条")
    print(f"  含 'skill' 字样的记录：{skill_word_hits} "
          f"({skill_word_hits/max(records,1)*100:.1f}%)")
    if args.skill_name:
        print(f"  含 '{args.skill_name}' 的记录：{skill_hits}")
    if args.deep:
        by_skill = Counter(path for _, path in read_events)
        print("\n=== SKILL.md 读取观测（间接证据）===")
        print(f"  去重 read 事件：{len(read_events)}")
        for path, count in by_skill.most_common():
            print(f"  {count:6}  {path}")
        print("  口径：只证明日志中观察到 read；不等于自动触发，也不能用于僵尸判定。")

    print(f"\n=== 出现最多的字段（仅键名）===")
    for k, c in keys.most_common(35):
        print(f"  {c:6}  {k}")

    print(f"\n=== 角色 / 类型枚举 ===")
    for k, c in (roles + types).most_common(20):
        print(f"  {c:6}  {k}")

    print("\n=== 判断要点 ===")
    has_role = any(k.endswith("role") for k in keys)
    has_tool = any("tool" in k.lower() for k in keys)
    has_ts = any(("timestamp" in k.lower() or k.endswith("time")) for k in keys)
    print(f"  能区分用户/助手轮次： {'是' if has_role else '否 —— 挖不出纠正信号'}")
    print(f"  有工具调用记录：     {'是' if has_tool else '否'}")
    print(f"  有时间戳：           {'是' if has_ts else '否'}")
    print(f"  能识别 skill 激活：  "
          f"{'可能，需人工看一条样本确认' if skill_word_hits else '否 —— 需要网关方案'}")
    print("\n本脚本不输出任何业务内容。要确认字段含义，请自己打开一条记录查看。")


if __name__ == "__main__":
    main()
