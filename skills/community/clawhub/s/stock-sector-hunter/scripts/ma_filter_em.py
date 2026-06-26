#!/usr/bin/env python3
"""
均线多头选股器 - 东方财富API直连版
更快的方式获取数据
"""

import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def get_ma_data_eastmoney(code, market):
    """使用东方财富API获取单只股票数据"""
    try:
        # 东财API获取股票日线数据
        url = f"http://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            "secid": f"{market}.{code}",
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": "101",  # 日线
            "fqt": "1",    # 前复权
            "beg": "20250501",
            "end": "20260630",
            "lmt": "20"    # 只取最近20天
        }
        
        resp = requests.get(url, params=params, timeout=5)
        data = resp.json()
        
        if data.get('data') and data['data'].get('klines'):
            klines = data['data']['klines']
            if len(klines) < 15:
                return None
            
            # 解析数据
            dates = []
            closes = []
            for kline in klines:
                parts = kline.split(',')
                dates.append(parts[0])
                closes.append(float(parts[2]))
            
            # 计算MA
            closes_series = pd.Series(closes)
            ma5 = closes_series.rolling(5).mean().iloc[-1]
            ma10 = closes_series.rolling(10).mean().iloc[-1]
            ma5_prev = closes_series.rolling(5).mean().iloc[-2]
            ma10_prev = closes_series.rolling(10).mean().iloc[-2]
            
            if ma5 > ma10 and ma5 > ma5_prev and ma10 > ma10_prev:
                return {
                    'code': code,
                    'close': closes[-1],
                    'ma5': round(ma5, 2),
                    'ma10': round(ma10, 2)
                }
    except Exception as e:
        pass
    return None


def get_stock_list():
    """获取00和60开头的股票列表"""
    # 使用东财的板块数据
    url = "http://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23",
        "fields": "f12,f14"
    }
    
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()
    
    stocks = []
    if data.get('data') and data['data'].get('diff'):
        for item in data['data']['diff']:
            code = item.get('f12', '')
            name = item.get('f14', '')
            if code.startswith('00') or code.startswith('60'):
                market = '0' if code.startswith('60') else '1'
                stocks.append((code, market, name))
    
    return stocks


def main():
    print("=" * 60)
    print("📊 均线多头选股器 | 东财API直连版")
    print("=" * 60)
    
    print("\n📋 获取股票列表...")
    stocks = get_stock_list()
    print(f"   共获取 {len(stocks)} 只股票\n")
    
    results = []
    total = len(stocks)
    completed = 0
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(get_ma_data_eastmoney, code, market): (code, market) 
                   for code, market, name in stocks}
        
        for future in as_completed(futures):
            completed += 1
            if completed % 500 == 0:
                print(f"  🔄 {completed}/{total} ... 发现 {len(results)} 只")
            
            result = future.result()
            if result:
                # 获取名称
                code = result['code']
                for c, m, name in stocks:
                    if c == code:
                        result['name'] = name
                        break
                results.append(result)
    
    results.sort(key=lambda x: x['code'])
    
    print(f"\n{'='*60}")
    print(f"📊 扫描完成：共找到 {len(results)} 只股票")
    print(f"   条件：MA5 > MA10 且 MA5向上 且 MA10向上")
    print(f"{'='*60}\n")
    
    if results:
        print(f"{'代码':<8} {'名称':<10} {'现价':>8} {'MA5':>8} {'MA10':>8}")
        print("-" * 50)
        for r in results:
            name = r.get('name', '')
            if len(name) > 8:
                name = name[:8]
            print(f"{r['code']:<8} {name:<10} {r['close']:>8.2f} {r['ma5']:>8.2f} {r['ma10']:>8.2f}")
    
    print(f"\n⚠️ 免责声明：以上内容仅供参考，不构成投资建议。")


if __name__ == "__main__":
    main()