#!/usr/bin/env python3
"""
Self-Improving Agent - 记忆检查工具
执行命令前检查是否有相关记忆
"""

import sys
import json
import os

MEMORY_DIR = os.path.expanduser("~/.openclaw/memory/self-improving")

def check_memory(command):
    """检查与命令相关的记忆"""
    if not os.path.exists(MEMORY_DIR):
        return []
    
    results = []
    
    # 检查错误记录
    errors_file = f"{MEMORY_DIR}/errors.jsonl"
    if os.path.exists(errors_file):
        with open(errors_file, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    # 简单匹配：命令包含关键词
                    cmd_keywords = command.lower().split()
                    err_cmd = entry.get("command", "").lower()
                    if any(kw in err_cmd for kw in cmd_keywords[:2]):
                        results.append(("错误", entry))
                except:
                    pass
    
    # 检查纠正记录
    corrections_file = f"{MEMORY_DIR}/corrections.jsonl"
    if os.path.exists(corrections_file):
        with open(corrections_file, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    # 检查主题是否匹配
                    if entry.get("topic", "").lower() in command.lower():
                        results.append(("纠正", entry))
                except:
                    pass
    
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: check_memory.py --command 'cmd'")
        sys.exit(1)
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--command', required=True)
    args = parser.parse_args()
    
    memories = check_memory(args.command)
    
    if memories:
        print(f"⚠️ 发现 {len(memories)} 条相关记忆:\n")
        for typ, mem in memories[:5]:  # 最多显示5条
            if typ == "错误":
                print(f"  [{typ}] {mem.get('timestamp', '')[:10]}")
                print(f"      命令: {mem.get('command', '')[:40]}...")
                print(f"      错误: {mem.get('error', '未知')[:40]}")
                if mem.get('fix'):
                    print(f"      💡 建议: {mem['fix']}")
            else:
                print(f"  [{typ}] {mem.get('timestamp', '')[:10]} - {mem.get('topic', '')}")
                print(f"      ❌ {mem.get('wrong', '')}")
                print(f"      ✅ {mem.get('correct', '')}")
            print()
    else:
        print("✅ 未发现相关记忆")

if __name__ == "__main__":
    main()
