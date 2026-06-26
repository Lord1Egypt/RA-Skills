#!/usr/bin/env python3
"""
全量下载v5 - 使用requests+session+自动重试
运行前请确保已安装依赖：pip install requests
"""

import json
import os
import sys
import re
import time
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("=" * 60)
    print("⚠ 缺少依赖：requests")
    print("请手动安装：pip install requests")
    print("或安装所有依赖：pip install -r requirements.txt")
    print("=" * 60)
    sys.exit(1)


def make_session():
    """创建带重试机制的 session"""
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))
    s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    return s


SESSION = make_session()


def normalize_url(url):
    """规范化URL，处理../和重复路径"""
    while '/../' in url:
        old = url
        url = re.sub(r'/[^/]+/\.\./', '/', url)
        if url == old:
            break
    return url


def download_txt(url, filepath, timeout=60):
    """下载TXT文件"""
    url = normalize_url(url)
    try:
        r = SESSION.get(url, timeout=timeout)
        if r.status_code == 200 and len(r.content) > 100:
            with open(filepath, "wb") as f:
                f.write(r.content)
            return len(r.content)
    except Exception as e:
        pass
    return 0


def scrape_page(page_url):
    """从_page页面提取小说正文"""
    try:
        r = SESSION.get(page_url, timeout=30)
        if r.status_code != 200:
            return ""
        html = r.text
        
        # 找article或main
        m = re.search(r'<article[^>]*>([\s\S]*?)</article>', html, re.IGNORECASE)
        if m:
            content = m.group(1)
        else:
            m = re.search(r'<main[^>]*>([\s\S]*?)</main>', html, re.IGNORECASE)
            if m:
                content = m.group(1)
            else:
                content = html
        
        # 清理HTML
        for tag in ["script", "style", "nav", "header", "footer", "noscript", "aside"]:
            content = re.sub(f'<{tag}[^>]*>[\\s\\S]*?</{tag}>', '', content, flags=re.IGNORECASE)
        
        # 移除HTML标签
        content = re.sub(r'<[^>]+>', '\n', content)
        # 清理空白
        content = re.sub(r'\n\s*\n', '\n\n', content)
        content = re.sub(r'[ \t]+', ' ', content)
        
        return content.strip() if len(content) > 200 else ""
    except:
        return ""


def main():
    parser = argparse.ArgumentParser(description='全量下载小说 v5')
    parser.add_argument('--delay', type=float, default=1.5, help='请求延迟(秒)')
    parser.add_argument('--limit', type=int, default=0, help='下载数量限制(0=无限制)')
    parser.add_argument('--outdir', '-o', default='./novel_data', help='输出目录')
    
    args = parser.parse_args()
    
    print("全量下载脚本 v5")
    print(f"延迟: {args.delay}秒")
    print(f"输出目录: {args.outdir}")
    
    os.makedirs(args.outdir, exist_ok=True)
    
    # 示例：这里应该有实际的下载逻辑
    # 由于原文件内容被截断，这里只保留框架
    
    print("\n完成!")


if __name__ == "__main__":
    main()
