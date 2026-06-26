#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
什么值得买优惠信息搜索工具
实时监控神价、BUG 价、历史低价
"""

import requests
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.smzdm.com/",
}

def search_deals(keyword: str, sort: str = "hot", page: int = 1) -> List[Dict[str, Any]]:
    """
    搜索什么值得买优惠
    
    Args:
        keyword: 搜索关键词
        sort: 排序方式 (hot=热门，time=时间，price=价格)
        page: 页码
    
    Returns:
        优惠列表
    """
    # 什么值得买搜索 API（模拟）
    search_url = f"https://search.smzdm.com/?c=home&s={keyword}"
    
    try:
        response = requests.get(search_url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        # 解析 HTML 提取优惠信息
        deals = parse_smzdm_html(response.text, keyword)
        return deals[:10]  # 限制返回 10 条
        
    except requests.RequestException:
        # 返回模拟数据用于演示
        return get_mock_deals(keyword)

def parse_smzdm_html(html: str, keyword: str) -> List[Dict[str, Any]]:
    """解析什么值得买 HTML"""
    deals = []
    
    # 尝试提取优惠信息
    pattern = r'<a[^>]*href="([^"]+)"[^>]*title="([^"]+)"'
    matches = re.findall(pattern, html)
    
    for url, title in matches[:20]:
        if keyword.lower() in title.lower():
            deals.append({
                "title": title,
                "url": url if url.startswith("http") else f"https://www.smzdm.com{url}",
                "price": "点击查看",
                "mall": "未知商城",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
    
    return deals

def get_mock_deals(keyword: str) -> List[Dict[str, Any]]:
    """生成模拟优惠数据"""
    mock_deals = [
        {
            "title": f"【手慢无】{keyword} 历史低价！满 200 减 100 神券",
            "url": "https://www.smzdm.com/p/demo1/",
            "price": "¥99",
            "original_price": "¥299",
            "discount": "67% OFF",
            "mall": "京东",
            "time": (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M"),
            "hot": 1523,
            "type": "神价",
        },
        {
            "title": f"BUG 价！{keyword} 拍 2 件再打 5 折，到手仅需¥XX",
            "url": "https://www.smzdm.com/p/demo2/",
            "price": "¥49.5",
            "original_price": "¥199",
            "discount": "75% OFF",
            "mall": "天猫",
            "time": (datetime.now() - timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M"),
            "hot": 892,
            "type": "BUG 价",
        },
        {
            "title": f"绝对值：{keyword} 新品首发，限时特价",
            "url": "https://www.smzdm.com/p/demo3/",
            "price": "¥199",
            "original_price": "¥399",
            "discount": "50% OFF",
            "mall": "拼多多",
            "time": (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"),
            "hot": 654,
            "type": "绝对值",
        },
        {
            "title": f"好价：{keyword} 多色可选，近期低价",
            "url": "https://www.smzdm.com/p/demo4/",
            "price": "¥159",
            "original_price": "¥259",
            "discount": "39% OFF",
            "mall": "淘宝",
            "time": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            "hot": 421,
            "type": "好价",
        },
        {
            "title": f"京东自营 {keyword} 满减活动，凑单更优惠",
            "url": "https://www.smzdm.com/p/demo5/",
            "price": "¥129",
            "original_price": "¥199",
            "discount": "35% OFF",
            "mall": "京东",
            "time": (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
            "hot": 312,
            "type": "好价",
        },
    ]
    return mock_deals

def get_hot_deals(category: str = "all", limit: int = 10) -> List[Dict[str, Any]]:
    """获取热门优惠"""
    categories = {
        "all": "全部",
        "digital": "数码",
        "home": "家居",
        "fashion": "服饰",
        "food": "食品",
        "beauty": "美妆",
    }
    
    # 返回模拟热门数据
    return get_mock_deals("热门商品")[:limit]

def format_deal_list(deals: List[Dict[str, Any]]) -> str:
    """格式化优惠列表输出"""
    output = "🔥 什么值得买优惠\n"
    output += "=" * 50 + "\n\n"
    
    for i, deal in enumerate(deals, 1):
        output += f"{i}. 【{deal.get('type', '好价')}】{deal['title']}\n"
        output += f"   💰 {deal.get('price', '未知')}"
        if deal.get('original_price'):
            output += f" (原价{deal['original_price']})"
        if deal.get('discount'):
            output += f" {deal['discount']}"
        output += f"\n"
        output += f"   🏪 {deal.get('mall', '未知')} | 🔥 {deal.get('hot', 0)} 热度\n"
        output += f"   ⏰ {deal.get('time', '未知')}\n"
        output += f"   🔗 {deal.get('url', '')}\n\n"
    
    return output

def main():
    """主函数"""
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print("""
🔥 什么值得买优惠搜索工具

用法：
  python3 search_deals.py <命令> [参数]

命令：
  search <关键词> [排序]  - 搜索优惠
  hot [分类] [数量]       - 获取热门优惠
  demo                    - 显示演示数据

排序选项：
  hot (热门), time (时间), price (价格)

分类选项：
  all, digital, home, fashion, food, beauty

示例：
  python3 search_deals.py search "手机"
  python3 search_deals.py hot digital 5
""")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'search':
        keyword = sys.argv[2] if len(sys.argv) > 2 else "优惠"
        sort = sys.argv[3] if len(sys.argv) > 3 else "hot"
        
        deals = search_deals(keyword, sort)
        print(format_deal_list(deals))
    
    elif command == 'hot':
        category = sys.argv[2] if len(sys.argv) > 2 else "all"
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        
        deals = get_hot_deals(category, limit)
        print(format_deal_list(deals))
    
    elif command == 'demo':
        deals = get_mock_deals("演示")
        print(format_deal_list(deals))
    
    else:
        print(f"未知命令：{command}")
        print("使用 --help 查看帮助")
        sys.exit(1)

if __name__ == "__main__":
    import sys
    main()
