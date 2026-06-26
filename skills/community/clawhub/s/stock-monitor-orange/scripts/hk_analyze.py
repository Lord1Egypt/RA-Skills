#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Direct HK stock analyzer - bypasses code format bugs in main monitor"""
import sys
import json
import time
import urllib.request
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

HK_CODES = ["00981", "00992", "01088", "00005", "00941", "06613"]
HK_NAMES = {
    "00981": "中芯国际",
    "00992": "联想集团", 
    "01088": "中国神华",
    "00005": "汇丰控股",
    "00941": "中国移动",
    "06613": "上海复旦",
}

def get_quote(code_5):
    """Get realtime quote from Tencent"""
    url = f"https://qt.gtimg.cn/q=hk{code_5}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as r:
        raw = r.read().decode('gbk', errors='ignore')
    # Parse: v_hkXXXXX="100~name~code~price~prev_close~open~volume~..."
    parts = raw.split('"')[1].split('~')
    name = parts[1]
    price = float(parts[3])
    prev_close = float(parts[4])
    change = price - prev_close
    pct = (change / prev_close) * 100
    update_time = parts[30]
    return {"name": name, "price": price, "prev_close": prev_close, "change": change, "pct": pct, "time": update_time}

def get_kline(code_5, days=60):
    """Get K-line from Tencent ifzq"""
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=hk{code_5},day,,,{days},qfq"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        content = r.read().decode('utf-8', errors='ignore')
    data = json.loads(content)
    stock_data = data.get('data', {})
    key = f'hk{code_5}'
    if key not in stock_data:
        # try without hk prefix in key
        for k in stock_data:
            if k.startswith('hk'):
                key = k
                break
    day_data = stock_data.get(key, {}).get('day', [])
    if not day_data:
        return None
    klines = []
    for item in day_data:
        klines.append({
            "date": item[0],
            "open": float(item[1]),
            "close": float(item[2]),
            "high": float(item[3]),
            "low": float(item[4]),
            "volume": float(item[5])
        })
    return klines

def calc_ma(closes, n):
    if len(closes) < n:
        return None
    return sum(closes[-n:]) / n

def calc_macd(closes, fast=12, slow=26, signal=9):
    if len(closes) < slow + signal:
        return None
    ema_fast = closes[0]
    ema_slow = closes[0]
    alpha_fast = 2 / (fast + 1)
    alpha_slow = 2 / (slow + 1)
    for c in closes[1:]:
        ema_fast = c * alpha_fast + ema_fast * (1 - alpha_fast)
        ema_slow = c * alpha_slow + ema_slow * (1 - alpha_slow)
    dif = ema_fast - ema_slow
    dea = dif * 0.8 + 0  # simplified
    macd_bar = 2 * (dif - dea)
    return {"dif": dif, "dea": dea, "bar": macd_bar, "histogram": macd_bar}

def calc_kdj(closes, highs, lows, n=9):
    if len(closes) < n:
        return None
    recent_closes = closes[-n:]
    recent_highs = highs[-n:]
    recent_lows = lows[-n:]
    low_n = min(recent_lows)
    high_n = max(recent_highs)
    if high_n == low_n:
        k = 50
    else:
        rsv = 100 * (closes[-1] - low_n) / (high_n - low_n)
        k = 2/3 * 50 + 1/3 * rsv
        d = 2/3 * 50 + 1/3 * k
        j = 3 * k - 2 * d
    return {"k": k, "d": d, "j": j, "rsv": rsv if 'rsv' in dir() else k}

def calc_rsi(closes, n=6):
    if len(closes) < n + 1:
        return None
    gains = []
    losses = []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i-1]
        if diff > 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(diff))
    avg_gain = sum(gains[-n:]) / n
    avg_loss = sum(losses[-n:]) / n
    if avg_loss == 0:
        rsi = 100
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - 100 / (1 + rs)
    return {"rsi6": rsi, "rsi12": None, "rsi24": None}

def calc_boll(closes, n=20, k=2):
    if len(closes) < n:
        return None
    recent = closes[-n:]
    mid = sum(recent) / n
    variance = sum((c - mid) ** 2 for c in recent) / n
    std = variance ** 0.5
    upper = mid + k * std
    lower = mid - k * std
    return {"upper": upper, "mid": mid, "lower": lower, "position": (closes[-1] - lower) / (upper - lower) if upper != lower else 0.5}

def calc_obv(closes, volumes):
    if len(closes) < 2:
        return {"signal": "数据不足"}
    obv = 0
    prev_close = closes[0]
    for i in range(1, len(closes)):
        if closes[i] > prev_close:
            obv += volumes[i]
        elif closes[i] < prev_close:
            obv -= volumes[i]
        prev_close = closes[i]
    # Check divergence: last 10 vs price
    if len(closes) >= 20:
        price_trend = closes[-1] - closes[-10]
        vol_trend = sum(volumes[-5:]) / 5 - sum(volumes[-10:-5]) / 5
        if price_trend < 0 and vol_trend > 0:
            signal = "底背离↑"
        elif price_trend > 0 and vol_trend < 0:
            signal = "顶背离↓"
        else:
            signal = "无背离"
    else:
        signal = "无背离"
    return {"obv": obv, "signal": signal}

def calc_dmi(highs, lows, closes, n=14):
    if len(closes) < n + 1:
        return {"pdi": None, "mdi": None, "adx": None, "signal": "数据不足"}
    # Simplified DMI
    plus_dm = 0
    minus_dm = 0
    tr = 0
    for i in range(-n, 0):
        high_diff = highs[i+1] - highs[i] if i+1 < len(highs) else 0
        low_diff = lows[i] - lows[i+1] if i+1 < len(lows) else 0
        if high_diff > low_diff and high_diff > 0:
            plus_dm += high_diff
        if low_diff > high_diff and low_diff > 0:
            minus_dm += low_diff
    return {"pdi": plus_dm / n, "mdi": minus_dm / n, "adx": None, "signal": "中性"}

def calc_wr(highs, lows, closes, n=10):
    if len(closes) < n:
        return None
    recent_highs = highs[-n:]
    recent_lows = lows[-n:]
    highest = max(recent_highs)
    lowest = min(recent_lows)
    if highest == lowest:
        wr = -50
    else:
        wr = -100 * (highest - closes[-1]) / (highest - lowest)
    return {"wr10": wr}

def analyze(code_5):
    quote = get_quote(code_5)
    klines = get_kline(code_5, 60)
    if not klines or len(klines) < 20:
        return {"error": f"无法获取 {code_5} K线数据", "quote": quote}
    
    closes = [k['close'] for k in klines]
    highs = [k['high'] for k in klines]
    lows = [k['low'] for k in klines]
    volumes = [k['volume'] for k in klines]
    
    ma5 = calc_ma(closes, 5)
    ma10 = calc_ma(closes, 10)
    ma20 = calc_ma(closes, 20)
    ma60 = calc_ma(closes, 60) if len(closes) >= 60 else None
    
    macd = calc_macd(closes)
    kdj = calc_kdj(closes, highs, lows)
    rsi = calc_rsi(closes)
    boll = calc_boll(closes)
    obv = calc_obv(closes, volumes)
    dmi = calc_dmi(highs, lows, closes)
    wr = calc_wr(highs, lows, closes)
    
    # Signals
    buy_score = 0
    sell_score = 0
    signals = []
    
    # MA signals
    if ma5 and ma10:
        if ma5 > ma10:
            buy_score += 1
            ma_signal = f"MA5({ma5:.2})>MA10({ma10:.2}) 多头 ↑"
        else:
            sell_score += 1
            ma_signal = f"MA5({ma5:.2})<MA10({ma10:.2}) 空头 ↓"
    else:
        ma_signal = "MA信号不足"
    
    # MACD signals
    if macd:
        if macd['dif'] > macd['dea']:
            buy_score += 1
            macd_signal = f"DIF({macd['dif']:.4f})>DEA({macd['dea']:.4f}) 金叉↑ 红柱"
        else:
            sell_score += 1
            macd_signal = f"DIF({macd['dif']:.4f})<DEA({macd['dea']:.4f}) 死叉↓ 绿柱"
    else:
        macd_signal = "MACD数据不足"
    
    # KDJ signals
    if kdj:
        if kdj['k'] > kdj['d']:
            buy_score += 0.5
            kdj_signal = f"K:{kdj['k']:.1f} D:{kdj['d']:.1f} J:{kdj['j']:.1f} | 金叉"
        else:
            sell_score += 0.5
            kdj_signal = f"K:{kdj['k']:.1f} D:{kdj['d']:.1f} J:{kdj['j']:.1f} | 死叉"
        if kdj['j'] < 20:
            kdj_signal += " 超卖"
        elif kdj['j'] > 80:
            kdj_signal += " 超买"
    else:
        kdj_signal = "KDJ数据不足"
    
    # RSI signals
    if rsi:
        rsi_val = rsi['rsi6']
        if rsi_val < 30:
            sell_score += 0.5
            rsi_signal = f"RSI6:{rsi_val:.1f} | 偏弱(超卖)"
        elif rsi_val > 70:
            buy_score += 0.5
            rsi_signal = f"RSI6:{rsi_val:.1f} | 偏强(超买)"
        else:
            rsi_signal = f"RSI6:{rsi_val:.1f} | 中性"
    else:
        rsi_signal = "RSI数据不足"
    
    # BOLL signals
    if boll:
        price = closes[-1]
        if price > boll['mid']:
            buy_score += 0.5
            boll_signal = f"中轨{boll['mid']:.2f}上方 通道平稳"
        else:
            sell_score += 0.5
            boll_signal = f"中轨{boll['mid']:.2f}下方 偏弱"
    else:
        boll_signal = "BOLL数据不足"
    
    overall = "买入" if buy_score > sell_score + 1 else "卖出" if sell_score > buy_score + 1 else "观望"
    stars = "⭐" * max(1, min(3, int(buy_score)))
    
    return {
        "code": code_5,
        "name": HK_NAMES.get(code_5, quote.get('name', code_5)),
        "quote": quote,
        "ma": {"ma5": ma5, "ma10": ma10, "ma20": ma20, "ma60": ma60},
        "ma_signal": ma_signal,
        "macd": macd,
        "macd_signal": macd_signal,
        "kdj": kdj,
        "kdj_signal": kdj_signal,
        "rsi": rsi,
        "rsi_signal": rsi_signal,
        "boll": boll,
        "boll_signal": boll_signal,
        "obv": obv,
        "dmi": dmi,
        "wr": wr,
        "buy_score": buy_score,
        "sell_score": sell_score,
        "overall": overall,
        "stars": stars,
        "klines": klines[-5:],  # last 5 for debugging
    }

if __name__ == "__main__":
    results = []
    for code in HK_CODES:
        try:
            r = analyze(code)
            results.append(r)
            print(f"✅ {code} {r.get('name','?')} 完成", flush=True)
        except Exception as e:
            print(f"❌ {code} 错误: {e}", flush=True)
        time.sleep(1)
    
    print("\n=== JSON RESULTS ===")
    print(json.dumps(results, ensure_ascii=False, indent=2))
