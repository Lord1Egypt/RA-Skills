#!/usr/bin/env python3
"""
Move SiYuan documents
移动思源笔记文档

Usage:
    python3 move.py --doc <doc_id> --to-notebook <nb_id>          # 移动文档到另一个笔记本
    python3 move.py --docs id1 id2 --to-notebook <nb_id>            # 批量移动文档
    python3 move.py --from-paths /path1 /path2 --to-nb <nb_id> --to-path /
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from siyuan_client import SiYuanClient, SiYuanError


def move_doc_by_id(client, doc_id, to_notebook_id, confirm=True):
    """Move a single document by ID"""
    try:
        # 获取文档信息
        try:
            hpath = client.get_hpath_by_id(doc_id)
            title = hpath.split('/')[-1] if '/' in hpath else hpath
        except:
            title = doc_id
        
        if confirm:
            response = input(f"⚠️  Move document '{title}' ({doc_id}) to notebook {to_notebook_id}? [y/N] ")
            if response.lower() != 'y':
                print("Cancelled")
                return False
        
        if client.move_docs_by_id([doc_id], to_notebook_id):
            print(f"✅ Moved document: {title}")
            return True
        else:
            print(f"❌ Failed to move document: {title}", file=sys.stderr)
            return False
    except SiYuanError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return False


def move_docs_by_id(client, doc_ids, to_notebook_id, confirm=True):
    """Move multiple documents by ID"""
    try:
        if confirm:
            response = input(f"⚠️  Move {len(doc_ids)} documents to notebook {to_notebook_id}? [y/N] ")
            if response.lower() != 'y':
                print("Cancelled")
                return False
        
        if client.move_docs_by_id(doc_ids, to_notebook_id):
            print(f"✅ Moved {len(doc_ids)} documents")
            return True
        else:
            print(f"❌ Failed to move documents", file=sys.stderr)
            return False
    except SiYuanError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return False


def move_docs_by_path(client, from_paths, to_notebook_id, to_path="/"):
    """Move documents by path"""
    try:
        if client.move_docs(from_paths, to_notebook_id, to_path):
            print(f"✅ Moved {len(from_paths)} document(s) to {to_path}")
            return True
        else:
            print(f"❌ Failed to move documents", file=sys.stderr)
            return False
    except SiYuanError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Move SiYuan documents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 move.py --doc 20240602141622-l7ou7t7 --to-notebook 20210817205410-2kvfpfn
  python3 move.py --docs id1 id2 id3 --to-notebook 20210817205410-2kvfpfn
  python3 move.py --from-paths /doc1.sy /doc2.sy --to-nb 20210817205410 --to-path /folder/
        """
    )
    parser.add_argument('--doc', '-d', metavar='ID', help='Document ID to move')
    parser.add_argument('--docs', nargs='+', metavar='ID', help='Multiple document IDs to move')
    parser.add_argument('--from-paths', nargs='+', metavar='PATH', help='Source document paths')
    parser.add_argument('--to-notebook', '-t', metavar='ID', required=True, help='Target notebook ID')
    parser.add_argument('--to-path', '-p', default='/', help='Target path (default: /)')
    parser.add_argument('--yes', '-y', action='store_true', help='Skip confirmation')
    
    args = parser.parse_args()
    
    try:
        client = SiYuanClient()
    except SiYuanError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    success = True
    
    if args.doc:
        success = move_doc_by_id(client, args.doc, args.to_notebook, confirm=not args.yes) and success
    elif args.docs:
        success = move_docs_by_id(client, args.docs, args.to_notebook, confirm=not args.yes) and success
    elif args.from_paths:
        success = move_docs_by_path(client, args.from_paths, args.to_notebook, args.to_path) and success
    else:
        parser.print_help()
        sys.exit(1)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
