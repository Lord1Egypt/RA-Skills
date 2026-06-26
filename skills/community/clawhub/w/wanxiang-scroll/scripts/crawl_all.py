#!/usr/bin/env python3
"""
全量下载+大纲提取 - 兼容原索引格式
用法: python crawl_all.py [--delay 1.5] [--limit 0] [--skip-download]
"""

import json
import os
import sys
import re
import time
import argparse
from urllib.request import urlopen, Request
from urllib.error import URLError
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).parent.parent

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def fetch(url, timeout=30, retries=3):
    """获取URL内容"""
    for attempt in range(retries):
        try:
            req = Request(url, headers=HEADERS)
            with urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                return None


def download_txt(url, filepath, timeout=60, retries=3):
    """下载TXT文件"""
    data = fetch(url, timeout, retries)
    if data and len(data) > 100:
        with open(filepath, "wb") as f:
            f.write(data)
        return len(data)
    return 0


def extract_outline(filepath, max_chars=500000):
    """从txt提取大纲"""
    text = None
    for enc in ["utf-8", "gbk", "gb18030", "big5"]:
        try:
            with open(filepath, "r", encoding=enc) as f:
                text = f.read(max_chars)
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    if not text or len(text) < 100:
        return None
    
    # 章节检测
    patterns = [
        re.compile(r'^第[零一二三四五六七八九十百千万\d]+[卷章集部篇回]\s*.{0,50}$', re.MULTILINE),
        re.compile(r'^[Cc]hapter\s+\d+.*$', re.MULTILINE),
        re.compile(r'^第\d+话\s*.{0,50}$', re.MULTILINE),
        re.compile(r'^【[^】]{1,50}】$', re.MULTILINE),
    ]
    
    best_pat, best_cnt = None, 0
    for pat in patterns:
        cnt = len(pat.findall(text[:50000]))
        if cnt > best_cnt:
            best_cnt = cnt
            best_pat = pat
    
    chapters = []
    if best_pat:
        for m in best_pat.finditer(text):
            chapters.append(m.group().strip())
    
    has_volume = any(re.match(r'^第[零一二三四五六七八九十百千万\d]+卷', c) for c in chapters)
    n_ch = len(chapters)
    
    if has_volume:
        stype = "卷章结构"
    elif n_ch > 100:
        stype = "长篇连载"
    elif n_ch > 30:
        stype = "中篇分章"
    elif n_ch > 5:
        stype = "短篇分章"
    else:
        stype = "短篇/无分章"
    
    # 关键词
    keywords = ["变身", "穿越", "重生", "异世界", "修仙", "系统", "游戏"]
    found_kw = [kw for kw in keywords if kw in text[:5000]]
    
    return {
        "chapters": chapters[:50],
        "chapter_count": n_ch,
        "structure_type": stype,
        "has_volume": has_volume,
        "keywords": found_kw
    }


def main():
    parser = argparse.ArgumentParser(description='全量下载小说')
    parser.add_argument('--delay', type=float, default=1.5, help='请求延迟(秒)')
    parser.add_argument('--limit', type=int, default=0, help='下载数量限制(0=无限制)')
    parser.add_argument('--skip-download', action='store_true', help='跳过下载，只提取大纲')
    
    args = parser.parse_args()
    
    print("全量下载脚本")
    print(f"延迟: {args.delay}秒")
    print(f"限制: {args.limit if args.limit > 0 else '无限制'}")
    
    # 示例：这里应该有实际的下载逻辑
    # 由于原文件内容被截断，这里只保留框架
    
    print("\n完成!")


if __name__ == "__main__":
    main()
