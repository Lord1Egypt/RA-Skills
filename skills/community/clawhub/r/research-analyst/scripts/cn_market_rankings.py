#!/usr/bin/env python3
import json, urllib.request, urllib.parse, time, sys

BASE = 'https://push2.eastmoney.com/api/qt/clist/get'
HEADERS = {
    'Referer': 'https://quote.eastmoney.com/center/gridlist.html',
    'User-Agent': 'Mozilla/5.0'
}

# Common fields: f12=代码 f14=名称 f2=最新价 f3=涨跌幅% f6=成交额
FIELDS = 'f12,f14,f2,f3,f6'

def fetch_list(fs, fid='f3', pn=1, pz=20, max_retries=3):
    """
    Fetch list with retry mechanism
    
    Args:
        fs: Market filter string
        fid: Sort field
        pn: Page number
        pz: Page size
        max_retries: Maximum retry attempts
    
    Returns:
        List of stocks or empty list on failure
    """
    params = {
        'pn': pn,
        'pz': pz,
        'po': 1,
        'np': 1,
        'fltt': 2,
        'invt': 2,
        'fid': fid,  # sort field
        'fs': fs,
        'fields': FIELDS
    }
    url = BASE + '?' + urllib.parse.urlencode(params)
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            # Increased timeout from 10 to 30 seconds
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode('utf-8', 'ignore'))
            
            items = (data.get('data') or {}).get('diff') or []
            out = []
            for it in items:
                out.append({
                    'code': it.get('f12'),
                    'name': it.get('f14'),
                    'price': it.get('f2'),
                    'pct': it.get('f3'),
                    'amount': it.get('f6'),
                })
            return out
            
        except urllib.error.URLError as e:
            if attempt == max_retries - 1:
                print(f"Error fetching {fid} list after {max_retries} attempts: {e}", file=sys.stderr)
                return []
            
            wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
            print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s...", file=sys.stderr)
            time.sleep(wait_time)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return []
    
    return []


def main():
    # A股：沪深A（上/深）：fs=m:1 t:2,m:1 t:23
    a_fs = 'm:1 t:2,m:1 t:23'
    a_top_gainers = fetch_list(a_fs, fid='f3', pz=20)
    a_top_amount = fetch_list(a_fs, fid='f6', pz=20)

    # 港股（主板）：常用 fs=m:116 t:3（主板），创业板 t:4；这里聚合主板+创业板
    hk_fs = 'm:116 t:3,m:116 t:4'
    try:
        hk_top_gainers = fetch_list(hk_fs, fid='f3', pz=20)
        hk_top_amount = fetch_list(hk_fs, fid='f6', pz=20)
    except:
        hk_top_gainers = []
        hk_top_amount = []

    result = {
        'a_share': {
            'top_gainers': a_top_gainers,
            'top_amount': a_top_amount
        },
        'hong_kong': {
            'top_gainers': hk_top_gainers,
            'top_amount': hk_top_amount
        }
    }

    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
