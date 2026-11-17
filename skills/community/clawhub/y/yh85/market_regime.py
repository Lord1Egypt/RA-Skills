#!/usr/bin/env python3
"""
萤火 YH6.1 行情分型引擎
三指标 → 五类行情 → 策略/仓位/SLTP 自适应

指标: ADX(14) + ATR百分位 + EMA453方向
输出: TREND_STEADY | TREND_VOL | WEAK_TREND | CHOPPY | SQUEEZE
"""

import numpy as np
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
import time

# ─── 行情类型枚举 ───
@dataclass
class Regime:
    TREND_STEADY = "TREND_STEADY"   # 强趋势+低波动 🔥 最理想
    TREND_VOL    = "TREND_VOL"      # 强趋势+高波动 ⚡ 注意震出
    WEAK_TREND   = "WEAK_TREND"     # 弱趋势 方向模糊
    CHOPPY       = "CHOPPY"         # 震荡+高波 🚫 暂停
    SQUEEZE      = "SQUEEZE"        # 震荡+低波 🥱 等待突破

# ─── 各行情策略适配参数 ───
REGIME_ADAPT = {
    Regime.TREND_STEADY: {
        "ema_enabled": True,        # EMA交叉策略
        "lstm_enabled": False,
        "position_ratio": 1.0,      # 仓位系数
        "sl_multiplier": 1.0,       # SL乘数 (1.0=正常)
        "tp_multiplier": 1.0,       # TP乘数
        "cooldown_minutes": 15,     # 冷却期
        "max_signals_per_hour": 3,  # 每小时信号上限
        "description": "强趋势+低波动 — 最理想行情，标准参数",
    },
    Regime.TREND_VOL: {
        "ema_enabled": True,
        "lstm_enabled": False,
        "position_ratio": 0.7,      # 降仓30%
        "sl_multiplier": 1.3,       # SL放宽30% 防震出
        "tp_multiplier": 1.2,       # TP放宽20% 给利润空间
        "cooldown_minutes": 10,
        "max_signals_per_hour": 2,
        "description": "强趋势+高波动 — 顺势但防震出",
    },
    Regime.WEAK_TREND: {
        "ema_enabled": True,
        "lstm_enabled": False,
        "position_ratio": 0.5,
        "sl_multiplier": 0.7,       # SL收紧 快进快出
        "tp_multiplier": 0.7,
        "cooldown_minutes": 30,
        "max_signals_per_hour": 1,
        "description": "弱趋势 — 仅EMA短打，收紧止损",
    },
    Regime.CHOPPY: {
        "ema_enabled": False,
        "lstm_enabled": False,
        "position_ratio": 0.0,      # 不开仓
        "sl_multiplier": 0,
        "tp_multiplier": 0,
        "cooldown_minutes": 60,
        "max_signals_per_hour": 0,
        "description": "震荡+高波 — 杀猪行情，暂停",
    },
    Regime.SQUEEZE: {
        "ema_enabled": False,
        "lstm_enabled": False,
        "position_ratio": 0.3,      # 仅允许极轻仓试探
        "sl_multiplier": 0.6,
        "tp_multiplier": 0.6,
        "cooldown_minutes": 60,
        "max_signals_per_hour": 1,
        "description": "震荡+低波 — 暴风雨前宁静，轻仓试探",
    },
}


def pd_ema(arr: np.ndarray, span: int) -> np.ndarray:
    """EMA 计算 (与策略保持一致)"""
    alpha = 2.0 / (span + 1)
    result = np.zeros_like(arr, dtype=np.float64)
    result[0] = arr[0]
    for i in range(1, len(arr)):
        result[i] = alpha * arr[i] + (1 - alpha) * result[i - 1]
    return result


def compute_adx(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> float:
    """计算 ADX 趋势强度 (当前值)"""
    n = len(close)
    if n < period + 1:
        return 0.0

    dm_plus = np.zeros(n)
    dm_minus = np.zeros(n)
    tr = np.zeros(n)

    for i in range(1, n):
        up = high[i] - high[i-1]
        down = low[i-1] - low[i]

        if up > down and up > 0:
            dm_plus[i] = up
        else:
            dm_plus[i] = 0

        if down > up and down > 0:
            dm_minus[i] = down
        else:
            dm_minus[i] = 0

        tr[i] = max(
            high[i] - low[i],
            abs(high[i] - close[i-1]),
            abs(low[i] - close[i-1])
        )

    # Wilder smoothing
    tr_smooth = np.zeros(n)
    dm_plus_smooth = np.zeros(n)
    dm_minus_smooth = np.zeros(n)

    tr_smooth[period] = np.sum(tr[1:period+1])
    dm_plus_smooth[period] = np.sum(dm_plus[1:period+1])
    dm_minus_smooth[period] = np.sum(dm_minus[1:period+1])

    for i in range(period+1, n):
        tr_smooth[i] = tr_smooth[i-1] - tr_smooth[i-1] / period + tr[i]
        dm_plus_smooth[i] = dm_plus_smooth[i-1] - dm_plus_smooth[i-1] / period + dm_plus[i]
        dm_minus_smooth[i] = dm_minus_smooth[i-1] - dm_minus_smooth[i-1] / period + dm_minus[i]

    di_plus = np.zeros(n)
    di_minus = np.zeros(n)
    dx = np.zeros(n)
    adx = np.zeros(n)

    for i in range(period, n):
        denom = tr_smooth[i] if tr_smooth[i] > 0 else 1e-8
        di_plus[i] = dm_plus_smooth[i] / denom * 100
        di_minus[i] = dm_minus_smooth[i] / denom * 100
        di_sum = di_plus[i] + di_minus[i] if (di_plus[i] + di_minus[i]) > 0 else 1e-8
        dx[i] = abs(di_plus[i] - di_minus[i]) / di_sum * 100

    # Wilder ADX smoothing
    adx[2*period-1] = np.mean(dx[period:2*period])
    for i in range(2*period, n):
        adx[i] = (adx[i-1] * (period-1) + dx[i]) / period

    return float(adx[-1])


def compute_atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> tuple:
    """计算 ATR 当前值 + 序列"""
    n = len(close)
    tr = np.zeros(n)
    for i in range(1, n):
        tr[i] = max(
            high[i] - low[i],
            abs(high[i] - close[i-1]),
            abs(low[i] - close[i-1])
        )
    atr = pd_ema(tr, period * 2 - 1)  # Wilder smoothing ≈ 2*period-1 EMA
    return float(atr[-1]), atr


def compute_atr_percentile(atr: np.ndarray, window: int = 20) -> float:
    """ATR 在最近 window 周期的百分位 (0-100)"""
    if len(atr) < window:
        return 50.0
    recent = atr[-window:]
    current = recent[-1]
    if np.std(recent) < 1e-12:
        return 50.0
    rank = np.sum(recent <= current)
    return float(rank / window * 100)


def compute_ema_deviation(close: np.ndarray, ema_span: int = 453) -> float:
    """价格相对EMA的偏离百分比 (+多/-空)"""
    if len(close) < ema_span + 1:
        return 0.0
    ema = pd_ema(close, ema_span)
    return float((close[-1] - ema[-1]) / ema[-1] * 100)


def compute_bb_width(close: np.ndarray, period: int = 20, std_mult: float = 2.0) -> float:
    """布林带宽度 (波动率收窄/扩张的辅助指标)"""
    if len(close) < period:
        return 0.0
    ma = np.mean(close[-period:])
    std = np.std(close[-period:])
    return float((ma + std_mult * std - (ma - std_mult * std)) / ma * 100)


def classify_regime(
    adx: float,
    atr_pct: float,
    ema_dev: float,
    bb_width: Optional[float] = None,
) -> str:
    """
    三指标 → 五类行情

    参数:
        adx: ADX(14) 值
        atr_pct: ATR百分位 0-100
        ema_dev: EMA453偏离 %
        bb_width: 布林带宽度 % (可选辅助)

    返回:
        TREND_STEADY | TREND_VOL | WEAK_TREND | CHOPPY | SQUEEZE
    """
    # 趋势判断
    is_strong_trend = adx >= 25
    is_weak_trend = 20 <= adx < 25
    is_ranging = adx < 20

    # 波动判断
    is_high_vol = atr_pct >= 70
    is_low_vol = atr_pct <= 30
    is_normal_vol = 30 < atr_pct < 70

    if is_strong_trend:
        if is_high_vol:
            return Regime.TREND_VOL
        else:
            return Regime.TREND_STEADY

    if is_weak_trend:
        return Regime.WEAK_TREND

    # adx < 20 震荡
    if is_high_vol or is_normal_vol:
        return Regime.CHOPPY
    else:
        return Regime.SQUEEZE


def analyze_regime(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: Optional[np.ndarray] = None,
) -> Dict:
    """
    一站式行情分型分析

    输入: OHLCV numpy arrays (建议>=50根, 30m或4h K线)
    输出: 完整诊断字典

    Usage:
        df = exchange.fetch_ohlcv('ETC/USDT:USDT', '30m', limit=100)
        h, l, c, v = [np.array(x) for x in ...]
        result = analyze_regime(h, l, c, v)
        print(result['regime'])  # 'TREND_STEADY'
    """
    n = len(close)
    if n < 50:
        return {"regime": "UNKNOWN", "reason": "数据不足(需>=50根K线)"}

    # ── 核心三指标 ──
    adx = compute_adx(high, low, close)
    atr_val, atr_series = compute_atr(high, low, close)
    atr_pct = compute_atr_percentile(atr_series)
    atr_ratio = atr_val / (np.mean(close[-14:]) + 1e-8) * 100  # ATR相对价格%

    ema_dev = compute_ema_deviation(close)
    bb_w = compute_bb_width(close)

    # 方向判定
    if ema_dev > 0.3:
        direction = "LONG"
    elif ema_dev < -0.3:
        direction = "SHORT"
    else:
        direction = "NEUTRAL"

    # ── 分类 ──
    regime = classify_regime(adx, atr_pct, ema_dev, bb_w)

    # ── 获取适配参数 ──
    adapt = REGIME_ADAPT.get(regime, REGIME_ADAPT[Regime.CHOPPY])

    return {
        "regime": regime,
        "direction": direction,
        "metrics": {
            "adx": round(adx, 1),
            "atr_val": round(atr_val, 6),
            "atr_pct": round(atr_ratio, 3),       # ATR相对价格%
            "atr_percentile": round(atr_pct, 1),   # ATR百分位
            "ema453_dev": round(ema_dev, 2),        # EMA偏离%
            "bb_width": round(bb_w, 2),
        },
        "adapt": adapt,
        "description": adapt.get("description", ""),
        "timestamp": time.time(),
    }


def get_global_regime(symbol_regimes: Dict[str, str]) -> Tuple[str, Dict]:
    """
    多币种综合 → 全局行情

    逻辑:
        >50%币种为CHOPPY/SQUEEZE → GLOBAL_CHOPPY (减少开仓)
        >50%币种为TREND_* → GLOBAL_TREND (正常交易)
        否则: MIXED

    返回: (global_regime, stats)
    """
    if not symbol_regimes:
        return "UNKNOWN", {}

    n = len(symbol_regimes)
    trending = sum(1 for r in symbol_regimes.values()
                   if r in (Regime.TREND_STEADY, Regime.TREND_VOL))
    ranging = sum(1 for r in symbol_regimes.values()
                  if r in (Regime.CHOPPY, Regime.SQUEEZE))
    weak = sum(1 for r in symbol_regimes.values() if r == Regime.WEAK_TREND)

    # 2026-07-20收紧: 震荡≥40%→CHOPPY, 趋势需≥65%→GLOBAL_TREND
    if ranging / n >= 0.4:
        global_r = "GLOBAL_CHOPPY"
        extra_factor = 0.4  # 全局仓位再打折
    elif trending / n >= 0.65:
        global_r = "GLOBAL_TREND"
        extra_factor = 1.0
    else:
        global_r = "MIXED"
        extra_factor = 0.7

    return global_r, {
        "trending": trending,
        "ranging": ranging,
        "weak": weak,
        "total": n,
        "global_position_factor": extra_factor,
        "details": symbol_regimes,
    }


# ─── 快速命令行测试 ───
if __name__ == "__main__":
    import sys
    import json

    # 生成测试数据
    np.random.seed(42)
    n = 100
    # 模拟强趋势
    trend_close = np.linspace(100, 120, n) + np.random.normal(0, 0.5, n)
    trend_high = trend_close + np.random.uniform(0.5, 1.5, n)
    trend_low = trend_close - np.random.uniform(0.5, 1.5, n)

    # 模拟震荡
    choppy_close = 100 + np.sin(np.linspace(0, 6*np.pi, n)) * 5 + np.random.normal(0, 0.3, n)
    choppy_high = choppy_close + np.random.uniform(0.3, 0.8, n)
    choppy_low = choppy_close - np.random.uniform(0.3, 0.8, n)

    print("=" * 60)
    print("行情分型测试")
    print("=" * 60)

    print("\n📈 趋势行情:")
    result = analyze_regime(trend_high, trend_low, trend_close)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n📊 震荡行情:")
    result2 = analyze_regime(choppy_high, choppy_low, choppy_close)
    print(json.dumps(result2, indent=2, ensure_ascii=False))

    print("\n🌍 全局行情:")
    test_regimes = {
        "BTC": Regime.TREND_STEADY,
        "ETH": Regime.TREND_VOL,
        "DOGE": Regime.CHOPPY,
        "DOT": Regime.SQUEEZE,
        "ADA": Regime.WEAK_TREND,
        "XRP": Regime.CHOPPY,
        "SOL": Regime.TREND_STEADY,
        "AVAX": Regime.CHOPPY,
    }
    global_r, stats = get_global_regime(test_regimes)
    print(global_r)
    print(json.dumps(stats, indent=2, ensure_ascii=False))
