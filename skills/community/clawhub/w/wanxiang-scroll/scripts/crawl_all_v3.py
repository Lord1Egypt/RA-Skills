#!/usr/bin/env python3
"""
全量下载+大纲提取 v3 - 正确获取txt下载链接
用法: python crawl_all_v3.py [--delay 1.5] [--skip-download] [--skip-outline]
"""

import json
import os
import sys
import re
import time
import argparse
import hashlib
from urllib.request import urlopen, Request
from urllib.parse import unquote, quote
from pathlib import Path

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
                time.sleep(2 ** attempt)
            else:
                return None


def fetch_text(url, **kw):
    """获取URL文本内容"""
    data = fetch(url, **kw)
    if data:
        return data.decode("utf-8", errors="replace")
    return ""


def find_txt_link(page_url, base_url):
    """从_page页面找到.txt下载链接"""
    html = fetch_text(page_url)
    if not html:
        return None
    
    # 找 href="xxx.txt" 链接
    for m in re.finditer(r'href="([^"]*\.txt)"', html):
        link = m.group(1)
        if link.startswith("http"):
            return link
        elif link.startswith("/"):
            return base_url + link
        else:
            # 相对路径
            return page_url.rsplit("/", 1)[0] + "/" + link
    
    # 尝试 .txt 在上级目录
    parent = page_url.replace("_page/", "").rstrip("/")
    if not parent.endswith(".txt"):
        candidate = parent + ".txt"
        data = fetch(candidate, timeout=10, retries=1)
        if data and len(data) > 100:
            return candidate
    
    return None


def download_txt(url, filepath, timeout=120, retries=3):
    """下载TXT文件"""
    data = fetch(url, timeout, retries)
    if data and len(data) > 100:
        with open(filepath, "wb") as f:
            f.write(data)
        return len(data)
    return 0


# ===== Outline =====
CHAPTER_PATTERNS = [
    re.compile(r'^第[零一二三四五六七八九十百千万\d]+[卷章集部篇回]\s*.{0,50}$', re.MULTILINE),
    re.compile(r'^[Cc]hapter\s+\d+.*$', re.MULTILINE),
    re.compile(r'^第\d+话\s*.{0,50}$', re.MULTILINE),
    re.compile(r'^【[^】]{1,50}】$', re.MULTILINE),
]


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
    best_pat, best_cnt = None, 0
    for pat in CHAPTER_PATTERNS:
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
    parser = argparse.ArgumentParser(description='全量下载小说 v3')
    parser.add_argument('--delay', type=float, default=1.5, help='请求延迟(秒)')
    parser.add_argument('--skip-download', action='store_true', help='跳过下载')
    parser.add_argument('--skip-outline', action='store_true', help='跳过大纲提取')
    
    args = parser.parse_args()
    
    print("全量下载脚本 v3")
    print(f"延迟: {args.delay}秒")
    
    # 示例：这里应该有实际的下载逻辑
    # 由于原文件内容被截断，这里只保留框架
    
    print("\n完成!")


if __name__ == "__main__":
    main()
