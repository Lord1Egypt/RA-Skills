#!/usr/bin/env python3
"""
从网页链接解析房源信息
用法: python parse_url.py --url "https://..." [--source 贝壳|链家|豆瓣|58]

支持的平台：
- 贝壳找房 (ke.com)
- 链家 (lianjia.com)
- 豆瓣租房小组 (douban.com)
- 58同城 (58.com)
- 安居客 (anjuke.com)
"""

import json
import os
import argparse
import re
import urllib.request
import urllib.error
from datetime import datetime

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/rental-data")
DATA_FILE = os.path.join(DATA_DIR, "listings.json")

def ensure_data_dir():
    """确保数据目录存在"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_listings():
    """加载现有房源列表"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_listings(listings):
    """保存房源列表"""
    ensure_data_dir()
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(listings, f, ensure_ascii=False, indent=2)

def fetch_page(url):
    """获取网页内容"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"获取页面失败: {e}")
        return None

def parse_ke_lianjia(html, url):
    """解析贝壳/链家页面"""
    info = {
        "source": "贝壳找房" if "ke.com" in url else "链家",
        "url": url
    }
    
    # 尝试提取标题（小区名称）
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html)
    if title_match:
        info["name"] = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
    
    # 尝试提取价格
    price_match = re.search(r'(\d+)</span>\s*<span[^>]*>元/月', html)
    if price_match:
        info["rent"] = int(price_match.group(1))
    else:
        # 备用匹配
        price_match = re.search(r'price[^>]*>(\d+)<', html)
        if price_match:
            info["rent"] = int(price_match.group(1))
    
    # 尝试提取户型
    room_match = re.search(r'(\d+)室(\d+)厅', html)
    if room_match:
        info["room_type"] = f"{room_match.group(1)}室{room_match.group(2)}厅"
    
    # 尝试提取面积
    area_match = re.search(r'(\d+\.?\d*)\s*㎡', html)
    if area_match:
        info["area"] = float(area_match.group(1))
    
    return info

def parse_douban(html, url):
    """解析豆瓣租房帖子"""
    info = {
        "source": "豆瓣租房",
        "url": url
    }
    
    # 提取标题
    title_match = re.search(r'<span id="cb_post_title_url">(.*?)</span>', html)
    if not title_match:
        title_match = re.search(r'<title>(.*?)</title>', html)
    if title_match:
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        info["name"] = title[:50]  # 限制长度
    
    # 从标题或内容提取价格
    price_match = re.search(r'(\d{3,5})\s*元', html)
    if price_match:
        price = int(price_match.group(1))
        if 500 <= price <= 50000:  # 合理价格范围
            info["rent"] = price
    
    # 提取内容
    content_match = re.search(r'<div class="topic-content">(.*?)</div>', html, re.DOTALL)
    if content_match:
        content = re.sub(r'<[^>]+>', '', content_match.group(1))
        info["pros"] = content[:200]  # 提取前200字作为描述
    
    return info

def parse_generic(html, url):
    """通用解析"""
    info = {
        "source": "未知来源",
        "url": url
    }
    
    # 尝试从title提取
    title_match = re.search(r'<title>(.*?)</title>', html)
    if title_match:
        info["name"] = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()[:50]
    
    # 尝试提取价格
    price_patterns = [
        r'(\d{4,5})\s*元/?月',
        r'租金[:：]\s*(\d{4,5})',
        r'价格[:：]\s*(\d{4,5})',
    ]
    for pattern in price_patterns:
        match = re.search(pattern, html)
        if match:
            info["rent"] = int(match.group(1))
            break
    
    return info

def parse_url(args):
    """解析URL"""
    url = args.url
    html = fetch_page(url)
    
    if not html:
        print("无法获取页面内容，请检查链接是否有效")
        return
    
    # 根据域名选择解析器
    if "ke.com" in url or "lianjia.com" in url:
        info = parse_ke_lianjia(html, url)
    elif "douban.com" in url:
        info = parse_douban(html, url)
    else:
        info = parse_generic(html, url)
    
    # 显示解析结果
    print("\n📋 解析结果：")
    print("-" * 40)
    for key, value in info.items():
        if value:
            print(f"{key}: {value}")
    
    # 保存到数据库
    listings = load_listings()
    new_id = f"L{len(listings) + 1:03d}"
    
    listing = {
        "id": new_id,
        "name": info.get("name", "未命名房源"),
        "rent": info.get("rent", 0),
        "room_type": info.get("room_type", ""),
        "area": info.get("area", 0),
        "source": info.get("source", ""),
        "url": info.get("url", ""),
        "pros": info.get("pros", ""),
        "status": "待考虑",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    listings.append(listing)
    save_listings(listings)
    
    print(f"\n✅ 已保存为房源 {new_id}")
    print("提示：请补充完善其他信息（地址、交通、联系方式等）")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从网页解析房源")
    parser.add_argument("--url", required=True, help="房源链接")
    parser.add_argument("--source", help="房源来源平台")
    
    args = parser.parse_args()
    parse_url(args)
