#!/usr/bin/env python3
"""
获取同花顺个股人气排名数据

用法:
    python3 fetch_popularity.py [--limit 20]
    
示例:
    python3 fetch_popularity.py
    python3 fetch_popularity.py --limit 50
"""

import sys
import json
import argparse
from datetime import datetime


def fetch_popularity_rank(limit: int = 20) -> dict:
    """
    获取同花顺个股人气排名
    
    Args:
        limit: 获取前 N 名（默认 20）
        
    Returns:
        包含排名数据的字典
    """
    # 注意：这个脚本需要通过 browser 工具执行
    # 这里提供的是数据结构示例
    
    result = {
        "rank_type": "个股人气排名",
        "limit": limit,
        "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": "同花顺问财 iwencai.com",
        "url": "https://www.iwencai.com/unifiedwap/result?w=个股人气排名",
        "stocks": []
    }
    
    # 实际数据获取需要通过 browser 工具：
    # 1. browser navigate 到问财人气排名页面
    # 2. browser snapshot 获取页面结构
    # 3. 解析 snapshot 提取表格数据
    
    return result


def parse_snapshot(snapshot_data: dict, limit: int = 20) -> dict:
    """
    解析 browser snapshot 数据，提取人气排名
    
    Args:
        snapshot_data: browser snapshot 返回的数据
        limit: 获取前 N 名
        
    Returns:
        包含排名数据的字典
    """
    result = {
        "rank_type": "个股人气排名",
        "limit": limit,
        "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": "同花顺问财",
        "stocks": []
    }
    
    # 在 snapshot 中查找表格区域
    # 查找包含"个股热度排名"的表格
    # 遍历 rowgroup > row 提取数据
    
    # 每行数据结构：
    # - cell 1: 排名
    # - cell 2: 股票代码
    # - cell 3: 股票简称
    # - cell 4: 现价
    # - cell 5: 涨跌幅
    # - cell 6: 热度排名
    # - cell 7: 热度值
    
    return result


def format_markdown(data: dict) -> str:
    """
    将排名数据格式化为 Markdown 表格
    
    Args:
        data: 排名数据字典
        
    Returns:
        Markdown 格式的字符串
    """
    lines = [
        f"# 同花顺个股人气排名 TOP{len(data['stocks'])}",
        "",
        f"**数据日期**：{data['fetch_time']}",
        "",
        "| 排名 | 股票代码 | 股票简称 | 现价 (元) | 涨跌幅 (%) | 热度排名 | 热度值 |",
        "|------|----------|----------|-----------|------------|----------|--------|"
    ]
    
    for stock in data['stocks']:
        change = stock.get('change', '')
        if change and not change.startswith('-') and change != '0':
            change = f"+{change}"
        
        lines.append(
            f"| {stock.get('rank', '')} | {stock.get('code', '')} | "
            f"{stock.get('name', '')} | {stock.get('price', '')} | "
            f"{change} | {stock.get('hot_rank', '')} | {stock.get('hot_value', '')} |"
        )
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='获取同花顺个股人气排名')
    parser.add_argument('--limit', type=int, default=20, help='获取前 N 名（默认 20）')
    parser.add_argument('--markdown', action='store_true', help='输出 Markdown 格式')
    args = parser.parse_args()
    
    data = fetch_popularity_rank(args.limit)
    
    if args.markdown:
        print(format_markdown(data))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
