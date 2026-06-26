#!/usr/bin/env python3
"""
提取 Notion 页面内容
"""

import sys
import json
import re
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def clean_text(text):
    """清理文本内容"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_notion(url):
    """提取 Notion 页面内容"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()
        
        try:
            print(f"正在访问: {url}")
            page.goto(url, wait_until='domcontentloaded', timeout=60000)
            page.wait_for_timeout(8000)  # Notion 加载较慢，等待 8 秒
            
            # 获取页面标题
            title = page.title()
            print(f"页面标题: {title}")
            
            # 获取 HTML
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # 提取标题（Notion 页面标题通常在 h1）
            article_title = ""
            h1_elem = soup.find('h1')
            if h1_elem:
                article_title = clean_text(h1_elem.get_text())
            
            # 提取正文内容
            content = []
            
            # Notion 的内容通常在特定结构中
            # 尝试多种选择器
            content_selectors = [
                '[data-block-id]',
                '.notion-page-content',
                'article',
                'main',
                '[class*="content"]'
            ]
            
            for selector in content_selectors:
                elems = soup.select(selector)
                if elems:
                    for elem in elems:
                        # 获取所有文本块
                        for block in elem.find_all(['p', 'h1', 'h2', 'h3', 'li', 'blockquote']):
                            text = clean_text(block.get_text())
                            if text and len(text) > 5:
                                content.append(text)
                    if len(content) > 5:  # 如果找到了足够的内容，就停止
                        break
            
            # 如果没有找到内容，尝试通用方法
            if not content:
                body = soup.find('body')
                if body:
                    for elem in body.find_all(['p', 'h1', 'h2', 'h3', 'li']):
                        text = clean_text(elem.get_text())
                        if text and len(text) > 10:
                            content.append(text)
            
            # 去重并保持顺序
            seen = set()
            unique_content = []
            for text in content:
                if text not in seen and text != article_title:
                    seen.add(text)
                    unique_content.append(text)
            
            browser.close()
            
            return {
                'success': True,
                'url': url,
                'page_title': title,
                'article_title': article_title,
                'content': '\n\n'.join(unique_content[:100]),  # 限制段落数
                'paragraph_count': len(unique_content)
            }
            
        except Exception as e:
            print(f"错误: {e}")
            browser.close()
            return {'success': False, 'error': str(e), 'url': url}


if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://www.notion.so/Playwright-CLI-Claude-Code-1bd25b1f28234a45b69b3f5d75a595c1'
    result = extract_notion(url)
    print(json.dumps(result, ensure_ascii=False, indent=2))
