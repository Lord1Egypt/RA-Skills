#!/usr/bin/env python3
"""
Export SiYuan notes to Markdown files
导出思源笔记为 Markdown 文件

Usage:
    python3 export.py -o ~/backup/              # 导出所有笔记本
    python3 export.py -n "工作" -o ~/backup/    # 导出指定笔记本
    python3 export.py -d 20240602141622 -o ~/   # 导出单个文档
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from siyuan_client import SiYuanClient, SiYuanError


def sanitize_filename(name: str) -> str:
    """Make filename safe for filesystem"""
    # 移除或替换不安全的字符
    unsafe = '<>:"/\\|?*\n\r\t'
    for char in unsafe:
        name = name.replace(char, '_')
    # 移除开头的点和空格
    name = name.strip('. ')
    # 限制长度
    if len(name) > 100:
        name = name[:100]
    return name or 'untitled'


def export_document(client, doc_id, output_dir, notebook_name=""):
    """Export a single document"""
    try:
        # 获取文档内容
        result = client.export_md_content(doc_id)
        content = result.get('content', '')
        hpath = result.get('hPath', '')
        
        # 确定文件名
        if hpath:
            # 使用 hpath 的最后一部分作为文件名
            title = hpath.split('/')[-1] if '/' in hpath else hpath
        else:
            # 从内容中提取标题
            lines = content.split('\n')
            title = lines[0].lstrip('#').strip() if lines else 'untitled'
        
        # 清理文件名
        safe_title = sanitize_filename(title)
        filename = f"{safe_title}.md"
        
        # 处理重复文件名
        filepath = output_dir / filename
        counter = 1
        while filepath.exists():
            filename = f"{safe_title}_{counter}.md"
            filepath = output_dir / filename
            counter += 1
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    except SiYuanError as e:
        print(f"  ❌ Failed to export {doc_id}: {e}", file=sys.stderr)
        return None


def export_notebook(client, notebook_id, output_dir):
    """Export all documents from a notebook"""
    try:
        # 获取笔记本信息
        notebooks = client.list_notebooks()
        notebook_name = next((nb['name'] for nb in notebooks if nb['id'] == notebook_id), "unknown")
        
        # 创建笔记本导出目录
        safe_name = sanitize_filename(notebook_name)
        nb_dir = output_dir / safe_name
        nb_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📖 Exporting: {notebook_name}")
        
        # 获取所有文档
        docs = client.query_sql(f"""
            SELECT id, content FROM blocks 
            WHERE box = '{notebook_id}' AND type = 'd'
        """)
        
        exported = 0
        failed = 0
        
        for doc in docs:
            doc_id = doc.get('id')
            if not doc_id:
                continue
            
            result = export_document(client, doc_id, nb_dir, notebook_name)
            if result:
                print(f"  ✓ {Path(result).name}")
                exported += 1
            else:
                failed += 1
        
        return exported, failed
    except SiYuanError as e:
        print(f"❌ Error exporting notebook: {e}", file=sys.stderr)
        return 0, 0


def main():
    parser = argparse.ArgumentParser(
        description='Export SiYuan notes to Markdown',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 export.py -o ~/Documents/SiYuan-Backups
  python3 export.py -n "工作" -o ~/backup/
  python3 export.py -d 20240602141622-l7ou7t7 -o ~/doc.md
        """
    )
    parser.add_argument('--output', '-o', default='~/Documents/SiYuan-Export',
                        help='Output directory (default: ~/Documents/SiYuan-Export)')
    parser.add_argument('--notebook', '-n', help='Export specific notebook by name')
    parser.add_argument('--doc', '-d', help='Export single document by ID')
    
    args = parser.parse_args()
    
    # 设置输出路径
    output_dir = Path(args.output).expanduser()
    
    # 如果导出单个文档且输出路径以 .md 结尾，作为文件处理
    if args.doc and args.output.endswith('.md'):
        output_file = output_dir
        output_dir = output_file.parent
    else:
        output_file = None
        # 添加时间戳子目录
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = output_dir / f"export_{timestamp}"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        client = SiYuanClient()
    except SiYuanError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 执行导出
    if args.doc:
        # 导出单个文档
        if output_file:
            result = export_document(client, args.doc, output_file.parent)
            if result:
                # 重命名到指定文件名
                Path(result).rename(output_file)
                print(f"✅ Exported to: {output_file}")
        else:
            result = export_document(client, args.doc, output_dir)
            if result:
                print(f"✅ Exported to: {result}")
    else:
        # 导出笔记本
        total_exported = 0
        total_failed = 0
        
        notebooks = client.list_notebooks()
        
        if args.notebook:
            # 导出指定笔记本
            notebook = next((nb for nb in notebooks if nb['name'] == args.notebook), None)
            if not notebook:
                print(f"❌ Notebook not found: {args.notebook}", file=sys.stderr)
                sys.exit(1)
            
            if notebook.get('closed'):
                print(f"⚠️  Notebook '{args.notebook}' is closed, opening...")
                client.open_notebook(notebook['id'])
            
            exported, failed = export_notebook(client, notebook['id'], output_dir)
            total_exported += exported
            total_failed += failed
        else:
            # 导出所有打开的笔记本
            for notebook in notebooks:
                if notebook.get('closed'):
                    print(f"⏭️  Skipping closed notebook: {notebook['name']}")
                    continue
                
                exported, failed = export_notebook(client, notebook['id'], output_dir)
                total_exported += exported
                total_failed += failed
                print()
        
        # 保存清单
        manifest = {
            "exported_at": datetime.now().isoformat(),
            "siyuan_version": client.system_version(),
            "total_exported": total_exported,
            "total_failed": total_failed,
        }
        
        with open(output_dir / "manifest.json", 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        print("=" * 50)
        print(f"✅ Export complete!")
        print(f"   Total: {total_exported} documents")
        print(f"   Failed: {total_failed}")
        print(f"   Location: {output_dir}")


if __name__ == "__main__":
    main()
