#!/usr/bin/env python3
"""查看/筛选思考火花"""

import json
import sys
import os
from datetime import datetime

DATA_FILE = os.path.expanduser("~/.openclaw/workspace/collection/思考火花.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"sparks": []}

def format_spark(s, show_content=True):
    lines = []
    lines.append(f"**{s['id']}** | {s['status']} | {s.get('origin', '-')}")
    if show_content:
        content = s.get('polished_content') or s.get('content', '')
        lines.append(f"  内容: {content[:100]}{'...' if len(content) > 100 else ''}")
    if s.get('tags'):
        lines.append(f"  标签: {', '.join(s['tags'])}")
    if s.get('source_refs'):
        lines.append(f"  关联: {', '.join(s['source_refs'])}")
    lines.append(f"  创建: {s.get('created_at', '')[:10]}")
    return "\n".join(lines)

def list_sparks(filter_type=None, tag=None):
    data = load_data()
    sparks = data.get("sparks", [])
    
    # 筛选
    if filter_type == "raw":
        sparks = [s for s in sparks if s["status"] == "raw"]
    elif filter_type == "polished":
        sparks = [s for s in sparks if s["status"] == "polished"]
    elif filter_type == "today":
        today = datetime.now().strftime("%Y-%m-%d")
        sparks = [s for s in sparks if s.get("created_at", "").startswith(today)]
    
    if tag:
        sparks = [s for s in sparks if tag in s.get("tags", [])]
    
    if not sparks:
        print("No sparks found.")
        return
    
    print(f"共 {len(sparks)} 条记录:\n")
    for s in sparks:
        print(format_spark(s))
        print()

if __name__ == "__main__":
    filter_type = None
    tag = None
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "raw":
            filter_type = "raw"
        elif sys.argv[1] == "polished":
            filter_type = "polished"
        elif sys.argv[1] == "today":
            filter_type = "today"
        elif sys.argv[1].startswith("tag:"):
            tag = sys.argv[1][4:]
    
    list_sparks(filter_type, tag)
