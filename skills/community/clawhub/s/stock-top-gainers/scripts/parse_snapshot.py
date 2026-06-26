#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从同花顺问财页面提取近 10 日涨幅排名数据

通过 OpenClaw browser snapshot 获取数据，解析表格并输出 JSON
"""

import sys
import json
import re


def parse_wencai_snapshot(snapshot_text: str) -> list:
    """
    从 browser snapshot 文本中解析股票数据
    
    解析格式：
    row "1 920028 新恒泰 22.70 141.49 1/850 141.49" [ref=e212]:
      - cell "1" [ref=e213]: "1"
      - cell "920028" [ref=e218]: "920028"
      - cell "新恒泰" [ref=e220]: ...
      - cell "22.70" [ref=e223]: "22.70"
      - cell "141.49" [ref=e225]: "141.49"
    
    返回：
    [
        {
            "排名": 1,
            "股票代码": "920028",
            "股票简称": "新恒泰",
            "收盘价": 22.70,
            "10 日涨幅": 141.49,
            "排名信息": "1/850",
            "今日涨跌": 141.49
        },
        ...
    ]
    """
    stocks = []
    
    # 匹配 row 行，提取股票数据
    # 格式：row "排名 代码 名称 现价 今日涨跌 排名信息 10 日涨幅"
    row_pattern = r'row "(\d+)\s+(\d{6})\s+([^"]+)\s+([\d.]+)\s+([-\d.]+)\s+(\d+/\d+)\s+([-\d.]+)"'
    
    for match in re.finditer(row_pattern, snapshot_text):
        rank = int(match.group(1))
        code = match.group(2)
        name = match.group(3).strip()
        price = float(match.group(4))
        today_change = float(match.group(5))
        rank_info = match.group(6)
        gain_10d = float(match.group(7))
        
        # 排除 ST 股票
        if 'ST' in name.upper():
            continue
        
        stocks.append({
            "排名": rank,
            "股票代码": code,
            "股票简称": name,
            "收盘价": price,
            "10 日涨幅": gain_10d,
            "今日涨跌": today_change,
            "排名信息": rank_info,
        })
    
    return stocks


def main():
    """主函数：从 stdin 读取 snapshot 数据，输出解析后的股票列表"""
    try:
        # 从 stdin 读取 snapshot 数据
        snapshot_text = sys.stdin.read()
        
        if not snapshot_text.strip():
            print(json.dumps([], ensure_ascii=False))
            return
        
        # 解析数据
        stocks = parse_wencai_snapshot(snapshot_text)
        
        # 按 10 日涨幅排序（从高到低）
        stocks.sort(key=lambda x: x["10 日涨幅"], reverse=True)
        
        # 取前 20 只
        top_20 = stocks[:20]
        
        # 输出 JSON
        print(json.dumps(top_20, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        print(json.dumps([], ensure_ascii=False))


if __name__ == "__main__":
    main()
