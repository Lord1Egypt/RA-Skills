#!/usr/bin/env python3
"""
记忆搜索脚本 - Memory Search Script

用法：
    python memory_search.py <关键词>
    python memory_search.py "之前" "项目"  # 多关键词

功能：
    在 MEMORY.md 和 memory/*.md 中搜索记忆
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_FILE = os.path.join(WORKSPACE, "MEMORY.md")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")


def search_file(file_path, keywords, max_results=10):
    """在单个文件中搜索关键词"""
    if not os.path.exists(file_path):
        return []
    
    results = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        line_lower = line.lower()
        if any(kw.lower() in line_lower for kw in keywords):
            # 获取上下文（前后各1行）
            context_before = lines[max(0, i-2):i]
            context_after = lines[i:min(len(lines), i+1)]
            context = context_before + context_after
            
            results.append({
                "file": file_path,
                "line": i,
                "content": line.strip(),
                "context": "".join(context)
            })
            
            if len(results) >= max_results:
                break
    
    return results


def search_memory(keywords):
    """搜索所有记忆文件"""
    all_results = []
    
    # 搜索 MEMORY.md
    if "MEMORY.md" in keywords or len(keywords) == 1:
        all_results.extend(search_file(MEMORY_FILE, keywords))
    
    # 搜索每日日记
    if os.path.exists(MEMORY_DIR):
        for filename in sorted(os.listdir(MEMORY_DIR), reverse=True):
            if filename.endswith(".md"):
                file_path = os.path.join(MEMORY_DIR, filename)
                all_results.extend(search_file(file_path, keywords, max_results=5))
    
    return all_results


def main():
    if len(sys.argv) < 2:
        print("用法: python memory_search.py <关键词> [关键词2 ...]")
        print("示例: python memory_search.py 项目 决策")
        sys.exit(1)
    
    keywords = sys.argv[1:]
    results = search_memory(keywords)
    
    if not results:
        print(f"未找到包含「{' '.join(keywords)}」的记忆")
        return
    
    print(f"找到 {len(results)} 条相关记忆：\n")
    for i, r in enumerate(results, 1):
        rel_path = os.path.relpath(r["file"], WORKSPACE)
        print(f"{i}. [{rel_path}:{r['line']}]")
        print(f"   {r['content']}")
        print()


if __name__ == "__main__":
    main()
