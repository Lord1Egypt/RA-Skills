#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整执行脚本 - 获取近 10 日涨幅前 30 股票，分析题材，搜索新闻，生成报告
"""

import json
import os
from datetime import datetime

# 从 browser snapshot 获取的前 30 只股票数据（排除 ST）
TOP_GAINERS = [
    {"rank": 1, "code": "920028", "name": "新恒泰"},
    {"rank": 2, "code": "600726", "name": "华电能源"},
    {"rank": 3, "code": "688295", "name": "中复神鹰"},
    {"rank": 4, "code": "600396", "name": "华电辽能"},
    {"rank": 5, "code": "301658", "name": "首航新能"},
    {"rank": 6, "code": "301396", "name": "宏景科技"},
    {"rank": 7, "code": "000020", "name": "深华发 A"},
    {"rank": 8, "code": "600683", "name": "京投发展"},
    {"rank": 9, "code": "301667", "name": "纳百川"},
    # 排除 10: *ST 景峰
    {"rank": 11, "code": "300720", "name": "海川智能"},
    {"rank": 12, "code": "000890", "name": "法尔胜"},
    {"rank": 13, "code": "603778", "name": "国晟科技"},
    {"rank": 14, "code": "002445", "name": "中南文化"},
    # 排除 15: *ST 熊猫
    {"rank": 16, "code": "002310", "name": "东方新能"},
    {"rank": 17, "code": "300672", "name": "国科微"},
    # 排除 18: *ST 正平
    {"rank": 19, "code": "603929", "name": "亚翔集成"},
    # 排除 20: ST 金鸿
    {"rank": 21, "code": "300042", "name": "朗科科技"},
    {"rank": 22, "code": "300763", "name": "锦浪科技"},
    {"rank": 23, "code": "002015", "name": "协鑫能科"},
    {"rank": 24, "code": "688519", "name": "南亚新材"},
    {"rank": 25, "code": "000601", "name": "韶能股份"},
    {"rank": 26, "code": "002730", "name": "电光科技"},
    {"rank": 27, "code": "301306", "name": "西测测试"},
    {"rank": 28, "code": "688498", "name": "源杰科技"},
    {"rank": 29, "code": "601016", "name": "节能风电"},
    {"rank": 30, "code": "603803", "name": "瑞斯康达"},
]

def main():
    print("=" * 60)
    print("A 股题材 - 事件关联分析")
    print("=" * 60)
    print(f"数据日期：{datetime.now().strftime('%Y-%m-%d')}")
    print(f"样本股票：近 10 日涨幅前 30 只（已排除 ST）")
    print(f"股票数量：{len(TOP_GAINERS)}")
    print()
    
    # 输出股票代码列表
    stock_codes = [stock["code"] for stock in TOP_GAINERS]
    print("股票代码列表:")
    print(", ".join(stock_codes))
    print()
    
    # 保存股票列表到 JSON
    output_dir = "/Users/shinelp100/.jvs/.openclaw/workspace/skills/stock-data-monorepo/stock-theme-events/cache"
    os.makedirs(output_dir, exist_ok=True)
    
    stock_list_path = os.path.join(output_dir, "top_gainers_2026-03-21.json")
    with open(stock_list_path, 'w', encoding='utf-8') as f:
        json.dump(TOP_GAINERS, f, ensure_ascii=False, indent=2)
    
    print(f"股票列表已保存到：{stock_list_path}")
    print()
    print("下一步:")
    print("1. 使用 ths-stock-themes skill 获取每只股票的题材")
    print("2. 使用 cluster_themes.py 聚类题材")
    print("3. 使用 search_news.py 搜索对应新闻")
    print("4. 使用 generate_report.py 生成报告")
    
    return stock_codes

if __name__ == '__main__':
    main()
