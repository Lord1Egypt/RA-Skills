#!/usr/bin/env python3
"""
Self-Improving Agent - 错误记录工具
自动捕获并记录命令失败
"""

import sys
import json
import os
from datetime import datetime

MEMORY_DIR = os.path.expanduser("~/.openclaw/memory/self-improving")

def ensure_dir():
    os.makedirs(MEMORY_DIR, exist_ok=True)

def log_error(command, error_msg, fix=None, priority="medium"):
    ensure_dir()
    
    entry = {
        "type": "error",
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "error": error_msg,
        "fix": fix,
        "priority": priority,
        "status": "pending"
    }
    
    # 追加到jsonl文件
    with open(f"{MEMORY_DIR}/errors.jsonl", "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    print(f"✅ 已记录错误: {command[:50]}...")
    print(f"   建议修复: {fix or '待分析'}")

def main():
    if len(sys.argv) < 3:
        print("Usage: log_error.py --command 'cmd' --error 'err' [--fix 'solution']")
        sys.exit(1)
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--command', required=True)
    parser.add_argument('--error', required=True)
    parser.add_argument('--fix', default=None)
    parser.add_argument('--priority', default='medium')
    
    args = parser.parse_args()
    log_error(args.command, args.error, args.fix, args.priority)

if __name__ == "__main__":
    main()
