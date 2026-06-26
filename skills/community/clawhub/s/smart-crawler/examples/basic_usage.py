"""
Smart Crawler - 基本使用示例
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from crawler import Crawler
from batch_crawler import BatchCrawler
from dynamic_crawler import DynamicCrawler


def demo_basic_crawler():
    """演示基础爬虫"""
    print("=" * 50)
    print("基础爬虫示例")
    print("=" * 50)
    
    # 初始化爬虫
    print("\n1. 初始化爬虫并设置延迟...")
    crawler = Crawler(delay_range=(0.5, 1.0))
    
    # 获取页面
    print("\n2. 获取测试页面...")
    try:
        html = crawler.fetch('https://httpbin.org/html')
        print(f"   页面长度: {len(html)} 字符")
        
        # 提取数据
        print("\n3. 提取数据...")
        data = crawler.extract(html, {
            'title': 'title::text',
            'heading': 'h1::text'
        })
        print(f"   标题: {data.get('title')}")
        print(f"   标题: {data.get('heading')}")
    except Exception as e:
        print(f"   请求失败: {e}")


def demo_batch_crawler():
    """演示批量爬虫"""
    print("\n" + "=" * 50)
    print("批量爬虫示例")
    print("=" * 50)
    
    # 准备URL列表
    urls = [
        'https://httpbin.org/html',
        'https://httpbin.org/html',
        'https://httpbin.org/html',
    ]
    
    print(f"\n1. 准备批量爬取 {len(urls)} 个页面...")
    
    # 批量爬取
    print("\n2. 开始批量爬取...")
    batch = BatchCrawler(concurrent=2, delay_range=(0.5, 1.0))
    
    try:
        results = batch.crawl(urls, extract_rules={
            'title': 'title::text'
        })
        
        print(f"   成功: {batch.get_stats()}")
        
        for i, result in enumerate(results, 1):
            title = result.get('data', {}).get('title', 'N/A')
            print(f"   页面 {i}: {title}")
    except Exception as e:
        print(f"   批量爬取失败: {e}")


def demo_dynamic_crawler():
    """演示动态页面爬虫"""
    print("\n" + "=" * 50)
    print("动态页面爬虫示例")
    print("=" * 50)
    
    print("\n1. 初始化动态爬虫...")
    
    try:
        crawler = DynamicCrawler(headless=True)
        
        print("\n2. 获取动态页面...")
        html = crawler.fetch('https://httpbin.org/html', wait_time=2)
        print(f"   页面长度: {len(html)} 字符")
        
        # 提取数据
        data = crawler.extract(html, {
            'title': 'title',
            'heading': 'h1'
        })
        print(f"   标题: {data.get('title')}")
        
        crawler.close()
    except Exception as e:
        print(f"   动态爬虫失败: {e}")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print(" Smart Crawler - 智能爬虫工具示例 ")
    print("=" * 60)
    
    demo_basic_crawler()
    demo_batch_crawler()
    demo_dynamic_crawler()
    
    print("\n" + "=" * 60)
    print("所有示例已完成！")
    print("=" * 60)
