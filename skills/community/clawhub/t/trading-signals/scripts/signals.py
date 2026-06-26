#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化交易信号脚本
"""

import yfinance as yf
import numpy as np
import sys


def get_klines(symbol, days=60):
    """获取K线数据"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=f'{days}d')
        
        if hist is None or len(hist) < 30:
            return None
        
        data = []
        for idx, row in hist.iterrows():
            data.append({
                'date': idx,
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                'volume': row['Volume']
            })
        
        return data
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None


def calculate_ema(prices, period):
    """计算EMA"""
    ema = []
    multiplier = 2 / (period + 1)
    
    # 初始SMA
    sma = sum(prices[:period]) / period
    ema.append(sma)
    
    # EMA
    for price in prices[period:]:
        ema_val = (price - ema[-1]) * multiplier + ema[-1]
        ema.append(ema_val)
    
    return ema


def calculate_macd(prices, fast=12, slow=26, signal=9):
    """计算MACD"""
    closes = [p['close'] for p in prices]
    
    ema_fast = calculate_ema(closes, fast)
    ema_slow = calculate_ema(closes, slow)
    
    # 对齐长度
    diff = len(ema_fast) - len(ema_slow)
    ema_fast = ema_fast[diff:]
    
    dif = [ema_fast[i] - ema_slow[i] for i in range(len(ema_slow))]
    dea = calculate_ema(dif, signal)
    
    # 对齐
    diff2 = len(dif) - len(dea)
    dif = dif[diff2:]
    
    macd = [(dif[i] - dea[i]) * 2 for i in range(len(dea))]
    
    return {
        'dif': dif[-1] if dif else 0,
        'dea': dea[-1] if dea else 0,
        'macd': macd[-1] if macd else 0,
        'hist': macd,
        'dif_list': dif,
        'dea_list': dea
    }


def calculate_rsi(prices, period=14):
    """计算RSI"""
    closes = [p['close'] for p in prices]
    
    deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    rsi = []
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
        if avg_loss == 0:
            rsi.append(100)
        else:
            rs = avg_gain / avg_loss
            rsi.append(100 - (100 / (1 + rs)))
    
    return rsi[-1] if rsi else 50


def calculate_kdj(klines):
    """计算KDJ"""
    closes = [k['close'] for k in klines]
    lows = [k['low'] for k in klines]
    highs = [k['high'] for k in klines]
    
    period = 9
    
    kdj_values = []
    for i in range(period, len(closes)):
        low_n = min(lows[i-period:i])
        high_n = max(highs[i-period:i])
        
        rsv = (closes[i] - low_n) / (high_n - low_n) * 100 if high_n > low_n else 50
        
        if len(kdj_values) == 0:
            k = d = rsv
        else:
            k = kdj_values[-1][0] * 2/3 + rsv / 3
            d = kdj_values[-1][1] * 2/3 + k / 3
        
        j = 3 * k - 2 * d
        kdj_values.append((k, d, j))
    
    return kdj_values[-1] if kdj_values else (50, 50, 50)


def calculate_ma(prices, period):
    """计算均线"""
    closes = [p['close'] for p in prices]
    return sum(closes[-period:]) / period


def calculate_bollinger(prices, period=20):
    """计算布林带"""
    closes = [p['close'] for p in prices]
    
    ma = sum(closes[-period:]) / period
    
    variance = sum([(c - ma) ** 2 for c in closes[-period:]]) / period
    std = variance ** 0.5
    
    upper = ma + 2 * std
    lower = ma - 2 * std
    
    return upper, ma, lower


def analyze_signals(symbol):
    """分析信号"""
    print(f"\n{'='*55}")
    print(f"量化信号: {symbol}")
    print('='*55)
    
    # 获取数据
    klines = get_klines(symbol, 60)
    if klines is None:
        print("❌ 数据获取失败")
        return
    
    print(f"📊 数据: {len(klines)}根K线")
    
    # 最新价格
    latest = klines[-1]
    prev = klines[-2] if len(klines) > 1 else latest
    change = (latest['close'] - prev['close']) / prev['close'] * 100
    
    print(f"💰 价格: {latest['close']:.2f} ({change:+.2f}%)")
    
    # MACD
    macd = calculate_macd(klines)
    print(f"\n📊 MACD信号:")
    print(f"   DIF: {macd['dif']:.2f} | DEA: {macd['dea']:.2f} | MACD: {macd['macd']:.2f}")
    
    # MACD信号判断
    if len(macd['dif_list']) > 1 and len(macd['dea_list']) > 1:
        prev_dif, prev_dea = macd['dif_list'][-2], macd['dea_list'][-2]
        curr_dif, curr_dea = macd['dif'], macd['dea']
        
        if prev_dif < prev_dea and curr_dif > curr_dea:
            macd_signal = "🟢 金叉"
        elif prev_dif > prev_dea and curr_dif < curr_dea:
            macd_signal = "🔴 死叉"
        elif curr_dif > curr_dea:
            macd_signal = "🟡 多头"
        else:
            macd_signal = "⚫ 空头"
        
        # 背离检查
        prices = [k['close'] for k in klines[-20:]]
        if prices[-1] < min(prices) and macd['macd'] > min(macd['hist'][-20:]):
            macd_signal += " | ⚠️ 底背离"
        elif prices[-1] > max(prices) and macd['macd'] < max(macd['hist'][-20:]):
            macd_signal += " | ⚠️ 顶背离"
    else:
        macd_signal = "数据不足"
    
    print(f"   信号: {macd_signal}")
    
    # RSI
    rsi = calculate_rsi(klines)
    print(f"\n📊 RSI信号:")
    print(f"   RSI(14): {rsi:.2f}")
    
    if rsi > 70:
        rsi_signal = "🔴 超买区"
    elif rsi < 30:
        rsi_signal = "🔵 超卖区"
    elif rsi > 50:
        rsi_signal = "🟢 偏多"
    else:
        rsi_signal = "🔴 偏空"
    
    print(f"   信号: {rsi_signal}")
    
    # KDJ
    k, d, j = calculate_kdj(klines)
    print(f"\n📊 KDJ信号:")
    print(f"   K: {k:.2f} | D: {d:.2f} | J: {j:.2f}")
    
    if j > 100:
        kdj_signal = "🔴 超买"
    elif j < 0:
        kdj_signal = "🔵 超卖"
    elif k > d:
        kdj_signal = "🟢 金叉"
    else:
        kdj_signal = "🔴 死叉"
    
    print(f"   信号: {kdj_signal}")
    
    # 均线
    ma5 = calculate_ma(klines, 5)
    ma10 = calculate_ma(klines, 10)
    ma20 = calculate_ma(klines, 20)
    
    print(f"\n📊 均线信号:")
    print(f"   MA5: {ma5:.2f} | MA10: {ma10:.2f} | MA20: {ma20:.2f}")
    
    if ma5 > ma10 > ma20:
        ma_signal = "🟢 多头排列"
    elif ma5 < ma10 < ma20:
        ma_signal = "🔴 空头排列"
    elif ma5 > ma10:
        ma_signal = "🟡 短期偏多"
    else:
        ma_signal = "⚫ 短期偏空"
    
    print(f"   信号: {ma_signal}")
    
    # 布林带
    upper, middle, lower = calculate_bollinger(klines)
    print(f"\n📊 布林带:")
    print(f"   上轨: {upper:.2f} | 中轨: {middle:.2f} | 下轨: {lower:.2f}")
    
    if latest['close'] > upper:
        bb_signal = "🔴 突破上轨"
    elif latest['close'] < lower:
        bb_signal = "🔵 突破下轨"
    elif latest['close'] > middle:
        bb_signal = "🟡 中轨上方"
    else:
        bb_signal = "⚪ 中轨下方"
    
    print(f"   信号: {bb_signal}")
    
    # 综合信号
    print(f"\n🎯 综合信号:")
    
    # 统计信号
    bullish = 0
    bearish = 0
    
    # MACD
    if macd['dif'] > macd['dea']:
        bullish += 1
    else:
        bearish += 1
    
    # RSI
    if rsi < 30:
        bullish += 1  # 超卖是机会
    elif rsi > 70:
        bearish += 1  # 超买是风险
    elif rsi > 50:
        bullish += 0.5
    else:
        bearish += 0.5
    
    # KDJ
    if j < 0:
        bullish += 1  # 超卖
    elif j > 100:
        bearish += 1  # 超买
    elif k > d:
        bullish += 0.5
    else:
        bearish += 0.5
    
    # 均线
    if ma5 > ma10:
        bullish += 1
    else:
        bearish += 1
    
    # 布林带
    if latest['close'] < lower:
        bullish += 1
    elif latest['close'] > upper:
        bearish += 1
    
    total = bullish + bearish
    
    if bullish >= total * 0.7:
        strength = "⭐⭐⭐ 强烈看多"
        advice = "关注买入机会"
    elif bullish >= total * 0.5:
        strength = "⭐⭐ 偏多"
        advice = "可以适当关注"
    elif bullish >= total * 0.3:
        strength = "⭐ 偏空"
        advice = "建议观望或减仓"
    else:
        strength = "⭐⭐⭐ 强烈看空"
        advice = "注意风险"
    
    print(f"   多头信号: {bullish:.1f} | 空头信号: {bearish:.1f}")
    print(f"   强度: {strength}")
    print(f"   建议: {advice}")
    
    print(f"\n{'='*55}")


def main():
    if len(sys.argv) < 2:
        symbols = ['AAPL', 'BTC-USD', '0700.HK']
        print("Usage: python3 signals.py <symbol>")
        print(f"默认分析: {symbols}")
    else:
        symbols = sys.argv[1:]
    
    for symbol in symbols:
        try:
            analyze_signals(symbol)
        except Exception as e:
            print(f"❌ {symbol} 分析失败: {e}")


if __name__ == "__main__":
    main()
