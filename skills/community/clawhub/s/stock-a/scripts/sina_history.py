#!/usr/bin/env python3
"""
新浪财经历史K线
用法: python sina_history.py <股票代码> <开始日期> <结束日期>
示例: python sina_history.py sh600519 20240101 20240325
"""
import sys
import requests
import json
import urllib.parse

def get_history(code, start_date, end_date):
    # scale: 240=日线, 1440=周线, 4320=月线
    url = "https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData"
    params = {
        "symbol": code,
        "scale": "240",
        "ma": "no",
        "datalen": "1024"
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://finance.sina.com.cn/'
    }
    
    r = requests.get(url, params=params, headers=headers, timeout=10)
    data = r.json()
    
    if not isinstance(data, list):
        return {"error": data.get("error", "获取失败")}
    
    # 筛选日期范围 (日期格式: 2026-01-06)
    start = start_date.replace('/', '-')
    end = end_date.replace('/', '-')
    
    result = []
    for item in data:
        day = item.get('day', '')
        # 处理日期格式转换 20240301 -> 2024-03-01
        if len(day) == 10:
            if start <= day <= end:
                result.append({
                    "date": day,
                    "open": float(item.get('open', 0)),
                    "high": float(item.get('high', 0)),
                    "low": float(item.get('low', 0)),
                    "close": float(item.get('close', 0)),
                    "volume": int(item.get('volume', 0))
                })
    
    return result[:500]  # 限制返回数量

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python sina_history.py <股票代码> <开始日期> <结束日期>")
        print("示例: python sina_history.py sh600519 2024-03-01 2024-03-25")
        sys.exit(1)
    
    code = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    
    result = get_history(code, start_date, end_date)
    
    if "error" in result:
        print(f"错误: {result['error']}")
        sys.exit(1)
    
    print(f"获取到 {len(result)} 条K线数据")
    print(json.dumps(result[:5], ensure_ascii=False, indent=2))
    if len(result) > 5:
        print("...")
