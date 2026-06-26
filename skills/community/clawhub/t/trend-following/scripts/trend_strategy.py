#!/usr/bin/env python3
"""
Trend-Following Strategy: Price + Volume Analysis
Generates buy/sell signals, support/resistance, and target prices.
"""

import yfinance as yf
import numpy as np
from datetime import datetime


def find_swing_points(high, low, window=10):
    """Find swing highs and lows."""
    swings_high = []
    swings_low = []
    for i in range(window, len(high) - window):
        if high.iloc[i] == max(high.iloc[i-window:i+window+1]):
            swings_high.append((i, high.iloc[i]))
        if low.iloc[i] == min(low.iloc[i-window:i+window+1]):
            swings_low.append((i, low.iloc[i]))
    return swings_high, swings_low


def find_nearest_levels(price, levels, direction, count=3):
    """Find nearest levels above (direction='above') or below (direction='below')."""
    if direction == 'above':
        candidates = [l for l in levels if l > price]
        candidates.sort()
    else:
        candidates = [l for l in levels if l < price]
        candidates.sort(reverse=True)
    return candidates[:count]


def analyze_trend(ticker_symbol, period="1y"):
    """Comprehensive trend analysis with volume + price signals."""

    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period=period)

    if hist.empty or len(hist) < 60:
        print(f"❌ Insufficient data for {ticker_symbol}")
        return

    close = hist['Close']
    high = hist['High']
    low = hist['Low']
    volume = hist['Volume']
    open_price = hist['Open']

    # === TREND INDICATORS ===

    # Moving averages
    ma20 = close.rolling(20).mean()
    ma50 = close.rolling(50).mean()
    ma200 = close.rolling(200).mean()

    # EMA
    ema12 = close.ewm(12).mean()
    ema26 = close.ewm(26).mean()

    # MACD
    macd = ema12 - ema26
    signal = macd.ewm(9).mean()
    macd_hist = macd - signal

    # RSI (14)
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # Bollinger Bands
    bb_mid = close.rolling(20).mean()
    bb_std = close.rolling(20).std()
    bb_upper = bb_mid + 2 * bb_std
    bb_lower = bb_mid - 2 * bb_std

    # Volume
    vol_ma20 = volume.rolling(20).mean()
    vol_spike = volume / vol_ma20

    # === CURRENT VALUES ===
    curr_price = close.iloc[-1]
    curr_rsi = rsi.iloc[-1]
    curr_macd = macd.iloc[-1]
    curr_signal = signal.iloc[-1]
    curr_macd_hist = macd_hist.iloc[-1]
    curr_vol_spike = vol_spike.iloc[-1]

    # === SWING POINTS FOR S/R ===
    swings_high, swings_low = find_swing_points(high, low, window=10)

    # Get all swing levels
    all_highs = [h for _, h in swings_high]
    all_lows = [l for _, l in swings_low]

    # Find nearest resistance (above) and support (below)
    resistance_levels = find_nearest_levels(curr_price, all_highs, 'above', count=5)
    support_levels = find_nearest_levels(curr_price, all_lows, 'below', count=5)

    resistance = resistance_levels[0] if resistance_levels else curr_price * 1.05
    support = support_levels[0] if support_levels else curr_price * 0.95

    # Pivot extremes
    pivot_high = high.max()
    pivot_low = low.min()

    # === BOTTOM DETECTION ===
    oversold = curr_rsi < 35
    near_bb_lower = curr_price <= bb_lower.iloc[-1]
    price_near_lows = curr_price <= pivot_low * 1.10

    possible_bottom = (oversold and near_bb_lower) or (oversold and price_near_lows)

    # === TREND ===
    uptrend = ma20.iloc[-1] > ma50.iloc[-1]
    strong_uptrend = uptrend and ma50.iloc[-1] > ma200.iloc[-1] if not np.isnan(ma200.iloc[-1]) else False

    # === BUY SIGNALS ===
    buy_signals = []

    # MACD bullish crossover
    if len(macd_hist) >= 2 and macd_hist.iloc[-1] > 0 and macd_hist.iloc[-2] <= 0:
        buy_signals.append("MACD golden cross (histogram crossed above 0)")

    # Volume + price confirmation
    if curr_vol_spike > 1.5 and curr_price > ma20.iloc[-1]:
        buy_signals.append(f"Volume surge ({curr_vol_spike:.1f}x avg) + price above MA20")

    # RSI healthy bounce
    if 40 <= curr_rsi <= 60 and curr_price > ma20.iloc[-1] and uptrend:
        buy_signals.append("RSI in healthy zone + uptrend confirmation")

    # Strong trend pullback entry
    if strong_uptrend and curr_price < ma20.iloc[-1] and curr_price > ma50.iloc[-1]:
        buy_signals.append("Pullback to MA20 in strong uptrend 🎯")

    # Bottom bounce
    if possible_bottom and curr_macd_hist > 0:
        buy_signals.append("⚠️ BOTTOM SIGNAL: RSI oversold + MACD bullish + near pivot low")

    # === SELL SIGNALS ===
    sell_signals = []

    if curr_rsi > 70:
        sell_signals.append("RSI overbought (>70)")
    elif curr_rsi > 65:
        sell_signals.append("RSI elevated (>65) - caution")

    if not uptrend and curr_price < ma20.iloc[-1]:
        sell_signals.append("Price below MA20 in downtrend")

    if curr_vol_spike > 2.0 and curr_price < close.iloc[-2]:
        sell_signals.append(f"High volume ({curr_vol_spike:.1f}x) on price decline")

    if curr_macd_hist < 0 and curr_macd < curr_signal:
        sell_signals.append("MACD bearish (below signal line)")

    if curr_price < support and possible_bottom == False:
        sell_signals.append("Breaking support level")

    # === TARGETS ===
    risk = resistance - curr_price
    reward = curr_price - support

    if reward > 0:
        rr1 = 1.0
        rr2 = 1.5
        rr3 = 2.0
    else:
        rr1, rr2, rr3 = 0.5, 1.0, 1.5

    stop_loss = support - reward * 0.3  # 30% buffer below support
    target1 = curr_price + risk * rr1
    target2 = curr_price + risk * rr2
    target3 = curr_price + risk * rr3

    risk_reward = (target3 - curr_price) / max(curr_price - stop_loss, 0.01)

    # === PRINT ===
    print("=" * 62)
    print(f"📊 {ticker_symbol.upper()} TREND ANALYSIS")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M')} | Period: {period}")
    print("=" * 62)

    print(f"\n💰 Current Price:  ${curr_price:.2f}")
    print(f"📈 RSI(14):        {curr_rsi:.1f}  {'🔴 OVERBOUGHT' if curr_rsi > 70 else '🟡 ELEVATED' if curr_rsi > 60 else '🟢 HEALTHY' if curr_rsi > 35 else '🟠 OVERSOLD'}")
    print(f"📊 MACD:           {curr_macd:.2f} | Signal: {curr_signal:.2f} | Hist: {curr_macd_hist:.2f}")
    print(f"📉 Volume vs Avg:  {curr_vol_spike:.1f}x")
    print(f"💵 BB Lower:       ${bb_lower.iloc[-1]:.2f} | BB Upper: ${bb_upper.iloc[-1]:.2f}")

    print(f"\n{'━' * 50}")
    print("📐 TREND STATUS")
    print(f"{'━' * 50}")
    print(f"   MA20:  ${ma20.iloc[-1]:.2f}  {'▲' if close.iloc[-1] > ma20.iloc[-1] else '▼'}")
    print(f"   MA50:  ${ma50.iloc[-1]:.2f}  {'▲' if close.iloc[-1] > ma50.iloc[-1] else '▼'}")
    if not np.isnan(ma200.iloc[-1]):
        print(f"   MA200: ${ma200.iloc[-1]:.2f} {'▲' if close.iloc[-1] > ma200.iloc[-1] else '▼'}")
    print(f"   Trend: {'🟢 STRONG UPTREND' if strong_uptrend else '🟡 UPTREND' if uptrend else '🔴 DOWNTREND'}")

    print(f"\n{'━' * 50}")
    print("🎯 KEY LEVELS")
    print(f"{'━' * 50}")
    print(f"   🔴 Resistance 1: ${resistance:.2f} (+{((resistance/curr_price)-1)*100:.1f}%)")
    if len(resistance_levels) > 1:
        print(f"   🔴 Resistance 2: ${resistance_levels[1]:.2f}")
    print(f"   💰 Current:       ${curr_price:.2f}")
    print(f"   🟢 Support 1:    ${support:.2f} (-{((curr_price-support)/curr_price)*100:.1f}%)")
    if len(support_levels) > 1:
        print(f"   🟢 Support 2:    ${support_levels[1]:.2f}")
    print(f"   📍 52wk Low:     ${pivot_low:.2f}  |  52wk High: ${pivot_high:.2f}")

    if possible_bottom:
        print(f"\n   ⚠️  【可能底部】RSI:{curr_rsi:.1f} | Near BB Lower:{near_bb_lower} | Near Pivot Low:{price_near_lows}")

    print(f"\n{'━' * 50}")
    print("📋 SIGNALS")
    print(f"{'━' * 50}")

    if buy_signals:
        print("\n   🟢 BUY SIGNALS:")
        for s in buy_signals:
            print(f"      ✅ {s}")
    else:
        print("\n   🟡 No buy signals currently")

    if sell_signals:
        print("\n   🔴 SELL SIGNALS:")
        for s in sell_signals:
            print(f"      ❌ {s}")
    else:
        print("\n   🟡 No strong sell signals")

    print(f"\n{'━' * 50}")
    print("🎯 ENTRY & TARGETS")
    print(f"{'━' * 50}")
    print(f"   Entry:           ${curr_price:.2f}")
    print(f"   Stop Loss:        ${stop_loss:.2f} (-{abs(((stop_loss/curr_price)-1)*100):.1f}%)")
    print(f"   Target 1 ({rr1:.1f}R):   ${target1:.2f} (+{((target1/curr_price)-1)*100:.1f}%)")
    print(f"   Target 2 ({rr2:.1f}R):   ${target2:.2f} (+{((target2/curr_price)-1)*100:.1f}%)")
    print(f"   Target 3 ({rr3:.1f}R):   ${target3:.2f} (+{((target3/curr_price)-1)*100:.1f}%)")
    print(f"   Risk/Reward:      1:{risk_reward:.1f}")

    print("\n" + "=" * 62)

    return {
        "price": curr_price,
        "rsi": curr_rsi,
        "trend": "strong_up" if strong_uptrend else "up" if uptrend else "down",
        "support": support,
        "resistance": resistance,
        "buy_signals": buy_signals,
        "sell_signals": sell_signals,
        "stop_loss": stop_loss,
        "targets": [target1, target2, target3],
        "possible_bottom": possible_bottom
    }


if __name__ == "__main__":
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else "ADBE"
    period = sys.argv[2] if len(sys.argv) > 2 else "1y"
    analyze_trend(ticker, period)
