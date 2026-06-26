#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
趋势评分 v2.0 - 更精细的评分机制
核心改进：
1. 信号不再是"有/无"，而是"强/中/弱"三档
2. 加入量价配合维度
3. 加入趋势持续性维度
4. 加入相对强弱维度（vs大盘）
5. 满分仍为100，但更难拿到高分
"""
import numpy as np
import pandas as pd


def calc_score_v2(df):
    """
    趋势评分 v2.0
    
    维度：
    A. MACD动能 (0-25分)
    B. 均线结构 (0-20分)
    C. RSI强度 (0-20分)
    D. 量价配合 (0-20分)  ← 新增
    E. 趋势持续性 (0-15分) ← 新增
    
    总分：100分
    """
    if len(df) < 30:
        return None

    last = df.iloc[-1]
    prev3 = df.iloc[-4:-1]   # 前3天
    prev5 = df.iloc[-6:-1]   # 前5天
    prev10 = df.iloc[-11:-1] # 前10天
    prev20 = df.iloc[-21:-1] # 前20天

    score = 0
    details = {}

    # ─────────────────────────────────────────
    # A. MACD动能 (0-25分)
    # ─────────────────────────────────────────
    macd_score = 0

    # A1. MACD柱线正负 (0-10分)
    hist = last["hist"]
    if hist > 0:
        # 柱线为正，看强度
        hist_max = df["hist"].rolling(20).max().iloc[-1]
        hist_ratio = hist / (hist_max + 1e-9)
        if hist_ratio > 0.7:
            macd_score += 10   # 强势
        elif hist_ratio > 0.3:
            macd_score += 7    # 中等
        else:
            macd_score += 4    # 弱势（刚转正）
    else:
        macd_score += 0

    # A2. MACD柱线趋势（连续增大）(0-10分)
    if len(prev5) >= 3:
        hist_vals = list(prev5["hist"].values) + [hist]
        # 计算连续增大的天数
        consecutive_up = 0
        for i in range(len(hist_vals)-1, 0, -1):
            if hist_vals[i] > hist_vals[i-1]:
                consecutive_up += 1
            else:
                break
        if consecutive_up >= 4:
            macd_score += 10
        elif consecutive_up >= 3:
            macd_score += 7
        elif consecutive_up >= 2:
            macd_score += 4
        elif consecutive_up >= 1:
            macd_score += 2

    # A3. DIF在DEA上方 (0-5分)
    if last["dif"] > last["dea"]:
        macd_score += 5

    details["macd_score"] = min(macd_score, 25)
    score += details["macd_score"]

    # ─────────────────────────────────────────
    # B. 均线结构 (0-20分)
    # ─────────────────────────────────────────
    ma_score = 0
    close = last["close"]
    ma5 = last["ma5"]
    ma10 = last["ma10"]
    ma20 = last["ma20"]

    # B1. 价格与MA20的关系 (0-8分)
    if close > ma20:
        # 在MA20上方，看距离
        dist_pct = (close - ma20) / ma20 * 100
        if 1 <= dist_pct <= 8:
            ma_score += 8   # 刚突破，最佳位置
        elif dist_pct < 1:
            ma_score += 5   # 刚刚突破
        elif dist_pct <= 15:
            ma_score += 4   # 已经涨了一段
        else:
            ma_score += 1   # 涨太多了，追高风险
    else:
        ma_score += 0

    # B2. 均线多头排列 (0-7分)
    if ma5 > ma10 > ma20:
        # 完美多头，看间距
        gap1 = (ma5 - ma10) / ma10 * 100
        gap2 = (ma10 - ma20) / ma20 * 100
        if gap1 > 0.5 and gap2 > 0.5:
            ma_score += 7   # 间距合理，趋势健康
        else:
            ma_score += 4   # 刚形成多头
    elif ma5 > ma10:
        ma_score += 2   # 短期多头
    else:
        ma_score += 0

    # B3. MA5斜率（上升速度）(0-5分)
    if len(prev5) >= 3:
        ma5_vals = prev5["ma5"].dropna().values
        if len(ma5_vals) >= 3:
            slope = np.polyfit(np.arange(len(ma5_vals)), ma5_vals, 1)[0]
            slope_pct = slope / ma5_vals[-1] * 100
            if slope_pct > 0.3:
                ma_score += 5   # 快速上升
            elif slope_pct > 0.1:
                ma_score += 3   # 稳步上升
            elif slope_pct > 0:
                ma_score += 1   # 缓慢上升

    details["ma_score"] = min(ma_score, 20)
    score += details["ma_score"]

    # ─────────────────────────────────────────
    # C. RSI强度 (0-20分)
    # ─────────────────────────────────────────
    rsi_score = 0
    rsi = last["rsi"]

    # C1. RSI绝对值 (0-10分)
    if 55 <= rsi <= 70:
        rsi_score += 10   # 最佳区间：强势但不过热
    elif 50 <= rsi < 55:
        rsi_score += 7    # 刚过50，趋势确认
    elif 70 < rsi <= 80:
        rsi_score += 4    # 偏热，注意回调
    elif rsi > 80:
        rsi_score += 1    # 过热，高风险
    else:
        rsi_score += 0    # <50，弱势

    # C2. RSI趋势（连续上升天数）(0-10分)
    if len(prev10) >= 5:
        rsi_vals = list(prev10["rsi"].values) + [rsi]
        # 计算RSI连续上升天数
        consecutive_up = 0
        for i in range(len(rsi_vals)-1, 0, -1):
            if rsi_vals[i] > rsi_vals[i-1]:
                consecutive_up += 1
            else:
                break
        if consecutive_up >= 5:
            rsi_score += 10
        elif consecutive_up >= 4:
            rsi_score += 8
        elif consecutive_up >= 3:
            rsi_score += 6
        elif consecutive_up >= 2:
            rsi_score += 4
        elif consecutive_up >= 1:
            rsi_score += 2

    details["rsi_score"] = min(rsi_score, 20)
    score += details["rsi_score"]

    # ─────────────────────────────────────────
    # D. 量价配合 (0-20分) ← 新增维度
    # ─────────────────────────────────────────
    vol_score = 0
    vol_ratio = last["vol_ratio"]

    # D1. 量比（当日成交量 vs 5日均量）(0-10分)
    if 1.5 <= vol_ratio <= 3.0:
        vol_score += 10   # 温和放量，最佳
    elif 1.2 <= vol_ratio < 1.5:
        vol_score += 7    # 轻微放量
    elif 1.0 <= vol_ratio < 1.2:
        vol_score += 4    # 平量
    elif vol_ratio > 3.0:
        vol_score += 2    # 过度放量，可能见顶
    else:
        vol_score += 0    # 缩量，弱势

    # D2. 价涨量增（近5天）(0-10分)
    if len(prev5) >= 3:
        price_up_days = 0
        vol_up_days = 0
        price_vol_match = 0

        for i in range(1, len(prev5)):
            price_up = prev5["close"].iloc[i] > prev5["close"].iloc[i-1]
            vol_up = prev5["volume"].iloc[i] > prev5["volume"].iloc[i-1]
            if price_up:
                price_up_days += 1
            if price_up and vol_up:
                price_vol_match += 1  # 价涨量增（健康）
            elif not price_up and not vol_up:
                price_vol_match += 0.5  # 价跌量缩（正常回调）

        match_ratio = price_vol_match / max(price_up_days, 1)
        if match_ratio >= 0.8:
            vol_score += 10
        elif match_ratio >= 0.6:
            vol_score += 7
        elif match_ratio >= 0.4:
            vol_score += 4
        else:
            vol_score += 0

    details["vol_score"] = min(vol_score, 20)
    score += details["vol_score"]

    # ─────────────────────────────────────────
    # E. 趋势持续性 (0-15分) ← 新增维度
    # ─────────────────────────────────────────
    trend_score = 0

    # E1. 近10天涨幅（不能太大也不能太小）(0-8分)
    if len(prev10) >= 5:
        gain_10d = (close / prev10["close"].iloc[0] - 1) * 100
        if 3 <= gain_10d <= 12:
            trend_score += 8   # 稳健上涨
        elif 1 <= gain_10d < 3:
            trend_score += 5   # 缓慢上涨
        elif 12 < gain_10d <= 20:
            trend_score += 3   # 涨幅偏大
        elif gain_10d > 20:
            trend_score += 0   # 涨太多，追高风险
        elif gain_10d > 0:
            trend_score += 2   # 微涨
        else:
            trend_score += 0   # 下跌

    # E2. 布林带位置（不能在上轨附近）(0-7分)
    boll_pos = last["boll_pos"]
    if -0.2 <= boll_pos <= 0.5:
        trend_score += 7   # 布林带中下轨，空间充足
    elif 0.5 < boll_pos <= 0.7:
        trend_score += 5   # 中轨偏上
    elif 0.7 < boll_pos <= 0.9:
        trend_score += 2   # 接近上轨
    elif boll_pos > 0.9:
        trend_score += 0   # 在上轨，回调风险高
    else:
        trend_score += 3   # 在下轨，可能反弹

    details["trend_score"] = min(trend_score, 15)
    score += details["trend_score"]

    # ─────────────────────────────────────────
    # 汇总
    # ─────────────────────────────────────────
    total = min(score, 100)

    details.update({
        "total": total,
        "rsi": round(float(rsi), 1),
        "boll_pos": round(float(boll_pos), 2),
        "vol_ratio": round(float(vol_ratio), 2),
        "macd_hist": round(float(last["hist"]), 4),
        "close": round(float(close), 2),
        "ma20": round(float(ma20), 2),
        # 兼容旧字段
        "score": total,
        "macd_hist_pos": 1 if last["hist"] > 0 else 0,
        "above_ma20": 1 if close > ma20 else 0,
        "rsi_rising": 1 if (len(prev5) > 1 and rsi > prev5["rsi"].iloc[0]) else 0,
        "rsi_above50": 1 if rsi > 50 else 0,
        "price_rising": 1 if (len(prev5) > 1 and np.polyfit(np.arange(len(prev5)), prev5["close"].values, 1)[0] > 0) else 0,
        "ma_bullish": 1 if (ma5 > ma10 > ma20) else 0,
        "macd_hist_rising": 1 if (len(prev5) > 1 and last["hist"] > prev5["hist"].iloc[-1]) else 0,
        "gain_5d": round(float((close / df.iloc[-6]["close"] - 1) * 100), 2) if len(df) >= 6 else 0,
    })

    return details


def score_description(score):
    """评分描述"""
    if score >= 85:
        return "🔥 极强信号"
    elif score >= 70:
        return "🟢 强势信号"
    elif score >= 55:
        return "🟡 中等信号"
    elif score >= 40:
        return "🟠 弱势信号"
    else:
        return "🔴 信号不足"


def score_breakdown(details):
    """评分明细"""
    lines = []
    lines.append(f"  MACD动能:  {details.get('macd_score', 0):>3}/25")
    lines.append(f"  均线结构:  {details.get('ma_score', 0):>3}/20")
    lines.append(f"  RSI强度:   {details.get('rsi_score', 0):>3}/20")
    lines.append(f"  量价配合:  {details.get('vol_score', 0):>3}/20")
    lines.append(f"  趋势持续:  {details.get('trend_score', 0):>3}/15")
    lines.append(f"  ─────────────")
    lines.append(f"  总分:      {details.get('total', 0):>3}/100")
    return "\n".join(lines)


if __name__ == "__main__":
    print("评分 v2.0 模块加载成功")
    print("维度：MACD动能(25) + 均线结构(20) + RSI强度(20) + 量价配合(20) + 趋势持续(15)")
