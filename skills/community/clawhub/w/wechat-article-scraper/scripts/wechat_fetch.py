#!/usr/bin/env python3
"""
微信文章抓取脚本 - PDF格式
用法: python3 wechat_fetch.py <关键词>
功能: 读取 articles_new.json，抓取每篇文章保存为PDF到本地
"""
import asyncio
import json
import os
import re
import sys
import time
from datetime import datetime
from playwright.async_api import async_playwright

WORKSPACE = os.path.expanduser('~/.openclaw/workspace')
ARTICLES_FILE = f'{WORKSPACE}/articles_new.json'
OUTPUT_DIR = f'{WORKSPACE}/wechat_pages'


def load_articles():
    """加载文章数据"""
    try:
        with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 找不到 {ARTICLES_FILE}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("错误: articles_new.json 格式错误")
        sys.exit(1)


def sanitize_filename(title):
    """清理文件名，移除非法字符"""
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    return title[:50]


async def fetch_article(page, url, title, index):
    """抓取单篇文章为PDF"""
    print(f"[{index}] 抓取: {title[:30]}...")
    
    try:
        await page.goto(url, wait_until='networkidle')
        
        # 等待页面渲染完成
        await page.wait_for_timeout(2000)
        
        # 生成文件名
        filename = sanitize_filename(f"{index:02d}_{title}")
        filepath = f'{OUTPUT_DIR}/{filename}.pdf'
        
        # 保存为PDF（保留完整样式）
        await page.pdf(
            path=filepath,
            format='A4',
            print_background=True,
            margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'}
        )
        
        print(f"    ✓ 已保存: {filepath}")
        return True
        
    except Exception as e:
        print(f"    ✗ 失败: {e}")
        return False


async def main():
    if len(sys.argv) < 2:
        print("用法: python3 wechat_fetch.py <关键词>")
        sys.exit(1)
    
    keyword = sys.argv[1]
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 加载文章
    print("加载文章数据...")
    articles = load_articles()
    print(f"共 {len(articles)} 篇文章\n")
    
    # 启动浏览器
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 创建桌面版页面
        context = await browser.new_context(
            viewport={'width': 1200, 'height': 800}
        )
        page = await context.new_page()
        
        success = 0
        for i, art in enumerate(articles, 1):
            url = art.get('url', '')
            title = art.get('title', f'article_{i}')
            
            if url:
                if await fetch_article(page, url, title, i):
                    success += 1
                
                # 每个文章之间间隔2秒，避免请求过快
                time.sleep(2)
        
        await browser.close()
    
    print(f"\n完成! 成功抓取 {success}/{len(articles)} 篇文章")
    print(f"保存位置: {OUTPUT_DIR}/")


if __name__ == '__main__':
    asyncio.run(main())
