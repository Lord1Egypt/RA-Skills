#!/usr/bin/env python3
"""
雪球热门获取脚本
Xueqiu Hot Discussions Fetcher
"""

import json
import sys

def get_xueqiu_hot(limit=10):
    """获取雪球热门（模拟数据）"""
    mock_posts = [
        {"id": 1, "title": "茅台年报出炉，净利润增长15%，每股分红创新高", "category": "消费", "views": 125000, "comments": 567, "symbol": "$贵州茅台(SH600519)$"},
        {"id": 2, "title": "新能源板块集体反弹，宁德时代涨超5%", "category": "新能源", "views": 98000, "comments": 432, "symbol": "$宁德时代(SZ300750)$"},
        {"id": 3, "title": "腾讯年报解读：游戏业务回暖，广告增长强劲", "category": "科技", "views": 87000, "comments": 389, "symbol": "$腾讯控股(00700)$"},
        {"id": 4, "title": "银行股估值修复行情能持续多久？", "category": "银行", "views": 76000, "comments": 321, "symbol": "#银行#"},
        {"id": 5, "title": "AI算力需求爆发，关注这些标的", "category": "科技", "views": 65000, "comments": 298, "symbol": "#AI#"},
        {"id": 6, "title": "药明康德一季报超预期，CRO板块走强", "category": "医药", "views": 54000, "comments": 267, "symbol": "$药明康德(SH603259)$"},
        {"id": 7, "title": "比亚迪销量再创新高，新能车龙头地位稳固", "category": "汽车", "views": 43000, "comments": 234, "symbol": "$比亚迪(SZ002594)$"},
        {"id": 8, "title": "光伏行业洗牌加速，龙头受益", "category": "新能源", "views": 32000, "comments": 198, "symbol": "#光伏#"},
        {"id": 9, "title": "消费复苏不及预期，关注必选消费", "category": "消费", "views": 21000, "comments": 176, "symbol": "#消费#"},
        {"id": 10, "title": "央企估值重塑，这些标的值得关注", "category": "央企", "views": 15000, "comments": 154, "symbol": "#央企#"},
    ]
    return mock_posts[:limit]

def format_output(data):
    output = "📈 雪球今日热门\n\n"
    for item in data:
        views_w = f"{item['views'] / 10000:.1f}万"
        output += f"{item['id']}. {item['title']}\n"
        output += f"   📂 {item['category']} | 👁 {views_w} | 💬 {item['comments']} | {item['symbol']}\n\n"
    return output

def main():
    limit = 10
    for arg in sys.argv[1:]:
        if arg.isdigit():
            limit = int(arg)
    
    data = get_xueqiu_hot(limit=limit)
    
    if "--json" in sys.argv or "-j" in sys.argv:
        print(json.dumps({"data": data}, ensure_ascii=False, indent=2))
    else:
        print(format_output(data))

if __name__ == "__main__":
    main()
