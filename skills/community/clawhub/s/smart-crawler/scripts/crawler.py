"""
Crawler - 基础爬虫
"""

import requests
import time
import random
from typing import Dict, Optional, List, Union
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Crawler:
    """基础爬虫类"""
    
    def __init__(self, proxy_pool: Optional[List[str]] = None,
                 delay_range: tuple = (0, 0),
                 timeout: int = 30,
                 max_retries: int = 3):
        self.proxy_pool = proxy_pool or []
        self.delay_range = delay_range
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
    
    def _get_proxy(self) -> Optional[Dict[str, str]]:
        """获取随机代理"""
        if not self.proxy_pool:
            return None
        proxy = random.choice(self.proxy_pool)
        return {'http': proxy, 'https': proxy}
    
    def _apply_delay(self):
        """应用延迟"""
        if self.delay_range[1] > 0:
            delay = random.uniform(*self.delay_range)
            time.sleep(delay)
    
    def fetch(self, url: str, **kwargs) -> str:
        """获取页面内容"""
        self._apply_delay()
        
        headers = kwargs.pop('headers', self.headers)
        proxy = self._get_proxy()
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    url,
                    headers=headers,
                    proxies=proxy,
                    timeout=self.timeout,
                    **kwargs
                )
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                return response.text
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"请求失败: {url}, 错误: {e}")
                time.sleep(2 ** attempt)  # 指数退避
        return ""
    
    def extract(self, html: str, rules: Dict[str, str]) -> Dict[str, Union[str, List[str]]]:
        """提取数据
        
        Args:
            html: HTML内容
            rules: 提取规则，格式为 {名称: 选择器}
                  支持 XPath (//开头) 和 CSS Selector
        """
        soup = BeautifulSoup(html, 'lxml')
        results = {}
        
        for name, selector in rules.items():
            try:
                if selector.startswith('//'):
                    # XPath
                    from lxml import etree
                    tree = etree.HTML(html)
                    elements = tree.xpath(selector)
                    if elements:
                        if isinstance(elements[0], str):
                            results[name] = elements[0] if len(elements) == 1 else elements
                        else:
                            results[name] = [e.text for e in elements]
                    else:
                        results[name] = None
                elif '::' in selector:
                    # CSS Selector with pseudo-element
                    parts = selector.split('::')
                    css_sel = parts[0]
                    attr = parts[1] if len(parts) > 1 else 'text'
                    
                    elements = soup.select(css_sel)
                    if elements:
                        if attr == 'text':
                            values = [e.get_text(strip=True) for e in elements]
                        else:
                            values = [e.get(attr, '') for e in elements]
                        results[name] = values[0] if len(values) == 1 else values
                    else:
                        results[name] = None
                else:
                    # CSS Selector
                    elements = soup.select(selector)
                    if elements:
                        values = [e.get_text(strip=True) for e in elements]
                        results[name] = values[0] if len(values) == 1 else values
                    else:
                        results[name] = None
            except Exception as e:
                results[name] = None
                print(f"提取失败 {name}: {e}")
        
        return results
    
    def json_extract(self, data: Union[str, Dict], path: str) -> Any:
        """JSONPath 提取"""
        import json
        from jsonpath_ng import parse
        
        if isinstance(data, str):
            data = json.loads(data)
        
        jsonpath_expression = parse(path)
        matches = jsonpath_expression.find(data)
        return [match.value for match in matches] if len(matches) > 1 else (matches[0].value if matches else None)
    
    def download(self, url: str, save_path: str, **kwargs) -> str:
        """下载文件"""
        self._apply_delay()
        
        proxy = self._get_proxy()
        response = self.session.get(
            url,
            headers=self.headers,
            proxies=proxy,
            timeout=self.timeout,
            stream=True,
            **kwargs
        )
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return save_path


if __name__ == '__main__':
    # 测试
    crawler = Crawler(delay_range=(1, 2))
    html = crawler.fetch('https://httpbin.org/html')
    
    data = crawler.extract(html, {
        'title': 'title::text',
        'heading': 'h1::text'
    })
    print(data)
