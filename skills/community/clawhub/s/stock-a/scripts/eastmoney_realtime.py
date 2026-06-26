#!/usr/bin/env python3
"""
东方财富实时行情 (通过同花顺接口)
用法: python eastmoney_realtime.py <股票代码>
示例: python eastmoney_realtime.py sh600519
"""
import sys
import requests
import json

def get_realtime(code):
    # 转换代码格式
    if code.startswith('sh'):
        secid = f"1.{code[2:]}"
    elif code.startswith('sz'):
        secid = f"0.{code[2:]}"
    else:
        return {"error": "代码格式错误"}
    
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "secid": secid,
        "fields": "f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f57,f58,f59,f60,f116,f117,f118,f162,f167,f168,f169,f170,f171,f173,f177"
    }
    
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    
    if data.get("data") is None:
        return {"error": "未获取到数据"}
    
    d = data["data"]
    
    return {
        "code": code,
        "name": d.get("f58", ""),
        "price": d.get("f43", 0) / 100,  # 分转元
        "change": d.get("f46", 0) / 100,
        "pct_change": d.get("f45", 0) / 100,
        "volume": d.get("f47", 0),
        "amount": d.get("f48", 0) / 100000000,  # 亿元
        "open": d.get("f50", 0) / 100,
        "high": d.get("f44", 0) / 100,
        "low": d.get("f45", 0) / 100,
        "pre_close": d.get("f52", 0) / 100,
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python eastmoney_realtime.py <股票代码>")
        print("示例: python eastmoney_realtime.py sh600519")
        sys.exit(1)
    
    code = sys.argv[1]
    result = get_realtime(code)
    
    if "error" in result:
        print(f"错误: {result['error']}")
        sys.exit(1)
    
    print(f"{result['name']} ({result['code'].upper()})")
    print("=" * 30)
    print(f"最新价: {result['price']:.2f}")
    print(f"涨跌: {result['change']:+.2f}")
    print(f"涨跌幅: {result['pct_change']:+.2f}%")
    print(f"开盘: {result['open']:.2f}")
    print(f"最高: {result['high']:.2f}")
    print(f"最低: {result['low']:.2f}")
    print(f"成交量: {result['volume']:,}手")
    print(f"成交额: {result['amount']:.2f}亿")
