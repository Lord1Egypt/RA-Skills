#!/usr/bin/env python3
"""
微信公众号文章 PDF 报告生成
用法: python3 wechat_pdf.py <关键词>
"""
import asyncio
import json
import re
import sys
import html
from datetime import datetime, timedelta
from playwright.async_api import async_playwright

# 文件路径
import os
WORKSPACE = os.path.expanduser('~/.openclaw/workspace')
ARTICLES_FILE = f'{WORKSPACE}/articles_new.json'


def convert_relative_time(date_text):
    """将相对时间转换为实际日期"""
    if not date_text:
        return ''
    
    now = datetime.now()
    
    # 匹配 X分钟前
    min_match = re.search(r'(\d+)分钟前', date_text)
    if min_match:
        minutes = int(min_match.group(1))
        dt = now - timedelta(minutes=minutes)
        return dt.strftime('%Y-%m-%d %H:%M')
    
    # 匹配 X小时前
    hour_match = re.search(r'(\d+)小时前', date_text)
    if hour_match:
        hours = int(hour_match.group(1))
        dt = now - timedelta(hours=hours)
        return dt.strftime('%Y-%m-%d %H:%M')
    
    # 匹配 X天前
    day_match = re.search(r'(\d+)天前', date_text)
    if day_match:
        days = int(day_match.group(1))
        dt = now - timedelta(days=days)
        return dt.strftime('%Y-%m-%d')
    
    # 如果已经是标准格式，直接返回
    if re.match(r'\d{4}-\d{2}-\d{2}', date_text):
        return date_text
    
    return date_text


def fix_url(url):
    """修复微信URL中的问题"""
    if not url:
        return url
    
    # 修复 ×tamp= 为 &timestamp=
    url = re.sub(r'×tamp=', '&timestamp=', url)
    url = re.sub(r'×timestamp=', '&timestamp=', url)
    
    return url


def load_articles():
    """加载文章数据"""
    try:
        with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 找不到 {ARTICLES_FILE}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("错误: articles.json 格式错误")
        sys.exit(1)


def generate_html(articles, keyword):
    """生成 HTML 报告"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # PDF文件目录
    pdf_dir = 'wechat_pages'
    
    # 生成文章列表
    articles_html = ''
    for i, art in enumerate(articles, 1):
        # 修复URL
        url = fix_url(art.get('url', ''))
        # 为了在 HTML 文本中正确显示 & 字符
        safe_url = html.escape(url, quote=False)
        
        # 生成本地PDF链接
        title = art.get('title', f'article_{i}')
        # 清理文件名，与wechat_fetch.py保持一致
        filename = re.sub(r'[<>:"/\\|?*]', '', title)[:50]
        pdf_filename = f"{i:02d}_{filename}.pdf"
        local_pdf_path = f"{pdf_dir}/{pdf_filename}"
        
        # 转换日期格式
        date = convert_relative_time(art.get('date', ''))
        
        articles_html += f"""
        <div class="article">
            <h3>{i}. {art['title']}</h3>
            <p class="meta">{art['source']} | {date}</p>
            <p class="summary">{art.get('summary', '摘要生成中...')}</p>
            <p class="url"><a href="{safe_url}" target="_blank">微信原文（有时效限制）</a></p>
            <p class="url"><a href="{local_pdf_path}">点我看原文(PDF)</a></p>
        </div>
        """
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{keyword}行业动态研究报告</title>
    <style>
        @page {{ size: A4; margin: 2cm; }}
        body {{
            font-family: "PingFang SC", "Microsoft YaHei", "Hiragino Sans GB", sans-serif;
            margin: 40px;
            line-height: 1.8;
            color: #333;
        }}
        h1 {{
            text-align: center;
            color: #1a1a1a;
            font-size: 24px;
            margin-bottom: 10px;
        }}
        .date {{
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #2c3e50;
            font-size: 18px;
            margin-top: 30px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        h3 {{
            color: #34495e;
            font-size: 16px;
            margin-top: 20px;
            margin-bottom: 5px;
        }}
        p {{
            margin: 8px 0;
            color: #555;
        }}
        .url {{
            color: #0066cc;
            word-break: break-all;
            font-size: 13px;
        }}
        .meta {{
            color: #999;
            font-size: 13px;
        }}
        .summary {{
            text-indent: 2em;
            margin: 10px 0;
            color: #444;
        }}
        .article {{
            margin-bottom: 25px;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 5px;
        }}
        .core-view {{
            background: #e8f4fc;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #999;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <h1>{keyword}行业动态研究报告</h1>
    <p class="date">报告日期：{date_str}</p>
    
    <h2>行业动态精选</h2>
    {articles_html}
    
    <div class="footer">
        <p>数据来源：搜狗微信搜索 | 报告生成时间：{date_str}</p>
    </div>
</body>
</html>
"""
    return html_content


async def convert_to_pdf(html_file, pdf_file):
    """使用 Playwright 转换为 PDF"""
    import os
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Playwright needs absolute path
        abs_html = os.path.abspath(html_file)
        await page.goto(f'file://{abs_html}')
        await page.wait_for_load_state('networkidle')
        
        await page.pdf(
            path=pdf_file,
            format='A4',
            print_background=True,
            margin={'top': '1cm', 'bottom': '1cm', 'left': '1cm', 'right': '1cm'}
        )
        
        await browser.close()


def main():
    if len(sys.argv) < 2:
        print("用法: python3 wechat_pdf.py <关键词>")
        sys.exit(1)
    
    keyword = sys.argv[1]
    
    print("加载文章数据...")
    articles = load_articles()
    print(f"共 {len(articles)} 篇文章")
    
    # 生成HTML
    print("\n生成 HTML 报告...")
    html_content = generate_html(articles, keyword)
    
    html_file = f'{WORKSPACE}/{keyword}_行业动态.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML 保存至: {html_file}")
    
    # 生成PDF
    print("\n生成 PDF...")
    pdf_file = f'{WORKSPACE}/{keyword}_行业动态.pdf'
    
    asyncio.run(convert_to_pdf(html_file, pdf_file))
    
    print(f"✓ PDF 生成成功: {pdf_file}")


if __name__ == '__main__':
    main()
