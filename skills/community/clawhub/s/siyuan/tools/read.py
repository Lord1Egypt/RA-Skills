#!/usr/bin/env python3
"""
Read SiYuan document content
读取思源笔记文档内容

Usage:
    python3 read.py <doc_id>                # 读取文档 Markdown 内容
    python3 read.py <doc_id> -o output.md   # 保存到文件
    python3 read.py <doc_id> -i             # 显示文档信息
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from siyuan_client import SiYuanClient, SiYuanError


def get_doc_info(client, doc_id):
    """Get document metadata"""
    try:
        # 获取文档路径信息
        path_info = client.get_path_by_id(doc_id)
        hpath = client.get_hpath_by_id(doc_id)
        
        # 获取文档属性
        attrs = client.get_block_attrs(doc_id)
        
        info = {
            "id": doc_id,
            "title": attrs.get('title', '(无标题)'),
            "notebook": path_info.get('notebook', 'N/A'),
            "storage_path": path_info.get('path', 'N/A'),
            "human_path": hpath,
            "type": attrs.get('type', 'N/A'),
            "updated": attrs.get('updated', 'N/A'),
            "created": attrs.get('created', 'N/A'),
        }
        
        return info
    except SiYuanError as e:
        print(f"Error getting document info: {e}", file=sys.stderr)
        return None


def read_doc(client, doc_id, output_file=None):
    """Read document markdown content"""
    try:
        result = client.export_md_content(doc_id)
        
        content = result.get('content', '')
        hpath = result.get('hPath', '')
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Saved to: {output_file}")
        else:
            if hpath:
                print(f"# Document: {hpath}\n")
            print(content)
        
        return content
    except SiYuanError as e:
        print(f"Error reading document: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Read SiYuan document content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 read.py 20240602141622-l7ou7t7
  python3 read.py 20240602141622-l7ou7t7 -o ~/doc.md
  python3 read.py 20240602141622-l7ou7t7 -i
        """
    )
    parser.add_argument('doc_id', help='Document ID (e.g., 20240602141622-l7ou7t7)')
    parser.add_argument('--info', '-i', action='store_true', help='Show document metadata only')
    parser.add_argument('--output', '-o', metavar='FILE', help='Save to file instead of stdout')
    
    args = parser.parse_args()
    
    try:
        client = SiYuanClient()
    except SiYuanError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    if args.info:
        info = get_doc_info(client, args.doc_id)
        if info:
            print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        read_doc(client, args.doc_id, args.output)


if __name__ == "__main__":
    main()
