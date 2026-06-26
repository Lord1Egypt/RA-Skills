"""
Batch Crawler - 批量爬虫
"""

from typing import List, Dict, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from scripts.crawler import Crawler
import time


class BatchCrawler:
    """批量爬虫"""
    
    def __init__(self, concurrent: int = 5, delay_range: tuple = (0.5, 1.5),
                 proxy_pool: Optional[List[str]] = None):
        self.concurrent = concurrent
        self.delay_range = delay_range
        self.proxy_pool = proxy_pool
        self.crawler = Crawler(
            proxy_pool=proxy_pool,
            delay_range=(0, 0)  # 外部控制延迟
        )
        self.results: List[Dict] = []
        self.errors: List[Dict] = []
    
    def crawl(self, urls: List[str], extract_rules: Optional[Dict] = None,
              callback: Optional[Callable] = None) -> List[Dict]:
        """
        批量爬取
        
        Args:
            urls: URL列表
            extract_rules: 数据提取规则
            callback: 回调函数，每个URL处理完成后调用
        
        Returns:
            爬取结果列表
        """
        self.results = []
        self.errors = []
        
        with ThreadPoolExecutor(max_workers=self.concurrent) as executor:
            future_to_url = {
                executor.submit(self._fetch_one, url, extract_rules, callback): url
                for url in urls
            }
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    if result:
                        self.results.append(result)
                except Exception as e:
                    self.errors.append({'url': url, 'error': str(e)})
                    print(f"爬取失败 {url}: {e}")
        
        return self.results
    
    def _fetch_one(self, url: str, extract_rules: Optional[Dict],
                   callback: Optional[Callable]) -> Optional[Dict]:
        """爬取单个URL"""
        try:
            # 应用延迟
            import random
            time.sleep(random.uniform(*self.delay_range))
            
            html = self.crawler.fetch(url)
            
            result = {'url': url, 'html': html}
            
            # 提取数据
            if extract_rules:
                data = self.crawler.extract(html, extract_rules)
                result['data'] = data
            
            # 调用回调
            if callback:
                callback(result)
            
            return result
        except Exception as e:
            self.errors.append({'url': url, 'error': str(e)})
            return None
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'success': len(self.results),
            'failed': len(self.errors),
            'total': len(self.results) + len(self.errors)
        }
    
    def save_results(self, path: str, format: str = 'json'):
        """保存结果"""
        import json
        import pandas as pd
        
        if format == 'json':
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
        elif format == 'csv':
            df = pd.DataFrame(self.results)
            df.to_csv(path, index=False)
        
        print(f"结果已保存: {path}")


if __name__ == '__main__':
    # 测试
    urls = [
        'https://httpbin.org/html',
        'https://httpbin.org/html',
    ]
    
    batch = BatchCrawler(concurrent=2, delay_range=(1, 2))
    results = batch.crawl(urls, extract_rules={
        'title': 'title::text'
    })
    
    print(f"成功: {batch.get_stats()}")
    for r in results:
        print(r.get('data'))
