#!/usr/bin/env python3
"""
quick_search.py - 快速搜索CLI
命令行快速搜索记忆，无需Web界面
"""
import sqlite3
import sys
import json
import re
from pathlib import Path
from datetime import datetime


MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
MEMORY_DB = MEMORY_DIR / "memory.db"


def search_memories(query: str, limit: int = 20, type_filter: str = None) -> list:
    """搜索记忆"""
    if not MEMORY_DB.exists():
        return []
    
    conn = sqlite3.connect(MEMORY_DB)
    
    # 基础查询
    sql = """
        SELECT id, type, importance, content, tags, created_at, updated_at
        FROM memories
        WHERE content LIKE ?
    """
    params = [f"%{query}%"]
    
    if type_filter:
        sql += " AND type = ?"
        params.append(type_filter)
    
    sql += " ORDER BY updated_at DESC LIMIT ?"
    params.append(limit)
    
    cursor = conn.execute(sql, params)
    results = []
    
    for row in cursor:
        results.append({
            "id": row[0],
            "type": row[1],
            "importance": row[2],
            "content": row[3],
            "tags": json.loads(row[4]) if row[4] else [],
            "created_at": row[5],
            "updated_at": row[6]
        })
    
    conn.close()
    return results


def format_result(item: dict, show_content: bool = True) -> str:
    """格式化单个结果"""
    importance_icons = {
        "critical": "🔴",
        "high": "🟠", 
        "normal": "🟢",
        "low": "⚪"
    }
    icon = importance_icons.get(item["importance"], "⚪")
    
    time_str = item["updated_at"][:16] if item["updated_at"] else ""
    
    output = f"\n{icon} [{item['type']}] {time_str}"
    
    if item["tags"]:
        tags_str = ", ".join(item["tags"][:5])
        output += f"\n   🏷️ {tags_str}"
    
    if show_content:
        content = item["content"]
        if len(content) > 200:
            content = content[:200] + "..."
        output += f"\n   {content}"
    
    output += f"\n   📎 ID: {item['id']}"
    
    return output


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="🦞 快速搜索记忆")
    parser.add_argument("query", nargs="?", help="搜索关键词")
    parser.add_argument("-l", "--limit", type=int, default=20, help="结果数量限制")
    parser.add_argument("-t", "--type", help="按类型过滤 (info/error/decision/task)")
    parser.add_argument("-j", "--json", action="store_true", help="JSON输出")
    parser.add_argument("-i", "--id", action="store_true", help="仅显示ID")
    parser.add_argument("-c", "--count", action="store_true", help="仅显示数量")
    
    args = parser.parse_args()
    
    if not args.query:
        parser.print_help()
        return
    
    results = search_memories(args.query, limit=args.limit, type_filter=args.type)
    
    if args.count:
        print(len(results))
        return
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    
    if not results:
        print("🔍 无结果")
        return
    
    print(f"\n🦞 搜索 '{args.query}' - 找到 {len(results)} 条")
    
    if args.id:
        for r in results:
            print(r["id"])
    else:
        for r in results:
            print(format_result(r))
    
    print()


if __name__ == "__main__":
    main()
