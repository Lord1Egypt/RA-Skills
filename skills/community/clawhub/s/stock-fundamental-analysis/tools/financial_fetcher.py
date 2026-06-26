#!/usr/bin/env python3
"""
财务数据获取器
从toc-trading数据适配器获取基本面数据
"""

import argparse
import json
import sys
import os

_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
_trading_src = os.path.join(_base, 'toc-trading', 'src')
if _trading_src not in sys.path:
    sys.path.insert(0, _trading_src)

from stock_data_adapter import StockDataAdapter


def fetch_financial(symbol: str) -> dict:
    """获取基本面数据"""
    adapter = StockDataAdapter()
    
    try:
        # 获取实时行情（包含PE/PB/市值）
        quote = adapter.get_realtime_quote(symbol)
        
        # 获取K线数据（用于计算历史走势）
        kline = adapter.get_kline(symbol, period='daily', count=250)  # 约一年数据
        
        result = {
            'success': True,
            'symbol': symbol,
            'name': quote.get('name', ''),
            'current_price': quote.get('price', 0),
            'pe': quote.get('pe', 0),
            'pb': quote.get('pb', 0),
            'mkt_cap': quote.get('mkt_cap', 0),  # 总市值
            'price_change': quote.get('change', 0),
            'high_52w': None,
            'low_52w': None,
            'volume': quote.get('volume', 0),
            'timestamp': quote.get('timestamp', ''),
        }
        
        # 计算52周高低
        if kline is not None and len(kline) > 0:
            highs = kline['high'].max() if 'high' in kline.columns else None
            lows = kline['low'].min() if 'low' in kline.columns else None
            result['high_52w'] = round(highs, 2) if highs else None
            result['low_52w'] = round(lows, 2) if lows else None
            
            # 计算一年涨跌幅
            if len(kline) >= 250:
                price_1y_ago = kline['close'].iloc[-250]
                current = quote.get('price', 0)
                if price_1y_ago > 0:
                    result['change_1y'] = round((current - price_1y_ago) / price_1y_ago * 100, 2)
        
        # 估值评价（简化版）
        pe = result['pe']
        if pe and pe > 0:
            if pe < 15:
                pe_comment = '偏低'
            elif pe < 30:
                pe_comment = '合理'
            elif pe < 50:
                pe_comment = '偏高'
            else:
                pe_comment = '极高'
        else:
            pe_comment = '无数据'
        result['pe_comment'] = pe_comment
        
        return result
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'symbol': symbol
        }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='财务数据获取器')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--output', default='/tmp/financial.json', help='输出文件')
    
    args = parser.parse_args()
    result = fetch_financial(args.symbol)
    
    with open(args.output, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    if result['success']:
        print(f"✅ 基本面数据获取成功: {result['name']} ({result['symbol']})")
        print(f"   现价: {result['current_price']} | PE: {result['pe']} | PB: {result['pb']}")
        print(f"   市值: {result['mkt_cap']/1e8:.2f}亿" if result['mkt_cap'] else "   市值: 无数据")
    else:
        print(f"❌ 获取失败: {result.get('error')}")
