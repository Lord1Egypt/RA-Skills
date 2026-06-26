#!/usr/bin/env python3
"""
全量下载v4 - 双策略：优先下载txt，失败则从_page页面提取正文
用法: python crawl_all_v4.py [--delay 2] [--workers 5]
"""

import json
import os
import sys
import re
import time
import argparse
from urllib.request import urlopen, Request
from urllib.parse import unquote
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = Path(__file__).parent.parent

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

sys.stdout.reconfigure(line_buffering=True)


def fetch(url, timeout=30, retries=3):
    """获取URL内容"""
    for attempt in range(retries):
        try:
            req = Request(url, headers=HEADERS)
            with urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1.5 * (attempt + 1))
            else:
                return None


def fetch_text(url, **kw):
    """获取URL文本内容"""
    data = fetch(url, **kw)
    if data:
        return data.decode("utf-8", errors="replace")
    return ""


def save_novel(name, content, txt_dir):
    """保存小说内容到txt"""
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', name)[:80]
    out_path = os.path.join(txt_dir, f"{safe_name}.txt")
    if isinstance(content, str):
        content = content.encode("utf-8")
    with open(out_path, "wb") as f:
        f.write(content)
    return len(content)


def try_download_txt(novel, txt_dir):
    """策略1: 直接下载txt文件"""
    name = novel.get("name", novel.get("title", ""))
    txt_url = novel.get("txt_url", "")
    
    if txt_url:
        data = fetch(txt_url, timeout=60, retries=2)
        if data and len(data) > 200:
            return save_novel(name, data, txt_dir), "txt"
    
    return 0, "fail"


def try_scrape_page(novel, txt_dir):
    """策略2: 从_page页面提取小说正文"""
    name = novel.get("name", novel.get("title", ""))
    page_url = novel.get("page_url", "")
    
    if not page_url:
        return 0, "fail"
    
    html = fetch_text(page_url, timeout=30, retries=2)
    if not html:
        return 0, "fail"
    
    # 提取正文
    content = ""
    
    # 方法1: 找article标签
    m = re.search(r'<article[^>]*>([\s\S]*?)</article>', html, re.IGNORECASE)
    if m:
        content = m.group(1)
    else:
        # 方法2: 找main标签
        m = re.search(r'<main[^>]*>([\s\S]*?)</main>', html, re.IGNORECASE)
        if m:
            content = m.group(1)
    
    if content:
        # 清理HTML标签
        content = re.sub(r'<[^>]+>', '', content)
        content = re.sub(r'\s+', '\n', content).strip()
        
        if len(content) > 200:
            return save_novel(name, content, txt_dir), "scrape"
    
    return 0, "fail"


def main():
    parser = argparse.ArgumentParser(description='全量下载小说 v4')
    parser.add_argument('--delay', type=float, default=2, help='请求延迟(秒)')
    parser.add_argument('--workers', type=int, default=5, help='并发数')
    
    args = parser.parse_args()
    
    print("全量下载脚本 v4")
    print(f"延迟: {args.delay}秒")
    print(f"并发: {args.workers}")
    
    # 示例：这里应该有实际的下载逻辑
    # 由于原文件内容被截断，这里只保留框架
    
    print("\n完成!")


if __name__ == "__main__":
    main()
