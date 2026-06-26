#!/usr/bin/env python3
"""
K线数据获取器
从toc-trading数据适配器获取K线数据，供技术分析Skill使用
"""

import argparse
import json
import sys
import os

# 添加toc-trading路径
_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
_trading_src = os.path.join(_base, 'toc-trading', 'src')
if _trading_src not in sys.path:
    sys.path.insert(0, _trading_src)

from stock_data_adapter import StockDataAdapter


def fetch_kline(symbol: str, period: str = 'daily', count: int = 120, market: str = 'A') -> dict:
    """获取K线数据"""
    adapter = StockDataAdapter()
    
    try:
        df = adapter.get_kline(symbol, period, count)
        
        if df is None or len(df) == 0:
            return {
                'success': False,
                'error': f'获取K线数据失败: {symbol}',
                'data': []
            }
        
        # 转换为标准格式
        records = []
        for _, row in df.iterrows():
            records.append({
                'date': str(row.get('date', '')),
                'open': float(row.get('open', 0)),
                'high': float(row.get('high', 0)),
                'low': float(row.get('low', 0)),
                'close': float(row.get('close', 0)),
                'volume': float(row.get('volume', 0)),
                'amount': float(row.get('amount', 0)) if 'amount' in row else 0,
                'pct_change': float(row.get('pct_change', 0)) if 'pct_change' in row else 0,
                'turnover': float(row.get('turnover', 0)) if 'turnover' in row else 0,
            })
        
        return {
            'success': True,
            'symbol': symbol,
            'period': period,
            'count': len(records),
            'data': records
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'data': []
        }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='K线数据获取器')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--period', default='daily', 
                       choices=['1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'])
    parser.add_argument('--count', type=int, default=120, help='K线数量')
    parser.add_argument('--market', default='A', choices=['A', 'US', 'HK'])
    parser.add_argument('--output', default='/tmp/kline.json', help='输出文件')
    
    args = parser.parse_args()
    result = fetch_kline(args.symbol, args.period, args.count, args.market)
    
    # 输出到文件
    with open(args.output, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 打印摘要
    if result['success']:
        print(f"✅ 获取成功: {result['symbol']} {result['period']} {result['count']}根K线")
        if result['data']:
            latest = result['data'][-1]
            print(f"   最新: {latest['date']} 收={latest['close']} 涨={latest['pct_change']:+.2f}%")
    else:
        print(f"❌ 获取失败: {result.get('error', '未知错误')}")
