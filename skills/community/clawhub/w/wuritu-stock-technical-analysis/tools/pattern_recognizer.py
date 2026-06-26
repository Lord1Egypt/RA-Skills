#!/usr/bin/env python3
"""
K线形态识别器
识别30+经典K线形态，输出形态名称、多空含义、可靠度
"""

import json
import pandas as pd
import numpy as np

try:
    import talib
    HAS_TALIB = True
except ImportError:
    HAS_TALIB = False


# TA-Lib 形态函数映射表
PATTERNS = {
    # ---------- 反转形态（看涨） ----------
    "CDLHAMMER":          {"name": "锤子线",       "type": "看涨反转", "reliability": "中"},
    "CDLINVERTEDHAMMER":  {"name": "倒锤线",       "type": "看涨反转", "reliability": "低"},
    "CDLMORNINGSTAR":     {"name": "早晨之星",     "type": "看涨反转", "reliability": "高"},
    "CDLMORNINGDOJISTAR": {"name": "早晨十字星",   "type": "看涨反转", "reliability": "高"},
    "CDLPIERCING":        {"name": "刺穿形态",     "type": "看涨反转", "reliability": "中"},
    "CDLENGULFING":       {"name": "吞没形态",     "type": "双向",     "reliability": "高"},
    "CDL3WHITESOLDIERS":  {"name": "三白兵",       "type": "看涨反转", "reliability": "高"},
    "CDLHARAMI":          {"name": "孕线形态",     "type": "双向",     "reliability": "中"},

    # ---------- 反转形态（看跌） ----------
    "CDLHANGINGMAN":      {"name": "上吊线",       "type": "看跌反转", "reliability": "中"},
    "CDLSHOOTINGSTAR":    {"name": "射击之星",     "type": "看跌反转", "reliability": "中"},
    "CDLEVENINGSTAR":     {"name": "黄昏之星",     "type": "看跌反转", "reliability": "高"},
    "CDLEVENINGDOJISTAR": {"name": "黄昏十字星",   "type": "看跌反转", "reliability": "高"},
    "CDLDARKCLOUDCOVER":  {"name": "乌云盖顶",     "type": "看跌反转", "reliability": "高"},
    "CDL3BLACKCROWS":     {"name": "三只乌鸦",     "type": "看跌反转", "reliability": "高"},
    "CDLABANDONEDBABY":   {"name": "弃婴形态",     "type": "双向",     "reliability": "高"},

    # ---------- 持续形态 ----------
    "CDL3LINESTRIKE":     {"name": "三线打击",     "type": "持续",     "reliability": "中"},
    "CDLSEPARATINGLINES": {"name": "分离线",       "type": "持续",     "reliability": "低"},
    "CDLMARUBOZU":        {"name": "光头光脚",     "type": "趋势确认", "reliability": "中"},

    # ---------- 中性/特殊形态 ----------
    "CDLDOJI":            {"name": "十字星",       "type": "变盘信号", "reliability": "中"},
    "CDLLONGLEGGEDDOJI":  {"name": "长脚十字星",   "type": "变盘信号", "reliability": "中"},
    "CDLDRAGONFLYDOJI":   {"name": "蜻蜓十字星",   "type": "看涨反转", "reliability": "中"},
    "CDLGRAVESTONEDOJI":  {"name": "墓碑十字星",   "type": "看跌反转", "reliability": "中"},
    "CDLSPINNINGTOP":     {"name": "纺锤线",       "type": "犹豫",     "reliability": "低"},
}


def recognize_patterns(df: pd.DataFrame) -> list[dict]:
    """
    扫描最近K线，识别所有匹配的形态
    返回: [{"pattern": "锤子线", "type": "看涨反转", "reliability": "中", "date": "...", "signal": 100/-100}]
    """
    if not HAS_TALIB:
        return [{"error": "TA-Lib未安装，无法进行形态识别"}]

    detected = []
    o, h, l, c = df["open"], df["high"], df["low"], df["close"]

    for func_name, info in PATTERNS.items():
        func = getattr(talib, func_name, None)
        if func is None:
            continue
        result = func(o, h, l, c)

        # 检查最近5根K线是否有信号
        for offset in range(-5, 0):
            if abs(result.iloc[offset]) > 0:
                signal_value = int(result.iloc[offset])
                direction = "看涨" if signal_value > 0 else "看跌"

                if info["type"] == "双向":
                    pattern_type = f"{info['type']}（本次{direction}）"
                else:
                    pattern_type = info["type"]

                detected.append({
                    "pattern": info["name"],
                    "type": pattern_type,
                    "reliability": info["reliability"],
                    "signal_strength": signal_value,
                    "direction": direction,
                    "date": str(df["date"].iloc[offset]),
                    "position": f"倒数第{abs(offset)}根K线",
                })

    # 按信号强度排序
    detected.sort(key=lambda x: abs(x["signal_strength"]), reverse=True)
    return detected


def detect_support_resistance(df: pd.DataFrame, window=20) -> dict:
    """
    识别关键支撑位和阻力位
    基于：前期高低点、密集成交区、整数关口
    """
    close = df["close"]
    high = df["high"]
    low = df["low"]
    volume = df["volume"]
    current_price = close.iloc[-1]

    # 方法1: 前期高低点
    recent_highs = []
    recent_lows = []
    for i in range(window, len(df) - window):
        if high.iloc[i] == high.iloc[i-window:i+window+1].max():
            recent_highs.append(round(high.iloc[i], 2))
        if low.iloc[i] == low.iloc[i-window:i+window+1].min():
            recent_lows.append(round(low.iloc[i], 2))

    # 方法2: 密集成交区（成交量加权价格聚类）
    vwap_bins = pd.cut(close, bins=20)
    vol_profile = df.groupby(vwap_bins, observed=False)["volume"].sum()
    high_vol_ranges = vol_profile.nlargest(3)

    # 方法3: 整数关口
    base = round(current_price, -1 if current_price > 100 else 0)
    round_levels = [base - 10, base, base + 10]

    # 汇总支撑/阻力
    supports = sorted(set(
        [p for p in recent_lows if p < current_price][-3:]
    ), reverse=True)

    resistances = sorted(set(
        [p for p in recent_highs if p > current_price][:3]
    ))

    return {
        "current_price": round(current_price, 2),
        "supports": supports,
        "resistances": resistances,
        "round_levels": round_levels,
        "high_volume_zones": [str(r) for r in high_vol_ranges.index.tolist()],
    }