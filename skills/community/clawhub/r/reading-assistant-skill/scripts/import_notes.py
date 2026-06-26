#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量导入脚本
支持从微信读书、Kindle等平台导入笔记
"""

import sys
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


def parse_wechat_export(file_path: str) -> Dict[str, any]:
    """
    解析微信读书导出文件
    
    支持格式：
    1. 纯文本格式（每条摘录以换行分隔）
    2. CSV格式
    
    返回:
        {
            "success": True/False,
            "excerpts": [摘录列表],
            "count": 摘录数量,
            "error": "错误信息（如果失败）"
        }
    """
    try:
        excerpts = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 微信读书导出格式：通常包含章节标题和划线内容
        # 格式示例：
        # 第一章 标题
        # 这是划线内容...
        # ◆ 这也是划线内容
        
        lines = content.split('\n')
        current_chapter = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检测章节标题
            chapter_match = re.match(r'^第[一二三四五六七八九十\d]+[章节回部篇]', line)
            if chapter_match:
                # 保存之前的摘录
                if current_content:
                    excerpts.append({
                        "content": '\n'.join(current_content),
                        "chapter": current_chapter,
                        "source": "wechat"
                    })
                    current_content = []
                
                current_chapter = line
                continue
            
            # 检测划线内容（微信读书用◆标记）
            if line.startswith('◆'):
                if current_content:
                    excerpts.append({
                        "content": '\n'.join(current_content),
                        "chapter": current_chapter,
                        "source": "wechat"
                    })
                    current_content = []
                
                current_content.append(line[1:].strip())  # 去掉◆
            else:
                # 普通内容
                current_content.append(line)
        
        # 保存最后一条
        if current_content:
            excerpts.append({
                "content": '\n'.join(current_content),
                "chapter": current_chapter,
                "source": "wechat"
            })
        
        return {
            "success": True,
            "excerpts": excerpts,
            "count": len(excerpts)
        }
        
    except Exception as e:
        return {
            "success": False,
            "excerpts": [],
            "count": 0,
            "error": f"解析微信读书文件失败: {str(e)}"
        }


def parse_kindle_export(file_path: str) -> Dict[str, any]:
    """
    解析Kindle导出文件
    
    支持格式：
    1. My Clippings.txt（Kindle设备导出）
    2. CSV格式（Kindle App导出）
    
    返回:
        同 parse_wechat_export
    """
    try:
        excerpts = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Kindle My Clippings.txt 格式
        # 每条笔记格式：
        # 书名 (作者)
        # - 您在位置 #123-125 的标注 | 添加于 2024年1月1日星期一
        # 
        # 摘录内容...
        # ==========
        
        if '==========' in content:
            # My Clippings.txt 格式
            notes = content.split('==========')
            
            for note in notes:
                if not note.strip():
                    continue
                
                lines = note.strip().split('\n')
                if len(lines) < 3:
                    continue
                
                # 解析书名和作者
                book_line = lines[0].strip()
                # 提取位置信息
                location_match = re.search(r'位置 #(\d+)', lines[1]) if len(lines) > 1 else None
                location = location_match.group(1) if location_match else None
                
                # 提取内容（从第3行开始）
                content_lines = lines[2:]
                note_content = '\n'.join(content_lines).strip()
                
                if note_content:
                    excerpts.append({
                        "content": note_content,
                        "chapter": f"位置 {location}" if location else None,
                        "source": "kindle"
                    })
        else:
            # 尝试CSV格式
            import csv
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    content = row.get('Highlight', row.get('Text', ''))
                    chapter = row.get('Chapter', row.get('Location', ''))
                    
                    if content:
                        excerpts.append({
                            "content": content,
                            "chapter": chapter if chapter else None,
                            "source": "kindle"
                        })
        
        return {
            "success": True,
            "excerpts": excerpts,
            "count": len(excerpts)
        }
        
    except Exception as e:
        return {
            "success": False,
            "excerpts": [],
            "count": 0,
            "error": f"解析Kindle文件失败: {str(e)}"
        }


def import_notes(
    file_path: str,
    source_type: str = "wechat",
    book_name: Optional[str] = None,
    preview_only: bool = True
) -> Dict[str, any]:
    """
    批量导入笔记
    
    参数:
        file_path: 导入文件路径
        source_type: 来源类型（wechat/kindle）
        book_name: 书籍名称（可选，从文件中提取）
        preview_only: 是否仅预览（不保存）
    
    返回:
        {
            "success": True/False,
            "preview": {
                "total_count": 总数,
                "chapters": {"章节名": 数量},
                "sample": [示例摘录]
            },
            "imported_count": 导入数量（如果已保存）,
            "error": "错误信息（如果失败）"
        }
    """
    try:
        # 解析文件
        if source_type == "wechat":
            parse_result = parse_wechat_export(file_path)
        elif source_type == "kindle":
            parse_result = parse_kindle_export(file_path)
        else:
            return {
                "success": False,
                "error": f"不支持的来源类型: {source_type}"
            }
        
        if not parse_result["success"]:
            return parse_result
        
        excerpts = parse_result["excerpts"]
        
        # 生成预览
        chapters = {}
        for excerpt in excerpts:
            chapter = excerpt.get("chapter") or "未分类"
            chapters[chapter] = chapters.get(chapter, 0) + 1
        
        preview = {
            "total_count": len(excerpts),
            "chapters": chapters,
            "sample": excerpts[:3]  # 前3条作为示例
        }
        
        if preview_only:
            return {
                "success": True,
                "preview": preview,
                "imported_count": 0
            }
        
        # 保存到书籍档案
        base_path = "./reading-notes"
        books_dir = os.path.join(base_path, "books")
        
        if not os.path.exists(books_dir):
            os.makedirs(books_dir)
        
        # 如果没有指定书名，从文件名提取
        if not book_name:
            book_name = Path(file_path).stem
        
        book_path = os.path.join(books_dir, f"{book_name}.json")
        
        # 加载或创建书籍档案
        if os.path.exists(book_path):
            with open(book_path, 'r', encoding='utf-8') as f:
                book_data = json.load(f)
        else:
            book_data = {
                "book_info": {
                    "title": book_name,
                    "author": None,
                    "status": "reading",
                    "created_at": datetime.now().strftime("%Y-%m-%d"),
                    "tags": []
                },
                "excerpts": []
            }
        
        # 添加摘录（带时间戳和ID）
        for excerpt in excerpts:
            excerpt["id"] = f"exc_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(book_data['excerpts'])}"
            excerpt["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            excerpt["tags"] = []
            book_data["excerpts"].append(excerpt)
        
        # 保存
        with open(book_path, 'w', encoding='utf-8') as f:
            json.dump(book_data, f, ensure_ascii=False, indent=2)
        
        return {
            "success": True,
            "preview": preview,
            "imported_count": len(excerpts)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"导入失败: {str(e)}"
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='笔记批量导入工具')
    parser.add_argument('file_path', help='导入文件路径')
    parser.add_argument('--source', '-s', choices=['wechat', 'kindle'], 
                       default='wechat', help='来源类型')
    parser.add_argument('--book', '-b', help='书籍名称')
    parser.add_argument('--save', action='store_true', help='保存到档案（默认仅预览）')
    
    args = parser.parse_args()
    
    result = import_notes(
        file_path=args.file_path,
        source_type=args.source,
        book_name=args.book,
        preview_only=not args.save
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
