#!/usr/bin/env python3
"""
截图调试 Notion 页面
"""

import sys
from playwright.sync_api import sync_playwright

def screenshot_notion(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()
        
        try:
            print(f"正在访问: {url}")
            # Notion 可能需要更长的加载时间
            page.goto(url, wait_until='domcontentloaded', timeout=60000)
            page.wait_for_timeout(10000)  # 等待 10 秒让内容加载
            
            # 截图
            screenshot_path = '/tmp/notion_page.png'
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"截图已保存: {screenshot_path}")
            
            # 获取标题
            title = page.title()
            print(f"页面标题: {title}")
            
            browser.close()
            return {'success': True, 'screenshot': screenshot_path, 'title': title}
            
        except Exception as e:
            print(f"错误: {e}")
            # 错误截图
            try:
                page.screenshot(path='/tmp/notion_error.png')
                print(f"错误截图: /tmp/notion_error.png")
            except:
                pass
            browser.close()
            return {'success': False, 'error': str(e)}

if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://www.notion.so/Playwright-CLI-Claude-Code-1bd25b1f28234a45b69b3f5d75a595c1'
    result = screenshot_notion(url)
    print(result)
