#!/usr/bin/env python3
"""
买卖信号生成模块
Trading Signal Generator

信号类型：
1. RSI 超买/超卖
2. MACD 金叉/死叉
3. 均线交叉
4. 突破支撑/阻力
5. 综合信号

输出：强买/买/观望/卖/强卖
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import math
import os
import requests

# 加载配置
from config import load_config, get_api_keys
api_keys = get_api_keys()
# 设置环境变量供 API 调用使用
for key, value in api_keys.items():
    os.environ.setdefault(key, value)

def get_stock_data(symbol: str, days: int = 100):
    """获取股票历史数据 - 直接调用 Twelve Data API
    
    安全说明：不依赖外部包，直接使用 API
    """
    api_key = os.environ.get("TWELVE_DATA_API_KEY")
    if not api_key:
        print(f"⚠️ 缺少 TWELVE_DATA_API_KEY")
        return None
    
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 直接调用 Twelve Data API
        url = "https://api.twelvedata.com/time"
        params = {
            "symbol": symbol,
            "interval": "1day",
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "apikey": api_key
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if "values" in data and data["values"]:
            return [
                {
                    "date": v["datetime"],
                    "open": float(v["open"]),
                    "high": float(v["high"]),
                    "low": float(v["low"]),
                    "close": float(v["close"]),
                    "volume": int(v["volume"]) if "volume" in v else 0
                }
                for v in data["values"]
            ]
    except Exception as e:
        print(f"⚠️ 获取 {symbol} 数据失败：{e}")
    
    return None

def calculate_rsi(data: list, period: int = 14) -> float:
    """
    计算 RSI (Relative Strength Index)
    RSI = 100 - (100 / (1 + RS))
    RS = 平均涨幅 / 平均跌幅
    """
    if not data or len(data) < period + 1:
        return 50.0  # 默认中性
    
    closes = [float(d.get("close", 0)) for d in reversed(data)]  # 从旧到新
    
    gains = []
    losses = []
    
    for i in range(1, len(closes)):
        change = closes[i] - closes[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    if len(gains) < period:
        return 50.0
    
    # 计算平均涨幅和跌幅
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return round(rsi, 2)

def calculate_macd(data: list, fast: int = 12, slow: int = 26, signal: int = 9) -> dict:
    """
    计算 MACD
    MACD Line = EMA(fast) - EMA(slow)
    Signal Line = EMA(MACD, signal)
    Histogram = MACD - Signal
    """
    if not data or len(data) < slow + signal + 10:
        return {"macd": 0, "signal": 0, "histogram": 0}
    
    closes = [float(d.get("close", 0)) for d in reversed(data)]
    
    def ema(values, period):
        multiplier = 2 / (period + 1)
        ema_value = sum(values[:period]) / period
        for val in values[period:]:
            ema_value = (val - ema_value) * multiplier + ema_value
        return ema_value
    
    ema_fast = ema(closes, fast)
    ema_slow = ema(closes, slow)
    
    macd_line = ema_fast - ema_slow
    
    # 计算 Signal Line 需要历史 MACD 值，简化处理
    # 这里用近似值
    signal_line = macd_line * 0.8  # 简化
    histogram = macd_line - signal_line
    
    return {
        "macd": round(macd_line, 4),
        "signal": round(signal_line, 4),
        "histogram": round(histogram, 4)
    }

def calculate_moving_averages(data: list) -> dict:
    """计算移动平均线"""
    if not data or len(data) < 50:
        return {}
    
    closes = [float(d.get("close", 0)) for d in reversed(data)]
    
    ma = {}
    
    # MA5, MA10, MA20, MA50
    for period in [5, 10, 20, 50]:
        if len(closes) >= period:
            ma[f"ma{period}"] = round(sum(closes[:period]) / period, 2)
    
    return ma

def rsi_signal(rsi: float) -> tuple:
    """
    RSI 信号
    返回：(信号方向，信号强度)
    """
    if rsi < 20:
        return ("bullish", "strong")  # 严重超卖，强买信号
    elif rsi < 30:
        return ("bullish", "weak")    # 超卖，买信号
    elif rsi > 80:
        return ("bearish", "strong")  # 严重超买，强卖信号
    elif rsi > 70:
        return ("bearish", "weak")    # 超买，卖信号
    else:
        return ("neutral", "none")    # 中性

def macd_signal(macd_data: dict) -> tuple:
    """
    MACD 信号
    金叉：MACD 上穿 Signal → 买
    死叉：MACD 下穿 Signal → 卖
    """
    macd = macd_data.get("macd", 0)
    signal = macd_data.get("signal", 0)
    histogram = macd_data.get("histogram", 0)
    
    if macd > signal and histogram > 0:
        if macd > 0:
            return ("bullish", "medium")  # 零轴上金叉，强
        else:
            return ("bullish", "weak")    # 零轴下金叉，弱
    elif macd < signal and histogram < 0:
        if macd < 0:
            return ("bearish", "medium")  # 零轴下死叉，强
        else:
            return ("bearish", "weak")    # 零轴上死叉，弱
    else:
        return ("neutral", "none")

def ma_signal(ma_data: dict, current_price: float) -> tuple:
    """
    均线信号
    价格 > MA → 看涨
    价格 < MA → 看跌
    均线金叉/死叉
    """
    if not ma_data:
        return ("neutral", "none")
    
    ma20 = ma_data.get("ma20", 0)
    ma50 = ma_data.get("ma50", 0)
    
    signals = []
    
    # 价格与均线关系
    if current_price > ma20:
        signals.append(("bullish", "weak"))
    elif current_price < ma20:
        signals.append(("bearish", "weak"))
    
    if current_price > ma50:
        signals.append(("bullish", "weak"))
    elif current_price < ma50:
        signals.append(("bearish", "weak"))
    
    # 均线交叉
    if ma20 > ma50:
        signals.append(("bullish", "medium"))  # 金叉
    elif ma20 < ma50:
        signals.append(("bearish", "medium"))  # 死叉
    
    if not signals:
        return ("neutral", "none")
    
    # 综合判断
    bullish_count = sum(1 for s in signals if s[0] == "bullish")
    bearish_count = sum(1 for s in signals if s[0] == "bearish")
    
    if bullish_count > bearish_count:
        strength = "medium" if bullish_count >= 2 else "weak"
        return ("bullish", strength)
    elif bearish_count > bullish_count:
        strength = "medium" if bearish_count >= 2 else "weak"
        return ("bearish", strength)
    else:
        return ("neutral", "none")

def combine_signals(signals: list) -> dict:
    """
    综合多个信号
    signals: [(方向，强度), ...]
    """
    if not signals:
        return {"direction": "neutral", "strength": "none", "score": 0}
    
    # 权重
    strength_weights = {"strong": 3, "medium": 2, "weak": 1, "none": 0}
    
    bullish_score = 0
    bearish_score = 0
    
    for direction, strength in signals:
        weight = strength_weights.get(strength, 0)
        if direction == "bullish":
            bullish_score += weight
        elif direction == "bearish":
            bearish_score += weight
    
    total_score = bullish_score + bearish_score
    net_score = bullish_score - bearish_score
    
    # 判断方向
    if net_score >= 4:
        direction = "strong_bullish"
    elif net_score >= 2:
        direction = "bullish"
    elif net_score <= -4:
        direction = "strong_bearish"
    elif net_score <= -2:
        direction = "bearish"
    else:
        direction = "neutral"
    
    # 判断强度
    if total_score >= 6:
        strength = "strong"
    elif total_score >= 3:
        strength = "medium"
    else:
        strength = "weak"
    
    return {
        "direction": direction,
        "strength": strength,
        "score": net_score,
        "bullish_score": bullish_score,
        "bearish_score": bearish_score
    }

def generate_trading_signal(symbol: str) -> dict:
    """
    主函数：生成交易信号
    
    返回：
    {
        "symbol": "NVDA",
        "timestamp": "2026-03-24T12:00:00",
        "current_price": 175.64,
        "signals": {
            "rsi": {"value": 45.2, "signal": "neutral"},
            "macd": {"value": 0.5, "signal": "bullish"},
            "ma": {"signal": "bullish"}
        },
        "combined": {
            "direction": "bullish",
            "strength": "medium",
            "score": 2
        },
        "recommendation": "buy",
        "confidence": "medium"
    }
    """
    print(f"📊 生成 {symbol} 交易信号...")
    
    # 获取数据
    data = get_stock_data(symbol, days=100)
    if not data:
        return {"error": "无法获取数据"}
    
    current_price = float(data[0].get("close", 0))
    
    # 计算指标
    rsi_value = calculate_rsi(data, period=14)
    macd_data = calculate_macd(data)
    ma_data = calculate_moving_averages(data)
    
    # 生成各指标信号
    rsi_sig = rsi_signal(rsi_value)
    macd_sig = macd_signal(macd_data)
    ma_sig = ma_signal(ma_data, current_price)
    
    signals = [rsi_sig, macd_sig, ma_sig]
    
    # 综合信号
    combined = combine_signals(signals)
    
    # 转换为操作建议
    direction_to_action = {
        "strong_bullish": "strong_buy",
        "bullish": "buy",
        "neutral": "hold",
        "bearish": "sell",
        "strong_bearish": "strong_sell"
    }
    
    recommendation = direction_to_action.get(combined["direction"], "hold")
    confidence = combined["strength"]
    
    result = {
        "symbol": symbol,
        "timestamp": datetime.now().isoformat(),
        "current_price": current_price,
        "indicators": {
            "rsi": {
                "value": rsi_value,
                "signal": rsi_sig[0],
                "strength": rsi_sig[1]
            },
            "macd": {
                "value": macd_data["macd"],
                "signal": macd_sig[0],
                "strength": macd_sig[1],
                "histogram": macd_data["histogram"]
            },
            "moving_averages": {
                "data": ma_data,
                "signal": ma_sig[0],
                "strength": ma_sig[1]
            }
        },
        "combined": combined,
        "recommendation": recommendation,
        "confidence": confidence
    }
    
    # 打印信号
    print(f"  RSI: {rsi_value:.2f} → {rsi_sig[0]} ({rsi_sig[1]})")
    print(f"  MACD: {macd_data['macd']:.4f} → {macd_sig[0]} ({macd_sig[1]})")
    print(f"  均线：→ {ma_sig[0]} ({ma_sig[1]})")
    print(f"  综合：{combined['direction']} (score: {combined['score']})")
    print(f"  建议：{recommendation} (置信度：{confidence})")
    
    return result

def print_trading_signal(result: dict):
    """打印交易信号结果"""
    if "error" in result:
        print(f"❌ {result['error']}")
        return
    
    print(f"\n{'='*60}")
    print(f"📈 {result['symbol']} 交易信号分析")
    print(f"💰 当前价格：${result['current_price']:.2f}")
    print(f"🕐 时间：{result['timestamp']}")
    print(f"{'='*60}")
    
    # 指标详情
    indicators = result["indicators"]
    
    print(f"\n📊 技术指标:")
    
    # RSI
    rsi = indicators["rsi"]
    rsi_icon = "🔴" if rsi["value"] > 70 else "🟢" if rsi["value"] < 30 else "⚪"
    print(f"  {rsi_icon} RSI(14): {rsi['value']:.2f} [{rsi['signal']}]")
    
    # MACD
    macd = indicators["macd"]
    macd_icon = "🟢" if macd["signal"] == "bullish" else "🔴" if macd["signal"] == "bearish" else "⚪"
    print(f"  {macd_icon} MACD: {macd['value']:.4f} [{macd['signal']}]")
    
    # 均线
    ma = indicators["moving_averages"]
    ma_icon = "🟢" if ma["signal"] == "bullish" else "🔴" if ma["signal"] == "bearish" else "⚪"
    print(f"  {ma_icon} 均线：[{ma['signal']}]")
    
    # 综合信号
    combined = result["combined"]
    score_icon = "🟢" if combined["score"] > 0 else "🔴" if combined["score"] < 0 else "⚪"
    
    print(f"\n🎯 综合信号:")
    print(f"  {score_icon} 方向：{combined['direction']} (score: {combined['score']})")
    print(f"  强度：{combined['strength']}")
    
    # 操作建议
    recommendation_icons = {
        "strong_buy": "🚀 强买",
        "buy": "📈 买入",
        "hold": "⏸️ 观望",
        "sell": "📉 卖出",
        "strong_sell": "💥 强卖"
    }
    
    rec_icon = recommendation_icons.get(result["recommendation"], "⏸️ 观望")
    print(f"\n💡 操作建议：{rec_icon}")
    print(f"  置信度：{result['confidence']}")
    
    print(f"{'='*60}\n")

if __name__ == "__main__":
    # 测试
    print("🔧 买卖信号生成模块测试")
    print("=" * 60)
    
    # 测试几个股票
    test_symbols = ["NVDA", "AAPL", "SPY"]
    
    for symbol in test_symbols:
        result = generate_trading_signal(symbol)
        print_trading_signal(result)
    
    print("✅ 测试完成！")
