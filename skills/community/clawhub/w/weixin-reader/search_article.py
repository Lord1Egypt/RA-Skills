#!/usr/bin/env python3
"""
搜索文章的其他来源
"""

import sys
import json
import re
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def search_google(query):
    """使用 Google 搜索"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        try:
            # 搜索
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            print(f"搜索: {search_url}")
            
            page.goto(search_url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(3000)
            
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # 提取搜索结果
            results = []
            
            # Google 搜索结果选择器
            for elem in soup.select('div.g, .yuRUbf'):
                link_elem = elem.select_one('a')
                title_elem = elem.select_one('h3')
                snippet_elem = elem.select_one('.VwiC3b, .s3v94d')
                
                if link_elem and title_elem:
                    url = link_elem.get('href', '')
                    title = title_elem.get_text(strip=True)
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                    
                    # 过滤掉 Google 自己的链接
                    if url and not url.startswith('/'):
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet[:200] if snippet else ''
                        })
            
            browser.close()
            
            return {
                'success': True,
                'query': query,
                'results_count': len(results),
                'results': results[:10]  # 返回前10个结果
            }
            
        except Exception as e:
            browser.close()
            return {'success': False, 'error': str(e)}


if __name__ == '__main__':
    query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'Playwright CLI Claude Code 傅红雪'
    result = search_google(query)
    print(json.dumps(result, ensure_ascii=False, indent=2))
