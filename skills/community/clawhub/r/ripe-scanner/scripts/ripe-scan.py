#!/usr/bin/env python3
"""
Ripe Scanner — Free momentum + social sentiment scanner for OpenClaw
Covers S&P 500 + Nasdaq 100 + crypto (~600 assets)
Zero API cost, fully local computation.

Features:
- Technical scoring: RSI, EMA 20/50, Bollinger Squeeze, Volume, 52w proximity
- Social sentiment: StockTwits + Reddit WSB
- Daily snapshots for historical win rate tracking
- Score change detection (new ripe signals)
- Crypto support (BTC, ETH, SOL, etc.)
"""
import json, os, sys, time, argparse, re
from datetime import datetime, timedelta
from pathlib import Path

CACHE_PATH = "/tmp/ripe_scanner_cache.json"
CACHE_TTL = 1800  # 30 minutes
HISTORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory/ripe_scanner")
SNAPSHOT_PATH = os.path.join(HISTORY_DIR, "snapshots")
SIGNALS_LOG = os.path.join(HISTORY_DIR, "signals_log.json")

os.makedirs(SNAPSHOT_PATH, exist_ok=True)


# ============ Universe ============

def get_sp500():
    """Fetch S&P 500 list from Wikipedia"""
    try:
        import pandas as pd
        tables = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
        return tables[0]['Symbol'].str.replace('.', '-', regex=False).tolist()
    except:
        return []

def get_nasdaq100():
    """Fetch Nasdaq 100 list from Wikipedia"""
    try:
        import pandas as pd
        tables = pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")
        for t in tables:
            for col in t.columns:
                if 'ticker' in col.lower() or 'symbol' in col.lower():
                    return t[col].tolist()
        return []
    except:
        return []

CRYPTO_TICKERS = [
    'BTC-USD', 'ETH-USD', 'SOL-USD', 'BNB-USD', 'XRP-USD',
    'ADA-USD', 'DOGE-USD', 'AVAX-USD', 'DOT-USD', 'MATIC-USD',
    'LINK-USD', 'UNI-USD', 'ATOM-USD', 'LTC-USD', 'NEAR-USD',
]

WATCHLIST_EXTRA = [
    'RKLB', 'SATS', 'MU', 'LMND', 'ONDS', 'HIMS',
    'ARM', 'SMCI', 'MRVL', 'GME', 'AMC', 'SOFI',
    'RIVN', 'LCID', 'NIO', 'XPEV', 'LI', 'GRAB', 'RBLX',
    'MSTR', 'COIN', 'HOOD', 'SNAP', 'PINS', 'U', 'ROKU',
]

# Fallback if Wikipedia parsing fails
FALLBACK_SP500 = [
    'AAPL','MSFT','AMZN','NVDA','GOOGL','META','TSLA','BRK-B','UNH','JNJ',
    'JPM','V','PG','XOM','MA','HD','CVX','MRK','ABBV','LLY','AVGO','PEP',
    'KO','COST','TMO','MCD','WMT','CSCO','ACN','ABT','DHR','ADBE','CRM',
    'CMCSA','NKE','NFLX','TXN','PM','NEE','UPS','RTX','INTC','AMD','QCOM',
    'INTU','AMAT','ISRG','BKNG','MDLZ','ADP','GILD','SYK','REGN','VRTX',
    'ADI','LRCX','PANW','MNST','KLAC','SNPS','CDNS','MELI','FTNT','DASH',
    'WDAY','ORLY','TEAM','DXCM','BIIB','ILMN','ZS','CRWD','NET','DDOG',
    'MDB','SNOW','PLTR','COIN','SQ','SHOP','SE','PDD','BIDU','JD',
    'BA','CAT','DE','GE','HON','LMT','MMM','UNP','FDX','CSX',
    'GS','MS','C','BAC','WFC','BLK','SCHW','AXP','USB','PNC',
    'PFE','BMY','AMGN','TMO','MDT','ELV','CI','HUM','ZTS','DXCM',
    'DIS','CMCSA','T','VZ','CHTR','TMUS','ATVI','EA','TTWO','PARA',
    'COP','SLB','EOG','MPC','PSX','VLO','OXY','DVN','HAL','FANG',
    'AMT','PLD','CCI','EQIX','SPG','DLR','O','WELL','AVB','EQR',
]

def get_universe(include_crypto=True):
    """Build full universe: S&P 500 + Nasdaq 100 + watchlist + crypto"""
    symbols = get_sp500()
    if len(symbols) < 100:
        print(f"  ℹ️  Wikipedia S&P 500 returned {len(symbols)}, using fallback list")
        symbols = FALLBACK_SP500.copy()
    
    ndx = get_nasdaq100()
    if ndx:
        symbols.extend(ndx)
    
    symbols.extend(WATCHLIST_EXTRA)
    
    if include_crypto:
        symbols.extend(CRYPTO_TICKERS)
    
    # Deduplicate, preserve order
    seen = set()
    unique = []
    for s in symbols:
        s = s.strip()
        if s and s not in seen:
            seen.add(s)
            unique.append(s)
    
    return unique


# ============ Technical Scoring ============

def compute_technicals(df):
    """Compute technical indicators from price DataFrame"""
    import numpy as np
    if df is None or len(df) < 50:
        return None
    
    close = df['Close'].values.astype(float)
    volume = df['Volume'].values.astype(float)
    high = df['High'].values.astype(float)
    low = df['Low'].values.astype(float)
    
    # RSI (14)
    deltas = np.diff(close)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[-14:])
    avg_loss = np.mean(losses[-14:])
    if avg_loss == 0:
        rsi = 100.0
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
    
    # EMA 20 and 50
    def ema(data, period):
        alpha = 2 / (period + 1)
        result = [float(data[0])]
        for i in range(1, len(data)):
            result.append(alpha * float(data[i]) + (1 - alpha) * result[-1])
        return np.array(result)
    
    ema20 = ema(close, 20)
    ema50 = ema(close, 50)
    
    price_above_20 = bool(close[-1] > ema20[-1])
    price_above_50 = bool(close[-1] > ema50[-1])
    ema20_above_50 = bool(ema20[-1] > ema50[-1])
    ema_score = (int(price_above_20) + int(price_above_50) + int(ema20_above_50)) / 3 * 100
    
    # Bollinger Squeeze
    sma20 = np.mean(close[-20:])
    std20 = np.std(close[-20:])
    bb_width = (2 * std20) / sma20 if sma20 > 0 else 0
    bb_widths = []
    for i in range(max(0, len(close)-50), len(close)):
        start = max(0, i-19)
        s = np.mean(close[start:i+1])
        sd = np.std(close[start:i+1])
        bb_widths.append((2*sd)/s if s > 0 else 0)
    avg_bb_width = np.mean(bb_widths) if bb_widths else bb_width
    squeeze = bool(bb_width < avg_bb_width * 0.75)
    squeeze_score = 100.0 if squeeze else max(0, (1 - bb_width/avg_bb_width) * 100) if avg_bb_width > 0 else 50
    
    # Volume surge
    avg_vol = np.mean(volume[-20:])
    vol_ratio = float(volume[-1] / avg_vol) if avg_vol > 0 else 1.0
    vol_score = min(100, vol_ratio * 50)
    
    # 52-week high proximity
    high_52w = float(np.max(high[-252:])) if len(high) >= 252 else float(np.max(high))
    proximity = close[-1] / high_52w if high_52w > 0 else 0
    proximity_score = max(0, min(100, float(proximity) * 100))
    
    # RSI score
    if 50 <= rsi <= 70:
        rsi_score = 100
    elif 40 <= rsi < 50:
        rsi_score = 70
    elif 70 < rsi <= 80:
        rsi_score = 60
    elif 30 <= rsi < 40:
        rsi_score = 50
    elif rsi > 80:
        rsi_score = 30
    else:
        rsi_score = 40
    
    return {
        'rsi': round(float(rsi), 1),
        'rsi_score': float(rsi_score),
        'ema_score': round(float(ema_score), 1),
        'ema20': round(float(ema20[-1]), 2),
        'ema50': round(float(ema50[-1]), 2),
        'squeeze': squeeze,
        'squeeze_score': round(float(squeeze_score), 1),
        'vol_ratio': round(float(vol_ratio), 2),
        'vol_score': round(float(vol_score), 1),
        'proximity_52w': round(float(proximity) * 100, 1),
        'proximity_score': round(float(proximity_score), 1),
        'price': round(float(close[-1]), 2),
        'change_1d': round(float((close[-1] / close[-2] - 1) * 100), 2) if len(close) > 1 else 0,
        'change_5d': round(float((close[-1] / close[-5] - 1) * 100), 2) if len(close) > 5 else 0,
    }


# ============ Social Sentiment ============

def get_stocktwits_sentiment(symbol):
    """StockTwits bull/bear sentiment (free, no key)"""
    import urllib.request
    # Skip crypto tickers on StockTwits (different format)
    clean_sym = symbol.replace('-USD', '.X') if '-USD' in symbol else symbol
    try:
        url = f"https://api.stocktwits.com/api/2/streams/symbol/{clean_sym}.json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
        messages = resp.get('messages', [])
        if not messages:
            return None
        bulls = sum(1 for m in messages if m.get('entities', {}).get('sentiment', {}).get('basic') == 'Bullish')
        bears = sum(1 for m in messages if m.get('entities', {}).get('sentiment', {}).get('basic') == 'Bearish')
        total = bulls + bears
        if total == 0:
            return {'bull_ratio': 0.5, 'volume': len(messages), 'bulls': 0, 'bears': 0}
        return {'bull_ratio': round(bulls / total, 2), 'volume': len(messages), 'bulls': bulls, 'bears': bears}
    except:
        return None

def get_reddit_sentiment(symbol):
    """Reddit WSB mentions and sentiment via Tavily search (Reddit blocked direct API)"""
    import urllib.request
    clean_sym = symbol.replace('-USD', '')
    try:
        # Use Tavily to search Reddit WSB
        tavily_key = os.environ.get('TAVILY_API_KEY', '')
        if not tavily_key:
            return None
        data = json.dumps({
            'api_key': tavily_key,
            'query': f'{clean_sym} site:reddit.com/r/wallstreetbets',
            'search_depth': 'basic',
            'max_results': 10
        }).encode()
        req = urllib.request.Request('https://api.tavily.com/search', data=data,
                                     headers={'Content-Type': 'application/json'})
        resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
        posts = resp.get('results', [])
        if not posts:
            return None
        
        bull_kw = ['buy','calls','moon','bullish','rocket','yolo','long','squeeze','breakout','🚀','💎']
        bear_kw = ['sell','puts','bearish','short','crash','dump','overvalued','bag','🐻']
        bull_count = bear_count = 0
        for post in posts:
            text = (post.get('title', '') + ' ' + post.get('content', '')[:200]).lower()
            if any(kw in text for kw in bull_kw): bull_count += 1
            if any(kw in text for kw in bear_kw): bear_count += 1
        
        total = bull_count + bear_count
        return {
            'mentions': len(posts), 'total_upvotes': 0,
            'bull_ratio': round(bull_count / total, 2) if total > 0 else 0.5,
            'bull_posts': bull_count, 'bear_posts': bear_count,
        }
    except:
        return None

def get_social_score(symbol):
    """Combined social sentiment score (0-100)"""
    st = get_stocktwits_sentiment(symbol)
    rd = get_reddit_sentiment(symbol)
    scores = []
    details = {}
    if st:
        scores.append(st['bull_ratio'] * 100)
        details['stocktwits'] = st
    if rd:
        scores.append(rd['bull_ratio'] * 100)
        details['reddit'] = rd
    if not scores:
        return 50, details
    return round(sum(scores) / len(scores), 1), details


# ============ Combined Scoring ============

def compute_final_score(tech, social_score):
    if tech is None:
        return 0
    return round(
        tech['rsi_score'] * 0.20 + tech['ema_score'] * 0.20 +
        tech['squeeze_score'] * 0.15 + tech['vol_score'] * 0.15 +
        tech['proximity_score'] * 0.10 + social_score * 0.20
    , 1)

def get_badge(score, rsi):
    if score >= 80 and rsi > 75:
        return '🟠 overripe'
    elif score >= 80:
        return '🍌 ripe'
    elif score >= 60:
        return '🟡 ripening'
    elif score >= 40:
        return '⚪ neutral'
    else:
        return '🔴 rotten'

def get_drivers(tech, social_score, social_details):
    drivers = []
    if tech is None:
        return drivers
    if tech['ema_score'] >= 100:
        drivers.append("Price above EMA20 & EMA50 — uptrend confirmed")
    if tech['squeeze']:
        drivers.append("Bollinger Squeeze detected — breakout potential")
    if tech['proximity_52w'] > 95:
        drivers.append("Near 52-week high — strength confirmed")
    if tech['vol_ratio'] > 1.5:
        drivers.append(f"Volume surge {tech['vol_ratio']:.1f}x above average")
    if tech['rsi'] > 70:
        drivers.append(f"RSI {tech['rsi']:.0f} — overbought warning")
    elif tech['rsi'] < 30:
        drivers.append(f"RSI {tech['rsi']:.0f} — oversold, bounce potential")
    elif 50 <= tech['rsi'] <= 65:
        drivers.append(f"RSI {tech['rsi']:.0f} — healthy momentum zone")
    if social_score > 70:
        drivers.append("Strong bullish social sentiment")
    elif social_score < 30:
        drivers.append("Bearish social sentiment")
    st = social_details.get('stocktwits')
    if st and st.get('volume', 0) > 20:
        drivers.append(f"StockTwits active: {st['bulls']}🐂 vs {st['bears']}🐻")
    rd = social_details.get('reddit')
    if rd and rd.get('mentions', 0) > 10:
        drivers.append(f"Reddit WSB: {rd['mentions']} mentions this week")
    return drivers


# ============ Batch Scan ============

def scan_batch(symbols, with_sentiment=False):
    """Scan multiple symbols with batched downloads"""
    import yfinance as yf
    import numpy as np
    
    results = []
    batch_size = 100
    all_data = {}
    
    print(f"📊 Downloading data for {len(symbols)} tickers...")
    for i in range(0, len(symbols), batch_size):
        batch = symbols[i:i+batch_size]
        pct = (i + len(batch)) / len(symbols) * 100
        print(f"  📥 Batch {i//batch_size+1}/{(len(symbols)-1)//batch_size+1} ({pct:.0f}%)")
        try:
            data = yf.download(batch, period='1y', interval='1d', progress=False, threads=True)
            if data is not None and not data.empty:
                import pandas as pd
                if isinstance(data.columns, pd.MultiIndex):
                    for sym in batch:
                        try:
                            sym_data = data.xs(sym, level=1, axis=1)
                            if not sym_data.empty and len(sym_data.dropna()) > 50:
                                all_data[sym] = sym_data.dropna()
                        except:
                            pass
                elif len(batch) == 1:
                    if len(data.dropna()) > 50:
                        all_data[batch[0]] = data.dropna()
        except Exception as e:
            print(f"  ⚠️ Batch error: {e}")
    
    print(f"📈 Computing technicals for {len(all_data)} tickers...")
    for sym, df in all_data.items():
        try:
            tech = compute_technicals(df)
            if tech is None:
                continue
            result = {
                'symbol': sym, 'technicals': tech, 'social_score': 50,
                'social_details': {}, 'price': tech['price'],
                'change_1d': tech['change_1d'], 'change_5d': tech['change_5d'],
                'is_crypto': '-USD' in sym,
            }
            result['score'] = compute_final_score(tech, 50)
            result['badge'] = get_badge(result['score'], tech['rsi'])
            result['drivers'] = get_drivers(tech, 50, {})
            results.append(result)
        except:
            pass
    
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Add sentiment for top N
    if with_sentiment and results:
        top_n = min(50, len(results))
        print(f"💬 Fetching sentiment for top {top_n} tickers...")
        for idx, r in enumerate(results[:top_n]):
            if idx % 10 == 0:
                print(f"  💬 {idx}/{top_n}...")
            try:
                social_score, social_details = get_social_score(r['symbol'])
                r['social_score'] = social_score
                r['social_details'] = social_details
                r['score'] = compute_final_score(r['technicals'], social_score)
                r['badge'] = get_badge(r['score'], r['technicals']['rsi'])
                r['drivers'] = get_drivers(r['technicals'], social_score, social_details)
            except:
                pass
            time.sleep(0.3)
        results.sort(key=lambda x: x['score'], reverse=True)
    
    return results


def scan_single(symbols):
    """Scan individual symbols with full sentiment"""
    import yfinance as yf
    results = []
    for sym in symbols:
        try:
            tk = yf.Ticker(sym)
            df = tk.history(period='1y', interval='1d')
            if df is None or len(df) < 50:
                print(f"⚠️ {sym}: Insufficient data")
                continue
            tech = compute_technicals(df)
            if tech is None:
                continue
            social_score, social_details = get_social_score(sym)
            result = {
                'symbol': sym, 'technicals': tech,
                'social_score': social_score, 'social_details': social_details,
                'price': tech['price'], 'change_1d': tech['change_1d'],
                'change_5d': tech['change_5d'], 'is_crypto': '-USD' in sym,
            }
            result['score'] = compute_final_score(tech, social_score)
            result['badge'] = get_badge(result['score'], tech['rsi'])
            result['drivers'] = get_drivers(tech, social_score, social_details)
            results.append(result)
        except Exception as e:
            print(f"⚠️ {sym}: {e}")
    return results


# ============ Snapshots & History ============

def save_snapshot(results):
    """Save daily snapshot for historical tracking"""
    today = datetime.now().strftime('%Y-%m-%d')
    snapshot = {
        'date': today,
        'timestamp': time.time(),
        'count': len(results),
        'results': [{
            'symbol': r['symbol'], 'score': r['score'],
            'badge': r['badge'], 'price': r['price'],
            'change_1d': r['change_1d'], 'change_5d': r['change_5d'],
            'rsi': r['technicals']['rsi'],
            'social_score': r['social_score'],
        } for r in results],
    }
    path = os.path.join(SNAPSHOT_PATH, f"{today}.json")
    with open(path, 'w') as f:
        json.dump(snapshot, f, indent=2)
    print(f"📸 Snapshot saved: {path}")
    
    # Log ripe signals for win rate tracking
    ripe_signals = [r for r in results if r['score'] >= 80 and 'overripe' not in r['badge']]
    if ripe_signals:
        log_signals(ripe_signals, today)

def log_signals(signals, date):
    """Append ripe signals to log for win rate tracking"""
    log = []
    if os.path.exists(SIGNALS_LOG):
        try:
            with open(SIGNALS_LOG) as f:
                log = json.load(f)
        except:
            log = []
    
    for s in signals:
        log.append({
            'date': date, 'symbol': s['symbol'], 'score': s['score'],
            'entry_price': s['price'], 'rsi': s['technicals']['rsi'],
            'result_1d': None, 'result_5d': None,  # Filled later
        })
    
    with open(SIGNALS_LOG, 'w') as f:
        json.dump(log, f, indent=2)

def update_signal_results():
    """Check past signals and fill in actual results"""
    import yfinance as yf
    if not os.path.exists(SIGNALS_LOG):
        print("No signal log found.")
        return
    
    with open(SIGNALS_LOG) as f:
        log = json.load(f)
    
    updated = 0
    symbols_needed = set()
    for entry in log:
        if entry.get('result_5d') is None:
            symbols_needed.add(entry['symbol'])
    
    if not symbols_needed:
        print("All signals already have results.")
        return
    
    print(f"📊 Updating results for {len(symbols_needed)} symbols...")
    prices = {}
    for sym in symbols_needed:
        try:
            tk = yf.Ticker(sym)
            hist = tk.history(period='1mo', interval='1d')
            if hist is not None and len(hist) > 0:
                prices[sym] = {d.strftime('%Y-%m-%d'): float(row['Close']) for d, row in hist.iterrows()}
        except:
            pass
    
    for entry in log:
        if entry.get('result_5d') is not None:
            continue
        sym = entry['symbol']
        if sym not in prices:
            continue
        
        entry_date = datetime.strptime(entry['date'], '%Y-%m-%d')
        sym_prices = prices[sym]
        sorted_dates = sorted(sym_prices.keys())
        
        try:
            idx = sorted_dates.index(entry['date'])
        except ValueError:
            continue
        
        # 1-day result
        if idx + 1 < len(sorted_dates) and entry.get('result_1d') is None:
            next_price = sym_prices[sorted_dates[idx + 1]]
            entry['result_1d'] = round((next_price / entry['entry_price'] - 1) * 100, 2)
            updated += 1
        
        # 5-day result
        if idx + 5 < len(sorted_dates):
            day5_price = sym_prices[sorted_dates[idx + 5]]
            entry['result_5d'] = round((day5_price / entry['entry_price'] - 1) * 100, 2)
            updated += 1
    
    with open(SIGNALS_LOG, 'w') as f:
        json.dump(log, f, indent=2)
    print(f"✅ Updated {updated} signal results")

def print_win_rate():
    """Print historical signal win rate stats"""
    if not os.path.exists(SIGNALS_LOG):
        print("No signal history yet. Run daily scans to build history.")
        return
    
    with open(SIGNALS_LOG) as f:
        log = json.load(f)
    
    # Update results first
    update_signal_results()
    with open(SIGNALS_LOG) as f:
        log = json.load(f)
    
    total = len(log)
    has_1d = [e for e in log if e.get('result_1d') is not None]
    has_5d = [e for e in log if e.get('result_5d') is not None]
    
    print(f"\n📊 SIGNAL PERFORMANCE HISTORY")
    print(f"{'='*50}")
    print(f"  Total signals logged: {total}")
    
    if has_1d:
        wins_1d = sum(1 for e in has_1d if e['result_1d'] > 0)
        avg_1d = sum(e['result_1d'] for e in has_1d) / len(has_1d)
        print(f"\n  1-Day Performance ({len(has_1d)} signals):")
        print(f"    Win Rate: {wins_1d/len(has_1d)*100:.1f}%")
        print(f"    Avg Return: {avg_1d:+.2f}%")
    
    if has_5d:
        wins_5d = sum(1 for e in has_5d if e['result_5d'] > 0)
        avg_5d = sum(e['result_5d'] for e in has_5d) / len(has_5d)
        print(f"\n  5-Day Performance ({len(has_5d)} signals):")
        print(f"    Win Rate: {wins_5d/len(has_5d)*100:.1f}%")
        print(f"    Avg Return: {avg_5d:+.2f}%")
    
    # Best and worst
    if has_5d:
        best = max(has_5d, key=lambda x: x['result_5d'])
        worst = min(has_5d, key=lambda x: x['result_5d'])
        print(f"\n  🏆 Best: ${best['symbol']} {best['result_5d']:+.1f}% (score {best['score']}, {best['date']})")
        print(f"  💀 Worst: ${worst['symbol']} {worst['result_5d']:+.1f}% (score {worst['score']}, {worst['date']})")
    
    if not has_1d and not has_5d:
        print("  No results yet — signals need 1-5 trading days to mature.")
    print()


# ============ Score Change Detection ============

def detect_changes(current_results):
    """Compare with yesterday's snapshot to find new/changed signals"""
    # Find most recent snapshot before today
    today = datetime.now().strftime('%Y-%m-%d')
    snapshots = sorted(Path(SNAPSHOT_PATH).glob('*.json'), reverse=True)
    prev_snapshot = None
    for sp in snapshots:
        if sp.stem != today:
            try:
                with open(sp) as f:
                    prev_snapshot = json.load(f)
                break
            except:
                continue
    
    if prev_snapshot is None:
        return None
    
    prev_scores = {r['symbol']: r for r in prev_snapshot.get('results', [])}
    changes = {'new_ripe': [], 'upgraded': [], 'downgraded': [], 'biggest_jumps': []}
    
    for r in current_results:
        sym = r['symbol']
        prev = prev_scores.get(sym)
        if prev is None:
            continue
        
        delta = r['score'] - prev['score']
        badge_now = r['badge'].split(' ')[1] if ' ' in r['badge'] else r['badge']
        badge_prev = prev['badge'].split(' ')[1] if ' ' in prev['badge'] else prev['badge']
        
        if badge_now == 'ripe' and badge_prev != 'ripe':
            changes['new_ripe'].append({**r, 'prev_score': prev['score'], 'delta': delta})
        elif delta >= 10:
            changes['upgraded'].append({**r, 'prev_score': prev['score'], 'delta': delta})
        elif delta <= -10:
            changes['downgraded'].append({**r, 'prev_score': prev['score'], 'delta': delta})
        
        if abs(delta) >= 5:
            changes['biggest_jumps'].append({**r, 'prev_score': prev['score'], 'delta': delta})
    
    changes['biggest_jumps'].sort(key=lambda x: abs(x['delta']), reverse=True)
    changes['prev_date'] = prev_snapshot.get('date', '?')
    return changes

def print_changes(changes):
    """Print score changes vs previous snapshot"""
    if changes is None:
        print("\n📊 No previous snapshot to compare against. Run again tomorrow!")
        return
    
    print(f"\n🔄 CHANGES vs {changes['prev_date']}")
    print(f"{'='*55}")
    
    if changes['new_ripe']:
        print(f"\n  🆕 Newly Ripe (just crossed 80+):")
        for r in changes['new_ripe']:
            print(f"    🍌 ${r['symbol']:<6} {r['prev_score']:.0f} → {r['score']:.0f} (+{r['delta']:.0f})  ${r['price']:.2f}")
    
    if changes['upgraded']:
        print(f"\n  📈 Big Upgrades (+10 or more):")
        for r in changes['upgraded'][:10]:
            print(f"    ⬆️  ${r['symbol']:<6} {r['prev_score']:.0f} → {r['score']:.0f} (+{r['delta']:.0f})  ${r['price']:.2f}")
    
    if changes['downgraded']:
        print(f"\n  📉 Big Downgrades (-10 or more):")
        for r in changes['downgraded'][:10]:
            print(f"    ⬇️  ${r['symbol']:<6} {r['prev_score']:.0f} → {r['score']:.0f} ({r['delta']:.0f})  ${r['price']:.2f}")
    
    if not changes['new_ripe'] and not changes['upgraded'] and not changes['downgraded']:
        print("  No significant changes detected.")
    print()


# ============ Output Formatting ============

def print_top(results, limit=10):
    print(f"\n🏆 TOP {min(limit, len(results))} MOMENTUM SIGNALS")
    print(f"{'Symbol':<10} {'Score':>5} {'Badge':<14} {'Price':>10} {'1d':>8} {'5d':>8} {'RSI':>5} {'Sent':>5}")
    print("-" * 72)
    for r in results[:limit]:
        t = r['technicals']
        sym = r['symbol']
        crypto = '₿' if r.get('is_crypto') else ' '
        print(f"{crypto}${sym:<8} {r['score']:>5.0f} {r['badge']:<14} ${r['price']:>9.2f} {r['change_1d']:>+7.1f}% {r['change_5d']:>+7.1f}% {t['rsi']:>5.0f} {r['social_score']:>4.0f}")
        if r['drivers']:
            print(f"          ↳ {', '.join(r['drivers'][:3])}")
    print()

def print_lookup(results):
    for r in results:
        t = r['technicals']
        asset_type = "Crypto" if r.get('is_crypto') else "Stock"
        print(f"\n{'='*60}")
        print(f"  ${r['symbol']}  —  {r['badge']}  Score: {r['score']:.0f}/100  [{asset_type}]")
        print(f"{'='*60}")
        print(f"  Price: ${r['price']:.2f}  |  1d: {r['change_1d']:+.1f}%  |  5d: {r['change_5d']:+.1f}%")
        print(f"\n  📊 Technical Profile:")
        print(f"     RSI(14): {t['rsi']:.1f}  {'⚠️ OVERBOUGHT' if t['rsi']>70 else '⚠️ OVERSOLD' if t['rsi']<30 else '✅'}")
        print(f"     EMA20: ${t['ema20']:.2f}  |  EMA50: ${t['ema50']:.2f}  |  Alignment: {t['ema_score']:.0f}%")
        print(f"     Squeeze: {'🔥 YES' if t['squeeze'] else 'No'}  |  Volume: {t['vol_ratio']:.1f}x avg")
        print(f"     52w High Proximity: {t['proximity_52w']:.1f}%")
        print(f"\n  💬 Social Sentiment: {r['social_score']:.0f}/100")
        st = r['social_details'].get('stocktwits')
        if st:
            print(f"     StockTwits: {st['bulls']}🐂 / {st['bears']}🐻  ({st['bull_ratio']*100:.0f}% bullish)  [{st['volume']} msgs]")
        rd = r['social_details'].get('reddit')
        if rd:
            print(f"     Reddit WSB: {rd['mentions']} mentions  |  {rd['bull_posts']}🐂 / {rd['bear_posts']}🐻  |  {rd['total_upvotes']} upvotes")
        if r['drivers']:
            print(f"\n  🎯 Key Drivers:")
            for d in r['drivers']:
                print(f"     • {d}")
        print()

def print_sentiment(results):
    for r in results:
        print(f"\n💬 ${r['symbol']} Social Sentiment: {r['social_score']:.0f}/100")
        st = r['social_details'].get('stocktwits')
        if st:
            bar_len = 20
            bull_bars = int(st['bull_ratio'] * bar_len)
            bar = '🟢' * bull_bars + '🔴' * (bar_len - bull_bars)
            print(f"   StockTwits: {bar} {st['bull_ratio']*100:.0f}% bullish")
            print(f"   {st['bulls']} bulls / {st['bears']} bears / {st['volume']} total msgs")
        else:
            print(f"   StockTwits: No data")
        rd = r['social_details'].get('reddit')
        if rd:
            print(f"   Reddit WSB: {rd['mentions']} mentions, {rd['total_upvotes']} upvotes")
            print(f"   {rd['bull_posts']} bullish / {rd['bear_posts']} bearish posts")
        else:
            print(f"   Reddit WSB: No recent mentions")

def print_pulse(results):
    badges = {}
    crypto_count = 0
    for r in results:
        badge_name = r['badge'].split(' ')[1] if ' ' in r['badge'] else 'neutral'
        badges[badge_name] = badges.get(badge_name, 0) + 1
        if r.get('is_crypto'):
            crypto_count += 1
    
    total = len(results)
    print(f"\n🌡️ MARKET PULSE — {total} assets scanned ({total - crypto_count} stocks + {crypto_count} crypto)")
    print(f"{'='*55}")
    for badge, emoji in [('ripe','🍌'), ('ripening','🟡'), ('overripe','🟠'), ('neutral','⚪'), ('rotten','🔴')]:
        c = badges.get(badge, 0)
        pct = c/total*100 if total > 0 else 0
        label = {'ripe':'Ripe (strong)','ripening':'Ripening','overripe':'Overripe (overbought)','neutral':'Neutral','rotten':'Rotten (weak)'}[badge]
        bar = '█' * int(pct / 2)
        print(f"  {emoji} {label:<24} {c:>4}  ({pct:>4.1f}%)  {bar}")
    
    ripe = [r for r in results if 'ripe' in r['badge'] and 'overripe' not in r['badge']]
    if ripe:
        print(f"\n  🏆 Top Ripe Signals:")
        for r in ripe[:8]:
            sym_prefix = '₿' if r.get('is_crypto') else ' '
            print(f"    {sym_prefix}${r['symbol']:<8} {r['score']:.0f}pts  ${r['price']:.2f}  {r['change_1d']:+.1f}%")
    
    overripe = [r for r in results if 'overripe' in r['badge']]
    if overripe:
        print(f"\n  ⚠️ Overripe (overbought):")
        for r in overripe[:5]:
            print(f"     ${r['symbol']:<8} RSI {r['technicals']['rsi']:.0f}  ${r['price']:.2f}")
    
    by_change = sorted(results, key=lambda x: abs(x['change_1d']), reverse=True)
    print(f"\n  🚀 Biggest Movers Today:")
    for r in by_change[:8]:
        emoji = '📈' if r['change_1d'] > 0 else '📉'
        print(f"     {emoji} ${r['symbol']:<8} {r['change_1d']:+.1f}%  (score: {r['score']:.0f})")
    print()


# ============ Cache ============

def load_cache():
    try:
        with open(CACHE_PATH) as f:
            cache = json.load(f)
        if time.time() - cache.get('timestamp', 0) < CACHE_TTL:
            return cache.get('results', [])
    except:
        pass
    return None

def save_cache(results):
    with open(CACHE_PATH, 'w') as f:
        json.dump({'timestamp': time.time(), 'scanned_at': datetime.now().isoformat(),
                    'count': len(results), 'results': results}, f)


# ============ Main ============

def main():
    parser = argparse.ArgumentParser(description='Ripe Scanner — Free Momentum + Sentiment Scanner')
    parser.add_argument('command', choices=['top', 'lookup', 'sentiment', 'pulse', 'changes', 'history', 'snapshot'],
                       help='top/lookup/sentiment/pulse/changes/history/snapshot')
    parser.add_argument('symbols', nargs='*', help='Ticker symbols (for lookup/sentiment)')
    parser.add_argument('--limit', type=int, default=10, help='Number of results')
    parser.add_argument('--min-score', type=int, default=0, help='Minimum score filter')
    parser.add_argument('--no-cache', action='store_true', help='Force fresh scan')
    parser.add_argument('--sentiment', action='store_true', help='Include sentiment in scan')
    parser.add_argument('--no-crypto', action='store_true', help='Exclude crypto')
    args = parser.parse_args()
    
    if args.command in ('lookup', 'sentiment') and not args.symbols:
        print("❌ Provide at least one ticker (e.g., TSLA AAPL BTC-USD)")
        sys.exit(1)
    
    if args.command == 'history':
        print_win_rate()
        return
    
    if args.command == 'lookup':
        results = scan_single(args.symbols)
        print_lookup(results)
        return
    
    if args.command == 'sentiment':
        results = scan_single(args.symbols)
        print_sentiment(results)
        return
    
    # Commands that need full scan
    results = None if args.no_cache else load_cache()
    if results is None:
        universe = get_universe(include_crypto=not args.no_crypto)
        print(f"🔍 Scanning {len(universe)} assets...")
        results = scan_batch(universe, with_sentiment=args.sentiment)
        save_cache(results)
        print(f"💾 Cached {len(results)} results")
    else:
        print(f"📦 Using cached data ({len(results)} assets)")
    
    if args.min_score > 0:
        results = [r for r in results if r['score'] >= args.min_score]
    
    if args.command == 'top':
        print_top(results, args.limit)
    elif args.command == 'pulse':
        print_pulse(results)
    elif args.command == 'changes':
        changes = detect_changes(results)
        print_changes(changes)
    elif args.command == 'snapshot':
        save_snapshot(results)
        print(f"✅ Snapshot saved with {len(results)} assets")

if __name__ == '__main__':
    main()
