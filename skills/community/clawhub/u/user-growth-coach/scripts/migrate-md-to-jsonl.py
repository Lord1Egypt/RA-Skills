#!/usr/bin/env python3
"""
migrate-md-to-jsonl.py
将 user-growth 的 markdown 记录迁移为 JSONL 格式。
"""

import json
import os
import re
from datetime import datetime

INPUT = os.path.expanduser(
    os.environ.get("GROWTH_MD_INPUT", "~/.openclaw/workspace/memory/user-growth/YYYY-MM.md")
)
OUTPUT = os.path.expanduser(
    os.environ.get("GROWTH_JSONL_OUTPUT", "~/.openclaw/workspace/memory/user-growth/YYYY-MM.jsonl")
)

def parse_md(filepath):
    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern 1: ## YYYY-MM-DD HH:MM | trigger | status
    p1 = re.findall(
        r'## (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) \| (\S+) \| (\S+)\n- 原始输入：(.+?)\n- 标签：(.+?)(?:\n|$)',
        content, re.DOTALL
    )
    for ts, trigger, status, inp, tags in p1:
        records.append({
            "id": ts.replace("-","").replace(" ","_").replace(":",""),
            "ts": ts + ":00+08:00",
            "trigger": trigger,
            "mode": "标准",
            "dimension": "未分类",
            "input": inp.strip(),
            "tags": [t.strip() for t in tags.split(",")],
            "mood": "neutral",
            "status": status
        })

    # Pattern 2: - 时间: ... 触发词: ... 
    blocks = re.split(r'(?=- 时间:)', content)
    for block in blocks:
        ts_m = re.search(r'时间:\s*(.+)', block)
        trigger_m = re.search(r'触发词:\s*(.+)', block)
        mode_m = re.search(r'模式:\s*(.+)', block)
        dim_m = re.search(r'维度:\s*(.+)', block)
        input_m = re.search(r'原始输入:\s*(.+)', block)
        tags_m = re.search(r'标签:\s*(.+)', block)
        status_m = re.search(r'状态:\s*(.+)', block)

        if ts_m and input_m:
            ts_raw = ts_m.group(1).strip()
            # 尝试解析时间
            try:
                dt = datetime.strptime(ts_raw, "%Y-%m-%d %H:%M")
                ts_iso = dt.strftime("%Y-%m-%dT%H:%M:00+08:00")
                rid = dt.strftime("%Y%m%d_%H%M")
            except ValueError:
                ts_iso = ts_raw
                rid = ts_raw.replace("-","").replace(" ","_").replace(":","")

            tags_raw = tags_m.group(1).strip() if tags_m else ""
            records.append({
                "id": rid,
                "ts": ts_iso,
                "trigger": trigger_m.group(1).strip() if trigger_m else "复盘",
                "mode": mode_m.group(1).strip() if mode_m else "标准",
                "dimension": dim_m.group(1).strip() if dim_m else "未分类",
                "input": input_m.group(1).strip(),
                "tags": [t.strip() for t in tags_raw.split(",") if t.strip()],
                "mood": "neutral",
                "status": status_m.group(1).strip() if status_m else "recorded"
            })

    # 去重（按 id）
    seen = set()
    unique = []
    for r in records:
        if r["id"] not in seen:
            seen.add(r["id"])
            unique.append(r)

    return unique


def main():
    if not os.path.exists(INPUT):
        print(f"源文件不存在: {INPUT}")
        return

    records = parse_md(INPUT)
    print(f"解析出 {len(records)} 条记录")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"✅ 已写入: {OUTPUT}")

    # 备份原文件
    backup = INPUT + ".bak"
    os.rename(INPUT, backup)
    print(f"📦 原文件已备份: {backup}")


if __name__ == "__main__":
    main()
