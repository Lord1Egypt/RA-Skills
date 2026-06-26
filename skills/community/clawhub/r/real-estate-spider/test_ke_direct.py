#!/usr/bin/env python3
"""
直接测试贝壳找房爬虫
"""

import requests
import re
import time
import json
import random

def test_ke_beijing():
    """测试贝壳找房北京站"""
    
    url = "https://bj.ke.com/ershoufang"
    
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
    
    print(f"请求URL: {url}")
    print("等待随机延迟...")
    time.sleep(random.uniform(3, 5))
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"页面大小: {len(response.text)} 字节")
        
        if response.status_code == 200:
            # 保存HTML内容到文件用于分析
            with open('ke_beijing.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("HTML已保存到 ke_beijing.html")
            
            # 尝试提取二手房信息
            html_content = response.text
            
            # 方法1：查找包含房产信息的JSON数据
            import re
            
            # 查找页面中的房产数据
            patterns = [
                r'"totalPrice":"([\d\.]+)"',
                r'"unitPrice":"([\d\.]+)"',
                r'"houseArea":"([\d\.]+)"',
                r'"buildYear":"([\d年]+)"',
                r'"orientation":"([^"]+)"',
                r'"decoration":"([^"]+)"',
                r'"title":"([^"]+)"',
                r'"communityName":"([^"]+)"',
                r'"areaName":"([^"]+)"',
                r'"totalPriceNum":(\d+)',
                r'"unitPriceNum":(\d+)',
                r'"area":([\d\.]+)',
            ]
            
            print("\n尝试提取数据...")
            
            for pattern in patterns:
                matches = re.findall(pattern, html_content)
                if matches:
                    print(f"模式 '{pattern[:30]}...' 找到 {len(matches)} 个匹配")
                    if len(matches) <= 10:
                        print(f"  示例: {matches[:5]}")
            
            # 查看是否有房源列表
            if '"totalPrice"' in html_content or '"unitPrice"' in html_content:
                print("\n发现房产价格数据")
                
                # 提取所有totalPrice和unitPrice
                total_prices = re.findall(r'"totalPrice":"([\d\.]+)"', html_content)
                unit_prices = re.findall(r'"unitPrice":"([\d\.]+)"', html_content)
                titles = re.findall(r'"title":"([^"]+)"', html_content)
                areas = re.findall(r'"houseArea":"([\d\.]+)"', html_content)
                
                if total_prices:
                    print(f"找到 {len(total_prices)} 个房产总价")
                    print(f"示例总价: {total_prices[:5]}")
                
                if unit_prices:
                    print(f"找到 {len(unit_prices)} 个房产单价")
                    print(f"示例单价: {unit_prices[:5]}")
                
                if titles:
                    print(f"找到 {len(titles)} 个房产标题")
                    print(f"示例标题: {titles[:3]}")
                
                if areas:
                    print(f"找到 {len(areas)} 个房产面积")
                    print(f"示例面积: {areas[:5]}")
                
                # 尝试提取房产列表信息
                house_list_pattern = r'"houseList":\[(.*?)\]'
                house_list_match = re.search(house_list_pattern, html_content, re.DOTALL)
                
                if house_list_match:
                    print("找到 houseList 数据")
                    house_list_json = house_list_match.group(1)
                    # 尝试解析为JSON
                    try:
                        import json
                        # 清理数据
                        house_data = json.loads(f'[{house_list_json}]')
                        print(f"成功解析 {len(house_data)} 个房产")
                        for i, house in enumerate(house_data[:3]):
                            print(f"房产 {i+1}: {house.get('title', '未知')}")
                            print(f"  总价: {house.get('totalPrice', '未知')}")
                            print(f"  单价: {house.get('unitPrice', '未知')}")
                            print(f"  面积: {house.get('houseArea', '未知')}")
                    except:
                        print("无法解析为JSON，可能格式有误")
            
            # 查找房源总数
            total_pattern = r'北京在售二手房\s*(\d+)\s*套'
            total_match = re.search(total_pattern, html_content)
            if total_match:
                total_houses = total_match.group(1)
                print(f"\n北京在售二手房总数: {total_houses} 套")
            
            # 查找热门小区
            hot_communities = re.findall(r'<a[^>]*href="[^"]*xiaoqu/[^"]*"[^>]*>([^<]+)</a>', html_content)
            if hot_communities:
                print(f"\n找到 {len(hot_communities)} 个热门小区")
                print("示例小区:", hot_communities[:10])
            
            return html_content
            
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"响应头部: {response.headers}")
            
    except Exception as e:
        print(f"请求出错: {e}")
        import traceback
        traceback.print_exc()
    
    return None

def analyze_ke_html(html_content):
    """分析贝壳找房HTML结构"""
    
    print("\n=== HTML结构分析 ===")
    
    # 查找所有可能的房产信息模式
    patterns = {
        "房产卡片": r'<div[^>]*class="[^"]*houseInfo[^"]*"[^>]*>',
        "价格信息": r'<div[^>]*class="[^"]*totalPrice[^"]*"[^>]*>',
        "单价信息": r'<div[^>]*class="[^"]*unitPrice[^"]*"[^>]*>',
        "标题链接": r'<a[^>]*href="/ershoufang/\d+\.html"[^>]*>',
        "小区信息": r'<div[^>]*class="[^"]*houseInfo[^"]*"[^>]*>.*?<a[^>]*>([^<]+)</a>',
        "位置信息": r'<div[^>]*class="[^"]*positionInfo[^"]*"[^>]*>',
    }
    
    for name, pattern in patterns.items():
        matches = re.findall(pattern, html_content, re.DOTALL)
        if matches:
            print(f"{name}: 找到 {len(matches)} 个匹配")
            if len(matches) <= 3:
                for i, match in enumerate(matches[:3]):
                    print(f"  示例 {i+1}: {match[:100]}...")
    
    # 提取具体房产信息
    print("\n=== 房产信息提取 ===")
    
    # 尝试查找房源列表
    listings = re.findall(r'<li[^>]*class="[^"]*clear[^"]*"[^>]*>.*?</li>', html_content, re.DOTALL)
    print(f"找到 {len(listings)} 个房源列表项")
    
    for i, listing in enumerate(listings[:5]):
        print(f"\n房源 {i+1}:")
        
        # 提取标题
        title_match = re.search(r'<a[^>]*title="([^"]+)"', listing)
        if title_match:
            print(f"  标题: {title_match.group(1)}")
        
        # 提取总价
        total_price_match = re.search(r'<div[^>]*class="[^"]*totalPrice[^"]*"[^>]*>([^<]+)</div>', listing)
        if total_price_match:
            print(f"  总价: {total_price_match.group(1)}")
        
        # 提取单价
        unit_price_match = re.search(r'<div[^>]*class="[^"]*unitPrice[^"]*"[^>]*>([^<]+)</div>', listing)
        if unit_price_match:
            print(f"  单价: {unit_price_match.group(1)}")
        
        # 提取位置
        position_match = re.search(r'<div[^>]*class="[^"]*positionInfo[^"]*"[^>]*>([^<]+)</div>', listing)
        if position_match:
            print(f"  位置: {position_match.group(1)}")

def main():
    print("=== 贝壳找房爬虫测试 ===")
    print("目标: https://bj.ke.com/ershoufang")
    
    html_content = test_ke_beijing()
    
    if html_content:
        print("\n=== 分析HTML结构 ===")
        analyze_ke_html(html_content)
        
        # 保存数据分析结果
        with open('ke_analysis.txt', 'w', encoding='utf-8') as f:
            f.write(f"页面大小: {len(html_content)} 字节\n")
            
            # 统计各种数据
            total_prices = re.findall(r'"totalPrice":"([\d\.]+)"', html_content)
            unit_prices = re.findall(r'"unitPrice":"([\d\.]+)"', html_content)
            titles = re.findall(r'"title":"([^"]+)"', html_content)
            
            f.write(f"找到的总价数量: {len(total_prices)}\n")
            f.write(f"找到的单价数量: {len(unit_prices)}\n")
            f.write(f"找到的标题数量: {len(titles)}\n")
            
            if total_prices:
                f.write(f"总价示例: {total_prices[:10]}\n")
            if unit_prices:
                f.write(f"单价示例: {unit_prices[:10]}\n")
            if titles:
                f.write(f"标题示例: {titles[:5]}\n")
        
        print("\n数据分析已保存到 ke_analysis.txt")
    
    print("\n=== 测试完成 ===")
    print("结论: 贝壳找房网站有完整的反爬虫机制，但我们可以获取到页面内容")
    print("下一步: 需要优化数据提取策略，可能需要解析JavaScript数据")

if __name__ == "__main__":
    main()