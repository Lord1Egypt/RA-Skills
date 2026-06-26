#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量查询多只股票
用法: python batch_query.py <股票代码1> <股票代码2> ...
示例: python batch_query.py 002475 000063 002241
"""

import sys
import subprocess
import re

def get_stock_price(stock_code):
    """获取单只股票实时价格"""
    url = f"https://qt.gtimg.cn/q={stock_code}"
    
    try:
        result = subprocess.run(
            ["curl", "-s", url],
            capture_output=True
        )
        
        try:
            data = result.stdout.decode('gbk', errors='ignore').strip()
        except:
            data = result.stdout.decode('utf-8', errors='ignore').strip()
        
        if not data or "v_" not in data:
            return None
            
        match = re.search(r'"([^"]+)"', data)
        if not match:
            return None
            
        fields = match.group(1).split("~")
        
        if len(fields) < 35:
            return None
            
        return {
            "name": fields[1],
            "code": fields[2],
            "price": float(fields[3]),
            "yesterday_close": float(fields[4]),
            "change_percent": float(fields[32]) if fields[32] else 0,
        }
        
    except Exception as e:
        return None

def normalize_code(code):
    """标准化股票代码"""
    code = code.strip()
    if code.startswith(("sz", "sh")):
        return code
    if code.startswith(("6", "5", "9")):
        return f"sh{code}"
    return f"sz{code}"

def main():
    if len(sys.argv) < 2:
        print("用法: python batch_query.py <代码1> <代码2> ...")
        print("示例: python batch_query.py 002475 000063 002241")
        sys.exit(1)
    
    codes = [normalize_code(c) for c in sys.argv[1:]]
    
    print(f"\n{'='*60}")
    print(f"{'股票名称':<12}{'代码':<10}{'现价':>10}{'涨跌':>10}")
    print(f"{'='*60}")
    
    total_change = 0
    count = 0
    
    for code in codes:
        data = get_stock_price(code)
        if data:
            change_str = f"{data['change_percent']:+.2f}%"
            change_emoji = "📈" if data['change_percent'] >= 0 else "📉"
            print(f"{data['name']:<12}{data['code']:<10}{data['price']:>10.2f}{change_emoji}{change_str:>8}")
            total_change += data['change_percent']
            count += 1
        else:
            print(f"{'--':<12}{code:<10}{'--':>10}{'--':>10}")
    
    print(f"{'='*60}")
    if count > 0:
        avg_change = total_change / count
        avg_emoji = "📈" if avg_change >= 0 else "📉"
        print(f"平均涨跌: {avg_emoji} {avg_change:+.2f}%")
    print()

if __name__ == "__main__":
    main()
