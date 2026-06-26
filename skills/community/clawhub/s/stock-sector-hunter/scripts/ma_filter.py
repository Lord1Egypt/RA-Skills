#!/usr/bin/env python3
"""
均线选股器：获取5日均线和10日均线同时向上的股票（MA5 > MA10 且向上）
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta


def get_a_stock_codes(prefix_filter="all", limit=None):
    """获取A股代码列表"""
    df = ak.stock_info_a_code_name()
    
    # 过滤 00 和 60 开头
    mask = df['code'].str.startswith('00') | df['code'].str.startswith('60')
    df = df[mask]
    
    codes = df['code'].tolist()
    if limit:
        codes = codes[:limit]
    
    return codes


def check_ma_status(symbol):
    """检查单只股票的均线状态"""
    try:
        # symbol 格式: sz000001 或 sh600001
        df = ak.stock_zh_a_daily(symbol=symbol, adjust='qfq')
        
        if df is None or len(df) < 15:
            return None
        
        # 计算均线
        df['ma5'] = df['close'].rolling(window=5).mean()
        df['ma10'] = df['close'].rolling(window=10).mean()
        
        # 取最近2天
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # 条件判断
        ma5_above_ma10 = latest['ma5'] > latest['ma10']     # MA5 > MA10
        ma5_up = latest['ma5'] > prev['ma5']               # MA5 比昨天高（向上）
        ma10_up = latest['ma10'] > prev['ma10']            # MA10 比昨天高（向上）
        
        if ma5_above_ma10 and ma5_up and ma10_up:
            return {
                'close': round(latest['close'], 2),
                'ma5': round(latest['ma5'], 2),
                'ma10': round(latest['ma10'], 2),
                'date': str(latest.name)
            }
        
        return None
        
    except Exception as e:
        return None


def main():
    print("=" * 60)
    print("📊 均线多头选股器 | 5日线 > 10日线 且 均向上")
    print("=" * 60)
    
    # 获取股票列表
    codes = get_a_stock_codes(limit=500)  # 先测500只
    print(f"\n📋 00/60 开头股票共 {len(codes)} 只，开始扫描...\n")
    
    results = []
    
    for i, code in enumerate(codes):
        # 构建 symbol
        symbol = f"sz{code}" if code.startswith('00') else f"sh{code}"
        
        if (i + 1) % 100 == 0:
            print(f"  🔄 已扫描 {i+1}/{len(codes)} ...")
        
        result = check_ma_status(symbol)
        if result:
            results.append({
                'code': code,
                **result
            })
            print(f"  ✅ {code}: 現價={result['close']}, MA5={result['ma5']}, MA10={result['ma10']}")
    
    print(f"\n{'='*60}")
    print(f"📊 扫描结果：共找到 {len(results)} 只股票")
    print(f"   条件：MA5 > MA10（金叉多头）且 MA5向上 且 MA10向上")
    print(f"{'='*60}\n")
    
    if results:
        # 按代码排序
        results.sort(key=lambda x: x['code'])
        
        print(f"{'代码':<8} {'現價':>8} {'MA5':>8} {'MA10':>8}")
        print("-" * 40)
        for r in results:
            print(f"{r['code']:<8} {r['close']:>8.2f} {r['ma5']:>8.2f} {r['ma10']:>8.2f}")
    
    print(f"\n⚠️ 免责声明：以上内容仅供参考，不构成投资建议。")


if __name__ == "__main__":
    main()