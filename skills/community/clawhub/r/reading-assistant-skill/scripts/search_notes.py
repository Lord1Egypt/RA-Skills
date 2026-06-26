#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
笔记搜索脚本
支持关键词搜索、标签筛选、章节筛选
"""

import sys
import json
import os
import re
from typing import Dict, List, Optional
from pathlib import Path


def load_book_data(book_path: str) -> Dict:
    """加载书籍档案"""
    try:
        with open(book_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}


def search_in_excerpt(excerpt: Dict, keyword: str, case_sensitive: bool = False) -> Dict:
    """
    在单条摘录中搜索关键词
    
    返回:
        {
            "matched": True/False,
            "content_highlight": "高亮后的内容",
            "match_fields": ["匹配的字段列表"]
        }
    """
    if not keyword:
        return {
            "matched": True,
            "content_highlight": excerpt.get("content", ""),
            "match_fields": []
        }
    
    flags = 0 if case_sensitive else re.IGNORECASE
    keyword_pattern = re.compile(re.escape(keyword), flags)
    
    matched = False
    match_fields = []
    content_highlight = excerpt.get("content", "")
    
    # 在内容中搜索
    if keyword_pattern.search(content_highlight):
        matched = True
        match_fields.append("content")
        # 高亮关键词
        content_highlight = keyword_pattern.sub(
            f'**{keyword}**',
            content_highlight
        )
    
    # 在深层含义中搜索
    if excerpt.get("deep_meaning") and keyword_pattern.search(excerpt["deep_meaning"]):
        matched = True
        match_fields.append("deep_meaning")
    
    # 在应用建议中搜索
    if excerpt.get("application") and keyword_pattern.search(excerpt["application"]):
        matched = True
        match_fields.append("application")
    
    # 在标签中搜索
    tags = excerpt.get("tags", [])
    if any(keyword.lower() in tag.lower() for tag in tags):
        matched = True
        match_fields.append("tags")
    
    return {
        "matched": matched,
        "content_highlight": content_highlight,
        "match_fields": match_fields
    }


def search_notes(
    base_path: str = "./reading-notes",
    keyword: Optional[str] = None,
    book_name: Optional[str] = None,
    tag: Optional[str] = None,
    chapter: Optional[str] = None,
    case_sensitive: bool = False
) -> Dict[str, any]:
    """
    搜索笔记
    
    参数:
        base_path: 笔记存储根目录
        keyword: 搜索关键词
        book_name: 指定书籍名称
        tag: 按标签筛选
        chapter: 按章节筛选
        case_sensitive: 是否区分大小写
    
    返回:
        {
            "success": True/False,
            "total_count": 总匹配数,
            "results": [
                {
                    "book_name": "书名",
                    "excerpt": {摘录详情},
                    "content_highlight": "高亮内容",
                    "match_fields": ["匹配字段"]
                }
            ],
            "error": "错误信息（如果失败）"
        }
    """
    try:
        books_dir = os.path.join(base_path, "books")
        
        if not os.path.exists(books_dir):
            return {
                "success": False,
                "error": f"笔记目录不存在: {books_dir}"
            }
        
        results = []
        
        # 确定要搜索的书籍
        if book_name:
            # 搜索指定书籍
            book_files = [f"{book_name}.json"]
        else:
            # 搜索所有书籍
            book_files = [f for f in os.listdir(books_dir) if f.endswith('.json')]
        
        for book_file in book_files:
            book_path = os.path.join(books_dir, book_file)
            book_data = load_book_data(book_path)
            
            if "error" in book_data:
                continue
            
            book_title = book_data.get("book_info", {}).get("title", book_file.replace('.json', ''))
            excerpts = book_data.get("excerpts", [])
            
            for excerpt in excerpts:
                # 章节筛选
                if chapter:
                    excerpt_chapter = excerpt.get("chapter", "")
                    if chapter.lower() not in excerpt_chapter.lower():
                        continue
                
                # 标签筛选
                if tag:
                    excerpt_tags = excerpt.get("tags", [])
                    if not any(tag.lower() in t.lower() for t in excerpt_tags):
                        continue
                
                # 关键词搜索
                search_result = search_in_excerpt(excerpt, keyword, case_sensitive)
                
                if search_result["matched"]:
                    results.append({
                        "book_name": book_title,
                        "excerpt": excerpt,
                        "content_highlight": search_result["content_highlight"],
                        "match_fields": search_result["match_fields"]
                    })
        
        return {
            "success": True,
            "total_count": len(results),
            "results": results
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"搜索失败: {str(e)}"
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='笔记搜索工具')
    parser.add_argument('--keyword', '-k', help='搜索关键词')
    parser.add_argument('--book', '-b', help='指定书籍名称')
    parser.add_argument('--tag', '-t', help='按标签筛选')
    parser.add_argument('--chapter', '-c', help='按章节筛选')
    parser.add_argument('--case-sensitive', action='store_true', help='区分大小写')
    parser.add_argument('--base-path', default='./reading-notes', help='笔记存储路径')
    
    args = parser.parse_args()
    
    result = search_notes(
        base_path=args.base_path,
        keyword=args.keyword,
        book_name=args.book,
        tag=args.tag,
        chapter=args.chapter,
        case_sensitive=args.case_sensitive
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
