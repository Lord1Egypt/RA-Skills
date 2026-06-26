#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新浪财经数据源 - Sina Finance Data Source
免费、无需API Key、稳定可靠的A股行情数据
接口说明：
- 实时行情: https://hq.sinajs.cn/list={codes}
- 历史K线: https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData
- 日K线: akshare内部也封装了新浪接口
"""

import re
import io
import sys
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any, Tuple

# Windows UTF-8
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import pandas as pd
    import requests
except ImportError:
    print("pip install pandas requests")
    sys.exit(1)


def convert_symbol_to_sina(symbol: str) -> str:
    """Convert stock code to Sina format.
    
    Examples:
        002475 -> sz002475
        600519 -> sh600519
        002475.SZ -> sz002475
        600519.SH -> sh600519
    """
    code = symbol.upper().replace('.SZ', '').replace('.SH', '').replace('.SS', '')
    if code.startswith(('6', '9', '5', '7')):
        return f'sh{code}'
    else:
        return f'sz{code}'


def fetch_realtime_quote(symbol: str) -> Optional[Dict[str, Any]]:
    """Fetch real-time quote from Sina Finance.
    
    Returns dict with: name, open, high, low, close, volume, amount, 
                       change, change_pct, date, time
    """
    sina_code = convert_symbol_to_sina(symbol)
    url = f'https://hq.sinajs.cn/list={sina_code}'
    
    headers = {
        'Referer': 'https://finance.sina.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = 'gbk'
        
        # Parse response: var hq_str_sz002475="立讯精密,59.14,58.70,..."
        match = re.search(r'"(.+)"', resp.text)
        if not match:
            return None
        
        fields = match.group(1).split(',')
        if len(fields) < 32:
            return None
        
        open_price = float(fields[1])
        yesterday_close = float(fields[2])
        current = float(fields[3])
        high = float(fields[4])
        low = float(fields[5])
        volume = int(fields[8])
        amount = float(fields[9])
        
        change = current - yesterday_close
        change_pct = (change / yesterday_close) * 100 if yesterday_close != 0 else 0
        
        return {
            'name': fields[0],
            'open': open_price,
            'yesterday_close': yesterday_close,
            'close': current,
            'high': high,
            'low': low,
            'volume': volume,
            'amount': amount,
            'change': round(change, 2),
            'change_pct': round(change_pct, 2),
            'date': fields[30],
            'time': fields[31]
        }
    except Exception as e:
        print(f"Sina realtime failed: {e}")
        return None


def fetch_kline(symbol: str, period: str = "6mo") -> Optional[pd.DataFrame]:
    """Fetch historical K-line data from Sina Finance.
    
    Args:
        symbol: Stock code (e.g., '002475', '600519.SH')
        period: '1mo', '3mo', '6mo', '1y'
    
    Returns:
        DataFrame with columns: date, open, high, low, close, volume, amount
        Indexed by date
    """
    sina_code = convert_symbol_to_sina(symbol)
    
    # Date range
    period_days = {'1mo': 30, '3mo': 90, '6mo': 180, '1y': 365, '2y': 730}
    days = period_days.get(period, 180)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=int(days * 1.2))  # extra buffer for non-trading days
    
    url = 'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData'
    params = {
        'symbol': sina_code,
        'scale': '240',     # daily (240 min = 1 day)
        'ma': 'no',
        'datalen': str(days),
    }
    
    headers = {
        'Referer': 'https://finance.sina.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    session = requests.Session()
    
    try:
        resp = session.get(url, params=params, headers=headers, timeout=15)
        
        # Response is JSON array directly (no wrapper)
        if resp.status_code != 200 or not resp.text.strip():
            return None
        
        # Handle potential JSONP or BOM
        text = resp.text.strip()
        if text.startswith('['):
            data = pd.read_json(io.StringIO(text))
        else:
            # Try parsing as JSON
            import json
            parsed = json.loads(text)
            data = pd.DataFrame(parsed)
        
        if data.empty:
            return None
        
        # Standardize column names
        col_map = {
            'day': 'date',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume'
        }
        data = data.rename(columns={k: v for k, v in col_map.items() if k in data.columns})
        
        if 'date' not in data.columns or 'close' not in data.columns:
            return None
        
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date')
        data = data.sort_index()
        
        # Filter by date range
        data = data[data.index >= start_date]
        
        # Ensure numeric types
        for col in ['open', 'high', 'low', 'close', 'volume']:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
        
        # Fill missing columns
        if 'volume' not in data.columns:
            data['volume'] = 0
        
        return data[['open', 'high', 'low', 'close', 'volume']]
        
    except Exception as e:
        print(f"Sina K-line failed: {e}")
        return None
    finally:
        session.close()


def fetch_batch_realtime(symbols: List[str]) -> Dict[str, Dict[str, Any]]:
    """Fetch realtime quotes for multiple stocks in one request.
    
    Args:
        symbols: List of stock codes
    
    Returns:
        Dict mapping symbol -> quote data
    """
    sina_codes = [convert_symbol_to_sina(s) for s in symbols]
    url = f'https://hq.sinajs.cn/list={",".join(sina_codes)}'
    
    headers = {
        'Referer': 'https://finance.sina.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    results = {}
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.encoding = 'gbk'
        
        for symbol, sina_code in zip(symbols, sina_codes):
            # Extract relevant line
            pattern = rf'hq_str_{sina_code}="([^"]*)"'
            match = re.search(pattern, resp.text)
            if match:
                fields = match.group(1).split(',')
                if len(fields) >= 32:
                    current = float(fields[3])
                    yesterday_close = float(fields[2])
                    change = current - yesterday_close
                    change_pct = (change / yesterday_close) * 100 if yesterday_close != 0 else 0
                    
                    results[symbol] = {
                        'name': fields[0],
                        'open': float(fields[1]),
                        'close': current,
                        'high': float(fields[4]),
                        'low': float(fields[5]),
                        'volume': int(fields[8]),
                        'amount': float(fields[9]),
                        'change': round(change, 2),
                        'change_pct': round(change_pct, 2),
                        'date': fields[30],
                        'time': fields[31]
                    }
    except Exception as e:
        print(f"Sina batch failed: {e}")
    
    return results


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Sina Finance Data Source')
    parser.add_argument('symbol', help='Stock code (e.g., 002475, 600519)')
    parser.add_argument('--mode', choices=['quote', 'kline', 'batch'], default='quote', help='Data mode')
    parser.add_argument('--period', default='6mo', help='K-line period')
    parser.add_argument('--symbols', nargs='+', help='Multiple symbols for batch mode')
    
    args = parser.parse_args()
    
    if args.mode == 'quote':
        result = fetch_realtime_quote(args.symbol)
        if result:
            for k, v in result.items():
                print(f"{k}: {v}")
        else:
            print("Failed to fetch quote")
    
    elif args.mode == 'kline':
        df = fetch_kline(args.symbol, args.period)
        if df is not None:
            print(f"Data source: Sina Finance")
            print(f"Records: {len(df)}")
            print(f"\nLatest 5:")
            print(df.tail())
        else:
            print("Failed to fetch K-line data")
    
    elif args.mode == 'batch':
        symbols = args.symbols or ['002475', '002594', '600519']
        results = fetch_batch_realtime(symbols)
        for sym, data in results.items():
            print(f"{sym}: {data.get('name')} - {data['close']} ({data['change_pct']}%)")
