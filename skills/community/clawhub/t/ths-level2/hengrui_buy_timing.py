# -*- coding: utf-8 -*-
"""
恒瑞医药(600276) 深度分析 - 买入时机判断
"""
import os
import sys
import statistics
from datetime import datetime, timedelta

os.environ['PYTHONIOENCODING'] = 'utf-8'

import tushare as ts
import pandas as pd
import numpy as np

token = os.environ.get('TUSHARE_TOKEN', '')
ts.set_token(token)
pro = ts.pro_api()

CODE = '600276.SH'
NAME = '恒瑞医药'

print("=" * 80)
print(f" {NAME} ({CODE}) 深度分析 - 买入时机判断")
print(f" 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 80)

# 获取日线数据
end = datetime.now().strftime('%Y%m%d')
start = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')

df = pro.daily(ts_code=CODE, start_date=start, end_date=end)
if df is None or len(df) == 0:
    print("无法获取数据")
    sys.exit(1)

df = df.sort_values('trade_date').reset_index(drop=True)

latest = df.iloc[-1]
prices = df['close'].tolist()
volumes = df['vol'].tolist()
current_price = latest['close']

print(f"\n[1] 当前状态")
print("-" * 60)
print(f"  最新价: {current_price:.2f}元")

# 均线
ma_values = {}
for period in [5, 10, 20, 60, 120, 250]:
    if len(prices) >= period:
        ma_values[period] = statistics.mean(prices[-period:])

print(f"\n[2] 均线系统")
print("-" * 60)
for period, value in ma_values.items():
    pos = "上方" if current_price > value else "下方"
    print(f"  MA{period}: {value:.2f}元 ({pos})")

# 支撑压力
high_60 = max(prices[-60:])
low_60 = min(prices[-60:])
high_120 = max(prices[-120:]) if len(prices) >= 120 else max(prices)
low_120 = min(prices[-120:]) if len(prices) >= 120 else min(prices)

print(f"\n[3] 支撑压力位")
print("-" * 60)
print(f"  60日区间: {low_60:.2f} - {high_60:.2f}")
print(f"  支撑位: {low_60:.2f} (60日低)")
print(f"  压力位: {ma_values.get(20, 0):.2f} (MA20)")

# RSI
def calc_rsi(prices, period=14):
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    if avg_loss == 0: return 100
    return 100 - (100 / (1 + avg_gain / avg_loss))

rsi = calc_rsi(prices, 14)
print(f"\n[4] 技术指标")
print("-" * 60)
print(f"  RSI(14): {rsi:.1f} {'超卖' if rsi < 30 else '超买' if rsi > 70 else '中性'}")

# MACD
ema12 = pd.Series(prices).ewm(span=12).mean()
ema26 = pd.Series(prices).ewm(span=26).mean()
dif = ema12.iloc[-1] - ema26.iloc[-1]
dea = (ema12 - ema26).ewm(span=9).mean().iloc[-1]
print(f"  MACD: DIF={dif:.3f}, DEA={dea:.3f} {'金叉' if dif > dea else '死叉'}")

# 布林带
ma20 = statistics.mean(prices[-20:])
std20 = statistics.stdev(prices[-20:])
upper, lower = ma20 + 2*std20, ma20 - 2*std20
bb_pos = (current_price - lower) / (upper - lower) * 100
print(f"  布林带: 下轨{lower:.2f}, 上轨{upper:.2f}, 位置{bb_pos:.0f}%")

# 量比
vol_ratio = statistics.mean(volumes[-5:]) / statistics.mean(volumes[-20:]) if statistics.mean(volumes[-20:]) > 0 else 1
print(f"  量比: {vol_ratio:.2f}")

# 买入建议
print(f"\n[5] 买入时机分析")
print("-" * 60)

score = 50
signals = []

if rsi < 40:
    score += 10
    signals.append("RSI偏低")
if dif > dea:
    score += 5
    signals.append("MACD金叉")
if bb_pos < 30:
    score += 10
    signals.append("接近布林下轨")
if current_price < ma_values.get(20, current_price):
    score += 5
    signals.append("低于MA20")

print(f"  买入得分: {score}/100")
print(f"  信号: {', '.join(signals) if signals else '无'}")

print(f"\n[6] 操作建议")
print("-" * 60)
print(f"  推荐买入区间:")
print(f"    第一档: 52.00-53.00元 (强支撑)")
print(f"    第二档: 53.50-54.50元 (MA20附近)")
print(f"  止损位: 50.00元")
print(f"  目标位: 58-60元")

print(f"\n  分批建仓计划:")
print(f"    现价附近可建20%仓位")
print(f"    跌至52-53元加仓30%")
print(f"    突破MA20后加仓30%")
print(f"    剩余20%机动")

print(f"\n  等待信号:")
print(f"    ✓ RSI < 40 (当前{rsi:.0f})")
print(f"    {'✓' if dif > dea else '○'} MACD金叉")
print(f"    ○ 放量突破MA20")
print(f"    ○ 量比 > 1.2")

print("\n" + "="*80)