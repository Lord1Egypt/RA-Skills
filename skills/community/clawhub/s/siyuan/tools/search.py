#!/usr/bin/env python3
"""
Search SiYuan notes using SQL
使用 SQL 搜索思源笔记

Usage:
    python3 search.py "keyword"              # 搜索关键词
    python3 search.py "keyword" -l 50        # 限制结果数量
    python3 search.py "SELECT * FROM blocks WHERE content LIKE '%test%'" --sql
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from siyuan_client import SiYuanClient, SiYuanError


def search_content(client, keyword, limit=20, output_json=False):
    """Search for content in blocks"""
    try:
        # 转义 SQL 中的特殊字符
        escaped_keyword = keyword.replace("'", "''").replace("%", "\\%")
        
        stmt = f"""
            SELECT * FROM blocks 
            WHERE content LIKE '%{escaped_keyword}%' 
            ORDER BY updated DESC 
            LIMIT {limit}
        """
        
        results = client.query_sql(stmt)
        
        if output_json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            if not results:
                print(f"No results found for: '{keyword}'")
                return []
            
            print(f"Found {len(results)} result(s) for '{keyword}':\n")
            
            for i, block in enumerate(results, 1):
                content = block.get('content', '').strip()
                if not content:
                    continue
                
                # 截断长内容
                if len(content) > 150:
                    content = content[:150] + "..."
                
                block_type = block.get('type', 'unknown')
                block_id = block.get('id', 'N/A')
                root_id = block.get('root_id', 'N/A')
                
                type_emoji = {
                    'd': '📄',  # Document
                    'h': '📌',  # Heading
                    'p': '📝',  # Paragraph
                    'c': '💬',  # Code
                    't': '📊',  # Table
                    'l': '📋',  # List
                }.get(block_type, '•')
                
                print(f"{i}. {type_emoji} {content}")
                print(f"   Block: {block_id} | Doc: {root_id}")
                print()
        
        return results
    except SiYuanError as e:
        print(f"Error: {e}", file=sys.stderr)
        return []


def search_by_sql(client, sql_stmt, output_json=False):
    """Execute raw SQL query"""
    try:
        results = client.query_sql(sql_stmt)
        
        if output_json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"Query returned {len(results)} row(s):\n")
            for i, row in enumerate(results[:20], 1):  # 只显示前20行
                print(f"{i}. {json.dumps(row, ensure_ascii=False)[:200]}...")
            if len(results) > 20:
                print(f"\n... and {len(results) - 20} more rows")
        
        return results
    except SiYuanError as e:
        print(f"Error: {e}", file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser(
        description='Search SiYuan notes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 search.py "neural network"
  python3 search.py "keyword" -l 50 -j
  python3 search.py "SELECT * FROM blocks WHERE type='d' LIMIT 10" --sql
        """
    )
    parser.add_argument('query', help='Search keyword or SQL statement')
    parser.add_argument('--limit', '-l', type=int, default=20, help='Max results (default: 20)')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    parser.add_argument('--sql', '-s', action='store_true', help='Query is raw SQL')
    
    args = parser.parse_args()
    
    try:
        client = SiYuanClient()
    except SiYuanError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    if args.sql:
        search_by_sql(client, args.query, args.json)
    else:
        search_content(client, args.query, args.limit, args.json)


if __name__ == "__main__":
    main()
