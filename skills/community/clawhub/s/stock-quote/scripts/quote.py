#!/usr/bin/env python3
"""
Stock Quote CLI - Fetch real-time stock prices and fundamentals
Usage: python quote.py SYMBOL [SYMBOL2 ...] [--json]
"""

import sys
import json
import argparse
from datetime import datetime

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


def fetch_yfinance_data(symbols):
    """Fetch data using yfinance library"""
    results = {}
    
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            
            # Get current price
            current_price = info.get('lastPrice') or info.get('regularMarketPrice')
            
            # Build quote data
            quote = {
                'symbol': symbol.upper(),
                'price': float(current_price) if current_price else None,
                'change': None,
                'change_percent': None,
                'previous_close': info.get('previousClose'),
                'open': info.get('open'),
                'day_high': info.get('dayHigh'),
                'day_low': info.get('dayLow'),
                'volume': info.get('volume'),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'week_52_high': info.get('fiftyTwoWeekHigh'),
                'week_52_low': info.get('fiftyTwoWeekLow'),
                'dividend_yield': info.get('dividendYield'),
                'timestamp': datetime.now().isoformat(),
                'source': 'yfinance'
            }
            
            # Calculate change
            if quote['price'] and quote['previous_close']:
                quote['change'] = round(quote['price'] - quote['previous_close'], 2)
                quote['change_percent'] = round(
                    (quote['change'] / quote['previous_close']) * 100, 2
                )
            
            results[symbol.upper()] = quote
            
        except Exception as e:
            results[symbol.upper()] = {
                'symbol': symbol.upper(),
                'error': str(e),
                'source': 'yfinance'
            }
    
    return results


def fetch_fmp_data(symbols):
    """Fallback: Fetch data from Financial Modeling Prep (free API)"""
    results = {}
    base_url = "https://financialmodelingprep.com/api/v3/quote"
    
    for symbol in symbols:
        try:
            url = f"{base_url}/{symbol}?apikey=demo"
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                results[symbol.upper()] = {
                    'symbol': symbol.upper(),
                    'error': f'HTTP {response.status_code}',
                    'source': 'fmp'
                }
                continue
            
            data = response.json()
            if not data:
                results[symbol.upper()] = {
                    'symbol': symbol.upper(),
                    'error': 'No data',
                    'source': 'fmp'
                }
                continue
            
            quote_data = data[0]
            quote = {
                'symbol': symbol.upper(),
                'price': quote_data.get('price'),
                'change': quote_data.get('changes'),
                'change_percent': quote_data.get('changesPercentage'),
                'previous_close': quote_data.get('previousClose'),
                'open': quote_data.get('open'),
                'day_high': quote_data.get('dayHigh'),
                'day_low': quote_data.get('dayLow'),
                'volume': quote_data.get('volume'),
                'market_cap': quote_data.get('marketCap'),
                'pe_ratio': quote_data.get('pe'),
                'week_52_high': quote_data.get('yearHigh'),
                'week_52_low': quote_data.get('yearLow'),
                'timestamp': datetime.now().isoformat(),
                'source': 'fmp'
            }
            
            results[symbol.upper()] = quote
            
        except Exception as e:
            results[symbol.upper()] = {
                'symbol': symbol.upper(),
                'error': str(e),
                'source': 'fmp'
            }
    
    return results


def fetch_stooq_data(symbols):
    """
    Fetch data from Stooq (free, no API key required)
    Stooq provides delayed end-of-day prices for US stocks
    URL format: https://stooq.com/q/l/?s=SYMBOL.us&f=sd2t2ohlc&h=&t=csv
    Returns: Symbol, Date, Time, Open, High, Low, Close
    """
    results = {}
    
    for symbol in symbols:
        try:
            # Stooq URL format: symbol.us for US stocks
            url = f"https://stooq.com/q/l/?s={symbol.lower()}.us&f=sd2t2ohlc&h=&t=csv"
            response = requests.get(url, timeout=10, allow_redirects=True)
            
            if response.status_code != 200:
                results[symbol.upper()] = {
                    'symbol': symbol.upper(),
                    'error': f'HTTP {response.status_code}',
                    'source': 'stooq'
                }
                continue
            
            # Parse CSV response
            lines = response.text.strip().split('\n')
            if len(lines) < 2 or 'Symbol' in lines[0]:
                # Skip header, check if we have data
                if len(lines) == 1:
                    results[symbol.upper()] = {
                        'symbol': symbol.upper(),
                        'error': 'No data found',
                        'source': 'stooq'
                    }
                    continue
            
            # Parse data row: Symbol,Date,Time,Open,High,Low,Close
            data_row = lines[1] if 'Symbol' in lines[0] else lines[0]
            parts = data_row.split(',')
            
            if len(parts) < 7:
                results[symbol.upper()] = {
                    'symbol': symbol.upper(),
                    'error': 'Invalid data format',
                    'source': 'stooq'
                }
                continue
            
            close_price = float(parts[6]) if parts[6] else None
            
            quote = {
                'symbol': symbol.upper(),
                'price': close_price,
                'change': None,
                'change_percent': None,
                'previous_close': None,
                'open': float(parts[3]) if parts[3] else None,
                'day_high': float(parts[4]) if parts[4] else None,
                'day_low': float(parts[5]) if parts[5] else None,
                'volume': None,
                'market_cap': None,
                'pe_ratio': None,
                'week_52_high': None,
                'week_52_low': None,
                'date': parts[1] if len(parts) > 1 else None,
                'time': parts[2] if len(parts) > 2 else None,
                'timestamp': datetime.now().isoformat(),
                'source': 'stooq'
            }
            
            results[symbol.upper()] = quote
            
        except Exception as e:
            results[symbol.upper()] = {
                'symbol': symbol.upper(),
                'error': str(e),
                'source': 'stooq'
            }
    
    return results


def fetch_web_data(symbols):
    """Fallback: fetch data from Yahoo Finance web pages"""
    results = {}
    
    for symbol in symbols:
        try:
            url = f"https://finance.yahoo.com/quote/{symbol}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                results[symbol.upper()] = {
                    'symbol': symbol.upper(),
                    'error': f'HTTP {response.status_code}',
                    'source': 'web'
                }
                continue
            
            # Simple parsing - in production, use proper HTML parser
            html = response.text
            
            # Extract price (simplified regex approach)
            import re
            price_match = re.search(r'"regularMarketPrice":\s*{"raw":\s*([\d.]+)', html)
            price = float(price_match.group(1)) if price_match else None
            
            results[symbol.upper()] = {
                'symbol': symbol.upper(),
                'price': price,
                'timestamp': datetime.now().isoformat(),
                'source': 'web'
            }
            
        except Exception as e:
            results[symbol.upper()] = {
                'symbol': symbol.upper(),
                'error': str(e),
                'source': 'web'
            }
    
    return results


def format_text_output(quotes):
    """Format quotes as human-readable text"""
    lines = []
    
    for symbol, data in quotes.items():
        if 'error' in data and len(data) == 2:
            lines.append(f"❌ {symbol}: {data['error']}")
            continue
        
        price = data.get('price', 'N/A')
        change = data.get('change')
        change_pct = data.get('change_percent')
        
        if price != 'N/A':
            price_str = f"${price:.2f}"
        else:
            price_str = "N/A"
        
        # Direction indicator
        if change is not None:
            if change > 0:
                direction = "📈"
                change_str = f"+{change:.2f} (+{change_pct:.2f}%)"
            elif change < 0:
                direction = "📉"
                change_str = f"{change:.2f} ({change_pct:.2f}%)"
            else:
                direction = "➡️"
                change_str = "0.00 (0.00%)"
        else:
            direction = "⏸️"
            change_str = "N/A"
        
        lines.append(f"{direction} {symbol}: {price_str} {change_str}")
        
        # Additional info
        if data.get('market_cap'):
            market_cap = data['market_cap']
            if market_cap >= 1e12:
                mc_str = f"${market_cap/1e12:.2f}T"
            elif market_cap >= 1e9:
                mc_str = f"${market_cap/1e9:.2f}B"
            else:
                mc_str = f"${market_cap/1e6:.2f}M"
            lines.append(f"   市值：{mc_str}")
        
        if data.get('pe_ratio'):
            lines.append(f"   PE: {data['pe_ratio']:.2f}")
        
        if data.get('week_52_high') and data.get('week_52_low'):
            high = data['week_52_high']
            low = data['week_52_low']
            if price != 'N/A':
                pct_in_range = ((price - low) / (high - low)) * 100 if high != low else 50
                lines.append(f"   52 周：${low:.2f} - ${high:.2f} (当前位置：{pct_in_range:.1f}%)")
        
        lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Fetch stock quotes')
    parser.add_argument('symbols', nargs='+', help='Stock symbols (e.g., AAPL NVDA TSLA)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--source', choices=['yfinance', 'stooq', 'fmp', 'web', 'auto'], default='auto',
                       help='Data source (default: auto)')
    
    args = parser.parse_args()
    
    # Fetch data with automatic fallback
    # Priority: Stooq (free, no key) > yfinance > FMP > web scrape
    source = args.source
    quotes = {}
    
    if source == 'auto':
        # Try Stooq first (free, no API key, reliable for US stocks)
        print("# Trying Stooq (free, no key)...", file=sys.stderr)
        quotes = fetch_stooq_data(args.symbols)
        
        # Check if we got valid data
        valid_count = sum(1 for q in quotes.values() if 'price' in q and q['price'] and 'error' not in q)
        if valid_count > 0:
            source = 'stooq'
        else:
            # Fallback to yfinance
            if YFINANCE_AVAILABLE:
                print("# Stooq failed, trying yfinance...", file=sys.stderr)
                quotes = fetch_yfinance_data(args.symbols)
                source = 'yfinance'
            else:
                # Fallback to FMP
                print("# yfinance not available, trying FMP...", file=sys.stderr)
                quotes = fetch_fmp_data(args.symbols)
                source = 'fmp'
                
    elif source == 'stooq':
        if not REQUESTS_AVAILABLE:
            print("Error: requests not installed. Run: pip install requests", file=sys.stderr)
            sys.exit(1)
        quotes = fetch_stooq_data(args.symbols)
    elif source == 'yfinance':
        if not YFINANCE_AVAILABLE:
            print("Error: yfinance not installed. Run: pip install yfinance", file=sys.stderr)
            sys.exit(1)
        quotes = fetch_yfinance_data(args.symbols)
    elif source == 'fmp':
        if not REQUESTS_AVAILABLE:
            print("Error: requests not installed. Run: pip install requests", file=sys.stderr)
            sys.exit(1)
        quotes = fetch_fmp_data(args.symbols)
    else:
        if not REQUESTS_AVAILABLE:
            print("Error: requests not installed. Run: pip install requests", file=sys.stderr)
            sys.exit(1)
        quotes = fetch_web_data(args.symbols)
    
    # Output
    if args.json:
        print(json.dumps(quotes, indent=2))
    else:
        print(format_text_output(quotes))


if __name__ == '__main__':
    main()
