#!/usr/bin/env python3
"""
腾讯财经实时行情
用法: python tengxun_realtime.py <股票代码>
示例: python tengxun_realtime.py sh600519
"""
import sys
import requests
import json

def get_realtime(code):
    url = f"https://qt.gtimg.cn/q={code}"
    r = requests.get(url, timeout=10)
    text = r.text
    
    if 'v_' not in text:
        return {"error": "未获取到数据"}
    
    # 解析格式: v_sh600519="1~贵州茅台~600519~1408.81~1407.33~1410.11~15735~7810~7925~1408.81~..."
    # 字段: 0市场,1名称,2代码,3当前价,4昨收,5开盘,6成交量,7成交额,8内盘,9最高,10最低...
    raw = text.split('"')[1]
    data = raw.split('~')
    
    if len(data) < 11:
        return {"error": "数据格式错误"}
    
    name = data[1]
    price = float(data[3]) if data[3] else 0
    pre_close = float(data[4]) if data[4] else 0
    open_price = float(data[5]) if data[5] else 0
    volume = int(float(data[6])) if data[6] else 0
    amount = float(data[7]) / 1000 if data[7] else 0  # 千元转为万元
    high = float(data[9]) if data[9] else 0
    low = float(data[10]) if data[10] else 0
    
    change = price - pre_close
    pct_change = (change / pre_close * 100) if pre_close else 0
    
    return {
        "code": code,
        "name": name,
        "price": price,
        "change": round(change, 2),
        "pct_change": round(pct_change, 2),
        "volume": volume,
        "amount": round(amount, 2),
        "open": open_price,
        "high": high,
        "low": low,
        "pre_close": pre_close
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python tengxun_realtime.py <股票代码>")
        print("示例: python tengxun_realtime.py sh600519")
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
    print(f"昨收: {result['pre_close']:.2f}")
    print(f"成交量: {result['volume']:,}手")
    print(f"成交额: {result['amount']:.2f}万")
