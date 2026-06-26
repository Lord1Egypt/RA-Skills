#!/usr/bin/env python3
"""
列出所有已归档的问题排查记录
"""
import os
import sys
import json

TROUBLE_DIR = ".trouble-shooting"
ARCHIVE_DIR = f"{TROUBLE_DIR}/archive"

def list_archives():
    if not os.path.exists(ARCHIVE_DIR):
        return []

    archives = []
    for filename in os.listdir(ARCHIVE_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(ARCHIVE_DIR, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    archives.append({
                        "id": data.get('id', 'unknown'),
                        "title": data.get('title', 'Untitled'),
                        "timestamp": data.get('timestamp', ''),
                        "solution_preview": data.get('solution', '')[:50] + '...' if data.get('solution') else 'No solution'
                    })
            except:
                pass

    return sorted(archives, key=lambda x: x['timestamp'], reverse=True)

def main():
    archives = list_archives()

    if not archives:
        print(json.dumps({"archives": [], "count": 0}))
        print("\n📭 暂无归档的问题排查记录")
        return

    result = {
        "archives": archives,
        "count": len(archives)
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))

    print(f"\n📚 已归档问题列表 (共 {len(archives)} 个):")
    print("-" * 60)
    for i, arc in enumerate(archives[:10], 1):
        print(f"{i}. [{arc['id']}] {arc['title']}")
        print(f"   时间: {arc['timestamp'][:16] if arc['timestamp'] else 'unknown'}")
        if i == 10 and len(archives) > 10:
            print(f"\n   ... 还有 {len(archives) - 10} 个记录")
            break

if __name__ == "__main__":
    main()
