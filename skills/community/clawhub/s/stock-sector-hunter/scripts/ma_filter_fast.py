#!/usr/bin/env python3
"""
均线多头选股器 - 并行加速版
MA5 > MA10 且 MA5向上、MA10向上
"""

import akshare as ak
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import os

def check_stock(code):
    """检查单只股票"""
    symbol = f'sz{code}' if code.startswith('00') else f'sh{code}'
    try:
        df = ak.stock_zh_a_daily(symbol=symbol, adjust='qfq')
        if df is None or len(df) < 15:
            return None
        
        df['ma5'] = df['close'].rolling(window=5).mean()
        df['ma10'] = df['close'].rolling(window=10).mean()
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        if latest['ma5'] > latest['ma10'] and \
           latest['ma5'] > prev['ma5'] and \
           latest['ma10'] > prev['ma10']:
            return {
                'code': code,
                'close': round(latest['close'], 2),
                'ma5': round(latest['ma5'], 2),
                'ma10': round(latest['ma10'], 2)
            }
    except:
        pass
    return None


def main():
    print("=" * 60, flush=True)
    print("📊 均线多头选股器 | MA5 > MA10 且 均向上", flush=True)
    print("=" * 60, flush=True)
    
    # 获取股票列表
    df = ak.stock_info_a_code_name()
    mask = df['code'].str.startswith('00') | df['code'].str.startswith('60')
    codes = df[mask]['code'].tolist()
    total = len(codes)
    
    print(f"\n📋 共 {total} 只 00/60 开头股票，使用10线程扫描...\n", flush=True)
    
    results = []
    completed = 0
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_stock, code): code for code in codes}
        
        for future in as_completed(futures):
            completed += 1
            if completed % 500 == 0:
                print(f"  🔄 {completed}/{total} ... 发现 {len(results)} 只\n", flush=True)
            
            result = future.result()
            if result:
                results.append(result)
    
    # 排序输出
    results.sort(key=lambda x: x['code'])
    
    print(f"\n{'='*60}", flush=True)
    print(f"📊 扫描完成：共找到 {len(results)} 只股票", flush=True)
    print(f"   条件：MA5 > MA10（金叉多头）且 MA5向上 且 MA10向上", flush=True)
    print(f"{'='*60}\n", flush=True)
    
    if results:
        # 保存到文件
        with open('/tmp/ma_stocks.txt', 'w') as f:
            f.write(f"{len(results)}\n")
            for r in results:
                f.write(f"{r['code']},{r['close']},{r['ma5']},{r['ma10']}\n")
        
        print(f"{'代码':<8} {'現价':>8} {'MA5':>8} {'MA10':>8}\n", flush=True)
        print("-" * 40, flush=True)
        for r in results:
            print(f"{r['code']:<8} {r['close']:>8.2f} {r['ma5']:>8.2f} {r['ma10']:>8.2f}", flush=True)
    
    print(f"\n⚠️ 免责声明：以上内容仅供参考，不构成投资建议。", flush=True)


if __name__ == "__main__":
    main()