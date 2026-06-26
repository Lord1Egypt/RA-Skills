#!/usr/bin/env python3
"""
使用 Playwright Stealth 模式的通用文章提取器
尝试绕过知乎等平台的反爬检测
"""

import sys
import json
import re
from playwright.sync_api import sync_playwright
from playwright_stealth.stealth import Stealth
from bs4 import BeautifulSoup


def clean_text(text):
    """清理文本内容"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_zhihu(soup):
    """提取知乎文章"""
    title = ""
    for selector in ['h1.Post-Title', 'h1', '[data-zop-title]', '.Title']:
        elem = soup.select_one(selector)
        if elem:
            title = clean_text(elem.get_text())
            if title:
                break
    
    author = ""
    for selector in ['.AuthorInfo-name', '.UserLink-link', '.author']:
        elem = soup.select_one(selector)
        if elem:
            author = clean_text(elem.get_text())
            if author:
                break
    
    content = ""
    for selector in ['.Post-RichTextContainer', '.RichContent-inner', 'article', '.content']:
        elem = soup.select_one(selector)
        if elem:
            for script in elem(['script', 'style', 'iframe']):
                script.decompose()
            paragraphs = []
            for p in elem.find_all(['p', 'h2', 'h3', 'li', 'blockquote']):
                text = clean_text(p.get_text())
                if text and len(text) > 5:
                    paragraphs.append(text)
            if paragraphs:
                content = '\n\n'.join(paragraphs)
                break
    
    return {'title': title, 'author': author, 'content': content}


def extract_with_stealth(url):
    """使用 stealth 模式提取文章"""
    
    with sync_playwright() as p:
        # 启动浏览器（非无头模式更容易绕过检测）
        browser = p.chromium.launch(
            headless=True,  # 可以尝试改为 False 看是否有区别
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
            ]
        )
        
        # 创建上下文，模拟真实浏览器
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
            permissions=['notifications'],
        )
        
        page = context.new_page()
        
        # 应用 stealth 模式
        Stealth().apply_stealth_sync(page)
        
        try:
            print(f"正在访问: {url}")
            
            # 先访问知乎首页建立会话
            page.goto('https://www.zhihu.com', wait_until='domcontentloaded', timeout=15000)
            page.wait_for_timeout(2000)
            
            # 再访问目标文章
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(5000)  # 等待内容渲染
            
            # 获取页面信息
            title = page.title()
            print(f"页面标题: {title}")
            
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # 检查是否被拦截
            error_elem = soup.select_one('pre')
            if error_elem and 'error' in error_elem.get_text().lower():
                error_text = error_elem.get_text()
                print(f"访问被拦截: {error_text[:200]}")
                browser.close()
                return {'success': False, 'error': '被反爬机制拦截', 'title': title}
            
            # 提取内容
            data = extract_zhihu(soup)
            
            # 截图保存（用于调试）
            screenshot_path = '/tmp/zhihu_stealth.png'
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"截图已保存: {screenshot_path}")
            
            browser.close()
            
            return {
                'success': True,
                'url': url,
                'page_title': title,
                **data,
                'content_length': len(data.get('content', '')),
                'screenshot': screenshot_path
            }
            
        except Exception as e:
            print(f"错误: {e}")
            # 尝试截图看发生了什么
            try:
                page.screenshot(path='/tmp/zhihu_error.png', full_page=True)
                print(f"错误截图: /tmp/zhihu_error.png")
            except:
                pass
            browser.close()
            return {'success': False, 'error': str(e), 'url': url}


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'error': '请提供文章链接'}, ensure_ascii=False))
        sys.exit(1)
    
    url = sys.argv[1]
    result = extract_with_stealth(url)
    print(json.dumps(result, ensure_ascii=False, indent=2))
