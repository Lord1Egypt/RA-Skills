#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取A股实时股价
用法: python get_price.py <股票代码>
示例: python get_price.py sz002475
"""

import sys
import subprocess
import re

def get_stock_price(stock_code):
    """获取单只股票实时价格"""
    url = f"https://qt.gtimg.cn/q={stock_code}"
    
    try:
        # 直接获取并解码
        result = subprocess.run(
            ["curl", "-s", url],
            capture_output=True
        )
        
        # 用GBK解码
        try:
            data = result.stdout.decode('gbk', errors='ignore').strip()
        except:
            data = result.stdout.decode('utf-8', errors='ignore').strip()
        
        # 解析数据
        if not data or "v_" not in data:
            return None
            
        # 提取数据部分
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
            "today_open": float(fields[5]),
            "volume": int(fields[6]) if fields[6] else 0,
            "high": float(fields[33]) if fields[33] else 0,
            "low": float(fields[34]) if fields[34] else 0,
            "change": float(fields[31]) if fields[31] else 0,
            "change_percent": float(fields[32]) if fields[32] else 0,
        }
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

def format_volume(vol):
    """格式化成交量"""
    if vol >= 100000000:
        return f"{vol/100000000:.2f}亿"
    elif vol >= 10000:
        return f"{vol/10000:.0f}万"
    return str(vol)

def main():
    if len(sys.argv) < 2:
        print("用法: python get_price.py <股票代码>")
        print("示例: python get_price.py sz002475")
        print("\n代码前缀:")
        print("  sz = 深圳 (如 sz000001)")
        print("  sh = 上海 (如 sh600519)")
        sys.exit(1)
    
    stock_code = sys.argv[1]
    
    # 自动添加前缀
    if not stock_code.startswith(("sz", "sh")):
        if stock_code.startswith(("6", "5", "9")):
            stock_code = f"sh{stock_code}"
        else:
            stock_code = f"sz{stock_code}"
    
    data = get_stock_price(stock_code)
    
    if not data:
        print(f"❌ 无法获取股票 {stock_code} 的数据")
        sys.exit(1)
    
    # 输出格式
    change_emoji = "📈" if data["change"] >= 0 else "📉"
    
    print(f"\n{'='*50}")
    print(f"{change_emoji} {data['name']} ({data['code']})")
    print(f"{'='*50}")
    print(f"  现价:     {data['price']:.2f}")
    print(f"  涨跌:     {data['change']:+.2f} ({data['change_percent']:+.2f}%)")
    print(f"  今开:     {data['today_open']:.2f}")
    print(f"  昨收:     {data['yesterday_close']:.2f}")
    print(f"  最高:     {data['high']:.2f}")
    print(f"  最低:     {data['low']:.2f}")
    print(f"  成交量:   {format_volume(data['volume'])}")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
