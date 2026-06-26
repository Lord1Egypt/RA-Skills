#!/usr/bin/env python3
"""
新浪财经实时行情
用法: python sina_realtime.py <股票代码>
示例: python sina_realtime.py sh600519
"""
import sys
import requests
import json

def get_realtime(code):
    url = f"https://hq.sinajs.cn/list={code}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://finance.sina.com.cn/'
    }
    
    r = requests.get(url, headers=headers, timeout=10)
    text = r.text
    
    if 'var hq_str_' not in text:
        return {"error": "未获取到数据"}
    
    # 解析: 贵州茅台,1410.110,1407.330,1408.810,1417.870,1401.010,1408.810,1409.270,1573458,221...
    data = text.split('"')[1].split(',')
    
    if len(data) < 10:
        return {"error": "数据格式错误"}
    
    name = data[0]
    open_price = float(data[1])
    pre_close = float(data[2])
    price = float(data[3])
    high = float(data[4])
    low = float(data[5])
    volume = int(float(data[7]))  # 处理可能的浮点数
    amount = float(data[8]) / 10000  # 亿元
    
    change = price - pre_close
    pct_change = (change / pre_close) * 100
    
    return {
        "code": code,
        "name": name,
        "price": price,
        "open": open_price,
        "pre_close": pre_close,
        "high": high,
        "low": low,
        "change": round(change, 2),
        "pct_change": round(pct_change, 2),
        "volume": volume,
        "amount": round(amount, 2)
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python sina_realtime.py <股票代码>")
        print("示例: python sina_realtime.py sh600519")
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
