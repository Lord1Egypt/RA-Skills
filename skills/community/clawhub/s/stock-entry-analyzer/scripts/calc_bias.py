#!/usr/bin/env python3
"""
乖离率 (BIAS) 计算器

基于刘晨明方法（减法版）：
均线偏离度 = ln(收盘价) - ln(20 日 EMA)

买入区间：5% - 15% (0.05 - 0.15)
"""

import argparse
import json
import math
import sys
from datetime import datetime

def calculate_ema(prices, period):
    """计算指数移动平均 (EMA)"""
    if len(prices) < period:
        return None
    
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period  # 初始 SMA
    
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    
    return ema

def calculate_bias(close_price, ema):
    """
    计算乖离率
    
    公式：ln(close) - ln(ema)  【减法版 - 刘晨明原文】
    
    返回：乖离率（小数形式，如 0.05 表示 5%）
    """
    if ema is None or ema <= 0 or close_price <= 0:
        return None
    
    bias = math.log(close_price) - math.log(ema)
    return bias  # 返回小数形式

def evaluate_bias(bias):
    """评估乖离率信号
    
    阈值（刘晨明原文）：
    - 入场：5%-15% (0.05-0.15) 适中，>15% 偏高
    - 离场：-5%-0% 坚守，<-5% 离场
    """
    if bias is None:
        return "❌ 数据不足", "neutral"
    
    # 转换为百分比便于比较
    bias_pct = bias * 100
    
    if 5.0 <= bias_pct <= 15.0:
        return "✅ 最佳买入区间", "buy"
    elif bias_pct > 15.0:
        return "⚠️ 偏高，警惕回调", "overbought"
    elif bias_pct > 15.0:
        return "🟡 接近买入区间", "watch"
    elif 0 < bias_pct < 5.0:
        return "🟡 偏离度不足", "weak"
    elif -5.0 <= bias_pct <= 0:
        return "🟡 跌穿均线，建议坚守", "hold"
    else:  # bias_pct < -5.0
        return "❌ 大幅跌穿，建议离场", "bearish"

def main():
    parser = argparse.ArgumentParser(description='计算股票乖离率 (BIAS)')
    parser.add_argument('--symbol', type=str, required=True, help='股票代码')
    parser.add_argument('--close', type=float, required=False, help='当前收盘价')
    parser.add_argument('--ema20', type=float, required=False, help='20 日 EMA 值')
    parser.add_argument('--period', type=int, default=20, help='EMA 周期 (默认 20)')
    parser.add_argument('--prices', type=str, required=False, help='历史价格列表 (逗号分隔)')
    parser.add_argument('--output', type=str, choices=['text', 'json'], default='text', help='输出格式')
    
    args = parser.parse_args()
    
    # 计算 EMA
    ema = args.ema20
    if args.prices and not ema:
        prices = [float(p) for p in args.prices.split(',')]
        ema = calculate_ema(prices, args.period)
    
    # 需要收盘价和 EMA
    if not args.close or not ema:
        print("错误：需要提供 --close 和 --ema20，或 --close 和 --prices", file=sys.stderr)
        sys.exit(1)
    
    # 计算乖离率
    bias = calculate_bias(args.close, ema)
    signal, status = evaluate_bias(bias)
    
    # 输出结果
    if args.output == 'json':
        result = {
            "symbol": args.symbol,
            "close": args.close,
            "ema20": ema,
            "bias": round(bias, 3) if bias else None,
            "signal": signal,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"📊 {args.symbol} 乖离率分析")
        print(f"=" * 40)
        print(f"收盘价：  ¥{args.close:.2f}")
        print(f"20 日 EMA: ¥{ema:.2f}")
        print(f"乖离率：  {bias*100:+.3f}%" if bias else "乖离率：  N/A")
        print(f"信  号：  {signal}")
        print(f"=" * 40)
        
        if status == "buy":
            print("✅ 处于最佳买入区间 (5%-15%)")
        elif status == "overbought":
            print("⚠️ 乖离率过高，警惕回调风险 (>15%)")
        elif status == "bearish":
            print("❌ 大幅跌穿均线，建议离场 (<-5%)")

if __name__ == '__main__':
    main()
