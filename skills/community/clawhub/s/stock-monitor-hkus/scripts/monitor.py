#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股/美股/加密货币实时监控 - 增强版
"""

import yfinance as yf
import json
import sys
from datetime import datetime
import numpy as np


# 股票配置
STOCKS = {
    # 港股
    '0700.HK': {'name': '腾讯', 'currency': 'HK$'},
    '9988.HK': {'name': '阿里', 'currency': 'HK$'},
    '3690.HK': {'name': '美团', 'currency': 'HK$'},
    '1810.HK': {'name': '小米', 'currency': 'HK$'},
    '0005.HK': {'name': '汇丰', 'currency': 'HK$'},
    # 美股
    'AAPL': {'name': '苹果', 'currency': '$'},
    'MSFT': {'name': '微软', 'currency': '$'},
    'GOOGL': {'name': '谷歌', 'currency': '$'},
    'TSLA': {'name': '特斯拉', 'currency': '$'},
    'NVDA': {'name': '英伟达', 'currency': '$'},
    # 加密货币
    'BTC-USD': {'name': '比特币', 'currency': '$'},
    'ETH-USD': {'name': '以太坊', 'currency': '$'},
}


def get_stock_data(symbol):
    """获取单只股票数据"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period='5d', interval='5m')
        
        if hist is None or len(hist) == 0:
            hist = ticker.history(period='5d')
        
        if hist is None or len(hist) == 0:
            return None
        
        closes = hist['Close'].values
        highs = hist['High'].values
        lows = hist['Low'].values
        volumes = hist['Volume'].values
        
        latest_price = closes[-1]
        prev_price = closes[-2] if len(closes) > 1 else latest_price
        
        # 均线
        ma5 = closes[-5:].mean() if len(closes) >= 5 else closes.mean()
        ma10 = closes[-10:].mean() if len(closes) >= 10 else closes.mean()
        ma20 = closes[-20:].mean() if len(closes) >= 20 else closes.mean()
        
        # RSI
        rsi = calculate_rsi(closes)
        
        # MACD
        macd = calculate_macd(closes)
        
        return {
            'price': latest_price,
            'change_pct': (latest_price - prev_price) / prev_price * 100,
            'ma5': ma5,
            'ma10': ma10,
            'ma20': ma20,
            'rsi': rsi,
            'macd': macd,
            'high_5d': highs.max(),
            'low_5d': lows.min(),
        }
    except Exception as e:
        return None


def calculate_rsi(closes, period=14):
    """计算RSI"""
    if len(closes) < period + 1:
        return 50
    
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(closes, fast=12, slow=26):
    """简单MACD判断"""
    if len(closes) < slow:
        return 'neutral'
    
    ema_fast = np.convolve(closes, np.ones(fast)/fast, mode='valid')
    ema_slow = np.convolve(closes, np.ones(slow)/slow, mode='valid')
    
    if len(ema_fast) < 2:
        return 'neutral'
    
    # 取最后两个值判断
    if ema_fast[-1] > ema_slow[-1]:
        return 'bullish'  # 多头
    else:
        return 'bearish'  # 空头


def main():
    print(f"📊 港股/美股/币圈监控 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    results = []
    
    for symbol, info in STOCKS.items():
        data = get_stock_data(symbol)
        if data:
            results.append((info['name'], symbol, data, info['currency']))
    
    # 按涨跌排序
    results.sort(key=lambda x: x[2]['change_pct'], reverse=True)
    
    # 输出
    for name, symbol, data, currency in results:
        trend = "📈" if data['change_pct'] > 0 else "📉"
        
        # RSI信号
        if data['rsi'] > 70:
            rsi_signal = "超买"
        elif data['rsi'] < 30:
            rsi_signal = "超卖"
        elif data['rsi'] > 50:
            rsi_signal = "偏多"
        else:
            rsi_signal = "偏空"
        
        # 均线信号
        if data['ma5'] > data['ma10']:
            ma_signal = "多头"
        else:
            ma_signal = "空头"
        
        # MACD信号
        macd_emoji = "🟢" if data['macd'] == 'bullish' else "🔴"
        
        print(f"{trend} {name}({symbol}): {currency}{data['price']:.2f} {data['change_pct']:+.2f}% | RSI:{data['rsi']:.0f} {rsi_signal} {ma_signal} {macd_emoji}")
    
    print(f"\n✅ 更新完成，共 {len(results)} 只")
    
    # 保存状态
    state = {
        'last_update': datetime.now().isoformat(),
        'stocks': {symbol: {'price': data['price'], 'change_pct': data['change_pct'], 'rsi': data['rsi']} 
                  for symbol, info, data, _ in results}
    }
    
    with open('/Users/apple/.openclaw/workspace/memory/stocks_monitor.json', 'w') as f:
        json.dump(state, f, indent=2)


if __name__ == "__main__":
    main()
