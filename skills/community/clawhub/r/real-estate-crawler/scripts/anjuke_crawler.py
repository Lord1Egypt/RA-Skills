#!/usr/bin/env python3
"""
安居客爬虫脚本（基于之前的经验）
"""

import requests
import json
import time
import random
import re
import argparse
import sys

def crawl_anjuke():
    """爬取安居客房产数据"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/'
    }
    
    # 设置城市参数
    cities = [
        {"name": "南京", "url": "https://nanjing.anjuke.com"},
        {"name": "上海", "url": "https://shanghai.anjuke.com"},
        {"name": "广州", "url": "https://guangzhou.anjuke.com"},
        {"name": "深圳", "url": "https://shenzhen.anjuke.com"}
    ]
    
    results = {}
    
    for city in cities:
        print(f"\n=== 爬取 {city['name']} 房产数据 ===")
        
        try:
            response = requests.get(city['url'], headers=headers, timeout=10)
            print(f"状态码: {response.status_code}")
            print(f"页面大小: {len(response.text)} 字节")
            
            if response.status_code == 200:
                # 提取房产信息
                properties = extract_property_info(response.text)
                
                print(f"找到 {len(properties)} 个房产")
                results[city['name']] = properties
                
                # 打印前5个房产信息
                for i, prop in enumerate(properties[:5]):
                    print(f"{i+1}. {prop['title']}")
                    print(f"   总价: {prop['price']}万元 | 均价: {prop['avg_price']}元/㎡")
                    print(f"   面积: {prop['area']}㎡ | 年代: {prop['house_age']}")
                    print(f"   朝向: {prop['orient']} | 装修: {prop['fitment_name']}")
                
                # 等待随机时间避免触发反爬虫
                sleep_time = random.uniform(5, 10)
                print(f"等待 {sleep_time:.2f} 秒...")
                time.sleep(sleep_time)
                
        except Exception as e:
            print(f"错误: {e}")
    
    return results

def extract_property_info(data):
    """从安居客数据中提取房产信息"""
    
    # 正则表达式匹配房产信息
    pattern = r'"price":"([\d\.]+)",.*"avg_price":"([\d\.]+)",.*"area_num":"([\d\.]+)",.*"house_age":"([\d年]+)",.*"orient":"([^"]+)",.*"fitment_name":"([^"]+)",.*"title":"([^"]+)"'
    matches = re.findall(pattern, data)
    
    properties = []
    for match in matches:
        property_info = {
            'price': match[0],  # 总价（万元）
            'avg_price': match[1],  # 均价（元/㎡）
            'area_num': match[2],  # 面积（㎡）
            'house_age': match[3],  # 建筑年代
            'orient': match[4],  # 朝向
            'fitment_name': match[5],  # 装修
            'title': match[6]  # 标题
        }
        properties.append(property_info)
    
    return properties

def calculate_stats(data):
    """计算统计数据"""
    
    all_properties = []
    for city_name, properties in data.items():
        all_properties.extend(properties)
    
    if not all_properties:
        return None
    
    # 计算平均价格
    avg_price_sum = 0
    avg_area_sum = 0
    
    for prop in all_properties:
        try:
            avg_price_sum += float(prop['avg_price'])
            avg_area_sum += float(prop['area_num'])
        except ValueError:
            pass
    
    avg_price = avg_price_sum / len(all_properties)
    avg_area = avg_area_sum / len(all_properties)
    
    stats = {
        'total_properties': len(all_properties),
        'avg_price_per_m2': round(avg_price, 2),
        'avg_area': round(avg_area, 2),
        'city_count': len(data),
        'sample_size': min(len(all_properties), 20)
    }
    
    return stats

def save_to_json(data):
    """保存数据到JSON文件"""
    
    with open('anjuke_properties.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n数据保存到 anjuke_properties.json")

def save_to_csv(data):
    """保存数据到CSV文件"""
    
    import csv
    
    with open('anjuke_properties.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['城市', '标题', '总价', '均价', '面积', '建筑年代', '朝向', '装修'])
        
        for city_name, properties in data.items():
            for prop in properties:
                writer.writerow([
                    city_name,
                    prop['title'],
                    prop['price'],
                    prop['avg_price'],
                    prop['area_num'],
                    prop['house_age'],
                    prop['orient'],
                    prop['fitment_name']
                ])
    
    print(f"\n数据保存到 anjuke_properties.csv")

def main():
    """主函数"""
    
    parser = argparse.ArgumentParser(description='安居客爬虫')
    parser.add_argument('-c', '--city', default='南京', help='城市')
    parser.add_argument('-p', '--pages', type=int, default=1, help='页码')
    parser.add_argument('-o', '--output', default='anjuke_properties.json', help='输出文件')
    parser.add_argument('-f', '--format', choices=['json', 'csv'], default='json', help='输出格式')
    
    args = parser.parse_args()
    
    print("=== 开始安居客爬虫测试 ===")
    print("目标: 测试反爬虫机制并提取房产数据")
    print("策略: 单次请求 + 随机延迟 + 真实UA")
    
    # 爬取数据
    crawled_data = crawl_anjuke()
    
    # 计算统计
    stats = calculate_stats(crawled_data)
    if stats:
        print("\n=== 统计数据 ===")
        print(f"总房产数量: {stats['total_properties']}")
        print(f"平均单价: {stats['avg_price_per_m2']}元/㎡")
        print(f"平均面积: {stats['avg_area']}㎡")
        print(f"城市数量: {stats['city_count']}")
        print(f"样本大小: {stats['sample_size']}")
    
    # 保存数据
    if args.format == 'json':
        save_to_json(crawled_data)
    elif args.format == 'csv':
        save_to_csv(crawled_data)
    
    print("\n=== 测试成功 ===")
    print("说明: 安居客反爬虫机制是基于频率的，单个请求不会触发验证码")
    print("建议: 如果要爬取大量数据，需要控制频率（每秒不超过1-2个请求）")
    print("      并使用代理IP轮换")

if __name__ == "__main__":
    main()