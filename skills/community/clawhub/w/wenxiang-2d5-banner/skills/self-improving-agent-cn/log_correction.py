#!/usr/bin/env python3
"""
Self-Improving Agent - 用户纠正记录工具
记录用户的纠正，避免再犯
"""

import sys
import json
import os
from datetime import datetime

MEMORY_DIR = os.path.expanduser("~/.openclaw/memory/self-improving")

def ensure_dir():
    os.makedirs(MEMORY_DIR, exist_ok=True)

def log_correction(topic, wrong, correct, context=None):
    ensure_dir()
    
    entry = {
        "type": "correction",
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "wrong": wrong,
        "correct": correct,
        "context": context,
        "count": 1  # 被纠正次数
    }
    
    # 检查是否已存在类似纠正
    corrections_file = f"{MEMORY_DIR}/corrections.jsonl"
    if os.path.exists(corrections_file):
        with open(corrections_file, "r") as f:
            for line in f:
                try:
                    old = json.loads(line.strip())
                    if old.get("topic") == topic and old.get("wrong") == wrong:
                        entry["count"] = old.get("count", 1) + 1
                        break
                except:
                    pass
    
    with open(corrections_file, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    print(f"✅ 已记录纠正 [{topic}]:")
    print(f"   ❌ 错误: {wrong}")
    print(f"   ✅ 正确: {correct}")
    if context:
        print(f"   📍 位置: {context}")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', required=True, help='纠正主题')
    parser.add_argument('--wrong', required=True, help='错误做法')
    parser.add_argument('--correct', required=True, help='正确做法')
    parser.add_argument('--context', default=None, help='上下文/位置')
    
    args = parser.parse_args()
    log_correction(args.topic, args.wrong, args.correct, args.context)

if __name__ == "__main__":
    main()
