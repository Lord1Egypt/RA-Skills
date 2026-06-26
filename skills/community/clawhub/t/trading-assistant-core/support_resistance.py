#!/usr/bin/env python3
"""
支撑/阻力位计算模块
Support and Resistance Level Calculator

算法：
1. 前高/前低法 - 最近 N 天的最高/最低点
2. 均线法 - 20/50/200 日均线
3. 斐波那契回撤 - 38.2%, 50%, 61.8%
4. 整数关口 - 心理价位
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

def get_stock_data(symbol: str, days: int = 60):
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
            # 转换为标准格式
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

def calculate_pivot_points(data: list) -> dict:
    """
    计算枢轴点（经典方法）
    Pivot = (High + Low + Close) / 3
    R1 = 2*Pivot - Low
    S1 = 2*Pivot - High
    R2 = Pivot + (High - Low)
    S2 = Pivot - (High - Low)
    """
    if not data or len(data) < 1:
        return {}
    
    latest = data[0]
    high = float(latest.get("high", 0))
    low = float(latest.get("low", 0))
    close = float(latest.get("close", 0))
    
    pivot = (high + low + close) / 3
    
    return {
        "pivot": round(pivot, 2),
        "r1": round(2 * pivot - low, 2),
        "s1": round(2 * pivot - high, 2),
        "r2": round(pivot + (high - low), 2),
        "s2": round(pivot - (high - low), 2),
        "r3": round(high + 2 * (pivot - low), 2),
        "s3": round(low - 2 * (high - pivot), 2)
    }

def calculate_previous_highs_lows(data: list, lookback: int = 20) -> dict:
    """
    计算前期高点和低点
    """
    if not data or len(data) < lookback:
        return {"high": None, "low": None}
    
    highs = [float(d.get("high", 0)) for d in data[:lookback]]
    lows = [float(d.get("low", 0)) for d in data[:lookback]]
    
    return {
        "high": round(max(highs), 2),
        "low": round(min(lows), 2)
    }

def calculate_fibonacci_retracement(data: list) -> dict:
    """
    计算斐波那契回撤位
    先找到区间（最高点到最低点），然后计算回撤位
    """
    if not data or len(data) < 20:
        return {}
    
    # 找到最近的高点和低点
    highs = [float(d.get("high", 0)) for d in data[:30]]
    lows = [float(d.get("low", 0)) for d in data[:30]]
    
    swing_high = max(highs)
    swing_low = min(lows)
    diff = swing_high - swing_low
    
    # 斐波那契比例
    fib_levels = {
        "0.0": swing_high,
        "0.236": swing_high - 0.236 * diff,
        "0.382": swing_high - 0.382 * diff,
        "0.5": swing_high - 0.5 * diff,
        "0.618": swing_high - 0.618 * diff,
        "0.786": swing_high - 0.786 * diff,
        "1.0": swing_low
    }
    
    return {k: round(v, 2) for k, v in fib_levels.items()}

def calculate_moving_averages(data: list) -> dict:
    """
    计算移动平均线（作为动态支撑/阻力）
    """
    if not data or len(data) < 200:
        # 数据不足，只计算可用的
        min_len = min(len(data), 50) if data else 0
        if min_len < 20:
            return {}
    
    closes = [float(d.get("close", 0)) for d in reversed(data)]  # 从旧到新
    
    ma = {}
    
    # MA20
    if len(closes) >= 20:
        ma["ma20"] = round(sum(closes[:20]) / 20, 2)
    
    # MA50
    if len(closes) >= 50:
        ma["ma50"] = round(sum(closes[:50]) / 50, 2)
    
    # MA200
    if len(closes) >= 200:
        ma["ma200"] = round(sum(closes[:200]) / 200, 2)
    
    return ma

def calculate_psychological_levels(current_price: float) -> list:
    """
    计算心理价位（整数关口）
    """
    levels = []
    
    # 找到合适的精度
    if current_price >= 100:
        step = 5  # $100 以上，每$5
    elif current_price >= 10:
        step = 1  # $10-100，每$1
    else:
        step = 0.1  # $10 以下，每$0.1
    
    # 找到附近的整数关口
    base = math.floor(current_price / step) * step
    
    for i in range(-3, 4):
        level = base + i * step
        if level > 0:
            levels.append(round(level, 2))
    
    return levels

def determine_strength(current_price: float, level: float, method: str) -> str:
    """
    判断支撑/阻力位强度
    """
    diff_pct = abs(level - current_price) / current_price * 100
    
    # 距离越近越强
    if diff_pct < 1:
        distance_strength = "strong"
    elif diff_pct < 3:
        distance_strength = "medium"
    else:
        distance_strength = "weak"
    
    # 方法权重
    method_weights = {
        "previous_high": 1.0,
        "previous_low": 1.0,
        "ma200": 1.0,
        "ma50": 0.8,
        "ma20": 0.6,
        "fib_0.618": 1.0,
        "fib_0.5": 0.8,
        "fib_0.382": 0.6,
        "pivot": 0.7,
        "psychological": 0.5
    }
    
    weight = method_weights.get(method, 0.5)
    
    # 综合判断
    if distance_strength == "strong" and weight >= 0.8:
        return "strong"
    elif distance_strength == "weak" or weight < 0.6:
        return "weak"
    else:
        return "medium"

def calculate_support_resistance(symbol: str, days: int = 60) -> dict:
    """
    主函数：计算支撑位和阻力位
    
    返回：
    {
        "symbol": "NVDA",
        "current_price": 172.70,
        "timestamp": "2026-03-24T12:00:00",
        "resistance_levels": [
            {"price": 180.0, "strength": "strong", "type": "previous_high"},
            ...
        ],
        "support_levels": [
            {"price": 165.0, "strength": "strong", "type": "previous_low"},
            ...
        ]
    }
    """
    print(f"📊 计算 {symbol} 支撑/阻力位...")
    
    # 获取数据
    data = get_stock_data(symbol, days)
    if not data:
        return {"error": "无法获取数据"}
    
    current_price = float(data[0].get("close", 0))
    
    # 计算各种指标
    pivots = calculate_pivot_points(data)
    prev_levels = calculate_previous_highs_lows(data)
    fib_levels = calculate_fibonacci_retracement(data)
    ma_levels = calculate_moving_averages(data)
    psych_levels = calculate_psychological_levels(current_price)
    
    # 收集阻力位（高于当前价）
    resistance_levels = []
    
    if prev_levels.get("high") and prev_levels["high"] > current_price:
        resistance_levels.append({
            "price": prev_levels["high"],
            "strength": determine_strength(current_price, prev_levels["high"], "previous_high"),
            "type": "previous_high"
        })
    
    for key, value in fib_levels.items():
        if value > current_price:
            resistance_levels.append({
                "price": value,
                "strength": determine_strength(current_price, value, f"fib_{key}"),
                "type": f"fibonacci_{key}"
            })
    
    for ma_name, ma_value in ma_levels.items():
        if ma_value > current_price:
            resistance_levels.append({
                "price": ma_value,
                "strength": determine_strength(current_price, ma_value, ma_name),
                "type": ma_name
            })
    
    for level in psych_levels:
        if level > current_price:
            resistance_levels.append({
                "price": level,
                "strength": determine_strength(current_price, level, "psychological"),
                "type": "psychological"
            })
    
    if pivots.get("r1") and pivots["r1"] > current_price:
        resistance_levels.append({
            "price": pivots["r1"],
            "strength": determine_strength(current_price, pivots["r1"], "pivot"),
            "type": "pivot_r1"
        })
    
    # 收集支撑位（低于当前价）
    support_levels = []
    
    if prev_levels.get("low") and prev_levels["low"] < current_price:
        support_levels.append({
            "price": prev_levels["low"],
            "strength": determine_strength(current_price, prev_levels["low"], "previous_low"),
            "type": "previous_low"
        })
    
    for key, value in fib_levels.items():
        if value < current_price:
            support_levels.append({
                "price": value,
                "strength": determine_strength(current_price, value, f"fib_{key}"),
                "type": f"fibonacci_{key}"
            })
    
    for ma_name, ma_value in ma_levels.items():
        if ma_value < current_price:
            support_levels.append({
                "price": ma_value,
                "strength": determine_strength(current_price, ma_value, ma_name),
                "type": ma_name
            })
    
    for level in psych_levels:
        if level < current_price:
            support_levels.append({
                "price": level,
                "strength": determine_strength(current_price, level, "psychological"),
                "type": "psychological"
            })
    
    if pivots.get("s1") and pivots["s1"] < current_price:
        support_levels.append({
            "price": pivots["s1"],
            "strength": determine_strength(current_price, pivots["s1"], "pivot"),
            "type": "pivot_s1"
        })
    
    # 排序：阻力位从低到高，支撑位从高到低
    resistance_levels.sort(key=lambda x: x["price"])
    support_levels.sort(key=lambda x: x["price"], reverse=True)
    
    # 只保留最强的 3 个阻力位和 3 个支撑位
    resistance_levels = resistance_levels[:5]
    support_levels = support_levels[:5]
    
    result = {
        "symbol": symbol,
        "current_price": current_price,
        "timestamp": datetime.now().isoformat(),
        "resistance_levels": resistance_levels,
        "support_levels": support_levels,
        "pivot_points": pivots,
        "fibonacci": fib_levels,
        "moving_averages": ma_levels
    }
    
    print(f"  ✅ 找到 {len(support_levels)} 个支撑位，{len(resistance_levels)} 个阻力位")
    
    return result

def print_support_resistance(result: dict):
    """打印支撑/阻力位结果"""
    if "error" in result:
        print(f"❌ {result['error']}")
        return
    
    print(f"\n{'='*60}")
    print(f"📈 {result['symbol']} 支撑/阻力位分析")
    print(f"💰 当前价格：${result['current_price']:.2f}")
    print(f"🕐 时间：{result['timestamp']}")
    print(f"{'='*60}")
    
    print(f"\n🔴 阻力位 (从高到低):")
    for i, level in enumerate(result["resistance_levels"], 1):
        strength_icon = {"strong": "🔴", "medium": "🟠", "weak": "🟡"}.get(level["strength"], "⚪")
        diff_pct = (level["price"] - result["current_price"]) / result["current_price"] * 100
        print(f"  {i}. {strength_icon} ${level['price']:.2f} ({level['type']}) [+{diff_pct:.1f}%] [{level['strength']}]")
    
    print(f"\n🟢 支撑位 (从高到低):")
    for i, level in enumerate(result["support_levels"], 1):
        strength_icon = {"strong": "🟢", "medium": "🟡", "weak": "⚪"}.get(level["strength"], "⚪")
        diff_pct = (level["price"] - result["current_price"]) / result["current_price"] * 100
        print(f"  {i}. {strength_icon} ${level['price']:.2f} ({level['type']}) [{diff_pct:.1f}%] [{level['strength']}]")
    
    if result.get("pivot_points"):
        print(f"\n📍 枢轴点:")
        pivots = result["pivot_points"]
        print(f"  Pivot: ${pivots.get('pivot', 0):.2f}")
        print(f"  R1: ${pivots.get('r1', 0):.2f}, R2: ${pivots.get('r2', 0):.2f}")
        print(f"  S1: ${pivots.get('s1', 0):.2f}, S2: ${pivots.get('s2', 0):.2f}")
    
    print(f"{'='*60}\n")

if __name__ == "__main__":
    # 测试
    print("🔧 支撑/阻力位计算模块测试")
    print("=" * 60)
    
    # 测试几个股票
    test_symbols = ["NVDA", "AAPL", "SPY"]
    
    for symbol in test_symbols:
        result = calculate_support_resistance(symbol)
        print_support_resistance(result)
    
    print("✅ 测试完成！")
