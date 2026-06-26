#!/usr/bin/env python3
"""
Crypto Market Analysis Script - Auto Crypto Trader
Fetches OHLCV data from Binance and runs full technical analysis (SMA, EMA, MACD, RSI, BB)

SECURITY MANIFEST:
- Makes public API requests to Binance
- No filesystem writes
- No shell execution
"""

import requests
import json
import sys
import argparse
import time
import math

# Configuration
BINANCE_API_URL = "https://api.binance.com/api/v3"

def fetch_klines(symbol: str, interval: str = '1h', limit: int = 100):
    """Fetch OHLCV data from Binance"""
    try:
        response = requests.get(
            f"{BINANCE_API_URL}/klines",
            params={'symbol': symbol, 'interval': interval, 'limit': limit},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        candles = []
        for kline in data:
            candles.append({
                'timestamp': kline[0],
                'open': float(kline[1]),
                'high': float(kline[2]),
                'low': float(kline[3]),
                'close': float(kline[4]),
                'volume': float(kline[5])
            })
        return candles
    except Exception as e:
        return {"error": str(e)}

def _calculate_sma(prices, period):
    if len(prices) < period: return prices[-1] if prices else 0
    return sum(prices[-period:]) / period

def _calculate_ema(prices, period):
    if len(prices) < period: return prices[-1] if prices else 0
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    return ema

def _calculate_rsi(prices, period=14):
    if len(prices) < period + 1: return 50
    changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [c if c > 0 else 0 for c in changes]
    losses = [-c if c < 0 else 0 for c in changes]
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0: return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def _calculate_std(prices):
    if not prices: return 0
    mean = sum(prices) / len(prices)
    variance = sum((p - mean) ** 2 for p in prices) / len(prices)
    return math.sqrt(variance)

def analyze_market(symbol: str, interval: str = '1h') -> dict:
    """Run full technical analysis on a Binance symbol"""
    symbol = symbol.upper()
    candles = fetch_klines(symbol, interval, 100)
    
    if isinstance(candles, dict) and "error" in candles:
        return {"error": f"Failed to fetch market data: {candles['error']}"}
        
    prices = [c['close'] for c in candles]
    current_price = prices[-1]
    
    try:
        sma_7 = _calculate_sma(prices, 7)
        sma_25 = _calculate_sma(prices, 25)
        ema_12 = _calculate_ema(prices, 12)
        ema_26 = _calculate_ema(prices, 26)
        rsi_14 = _calculate_rsi(prices, 14)
        
        # MACD (approximation)
        macd_line = ema_12 - ema_26
        
        # Bollinger Bands
        bb_sma_20 = _calculate_sma(prices, 20)
        bb_std_20 = _calculate_std(prices[-20:])
        bb_upper = bb_sma_20 + (2 * bb_std_20)
        bb_lower = bb_sma_20 - (2 * bb_std_20)
        
        # Determine signals
        signal_score = 0
        signals = []
        
        if rsi_14 < 30:
            signal_score += 20
            signals.append("RSI Oversold (<30) -> BUY")
        elif rsi_14 > 70:
            signal_score -= 20
            signals.append("RSI Overbought (>70) -> SELL")
            
        if current_price > sma_25 and sma_7 > sma_25:
            signal_score += 15
            signals.append("Uptrend (Price & SMA7 > SMA25) -> BUY")
        elif current_price < sma_25 and sma_7 < sma_25:
            signal_score -= 15
            signals.append("Downtrend (Price & SMA7 < SMA25) -> SELL")
            
        position = (current_price - bb_lower) / (bb_upper - bb_lower) if (bb_upper - bb_lower) > 0 else 0.5
        if position < 0.1:
            signal_score += 10
            signals.append("Near lower Bollinger Band -> BUY")
        elif position > 0.9:
            signal_score -= 10
            signals.append("Near upper Bollinger Band -> SELL")
            
        if signal_score >= 20: decision = "BUY"
        elif signal_score <= -20: decision = "SELL"
        else: decision = "HOLD"
        
        return {
            "status": "success",
            "symbol": symbol,
            "interval": interval,
            "current_price": current_price,
            "indicators": {
                "sma_7": round(sma_7, 4),
                "sma_25": round(sma_25, 4),
                "rsi_14": round(rsi_14, 2),
                "macd_line": round(macd_line, 4),
                "bb_upper": round(bb_upper, 4),
                "bb_lower": round(bb_lower, 4)
            },
            "analysis": {
                "signals": signals,
                "score": signal_score,
                "action": decision
            }
        }
        
    except Exception as e:
        return {"error": f"Error calculating indicators: {str(e)}"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Market analysis")
    parser.add_argument("--symbol", required=True, help="e.g., BTCUSDT")
    parser.add_argument("--interval", default="1h", help="e.g., 15m, 1h, 1d")
    parser.add_argument("--user", required=True, help="User ID for billing")
    parser.add_argument("--test-mode", action="store_true")
    
    args = parser.parse_args()
    
    if not args.test_mode:
        from billing import charge_user
        bill = charge_user(args.user)
        if not bill["ok"]:
            print(json.dumps({"error": "Payment required", "payment_url": bill.get("payment_url")}, indent=2))
            sys.exit(1)
            
    print(json.dumps(analyze_market(args.symbol, args.interval), indent=2))
