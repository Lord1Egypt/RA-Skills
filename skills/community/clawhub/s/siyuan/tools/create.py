#!/usr/bin/env python3
"""
Create SiYuan notebooks and documents
创建思源笔记的笔记本和文档

Usage:
    python3 create.py --notebook "New Notebook"          # 创建笔记本
    python3 create.py --doc 20210817205410 /path "内容"  # 在笔记本中创建文档
    python3 create.py --doc 20210817205410 /folder/doc "# Title\n\nContent"
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from siyuan_client import SiYuanClient, SiYuanError


def create_notebook(client, name):
    """Create a new notebook"""
    try:
        result = client.create_notebook(name)
        notebook_id = result.get('notebook', {}).get('id')
        print(f"✅ Created notebook: {name}")
        print(f"   ID: {notebook_id}")
        return notebook_id
    except SiYuanError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return None


def create_document(client, notebook_id, path, markdown=""):
    """Create a new document"""
    try:
        doc_id = client.create_doc_with_md(notebook_id, path, markdown)
        print(f"✅ Created document: {path}")
        print(f"   ID: {doc_id}")
        return doc_id
    except SiYuanError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Create SiYuan notebooks and documents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 create.py --notebook "My Project"
  python3 create.py --doc 20210817205410 /readme "# Hello\n\nWorld"
  python3 create.py --doc 20210817205410 /notes/ideas "## Ideas\n\n- First idea"
        """
    )
    parser.add_argument('--notebook', '-n', metavar='NAME', help='Create a new notebook')
    parser.add_argument('--doc', '-d', nargs=3, metavar=('NOTEBOOK_ID', 'PATH', 'MARKDOWN'),
                        help='Create a document (path should start with /)')
    
    args = parser.parse_args()
    
    if not args.notebook and not args.doc:
        parser.print_help()
        sys.exit(1)
    
    try:
        client = SiYuanClient()
    except SiYuanError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    if args.notebook:
        create_notebook(client, args.notebook)
    
    if args.doc:
        notebook_id, path, markdown = args.doc
        create_document(client, notebook_id, path, markdown)


if __name__ == "__main__":
    main()
