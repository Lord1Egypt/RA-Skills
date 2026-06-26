"""实战 98: 东方财富实时报价 scraper
- 公开 API: push2.eastmoney.com/api/qt/stock/get
- secid: 0.002594 (上证)/ 1.002594 (深证) / 0.00700 (港股) / 105.AAPL (美股)
- fields: f43=现价 f44=最高 f45=最低 f46=昨收 f60=今开 f170=涨跌幅(%)
- 反爬: UA + Referer
- 缓存: 5 min TTL
"""
import json
import time
import urllib.request
import urllib.error
from typing import Dict, Optional

# 实战 98: 缓存
_CACHE = {}
_CACHE_TTL = 300  # 5 min

# secid 映射 (实战 98: 从 STOCK_MAP 推导)
def get_secid(code: str, market: str) -> Optional[str]:
    """从 code + market 推 secid
    - SZ (深证) → 1.XXXXXX
    - SH (上证) / HK → 0.XXXXXX
    - US → 105.XXXX
    - CRYPTO → None (东财不支持)
    """
    if not code or code == '-':
        return None
    if market == 'SZ':
        return f'1.{code}'
    if market in ('SH', 'HK'):
        return f'0.{code}'
    if market == 'US':
        return f'105.{code}'
    return None


def fetch_quote(code: str, market: str) -> Optional[Dict]:
    """调用东财 API 获取实时报价
    返回: {price, open, high, low, prev_close, change_pct} 或 None
    """
    secid = get_secid(code, market)
    if not secid:
        return None

    # 缓存
    cache_key = f'{secid}'
    now = time.time()
    if cache_key in _CACHE:
        cached_data, cached_time = _CACHE[cache_key]
        if now - cached_time < _CACHE_TTL:
            return cached_data

    url = f'https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f44,f45,f46,f60,f170,f168,f167'
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Referer': 'https://quote.eastmoney.com/',
                'Accept': 'application/json, text/plain, */*',
            }
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode('utf-8', errors='ignore')
        data = json.loads(raw)
        if data.get('rc') != 0 or not data.get('data'):
            return None
        d = data['data']
        # f43: 现价(厘) → /100 = 元
        # f170: 涨跌幅(厘) → /100 = %
        result = {
            'price': d.get('f43', 0) / 100 if d.get('f43') else None,
            'open': d.get('f60', 0) / 100 if d.get('f60') else None,
            'high': d.get('f44', 0) / 100 if d.get('f44') else None,
            'low': d.get('f45', 0) / 100 if d.get('f45') else None,
            'prev_close': d.get('f46', 0) / 100 if d.get('f46') else None,
            'change_pct': d.get('f170', 0) / 100 if d.get('f170') else None,
            'volume': d.get('f168'),  # 成交量(手)
            'amount': d.get('f167'),  # 成交额(元)
            'timestamp': int(now),
            'source': 'eastmoney',
        }
        _CACHE[cache_key] = (result, now)
        return result
    except (urllib.error.URLError, json.JSONDecodeError, Exception) as e:
        return {'error': str(e), 'timestamp': int(now)}


def get_quote_with_real(symbol_or_name: str) -> Dict:
    """实战 98: 替代 realtime.get_quote, 真接东财 API"""
    import realtime as _rt
    # 1) 先 mock 找 code
    mock = _rt.get_quote(symbol_or_name)
    if not mock.get('success'):
        return mock

    code = mock.get('code')
    market = mock.get('market')
    if market == 'PRIVATE':
        return {
            'success': False,
            'query': symbol_or_name,
            'error': f'{mock.get("name")} 未上市, 无实时报价',
            'realtime_links': mock.get('realtime_links'),
        }

    # 2) 真接东财
    real = fetch_quote(code, market)
    if not real or 'error' in real:
        # fallback to mock
        return mock

    # 3) 合并
    return {
        'success': True,
        'query': symbol_or_name,
        'name': mock.get('name'),
        'code': code,
        'market': market,
        'quote': {
            'price': real.get('price'),
            'change_pct': real.get('change_pct'),
            'change': (real.get('price') - real.get('prev_close')) if real.get('price') and real.get('prev_close') else None,
            'open': real.get('open'),
            'high': real.get('high'),
            'low': real.get('low'),
            'prev_close': real.get('prev_close'),
            'volume': real.get('volume'),
            'timestamp': real.get('timestamp'),
            'source': 'eastmoney',
        },
        'realtime_links': mock.get('realtime_links'),
    }
