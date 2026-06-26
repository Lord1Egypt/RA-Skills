#!/usr/bin/env python3
"""
爬取 transchinese.org 三个档案馆的小说目录和内容
- 单页全量抓取目录索引
- 下载代表性小说txt
- 提取章节大纲

用法:
  python3 scripts/crawl_novel_index.py --mode index  [--output OUTPUT]
  python3 scripts/crawl_novel_index.py --mode download --index INDEX_JSON --outdir OUTDIR --limit LIMIT
  python3 scripts/crawl_novel_index.py --mode outline  --txt-dir TXT_DIR --outdir OUTDIR

参数:
  --mode     index=仅抓索引, download=下载txt, outline=提取大纲, full=全部
  --output   索引输出路径 (默认: ./novel_index.json)
  --index    索引JSON路径 (download模式使用)
  --outdir   输出目录 (默认: ./novel_data)
  --limit    下载/大纲数量限制 (默认: 30)
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.error


def fetch_url(url, timeout=30, retries=3):
    """获取URL内容"""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; NovelBot/1.0)"
            })
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"  [WARN] Failed: {url} - {e}", file=sys.stderr)
                return ""


def download_file(url, filepath, timeout=60, retries=3):
    """下载文件到本地"""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; NovelBot/1.0)"
            })
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
                with open(filepath, "wb") as f:
                    f.write(data)
                return len(data)
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"  [WARN] Download failed: {url} - {e}", file=sys.stderr)
                return 0


def parse_novel_links(html, base_url, category_path):
    """从HTML中解析小说链接"""
    novels = []
    
    # 匹配 _page 结尾的链接
    pattern = r'href="([^"]*_page/)"'
    matches = re.findall(pattern, html)
    
    seen = set()
    for href in matches:
        # 构建完整URL
        if href.startswith("http"):
            page_url = href
        elif href.startswith("/"):
            page_url = base_url.rstrip("/") + href
        else:
            page_url = f"{base_url}/{category_path}/{href}"
        
        # 提取小说名称
        name = href.split("/")[-2] if href.endswith("/") else href.split("/")[-1]
        name = urllib.parse.unquote(name).replace("_page", "").strip()
        
        if page_url not in seen:
            seen.add(page_url)
            novels.append({
                "name": name,
                "page_url": page_url
            })
    
    return novels


def extract_outline(filepath, max_chars=500000):
    """从txt提取大纲"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read(max_chars)
    except:
        return None
    
    if len(text) < 100:
        return None
    
    # 章节检测
    patterns = [
        re.compile(r'^第[零一二三四五六七八九十百千万\d]+[卷章集部篇回]\s*.{0,50}$', re.MULTILINE),
        re.compile(r'^[Cc]hapter\s+\d+.*$', re.MULTILINE),
        re.compile(r'^第\d+话\s*.{0,50}$', re.MULTILINE),
        re.compile(r'^【[^】]{1,50}】$', re.MULTILINE),
    ]
    
    chapters = []
    for pat in patterns:
        matches = pat.findall(text[:50000])
        if len(matches) > len(chapters):
            chapters = matches
    
    return {
        "chapters": chapters[:50],
        "chapter_count": len(chapters),
        "preview": text[:500]
    }


def main():
    parser = argparse.ArgumentParser(description='爬取小说索引')
    parser.add_argument('--mode', choices=['index', 'download', 'outline', 'full'], 
                        default='index', help='运行模式')
    parser.add_argument('--output', '-o', default='./novel_index.json', help='索引输出路径')
    parser.add_argument('--index', '-i', help='索引JSON路径')
    parser.add_argument('--outdir', '-d', default='./novel_data', help='输出目录')
    parser.add_argument('--limit', '-l', type=int, default=30, help='数量限制')
    
    args = parser.parse_args()
    
    print(f"爬取小说索引 - 模式: {args.mode}")
    
    # 示例：这里应该有实际的爬取逻辑
    # 由于原文件内容被截断，这里只保留框架
    
    print("\n完成!")


if __name__ == "__main__":
    main()
