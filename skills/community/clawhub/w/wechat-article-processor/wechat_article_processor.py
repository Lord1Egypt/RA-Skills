#!/usr/bin/env python3
"""
微信公众号文章处理脚本

功能：
1. 用浏览器抓取微信公众号文章全文
2. 结构化整理内容
3. 保存到飞书文档

用法：
    python wechat_article_processor.py <文章链接>
"""

import re
import sys
import json
from pathlib import Path
from datetime import datetime


def extract_article_content(browser_output: str) -> dict:
    """从浏览器输出中提取文章内容"""
    
    # 提取标题
    title_match = re.search(r'heading "(.+?)" \[level=1\]', browser_output)
    title = title_match.group(1) if title_match else "未获取到标题"
    
    # 提取作者
    author_match = re.search(r'link "(.+?)" \[ref=', browser_output)
    author = author_match.group(1) if author_match else "未知"
    
    # 提取发布时间
    time_match = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日\s*\d{1,2}:\d{2})', browser_output)
    publish_time = time_match.group(1) if time_match else ""
    
    # 提取正文内容（所有 paragraph 文本）
    paragraphs = re.findall(r'paragraph \[ref=\w+\]:\s*\n?\s*generic \[ref=\w+\]:\s*\n?\s*(.+?)(?=\n\s*(?:paragraph|generic|heading|img|link|$))', 
                          browser_output, re.DOTALL)
    
    # 清理正文
    content_lines = []
    for p in paragraphs:
        # 清理多余空白
        p = re.sub(r'\s+', ' ', p).strip()
        if p and len(p) > 5:  # 过滤太短的
            content_lines.append(p)
    
    return {
        "title": title,
        "author": author,
        "publish_time": publish_time,
        "content": content_lines
    }


def format_as_markdown(article: dict) -> str:
    """将文章格式化为 Markdown"""
    
    md = f"# {article['title']}\n\n"
    
    if article['author']:
        md += f"> **作者**：{article['author']}  "
    if article['publish_time']:
        md += f"**发布时间**：{article['publish_time']}\n\n"
    
    md += "---\n\n"
    
    # 添加正文
    for para in article['content']:
        md += f"{para}\n\n"
    
    return md


def main():
    if len(sys.argv) < 2:
        print("用法：python wechat_article_processor.py <微信公众号链接>")
        sys.exit(1)
    
    url = sys.argv[1]
    
    print(f"正在处理：{url}")
    print("请使用 browser 工具打开链接并获取内容")
    print("然后调用本脚本进行解析")


if __name__ == "__main__":
    main()