#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""量化交易信号"""

import yfinance as yf
import numpy as np
import sys

def get_data(symbol, days=60):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=f'{days}d')
        if hist is None or len(hist) < 30:
            return None
        return [{'close': row['Close'], 'high': row['High'], 'low': row['Low']} for _, row in hist.iterrows()]
    except:
        return None

def calc_ema(prices, period):
    ema = []
    mult = 2 / (period + 1)
    sma = sum(prices[:period]) / period
    ema.append(sma)
    for p in prices[period:]:
        ema.append((p - ema[-1]) * mult + ema[-1])
    return ema

def calc_macd(prices):
    closes = [p['close'] for p in prices]
    ema12 = calc_ema(closes, 12)
    ema26 = calc_ema(closes, 26)
    diff = len(ema12) - len(ema26)
    ema12 = ema12[diff:]
    dif = [ema12[i] - ema26[i] for i in range(len(ema26))]
    dea = calc_ema(dif, 9)
    diff2 = len(dif) - len(dea)
    dif = dif[diff2:]
    macd = [(dif[i] - dea[i]) * 2 for i in range(len(dea))]
    return {'dif': dif[-1] if dif else 0, 'dea': dea[-1] if dea else 0, 'macd': macd[-1] if macd else 0}

def calc_rsi(prices, period=14):
    closes = [p['close'] for p in prices]
    deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    avg_g = sum(gains[:period]) / period
    avg_l = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_g = (avg_g * (period - 1) + gains[i]) / period
        avg_l = (avg_l * (period - 1) + losses[i]) / period
    if avg_l == 0:
        return 100
    return 100 - (100 / (1 + avg_g / avg_l))

def calc_ma(prices, period):
    return sum([p['close'] for p in prices[-period:]]) / period

def calc_bb(prices, period=20):
    closes = [p['close'] for p in prices]
    ma = sum(closes[-period:]) / period
    std = (sum([(c - ma) ** 2 for c in closes[-period:]]) / period) ** 0.5
    return ma + 2 * std, ma, ma - 2 * std

def analyze(symbol):
    print(f"\n{'='*45}")
    print(f"量化信号: {symbol}")
    print('='*45)
    
    data = get_data(symbol)
    if not data:
        print("❌ 数据获取失败")
        return
    
    latest = data[-1]['close']
    print(f"💰 价格: {latest:.2f}")
    
    # MACD
    macd = calc_macd(data)
    macd_sig = "🟢" if macd['dif'] > macd['dea'] else "🔴"
    print(f"\nMACD: DIF={macd['dif']:.1f} DEA={macd['dea']:.1f} | {macd_sig}")
    
    # RSI
    rsi = calc_rsi(data)
    if rsi > 70:
        rsi_sig = "🔴超买"
    elif rsi < 30:
        rsi_sig = "🔵超卖"
    elif rsi > 50:
        rsi_sig = "🟢偏多"
    else:
        rsi_sig = "🔴偏空"
    print(f"RSI: {rsi:.1f} | {rsi_sig}")
    
    # MA
    ma5 = calc_ma(data, 5)
    ma10 = calc_ma(data, 10)
    if ma5 > ma10:
        ma_sig = "🟢多头"
    else:
        ma_sig = "🔴空头"
    print(f"均线: MA5={ma5:.1f} MA10={ma10:.1f} | {ma_sig}")
    
    # BB
    upper, middle, lower = calc_bb(data)
    if latest > upper:
        bb_sig = "🔴突破上轨"
    elif latest < lower:
        bb_sig = "🔵突破下轨"
    else:
        bb_sig = "⚪中轨附近"
    print(f"布林: 上={upper:.1f} 中={middle:.1f} 下={lower:.1f} | {bb_sig}")
    
    # 综合
    bullish = 0
    if macd['dif'] > macd['dea']:
        bullish += 1
    if rsi < 30:
        bullish += 1
    elif rsi > 70:
        bullish -= 1
    if ma5 > ma10:
        bullish += 1
    if latest < lower:
        bullish += 1
    elif latest > upper:
        bullish -= 1
    
    if bullish >= 2:
        strength = "⭐⭐⭐ 看多"
        advice = "关注买入"
    elif bullish >= 1:
        strength = "⭐⭐ 偏多"
        advice = "可关注"
    elif bullish >= 0:
        strength = "⭐ 偏空"
        advice = "观望"
    else:
        strength = "⭐⭐⭐ 看空"
        advice = "注意风险"
    
    print(f"\n🎯 综合: {strength} | 建议: {advice}")
    print('='*45)

if __name__ == "__main__":
    symbols = sys.argv[1:] if len(sys.argv) > 1 else ['AAPL', 'BTC-USD']
    for s in symbols:
        analyze(s)
