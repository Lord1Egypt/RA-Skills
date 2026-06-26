"""
Smart Crawler - 单元测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from crawler import Crawler
from batch_crawler import BatchCrawler


class TestCrawler(unittest.TestCase):
    """测试基础爬虫"""
    
    def setUp(self):
        self.crawler = Crawler(delay_range=(0, 0))
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.crawler)
        self.assertEqual(self.crawler.timeout, 30)
    
    def test_extract(self):
        """测试数据提取"""
        html = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Hello World</h1>
                <p class='price'>$100</p>
            </body>
        </html>
        """
        
        data = self.crawler.extract(html, {
            'title': 'title::text',
            'heading': 'h1::text',
            'price': '.price::text'
        })
        
        self.assertEqual(data['title'], 'Test Page')
        self.assertEqual(data['heading'], 'Hello World')
        self.assertEqual(data['price'], '$100')
    
    def test_extract_xpath(self):
        """测试XPath提取"""
        html = """
        <html><body>
            <div class='item'>Item 1</div>
            <div class='item'>Item 2</div>
        </body></html>
        """
        
        data = self.crawler.extract(html, {
            'items': "//div[@class='item']/text()"
        })
        
        self.assertIsNotNone(data['items'])


class TestBatchCrawler(unittest.TestCase):
    """测试批量爬虫"""
    
    def test_init(self):
        """测试初始化"""
        batch = BatchCrawler(concurrent=3)
        self.assertEqual(batch.concurrent, 3)
    
    def test_get_stats(self):
        """测试统计信息"""
        batch = BatchCrawler()
        stats = batch.get_stats()
        self.assertEqual(stats['success'], 0)
        self.assertEqual(stats['failed'], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
