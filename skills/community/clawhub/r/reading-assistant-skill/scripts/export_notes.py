#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多格式导出脚本
支持导出为 Markdown、HTML、PDF 格式
"""

import sys
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


def export_to_markdown(book_data: Dict, include_analysis: bool = True) -> str:
    """
    导出为 Markdown 格式
    
    参数:
        book_data: 书籍数据
        include_analysis: 是否包含深层分析
    
    返回:
        Markdown 格式的文本
    """
    book_info = book_data.get("book_info", {})
    excerpts = book_data.get("excerpts", [])
    
    # 按章节组织
    chapters = {}
    for excerpt in excerpts:
        chapter = excerpt.get("chapter") or "未分类"
        if chapter not in chapters:
            chapters[chapter] = []
        chapters[chapter].append(excerpt)
    
    # 生成 Markdown
    md_lines = []
    
    # 标题
    md_lines.append(f"# {book_info.get('title', '未知书名')}")
    md_lines.append("")
    
    # 元信息
    if book_info.get("author"):
        md_lines.append(f"**作者**: {book_info['author']}")
    if book_info.get("tags"):
        md_lines.append(f"**标签**: {', '.join(book_info['tags'])}")
    md_lines.append(f"**创建时间**: {book_info.get('created_at', '未知')}")
    md_lines.append(f"**摘录数量**: {len(excerpts)}")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    
    # 目录
    md_lines.append("## 目录")
    md_lines.append("")
    for chapter in chapters.keys():
        md_lines.append(f"- [{chapter}](#{chapter.replace(' ', '-')})")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    
    # 章节内容
    for chapter, chapter_excerpts in chapters.items():
        md_lines.append(f"## {chapter}")
        md_lines.append("")
        
        for i, excerpt in enumerate(chapter_excerpts, 1):
            # 摘录内容
            md_lines.append(f"### 摘录 {i}")
            md_lines.append("")
            md_lines.append(f"> {excerpt.get('content', '')}")
            md_lines.append("")
            
            # 标签
            if excerpt.get("tags"):
                md_lines.append(f"**标签**: {', '.join(excerpt['tags'])}")
                md_lines.append("")
            
            # 深层分析
            if include_analysis and excerpt.get("deep_meaning"):
                md_lines.append("**深层含义**:")
                md_lines.append("")
                md_lines.append(excerpt["deep_meaning"])
                md_lines.append("")
            
            # 应用建议
            if include_analysis and excerpt.get("application"):
                md_lines.append("**应用建议**:")
                md_lines.append("")
                md_lines.append(excerpt["application"])
                md_lines.append("")
            
            md_lines.append("---")
            md_lines.append("")
    
    return '\n'.join(md_lines)


def export_to_html(book_data: Dict, include_analysis: bool = True) -> str:
    """
    导出为 HTML 格式
    
    参数:
        book_data: 书籍数据
        include_analysis: 是否包含深层分析
    
    返回:
        HTML 格式的文本
    """
    book_info = book_data.get("book_info", {})
    excerpts = book_data.get("excerpts", [])
    
    # 按章节组织
    chapters = {}
    for excerpt in excerpts:
        chapter = excerpt.get("chapter") or "未分类"
        if chapter not in chapters:
            chapters[chapter] = []
        chapters[chapter].append(excerpt)
    
    # 生成 HTML
    html_lines = []
    
    # HTML 头部
    html_lines.append('<!DOCTYPE html>')
    html_lines.append('<html lang="zh-CN">')
    html_lines.append('<head>')
    html_lines.append('    <meta charset="UTF-8">')
    html_lines.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_lines.append(f'    <title>{book_info.get("title", "读书笔记")}</title>')
    html_lines.append('    <style>')
    html_lines.append('        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; color: #333; }')
    html_lines.append('        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }')
    html_lines.append('        h2 { color: #34495e; margin-top: 30px; }')
    html_lines.append('        h3 { color: #7f8c8d; }')
    html_lines.append('        blockquote { background: #f9f9f9; border-left: 5px solid #3498db; padding: 10px 20px; margin: 20px 0; }')
    html_lines.append('        .tag { display: inline-block; background: #3498db; color: white; padding: 3px 10px; border-radius: 15px; font-size: 0.9em; margin-right: 5px; }')
    html_lines.append('        .meta { color: #95a5a6; font-size: 0.9em; margin-bottom: 20px; }')
    html_lines.append('        .excerpt { margin-bottom: 30px; padding: 20px; background: #fff; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }')
    html_lines.append('        .analysis { background: #ecf0f1; padding: 15px; border-radius: 5px; margin-top: 15px; }')
    html_lines.append('    </style>')
    html_lines.append('</head>')
    html_lines.append('<body>')
    
    # 标题
    html_lines.append(f'    <h1>{book_info.get("title", "未知书名")}</h1>')
    html_lines.append('    <div class="meta">')
    if book_info.get("author"):
        html_lines.append(f'        <strong>作者:</strong> {book_info["author"]} | ')
    if book_info.get("tags"):
        html_lines.append(f'        <strong>标签:</strong> {", ".join(book_info["tags"])} | ')
    html_lines.append(f'        <strong>摘录数量:</strong> {len(excerpts)}')
    html_lines.append('    </div>')
    
    # 目录
    html_lines.append('    <h2>目录</h2>')
    html_lines.append('    <ul>')
    for chapter in chapters.keys():
        html_lines.append(f'        <li><a href="#{chapter.replace(" ", "-")}">{chapter}</a></li>')
    html_lines.append('    </ul>')
    
    # 章节内容
    for chapter, chapter_excerpts in chapters.items():
        html_lines.append(f'    <h2 id="{chapter.replace(" ", "-")}">{chapter}</h2>')
        
        for i, excerpt in enumerate(chapter_excerpts, 1):
            html_lines.append('    <div class="excerpt">')
            html_lines.append(f'        <h3>摘录 {i}</h3>')
            html_lines.append(f'        <blockquote>{excerpt.get("content", "")}</blockquote>')
            
            # 标签
            if excerpt.get("tags"):
                html_lines.append('        <div>')
                for tag in excerpt["tags"]:
                    html_lines.append(f'            <span class="tag">{tag}</span>')
                html_lines.append('        </div>')
            
            # 深层分析
            if include_analysis and excerpt.get("deep_meaning"):
                html_lines.append('        <div class="analysis">')
                html_lines.append('            <strong>深层含义:</strong>')
                html_lines.append(f'            <p>{excerpt["deep_meaning"]}</p>')
                html_lines.append('        </div>')
            
            # 应用建议
            if include_analysis and excerpt.get("application"):
                html_lines.append('        <div class="analysis">')
                html_lines.append('            <strong>应用建议:</strong>')
                html_lines.append(f'            <p>{excerpt["application"]}</p>')
                html_lines.append('        </div>')
            
            html_lines.append('    </div>')
    
    html_lines.append('</body>')
    html_lines.append('</html>')
    
    return '\n'.join(html_lines)


def export_notes(
    book_name: str,
    format: str = "markdown",
    output_path: Optional[str] = None,
    include_analysis: bool = True,
    base_path: str = "./reading-notes"
) -> Dict[str, any]:
    """
    导出笔记
    
    参数:
        book_name: 书籍名称
        format: 导出格式（markdown/html/pdf）
        output_path: 输出路径（可选）
        include_analysis: 是否包含深层分析
        base_path: 笔记存储路径
    
    返回:
        {
            "success": True/False,
            "output_path": "输出文件路径",
            "format": "格式",
            "excerpt_count": 摘录数量,
            "error": "错误信息（如果失败）"
        }
    """
    try:
        # 加载书籍档案
        book_file = os.path.join(base_path, "books", f"{book_name}.json")
        
        if not os.path.exists(book_file):
            return {
                "success": False,
                "error": f"书籍档案不存在: {book_name}"
            }
        
        with open(book_file, 'r', encoding='utf-8') as f:
            book_data = json.load(f)
        
        # 确定输出路径
        if not output_path:
            export_dir = os.path.join(base_path, "exports")
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)
            
            ext = "md" if format == "markdown" else "html" if format == "html" else "pdf"
            output_path = os.path.join(export_dir, f"{book_name}.{ext}")
        
        # 导出
        if format == "markdown":
            content = export_to_markdown(book_data, include_analysis)
        elif format == "html":
            content = export_to_html(book_data, include_analysis)
        elif format == "pdf":
            # PDF 需要额外依赖，这里先生成 HTML，提示用户使用浏览器打印
            content = export_to_html(book_data, include_analysis)
            output_path = output_path.replace('.pdf', '.html')
            # 实际应用中可以使用 weasyprint 等库生成 PDF
        else:
            return {
                "success": False,
                "error": f"不支持的格式: {format}"
            }
        
        # 保存文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "output_path": output_path,
            "format": format,
            "excerpt_count": len(book_data.get("excerpts", []))
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"导出失败: {str(e)}"
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='笔记导出工具')
    parser.add_argument('book_name', help='书籍名称')
    parser.add_argument('--format', '-f', choices=['markdown', 'html', 'pdf'],
                       default='markdown', help='导出格式')
    parser.add_argument('--output', '-o', help='输出路径')
    parser.add_argument('--no-analysis', action='store_true', help='不包含深层分析')
    parser.add_argument('--base-path', default='./reading-notes', help='笔记存储路径')
    
    args = parser.parse_args()
    
    result = export_notes(
        book_name=args.book_name,
        format=args.format,
        output_path=args.output,
        include_analysis=not args.no_analysis,
        base_path=args.base_path
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
