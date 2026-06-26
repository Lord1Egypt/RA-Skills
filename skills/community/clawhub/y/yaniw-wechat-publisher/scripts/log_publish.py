#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记录发布日志
"""

import json
import os
from pathlib import Path
from datetime import datetime

def log_publish(base_dir, article_info):
    """记录发布日志"""
    
    # 获取日期
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 日志文件路径
    log_dir = Path(base_dir) / "articles" / today
    log_file = log_dir / "publish_log.json"
    
    # 确保目录存在
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 读取现有日志
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8') as f:
            log_data = json.load(f)
    else:
        log_data = {
            "date": today,
            "articles": [],
            "summary": {
                "total_articles": 0,
                "total_words": 0,
                "publish_success": 0,
                "publish_failed": 0
            }
        }
    
    # 添加新文章记录
    article_record = {
        "id": f"article_{today.replace('-', '')}_{len(log_data['articles']) + 1:03d}",
        "title": article_info.get('title', ''),
        "created_at": datetime.now().isoformat(),
        "status": article_info.get('status', 'published'),
        "media_id": article_info.get('media_id', ''),
        "cover_style": article_info.get('cover_style', 1),
        "published_at": datetime.now().isoformat(),
        "word_count": article_info.get('word_count', 0),
        "tags": article_info.get('tags', [])
    }
    
    log_data['articles'].append(article_record)
    
    # 更新统计
    log_data['summary']['total_articles'] += 1
    log_data['summary']['total_words'] += article_info.get('word_count', 0)
    if article_info.get('status') == 'published':
        log_data['summary']['publish_success'] += 1
    else:
        log_data['summary']['publish_failed'] += 1
    
    # 保存日志
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 发布日志已记录: {log_file}")
    return log_file

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("用法: python log_publish.py <base_dir> <article_json>")
        sys.exit(1)
    
    base_dir = sys.argv[1]
    article_json = json.loads(sys.argv[2])
    log_publish(base_dir, article_json)
