#!/usr/bin/env python3
"""
房产中介网站通用爬虫脚本
支持：安居客、贝壳找房、链家、搜房网
"""

import json
import time
import random
import requests
from dataclasses import dataclass
import re
import argparse
import sys

@dataclass
class PropertyData:
    """房产数据模型"""
    title: str          # 房源标题
    price: str          # 价格（总价）
    avg_price: str      # 均价（元/㎡）
    area: str           # 面积（㎡）
    location: str       # 位置
    house_type: str     # 户型
    age: str            # 建筑年代
    orientation: str    # 朝向
    decoration: str     # 装修状态
    source: str         # 来源网站

class RealEstateSpider:
    """通用房产爬虫"""
    
    def __init__(self, website="anjuke"):
        """初始化爬虫"""
        self.website = website
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # 网站基础URL
        self.urls = {
            'anjuke': 'https://www.anjuke.com',
            'ke': 'https://ke.com',
            'lianjia': 'https://www.lianjia.com',
            'soufun': 'https://www.soufun.com'
        }
        
    def crawl(self, city="北京", district=None, page=1):
        """爬取房产数据"""
        
        # 构建URL
        url = self.build_url(city, district, page)
        
        print(f"开始爬取 {self.website} - {city}")
        print(f"目标URL: {url}")
        
        # 发送请求
        html_data = self.send_request(url)
        
        if html_data:
            # 解析数据
            properties = self.parse_data(html_data)
            
            # 统计分析
            stats = self.calculate_stats(properties)
            
            return {
                'data': properties,
                'stats': stats,
                'url': url
            }
        else:
            return {
                'data': [],
                'stats': None,
                'url': url
            }
    
    def build_url(self, city, district=None, page=1):
        """构建目标URL"""
        
        from config.real_estate_config import CONFIG
        
        if self.website == "anjuke":
            base = f"{CONFIG['anjuke']['url']}/fangyuan/{city}"
            if district:
                base = f"{CONFIG['anjuke']['url']}/fangyuan/{city}/{district}"
            if page > 1:
                base += f"?page={page}"
                
        elif self.website == "ke":
            # 获取城市前缀
            city_prefixes = CONFIG['ke']['city_prefixes']
            city_prefix = city_prefixes.get(city, "bj")  # 默认北京
            base = f"https://{city_prefix}.ke.com"
            if district:
                base += f"/district/{district}"
            if page > 1:
                base += f"?page={page}"
                
        elif self.website == "lianjia":
            base = f"{CONFIG['lianjia']['url']}/ershoufang/{city}"
            if district:
                base = f"{CONFIG['lianjia']['url']}/ershoufang/{city}/{district}"
            if page > 1:
                base += f"?page={page}"
                
        elif self.website == "soufun":
            base = f"{CONFIG['soufun']['url']}/esf/{city}"
            if district:
                base = f"{CONFIG['soufun']['url']}/esf/{city}/{district}"
            if page > 1:
                base += f"?page={page}"
                
        else:
            base = CONFIG.get(self.website, CONFIG['anjuke'])['url']
            
        return base
    
    def send_request(self, url):
        """发送HTTP请求"""
        
        # 随机延迟，避免频率检测
        sleep_time = random.uniform(2, 5)
        print(f"等待 {sleep_time:.2f} 秒以避免检测...")
        time.sleep(sleep_time)
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                print(f"请求成功，页面大小: {len(response.text)} 字节")
                return response.text
            else:
                print(f"请求失败，状态码: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"请求出错: {e}")
            return None
    
    def parse_data(self, html_data):
        """解析HTML数据"""
        
        properties = []
        
        if self.website == "anjuke":
            # 安居客解析规则
            pattern = r'"price":"([\d\.]+)",.*"avg_price":"([\d\.]+)",.*"area_num":"([\d\.]+)",.*"house_age":"([\d年]+)",.*"orient":"([^"]+)",.*"fitment_name":"([^"]+)",.*"title":"([^"]+)"'
            
        elif self.website == "ke":
            # 贝壳找房解析规则（示例）
            pattern = r'"totalPrice":"([\d\.]+)",.*"unitPrice":"([\d\.]+)",.*"houseArea":"([\d\.]+)",.*"buildYear":"([\d年]+)",.*"orientation":"([^"]+)",.*"decoration":"([^"]+)",.*"title":"([^"]+)"'
            
        elif self.website == "lianjia":
            # 链家解析规则（示例）
            pattern = r'"priceTotal":"([\d\.]+)",.*"priceUnit":"([\d\.]+)",.*"area":"([\d\.]+)",.*"buildingAge":"([\d年]+)",.*"orientation":"([^"]+)",.*"decoration":"([^"]+)",.*"title":"([^"]+)"'
            
        elif self.website == "soufun":
            # 搜房网解析规则（示例）
            pattern = r'"price":"([\d\.]+)",.*"unitPrice":"([\d\.]+)",.*"area":"([\d\.]+)",.*"age":"([\d年]+)",.*"orientation":"([^"]+)",.*"decoration":"([^"]+)",.*"title":"([^"]+)"'
            
        else:
            pattern = r'"price":"([\d\.]+)",.*"avg_price":"([\d\.]+)",.*"area_num":"([\d\.]+)",.*"house_age":"([\d年]+)",.*"orient":"([^"]+)",.*"fitment_name":"([^"]+)",.*"title":"([^"]+)"'
        
        matches = re.findall(pattern, html_data)
        
        for match in matches:
            property = PropertyData(
                title=match[6],
                price=match[0],
                avg_price=match[1],
                area=match[2],
                location="待提取",  # 需要根据具体网站调整
                house_type="待提取",  # 需要根据具体网站调整
                age=match[3],
                orientation=match[4],
                decoration=match[5],
                source=self.website
            )
            properties.append(property)
        
        print(f"解析到 {len(properties)} 个房产信息")
        return properties
    
    def calculate_stats(self, properties):
        """计算统计数据"""
        
        if not properties:
            return None
        
        avg_price_sum = 0
        avg_unit_price_sum = 0
        area_sum = 0
        
        for prop in properties:
            try:
                avg_price_sum += float(prop.price)
                avg_unit_price_sum += float(prop.avg_price)
                area_sum += float(prop.area)
            except ValueError:
                pass
        
        avg_price = avg_price_sum / len(properties)
        avg_unit_price = avg_unit_price_sum / len(properties)
        avg_area = area_sum / len(properties)
        
        stats = {
            'count': len(properties),
            'avg_price_total': round(avg_price, 2),
            'avg_price_per_m2': round(avg_unit_price, 2),
            'avg_area': round(avg_area, 2)
        }
        
        return stats
    
    def save_json(self, data, filename):
        """保存为JSON文件"""
        
        properties = data['data']
        
        save_data = []
        for prop in properties:
            save_data.append({
                'title': prop.title,
                'price': prop.price,
                'avg_price': prop.avg_price,
                'area': prop.area,
                'location': prop.location,
                'house_type': prop.house_type,
                'age': prop.age,
                'orientation': prop.orientation,
                'decoration': prop.decoration,
                'source': prop.source
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"数据保存到: {filename}")
        
    def save_csv(self, data, filename):
        """保存为CSV文件"""
        
        import csv
        
        properties = data['data']
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['title', 'price', 'avg_price', 'area', 'location', 'house_type', 'age', 'orientation', 'decoration', 'source'])
            
            for prop in properties:
                writer.writerow([
                    prop.title,
                    prop.price,
                    prop.avg_price,
                    prop.area,
                    prop.location,
                    prop.house_type,
                    prop.age,
                    prop.orientation,
                    prop.decoration,
                    prop.source
                ])
        
        print(f"数据保存到: {filename}")

def main():
    """主函数"""
    
    parser = argparse.ArgumentParser(description='房产中介网站通用爬虫')
    parser.add_argument('-w', '--website', choices=['anjuke', 'ke', 'lianjia', 'soufun'], default='anjuke', help='目标网站')
    parser.add_argument('-c', '--city', default='北京', help='城市')
    parser.add_argument('-d', '--district', help='区域')
    parser.add_argument('-p', '--page', type=int, default=1, help='页码')
    parser.add_argument('-o', '--output', default='properties.json', help='输出文件')
    parser.add_argument('-f', '--format', choices=['json', 'csv'], default='json', help='输出格式')
    
    args = parser.parse_args()
    
    # 创建爬虫实例
    spider = RealEstateSpider(args.website)
    
    # 爬取数据
    result = spider.crawl(args.city, args.district, args.page)
    
    if result['data']:
        # 打印统计信息
        stats = result['stats']
        print(f"\n=== 统计数据 ===")
        print(f"房产数量: {stats['count']}")
        print(f"平均总价: {stats['avg_price_total']} 万元")
        print(f"平均单价: {stats['avg_price_per_m2']} 元/㎡")
        print(f"平均面积: {stats['avg_area']} ㎡")
        
        # 保存数据
        if args.format == 'json':
            spider.save_json(result, args.output)
        elif args.format == 'csv':
            spider.save_csv(result, args.output.replace('.json', '.csv'))
        
        # 打印前5个房产信息
        print(f"\n=== 前5个房产信息 ===")
        for i, prop in enumerate(result['data'][:5]):
            print(f"{i+1}. {prop.title}")
            print(f"   总价: {prop.price}万元 | 均价: {prop.avg_price}元/㎡")
            print(f"   面积: {prop.area}㎡ | 年代: {prop.age}")
            print(f"   朝向: {prop.orientation} | 装修: {prop.decoration}")
    
    else:
        print(f"没有找到房产信息")
        print(f"URL: {result['url']}")
        
    print("\n=== 爬虫完成 ===")

if __name__ == "__main__":
    main()