"""
爬虫引擎 - Crawler Engine
支持 Playwright 和 Requests 两种模式
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Union
import time
import random


class CrawlerEngine:
    """智能爬虫引擎"""
    
    DEFAULT_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    def __init__(self, use_proxy: bool = False, headless: bool = True, 
                 delay_range: tuple = (1, 3)):
        """
        初始化爬虫引擎
        
        Args:
            use_proxy: 是否使用代理
            headless: 是否无头模式
            delay_range: 请求延迟范围 (min, max) 秒
        """
        self.use_proxy = use_proxy
        self.headless = headless
        self.delay_range = delay_range
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)
        self._playwright_page = None
    
    def crawl(self, url: str, extract_rules: Dict[str, str] = None,
              method: str = 'static', **kwargs) -> Dict:
        """
        爬取网页
        
        Args:
            url: 目标URL
            extract_rules: 数据提取规则 {'字段名': 'xpath或css选择器'}
            method: 'static'(requests) 或 'dynamic'(playwright)
        
        Returns:
            提取的数据字典
        """
        # 添加随机延迟
        time.sleep(random.uniform(*self.delay_range))
        
        if method == 'dynamic':
            return self._crawl_dynamic(url, extract_rules)
        else:
            return self._crawl_static(url, extract_rules)
    
    def _crawl_static(self, url: str, extract_rules: Dict[str, str]) -> Dict:
        """静态爬取（使用 requests）"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            result = {'url': url, 'status_code': response.status_code, 'data': {}}
            
            if extract_rules:
                for field, selector in extract_rules.items():
                    elements = soup.select(selector)
                    result['data'][field] = [e.get_text(strip=True) for e in elements]
            
            return result
        except Exception as e:
            return {'url': url, 'error': str(e)}
    
    def _crawl_dynamic(self, url: str, extract_rules: Dict[str, str]) -> Dict:
        """动态爬取（使用 Playwright）"""
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = context.new_page()
                page.goto(url, wait_until='networkidle')
                
                result = {'url': url, 'data': {}}
                
                if extract_rules:
                    for field, selector in extract_rules.items():
                        try:
                            elements = page.query_selector_all(selector)
                            result['data'][field] = [e.inner_text() for e in elements]
                        except:
                            result['data'][field] = []
                
                browser.close()
                return result
        except Exception as e:
            return {'url': url, 'error': str(e)}
    
    def batch_crawl(self, urls: List[str], extract_rules: Dict[str, str],
                   max_workers: int = 5) -> List[Dict]:
        """批量爬取"""
        from concurrent.futures import ThreadPoolExecutor
        
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.crawl, url, extract_rules) 
                      for url in urls]
            for future in futures:
                results.append(future.result())
        return results
