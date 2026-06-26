"""
测试脚本 - 验证 toutiao-article-reader 功能
"""

import sys
import os

# 添加脚本路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from read_article import ArticleReader

# 测试 URL 列表
TEST_URLS = [
    {
        'name': '今日头条',
        'url': 'https://www.toutiao.com/article/7622885072810607113/',
        'expected_platform': '今日头条'
    },
    # 可以添加更多测试 URL
]

def test_read_article():
    """测试文章读取"""
    print("\n" + "="*60)
    print("Testing toutiao-article-reader")
    print("="*60)
    
    reader = ArticleReader(timeout=30000, headless=True)
    
    for i, test_case in enumerate(TEST_URLS, 1):
        print(f"\n测试 {i}/{len(TEST_URLS)}: {test_case['name']}")
        print("-"*60)
        
        result = reader.read(test_case['url'])
        
        if result['success']:
            print(f"OK: Success")
            print(f"   Title: {result['title'][:50]}...")
            print(f"   Platform: {result['platform']}")
            print(f"   Words: {result['word_count']}")
            print(f"   Author: {result['author'] or 'Unknown'}")
            
            # 验证平台识别
            if result['platform'] == test_case['expected_platform']:
                print(f"   OK: Platform correct")
            else:
                print(f"   WARN: Platform mismatch")
    
    print("\n" + "="*60)
    print("Test Complete")
    print("="*60)

if __name__ == '__main__':
    test_read_article()
