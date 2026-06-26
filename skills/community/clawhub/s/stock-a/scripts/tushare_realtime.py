#!/usr/bin/env python3
"""
Tushare普通接口实时行情 (即将停用,作为备用)
用法: python tushare_realtime.py <股票代码>
示例: python tushare_realtime.py 600519
"""
import sys
import tushare as ts
import warnings
warnings.filterwarnings('ignore')

def get_realtime(code):
    # 代码转换 600519 -> 600519
    if '.' in code:
        code = code.split('.')[0].replace('sh', '').replace('sz', '')
    
    try:
        df = ts.get_realtime_quotes(code)
        if df.empty:
            return {"error": "未获取到数据"}
        
        row = df.iloc[0]
        price = float(row['price'])
        pre_close = float(row['pre_close'])
        change = price - pre_close
        pct_change = (change / pre_close * 100) if pre_close else 0
        
        return {
            "code": code,
            "name": row['name'],
            "price": price,
            "change": round(change, 2),
            "pct_change": round(pct_change, 2),
            "open": float(row['open']),
            "high": float(row['high']),
            "low": float(row['low']),
            "volume": int(float(row['volume'])),
            "amount": float(row['amount']) / 10000,  # 万元
            "pre_close": pre_close,
            "warning": "此接口即将停用,建议使用Pro版"
        }
    except Exception as e:
        return {"error": str(e)[:50]}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python tushare_realtime.py <股票代码>")
        print("示例: python tushare_realtime.py 600519")
        sys.exit(1)
    
    code = sys.argv[1]
    result = get_realtime(code)
    
    if "error" in result:
        print(f"错误: {result['error']}")
        sys.exit(1)
    
    print(f"{result['name']} ({result['code']})")
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
    print("⚠️", result.get("warning", ""))
