#!/usr/bin/env python3
"""
调试版提取器 - 保存截图和 HTML 用于分析
"""

import sys
import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def debug_page(url, output_dir='/tmp'):
    """调试页面，保存截图和 HTML"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()
        
        try:
            print(f"正在访问: {url}")
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            page.wait_for_timeout(5000)  # 等待 5 秒
            
            # 截图
            screenshot_path = f"{output_dir}/debug_zhihu.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"截图已保存: {screenshot_path}")
            
            # 保存 HTML
            html = page.content()
            html_path = f"{output_dir}/debug_zhihu.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"HTML 已保存: {html_path}")
            
            # 简单分析
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title')
            print(f"页面标题: {title.get_text() if title else '无'}")
            
            # 查找可能的内容区域
            selectors = ['article', 'main', '.Post-content', '.RichContent', '[class*="content"]']
            for sel in selectors:
                elems = soup.select(sel)
                print(f"选择器 '{sel}': 找到 {len(elems)} 个元素")
            
            browser.close()
            return {'success': True, 'screenshot': screenshot_path, 'html': html_path}
            
        except Exception as e:
            print(f"错误: {e}")
            browser.close()
            return {'success': False, 'error': str(e)}


if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://zhuanlan.zhihu.com/p/2010717224810353568'
    result = debug_page(url)
    print(json.dumps(result, indent=2))
