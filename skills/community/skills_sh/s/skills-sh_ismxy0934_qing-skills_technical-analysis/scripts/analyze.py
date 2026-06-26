#!/usr/bin/env python3
"""
股票技术分析脚本

用法:
    python analyze.py 600519 --date 2025-01-01

输入: output/<code>/<date>/data.json
输出: output/<code>/<date>/analysis.json
"""

import json
import os
import sys
from datetime import datetime
from enum import Enum

import pandas as pd
import numpy as np


# === 交易参数 ===
BIAS_THRESHOLD = 5.0        # 乖离率阈值（%）
VOLUME_SHRINK_RATIO = 0.7   # 缩量判断阈值
VOLUME_HEAVY_RATIO = 1.5    # 放量判断阈值
MA_SUPPORT_TOLERANCE = 0.02  # MA 支撑判断容忍度（2%）

# === MACD 参数 ===
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# === RSI 参数 ===
RSI_SHORT = 6
RSI_MID = 12
RSI_LONG = 24
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30


# === 状态枚举 ===
class TrendStatus(Enum):
    STRONG_BULL = "强势多头"
    BULL = "多头排列"
    WEAK_BULL = "弱势多头"
    CONSOLIDATION = "盘整"
    WEAK_BEAR = "弱势空头"
    BEAR = "空头排列"
    STRONG_BEAR = "强势空头"


class VolumeStatus(Enum):
    HEAVY_VOLUME_UP = "放量上涨"
    HEAVY_VOLUME_DOWN = "放量下跌"
    SHRINK_VOLUME_UP = "缩量上涨"
    SHRINK_VOLUME_DOWN = "缩量回调"
    NORMAL = "量能正常"


class MACDStatus(Enum):
    GOLDEN_CROSS_ZERO = "零轴上金叉"
    GOLDEN_CROSS = "金叉"
    BULLISH = "多头"
    CROSSING_UP = "上穿零轴"
    CROSSING_DOWN = "下穿零轴"
    BEARISH = "空头"
    DEATH_CROSS = "死叉"


class RSIStatus(Enum):
    OVERBOUGHT = "超买"
    STRONG_BUY = "强势"
    NEUTRAL = "中性"
    WEAK = "弱势"
    OVERSOLD = "超卖"


class BuySignal(Enum):
    STRONG_BUY = "强烈买入"
    BUY = "买入"
    HOLD = "持有"
    WAIT = "观望"
    SELL = "卖出"
    STRONG_SELL = "强烈卖出"


# === 指标计算 ===
def calculate_ma(df: pd.DataFrame) -> pd.DataFrame:
    """计算均线"""
    df = df.copy()
    df['MA5'] = df['close'].rolling(window=5).mean()
    df['MA10'] = df['close'].rolling(window=10).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['MA60'] = df['close'].rolling(window=60).mean() if len(df) >= 60 else df['MA20']
    return df


def calculate_macd(df: pd.DataFrame) -> pd.DataFrame:
    """计算 MACD"""
    df = df.copy()
    ema_fast = df['close'].ewm(span=MACD_FAST, adjust=False).mean()
    ema_slow = df['close'].ewm(span=MACD_SLOW, adjust=False).mean()
    df['MACD_DIF'] = ema_fast - ema_slow
    df['MACD_DEA'] = df['MACD_DIF'].ewm(span=MACD_SIGNAL, adjust=False).mean()
    df['MACD_BAR'] = (df['MACD_DIF'] - df['MACD_DEA']) * 2
    return df


def calculate_rsi(df: pd.DataFrame) -> pd.DataFrame:
    """计算 RSI"""
    df = df.copy()
    for period in [RSI_SHORT, RSI_MID, RSI_LONG]:
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        df[f'RSI_{period}'] = rsi.fillna(50)
    return df


# === 趋势分析 ===
def analyze_trend(df: pd.DataFrame) -> dict:
    """分析趋势状态"""
    latest = df.iloc[-1]
    ma5, ma10, ma20 = latest['MA5'], latest['MA10'], latest['MA20']

    if ma5 > ma10 > ma20:
        prev = df.iloc[-5] if len(df) >= 5 else df.iloc[-1]
        prev_spread = (prev['MA5'] - prev['MA20']) / prev['MA20'] * 100 if prev['MA20'] > 0 else 0
        curr_spread = (ma5 - ma20) / ma20 * 100 if ma20 > 0 else 0

        if curr_spread > prev_spread and curr_spread > 5:
            status = TrendStatus.STRONG_BULL
            alignment = "强势多头排列，均线发散上行"
            strength = 90
        else:
            status = TrendStatus.BULL
            alignment = "多头排列 MA5>MA10>MA20"
            strength = 75

    elif ma5 > ma10 and ma10 <= ma20:
        status = TrendStatus.WEAK_BULL
        alignment = "弱势多头，MA5>MA10 但 MA10≤MA20"
        strength = 55

    elif ma5 < ma10 < ma20:
        prev = df.iloc[-5] if len(df) >= 5 else df.iloc[-1]
        prev_spread = (prev['MA20'] - prev['MA5']) / prev['MA5'] * 100 if prev['MA5'] > 0 else 0
        curr_spread = (ma20 - ma5) / ma5 * 100 if ma5 > 0 else 0

        if curr_spread > prev_spread and curr_spread > 5:
            status = TrendStatus.STRONG_BEAR
            alignment = "强势空头排列，均线发散下行"
            strength = 10
        else:
            status = TrendStatus.BEAR
            alignment = "空头排列 MA5<MA10<MA20"
            strength = 25

    elif ma5 < ma10 and ma10 >= ma20:
        status = TrendStatus.WEAK_BEAR
        alignment = "弱势空头，MA5<MA10 但 MA10≥MA20"
        strength = 40

    else:
        status = TrendStatus.CONSOLIDATION
        alignment = "均线缠绕，趋势不明"
        strength = 50

    return {
        'status': status.value,
        'status_code': status.name,
        'ma_alignment': alignment,
        'strength': strength,
        'is_bullish': status in [TrendStatus.STRONG_BULL, TrendStatus.BULL, TrendStatus.WEAK_BULL]
    }


# === 乖离率计算 ===
def calculate_bias(price: float, ma5: float, ma10: float, ma20: float) -> dict:
    """计算乖离率"""
    bias_ma5 = (price - ma5) / ma5 * 100 if ma5 > 0 else 0
    bias_ma10 = (price - ma10) / ma10 * 100 if ma10 > 0 else 0
    bias_ma20 = (price - ma20) / ma20 * 100 if ma20 > 0 else 0

    warning = abs(bias_ma5) > BIAS_THRESHOLD

    if abs(bias_ma5) < 2:
        status = "安全"
    elif abs(bias_ma5) < 5:
        status = "警戒"
    else:
        status = "危险"

    return {
        'ma5': round(bias_ma5, 2),
        'ma10': round(bias_ma10, 2),
        'ma20': round(bias_ma20, 2),
        'warning': bool(warning),
        'status': status
    }


# === MACD 分析 ===
def analyze_macd(df: pd.DataFrame) -> dict:
    """分析 MACD 状态"""
    if len(df) < MACD_SLOW:
        return {'status': 'UNKNOWN', 'status_desc': '数据不足', 'signal': '数据不足'}

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    dif = latest['MACD_DIF']
    dea = latest['MACD_DEA']
    bar = latest['MACD_BAR']

    prev_diff = prev['MACD_DIF'] - prev['MACD_DEA']
    curr_diff = dif - dea

    is_golden_cross = prev_diff <= 0 and curr_diff > 0
    is_death_cross = prev_diff >= 0 and curr_diff < 0
    is_crossing_up = prev['MACD_DIF'] <= 0 and dif > 0
    is_crossing_down = prev['MACD_DIF'] >= 0 and dif < 0

    if is_golden_cross and dif > 0:
        status = MACDStatus.GOLDEN_CROSS_ZERO
        signal = "零轴上金叉，强烈买入信号"
    elif is_crossing_up:
        status = MACDStatus.CROSSING_UP
        signal = "DIF上穿零轴，趋势转强"
    elif is_golden_cross:
        status = MACDStatus.GOLDEN_CROSS
        signal = "金叉，趋势向上"
    elif is_death_cross:
        status = MACDStatus.DEATH_CROSS
        signal = "死叉，趋势向下"
    elif is_crossing_down:
        status = MACDStatus.CROSSING_DOWN
        signal = "DIF下穿零轴，趋势转弱"
    elif dif > 0 and dea > 0:
        status = MACDStatus.BULLISH
        signal = "多头排列，持续上涨"
    elif dif < 0 and dea < 0:
        status = MACDStatus.BEARISH
        signal = "空头排列，持续下跌"
    else:
        status = MACDStatus.BULLISH
        signal = "MACD 中性区域"

    return {
        'dif': round(dif, 4),
        'dea': round(dea, 4),
        'bar': round(bar, 4),
        'status': status.name,
        'status_desc': status.value,
        'signal': signal
    }


# === RSI 分析 ===
def analyze_rsi(df: pd.DataFrame) -> dict:
    """分析 RSI 状态"""
    if len(df) < RSI_LONG:
        return {'status': 'UNKNOWN', 'status_desc': '数据不足', 'signal': '数据不足'}

    latest = df.iloc[-1]
    rsi6 = latest[f'RSI_{RSI_SHORT}']
    rsi12 = latest[f'RSI_{RSI_MID}']
    rsi24 = latest[f'RSI_{RSI_LONG}']

    if rsi12 > RSI_OVERBOUGHT:
        status = RSIStatus.OVERBOUGHT
        signal = f"RSI超买({rsi12:.1f}>70)，短期回调风险高"
    elif rsi12 > 60:
        status = RSIStatus.STRONG_BUY
        signal = f"RSI强势({rsi12:.1f})，多头力量充足"
    elif rsi12 >= 40:
        status = RSIStatus.NEUTRAL
        signal = f"RSI中性({rsi12:.1f})，震荡整理中"
    elif rsi12 >= RSI_OVERSOLD:
        status = RSIStatus.WEAK
        signal = f"RSI弱势({rsi12:.1f})，关注反弹"
    else:
        status = RSIStatus.OVERSOLD
        signal = f"RSI超卖({rsi12:.1f}<30)，反弹机会大"

    return {
        'rsi6': round(rsi6, 1),
        'rsi12': round(rsi12, 1),
        'rsi24': round(rsi24, 1),
        'status': status.name,
        'status_desc': status.value,
        'signal': signal
    }


# === 量能分析 ===
def analyze_volume(df: pd.DataFrame) -> dict:
    """分析量能"""
    if len(df) < 5:
        return {'status': 'UNKNOWN', 'status_desc': '数据不足'}

    latest = df.iloc[-1]
    vol_5d_avg = df['volume'].iloc[-6:-1].mean()
    ratio = latest['volume'] / vol_5d_avg if vol_5d_avg > 0 else 1

    prev_close = df.iloc[-2]['close']
    price_change = (latest['close'] - prev_close) / prev_close * 100

    if ratio >= VOLUME_HEAVY_RATIO:
        if price_change > 0:
            status = VolumeStatus.HEAVY_VOLUME_UP
            trend = "放量上涨，多头力量强劲"
            is_healthy = True
        else:
            status = VolumeStatus.HEAVY_VOLUME_DOWN
            trend = "放量下跌，注意风险"
            is_healthy = False
    elif ratio <= VOLUME_SHRINK_RATIO:
        if price_change > 0:
            status = VolumeStatus.SHRINK_VOLUME_UP
            trend = "缩量上涨，上攻动能不足"
            is_healthy = False
        else:
            status = VolumeStatus.SHRINK_VOLUME_DOWN
            trend = "缩量回调，洗盘特征明显（好）"
            is_healthy = True
    else:
        status = VolumeStatus.NORMAL
        trend = "量能正常"
        is_healthy = True

    return {
        'status': status.name,
        'status_desc': status.value,
        'ratio_5d': round(ratio, 2),
        'trend': trend,
        'is_healthy': is_healthy
    }


# === 支撑压力分析 ===
def analyze_support_resistance(df: pd.DataFrame, price: float, ma5: float, ma10: float, ma20: float) -> dict:
    """分析支撑压力位"""
    support_levels = []
    resistance_levels = []

    support_ma5 = False
    if ma5 > 0:
        ma5_distance = abs(price - ma5) / ma5
        if ma5_distance <= MA_SUPPORT_TOLERANCE and price >= ma5:
            support_ma5 = True
            support_levels.append(round(ma5, 2))

    support_ma10 = False
    if ma10 > 0:
        ma10_distance = abs(price - ma10) / ma10
        if ma10_distance <= MA_SUPPORT_TOLERANCE and price >= ma10:
            support_ma10 = True
            if round(ma10, 2) not in support_levels:
                support_levels.append(round(ma10, 2))

    if ma20 > 0 and price >= ma20:
        if round(ma20, 2) not in support_levels:
            support_levels.append(round(ma20, 2))

    if len(df) >= 20:
        recent_high = df['high'].iloc[-20:].max()
        if recent_high > price:
            resistance_levels.append(round(recent_high, 2))

    return {
        'support_ma5': support_ma5,
        'support_ma10': support_ma10,
        'support_levels': support_levels,
        'resistance_levels': resistance_levels
    }


# === 综合评分 ===
def generate_signal(trend: dict, bias: dict, macd: dict, rsi: dict,
                   volume: dict, support: dict) -> dict:
    """生成买入信号（100分制）"""
    score = 0
    reasons = []
    risks = []

    # 趋势评分（30分）
    trend_scores = {
        'STRONG_BULL': 30, 'BULL': 26, 'WEAK_BULL': 18,
        'CONSOLIDATION': 12, 'WEAK_BEAR': 8, 'BEAR': 4, 'STRONG_BEAR': 0
    }
    score += trend_scores.get(trend['status_code'], 12)

    if trend['status_code'] in ['STRONG_BULL', 'BULL']:
        reasons.append(f"{trend['status']}，顺势做多")
    elif trend['status_code'] in ['BEAR', 'STRONG_BEAR']:
        risks.append(f"{trend['status']}，不宜做多")

    # 乖离率评分（20分）
    bias_val = bias['ma5']
    if bias_val < 0:
        if bias_val > -3:
            score += 20
            reasons.append(f"价格略低于MA5({bias_val:.1f}%)，回踩买点")
        elif bias_val > -5:
            score += 16
            reasons.append(f"价格回踩MA5({bias_val:.1f}%)，观察支撑")
        else:
            score += 8
            risks.append(f"乖离率过大({bias_val:.1f}%)，可能破位")
    elif bias_val < 2:
        score += 18
        reasons.append(f"价格贴近MA5({bias_val:.1f}%)，介入好时机")
    elif bias_val < BIAS_THRESHOLD:
        score += 14
        reasons.append(f"价格略高于MA5({bias_val:.1f}%)，可小仓介入")
    else:
        score += 4
        risks.append(f"乖离率过高({bias_val:.1f}%>5%)，严禁追高")

    # 量能评分（15分）
    volume_scores = {
        'SHRINK_VOLUME_DOWN': 15, 'HEAVY_VOLUME_UP': 12, 'NORMAL': 10,
        'SHRINK_VOLUME_UP': 6, 'HEAVY_VOLUME_DOWN': 0,
    }
    score += volume_scores.get(volume['status'], 8)

    if volume['status'] == 'SHRINK_VOLUME_DOWN':
        reasons.append("缩量回调，主力洗盘")
    elif volume['status'] == 'HEAVY_VOLUME_DOWN':
        risks.append("放量下跌，注意风险")

    # 支撑评分（10分）
    if support['support_ma5']:
        score += 5
        reasons.append("MA5支撑有效")
    if support['support_ma10']:
        score += 5
        reasons.append("MA10支撑有效")

    # MACD 评分（15分）
    macd_scores = {
        'GOLDEN_CROSS_ZERO': 15, 'GOLDEN_CROSS': 12, 'CROSSING_UP': 10,
        'BULLISH': 8, 'BEARISH': 2, 'CROSSING_DOWN': 0, 'DEATH_CROSS': 0,
    }
    score += macd_scores.get(macd['status'], 5)

    if macd['status'] in ['GOLDEN_CROSS_ZERO', 'GOLDEN_CROSS']:
        reasons.append(macd['signal'])
    elif macd['status'] in ['DEATH_CROSS', 'CROSSING_DOWN']:
        risks.append(macd['signal'])

    # RSI 评分（10分）
    rsi_scores = {
        'OVERSOLD': 10, 'STRONG_BUY': 8, 'NEUTRAL': 5, 'WEAK': 3, 'OVERBOUGHT': 0,
    }
    score += rsi_scores.get(rsi['status'], 5)

    if rsi['status'] in ['OVERSOLD', 'STRONG_BUY']:
        reasons.append(rsi['signal'])
    elif rsi['status'] == 'OVERBOUGHT':
        risks.append(rsi['signal'])

    # 综合判断
    if score >= 75 and trend['status_code'] in ['STRONG_BULL', 'BULL']:
        action = BuySignal.STRONG_BUY
    elif score >= 60 and trend['status_code'] in ['STRONG_BULL', 'BULL', 'WEAK_BULL']:
        action = BuySignal.BUY
    elif score >= 45:
        action = BuySignal.HOLD
    elif score >= 30:
        action = BuySignal.WAIT
    elif trend['status_code'] in ['BEAR', 'STRONG_BEAR']:
        action = BuySignal.STRONG_SELL
    else:
        action = BuySignal.SELL

    return {
        'action': action.value,
        'action_code': action.name,
        'score': score,
        'reasons': reasons,
        'risks': risks
    }


# === 主分析函数 ===
def technical_analysis(stock_data: dict) -> dict:
    """主分析函数"""
    klines = stock_data['klines']
    df = pd.DataFrame(klines)

    if len(df) < 20:
        return {'ok': False, 'error': '数据不足，无法进行趋势分析（至少需要 20 根K线）'}

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    # 计算指标
    df = calculate_ma(df)
    df = calculate_macd(df)
    df = calculate_rsi(df)

    # 获取最新数据
    latest = df.iloc[-1]
    price = latest['close']
    ma5 = latest['MA5']
    ma10 = latest['MA10']
    ma20 = latest['MA20']
    ma60 = latest.get('MA60', ma20)

    # 分析各维度
    trend = analyze_trend(df)
    bias = calculate_bias(price, ma5, ma10, ma20)
    macd = analyze_macd(df)
    rsi = analyze_rsi(df)
    volume = analyze_volume(df)
    support = analyze_support_resistance(df, price, ma5, ma10, ma20)

    # 生成信号
    signal = generate_signal(trend, bias, macd, rsi, volume, support)

    return {
        'ok': True,
        'code': stock_data['code'],
        'name': stock_data.get('name', stock_data['code']),
        'market': stock_data.get('market', ''),
        'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'trend': trend,
        'price': {
            'current': round(price, 2),
            'ma5': round(ma5, 2),
            'ma10': round(ma10, 2),
            'ma20': round(ma20, 2),
            'ma60': round(ma60, 2) if not pd.isna(ma60) else round(ma20, 2)
        },
        'bias': bias,
        'macd': macd,
        'rsi': rsi,
        'volume': volume,
        'support_resistance': support,
        'signal': signal,
        # 透传原始数据供下游使用
        'chip': stock_data.get('chip'),
        'realtime': stock_data.get('realtime'),
    }


def get_project_root() -> str:
    """获取项目根目录"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='股票技术分析')
    parser.add_argument('code', help='股票代码')
    parser.add_argument('--date', required=True, help='日期，格式 YYYY-MM-DD')
    args = parser.parse_args()

    root = get_project_root()

    # 读取数据文件
    input_path = os.path.join(root, 'output', args.code, args.date, 'data.json')
    if not os.path.exists(input_path):
        print(f"[错误] 数据文件不存在: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    # 执行分析
    result = technical_analysis(input_data)

    if result.get('ok') is False or result.get('error'):
        print(f"[错误] {result.get('error', '分析失败')}", file=sys.stderr)
        sys.exit(1)

    # 保存结果
    output_dir = os.path.join(root, 'output', args.code, args.date)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'analysis.json')

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[读取] {input_path}", file=sys.stderr)
    print(f"[保存] {output_path}", file=sys.stderr)
    print(json.dumps(result, ensure_ascii=False, indent=2))
