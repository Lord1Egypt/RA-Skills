#!/usr/bin/env python3
"""
Crypto Technical Indicator Calculator - OpenClaw Skill Script
Calculates professional-grade technical indicators for cryptocurrency trading analysis.

Supported Indicators:
- SMA (7, 14, 30 periods)
- EMA (12, 26 periods)
- MACD (12/26/9)
- RSI (14 periods)
- Bollinger Bands (20 periods, 2 std)
- ATR (14 periods)
- Price momentum & volatility metrics

SECURITY MANIFEST:
- This script makes GET requests to public cryptocurrency APIs for price data
- No filesystem writes except stdout
- No shell execution
- Requires: requests (pip install requests)

Usage:
    python calc_indicators.py --user USER_ID --coin BTC
    python calc_indicators.py --user USER_ID --coin ETH --days 60
    python calc_indicators.py --coin BTC --test-mode
"""

import requests
import json
import sys
import argparse
import time
import math
from typing import Dict, List, Optional

# ============ Configuration ============

SUPPORTED_COINS = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'DOGE']

BINANCE_API_URL = "https://api.binance.com/api/v3"
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

BINANCE_SYMBOLS = {
    'BTC': 'BTCUSDT', 'ETH': 'ETHUSDT', 'SOL': 'SOLUSDT',
    'BNB': 'BNBUSDT', 'XRP': 'XRPUSDT', 'DOGE': 'DOGEUSDT'
}

COINGECKO_MAPPING = {
    'BTC': 'bitcoin', 'ETH': 'ethereum', 'SOL': 'solana',
    'BNB': 'binancecoin', 'XRP': 'ripple', 'DOGE': 'dogecoin'
}


# ============ Data Fetching ============

def fetch_price_history(coin: str, days: int = 30) -> Optional[List[Dict]]:
    """Fetch OHLCV data from Binance, fallback to CoinGecko"""
    coin = coin.upper()

    # Try Binance first
    try:
        symbol = BINANCE_SYMBOLS.get(coin)
        if symbol:
            interval = '1d' if days > 7 else '1h'
            limit = max(days, 60)  # Get at least 60 data points for indicator accuracy

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
            if candles:
                return candles
    except Exception:
        pass

    # Fallback: CoinGecko
    try:
        coin_id = COINGECKO_MAPPING.get(coin, coin.lower())
        response = requests.get(
            f"{COINGECKO_API_URL}/coins/{coin_id}/ohlc",
            params={'vs_currency': 'usd', 'days': max(days, 60)},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        candles = []
        for item in data:
            candles.append({
                'timestamp': item[0],
                'open': item[1],
                'high': item[2],
                'low': item[3],
                'close': item[4] if len(item) > 4 else item[3],
                'volume': 0
            })
        if candles:
            return candles
    except Exception:
        pass

    return None


# ============ Indicator Calculations ============

def calculate_sma(prices: List[float], period: int) -> float:
    """Simple Moving Average"""
    if len(prices) < period:
        return prices[-1] if prices else 0
    return sum(prices[-period:]) / period


def calculate_ema(prices: List[float], period: int) -> float:
    """Exponential Moving Average"""
    if len(prices) < period:
        return prices[-1] if prices else 0

    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period

    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema

    return ema


def calculate_ema_series(prices: List[float], period: int) -> List[float]:
    """Calculate full EMA series for MACD"""
    if len(prices) < period:
        return prices[:]

    multiplier = 2 / (period + 1)
    ema_values = []

    # Initial EMA = SMA of first N prices
    ema = sum(prices[:period]) / period
    for i in range(period):
        ema_values.append(ema)

    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
        ema_values.append(ema)

    return ema_values


def calculate_std(prices: List[float]) -> float:
    """Standard Deviation"""
    if not prices:
        return 0
    mean = sum(prices) / len(prices)
    variance = sum((p - mean) ** 2 for p in prices) / len(prices)
    return math.sqrt(variance)


def calculate_rsi(prices: List[float], period: int = 14) -> float:
    """Relative Strength Index"""
    if len(prices) < period + 1:
        return 50  # neutral

    changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [c if c > 0 else 0 for c in changes]
    losses = [-c if c < 0 else 0 for c in changes]

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def calculate_macd(prices: List[float]) -> Dict:
    """MACD (12/26/9)"""
    ema_12_series = calculate_ema_series(prices, 12)
    ema_26_series = calculate_ema_series(prices, 26)

    # MACD line = EMA12 - EMA26
    min_len = min(len(ema_12_series), len(ema_26_series))
    macd_line_series = [
        ema_12_series[i] - ema_26_series[i] for i in range(min_len)
    ]

    # Signal line = EMA9 of MACD line
    if len(macd_line_series) >= 9:
        signal_line = calculate_ema(macd_line_series, 9)
    else:
        signal_line = macd_line_series[-1] if macd_line_series else 0

    macd_value = macd_line_series[-1] if macd_line_series else 0
    histogram = macd_value - signal_line

    return {
        'macd_line': round(macd_value, 6),
        'signal_line': round(signal_line, 6),
        'histogram': round(histogram, 6)
    }


def calculate_bollinger_bands(prices: List[float], period: int = 20, num_std: float = 2.0) -> Dict:
    """Bollinger Bands"""
    if len(prices) < period:
        current = prices[-1] if prices else 0
        return {
            'upper': current, 'middle': current, 'lower': current,
            'bandwidth': 0, 'position': 0.5
        }

    sma = sum(prices[-period:]) / period
    std = calculate_std(prices[-period:])

    upper = sma + (num_std * std)
    lower = sma - (num_std * std)
    bandwidth = ((upper - lower) / sma) * 100 if sma > 0 else 0

    current = prices[-1]
    position = (current - lower) / (upper - lower) if (upper - lower) > 0 else 0.5

    return {
        'upper': round(upper, 2),
        'middle': round(sma, 2),
        'lower': round(lower, 2),
        'bandwidth': round(bandwidth, 4),
        'position': round(position, 4)
    }


def calculate_atr(candles: List[Dict], period: int = 14) -> float:
    """Average True Range"""
    if len(candles) < 2:
        return 0

    true_ranges = []
    for i in range(1, len(candles)):
        high = candles[i]['high']
        low = candles[i]['low']
        prev_close = candles[i - 1]['close']

        tr = max(
            high - low,
            abs(high - prev_close),
            abs(low - prev_close)
        )
        true_ranges.append(tr)

    if len(true_ranges) < period:
        return sum(true_ranges) / len(true_ranges) if true_ranges else 0

    return sum(true_ranges[-period:]) / period


# ============ Main Analysis ============

def analyze_coin(coin: str, days: int = 30) -> Dict:
    """Run full technical analysis on a coin"""
    coin = coin.upper()
    if coin not in SUPPORTED_COINS:
        return {"error": f"Unsupported coin: {coin}. Supported: {', '.join(SUPPORTED_COINS)}"}

    # Fetch price data
    candles = fetch_price_history(coin, days)
    if not candles or len(candles) < 14:
        return {"error": f"Insufficient price data for {coin}. Need at least 14 data points."}

    close_prices = [c['close'] for c in candles]
    current_price = close_prices[-1]

    # Calculate all indicators
    sma_7 = calculate_sma(close_prices, 7)
    sma_14 = calculate_sma(close_prices, 14)
    sma_30 = calculate_sma(close_prices, 30)

    ema_12 = calculate_ema(close_prices, 12)
    ema_26 = calculate_ema(close_prices, 26)

    macd = calculate_macd(close_prices)
    rsi = calculate_rsi(close_prices, 14)
    bb = calculate_bollinger_bands(close_prices, 20, 2.0)
    atr = calculate_atr(candles, 14)

    # Price momentum
    if len(close_prices) >= 7:
        momentum_7d = ((current_price - close_prices[-7]) / close_prices[-7]) * 100
    else:
        momentum_7d = 0

    if len(close_prices) >= 30:
        momentum_30d = ((current_price - close_prices[-30]) / close_prices[-30]) * 100
    else:
        momentum_30d = 0

    # Volatility
    volatility = (calculate_std(close_prices[-20:]) / sma_7) * 100 if sma_7 > 0 else 0

    # Support & Resistance (simple: recent low & high)
    recent_prices = close_prices[-20:] if len(close_prices) >= 20 else close_prices
    support = min(recent_prices)
    resistance = max(recent_prices)

    # Signal Generation
    signals = []
    signal_score = 0  # -100 to +100, negative=bearish, positive=bullish

    # RSI signals
    if rsi < 30:
        signals.append("RSI oversold (<30) → Potential BUY")
        signal_score += 25
    elif rsi > 70:
        signals.append("RSI overbought (>70) → Potential SELL")
        signal_score -= 25
    elif rsi < 45:
        signals.append("RSI leaning bearish")
        signal_score -= 10
    elif rsi > 55:
        signals.append("RSI leaning bullish")
        signal_score += 10

    # MACD signals
    if macd['histogram'] > 0 and macd['macd_line'] > macd['signal_line']:
        signals.append("MACD bullish crossover → BUY signal")
        signal_score += 20
    elif macd['histogram'] < 0 and macd['macd_line'] < macd['signal_line']:
        signals.append("MACD bearish crossover → SELL signal")
        signal_score -= 20

    # Bollinger Band signals
    if bb['position'] < 0.1:
        signals.append("Price near lower Bollinger Band → Potential bounce")
        signal_score += 15
    elif bb['position'] > 0.9:
        signals.append("Price near upper Bollinger Band → Potential pullback")
        signal_score -= 15

    # SMA trend
    if current_price > sma_30 and sma_7 > sma_30:
        signals.append("Uptrend: Price & SMA7 above SMA30")
        signal_score += 15
    elif current_price < sma_30 and sma_7 < sma_30:
        signals.append("Downtrend: Price & SMA7 below SMA30")
        signal_score -= 15

    # Overall assessment
    if signal_score > 30:
        overall = "STRONG BUY"
    elif signal_score > 10:
        overall = "BUY"
    elif signal_score > -10:
        overall = "NEUTRAL"
    elif signal_score > -30:
        overall = "SELL"
    else:
        overall = "STRONG SELL"

    return {
        "status": "success",
        "coin": coin,
        "current_price": round(current_price, 2),
        "data_points": len(candles),
        "timestamp": int(time.time()),
        "moving_averages": {
            "sma_7": round(sma_7, 2),
            "sma_14": round(sma_14, 2),
            "sma_30": round(sma_30, 2),
            "ema_12": round(ema_12, 2),
            "ema_26": round(ema_26, 2)
        },
        "macd": macd,
        "rsi_14": round(rsi, 2),
        "bollinger_bands": bb,
        "atr_14": round(atr, 2),
        "momentum": {
            "change_7d_pct": round(momentum_7d, 2),
            "change_30d_pct": round(momentum_30d, 2)
        },
        "volatility_pct": round(volatility, 2),
        "support_resistance": {
            "support": round(support, 2),
            "resistance": round(resistance, 2)
        },
        "signals": signals,
        "signal_score": signal_score,
        "overall_assessment": overall
    }


def main():
    parser = argparse.ArgumentParser(description="Crypto Technical Indicator Calculator")
    parser.add_argument("--coin", required=True, help="Coin symbol (e.g. BTC, ETH, SOL)")
    parser.add_argument("--days", type=int, default=30, help="Days of data for analysis (default: 30)")
    parser.add_argument("--user", type=str, default="", help="User ID for billing")
    parser.add_argument("--test-mode", action="store_true", help="Skip billing for testing")

    args = parser.parse_args()

    # Billing check
    if args.user and not args.test_mode:
        from billing import charge_user
        billing_result = charge_user(args.user)
        if not billing_result["ok"]:
            output = {
                "error": "Payment required",
                "message": billing_result.get("message", "Insufficient balance"),
                "payment_url": billing_result.get("payment_url")
            }
            print(json.dumps(output, indent=2))
            sys.exit(1)

    result = analyze_coin(args.coin, args.days)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
