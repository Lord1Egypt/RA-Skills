#!/usr/bin/env python3
"""
港股分析脚本 - 使用腾讯财经数据源进行技术面+基本面分析

用法:
    python3 analyze_stock.py <股票代码> [--period <周期>] [--output <输出文件>]

示例:
    python3 analyze_stock.py 0700.HK
    python3 analyze_stock.py 0700.HK --period 6mo --output report.json
    python3 analyze_stock.py 9988.HK --period 1y
"""

import sys
import json
import argparse
import time
import html
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

try:
    from db import (
        ANALYSIS_CACHE_TTL_SECONDS,
        AUX_CACHE_TTL_SECONDS,
        clear_analysis_cache,
        get_cached_analysis,
        get_cached_aux,
        get_kline_df,
        get_latest_kline_date,
        init_db,
        set_cached_analysis,
        set_cached_aux,
        upsert_kline_df,
        upsert_watchlist_item,
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from db import (
        ANALYSIS_CACHE_TTL_SECONDS,
        AUX_CACHE_TTL_SECONDS,
        clear_analysis_cache,
        get_cached_analysis,
        get_cached_aux,
        get_kline_df,
        get_latest_kline_date,
        init_db,
        set_cached_analysis,
        set_cached_aux,
        upsert_kline_df,
        upsert_watchlist_item,
    )

try:
    import numpy as np
except ImportError:
    print("ERROR: numpy 未安装。请运行: pip3 install numpy", file=sys.stderr)
    sys.exit(1)

try:
    import pandas as pd
except ImportError:
    print("ERROR: pandas 未安装。请运行: pip3 install pandas", file=sys.stderr)
    sys.exit(1)


# ─────────────────────────────────────────────
#  缓存与重试机制
# ─────────────────────────────────────────────

MAX_RETRIES = 3
RETRY_BASE_DELAY = 2
ANALYSIS_CACHE_TTL = ANALYSIS_CACHE_TTL_SECONDS


# ─────────────────────────────────────────────
#  腾讯财经数据获取
# ─────────────────────────────────────────────


def normalize_stock_code(code: str) -> dict:
    """标准化股票代码，支持港股/A股/美股。"""
    raw = code.strip().upper()

    if raw.endswith('.HK'):
        digits = raw[:-3].lstrip('0') or '0'
        return {
            'market': 'HK',
            'code': digits.zfill(4) + '.HK',
            'tencent_symbol': 'hk' + digits.zfill(5),
            'exchange': 'HKEX',
        }

    if raw.startswith(('SH', 'SZ')) and len(raw) == 8 and raw[2:].isdigit():
        market = raw[:2]
        return {
            'market': market,
            'code': raw,
            'tencent_symbol': raw.lower(),
            'exchange': 'SSE' if market == 'SH' else 'SZSE',
        }

    if raw.endswith('.US'):
        symbol = raw[:-3]
        return {
            'market': 'US',
            'code': symbol,
            'tencent_symbol': 'us' + symbol,
            'exchange': 'US',
        }

    if raw.startswith('US.'):
        symbol = raw[3:]
        return {
            'market': 'US',
            'code': symbol,
            'tencent_symbol': 'us' + symbol,
            'exchange': 'US',
        }

    if raw.isdigit():
        if len(raw) <= 5:
            digits = raw.lstrip('0') or '0'
            return {
                'market': 'HK',
                'code': digits.zfill(4) + '.HK',
                'tencent_symbol': 'hk' + digits.zfill(5),
                'exchange': 'HKEX',
            }
        if len(raw) == 6:
            market = 'SH' if raw.startswith(('5', '6', '9')) else 'SZ'
            return {
                'market': market,
                'code': market + raw,
                'tencent_symbol': (market + raw).lower(),
                'exchange': 'SSE' if market == 'SH' else 'SZSE',
            }

    symbol = raw.replace('.', '').replace('-', '')
    return {
        'market': 'US',
        'code': symbol,
        'tencent_symbol': 'us' + symbol,
        'exchange': 'US',
    }


def fetch_tencent_quote(code: str) -> dict:
    """获取腾讯财经实时行情"""
    stock = normalize_stock_code(code)
    symbol = stock['tencent_symbol']
    url = f"http://qt.gtimg.cn/q={symbol}"

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://gu.qq.com/',
            })
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read().decode('gb2312', errors='ignore')
                return _parse_tencent_quote(data, symbol, stock)
        except urllib.error.URLError as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BASE_DELAY * (attempt + 1))
            else:
                raise Exception(f"获取实时行情失败: {e}")
    return {}


def fetch_eastmoney_quote(code: str) -> dict:
    """获取东方财富实时行情（当前仅作为 A 股 fallback）。"""
    stock = normalize_stock_code(code)
    if stock['market'] not in ('SH', 'SZ') or len(stock['code']) != 8:
        return {}

    raw_code = stock['code'][2:]
    secid_prefix = '1' if stock['market'] == 'SH' else '0'
    fields = 'f43,f44,f45,f46,f57,f58,f60,f116,f164,f167,f168,f169,f170'
    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid_prefix}.{raw_code}&fields={fields}"

    def scaled(value, digits=100):
        if value in (None, ''):
            return None
        try:
            return round(float(value) / digits, 2)
        except (TypeError, ValueError):
            return None

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0',
                'Referer': 'https://quote.eastmoney.com/',
            })
            with urllib.request.urlopen(req, timeout=10) as response:
                payload = json.loads(response.read().decode('utf-8'))
                data = payload.get('data') or {}
                price = scaled(data.get('f43'))
                if not price:
                    return {}
                change_amount = scaled(data.get('f169'))
                change_pct = scaled(data.get('f170'))
                return {
                    'name': data.get('f58') or stock['code'],
                    'code': stock['code'],
                    'market': stock['market'],
                    'exchange': stock.get('exchange'),
                    'tencent_symbol': stock['tencent_symbol'],
                    'price': price,
                    'prev_close': scaled(data.get('f60')),
                    'open': scaled(data.get('f46')),
                    'volume': None,
                    'high': scaled(data.get('f44')),
                    'low': scaled(data.get('f45')),
                    'change_amount': change_amount,
                    'change_pct': change_pct,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'currency': 'CNY',
                    'pe': scaled(data.get('f164')),
                    'pb': scaled(data.get('f167')),
                    'market_cap': data.get('f116'),
                    '52w_high': None,
                    '52w_low': None,
                    'raw_code': data.get('f57') or raw_code,
                    'quote_source': 'eastmoney',
                }
        except (urllib.error.URLError, json.JSONDecodeError) as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BASE_DELAY * (attempt + 1))
            else:
                raise Exception(f"获取东方财富行情失败: {e}")
    return {}


def fetch_quote_with_fallback(code: str) -> dict:
    """先取主源；A 股主源失败时自动尝试东方财富。"""
    stock = normalize_stock_code(code)
    errors = []

    try:
        quote = fetch_tencent_quote(code)
        if quote and quote.get('price'):
            quote.setdefault('quote_source', 'tencent')
            return quote
    except Exception as e:
        errors.append(f"tencent={e}")

    if stock['market'] in ('SH', 'SZ'):
        try:
            quote = fetch_eastmoney_quote(code)
            if quote and quote.get('price'):
                return quote
        except Exception as e:
            errors.append(f"eastmoney={e}")

    if errors:
        raise Exception('; '.join(errors))
    return {}


def _parse_tencent_quote(data: str, symbol: str, stock: dict) -> dict:
    """解析腾讯财经实时行情响应"""
    var_name = f"v_{symbol}"
    for line in data.strip().split(";"):
        line = line.strip()
        if not line or var_name not in line:
            continue
        # 提取引号内的内容
        parts = line.split('"')
        if len(parts) < 2:
            continue
        values = parts[1].split("~")
        if len(values) < 35:  # 至少需要35个字段
            continue
        
        def safe_float(idx: int, default: float = 0.0) -> float:
            try:
                return float(values[idx]) if values[idx] else default
            except (ValueError, IndexError):
                return default
        
        def safe_str(idx: int, default: str = "") -> str:
            return values[idx] if idx < len(values) else default
        
        # 字段映射 (根据腾讯财经API实际数据)
        # 0:市场 1:名称 2:代码 3:现价 4:昨收 5:今开 6:成交量
        # 30:时间戳 31:涨跌额 32:涨跌幅 33:最高 34:最低
        # 39:市盈率 47:市净率 37:总市值 48:52周高 49:52周低
        market = stock['market']
        currency = 'HKD' if market == 'HK' else ('CNY' if market in ('SH', 'SZ') else safe_str(35, 'USD') or 'USD')
        pb_idx = 47 if market in ('HK', 'US') else 46
        market_cap_idx = 37 if market == 'HK' else (57 if market in ('SH', 'SZ') else 44)
        high_52_idx = 48 if market in ('HK', 'US') else 41
        low_52_idx = 49 if market in ('HK', 'US') else 42
        return {
            'name': values[1],
            'code': stock['code'],
            'market': market,
            'exchange': stock.get('exchange'),
            'tencent_symbol': symbol,
            'price': safe_float(3),
            'prev_close': safe_float(4),
            'open': safe_float(5),
            'volume': safe_float(6),
            'high': safe_float(33),
            'low': safe_float(34),
            'change_amount': safe_float(31),
            'change_pct': safe_float(32),
            'timestamp': safe_str(30),
            'currency': currency,
            'pe': safe_float(39) if len(values) > 39 else None,
            'pb': safe_float(pb_idx) if len(values) > pb_idx else None,
            'market_cap': safe_str(market_cap_idx),
            '52w_high': safe_float(high_52_idx) if len(values) > high_52_idx else None,
            '52w_low': safe_float(low_52_idx) if len(values) > low_52_idx else None,
            'raw_code': safe_str(2),
        }
    return {}


def fetch_tencent_kline(code: str, days: int = 120) -> pd.DataFrame:
    """获取腾讯财经K线数据"""
    stock = normalize_stock_code(code)
    symbol = stock['tencent_symbol']
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={symbol},day,,,{days},qfq"

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://gu.qq.com/',
            })
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))
                return _parse_tencent_kline(data, symbol)
        except (urllib.error.URLError, json.JSONDecodeError) as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BASE_DELAY * (attempt + 1))
            else:
                raise Exception(f"获取K线数据失败: {e}")
    return pd.DataFrame()


def _parse_tencent_kline(data: dict, symbol: str) -> pd.DataFrame:
    """解析腾讯财经K线数据"""
    if data.get('code') != 0 or not data.get('data') or symbol not in data['data']:
        return pd.DataFrame()

    symbol_data = data['data'][symbol]
    day_data = symbol_data.get('day') or symbol_data.get('qfqday') or symbol_data.get('hfqday') or []
    if not day_data:
        return pd.DataFrame()

    records = []
    for item in day_data:
        if len(item) >= 6:
            records.append({
                'Date': item[0],
                'Open': float(item[1]),
                'Close': float(item[2]),
                'Low': float(item[3]),
                'High': float(item[4]),
                'Volume': float(item[5]),
            })

    df = pd.DataFrame(records)
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
    return df


def fetch_eastmoney_kline(code: str, days: int = 120) -> pd.DataFrame:
    """获取东方财富日线（当前仅作为 A 股 fallback）。"""
    stock = normalize_stock_code(code)
    if stock['market'] not in ('SH', 'SZ') or len(stock['code']) != 8:
        return pd.DataFrame()

    raw_code = stock['code'][2:]
    secid_prefix = '1' if stock['market'] == 'SH' else '0'
    end = datetime.now().strftime('%Y%m%d')
    # 多抓一些，避免交易日折算不足
    start = (datetime.now() - timedelta(days=max(days * 2, 180))).strftime('%Y%m%d')
    url = (
        "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        f"?secid={secid_prefix}.{raw_code}"
        "&fields1=f1,f2,f3,f4,f5,f6"
        "&fields2=f51,f52,f53,f54,f55,f56,f57,f58"
        "&klt=101&fqt=1"
        f"&beg={start}&end={end}"
    )

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0',
                'Referer': 'https://quote.eastmoney.com/',
            })
            with urllib.request.urlopen(req, timeout=20) as response:
                payload = json.loads(response.read().decode('utf-8'))
                klines = ((payload.get('data') or {}).get('klines')) or []
                if not klines:
                    return pd.DataFrame()
                records = []
                for item in klines:
                    parts = item.split(',')
                    if len(parts) < 6:
                        continue
                    records.append({
                        'Date': parts[0],
                        'Open': float(parts[1]),
                        'Close': float(parts[2]),
                        'High': float(parts[3]),
                        'Low': float(parts[4]),
                        'Volume': float(parts[5]),
                    })
                df = pd.DataFrame(records)
                if not df.empty:
                    df['Date'] = pd.to_datetime(df['Date'])
                    df.set_index('Date', inplace=True)
                return df
        except (urllib.error.URLError, json.JSONDecodeError, ValueError) as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BASE_DELAY * (attempt + 1))
            else:
                raise Exception(f"获取东方财富K线失败: {e}")
    return pd.DataFrame()


def fetch_us_kline_yahoo(symbol: str, period: str = '6mo') -> pd.DataFrame:
    range_map = {
        '1mo': '1mo',
        '3mo': '3mo',
        '6mo': '6mo',
        '1y': '1y',
        '2y': '2y',
        '5y': '5y',
    }
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={range_map.get(period, '6mo')}&interval=1d&includePrePost=false"

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=20) as response:
                data = json.loads(response.read().decode('utf-8'))

            result = data.get('chart', {}).get('result', [])
            if not result:
                return pd.DataFrame()
            result = result[0]
            timestamps = result.get('timestamp') or []
            quote = (result.get('indicators', {}).get('quote') or [{}])[0]
            opens = quote.get('open') or []
            highs = quote.get('high') or []
            lows = quote.get('low') or []
            closes = quote.get('close') or []
            volumes = quote.get('volume') or []

            records = []
            for i, ts in enumerate(timestamps):
                if i >= len(opens) or opens[i] is None or closes[i] is None or highs[i] is None or lows[i] is None:
                    continue
                records.append({
                    'Date': datetime.fromtimestamp(ts).strftime('%Y-%m-%d'),
                    'Open': float(opens[i]),
                    'Close': float(closes[i]),
                    'Low': float(lows[i]),
                    'High': float(highs[i]),
                    'Volume': float(volumes[i] or 0),
                })

            df = pd.DataFrame(records)
            if not df.empty:
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)
            return df
        except (urllib.error.URLError, json.JSONDecodeError, ValueError) as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BASE_DELAY * (attempt + 1))
            else:
                raise Exception(f"获取 Yahoo K线失败: {e}")

    return pd.DataFrame()


POSITIVE_NEWS_KEYWORDS = [
    'beat', 'surge', 'upgrade', 'record', 'growth', 'profit', 'win', 'breakthrough', 'bullish',
    '超预期', '增长', '中标', '利好', '创新高', '回购', '增持', '扭亏', '突破', '上调'
]
NEGATIVE_NEWS_KEYWORDS = [
    'miss', 'lawsuit', 'probe', 'fraud', 'downgrade', 'slump', 'warning', 'decline', 'loss', 'risk',
    '诉讼', '调查', '减持', '亏损', '预警', '下滑', '利空', '处罚', '暴跌', '风险'
]


def build_news_query(code: str, quote: dict) -> tuple[str, str]:
    stock = normalize_stock_code(code)
    name = (quote.get('name') or stock['code']).strip()
    if stock['market'] in ('SH', 'SZ'):
        return f'{name} {stock["code"][2:]}', 'zh'
    if stock['market'] == 'HK':
        return f'{name} {stock["code"].replace(".HK", "")}', 'zh'
    return f'{name} {stock["code"]}', 'en'


def score_news_title(title: str) -> int:
    lower = title.lower()
    score = 0
    for kw in POSITIVE_NEWS_KEYWORDS:
        if kw.lower() in lower:
            score += 1
    for kw in NEGATIVE_NEWS_KEYWORDS:
        if kw.lower() in lower:
            score -= 1
    return score


def summarize_news_sentiment(items: list[dict]) -> dict:
    if not items:
        return {
            'label': '暂无',
            'heat': '低',
            'score': 0,
            'positive': 0,
            'negative': 0,
            'neutral': 0,
        }

    pos = neg = neu = 0
    total_score = 0
    for item in items:
        score = score_news_title(item.get('title', ''))
        total_score += score
        if score > 0:
            pos += 1
        elif score < 0:
            neg += 1
        else:
            neu += 1

    if total_score >= 2:
        label = '偏正面'
    elif total_score <= -2:
        label = '偏负面'
    else:
        label = '中性'

    count = len(items)
    if count >= 10:
        heat = '高'
    elif count >= 5:
        heat = '中'
    else:
        heat = '低'

    return {
        'label': label,
        'heat': heat,
        'score': total_score,
        'positive': pos,
        'negative': neg,
        'neutral': neu,
    }


def fetch_google_news_rss(code: str, quote: dict, limit: int = 5) -> dict:
    query, lang = build_news_query(code, quote)
    if lang == 'zh':
        params = f'q={urllib.parse.quote(query)}&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'
    else:
        params = f'q={urllib.parse.quote(query)}&hl=en-US&gl=US&ceid=US:en'
    url = f'https://news.google.com/rss/search?{params}'

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=20) as response:
                xml_text = response.read().decode('utf-8', 'ignore')
            root = ET.fromstring(xml_text)
            channel = root.find('channel')
            rss_items = channel.findall('item') if channel is not None else []
            items = []
            for node in rss_items[:limit]:
                title = html.unescape((node.findtext('title') or '').strip())
                link = (node.findtext('link') or '').strip()
                pub_date = (node.findtext('pubDate') or '').strip()
                source = html.unescape((node.findtext('source') or '').strip())
                if not title:
                    continue
                items.append({
                    'title': title,
                    'link': link,
                    'published_at': pub_date,
                    'source': source or 'Google News',
                })
            sentiment = summarize_news_sentiment(items)
            return {
                'query': query,
                'source': 'google-news-rss',
                'items': items,
                'sentiment': sentiment,
            }
        except Exception:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BASE_DELAY * (attempt + 1))
            else:
                return {
                    'query': query,
                    'source': 'google-news-rss',
                    'items': [],
                    'sentiment': summarize_news_sentiment([]),
                }

    return {
        'query': query,
        'source': 'google-news-rss',
        'items': [],
        'sentiment': summarize_news_sentiment([]),
    }


SEC_TICKER_MAP_CACHE = None
EVENT_KEYWORDS = {
    '业绩': ['财报', '业绩', '盈利', '营收', '季报', '年报', 'earnings', 'revenue', 'profit'],
    '订单/中标': ['中标', '订单', '签约', '合作', 'contract', 'deal'],
    '资本动作': ['回购', '增持', '减持', '融资', '定增', 'buyback', 'offering'],
    '监管/风险': ['调查', '诉讼', '处罚', '风险', '警告', 'probe', 'lawsuit', 'fraud', 'warning'],
    '产品/技术': ['新品', '发布', '突破', '芯片', 'ai', 'launch', 'breakthrough'],
}


def classify_event_title(title: str) -> str:
    lower = title.lower()
    for label, keywords in EVENT_KEYWORDS.items():
        if any(kw.lower() in lower for kw in keywords):
            return label
    return '市场动态'


def derive_events_from_news(news: dict, limit: int = 3) -> dict:
    items = []
    for item in (news.get('items') or [])[:limit]:
        items.append({
            'title': item.get('title', ''),
            'category': classify_event_title(item.get('title', '')),
            'source': item.get('source', 'Google News'),
            'published_at': item.get('published_at', ''),
            'link': item.get('link', ''),
        })
    return {
        'source': 'news-derived',
        'items': items,
    }


def fetch_sec_ticker_map() -> dict:
    global SEC_TICKER_MAP_CACHE
    if SEC_TICKER_MAP_CACHE is not None:
        return SEC_TICKER_MAP_CACHE
    req = urllib.request.Request(
        'https://www.sec.gov/files/company_tickers.json',
        headers={'User-Agent': 'Mozilla/5.0 stockbuddy@example.com'}
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        payload = json.loads(response.read().decode('utf-8'))
    mapping = {}
    for _, item in payload.items():
        ticker = (item.get('ticker') or '').upper()
        cik = str(item.get('cik_str') or '').strip()
        if ticker and cik:
            mapping[ticker] = cik.zfill(10)
    SEC_TICKER_MAP_CACHE = mapping
    return mapping


def fetch_sec_events(code: str, quote: dict, limit: int = 3) -> dict:
    stock = normalize_stock_code(code)
    if stock['market'] != 'US':
        return {'source': 'sec', 'items': []}

    ticker = stock['code'].upper()
    try:
        mapping = fetch_sec_ticker_map()
        cik = mapping.get(ticker)
        if not cik:
            return {'source': 'sec', 'items': []}
        req = urllib.request.Request(
            f'https://data.sec.gov/submissions/CIK{cik}.json',
            headers={'User-Agent': 'Mozilla/5.0 stockbuddy@example.com'}
        )
        with urllib.request.urlopen(req, timeout=20) as response:
            payload = json.loads(response.read().decode('utf-8'))
        recent = ((payload.get('filings') or {}).get('recent')) or {}
        forms = recent.get('form') or []
        dates = recent.get('filingDate') or []
        accessions = recent.get('accessionNumber') or []
        primary_docs = recent.get('primaryDocument') or []
        items = []
        for i in range(min(len(forms), len(dates), len(accessions), len(primary_docs), limit)):
            form = forms[i]
            filing_date = dates[i]
            acc = accessions[i].replace('-', '')
            doc = primary_docs[i]
            link = f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc}/{doc}' if doc else ''
            items.append({
                'title': f'SEC {form} filed on {filing_date}',
                'category': 'SEC申报',
                'source': 'SEC',
                'published_at': filing_date,
                'link': link,
            })
        return {'source': 'sec', 'items': items}
    except Exception:
        return {'source': 'sec', 'items': []}


def build_buzz_radar(news: dict, events: dict) -> dict:
    sentiment = news.get('sentiment') or {}
    news_heat = sentiment.get('heat', '低')
    total_events = len(events.get('items') or [])
    score = 0
    if news_heat == '高':
        score += 2
    elif news_heat == '中':
        score += 1
    if sentiment.get('label') in ('偏正面', '偏负面'):
        score += 1
    if total_events >= 3:
        score += 1

    if score >= 4:
        level = '过热'
    elif score >= 2:
        level = '升温'
    else:
        level = '正常'

    return {
        'level': level,
        'news_heat': news_heat,
        'event_count': total_events,
        'sentiment': sentiment.get('label', '暂无'),
        'source': 'news-derived-buzz',
    }


def build_event_layer(code: str, quote: dict, news: dict) -> dict:
    stock = normalize_stock_code(code)
    if stock['market'] == 'US':
        sec_events = fetch_sec_events(code, quote)
        if sec_events.get('items'):
            return sec_events
    return derive_events_from_news(news)


def get_or_refresh_aux_layers(code: str, quote: dict, refresh: bool = False) -> dict:
    news = None if refresh else get_cached_aux(code, 'news')
    if not news:
        news = fetch_google_news_rss(code, quote)
        set_cached_aux(code, 'news', news, ttl_seconds=AUX_CACHE_TTL_SECONDS)

    events = None if refresh else get_cached_aux(code, 'events')
    if not events:
        events = build_event_layer(code, quote, news)
        set_cached_aux(code, 'events', events, ttl_seconds=AUX_CACHE_TTL_SECONDS)

    buzz = None if refresh else get_cached_aux(code, 'buzz')
    if not buzz:
        buzz = build_buzz_radar(news, events)
        set_cached_aux(code, 'buzz', buzz, ttl_seconds=AUX_CACHE_TTL_SECONDS)

    return {
        'news': news,
        'events': events,
        'buzz': buzz,
    }


def period_to_days(period: str) -> int:
    """将周期字符串转换为天数"""
    mapping = {
        "1mo": 30,
        "3mo": 90,
        "6mo": 180,
        "1y": 250,
        "2y": 500,
        "5y": 1250,
    }
    return mapping.get(period, 180)


def min_kline_points(required_days: int) -> int:
    return 20 if required_days <= 30 else 30


def refresh_kline_cache(code: str, required_days: int, period: str = '6mo') -> tuple[pd.DataFrame, str]:
    """使用 SQLite 保存日线数据，并按需增量刷新。返回 (hist, source)。"""
    stock = normalize_stock_code(code)
    buffer_days = 30
    latest_date = get_latest_kline_date(code)
    fetch_days = max(required_days + buffer_days, 60)
    source_used = 'tencent'

    if latest_date:
        latest_dt = datetime.strptime(latest_date, "%Y-%m-%d")
        missing_days = max((datetime.now() - latest_dt).days, 0)
        if missing_days <= 2:
            fetch_days = min(fetch_days, 60)
        else:
            fetch_days = max(missing_days + buffer_days, 60)

    fetched = fetch_tencent_kline(code, fetch_days)
    if stock['market'] in ('SH', 'SZ') and len(fetched) <= 2:
        fetched = fetch_eastmoney_kline(code, fetch_days)
        source_used = 'eastmoney' if not fetched.empty else source_used
    elif stock['market'] == 'US' and len(fetched) <= 2:
        fetched = fetch_us_kline_yahoo(stock['code'], period)
        source_used = 'yahoo' if not fetched.empty else source_used

    if not fetched.empty:
        upsert_kline_df(code, fetched, source=source_used)

    hist = get_kline_df(code, required_days + buffer_days)
    if len(hist) < min_kline_points(required_days):
        fallback = fetch_tencent_kline(code, required_days + buffer_days)
        fallback_source = 'tencent'
        if stock['market'] in ('SH', 'SZ') and len(fallback) <= 2:
            fallback = fetch_eastmoney_kline(code, required_days + buffer_days)
            fallback_source = 'eastmoney' if not fallback.empty else fallback_source
        elif stock['market'] == 'US' and len(fallback) <= 2:
            fallback = fetch_us_kline_yahoo(stock['code'], period)
            fallback_source = 'yahoo' if not fallback.empty else fallback_source
        if not fallback.empty:
            upsert_kline_df(code, fallback, source=fallback_source)
            hist = get_kline_df(code, required_days + buffer_days)
            source_used = fallback_source
    return hist, source_used


# ─────────────────────────────────────────────
#  技术指标计算 (保持不变)
# ─────────────────────────────────────────────

def calc_ma(close: pd.Series, windows: list[int] = None) -> dict:
    """计算多周期移动平均线"""
    if windows is None:
        windows = [5, 10, 20, 60, 120, 250]
    result = {}
    for w in windows:
        if len(close) >= w:
            ma = close.rolling(window=w).mean()
            result[f"MA{w}"] = round(ma.iloc[-1], 3)
    return result


def calc_ema(close: pd.Series, span: int) -> pd.Series:
    """计算指数移动平均线"""
    return close.ewm(span=span, adjust=False).mean()


def calc_macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> dict:
    """计算MACD指标"""
    ema_fast = calc_ema(close, fast)
    ema_slow = calc_ema(close, slow)
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal, adjust=False).mean()
    macd_hist = 2 * (dif - dea)

    return {
        "DIF": round(dif.iloc[-1], 4),
        "DEA": round(dea.iloc[-1], 4),
        "MACD": round(macd_hist.iloc[-1], 4),
        "signal": _macd_signal(dif, dea, macd_hist),
    }


def _macd_signal(dif: pd.Series, dea: pd.Series, macd_hist: pd.Series) -> str:
    """MACD信号判断"""
    if len(dif) < 3:
        return "中性"
    if dif.iloc[-1] > dea.iloc[-1] and dif.iloc[-2] <= dea.iloc[-2]:
        return "金叉-买入信号"
    if dif.iloc[-1] < dea.iloc[-1] and dif.iloc[-2] >= dea.iloc[-2]:
        return "死叉-卖出信号"
    if dif.iloc[-1] > 0 and dea.iloc[-1] > 0:
        if macd_hist.iloc[-1] > macd_hist.iloc[-2]:
            return "多头增强"
        return "多头区域"
    if dif.iloc[-1] < 0 and dea.iloc[-1] < 0:
        if macd_hist.iloc[-1] < macd_hist.iloc[-2]:
            return "空头增强"
        return "空头区域"
    return "中性"


def calc_rsi(close: pd.Series, periods: list[int] = None) -> dict:
    """计算RSI指标"""
    if periods is None:
        periods = [6, 12, 24]
    result = {}
    delta = close.diff()
    for p in periods:
        if len(close) < p + 1:
            continue
        gain = delta.clip(lower=0).rolling(window=p).mean()
        loss = (-delta.clip(upper=0)).rolling(window=p).mean()
        rs = gain / loss.replace(0, np.nan)
        rsi = 100 - (100 / (1 + rs))
        val = round(rsi.iloc[-1], 2)
        result[f"RSI{p}"] = val
    rsi_main = result.get("RSI12", result.get("RSI6", 50))
    if rsi_main > 80:
        result["signal"] = "严重超买-卖出信号"
    elif rsi_main > 70:
        result["signal"] = "超买-注意风险"
    elif rsi_main < 20:
        result["signal"] = "严重超卖-买入信号"
    elif rsi_main < 30:
        result["signal"] = "超卖-关注买入"
    else:
        result["signal"] = "中性"
    return result


def calc_kdj(high: pd.Series, low: pd.Series, close: pd.Series, n: int = 9) -> dict:
    """计算KDJ指标"""
    if len(close) < n:
        return {"K": 50, "D": 50, "J": 50, "signal": "数据不足"}
    lowest_low = low.rolling(window=n).min()
    highest_high = high.rolling(window=n).max()
    rsv = (close - lowest_low) / (highest_high - lowest_low).replace(0, np.nan) * 100

    k = pd.Series(index=close.index, dtype=float)
    d = pd.Series(index=close.index, dtype=float)
    k.iloc[n - 1] = 50
    d.iloc[n - 1] = 50
    for i in range(n, len(close)):
        k.iloc[i] = 2 / 3 * k.iloc[i - 1] + 1 / 3 * rsv.iloc[i]
        d.iloc[i] = 2 / 3 * d.iloc[i - 1] + 1 / 3 * k.iloc[i]
    j = 3 * k - 2 * d

    k_val = round(k.iloc[-1], 2)
    d_val = round(d.iloc[-1], 2)
    j_val = round(j.iloc[-1], 2)

    signal = "中性"
    if k_val > d_val and k.iloc[-2] <= d.iloc[-2]:
        signal = "金叉-买入信号"
    elif k_val < d_val and k.iloc[-2] >= d.iloc[-2]:
        signal = "死叉-卖出信号"
    elif j_val > 100:
        signal = "超买区域"
    elif j_val < 0:
        signal = "超卖区域"

    return {"K": k_val, "D": d_val, "J": j_val, "signal": signal}


def calc_bollinger(close: pd.Series, window: int = 20, num_std: float = 2) -> dict:
    """计算布林带"""
    if len(close) < window:
        return {"signal": "数据不足"}
    ma = close.rolling(window=window).mean()
    std = close.rolling(window=window).std()
    upper = ma + num_std * std
    lower = ma - num_std * std

    current = close.iloc[-1]
    upper_val = round(upper.iloc[-1], 3)
    lower_val = round(lower.iloc[-1], 3)
    mid_val = round(ma.iloc[-1], 3)
    bandwidth = round((upper_val - lower_val) / mid_val * 100, 2)

    signal = "中性"
    if current > upper_val:
        signal = "突破上轨-超买"
    elif current < lower_val:
        signal = "突破下轨-超卖"
    elif current > mid_val:
        signal = "中轨上方-偏强"
    else:
        signal = "中轨下方-偏弱"

    return {
        "upper": upper_val,
        "middle": mid_val,
        "lower": lower_val,
        "bandwidth_pct": bandwidth,
        "signal": signal,
    }


def calc_volume_analysis(volume: pd.Series, close: pd.Series) -> dict:
    """成交量分析"""
    if len(volume) < 20:
        return {"signal": "数据不足"}
    avg_5 = volume.rolling(5).mean().iloc[-1]
    avg_20 = volume.rolling(20).mean().iloc[-1]
    current = volume.iloc[-1]
    vol_ratio = round(current / avg_5, 2) if avg_5 > 0 else 0
    price_change = close.iloc[-1] - close.iloc[-2]

    signal = "中性"
    if vol_ratio > 2 and price_change > 0:
        signal = "放量上涨-强势"
    elif vol_ratio > 2 and price_change < 0:
        signal = "放量下跌-弱势"
    elif vol_ratio < 0.5 and price_change > 0:
        signal = "缩量上涨-动力不足"
    elif vol_ratio < 0.5 and price_change < 0:
        signal = "缩量下跌-抛压减轻"

    return {
        "current_volume": int(current),
        "avg_5d_volume": int(avg_5),
        "avg_20d_volume": int(avg_20),
        "volume_ratio": vol_ratio,
        "signal": signal,
    }


def calc_ma_trend(close: pd.Series) -> dict:
    """均线趋势分析"""
    mas = calc_ma(close, [5, 10, 20, 60])
    current = close.iloc[-1]

    above_count = sum(1 for v in mas.values() if current > v)
    total = len(mas)

    if above_count == total and total > 0:
        signal = "多头排列-强势"
    elif above_count == 0:
        signal = "空头排列-弱势"
    elif above_count >= total * 0.7:
        signal = "偏多"
    elif above_count <= total * 0.3:
        signal = "偏空"
    else:
        signal = "震荡"

    return {**mas, "trend_signal": signal, "price_above_ma_count": f"{above_count}/{total}"}


# ─────────────────────────────────────────────
#  基本面分析 (基于腾讯数据)
# ─────────────────────────────────────────────

def get_fundamentals(quote: dict) -> dict:
    """基于实时行情数据的基本面分析"""
    result = {}

    pe = quote.get('pe')
    pb = quote.get('pb')
    result['PE'] = round(pe, 2) if pe else None
    result['PB'] = round(pb, 2) if pb else None
    result['PS'] = None
    result['market_cap'] = quote.get('market_cap', '')
    result['52w_high'] = quote.get('52w_high')
    result['52w_low'] = quote.get('52w_low')
    result['company_name'] = quote.get('name', '未知')
    result['sector'] = quote.get('market', '未知市场')
    result['industry'] = quote.get('exchange') or quote.get('market', '未知')
    result['currency'] = quote.get('currency', 'N/A')
    result['market'] = quote.get('market', 'N/A')
    result['fundamental_signal'] = _fundamental_signal(result)
    return result


def _fundamental_signal(data: dict) -> str:
    """基本面信号判断 (简化版)"""
    score = 0
    reasons = []

    pe = data.get("PE")
    if pe is not None and pe > 0:
        if pe < 15:
            score += 2
            reasons.append(f"PE低估值({pe})")
        elif pe < 25:
            score += 1
            reasons.append(f"PE合理({pe})")
        elif pe > 40:
            score -= 1
            reasons.append(f"PE偏高({pe})")

    pb = data.get("PB")
    if pb is not None:
        if pb < 1:
            score += 1
            reasons.append(f"PB破净({pb})")
        elif pb > 5:
            score -= 1
            reasons.append(f"PB偏高({pb})")

    if score >= 3:
        signal = "基本面优秀"
    elif score >= 1:
        signal = "基本面良好"
    elif score >= 0:
        signal = "基本面一般"
    else:
        signal = "基本面较差"

    return f"{signal} ({'; '.join(reasons[:3])})" if reasons else signal


# ─────────────────────────────────────────────
#  综合评分与建议
# ─────────────────────────────────────────────

MARKET_PROFILES = {
    "HK": {"technical": 0.62, "fundamental": 0.38, "risk_penalty": 1.0},
    "SH": {"technical": 0.58, "fundamental": 0.42, "risk_penalty": 0.9},
    "SZ": {"technical": 0.60, "fundamental": 0.40, "risk_penalty": 1.0},
    "US": {"technical": 0.55, "fundamental": 0.45, "risk_penalty": 0.85},
}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def detect_market_regime(hist: pd.DataFrame, technical: dict, quote: dict) -> dict:
    close = hist["Close"]
    ma20 = close.rolling(20).mean().iloc[-1] if len(close) >= 20 else close.iloc[-1]
    ma60 = close.rolling(60).mean().iloc[-1] if len(close) >= 60 else ma20
    current = close.iloc[-1]
    rsi12 = technical.get("rsi", {}).get("RSI12", technical.get("rsi", {}).get("RSI6", 50))
    high_52w = quote.get("52w_high")
    low_52w = quote.get("52w_low")
    pos_52w = None
    if high_52w and low_52w and high_52w != low_52w:
        pos_52w = (current - low_52w) / (high_52w - low_52w)

    if current > ma20 > ma60 and rsi12 >= 55:
        regime = "趋势延续"
    elif rsi12 <= 35 and technical.get("kdj", {}).get("J", 50) < 20:
        regime = "超跌反弹"
    elif pos_52w is not None and pos_52w > 0.85 and rsi12 >= 68:
        regime = "高位风险"
    elif abs(current / ma20 - 1) < 0.03 and 40 <= rsi12 <= 60:
        regime = "区间震荡"
    else:
        regime = "估值修复/等待确认"

    return {"regime": regime, "position_52w": round(pos_52w, 4) if pos_52w is not None else None}


def compute_layer_scores(hist: pd.DataFrame, technical: dict, fundamental: dict, quote: dict) -> dict:
    close = hist["Close"]
    current = close.iloc[-1]
    ret_5 = (current / close.iloc[-6] - 1) if len(close) > 5 else 0
    ret_20 = (current / close.iloc[-21] - 1) if len(close) > 20 else ret_5
    ma = technical.get("ma_trend", {})
    above = ma.get("price_above_ma_count", "0/1").split("/")
    above_ratio = (int(above[0]) / max(int(above[1]), 1)) if len(above) == 2 else 0
    macd_sig = technical.get("macd", {}).get("signal", "")
    rsi = technical.get("rsi", {}).get("RSI12", technical.get("rsi", {}).get("RSI6", 50))
    kdj_j = technical.get("kdj", {}).get("J", 50)
    volume_ratio = technical.get("volume", {}).get("volume_ratio", 1)
    boll_sig = technical.get("bollinger", {}).get("signal", "")
    pe = fundamental.get("PE")
    pb = fundamental.get("PB")
    high_52w = fundamental.get("52w_high")
    low_52w = fundamental.get("52w_low")
    pos_52w = 0.5
    if high_52w and low_52w and high_52w != low_52w:
        pos_52w = clamp((quote.get("price", current) - low_52w) / (high_52w - low_52w), 0, 1)

    trend = (ret_20 * 100 * 0.6) + (above_ratio - 0.5) * 8
    if "多头" in macd_sig or "金叉" in macd_sig:
        trend += 1.5
    elif "空头" in macd_sig or "死叉" in macd_sig:
        trend -= 1.5

    momentum = ret_5 * 100 * 0.8
    momentum += 1.2 if volume_ratio > 1.5 and ret_5 > 0 else 0
    momentum -= 1.2 if volume_ratio > 1.5 and ret_5 < 0 else 0
    momentum += 0.8 if "金叉" in technical.get("kdj", {}).get("signal", "") else 0
    momentum -= 0.8 if "死叉" in technical.get("kdj", {}).get("signal", "") else 0

    risk = 0.0
    if rsi > 75:
        risk -= 2.2
    elif rsi < 28:
        risk += 1.0
    if kdj_j > 100:
        risk -= 1.2
    elif kdj_j < 0:
        risk += 0.8
    if pos_52w > 0.88:
        risk -= 1.2
    elif pos_52w < 0.18:
        risk += 0.8
    if "突破上轨" in boll_sig:
        risk -= 0.8
    elif "突破下轨" in boll_sig:
        risk += 0.6

    valuation = 0.0
    if pe is not None:
        if 0 < pe < 15:
            valuation += 2.0
        elif pe < 25:
            valuation += 1.0
        elif pe > 40:
            valuation -= 1.5
    if pb is not None:
        if 0 < pb < 1:
            valuation += 1.0
        elif pb > 6:
            valuation -= 1.0

    relative_strength = clamp(ret_20 * 100 / 4, -3, 3)
    volume_structure = clamp((volume_ratio - 1.0) * 2, -2.5, 2.5)

    return {
        "trend": round(clamp(trend, -5, 5), 2),
        "momentum": round(clamp(momentum, -5, 5), 2),
        "risk": round(clamp(risk, -5, 5), 2),
        "valuation": round(clamp(valuation, -5, 5), 2),
        "relative_strength": round(relative_strength, 2),
        "volume_structure": round(volume_structure, 2),
    }


def evaluate_signal_quality(layer_scores: dict) -> dict:
    positives = sum(1 for v in layer_scores.values() if v > 0.8)
    negatives = sum(1 for v in layer_scores.values() if v < -0.8)
    dispersion = max(layer_scores.values()) - min(layer_scores.values())
    agreement = abs(positives - negatives)
    confidence = 40 + agreement * 8 - min(dispersion * 2.5, 18)
    confidence = int(clamp(confidence, 18, 92))
    if confidence >= 72:
        level = "高"
    elif confidence >= 55:
        level = "中"
    else:
        level = "低"
    return {"score": confidence, "level": level, "positives": positives, "negatives": negatives}


def backtest_current_signal(hist: pd.DataFrame, period: str) -> dict:
    horizons = [5, 10, 20]
    closes = hist["Close"].reset_index(drop=True)
    if len(closes) < 45:
        return {"samples": 0, "message": "历史样本不足"}
    current_ret20 = (closes.iloc[-1] / closes.iloc[-21] - 1) if len(closes) > 20 else 0
    current_ret5 = (closes.iloc[-1] / closes.iloc[-6] - 1) if len(closes) > 5 else 0
    matched = []
    for i in range(25, len(closes) - 20):
        r20 = closes.iloc[i] / closes.iloc[i-20] - 1
        r5 = closes.iloc[i] / closes.iloc[i-5] - 1
        if abs(r20 - current_ret20) < 0.06 and abs(r5 - current_ret5) < 0.04:
            matched.append(i)
    if len(matched) < 5:
        return {"samples": len(matched), "message": "相似信号样本不足"}

    perf = {"samples": len(matched)}
    all_forward = []
    for h in horizons:
        vals = []
        for i in matched:
            if i + h < len(closes):
                vals.append(closes.iloc[i + h] / closes.iloc[i] - 1)
        if vals:
            perf[f"forward_{h}d_avg_pct"] = round(sum(vals) / len(vals) * 100, 2)
            perf[f"forward_{h}d_win_rate"] = round(sum(1 for x in vals if x > 0) / len(vals) * 100, 2)
            all_forward.extend(vals)
    if all_forward:
        perf["max_drawdown_proxy_pct"] = round(min(all_forward) * 100, 2)
    perf["period"] = period
    return perf


def decide_action_type(regime: str, total_score: float, confidence: dict) -> tuple[str, str]:
    if total_score >= 4.5 and confidence["score"] >= 70:
        return "强烈买入", "趋势型买入" if regime == "趋势延续" else "高置信度买入"
    if total_score >= 2:
        if regime == "超跌反弹":
            return "买入", "超跌博弈型买入"
        return "买入", "趋势跟随型买入"
    if total_score <= -4.5 and confidence["score"] >= 70:
        return "强烈卖出", "风险规避型卖出"
    if total_score <= -2:
        return "卖出", "止盈/止损型卖出"
    return "持有/观望", "等待确认"


def generate_recommendation(technical: dict, fundamental: dict, current_price: float, hist: pd.DataFrame, quote: dict) -> dict:
    market = quote.get("market", "HK")
    profile = MARKET_PROFILES.get(market, MARKET_PROFILES["HK"])
    regime = detect_market_regime(hist, technical, quote)
    layer_scores = compute_layer_scores(hist, technical, fundamental, quote)
    confidence = evaluate_signal_quality(layer_scores)

    technical_bucket = (
        layer_scores["trend"] * 0.35 +
        layer_scores["momentum"] * 0.25 +
        layer_scores["relative_strength"] * 0.20 +
        layer_scores["volume_structure"] * 0.20
    )
    fundamental_bucket = layer_scores["valuation"]
    risk_bucket = layer_scores["risk"] * profile["risk_penalty"]
    total_score = technical_bucket * profile["technical"] + fundamental_bucket * profile["fundamental"] + risk_bucket
    total_score = round(clamp(total_score, -8, 8), 2)

    action, action_type = decide_action_type(regime["regime"], total_score, confidence)
    icon_map = {"强烈买入": "🟢🟢", "买入": "🟢", "持有/观望": "🟡", "卖出": "🔴", "强烈卖出": "🔴🔴"}
    en_map = {"强烈买入": "STRONG_BUY", "买入": "BUY", "持有/观望": "HOLD", "卖出": "SELL", "强烈卖出": "STRONG_SELL"}
    icon = icon_map[action]

    key_signals = [
        f"市场场景: {regime['regime']}",
        f"趋势层: {layer_scores['trend']}",
        f"动量层: {layer_scores['momentum']}",
        f"风险层: {layer_scores['risk']}",
        f"估值层: {layer_scores['valuation']}",
        f"置信度: {confidence['level']}({confidence['score']})",
    ]

    return {
        "action": action,
        "action_en": en_map[action],
        "action_type": action_type,
        "score": total_score,
        "icon": icon,
        "market_profile": market,
        "regime": regime,
        "layer_scores": layer_scores,
        "confidence": confidence,
        "key_signals": key_signals,
        "summary": f"{icon} {action} / {action_type} (综合评分: {total_score})",
    }


# ─────────────────────────────────────────────
#  主流程
# ─────────────────────────────────────────────

def analyze_stock(code: str, period: str = "6mo", use_cache: bool = True) -> dict:
    """对单只股票进行完整分析"""
    init_db()
    stock = normalize_stock_code(code)
    full_code = stock['code']

    if use_cache:
        cached = get_cached_analysis(full_code, period)
        if cached:
            aux = get_or_refresh_aux_layers(full_code, cached.get('fundamental', {}) | {'name': cached.get('fundamental', {}).get('company_name', '')}, refresh=False)
            cached['news'] = aux['news']
            cached['events'] = aux['events']
            cached['buzz'] = aux['buzz']
            cached.setdefault('data_sources', {})
            cached['data_sources']['news'] = aux['news'].get('source', 'google-news-rss')
            cached['data_sources']['event'] = aux['events'].get('source', 'news-derived')
            cached['data_sources']['buzz'] = aux['buzz'].get('source', 'news-derived-buzz')
            print(f"📦 使用缓存数据 ({full_code})，分析缓存有效期 {ANALYSIS_CACHE_TTL}s，辅助层缓存有效期 {AUX_CACHE_TTL_SECONDS}s", file=sys.stderr)
            return cached

    result = {"code": full_code, "market": stock['market'], "analysis_time": datetime.now().isoformat(), "error": None}

    try:
        quote = fetch_quote_with_fallback(full_code)
        if not quote or not quote.get("price"):
            result["error"] = f"无法获取 {full_code} 的实时行情"
            return result

        result["data_sources"] = {
            "quote": quote.get("quote_source", "tencent"),
            "kline": None,
            "news": None,
            "event": None,
            "buzz": None,
        }

        upsert_watchlist_item(
            code=full_code,
            market=quote.get('market', stock['market']),
            tencent_symbol=quote.get('tencent_symbol', stock['tencent_symbol']),
            name=quote.get('name'),
            exchange=quote.get('exchange', stock.get('exchange')),
            currency=quote.get('currency'),
            last_price=quote.get('price'),
            pe=quote.get('pe'),
            pb=quote.get('pb'),
            market_cap=quote.get('market_cap'),
            week52_high=quote.get('52w_high'),
            week52_low=quote.get('52w_low'),
            quote_time=quote.get('timestamp'),
            meta=quote,
        )

        current_price = quote["price"]
        result["current_price"] = current_price
        result["price_date"] = quote.get("timestamp", "")
        result["price_change"] = quote.get("change_amount")
        result["price_change_pct"] = quote.get("change_pct")

        days = period_to_days(period)
        hist, kline_source = refresh_kline_cache(full_code, days, period)
        result["data_sources"]["kline"] = kline_source
        if hist.empty or len(hist) < min_kline_points(days):
            result["error"] = f"无法获取 {full_code} 的历史K线数据 (仅获得 {len(hist)} 条)"
            return result

        result["data_points"] = len(hist)
        close = hist["Close"]
        high = hist["High"]
        low = hist["Low"]
        volume = hist["Volume"]

        technical = {
            "ma_trend": calc_ma_trend(close),
            "macd": calc_macd(close),
            "rsi": calc_rsi(close),
            "kdj": calc_kdj(high, low, close),
            "bollinger": calc_bollinger(close),
            "volume": calc_volume_analysis(volume, close),
        }
        result["technical"] = technical

        fundamental = get_fundamentals(quote)
        result["fundamental"] = fundamental
        result["recommendation"] = generate_recommendation(technical, fundamental, current_price, hist, quote)
        result["signal_validation"] = backtest_current_signal(hist, period)

        aux = get_or_refresh_aux_layers(full_code, quote, refresh=not use_cache)
        result["news"] = aux["news"]
        result["events"] = aux["events"]
        result["buzz"] = aux["buzz"]
        result["data_sources"]["news"] = aux["news"].get("source", "google-news-rss")
        result["data_sources"]["event"] = aux["events"].get("source", "news-derived")
        result["data_sources"]["buzz"] = aux["buzz"].get("source", "news-derived-buzz")

        if result.get("error") is None:
            set_cached_analysis(full_code, period, result)

    except Exception as e:
        result["error"] = f"分析过程出错: {str(e)}"

    return result


def main():
    parser = argparse.ArgumentParser(description="多市场股票分析工具 (腾讯财经/Yahoo 数据源)")
    parser.add_argument("code", help="股票代码，如 0700.HK / 600519 / SH600519 / AAPL")
    parser.add_argument("--period", default="6mo", help="数据周期 (1mo/3mo/6mo/1y/2y/5y)")
    parser.add_argument("--output", help="输出JSON文件路径")
    parser.add_argument("--no-cache", action="store_true", help="跳过缓存，强制重新请求数据")
    parser.add_argument("--clear-cache", action="store_true", help="清除所有缓存后退出")
    args = parser.parse_args()

    if args.clear_cache:
        cleared = clear_analysis_cache()
        if cleared:
            print(f"✅ 已清除 {cleared} 条分析缓存")
        else:
            print("ℹ️ 无缓存可清除")
        return

    result = analyze_stock(args.code, args.period, use_cache=not args.no_cache)
    output = json.dumps(result, ensure_ascii=False, indent=2, default=str)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"分析结果已保存至 {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
