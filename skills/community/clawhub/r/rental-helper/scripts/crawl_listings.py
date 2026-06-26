#!/usr/bin/env python3
"""
从各大租房网站抓取房源信息
用法: python crawl_listings.py --platform 贝壳 --city 北京 --area 朝阳区 --budget 5000

支持平台：
- 贝壳找房 (ke.com)
- 链家 (lianjia.com)
- 58同城 (58.com)
- 安居客 (anjuke.com)
"""

import json
import os
import argparse
import urllib.request
import urllib.error
import re
import ssl
from datetime import datetime
from urllib.parse import quote

# 忽略SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/rental-data")
DATA_FILE = os.path.join(DATA_DIR, "listings.json")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_listings():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_listings(listings):
    ensure_data_dir()
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(listings, f, ensure_ascii=False, indent=2)

def fetch_page(url, headers=None):
    """获取网页内容"""
    try:
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        if headers:
            default_headers.update(headers)
        
        req = urllib.request.Request(url, headers=default_headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"获取页面失败: {e}")
        return None

def crawl_ke_beike(city, area, budget, limit=10):
    """抓取贝壳/链家房源"""
    listings = []
    
    # 城市代码映射
    city_codes = {
        '北京': 'bj',
        '上海': 'sh',
        '广州': 'gz',
        '深圳': 'sz',
        '杭州': 'hz',
        '南京': 'nj',
        '成都': 'cd',
        '武汉': 'wh',
        '西安': 'xa',
        '重庆': 'cq',
    }
    
    city_code = city_codes.get(city, 'bj')
    
    # 构建URL - 对区域进行URL编码
    price_max = budget if budget else 10000
    encoded_area = quote(area.encode('utf-8')) if area else ''
    url = f"https://{city_code}.ke.com/zufang/{encoded_area}/rp{price_max}/"
    
    print(f"正在抓取: {url}")
    html = fetch_page(url)
    
    if not html:
        return listings
    
    # 解析房源列表
    # 贝壳/链家页面结构
    pattern = r'data-houseid="(\d+)".*?<a[^>]*href="([^"]*zufang[^"]*)"[^>]*title="([^"]*)".*?<span[^>]*class="price">\s*<em>(\d+)</em>.*?<span[^>]*class="unit">([^<]*)</span>'
    matches = re.findall(pattern, html, re.DOTALL)
    
    for i, match in enumerate(matches[:limit]):
        house_id, link, title, price, unit = match
        
        # 提取更多信息
        room_type = ""
        area_size = 0
        
        room_match = re.search(r'(\d+)室(\d+)厅', title)
        if room_match:
            room_type = f"{room_match.group(1)}室{room_match.group(2)}厅"
        
        area_match = re.search(r'(\d+\.?\d*)㎡', title)
        if area_match:
            area_size = float(area_match.group(1))
        
        listing = {
            "id": f"CRAWL_{city_code}_{house_id}",
            "name": title[:50],
            "rent": int(price),
            "room_type": room_type,
            "area": area_size,
            "source": "贝壳找房",
            "url": f"https://{city_code}.ke.com{link}" if not link.startswith('http') else link,
            "status": "待考虑",
            "created_at": datetime.now().isoformat(),
        }
        listings.append(listing)
    
    return listings

def crawl_58tongcheng(city, area, budget, limit=10):
    """抓取58同城房源"""
    listings = []
    
    # 构建搜索URL - 正确编码中文
    keyword = quote(f"{city} {area} 租房".encode('utf-8'))
    # 58同城城市代码映射
    city_codes_58 = {
        '北京': 'bj',
        '上海': 'sh',
        '广州': 'gz',
        '深圳': 'sz',
        '杭州': 'hz',
        '南京': 'nj',
        '成都': 'cd',
        '武汉': 'wh',
        '西安': 'xa',
        '重庆': 'cq',
    }
    city_code = city_codes_58.get(city, 'bj')
    url = f"https://{city_code}.58.com/zufang/?key={keyword}"
    
    print(f"正在抓取: {url}")
    html = fetch_page(url)
    
    if not html:
        return listings
    
    # 58同城页面解析（简化版）
    # 注意：58同城反爬较强，这里提供基础解析
    pattern = r'<h2[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>.*?</h2>.*?<b[^>]*class="strongbox">(\d+)</b>\s*<i[^>]*>元/月</i>'
    matches = re.findall(pattern, html, re.DOTALL)
    
    for i, match in enumerate(matches[:limit]):
        link, title, price = match
        title = re.sub(r'<[^>]+>', '', title).strip()
        
        if budget and int(price) > budget:
            continue
        
        listing = {
            "id": f"CRAWL_58_{i}",
            "name": title[:50],
            "rent": int(price),
            "source": "58同城",
            "url": link if link.startswith('http') else f"https:{link}",
            "status": "待考虑",
            "created_at": datetime.now().isoformat(),
        }
        listings.append(listing)
    
    return listings

def crawl_anjuke(city, area, budget, limit=10):
    """抓取安居客房源"""
    listings = []
    
    # 城市代码
    city_codes = {
        '北京': 'beijing',
        '上海': 'shanghai',
        '广州': 'guangzhou',
        '深圳': 'shenzhen',
        '成都': 'chengdu',
        '杭州': 'hangzhou',
    }
    
    city_code = city_codes.get(city, 'beijing')
    
    # 构建URL - 正确编码中文
    url = f"https://{city_code}.zu.anjuke.com/"
    if area:
        encoded_area = quote(area.encode('utf-8'))
        url += f"?kw={encoded_area}"
    
    print(f"正在抓取: {url}")
    html = fetch_page(url)
    
    if not html:
        return listings
    
    # 安居客页面解析
    pattern = r'<h3[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>.*?</h3>.*?<strong[^>]*>(\d+)</strong>\s*<span[^>]*>元/月</span>'
    matches = re.findall(pattern, html, re.DOTALL)
    
    for i, match in enumerate(matches[:limit]):
        link, title, price = match
        title = re.sub(r'<[^>]+>', '', title).strip()
        
        if budget and int(price) > budget:
            continue
        
        listing = {
            "id": f"CRAWL_ANJUKE_{i}",
            "name": title[:50],
            "rent": int(price),
            "source": "安居客",
            "url": link if link.startswith('http') else f"https:{link}",
            "status": "待考虑",
            "created_at": datetime.now().isoformat(),
        }
        listings.append(listing)
    
    return listings

def crawl_xianyu(keyword, budget, limit=10):
    """抓取闲鱼房源"""
    print("⚠️ 闲鱼需要登录，建议使用手动导入方式")
    print("提示：可以复制闲鱼房源信息，使用 parse_image.py 从截图识别")
    return []

def crawl_listings(args):
    """主抓取函数"""
    all_listings = []
    
    platforms = {
        '贝壳': crawl_ke_beike,
        '链家': crawl_ke_beike,
        '58': crawl_58tongcheng,
        '58同城': crawl_58tongcheng,
        '安居客': crawl_anjuke,
    }
    
    if args.platform:
        platform_list = [args.platform]
    else:
        platform_list = ['贝壳', '58同城', '安居客']
    
    for platform in platform_list:
        crawler = platforms.get(platform)
        if crawler:
            print(f"\n🔍 正在从 {platform} 抓取...")
            listings = crawler(args.city, args.area, args.budget, args.limit)
            all_listings.extend(listings)
            print(f"✅ 从 {platform} 抓取到 {len(listings)} 条房源")
    
    if not all_listings:
        print("\n⚠️ 未抓取到房源，可能原因：")
        print("   1. 网站反爬限制")
        print("   2. 网络连接问题")
        print("   3. 页面结构变化")
        print("\n建议：使用 parse_url.py 手动解析具体房源链接")
        return
    
    # 去重（基于URL）
    seen_urls = set()
    unique_listings = []
    for l in all_listings:
        if l['url'] not in seen_urls:
            seen_urls.add(l['url'])
            unique_listings.append(l)
    
    # 显示结果
    print(f"\n📊 抓取结果汇总：")
    print(f"   总计: {len(unique_listings)} 条房源")
    
    print(f"\n{'ID':<20}{'来源':<10}{'租金':<10}{'名称':<30}")
    print("-" * 70)
    for l in unique_listings[:10]:
        name = l['name'][:28]
        print(f"{l['id']:<20}{l['source']:<10}{l['rent']:<10}{name:<30}")
    
    if len(unique_listings) > 10:
        print(f"... 还有 {len(unique_listings) - 10} 条")
    
    # 保存到数据库
    if args.save:
        existing = load_listings()
        
        # 为抓取的房源生成新ID
        for i, l in enumerate(unique_listings):
            new_id = f"L{len(existing) + i + 1:03d}"
            l['id'] = new_id
        
        existing.extend(unique_listings)
        save_listings(existing)
        
        print(f"\n✅ 已保存 {len(unique_listings)} 条房源到数据库")
    else:
        print(f"\n💡 使用 --save 参数保存到数据库")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="抓取租房网站房源")
    parser.add_argument("--platform", choices=['贝壳', '链家', '58', '58同城', '安居客'], 
                       help="目标平台（默认全部）")
    parser.add_argument("--city", default="北京", help="城市（默认：北京）")
    parser.add_argument("--area", help="区域/商圈")
    parser.add_argument("--budget", type=int, help="预算上限")
    parser.add_argument("--limit", type=int, default=10, help="每个平台抓取数量（默认10）")
    parser.add_argument("--save", action="store_true", help="保存到数据库")
    
    args = parser.parse_args()
    crawl_listings(args)
