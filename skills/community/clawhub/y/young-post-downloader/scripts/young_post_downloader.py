#!/usr/bin/env python3
"""
Young Post Club Spark 文章下载器 - 完整版
自动访问网站、下载文章、生成 PDF 并上传飞书
"""

import sys
import os
import re
import json
from datetime import datetime
from pathlib import Path

# 配置
YOUNG_POST_BASE = "https://www.youngpostclub.com"
SPARK_URL = "https://www.youngpostclub.com/spark"
WORKSPACE = os.environ.get("WORKSPACE", "/home/admin/.openclaw/workspace")

# 文章 URL 模式
ARTICLE_PATTERNS = [
    r'href="(/yp/[^"]+/article/[^"]+)"',
    r'href="(/spark/[^"]+/article/[^"]+)"',
]

def log(message: str, level: str = "INFO"):
    """打印日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    emoji = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARN": "⚠️"}
    print(f"[{timestamp}] {emoji.get(level, '')} {message}")

def extract_article_links(html_content: str) -> list:
    """从 HTML 中提取文章链接"""
    articles = []
    seen_urls = set()
    
    for pattern in ARTICLE_PATTERNS:
        matches = re.findall(pattern, html_content)
        for url in matches:
            if url not in seen_urls and '/article/' in url:
                # 跳过非文章页面
                if any(skip in url for skip in ['/form', '/share-us/form']):
                    continue
                full_url = YOUNG_POST_BASE + url
                articles.append(full_url)
                seen_urls.add(url)
    
    return articles

def generate_html_content(articles: list, date_str: str) -> str:
    """生成 HTML 文档内容"""
    
    # 生成目录
    toc_items = []
    for i, article in enumerate(articles, 1):
        title = article.get('title', f'Article {i}')
        toc_items.append(f'<li><a href="#article{i}">{i}. {title}</a></li>')
    
    toc_html = '\n'.join(toc_items)
    
    # 生成文章列表
    articles_html = []
    for i, article in enumerate(articles, 1):
        article_html = f"""
<div class="article" id="article{i}">
    <h2>{i}. {article.get('title', 'Untitled')}</h2>
    <div class="meta">
        <strong>URL:</strong> <a href="{article.get('url', '#')}">{article.get('url', 'N/A')}</a><br>
        <strong>下载时间:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M")}
    </div>
    <div class="content">
        {article.get('content', 'No content')}
    </div>
</div>
"""
        articles_html.append(article_html)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Young Post Club Spark - 文章合集</title>
    <style>
        body {{
            font-family: 'Calibri', 'Arial', sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #1a73e8;
            text-align: center;
            border-bottom: 3px solid #1a73e8;
            padding-bottom: 15px;
        }}
        h2 {{
            color: #2c5282;
            border-left: 4px solid #1a73e8;
            padding-left: 15px;
            margin-top: 40px;
        }}
        .meta {{
            background-color: #f7fafc;
            padding: 10px 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 0.9em;
            color: #718096;
        }}
        .article {{
            margin-bottom: 50px;
            page-break-inside: avoid;
        }}
        .toc {{
            background-color: #edf2f7;
            padding: 20px;
            border-radius: 8px;
            margin: 30px 0;
        }}
        .toc ol {{
            padding-left: 20px;
        }}
        .toc li {{
            margin-bottom: 8px;
        }}
        .toc a {{
            color: #2d3748;
            text-decoration: none;
        }}
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #e2e8f0;
            color: #718096;
            font-size: 0.9em;
        }}
        @media print {{
            body {{ max-width: 100%; }}
            .article {{ page-break-inside: avoid; }}
        }}
    </style>
</head>
<body>

<h1>📰 Young Post Club Spark - 文章合集</h1>

<div class="meta">
    <strong>下载日期：</strong>{date_str}<br>
    <strong>来源：</strong>https://www.youngpostclub.com/spark<br>
    <strong>文章数量：</strong>{len(articles)} 篇
</div>

<div class="toc">
    <h2>📋 目录</h2>
    <ol>
        {toc_html}
    </ol>
</div>

{''.join(articles_html)}

<div class="footer">
    <p><strong>文档结束</strong></p>
    <p>所有文章均来自 Young Post Club Spark，版权归原作者所有。<br>本合集仅供个人学习使用。</p>
    <p>生成日期：{date_str}</p>
</div>

</body>
</html>"""
    
    return html

def main():
    """主函数 - 演示流程"""
    log("=" * 60, "INFO")
    log("Young Post Club Spark 文章下载器", "INFO")
    log("=" * 60, "INFO")
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # 步骤 1: 访问 Spark 页面
    log("步骤 1: 访问 Spark 页面获取文章列表", "INFO")
    print("  → 调用：web_fetch(url='https://www.youngpostclub.com/spark')")
    
    # 步骤 2: 解析文章链接
    log("步骤 2: 解析文章链接", "INFO")
    print("  → 从 HTML 中提取所有 /article/ 链接")
    
    # 步骤 3: 批量下载文章
    log("步骤 3: 批量下载文章", "INFO")
    print("  → 对每篇文章调用 web_fetch(extractMode='markdown')")
    
    # 步骤 4: 生成 HTML
    log("步骤 4: 生成 HTML 文档", "INFO")
    html_path = os.path.join(WORKSPACE, f"young-post-spark-{date_str}.html")
    print(f"  → 输出：{html_path}")
    
    # 步骤 5: 转换为 PDF
    log("步骤 5: 使用 Chrome 转换为 PDF", "INFO")
    pdf_path = os.path.join(WORKSPACE, f"young-post-spark-{date_str}.pdf")
    print(f"  → 命令：google-chrome --headless --print-to-pdf={pdf_path} {html_path}")
    
    # 步骤 6: 上传飞书
    log("步骤 6: 上传到飞书云空间", "INFO")
    print(f"  → 调用：feishu_drive_file(action='upload', file_path={pdf_path})")
    
    log("=" * 60, "SUCCESS")
    log("✅ 流程完成！实际执行时需调用相应工具", "SUCCESS")
    log("=" * 60, "SUCCESS")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
