#!/usr/bin/env python3
"""
Delete SiYuan notebooks and documents
删除思源笔记的笔记本和文档

Usage:
    python3 delete.py --notebook <notebook_id>          # 删除笔记本
    python3 delete.py --doc <doc_id>                   # 删除文档
    python3 delete.py --block <block_id>               # 删除块
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from siyuan_client import SiYuanClient, SiYuanError


def delete_notebook(client, notebook_id, confirm=True):
    """Delete a notebook"""
    try:
        # 获取笔记本名称
        notebooks = client.list_notebooks()
        notebook = next((nb for nb in notebooks if nb['id'] == notebook_id), None)
        
        if not notebook:
            print(f"❌ Notebook not found: {notebook_id}", file=sys.stderr)
            return False
        
        name = notebook['name']
        
        if confirm:
            response = input(f"⚠️  Delete notebook '{name}' ({notebook_id})? [y/N] ")
            if response.lower() != 'y':
                print("Cancelled")
                return False
        
        if client.remove_notebook(notebook_id):
            print(f"✅ Deleted notebook: {name}")
            return True
        else:
            print(f"❌ Failed to delete notebook: {name}", file=sys.stderr)
            return False
    except SiYuanError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return False


def delete_document(client, doc_id, confirm=True):
    """Delete a document"""
    try:
        # 获取文档标题
        try:
            attrs = client.get_block_attrs(doc_id)
            title = attrs.get('title', doc_id)
        except:
            title = doc_id
        
        if confirm:
            response = input(f"⚠️  Delete document '{title}' ({doc_id})? [y/N] ")
            if response.lower() != 'y':
                print("Cancelled")
                return False
        
        if client.remove_doc_by_id(doc_id):
            print(f"✅ Deleted document: {title}")
            return True
        else:
            print(f"❌ Failed to delete document: {title}", file=sys.stderr)
            return False
    except SiYuanError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return False


def delete_block(client, block_id, confirm=True):
    """Delete a block"""
    try:
        if confirm:
            response = input(f"⚠️  Delete block {block_id}? [y/N] ")
            if response.lower() != 'y':
                print("Cancelled")
                return False
        
        if client.delete_block(block_id):
            print(f"✅ Deleted block: {block_id}")
            return True
        else:
            print(f"❌ Failed to delete block: {block_id}", file=sys.stderr)
            return False
    except SiYuanError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Delete SiYuan notebooks and documents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 delete.py --notebook 20210817205410-2kvfpfn
  python3 delete.py --doc 20240602141622-l7ou7t7
  python3 delete.py --block 20240602141622-abcdef1
        """
    )
    parser.add_argument('--notebook', '-n', metavar='ID', help='Delete notebook by ID')
    parser.add_argument('--doc', '-d', metavar='ID', help='Delete document by ID')
    parser.add_argument('--block', '-b', metavar='ID', help='Delete block by ID')
    parser.add_argument('--yes', '-y', action='store_true', help='Skip confirmation')
    
    args = parser.parse_args()
    
    if not args.notebook and not args.doc and not args.block:
        parser.print_help()
        sys.exit(1)
    
    try:
        client = SiYuanClient()
    except SiYuanError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    success = True
    
    if args.notebook:
        success = delete_notebook(client, args.notebook, confirm=not args.yes) and success
    
    if args.doc:
        success = delete_document(client, args.doc, confirm=not args.yes) and success
    
    if args.block:
        success = delete_block(client, args.block, confirm=not args.yes) and success
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
