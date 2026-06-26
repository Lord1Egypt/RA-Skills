"""
Dynamic Crawler - 动态页面爬虫 (基于 Playwright)
"""

from typing import Dict, Optional, Any
from playwright.sync_api import sync_playwright


class DynamicCrawler:
    """动态页面爬虫"""
    
    def __init__(self, headless: bool = True, browser: str = 'chromium'):
        self.headless = headless
        self.browser_type = browser
        self.playwright = None
        self.browser = None
        self.context = None
    
    def _init_browser(self):
        """初始化浏览器"""
        if self.playwright is None:
            self.playwright = sync_playwright().start()
            
            if self.browser_type == 'chromium':
                browser = self.playwright.chromium
            elif self.browser_type == 'firefox':
                browser = self.playwright.firefox
            else:
                browser = self.playwright.webkit
            
            self.browser = browser.launch(headless=self.headless)
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
    
    def fetch(self, url: str, wait_for: Optional[str] = None,
              wait_time: int = 3, actions: Optional[list] = None) -> str:
        """
        获取动态页面内容
        
        Args:
            url: 目标URL
            wait_for: 等待的CSS选择器
            wait_time: 等待时间(秒)
            actions: 页面操作列表
        
        Returns:
            页面HTML内容
        """
        self._init_browser()
        page = self.context.new_page()
        
        try:
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # 执行自定义操作
            if actions:
                for action in actions:
                    if action['type'] == 'click':
                        page.click(action['selector'])
                    elif action['type'] == 'type':
                        page.fill(action['selector'], action['text'])
                    elif action['type'] == 'scroll':
                        page.evaluate('window.scrollBy(0, window.innerHeight)')
                    page.wait_for_timeout(500)
            
            # 等待特定元素
            if wait_for:
                page.wait_for_selector(wait_for, timeout=wait_time * 1000)
            else:
                page.wait_for_timeout(wait_time * 1000)
            
            html = page.content()
            return html
        finally:
            page.close()
    
    def extract(self, html: str, rules: Dict[str, str]) -> Dict[str, Any]:
        """提取数据"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, 'lxml')
        results = {}
        
        for name, selector in rules.items():
            try:
                elements = soup.select(selector)
                if elements:
                    values = [e.get_text(strip=True) for e in elements]
                    results[name] = values[0] if len(values) == 1 else values
                else:
                    results[name] = None
            except Exception as e:
                results[name] = None
        
        return results
    
    def screenshot(self, url: str, save_path: str, full_page: bool = True):
        """页面截图"""
        self._init_browser()
        page = self.context.new_page()
        
        try:
            page.goto(url, wait_until='networkidle')
            page.screenshot(path=save_path, full_page=full_page)
            print(f"截图已保存: {save_path}")
        finally:
            page.close()
    
    def close(self):
        """关闭浏览器"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()


if __name__ == '__main__':
    # 测试
    crawler = DynamicCrawler()
    html = crawler.fetch('https://httpbin.org/html', wait_time=2)
    
    data = crawler.extract(html, {
        'title': 'title',
        'heading': 'h1'
    })
    print(data)
    
    crawler.close()
