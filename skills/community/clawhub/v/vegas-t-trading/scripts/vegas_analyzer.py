#!/home/linuxbrew/.linuxbrew/bin/python3.10
# -*- coding: utf-8 -*-
"""
维加斯通道 Pro 做 T 分析工具（v2.0）
基于 EMA12/13/144/169/576/676 均线组合，融合量价共振与多周期分析
数据源：强制使用 AKShare
"""

import sys
import json
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

# 尝试导入 pandas（用于 AKShare）
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("❌ pandas 未安装，请运行：pip3 install pandas -U")


@dataclass
class KlineData:
    """K 线数据"""
    timestamp: float
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class SignalLevel:
    """信号等级定义"""
    name: str
    emoji: str
    stars: int
    description: str


@dataclass
class FibonacciLevels:
    """斐波那契回撤/扩展位"""
    high: float = 0.0
    low: float = 0.0
    diff: float = 0.0
    level_0: float = 0.0      # 0%
    level_236: float = 0.0    # 23.6%
    level_382: float = 0.0    # 38.2%
    level_5: float = 0.0      # 50%
    level_618: float = 0.0    # 61.8% 黄金分割
    level_786: float = 0.0    # 78.6%
    level_1: float = 0.0      # 100%
    level_1382: float = 0.0   # 138.2% 扩展
    level_1618: float = 0.0   # 161.8% 扩展


@dataclass
class ScoreDimensions:
    """评分维度"""
    trend_60m: float = 0.0    # 60 分钟趋势 (30%)
    trend_15m: float = 0.0    # 15 分钟趋势 (20%)
    entry_5m: float = 0.0     # 5 分钟入场 (30%)
    fibonacci: float = 0.0    # 斐波那契共振 (20%)
    total: float = 0.0        # 总分


@dataclass
class VegasSignal:
    """维加斯通道信号（v3.0 多维共振版）"""
    timestamp: float
    price: float
    signal_type: str  # "BUY", "SELL", "HOLD"
    signal_level: str  # "EPIC", "STANDARD", "TRAP", "DUMP"
    confidence: float  # 0-1
    reason: str
    target_buy: Optional[float] = None
    target_sell: Optional[float] = None
    stop_loss: Optional[float] = None
    risk_reward: float = 0.0
    volume_surge: bool = False
    rsi: float = 50.0
    tunnel_width_pct: float = 0.0
    trend_baseline: str = "NEUTRAL"  # "BULLISH", "BEARISH", "NEUTRAL"
    fibonacci: Optional[FibonacciLevels] = None
    score: Optional[ScoreDimensions] = None
    fib_confluence: str = ""  # 斐波那契共振描述


@dataclass
class MultiPeriodResult:
    """多周期共振分析结果"""
    period_60m: Optional[VegasSignal] = None
    period_15m: Optional[VegasSignal] = None
    period_5m: Optional[VegasSignal] = None
    consensus: str = "NONE"  # "STRONG_BUY", "BUY", "HOLD", "SELL", "STRONG_SELL"
    consensus_confidence: float = 0.0
    buy_count: int = 0
    sell_count: int = 0
    hold_count: int = 0


# 信号等级定义
SIGNAL_LEVELS = {
    "EPIC": SignalLevel("史诗级", "⭐", 4, "三重共振 - 强烈建议执行"),
    "STANDARD": SignalLevel("标准", "✅", 3, "隧道支撑/压力 - 可执行"),
    "TRAP": SignalLevel("诱多陷阱", "⚠️", 1, "乖离过大 - 禁止追涨"),
    "DUMP": SignalLevel("强力抛售", "❌", 4, "隧道破位 - 卖出避险"),
}


def calculate_ema(prices: List[float], period: int) -> List[float]:
    """计算 EMA"""
    if len(prices) < period:
        return []
    
    ema = []
    multiplier = 2 / (period + 1)
    
    # 第一个 EMA 用 SMA
    sma = sum(prices[:period]) / period
    ema.append(sma)
    
    # 后续用 EMA 公式
    for i in range(period, len(prices)):
        ema_val = (prices[i] - ema[-1]) * multiplier + ema[-1]
        ema.append(ema_val)
    
    return ema


def calculate_rsi(prices: List[float], period: int = 14) -> float:
    """计算 RSI"""
    if len(prices) < period + 1:
        return 50.0
    
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    if len(gains) < period:
        return 50.0
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_fibonacci(klines: List[KlineData], lookback: int = 100) -> FibonacciLevels:
    """
    计算斐波那契回撤/扩展位
    基于过去 lookback 根 K 线的最高点和最低点
    """
    if len(klines) < 2:
        return FibonacciLevels()
    
    # 获取 lookback 周期内的最高点和最低点
    recent_klines = klines[-lookback:] if len(klines) >= lookback else klines
    high = max(k.high for k in recent_klines)
    low = min(k.low for k in recent_klines)
    diff = high - low
    
    # 计算斐波那契位
    fib = FibonacciLevels(
        high=high,
        low=low,
        diff=diff,
        level_0=high,
        level_236=high - 0.236 * diff,
        level_382=high - 0.382 * diff,
        level_5=high - 0.5 * diff,
        level_618=high - 0.618 * diff,
        level_786=high - 0.786 * diff,
        level_1=low,
        level_1382=low + 0.382 * diff,
        level_1618=low + 0.618 * diff
    )
    
    return fib


def check_fib_confluence(price: float, fib: FibonacciLevels, tunnel_support: float, tunnel_resistance: float) -> tuple:
    """
    检查斐波那契与维加斯通道的共振
    返回 (共振强度 0-1, 共振描述)
    """
    if fib.diff == 0:
        return 0.0, "无斐波那契数据"
    
    tolerance = fib.diff * 0.01  # 1% 容差
    
    confluences = []
    strength = 0.0
    
    # 检查支撑位共振
    fib_levels_support = [
        (fib.level_618, "61.8% 黄金分割"),
        (fib.level_5, "50% 中轴"),
        (fib.level_382, "38.2%"),
        (fib.level_786, "78.6% 深度回撤")
    ]
    
    for level, name in fib_levels_support:
        if abs(price - level) < tolerance:
            confluences.append(f"价格重合斐波那契{name}({level:.2f})")
            if "61.8%" in name:
                strength += 0.4
            elif "50%" in name:
                strength += 0.3
            else:
                strength += 0.2
    
    # 检查与隧道支撑的共振
    if abs(tunnel_support - price) < tolerance * 2:
        for level, name in fib_levels_support:
            if abs(tunnel_support - level) < tolerance * 2:
                confluences.append(f"隧道支撑 ({tunnel_support:.2f}) 与{name}共振")
                strength += 0.3
                break
    
    # 检查扩展位（压力）
    if price > fib.high:
        if abs(price - fib.level_1382) < tolerance:
            confluences.append(f"价格触及 138.2% 扩展位 ({fib.level_1382:.2f})")
            strength += 0.2
        elif abs(price - fib.level_1618) < tolerance:
            confluences.append(f"价格触及 161.8% 扩展位 ({fib.level_1618:.2f})")
            strength += 0.3
    
    strength = min(strength, 1.0)
    description = "; ".join(confluences) if confluences else "无明显共振"
    
    return strength, description


def check_volume_surge(volumes: List[float], multiplier: float = 1.5) -> bool:
    """检测成交量是否有效放大 (当前量 > N 周期均量 * multiplier)"""
    if len(volumes) < 5:
        return False
    
    avg_volume = sum(volumes[-5:]) / 5
    current_volume = volumes[-1]
    
    return current_volume > avg_volume * multiplier


def calculate_risk_reward(current_price: float, support: float, resistance: float) -> float:
    """计算盈亏比，低于 1:2 的交易不建议执行"""
    risk = current_price - support
    reward = resistance - current_price
    
    if risk <= 0:
        return 0.0
    
    return reward / risk


def calculate_multi_dimensional_score(
    tunnel_60m: Optional[Dict],
    tunnel_15m: Optional[Dict],
    tunnel_5m: Optional[Dict],
    fib: FibonacciLevels,
    current_price: float,
    signal_5m: VegasSignal
) -> ScoreDimensions:
    """
    计算多维时空共振评分（总分 100）
    
    维度权重：
    - 60 分钟趋势：30%
    - 15 分钟趋势：20%
    - 5 分钟入场：30%
    - 斐波那契共振：20%
    """
    score = ScoreDimensions()
    
    # 1. 60 分钟趋势评分 (30%)
    if tunnel_60m and tunnel_60m.get('prices'):
        ema144_60 = tunnel_60m['ema144'][-1] if tunnel_60m['ema144'] else 0
        ema169_60 = tunnel_60m['ema169'][-1] if tunnel_60m['ema169'] else 0
        ema576_60 = tunnel_60m['ema576'][-1] if tunnel_60m['ema576'] else 0
        
        # 价格在 EMA144 之上 (+15%)
        if current_price > ema144_60:
            score.trend_60m += 15
        # 隧道斜率向上 (+15%)
        if ema144_60 > ema169_60 > ema576_60 and ema576_60 > 0:
            score.trend_60m += 15
    
    # 2. 15 分钟趋势评分 (20%)
    if tunnel_15m and tunnel_15m.get('prices'):
        ema144_15 = tunnel_15m['ema144'][-1] if tunnel_15m['ema144'] else 0
        ema169_15 = tunnel_15m['ema169'][-1] if tunnel_15m['ema169'] else 0
        
        # 正在回踩隧道 (+20%)
        tunnel_mid_15 = (ema144_15 + ema169_15) / 2 if ema144_15 and ema169_15 else 0
        if tunnel_mid_15 > 0 and abs(current_price - tunnel_mid_15) / tunnel_mid_15 < 0.02:
            score.trend_15m += 20
    
    # 3. 5 分钟入场评分 (30%)
    if tunnel_5m and tunnel_5m.get('prices'):
        ema12_5 = tunnel_5m['ema12'][-1] if tunnel_5m['ema12'] else 0
        ema13_5 = tunnel_5m['ema13'][-1] if tunnel_5m['ema13'] else 0
        ema144_5 = tunnel_5m['ema144'][-1] if tunnel_5m['ema144'] else 0
        ema169_5 = tunnel_5m['ema169'][-1] if tunnel_5m['ema169'] else 0
        
        # EMA12/13 金叉 (+15%)
        if len(tunnel_5m['ema12']) >= 2 and len(tunnel_5m['ema13']) >= 2:
            prev_ema12 = tunnel_5m['ema12'][-2]
            prev_ema13 = tunnel_5m['ema13'][-2]
            if prev_ema12 <= prev_ema13 and ema12_5 > ema13_5:
                score.entry_5m += 15
        
        # 价格站稳 EMA169 (+15%)
        if ema169_5 > 0 and current_price > ema169_5:
            score.entry_5m += 15
    
    # 4. 斐波那契共振评分 (20%)
    tunnel_support = tunnel_5m['ema169'][-1] if tunnel_5m and tunnel_5m.get('ema169') else 0
    tunnel_resistance = tunnel_5m['ema12'][-1] if tunnel_5m and tunnel_5m.get('ema12') else 0
    
    fib_strength, _ = check_fib_confluence(current_price, fib, tunnel_support, tunnel_resistance)
    score.fibonacci = fib_strength * 20  # 转换为 0-20 分
    
    # 计算总分
    score.total = score.trend_60m + score.trend_15m + score.entry_5m + score.fibonacci
    
    return score


def calculate_vegas_tunnel(klines: List[KlineData]) -> Dict:
    """
    计算维加斯通道 Pro
    - 短期通道：EMA12 + EMA13
    - 长期通道：EMA144 + EMA169
    - 趋势基准：EMA576 + EMA676
    """
    closes = [k.close for k in klines]
    volumes = [k.volume for k in klines]
    
    ema12 = calculate_ema(closes, 12)
    ema13 = calculate_ema(closes, 13)
    ema144 = calculate_ema(closes, 144)
    ema169 = calculate_ema(closes, 169)
    ema576 = calculate_ema(closes, 576)
    ema676 = calculate_ema(closes, 676)
    
    # 对齐长度（以最短的为准）
    min_len = min(len(ema12), len(ema13), len(ema144), len(ema169), len(ema576), len(ema676))
    
    if min_len == 0:
        return {
            'ema12': [], 'ema13': [], 'ema144': [], 'ema169': [],
            'ema576': [], 'ema676': [], 'prices': [], 'volumes': []
        }
    
    return {
        'ema12': ema12[-min_len:],
        'ema13': ema13[-min_len:],
        'ema144': ema144[-min_len:],
        'ema169': ema169[-min_len:],
        'ema576': ema576[-min_len:],
        'ema676': ema676[-min_len:],
        'prices': closes[-min_len:],
        'volumes': volumes[-min_len:]
    }


def analyze_t_signal(tunnel: Dict, current_price: float, check_volume: bool = False) -> VegasSignal:
    """
    分析做 T 信号（Pro 版）
    
    维加斯通道交易规则：
    1. 价格上穿短期通道（EMA12/13）→ 买入信号
    2. 价格下穿短期通道 → 卖出信号
    3. 短期通道上穿长期通道 → 强买入
    4. 短期通道下穿长期通道 → 强卖出
    5. 价格回踩长期通道不破 → 买入
    6. 价格反弹长期通道不过 → 卖出
    7. EMA576/676 判断大趋势，防止逆势操作
    """
    ema12 = tunnel['ema12'][-1] if tunnel['ema12'] else 0
    ema13 = tunnel['ema13'][-1] if tunnel['ema13'] else 0
    ema144 = tunnel['ema144'][-1] if tunnel['ema144'] else 0
    ema169 = tunnel['ema169'][-1] if tunnel['ema169'] else 0
    ema576 = tunnel['ema576'][-1] if tunnel['ema576'] else 0
    ema676 = tunnel['ema676'][-1] if tunnel['ema676'] else 0
    
    short_tunnel_mid = (ema12 + ema13) / 2
    long_tunnel_mid = (ema144 + ema169) / 2
    long_tunnel_top = max(ema144, ema169)
    long_tunnel_bottom = min(ema144, ema169)
    baseline_mid = (ema576 + ema676) / 2 if ema576 and ema676 else 0
    
    # 计算通道宽度
    tunnel_width = long_tunnel_top - long_tunnel_bottom
    tunnel_width_pct = (tunnel_width / long_tunnel_mid * 100) if long_tunnel_mid > 0 else 0
    
    # 判断大趋势（基于 EMA576/676）
    if ema576 > ema676 and current_price > baseline_mid:
        trend_baseline = "BULLISH"
    elif ema576 < ema676 and current_price < baseline_mid:
        trend_baseline = "BEARISH"
    else:
        trend_baseline = "NEUTRAL"
    
    # 判断短期趋势
    is_uptrend = ema12 > ema13 > ema144 > ema169
    is_downtrend = ema12 < ema13 < ema144 < ema169
    
    # 计算 RSI
    rsi = calculate_rsi(tunnel['prices']) if tunnel['prices'] else 50.0
    
    # 检测成交量 surge
    volume_surge = False
    if check_volume and tunnel['volumes']:
        volume_surge = check_volume_surge(tunnel['volumes'])
    
    # 计算做 T 区间
    buy_zone_top = long_tunnel_top * 1.005
    buy_zone_bottom = long_tunnel_bottom * 0.995
    sell_zone_bottom = short_tunnel_mid * 1.01
    sell_zone_top = short_tunnel_mid * 1.025
    
    # 计算支撑和阻力
    support = long_tunnel_bottom * 0.99
    resistance = short_tunnel_mid * 1.02
    
    # 计算盈亏比
    risk_reward = calculate_risk_reward(current_price, support, resistance)
    
    # 判断信号
    signal_type = "HOLD"
    signal_level = "STANDARD"
    confidence = 0.5
    reason = ""
    target_buy = None
    target_sell = None
    stop_loss = None
    
    # 通道走平检测 - 震荡市
    if tunnel_width_pct < 0.5:
        signal_type = "HOLD"
        signal_level = "STANDARD"
        confidence = 0.4
        reason = f"通道走平 (宽度{tunnel_width_pct:.2f}%)，震荡市建议观望"
    
    # RSI 超买检测 - 诱多陷阱
    elif rsi > 80:
        signal_type = "HOLD"
        signal_level = "TRAP"
        confidence = 0.3
        reason = f"RSI={rsi:.1f} 严重超买，乖离过大，禁止追涨"
    
    # RSI 超卖检测 - 禁止杀跌
    elif rsi < 20:
        signal_type = "HOLD"
        signal_level = "STANDARD"
        confidence = 0.4
        reason = f"RSI={rsi:.1f} 严重超卖，禁止杀跌，等待反弹"
    
    # 史诗级买入：三重共振
    elif (is_uptrend and trend_baseline == "BULLISH" and 
          buy_zone_bottom <= current_price <= buy_zone_top and volume_surge):
        signal_type = "BUY"
        signal_level = "EPIC"
        confidence = 0.92
        reason = f"⭐ 史诗级三重共振：上升趋势 + 回踩隧道 + 放量"
        target_buy = current_price
        target_sell = resistance
        stop_loss = support
    
    # 强买入：上升趋势 + 回踩长期通道
    elif is_uptrend and trend_baseline == "BULLISH" and buy_zone_bottom <= current_price <= buy_zone_top:
        signal_type = "BUY"
        signal_level = "STANDARD"
        confidence = 0.85
        reason = f"上升趋势中回踩长期通道支撑 ({long_tunnel_bottom:.2f}-{long_tunnel_top:.2f})"
        target_buy = current_price
        target_sell = resistance
        stop_loss = support
    
    # 强卖出：下降趋势 + 价格反弹长期通道
    elif is_downtrend and trend_baseline == "BEARISH" and long_tunnel_bottom <= current_price <= long_tunnel_top:
        signal_type = "SELL"
        signal_level = "STANDARD"
        confidence = 0.85
        reason = f"下降趋势中反弹长期通道压力 ({long_tunnel_bottom:.2f}-{long_tunnel_top:.2f})"
        target_sell = current_price
        target_buy = support
        stop_loss = long_tunnel_top * 1.01
    
    # 强力抛售：隧道破位
    elif current_price < long_tunnel_bottom * 0.98 and volume_surge:
        signal_type = "SELL"
        signal_level = "DUMP"
        confidence = 0.88
        reason = f"❌ 放量跌破隧道下轨，卖出避险"
        target_sell = current_price
        stop_loss = long_tunnel_bottom * 1.01
    
    # 普通买入：价格接近长期通道底部
    elif current_price <= long_tunnel_bottom * 1.01 and trend_baseline != "BEARISH":
        signal_type = "BUY"
        signal_level = "STANDARD"
        confidence = 0.7
        reason = f"价格接近长期通道下轨支撑 ({long_tunnel_bottom:.2f})"
        target_buy = current_price
        target_sell = resistance
        stop_loss = support
    
    # 普通卖出：价格远离长期通道（超买）
    elif current_price >= short_tunnel_mid * 1.03:
        signal_type = "SELL"
        signal_level = "STANDARD"
        confidence = 0.7
        reason = f"价格偏离短期通道过远，可能回调"
        target_sell = current_price
        stop_loss = short_tunnel_mid * 1.01
    
    # 突破买入：价格上穿短期通道
    elif current_price > short_tunnel_mid * 1.005 and current_price < short_tunnel_mid * 1.02:
        signal_type = "BUY"
        signal_level = "STANDARD"
        confidence = 0.65
        reason = f"价格上穿短期通道，动能向上"
        target_buy = current_price
        target_sell = current_price * 1.02
        stop_loss = short_tunnel_mid * 0.99
    
    # 跌破卖出：价格下穿短期通道
    elif current_price < short_tunnel_mid * 0.995:
        signal_type = "SELL"
        signal_level = "STANDARD"
        confidence = 0.65
        reason = f"价格下穿短期通道，动能向下"
        target_sell = current_price
        stop_loss = short_tunnel_mid * 1.01
    
    # 默认持有
    else:
        signal_type = "HOLD"
        signal_level = "STANDARD"
        confidence = 0.5
        reason = f"价格在通道内震荡，等待明确信号"
    
    # 成交量 surge 调整置信度
    if volume_surge and signal_type != "HOLD":
        confidence = min(confidence + 0.05, 0.95)
    
    return VegasSignal(
        timestamp=datetime.now().timestamp(),
        price=current_price,
        signal_type=signal_type,
        signal_level=signal_level,
        confidence=confidence,
        reason=reason,
        target_buy=target_buy,
        target_sell=target_sell,
        stop_loss=stop_loss,
        risk_reward=risk_reward,
        volume_surge=volume_surge,
        rsi=rsi,
        tunnel_width_pct=tunnel_width_pct,
        trend_baseline=trend_baseline
    )


def analyze_with_fibonacci(klines: List[KlineData], tunnel: Dict, current_price: float, 
                           check_volume: bool = False) -> VegasSignal:
    """
    分析做 T 信号（带斐波那契）
    """
    # 基础信号分析
    signal = analyze_t_signal(tunnel, current_price, check_volume)
    
    # 计算斐波那契
    fib = calculate_fibonacci(klines, lookback=100)
    signal.fibonacci = fib
    
    # 检查斐波那契共振
    long_tunnel_bottom = tunnel['ema169'][-1] if tunnel.get('ema169') else 0
    short_tunnel_mid = (tunnel['ema12'][-1] + tunnel['ema13'][-1]) / 2 if tunnel.get('ema12') and tunnel.get('ema13') else 0
    
    fib_strength, fib_desc = check_fib_confluence(current_price, fib, long_tunnel_bottom, short_tunnel_mid)
    signal.fib_confluence = fib_desc
    
    # 斐波那契共振调整置信度
    if fib_strength > 0.5:
        signal.confidence = min(signal.confidence + 0.1, 0.95)
        if "61.8%" in fib_desc:
            signal.signal_level = "EPIC"
            signal.reason = f"⭐ {signal.reason} + 斐波那契 61.8% 黄金共振"
    
    return signal


def analyze_multi_period(symbol: str, market_type: str, exchange: str) -> tuple:
    """
    多周期共振分析 (60-15-5) + 斐波那契 + 评分
    返回 (MultiPeriodResult, tunnel_60m, tunnel_15m, tunnel_5m, klines_5m, fib)
    """
    result = MultiPeriodResult()
    tunnels = {}
    klines_data = {}
    
    periods = ["60", "15", "5"]
    signals = []
    
    for period in periods:
        try:
            if market_type == 'a_stock':
                klines = fetch_a_stock_kline(symbol, period)
            else:
                klines = fetch_crypto_kline(symbol, period, exchange)
            
            if len(klines) >= 169:
                tunnel = calculate_vegas_tunnel(klines)
                current_price = klines[-1].close
                # 使用带斐波那契的分析
                signal = analyze_with_fibonacci(klines, tunnel, current_price, check_volume=True)
                signals.append((period, signal))
                tunnels[period] = tunnel
                klines_data[period] = klines
                
                if period == "60":
                    result.period_60m = signal
                elif period == "15":
                    result.period_15m = signal
                elif period == "5":
                    result.period_5m = signal
        except Exception as e:
            pass  # 跳过无法获取的周期
    
    # 计算共振
    for period, signal in signals:
        if signal.signal_type == "BUY":
            result.buy_count += 1
        elif signal.signal_type == "SELL":
            result.sell_count += 1
        else:
            result.hold_count += 1
    
    # 判断共识
    total = len(signals)
    if total == 0:
        result.consensus = "NONE"
        result.consensus_confidence = 0.0
    elif result.buy_count == 3:
        result.consensus = "STRONG_BUY"
        result.consensus_confidence = 0.95
    elif result.buy_count == 2:
        result.consensus = "BUY"
        result.consensus_confidence = 0.75
    elif result.sell_count == 3:
        result.consensus = "STRONG_SELL"
        result.consensus_confidence = 0.95
    elif result.sell_count == 2:
        result.consensus = "SELL"
        result.consensus_confidence = 0.75
    else:
        result.consensus = "HOLD"
        result.consensus_confidence = 0.5
    
    # 获取 5 分钟数据用于评分
    tunnel_60m = tunnels.get("60")
    tunnel_15m = tunnels.get("15")
    tunnel_5m = tunnels.get("5")
    klines_5m = klines_data.get("5", [])
    
    # 计算斐波那契（基于 5 分钟 K 线）
    fib = calculate_fibonacci(klines_5m, lookback=100) if klines_5m else FibonacciLevels()
    
    # 计算多维评分
    current_price = klines_5m[-1].close if klines_5m else 0
    signal_5m = result.period_5m or VegasSignal(timestamp=0, price=current_price, signal_type="HOLD", 
                                                  signal_level="STANDARD", confidence=0.5, reason="")
    
    score = calculate_multi_dimensional_score(tunnel_60m, tunnel_15m, tunnel_5m, fib, current_price, signal_5m)
    
    return result, tunnel_60m, tunnel_15m, tunnel_5m, klines_5m, fib, score


def fetch_a_stock_kline(symbol: str, period: str = "5", count: int = 1000, max_retries: int = 3) -> List[KlineData]:
    """
    获取 A 股 K 线数据（强制使用 AKShare）
    
    ⚠️ 仅使用 AKShare 数据源，确保数据准确性
    如果 AKShare 失败，不会 fallback 到其他数据源
    
    需要安装：pip install akshare (Python 3.8+)
    """
    period_map = {"5": "5", "15": "15", "60": "60"}
    klt = period_map.get(period, "5")
    
    # 强制仅使用 AKShare，带重试机制
    for attempt in range(1, max_retries + 1):
        try:
            if attempt > 1:
                wait_time = 2 ** (attempt - 1)  # 指数退避：2s, 4s, 8s
                print(f"  ⏳ 等待 {wait_time} 秒后重试 (第 {attempt}/{max_retries} 次)...")
                import time
                time.sleep(wait_time)
            else:
                print(f"  [AKShare] 获取 {period} 分钟 K 线中... (第 {attempt}/{max_retries} 次尝试)")
            
            import akshare as ak
            
            # AKShare 分钟 K 线 API
            df = ak.stock_zh_a_hist_min_em(symbol=symbol, period=klt)
            
            if df is not None and len(df) > 0:
                klines = []
                for _, row in df.iterrows():
                    klines.append(KlineData(
                        timestamp=pd.Timestamp(row['时间']).timestamp(),
                        open=float(row['开盘']),
                        high=float(row['最高']),
                        low=float(row['最低']),
                        close=float(row['收盘']),
                        volume=float(row['成交量']) if '成交量' in row else 0
                    ))
                
                print(f"  ✓ AKShare 成功获取 {len(klines)} 条 {period} 分钟 K 线数据")
                return klines[-count:]  # 返回最近的 count 条
        
        except ImportError:
            print("  ❌ 错误：AKShare 未安装")
            print("  请运行：pip3 install akshare pandas -U")
            raise Exception("AKShare 未安装，无法获取数据")
        
        except Exception as e:
            error_msg = str(e)
            if attempt == max_retries:
                print(f"  ❌ AKShare 所有重试均失败：{error_msg}")
                print("  建议：1) 检查网络连接 2) 稍后再试 3) 检查 AKShare 版本")
                raise Exception(f"AKShare 数据获取失败（已重试 {max_retries} 次）: {error_msg}")
            else:
                print(f"  ⚠️ AKShare 尝试 {attempt}/{max_retries} 失败：{error_msg}")
    
    # 理论上不会到达这里
    raise Exception("AKShare 数据获取失败")


def fetch_crypto_kline(symbol: str, period: str = "5", exchange: str = "binance") -> List[KlineData]:
    """获取加密货币 K 线数据（使用币安 API）"""
    period_map = {"5": "5m", "15": "15m", "60": "1h"}
    interval = period_map.get(period, "5m")
    
    symbol_clean = symbol.replace('/', '').replace('USDT', 'USDT')
    
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol_clean}&interval={interval}&limit=1000"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        klines = []
        for candle in data:
            klines.append(KlineData(
                timestamp=candle[0] / 1000,
                open=float(candle[1]),
                high=float(candle[2]),
                low=float(candle[3]),
                close=float(candle[4]),
                volume=float(candle[5])
            ))
        
        return klines
    except Exception as e:
        raise Exception(f"获取加密货币数据失败：{str(e)}")


def get_signal_emoji(signal_type: str, signal_level: str) -> str:
    """获取信号 emoji"""
    level_emoji = {
        "EPIC": "⭐⭐⭐⭐",
        "STANDARD": "✅",
        "TRAP": "⚠️",
        "DUMP": "❌"
    }
    
    type_emoji = {
        "BUY": "🟢",
        "SELL": "🔴",
        "HOLD": "⚪"
    }
    
    level = level_emoji.get(signal_level, "")
    type_e = type_emoji.get(signal_type, "⚪")
    
    return f"{type_e} {level}"


def format_output_pro(signal: VegasSignal, tunnel: Dict, period: str, symbol: str, 
                      market_type: str, multi_result: Optional[MultiPeriodResult] = None) -> str:
    """格式化输出（Pro 实战版）"""
    
    ema12 = tunnel['ema12'][-1] if tunnel['ema12'] else 0
    ema13 = tunnel['ema13'][-1] if tunnel['ema13'] else 0
    ema144 = tunnel['ema144'][-1] if tunnel['ema144'] else 0
    ema169 = tunnel['ema169'][-1] if tunnel['ema169'] else 0
    ema576 = tunnel['ema576'][-1] if tunnel['ema576'] else 0
    ema676 = tunnel['ema676'][-1] if tunnel['ema676'] else 0
    
    # 信号等级描述
    level_desc = {
        "EPIC": "史诗级 (三重共振)",
        "STANDARD": "标准信号",
        "TRAP": "诱多陷阱",
        "DUMP": "强力抛售"
    }
    
    # 状态描述
    status_desc = {
        ("BUY", "EPIC"): "🟢 强烈建议买入 (回踩确认)",
        ("BUY", "STANDARD"): "🟢 建议买入",
        ("SELL", "DUMP"): "🔴 强烈建议卖出 (破位避险)",
        ("SELL", "STANDARD"): "🔴 建议卖出",
        ("HOLD", "TRAP"): "⚠️ 观望 (超买风险)",
        ("HOLD", "STANDARD"): "⚪ 持有观望",
    }
    
    status_key = (signal.signal_type, signal.signal_level)
    status = status_desc.get(status_key, f"{signal.signal_type} - {level_desc.get(signal.signal_level, '')}")
    
    output = f"""
📈 [{symbol}] 维加斯做 T 报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

当前状态：{status}
信号等级：{get_signal_emoji(signal.signal_type, signal.signal_level)} {level_desc.get(signal.signal_level, '')}

┌──────────────────────────────────────┐
│ 📊 核心指标                           │
├──────────────────────────────────────┤
│ 现价           {signal.price:.2f}   {"处于隧道支撑区" if signal.signal_type == "BUY" else "中性区域"}  │
│ EMA144/169     {ema144:.2f}/{ema169:.2f}  {"强支撑位" if ema144 > ema169 else "压力位"}   │
│ EMA576/676     {ema576:.2f}/{ema676:.2f}  {"趋势向上" if signal.trend_baseline == "BULLISH" else "趋势向下" if signal.trend_baseline == "BEARISH" else "趋势中性"}   │
│ 成交量         {"🟢 放大" if signal.volume_surge else "⚪ 正常"}  {"资金介入" if signal.volume_surge else ""}  │
│ RSI(14)        {signal.rsi:.1f}     {"超买" if signal.rsi > 70 else "超卖" if signal.rsi < 30 else "中性"}       │
└──────────────────────────────────────┘
"""
    
    # 操盘计划
    if signal.signal_type in ["BUY", "SELL"]:
        output += f"""
🎯 操盘计划：
"""
        if signal.target_buy:
            output += f"├ 买入区间：{signal.target_buy:.2f} 附近 (底仓接回)\n"
        if signal.target_sell:
            output += f"├ 第一目标：{signal.target_sell:.2f} (前期高点)\n"
        if signal.stop_loss:
            output += f"├ 止损参考：{signal.stop_loss:.2f} (收盘跌破 15 分钟不收回)\n"
        if signal.risk_reward > 0:
            rr_text = "✅" if signal.risk_reward >= 2.0 else "⚠️"
            output += f"└ 盈亏比：1:{signal.risk_reward:.1f} {rr_text}\n"
    else:
        output += f"""
🎯 操盘计划：
├ 建议：等待明确信号
└ 关注：{ema144:.2f}-{ema169:.2f} 隧道区域
"""
    
    # 多周期共振
    if multi_result:
        p60_type = multi_result.period_60m.signal_type if multi_result.period_60m else "N/A"
        p60_conf = f"{multi_result.period_60m.confidence:.0%}" if multi_result.period_60m else ""
        p15_type = multi_result.period_15m.signal_type if multi_result.period_15m else "N/A"
        p15_conf = f"{multi_result.period_15m.confidence:.0%}" if multi_result.period_15m else ""
        p5_type = multi_result.period_5m.signal_type if multi_result.period_5m else "N/A"
        p5_conf = f"{multi_result.period_5m.confidence:.0%}" if multi_result.period_5m else ""
        consensus_text = multi_result.consensus.replace('_', ' ') if multi_result.consensus else "NONE"
        
        output += f"""
📊 多周期共振 (60-15-5):
├ 60min: {p60_type} {p60_conf}
├ 15min: {p15_type} {p15_conf}
├ 5min:  {p5_type} {p5_conf}
└ 综合：{consensus_text} (置信度:{multi_result.consensus_confidence:.0%})
"""
    
    # 斐波那契共振
    if signal.fibonacci and signal.fibonacci.diff > 0:
        fib = signal.fibonacci
        output += f"""
📐 斐波那契回撤 (100 周期):
├ 高点：{fib.high:.2f} | 低点：{fib.low:.2f}
├ 61.8%: {fib.level_618:.2f} | 50%: {fib.level_5:.2f} | 38.2%: {fib.level_382:.2f}
└ 共振：{signal.fib_confluence}
"""
    
    # 多维评分
    if signal.score and signal.score.total > 0:
        s = signal.score
        score_bar = "█" * int(s.total / 10) + "░" * (10 - int(s.total / 10))
        recommendation = "满仓做 T" if s.total > 80 else "半仓操作" if s.total > 50 else "轻仓/观望"
        output += f"""
📊 多维共振评分：{score_bar} {s.total}/100
├ 60 分钟趋势：{s.trend_60m}/30 | 15 分钟：{s.trend_15m}/20
├ 5 分钟入场：{s.entry_5m}/30 | 斐波那契：{s.fibonacci}/20
└ 建议：{recommendation}
"""
    
    # 老司机私房菜
    if signal.signal_type == "BUY" and signal.signal_level == "EPIC":
        output += """
💡 老司机私房菜：
如果 5 分钟 K 线在隧道附近收出"长下影线"或"早晨之星"，
成功率将提升至 90% 以上。
"""
    elif signal.signal_type == "SELL" and signal.signal_level == "DUMP":
        output += """
💡 老司机私房菜：
放量破位后立即止损，不要幻想反弹。
保住本金，等待下一次机会。
"""
    elif signal.tunnel_width_pct < 0.5:
        output += """
💡 老司机私房菜：
通道走平时容易反复打脸，建议降低仓位或观望。
等待通道重新打开后再操作。
"""
    
    output += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 风险提示：本分析仅供参考，不构成投资建议
"""
    
    return output


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='维加斯通道 Pro 做 T 分析')
    parser.add_argument('--symbol', required=True, help='股票代码 (如 603993) 或 加密货币 (如 BTC/USDT)')
    parser.add_argument('--period', default='5', choices=['5', '15', '60'], help='K 线周期 (分钟)')
    parser.add_argument('--multi', action='store_true', help='启用多周期共振分析 (60-15-5)')
    parser.add_argument('--market', default='auto', choices=['auto', 'a_stock', 'crypto'], help='市场类型')
    parser.add_argument('--exchange', default='binance', help='加密货币交易所')
    parser.add_argument('--volume-check', action='store_true', help='启用成交量 surge 检测')
    parser.add_argument('--format', default='text', choices=['text', 'json'], help='输出格式')
    
    args = parser.parse_args()
    
    try:
        # 判断市场类型
        market_type = args.market
        if market_type == 'auto':
            if '/' in args.symbol:
                market_type = 'crypto'
            else:
                market_type = 'a_stock'
        
        multi_result = None
        tunnel = None
        market_name = ""
        period = args.period
        
        # 多周期分析
        signal = None  # 初始化 signal
        if args.multi:
            multi_data = analyze_multi_period(args.symbol, market_type, args.exchange)
            multi_result = multi_data[0]
            tunnel_60m, tunnel_15m, tunnel_5m, klines_5m, fib, score = multi_data[1:]
            
            if args.format == 'text' and multi_result.consensus != "NONE":
                # 使用 5 分钟信号作为主信号，但显示多周期结果
                if multi_result.period_5m:
                    signal = multi_result.period_5m
                    period = "5/15/60"
                elif multi_result.period_15m:
                    signal = multi_result.period_15m
                    period = "15/60"
                elif multi_result.period_60m:
                    signal = multi_result.period_60m
                    period = "60"
                
                if signal:
                    # 更新信号的斐波那契和评分
                    signal.fibonacci = fib
                    signal.score = score
                    market_name = f"{market_type}"
                else:
                    print("⚠️ 多周期数据不足，降级为单周期分析")
                    args.multi = False
            else:
                if multi_result.consensus == "NONE":
                    print("⚠️ 多周期数据不足，降级为单周期分析")
                    args.multi = False
        
        # 单周期分析（或多周期降级）
        if not args.multi:
            # 获取 K 线数据
            if market_type == 'a_stock':
                klines = fetch_a_stock_kline(args.symbol, args.period)
                market_name = "A 股"
            else:
                klines = fetch_crypto_kline(args.symbol, args.period, args.exchange)
                market_name = "加密货币"
            
            if len(klines) < 676:
                print(f"⚠️ 数据不足 (需要至少 676 根 K 线用于 EMA676，当前{len(klines)}根)")
                print("   将使用可用数据计算，EMA576/676 可能缺失\n")
            
            # 计算维加斯通道
            tunnel = calculate_vegas_tunnel(klines)
            
            # 当前价格
            current_price = klines[-1].close if klines else 0
            
            # 分析信号
            signal = analyze_t_signal(tunnel, current_price, check_volume=args.volume_check)
            period = args.period
        # 多周期模式下，signal 已经在上面设置，tunnel 使用 tunnel_5m
        elif signal:
            tunnel = tunnel_5m if tunnel_5m else {}
            klines = klines_5m if klines_5m else []
        
        # 输出
        if args.format == 'json':
            result = {
                'symbol': args.symbol,
                'market': market_name if not args.multi else f"{market_name} (多周期)",
                'period': period,
                'timestamp': datetime.now().isoformat(),
                'current_price': signal.price,
                'signal': signal.signal_type,
                'signal_level': signal.signal_level,
                'confidence': signal.confidence,
                'reason': signal.reason,
                'target_buy': signal.target_buy,
                'target_sell': signal.target_sell,
                'stop_loss': signal.stop_loss,
                'risk_reward': signal.risk_reward,
                'volume_surge': signal.volume_surge,
                'rsi': signal.rsi,
                'trend_baseline': signal.trend_baseline,
                'tunnel': {
                    'ema12': tunnel['ema12'][-1] if tunnel['ema12'] else None,
                    'ema13': tunnel['ema13'][-1] if tunnel['ema13'] else None,
                    'ema144': tunnel['ema144'][-1] if tunnel['ema144'] else None,
                    'ema169': tunnel['ema169'][-1] if tunnel['ema169'] else None,
                    'ema576': tunnel['ema576'][-1] if tunnel['ema576'] else None,
                    'ema676': tunnel['ema676'][-1] if tunnel['ema676'] else None
                }
            }
            
            if multi_result:
                result['multi_period'] = {
                    'consensus': multi_result.consensus,
                    'confidence': multi_result.consensus_confidence,
                    'buy_count': multi_result.buy_count,
                    'sell_count': multi_result.sell_count,
                    'hold_count': multi_result.hold_count
                }
            
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            output = format_output_pro(signal, tunnel, period, args.symbol, 
                                       market_name if not args.multi else f"{market_name}",
                                       multi_result)
            print(output)
        
    except Exception as e:
        error_result = {
            'error': str(e),
            'symbol': args.symbol,
            'timestamp': datetime.now().isoformat()
        }
        if args.format == 'json':
            print(json.dumps(error_result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 分析失败：{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
