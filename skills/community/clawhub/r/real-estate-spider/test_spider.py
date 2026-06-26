#!/usr/bin/env python3
"""
测试房产爬虫技能
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.real_estate_crawler import RealEstateSpider

def test_anjuke():
    """测试安居客爬虫"""
    print("=== 测试安居客爬虫 ===")
    
    spider = RealEstateSpider("anjuke")
    result = spider.crawl(city="南京", page=1)
    
    if result['data']:
        print(f"找到 {len(result['data'])} 个房产")
        spider.save_json(result, "test_anjuke.json")
        
        # 打印前3个房产信息
        for i, prop in enumerate(result['data'][:3]):
            print(f"{i+1}. {prop.title}")
            print(f"   总价: {prop.price}万元 | 均价: {prop.avg_price}元/㎡")
            print(f"   面积: {prop.area}㎡ | 年代: {prop.age}")
            print(f"   朝向: {prop.orientation} | 装修: {prop.decoration}")
    else:
        print("没有找到房产信息")
    
def test_ke():
    """测试贝壳找房爬虫"""
    print("=== 测试贝壳找房爬虫 ===")
    
    spider = RealEstateSpider("ke")
    result = spider.crawl(city="上海", page=1)
    
    if result['data']:
        print(f"找到 {len(result['data'])} 个房产")
        spider.save_json(result, "test_ke.json")
        
        # 打印前3个房产信息
        for i, prop in enumerate(result['data'][:3]):
            print(f"{i+1}. {prop.title}")
            print(f"   总价: {prop.price}万元 | 均价: {prop.avg_price}元/㎡")
            print(f"   面积: {prop.area}㎡ | 年代: {prop.age}")
            print(f"   朝向: {prop.orientation} | 装修: {prop.decoration}")
    else:
        print("没有找到房产信息")

def test_config():
    """测试配置文件"""
    print("=== 测试配置文件 ===")
    
    from config.real_estate_config import CONFIG
    
    for website, config in CONFIG.items():
        print(f"{website}: {config['name']}")
        print(f"   URL: {config['url']}")
        print(f"   反爬虫等级: {config['anti_crawler_level']}")
        print(f"   反爬虫提示: {config['anti_crawler_tips']}")
        print()

def main():
    """主测试函数"""
    print("=== 房产中介网站爬虫测试 ===")
    
    # 测试配置文件
    test_config()
    
    # 测试安居客
    test_anjuke()
    
    # 测试贝壳找房
    test_ke()
    
    print("=== 测试完成 ===")

if __name__ == "__main__":
    main()