#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阅读统计脚本
生成阅读统计报告
"""

import sys
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Optional
from pathlib import Path


def get_book_stats(book_data: Dict) -> Dict:
    """
    获取单本书的统计数据
    
    参数:
        book_data: 书籍数据
    
    返回:
        统计数据字典
    """
    book_info = book_data.get("book_info", {})
    excerpts = book_data.get("excerpts", [])
    
    stats = {
        "title": book_info.get("title", "未知书名"),
        "author": book_info.get("author"),
        "status": book_info.get("status", "reading"),
        "created_at": book_info.get("created_at"),
        "excerpt_count": len(excerpts),
        "chapters": set(),
        "tags": Counter(),
        "daily_counts": defaultdict(int),
        "sources": Counter()
    }
    
    for excerpt in excerpts:
        # 章节统计
        chapter = excerpt.get("chapter")
        if chapter:
            stats["chapters"].add(chapter)
        
        # 标签统计
        tags = excerpt.get("tags", [])
        stats["tags"].update(tags)
        
        # 日期统计
        created_at = excerpt.get("created_at")
        if created_at:
            # 提取日期部分
            date_str = created_at.split(" ")[0] if " " in created_at else created_at
            stats["daily_counts"][date_str] += 1
        
        # 来源统计
        source = excerpt.get("source", "manual")
        stats["sources"][source] += 1
    
    # 转换 set 为 list 以便 JSON 序列化
    stats["chapters"] = list(stats["chapters"])
    stats["chapter_count"] = len(stats["chapters"])
    stats["tags"] = dict(stats["tags"].most_common(10))  # Top 10 标签
    stats["daily_counts"] = dict(sorted(stats["daily_counts"].items()))
    stats["sources"] = dict(stats["sources"])
    
    return stats


def get_overall_stats(base_path: str = "./reading-notes") -> Dict[str, any]:
    """
    获取所有书籍的统计数据
    
    参数:
        base_path: 笔记存储根目录
    
    返回:
        {
            "success": True/False,
            "stats": {
                "total_books": 书籍总数,
                "books_by_status": {"reading": X, "completed": Y, "archived": Z},
                "total_excerpts": 总摘录数,
                "books": [每本书的统计],
                "all_tags": Counter,
                "reading_days": 阅读天数
            },
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
        
        book_files = [f for f in os.listdir(books_dir) if f.endswith('.json')]
        
        all_stats = []
        books_by_status = defaultdict(int)
        total_excerpts = 0
        all_tags = Counter()
        all_dates = set()
        
        for book_file in book_files:
            book_path = os.path.join(books_dir, book_file)
            
            with open(book_path, 'r', encoding='utf-8') as f:
                book_data = json.load(f)
            
            stats = get_book_stats(book_data)
            all_stats.append(stats)
            
            books_by_status[stats["status"]] += 1
            total_excerpts += stats["excerpt_count"]
            all_tags.update(stats["tags"])
            all_dates.update(stats["daily_counts"].keys())
        
        # 生成报告
        report = {
            "total_books": len(book_files),
            "books_by_status": dict(books_by_status),
            "total_excerpts": total_excerpts,
            "books": all_stats,
            "all_tags": dict(all_tags.most_common(20)),
            "reading_days": len(all_dates),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return {
            "success": True,
            "stats": report
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"统计失败: {str(e)}"
        }


def generate_reading_report(book_name: str, base_path: str = "./reading-notes") -> Dict[str, any]:
    """
    生成单本书的阅读报告
    
    参数:
        book_name: 书籍名称
        base_path: 笔记存储路径
    
    返回:
        {
            "success": True/False,
            "report": {
                "book_info": 书籍信息,
                "statistics": 统计数据,
                "timeline": 时间线,
                "tag_cloud": 标签云,
                "chapters": 章节分布
            },
            "error": "错误信息（如果失败）"
        }
    """
    try:
        book_file = os.path.join(base_path, "books", f"{book_name}.json")
        
        if not os.path.exists(book_file):
            return {
                "success": False,
                "error": f"书籍档案不存在: {book_name}"
            }
        
        with open(book_file, 'r', encoding='utf-8') as f:
            book_data = json.load(f)
        
        stats = get_book_stats(book_data)
        
        # 生成章节分布
        excerpts = book_data.get("excerpts", [])
        chapter_dist = Counter()
        for excerpt in excerpts:
            chapter = excerpt.get("chapter", "未分类")
            chapter_dist[chapter] += 1
        
        # 生成时间线（最近7天）
        timeline = []
        today = datetime.now()
        for i in range(7):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            count = stats["daily_counts"].get(date, 0)
            timeline.append({
                "date": date,
                "count": count
            })
        timeline.reverse()
        
        report = {
            "book_info": book_data.get("book_info", {}),
            "statistics": {
                "excerpt_count": stats["excerpt_count"],
                "chapter_count": stats["chapter_count"],
                "tag_count": len(stats["tags"]),
                "reading_days": len(stats["daily_counts"])
            },
            "timeline": timeline,
            "tag_cloud": stats["tags"],
            "chapter_distribution": dict(chapter_dist.most_common(10)),
            "sources": stats["sources"],
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return {
            "success": True,
            "report": report
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"生成报告失败: {str(e)}"
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='阅读统计工具')
    parser.add_argument('--book', '-b', help='指定书籍名称（不指定则统计所有书籍）')
    parser.add_argument('--base-path', default='./reading-notes', help='笔记存储路径')
    
    args = parser.parse_args()
    
    if args.book:
        result = generate_reading_report(args.book, args.base_path)
    else:
        result = get_overall_stats(args.base_path)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
