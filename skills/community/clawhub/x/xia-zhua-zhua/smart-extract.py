#!/usr/bin/env python3
"""
smart-extract.py - AI 驱动内容提取
使用 readability-lxml 自动识别网页主内容区域

这是"教它识字"模式的实现：
不是给 AI 预设选择器，而是让它自己判断"这里是正文"
"""

import sys
import os
import json
import argparse
import tempfile
from readability import readability
from lxml import html, etree

def extract(url, html_content=None):
    """
    使用 readability 自动提取主内容
    返回: { title, content(html), text_content, excerpt }
    """
    if html_content:
        doc = html.fromstring(html_content.encode('utf-8', errors='replace'))
    else:
        # 从 URL 加载（仅用于调试，生产环境用 Playwright 获取 HTML）
        import urllib.request
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            html_content = resp.read()
        doc = html.fromstring(html_content)

    # readability 需要 document 对象
    doc_tree = readability.Document(html_content if html_content else doc.tobytes())

    try:
        title = doc_tree.title()
    except:
        title = ''

    try:
        content_html = doc_tree.summary().decode('utf-8', errors='replace')
    except:
        content_html = ''

    try:
        text = doc_tree.content()
    except:
        text = ''

    try:
        excerpt = doc_tree.short_title() or ''
    except:
        excerpt = ''

    # 返回结构化数据
    result = {
        'title': title.strip() if title else '',
        'content': content_html,
        'text_content': text.strip() if text else '',
        'excerpt': excerpt.strip() if excerpt else '',
    }

    return result


def main():
    parser = argparse.ArgumentParser(description='smart-extract - AI 内容提取')
    parser.add_argument('--url', required=True, help='网页 URL')
    parser.add_argument('--html-file', help='HTML 文件路径（可选）')
    parser.add_argument('--json', action='store_true', help='输出 JSON')
    args = parser.parse_args()

    html_content = None
    if args.html_file and os.path.exists(args.html_file):
        with open(args.html_file, 'r', encoding='utf-8', errors='replace') as f:
            html_content = f.read()

    result = extract(args.url, html_content)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"Title: {result['title']}")
        print(f"Excerpt: {result['excerpt']}")
        print(f"Content length: {len(result['content'])} chars")
        print(f"Text content length: {len(result['text_content'])} chars")


if __name__ == '__main__':
    main()
