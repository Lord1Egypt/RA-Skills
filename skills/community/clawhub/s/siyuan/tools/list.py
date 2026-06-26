#!/usr/bin/env python3
"""
List SiYuan notebooks and documents
列出思源笔记的笔记本和文档

Usage:
    python3 list.py --notebooks              # 列出所有笔记本
    python3 list.py --docs <notebook_id>     # 列出指定笔记本中的文档
    python3 list.py -n -j                    # JSON 格式输出笔记本列表
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from siyuan_client import SiYuanClient, SiYuanError


def list_notebooks(client, output_json=False):
    """List all notebooks"""
    try:
        notebooks = client.list_notebooks()
        
        if output_json:
            print(json.dumps(notebooks, ensure_ascii=False, indent=2))
        else:
            print(f"Found {len(notebooks)} notebook(s):\n")
            for nb in notebooks:
                status = "📕" if nb.get('closed') else "📖"
                print(f"{status} {nb['name']}")
                print(f"   ID: {nb['id']}")
                print(f"   Sort: {nb.get('sort', 'N/A')}")
                print()
        
        return notebooks
    except SiYuanError as e:
        print(f"Error: {e}", file=sys.stderr)
        return []


def list_docs(client, notebook_id, output_json=False):
    """List documents in a notebook using SQL query"""
    try:
        # 使用 SQL 查询获取文档列表
        docs = client.query_sql(f"""
            SELECT id, content, created, updated, path 
            FROM blocks 
            WHERE box = '{notebook_id}' AND type = 'd' 
            ORDER BY updated DESC
        """)
        
        if output_json:
            print(json.dumps(docs, ensure_ascii=False, indent=2))
        else:
            # 获取笔记本名称
            notebooks = client.list_notebooks()
            notebook_name = next((nb['name'] for nb in notebooks if nb['id'] == notebook_id), "Unknown")
            
            print(f"Documents in '{notebook_name}' ({len(docs)} total):\n")
            for doc in docs:
                doc_id = doc.get('id', 'N/A')
                title = doc.get('content', '(无标题)').lstrip('#').strip() if doc.get('content') else '(无标题)'
                updated = doc.get('updated', 'N/A')
                if len(updated) >= 14:
                    updated = f"{updated[:4]}-{updated[4:6]}-{updated[6:8]} {updated[8:10]}:{updated[10:12]}"
                
                print(f"📝 {title}")
                print(f"   ID: {doc_id}")
                print(f"   Updated: {updated}")
                print()
        
        return docs
    except SiYuanError as e:
        print(f"Error: {e}", file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser(
        description='List SiYuan notebooks and documents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 list.py --notebooks              # List all notebooks
  python3 list.py --docs 20210817205410    # List docs in notebook
  python3 list.py -n -j                    # Output notebooks as JSON
        """
    )
    parser.add_argument('--notebooks', '-n', action='store_true', help='List all notebooks')
    parser.add_argument('--docs', '-d', metavar='NOTEBOOK_ID', help='List documents in notebook')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Initialize client
    try:
        client = SiYuanClient()
    except SiYuanError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Execute command
    if args.docs:
        list_docs(client, args.docs, args.json)
    else:
        # Default to listing notebooks
        list_notebooks(client, args.json)


if __name__ == "__main__":
    main()
