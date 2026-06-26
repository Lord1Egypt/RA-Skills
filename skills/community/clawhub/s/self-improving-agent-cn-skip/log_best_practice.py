#!/usr/bin/env python3
"""
Self-Improving Agent - 最佳实践记录工具
记录发现的最佳做法
"""

import sys
import json
import os
from datetime import datetime

MEMORY_DIR = os.path.expanduser("~/.openclaw/memory/self-improving")

def ensure_dir():
    os.makedirs(MEMORY_DIR, exist_ok=True)

def log_best_practice(category, practice, reason=None):
    ensure_dir()
    
    entry = {
        "type": "best_practice",
        "timestamp": datetime.now().isoformat(),
        "category": category,  # security, performance, style, etc.
        "practice": practice,
        "reason": reason,
        "usage_count": 0
    }
    
    with open(f"{MEMORY_DIR}/best_practices.jsonl", "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    print(f"✅ 已记录最佳实践 [{category}]:")
    print(f"   💡 {practice}")
    if reason:
        print(f"   📝 {reason}")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--category', required=True, 
                       help='类别: security, performance, style, workflow')
    parser.add_argument('--practice', required=True, help='最佳实践内容')
    parser.add_argument('--reason', default=None, help='原因/好处')
    
    args = parser.parse_args()
    log_best_practice(args.category, args.practice, args.reason)

if __name__ == "__main__":
    main()
