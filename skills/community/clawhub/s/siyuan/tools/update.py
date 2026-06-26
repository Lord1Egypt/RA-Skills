#!/usr/bin/env python3
"""
Update SiYuan document and block content
更新思源笔记文档和块内容

Usage:
    python3 update.py --doc <doc_id> --markdown "# New Title\n\nContent"  # 更新文档
    python3 update.py --block <block_id> --markdown "New content"       # 更新块
    python3 update.py --append <doc_id> --markdown "\n\nAppended text"  # 追加内容
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from siyuan_client import SiYuanClient, SiYuanError


def update_document(client, doc_id, markdown):
    """Update document content (replaces entire document)"""
    try:
        # 获取文档所在笔记本
        path_info = client.get_path_by_id(doc_id)
        notebook_id = path_info.get('notebook')
        
        if not notebook_id:
            print(f"❌ Cannot determine notebook for document: {doc_id}", file=sys.stderr)
            return False
        
        # 获取路径
        hpath = client.get_hpath_by_id(doc_id)
        path = hpath if hpath else doc_id
        
        # 删除旧文档并创建新文档
        # 注意：由于思源没有直接更新文档内容的API，我们使用删除+重建的方式
        # 但这会改变文档ID，谨慎使用！
        print(f"⚠️  Warning: This will delete and recreate the document (ID will change)", file=sys.stderr)
        response = input(f"Continue? [y/N] ")
        if response.lower() != 'y':
            print("Cancelled")
            return False
        
        # 删除旧文档
        client.remove_doc_by_id(doc_id)
        
        # 创建新文档
        new_doc_id = client.create_doc_with_md(notebook_id, path, markdown)
        
        print(f"✅ Updated document (new ID: {new_doc_id})")
        return True
    except SiYuanError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return False


def update_block(client, block_id, markdown):
    """Update a block's content"""
    try:
        if client.update_block("markdown", markdown, block_id):
            print(f"✅ Updated block: {block_id}")
            return True
        else:
            print(f"❌ Failed to update block: {block_id}", file=sys.stderr)
            return False
    except SiYuanError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return False


def append_to_document(client, doc_id, markdown):
    """Append content to the end of a document"""
    try:
        result = client.append_block("markdown", markdown, doc_id)
        if result:
            print(f"✅ Appended {len(result)} block(s) to document")
            return True
        else:
            print(f"❌ Failed to append to document", file=sys.stderr)
            return False
    except SiYuanError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return False


def prepend_to_document(client, doc_id, markdown):
    """Prepend content to the beginning of a document"""
    try:
        result = client.prepend_block("markdown", markdown, doc_id)
        if result:
            print(f"✅ Prepended {len(result)} block(s) to document")
            return True
        else:
            print(f"❌ Failed to prepend to document", file=sys.stderr)
            return False
    except SiYuanError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return False


def insert_block(client, markdown, parent_id=None, previous_id=None, next_id=None):
    """Insert a block at specific position"""
    try:
        result = client.insert_block("markdown", markdown, parent_id, previous_id, next_id)
        if result:
            print(f"✅ Inserted {len(result)} block(s)")
            for block in result:
                for op in block.get('doOperations', []):
                    print(f"   ID: {op.get('id')}")
            return True
        else:
            print(f"❌ Failed to insert block", file=sys.stderr)
            return False
    except SiYuanError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Update SiYuan document and block content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 update.py --block 20240602141622-abcdef1 --markdown "Updated content"
  python3 update.py --append 20240602141622-l7ou7t7 --markdown "\n\nFooter text"
  python3 update.py --prepend 20240602141622-l7ou7t7 --markdown "# New Header\n"
  python3 update.py --insert "New paragraph" --parent 20240602141622-l7ou7t7
        """
    )
    parser.add_argument('--doc', '-d', metavar='ID', help='Document ID to update (caution: changes ID)')
    parser.add_argument('--block', '-b', metavar='ID', help='Block ID to update')
    parser.add_argument('--append', '-a', metavar='ID', help='Document ID to append to')
    parser.add_argument('--prepend', '-p', metavar='ID', help='Document ID to prepend to')
    parser.add_argument('--insert', '-i', metavar='MARKDOWN', help='Markdown content to insert')
    parser.add_argument('--markdown', '-m', required=True, help='Markdown content')
    parser.add_argument('--parent-id', help='Parent block/document ID for insert')
    parser.add_argument('--previous-id', help='Insert after this block ID')
    parser.add_argument('--next-id', help='Insert before this block ID')
    
    args = parser.parse_args()
    
    try:
        client = SiYuanClient()
    except SiYuanError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    success = False
    
    if args.doc:
        success = update_document(client, args.doc, args.markdown)
    elif args.block:
        success = update_block(client, args.block, args.markdown)
    elif args.append:
        success = append_to_document(client, args.append, args.markdown)
    elif args.prepend:
        success = prepend_to_document(client, args.prepend, args.markdown)
    elif args.insert:
        success = insert_block(client, args.insert, args.parent_id, args.previous_id, args.next_id)
    else:
        parser.print_help()
        sys.exit(1)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
