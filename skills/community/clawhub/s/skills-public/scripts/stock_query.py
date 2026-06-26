#!/usr/bin/env python3
"""
股票查询工具 - 使用 web 搜索获取股票信息
当直接 API 不可用时，通过搜索获取股票数据

Usage:
    python stock_query.py <symbol>
"""

import sys
import json

def format_query(symbol):
    """格式化搜索查询"""
    symbol = symbol.upper().strip()
    return f"{symbol} 股票 实时行情 股价 涨跌幅"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python stock_query.py <股票代码>")
        print("提示：此脚本需要配合 web 搜索技能使用")
        sys.exit(1)
    
    symbol = sys.argv[1]
    query = format_query(symbol)
    
    # 输出搜索查询，供上层调用
    output = {
        'action': 'web_search',
        'query': query,
        'symbol': symbol,
    }
    
    print(json.dumps(output, ensure_ascii=False))
