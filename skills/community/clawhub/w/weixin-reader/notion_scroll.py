#!/usr/bin/env python3
"""
滚动截取 Notion 页面完整内容
"""

import sys
from playwright.sync_api import sync_playwright

def scroll_and_capture(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            viewport={'width': 1280, 'height': 2000}  # 更高的视口
        )
        page = context.new_page()
        
        try:
            print(f"正在访问: {url}")
            page.goto(url, wait_until='domcontentloaded', timeout=60000)
            page.wait_for_timeout(10000)  # 等待 10 秒
            
            # 滚动页面加载更多内容
            for i in range(5):
                page.evaluate('window.scrollBy(0, 800)')
                page.wait_for_timeout(1000)
            
            # 回到顶部
            page.evaluate('window.scrollTo(0, 0)')
            page.wait_for_timeout(1000)
            
            # 截图
            screenshot_path = '~/.openclaw/workspace/notion_article_full.png'
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"完整截图已保存: {screenshot_path}")
            
            # 获取标题
            title = page.title()
            print(f"页面标题: {title}")
            
            # 获取文本内容
            text_content = page.evaluate('''() => {
                const elements = document.querySelectorAll('p, h1, h2, h3, li');
                return Array.from(elements).map(e => e.innerText).filter(t => t.length > 5);
            }''')
            
            browser.close()
            
            return {
                'success': True,
                'title': title,
                'content': text_content
            }
            
        except Exception as e:
            print(f"错误: {e}")
            browser.close()
            return {'success': False, 'error': str(e)}

if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://www.notion.so/Playwright-CLI-Claude-Code-1bd25b1f28234a45b69b3f5d75a595c1?source=copy_link'
    result = scroll_and_capture(url)
    
    if result['success']:
        print("\n=== 文章内容 ===\n")
        for i, text in enumerate(result['content'][:50], 1):  # 限制输出数量
            print(f"{i}. {text}")
    else:
        print(result)
