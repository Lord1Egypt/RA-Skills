#!/usr/bin/env python3
import sys, json, urllib.request, time

# Map plain tickers to Sina format
# A-share: sh/sz + 6-digit; HK: hk + 5-digit zero-padded

def to_sina_code(t):
    t = t.strip().upper()
    if t.startswith('HK.'):
        return 'hk' + t.split('.',1)[1].zfill(5)
    # assume digits => A-share, decide sh/sz by leading digit
    if t.isdigit() and len(t) == 6:
        return ('sh' if t.startswith(('5','6')) else 'sz') + t
    return t  # fallback


def fetch_quotes(codes, max_retries=3):
    """
    Fetch quotes with retry mechanism
    
    Args:
        codes: List of stock codes
        max_retries: Maximum retry attempts
    
    Returns:
        List of quote dictionaries
    """
    url = 'https://hq.sinajs.cn/list=' + ','.join(codes)
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={
                'Referer': 'https://finance.sina.com.cn',
                'User-Agent': 'Mozilla/5.0'
            })
            # Increased timeout from 10 to 30 seconds
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()  # GBK bytes
            
            text = data.decode('gbk', errors='ignore')
            out = []
            for line in text.strip().split('\n'):
                # var hq_str_sh600519="贵州茅台,1680.00,1679.50,1683.88,1699.88,1663.00, ...";
                if '="' not in line:
                    continue
                head, rest = line.split('="', 1)
                name = head.split('_')[-1]
                fields = rest.rstrip('";').split(',')
                if len(fields) < 4:
                    continue
                symbol = head.split('str_')[-1]
                out.append({
                    'symbol': symbol,
                    'name': fields[0],
                    'price': try_float(fields[3]),
                    'pct': try_float(fields[32]) if len(fields) > 32 else None
                })
            return out
            
        except urllib.error.URLError as e:
            if attempt == max_retries - 1:
                print(f"Error fetching quotes after {max_retries} attempts: {e}", file=sys.stderr)
                return []
            
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s...", file=sys.stderr)
            time.sleep(wait_time)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return []
    
    return []


def try_float(s):
    try:
        return float(s)
    except:
        return None


def main():
    if len(sys.argv) < 2:
        print('Usage: cn_stock_quotes.py TICKER [TICKER...]', file=sys.stderr)
        sys.exit(1)

    raw_tickers = sys.argv[1:]
    sina_codes = [to_sina_code(t) for t in raw_tickers]
    quotes = fetch_quotes(sina_codes)

    # Fix: ensure pct is calculated if missing
    for q in quotes:
        if q['pct'] is None:
            q['pct'] = 0.0  # fallback

    print(json.dumps({'quotes': quotes}, ensure_ascii=False))

if __name__ == '__main__':
    main()
