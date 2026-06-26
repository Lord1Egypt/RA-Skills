#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║         跨市场股票技术指标扫描系统  v4.0 (TradingView Edition)    ║
║         Multi-Market Stock Technical Indicator Scanner            ║
║                                                                  ║
║  数据来源: TradingView (tvDatafeed)                               ║
║  支持市场: A股 / 港股 / 美股 / 日股                              ║
║  输入: Obsidian vault 中的 watchlist.csv                         ║
║  输出: Obsidian vault 中的 Markdown 技术分析日报                  ║
║                                                                  ║
║  筛选信号 (14项):                                                ║
║    1.  MA5/MA10 黄金交叉 (量能+趋势确认)                         ║
║    2.  MA5/MA10 死亡交叉 (量能确认)                               ║
║    3.  RSI 超卖回升 / 底背离                                     ║
║    4.  RSI 超买                                                  ║
║    5.  突破历史新高 (252日窗口)                                   ║
║    6.  BOLL 上轨突破 / 下轨跌破                                  ║
║    7.  下行趋势均线收窄靠拢 MA20                                 ║
║    8.  MACD 金叉 / 死叉                                          ║
║    9.  放量突破                                                  ║
║   10.  缩量回调                                                  ║
║   11.  量价背离预警                                              ║
║   12.  周K趋势                                                   ║
║   13.  日周共振                                                  ║
║   14.  综合评分 (0-100)                                          ║
║                                                                  ║
║  用法:                                                           ║
║    python scanner.py --csv watchlist.csv --output ./reports       ║
║    python scanner.py --demo                                      ║
║    python scanner.py --workers 8 --min-score 50                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import argparse
import json
import sys
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")


# ════════════════════════════════════════════════════════════════
# 默认参数
# ════════════════════════════════════════════════════════════════
DEFAULTS = {
    "csv":                  "watchlist.csv",
    "output_dir":           "./技术指标扫描",
    "rsi_period":           14,
    "rsi_oversold":         30,
    "rsi_overbought":       70,
    "ma_short":             5,
    "ma_long":              10,
    "ma_mid":               20,
    "ma_trend":             60,
    "boll_period":          20,
    "boll_k":               2.0,
    "lookback_days":        120,
    "ath_days":             252,
    "request_delay":        0.3,
    "timeout":              15,
    "max_retries":          2,
    "near_ma20_pct":        0.03,
    "spread_narrow_ratio":  0.85,
    "macd_fast":            12,
    "macd_slow":            26,
    "macd_signal":          9,
    "atr_period":           14,
    "atr_stop_mult":        2.0,
    "vol_confirm_ratio":    1.2,
    "vol_breakout_ratio":   1.5,
    "vol_pullback_ratio":   0.7,
    "workers":              6,
    "min_score":            0,
}

MARKET_EMOJI = {
    "US":   "🇺🇸",
    "A股":  "🇨🇳",
    "港股": "🇭🇰",
    "日股": "🇯🇵",
}


# ════════════════════════════════════════════════════════════════
# TradingView 数据获取
# ════════════════════════════════════════════════════════════════
def _resolve_tv_symbol(ticker: str, market_hint: str) -> list[tuple[str, str]]:
    """
    将 watchlist ticker 转为 (symbol, exchange) 列表供 TradingView 查询。
    返回多个候选，按优先级排列。
    """
    t = ticker.strip().upper()
    hint = market_hint.strip()

    # A股 - 上交所
    if t.endswith(".SS") or t.endswith(".SH"):
        code = t.rsplit(".", 1)[0]
        return [(code, "SSE")]
    # A股 - 深交所
    if t.endswith(".SZ"):
        code = t.rsplit(".", 1)[0]
        return [(code, "SZSE")]
    # 港股
    if t.endswith(".HK"):
        code = t.rsplit(".", 1)[0].lstrip("0").zfill(5)
        return [(code, "HKEX")]
    # 日股
    if t.endswith(".T"):
        code = t.rsplit(".", 1)[0]
        return [(code, "TSE")]

    # 纯数字
    if t.isdigit():
        if hint == "港股":
            return [(t.lstrip("0").zfill(5), "HKEX")]
        if hint == "日股":
            return [(t, "TSE")]
        if len(t) == 6:
            if t[0] in ("6", "7", "9"):
                return [(t, "SSE")]
            else:
                return [(t, "SZSE")]
        if len(t) in (4, 5):
            return [(t.zfill(5), "HKEX")]

    # 默认当作美股
    if hint.upper() in ("US", "美股") or not t[0].isdigit():
        return [
            (t, "NASDAQ"),
            (t, "NYSE"),
            (t, "AMEX"),
        ]

    return []


def _fetch_tradingview(symbol: str, exchange: str, n_bars: int,
                       timeout: int = 15) -> pd.DataFrame | None:
    """
    通过 tvDatafeed 从 TradingView 获取日线 OHLCV 数据。
    返回 DataFrame(Date index, Open/High/Low/Close/Volume columns) 或 None。
    """
    try:
        from tvDatafeed import TvDatafeed, Interval
    except ImportError:
        print("  ⚠️  tvDatafeed 未安装，尝试: pip install tvDatafeed --break-system-packages")
        return None

    try:
        tv = TvDatafeed()
        df = tv.get_hist(
            symbol=symbol,
            exchange=exchange,
            interval=Interval.in_daily,
            n_bars=n_bars,
        )
        if df is None or len(df) < 10:
            return None

        # tvDatafeed 返回列名为 open/high/low/close/volume (小写)
        df = df.rename(columns={
            "open": "Open", "high": "High", "low": "Low",
            "close": "Close", "volume": "Volume",
        })
        # 确保 index 为 DatetimeIndex
        df.index = pd.to_datetime(df.index)
        df.index.name = "Date"

        # 只保留需要的列
        keep_cols = ["Open", "High", "Low", "Close", "Volume"]
        for c in keep_cols:
            if c not in df.columns:
                return None

        return df[keep_cols].dropna().sort_index()
    except Exception as e:
        return None


def _fetch_tv_weekly(symbol: str, exchange: str, n_bars: int = 60,
                     timeout: int = 15) -> pd.DataFrame | None:
    """获取周线数据用于周K趋势判断（可选，如果日线 resample 不够准确）。"""
    try:
        from tvDatafeed import TvDatafeed, Interval
        tv = TvDatafeed()
        df = tv.get_hist(
            symbol=symbol, exchange=exchange,
            interval=Interval.in_weekly, n_bars=n_bars,
        )
        if df is None or len(df) < 10:
            return None
        df = df.rename(columns={
            "open": "Open", "high": "High", "low": "Low",
            "close": "Close", "volume": "Volume",
        })
        df.index = pd.to_datetime(df.index)
        return df[["Open", "High", "Low", "Close", "Volume"]].dropna().sort_index()
    except Exception:
        return None


def fetch_data(ticker: str, market_hint: str, cfg: dict) -> pd.DataFrame | None:
    """主数据拉取入口：遍历候选 (symbol, exchange) 尝试 TradingView。"""
    candidates = _resolve_tv_symbol(ticker, market_hint)
    fetch_days = max(cfg["lookback_days"], cfg.get("ath_days", 252))
    n_bars = int(fetch_days * 1.5)  # 多拉一些以应对节假日
    min_bars = max(cfg.get("ma_trend", 60), cfg.get("macd_slow", 26) + cfg.get("macd_signal", 9)) + 5

    for symbol, exchange in candidates:
        df = _fetch_tradingview(symbol, exchange, n_bars, cfg.get("timeout", 15))
        if df is not None and len(df) >= min_bars:
            time.sleep(cfg.get("request_delay", 0.3))
            return df
        time.sleep(0.05)

    return None


# ════════════════════════════════════════════════════════════════
# 离线演示数据（--demo 模式）
# ════════════════════════════════════════════════════════════════
def mock_data(ticker: str, lookback_days: int) -> pd.DataFrame:
    rng    = np.random.default_rng(abs(hash(ticker)) % (2**31))
    days   = max(lookback_days, 130)
    dates  = pd.bdate_range(end=datetime.today(), periods=days)
    price  = 100.0
    closes = []
    for _ in range(days):
        price = max(price * (1 + rng.normal(0, 0.015)), 1)
        closes.append(price)
    closes = np.array(closes)
    return pd.DataFrame({
        "Open":   closes * (1 + rng.uniform(-0.005, 0.005, days)),
        "High":   closes * (1 + rng.uniform(0.000, 0.015, days)),
        "Low":    closes * (1 - rng.uniform(0.000, 0.015, days)),
        "Close":  closes,
        "Volume": rng.integers(1_000_000, 50_000_000, days).astype(float),
    }, index=dates)


# ════════════════════════════════════════════════════════════════
# 技术指标计算
# ════════════════════════════════════════════════════════════════
def compute_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta    = close.diff()
    gain     = delta.clip(lower=0)
    loss     = (-delta).clip(lower=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def compute_macd(close: pd.Series, fast: int = 12, slow: int = 26,
                 signal: int = 9) -> tuple[pd.Series, pd.Series, pd.Series]:
    ema_fast    = close.ewm(span=fast,   adjust=False).mean()
    ema_slow    = close.ewm(span=slow,   adjust=False).mean()
    macd_line   = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram   = macd_line - signal_line
    return macd_line, signal_line, histogram


def compute_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high  = df["High"]
    low   = df["Low"]
    prev_close = df["Close"].shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low  - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(com=period - 1, min_periods=period).mean()


def compute_indicators(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    df = df.copy()
    ma_s         = cfg["ma_short"]
    ma_l         = cfg["ma_long"]
    ma_mid       = cfg.get("ma_mid", 20)
    ma_trend     = cfg.get("ma_trend", 60)
    ath_days     = cfg.get("ath_days", 252)
    boll_period  = cfg.get("boll_period", 20)
    boll_k       = cfg.get("boll_k", 2.0)
    near_pct     = cfg.get("near_ma20_pct", 0.03)
    narrow_ratio = cfg.get("spread_narrow_ratio", 0.85)
    vol_confirm  = cfg.get("vol_confirm_ratio", 1.2)
    vol_breakout = cfg.get("vol_breakout_ratio", 1.5)
    vol_pullback = cfg.get("vol_pullback_ratio", 0.7)
    atr_period   = cfg.get("atr_period", 14)
    atr_mult     = cfg.get("atr_stop_mult", 2.0)
    macd_fast    = cfg.get("macd_fast", 12)
    macd_slow    = cfg.get("macd_slow", 26)
    macd_signal  = cfg.get("macd_signal", 9)

    # ── 均线 ────────────────────────────────────────────────────
    df["MA_short"]      = df["Close"].rolling(ma_s).mean()
    df["MA_long"]       = df["Close"].rolling(ma_l).mean()
    df["MA_mid"]        = df["Close"].rolling(ma_mid).mean()
    df["MA_trend"]      = df["Close"].rolling(ma_trend).mean()
    df["MA_short_prev"] = df["MA_short"].shift(1)
    df["MA_long_prev"]  = df["MA_long"].shift(1)

    # ── 成交量均线 ───────────────────────────────────────────────
    df["Vol_MA5"]  = df["Volume"].rolling(5).mean()
    df["Vol_MA20"] = df["Volume"].rolling(20).mean()

    # ── RSI ──────────────────────────────────────────────────────
    df["RSI"] = compute_rsi(df["Close"], cfg["rsi_period"])

    # ── MACD ─────────────────────────────────────────────────────
    df["MACD"], df["MACD_signal"], df["MACD_hist"] = compute_macd(
        df["Close"], macd_fast, macd_slow, macd_signal)
    df["MACD_prev"]        = df["MACD"].shift(1)
    df["MACD_signal_prev"] = df["MACD_signal"].shift(1)
    df["MACD_hist_prev"]   = df["MACD_hist"].shift(1)

    # ── ATR & 动态止损 ───────────────────────────────────────────
    df["ATR"]       = compute_atr(df, atr_period)
    df["stop_loss"] = df["Close"] - atr_mult * df["ATR"]

    # ── 黄金交叉 / 死亡交叉 ─────────────────────────────────────
    volume_confirm_up   = df["Volume"] > df["Vol_MA20"] * vol_confirm
    volume_confirm_down = df["Volume"] > df["Vol_MA20"] * vol_confirm
    ma20_slope_up   = df["MA_mid"].diff(3) > 0
    ma20_slope_down = df["MA_mid"].diff(3) < 0

    df["golden_cross"] = (
        (df["MA_short"] > df["MA_long"]) &
        (df["MA_short_prev"] <= df["MA_long_prev"]) &
        volume_confirm_up & ma20_slope_up
    )
    df["golden_cross_raw"] = (
        (df["MA_short"] > df["MA_long"]) &
        (df["MA_short_prev"] <= df["MA_long_prev"])
    )
    df["death_cross"] = (
        (df["MA_short"] < df["MA_long"]) &
        (df["MA_short_prev"] >= df["MA_long_prev"]) &
        volume_confirm_down & ma20_slope_down
    )
    df["death_cross_raw"] = (
        (df["MA_short"] < df["MA_long"]) &
        (df["MA_short_prev"] >= df["MA_long_prev"])
    )

    # ── MACD 金叉 / 死叉 ──────────────────────────────────────────
    df["macd_golden"]      = (df["MACD"] > df["MACD_signal"]) & (df["MACD_prev"] <= df["MACD_signal_prev"])
    df["macd_death"]       = (df["MACD"] < df["MACD_signal"]) & (df["MACD_prev"] >= df["MACD_signal_prev"])
    df["macd_golden_zero"] = df["macd_golden"] & (df["MACD"] > 0)
    df["macd_hist_flip"]   = (df["MACD_hist"] > 0) & (df["MACD_hist_prev"] <= 0)

    # ── RSI 超卖回升 & 底背离 ──────────────────────────────────
    rsi_os = cfg["rsi_oversold"]
    rsi_ob = cfg["rsi_overbought"]
    df["rsi_recover"] = (
        (df["RSI"].shift(1) < rsi_os) & (df["RSI"] >= rsi_os)
    )
    price_new_low   = df["Close"] < df["Close"].rolling(10).min().shift(1)
    rsi_not_new_low = df["RSI"] > df["RSI"].rolling(10).min().shift(1)
    df["rsi_bullish_div"] = price_new_low & rsi_not_new_low & (df["RSI"] < 45)
    df["oversold"]   = df["RSI"] < rsi_os
    df["overbought"] = df["RSI"] > rsi_ob

    # ── BOLL ─────────────────────────────────────────────────────
    df["BOLL_mid"]   = df["Close"].rolling(boll_period).mean()
    boll_std         = df["Close"].rolling(boll_period).std()
    df["BOLL_upper"] = df["BOLL_mid"] + boll_k * boll_std
    df["BOLL_lower"] = df["BOLL_mid"] - boll_k * boll_std
    df["boll_above_upper"] = df["Close"] > df["BOLL_upper"]
    df["boll_below_lower"] = df["Close"] < df["BOLL_lower"]

    # ── 成交量形态 ────────────────────────────────────────────────
    uptrend = df["MA_short"] > df["MA_mid"]
    price_breakout = df["Close"] > df["Close"].rolling(20).max().shift(1)
    df["volume_breakout"] = price_breakout & (df["Volume"] > df["Vol_MA20"] * vol_breakout)
    price_down = df["Close"] < df["Close"].shift(1)
    df["healthy_pullback"] = uptrend & price_down & (df["Volume"] < df["Vol_MA5"] * vol_pullback)
    price_up_3d = (df["Close"] > df["Close"].shift(1)) & (df["Close"].shift(1) > df["Close"].shift(2))
    vol_down_3d = (df["Volume"] < df["Volume"].shift(1)) & (df["Volume"].shift(1) < df["Volume"].shift(2))
    df["price_vol_divergence"] = price_up_3d & vol_down_3d & uptrend

    # ── 下行趋势均线收窄靠拢 MA20 ─────────────────────────────
    downtrend = df["MA_short"] < df["MA_long"]
    df["MA_spread"]       = df["MA_long"] - df["MA_short"]
    df["MA_spread_avg5"]  = df["MA_spread"].shift(1).rolling(5, min_periods=2).mean()
    spread_narrowed       = df["MA_spread"] < (df["MA_spread_avg5"] * narrow_ratio)
    ma20_valid            = df["MA_mid"].notna() & (df["MA_mid"] > 0)
    near_short            = (df["MA_short"] - df["MA_mid"]).abs() / df["MA_mid"] <= near_pct
    near_long             = (df["MA_long"]  - df["MA_mid"]).abs() / df["MA_mid"] <= near_pct
    df["ma_narrow_near_20"] = downtrend & spread_narrowed & near_short & near_long & ma20_valid

    # ── 周K趋势 ──────────────────────────────────────────────────
    week_rule = "W-FRI"
    weekly    = df.resample(week_rule).agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last"}
    ).dropna()
    if len(weekly) >= 10:
        weekly["MA5_w"]  = weekly["Close"].rolling(5).mean()
        weekly["MA10_w"] = weekly["Close"].rolling(10).mean()
        last_week        = weekly.iloc[-1]
        week_bull        = (
            pd.notna(last_week.get("MA5_w")) and
            pd.notna(last_week.get("MA10_w")) and
            last_week["MA5_w"] > last_week["MA10_w"]
        )
        df["week_trend_bull"]             = week_bull
        df["week_trend"]                  = "多头" if week_bull else "空头"
        daily_bull                        = df["MA_short"] > df["MA_long"]
        df["daily_weekly_resonance_bull"] = daily_bull & df["week_trend_bull"]
        df["daily_weekly_resonance_bear"] = (~daily_bull) & (~df["week_trend_bull"])
    else:
        df["week_trend_bull"]             = np.nan
        df["week_trend"]                  = ""
        df["daily_weekly_resonance_bull"] = False
        df["daily_weekly_resonance_bear"] = False

    # ── 历史新高 ──────────────────────────────────────────────────
    window = min(ath_days, len(df) - 1) if len(df) > 1 else 1
    df["hist_high"]      = df["High"].shift(1).rolling(window, min_periods=1).max()
    df["new_high"]       = df["High"]  >= df["hist_high"]
    df["new_high_close"] = df["Close"] >= df["High"].shift(1).rolling(window, min_periods=1).max()

    return df


# ════════════════════════════════════════════════════════════════
# 综合评分系统
# ════════════════════════════════════════════════════════════════
def compute_score(result: dict) -> int:
    score = 0
    # 趋势类（最高 40 分）
    if result.get("daily_weekly_resonance_bull"):  score += 20
    elif result.get("golden_cross"):               score += 14
    elif result.get("golden_cross_raw"):           score += 8
    if result.get("new_high_close"):               score += 10
    elif result.get("new_high"):                   score += 6
    if result.get("death_cross"):                  score -= 15
    elif result.get("daily_weekly_resonance_bear"):score -= 12

    # 动量类（最高 35 分）
    rsi = result.get("rsi")
    if rsi is not None:
        if result.get("rsi_recover"):              score += 15
        elif result.get("rsi_bullish_div"):        score += 12
        elif rsi < 35:                             score += 8
        elif rsi > 70:                             score -= 8
        elif rsi > 65:                             score -= 3
    if result.get("macd_golden_zero"):             score += 14
    elif result.get("macd_golden"):                score += 9
    elif result.get("macd_hist_flip"):             score += 6
    if result.get("macd_death"):                   score -= 10

    # 量价类（最高 25 分）
    if result.get("volume_breakout"):              score += 18
    if result.get("healthy_pullback"):             score += 8
    if result.get("boll_below_lower"):             score += 7
    if result.get("ma_narrow_near_20"):            score += 7
    if result.get("price_vol_divergence"):         score -= 12
    if result.get("boll_above_upper"):             score -= 5

    return max(0, min(100, score))


# ════════════════════════════════════════════════════════════════
# 单股分析
# ════════════════════════════════════════════════════════════════
def analyse_ticker(row: pd.Series, cfg: dict, use_mock: bool) -> dict:
    ticker      = str(row["ticker"]).strip()
    market_hint = str(row.get("market", "")).strip()

    df = mock_data(ticker, cfg["lookback_days"]) if use_mock else fetch_data(ticker, market_hint, cfg)

    if df is None:
        return {
            "ticker": ticker, "name": row.get("name", ticker),
            "market": market_hint or "—", "sector": row.get("sector", "—"),
            "error": "数据获取失败（TradingView 无数据或网络异常）",
            "score": 0, "buy_signals": [], "multi_buy": False,
            "week_trend": "—",
            "daily_weekly_resonance_bull": False,
            "daily_weekly_resonance_bear": False,
        }

    df     = compute_indicators(df, cfg)
    latest = df.iloc[-1]
    prev   = df.iloc[-2] if len(df) >= 2 else latest

    def _f(v):
        return None if (v is None or (isinstance(v, float) and np.isnan(v))) else v

    close      = latest["Close"]
    high       = latest["High"]
    ma_short   = latest["MA_short"]
    ma_long    = latest["MA_long"]
    rsi        = latest["RSI"]
    pct_chg    = (close - prev["Close"]) / prev["Close"] * 100 if prev["Close"] else 0
    hist_high  = latest.get("hist_high", np.nan)
    boll_upper = latest.get("BOLL_upper")
    boll_lower = latest.get("BOLL_lower")
    macd_val   = latest.get("MACD")
    macd_sig   = latest.get("MACD_signal")
    macd_hist  = latest.get("MACD_hist")
    atr_val    = latest.get("ATR")
    stop_loss  = latest.get("stop_loss")
    vol_ma20   = latest.get("Vol_MA20", np.nan)
    avg_daily_val = (vol_ma20 * close) if _f(vol_ma20) else None

    # 信号布尔值
    golden_cross     = bool(latest.get("golden_cross", False))
    golden_cross_raw = bool(latest.get("golden_cross_raw", False))
    death_cross      = bool(latest.get("death_cross", False))
    death_cross_raw  = bool(latest.get("death_cross_raw", False))
    boll_above       = bool(latest.get("boll_above_upper", False))
    boll_below       = bool(latest.get("boll_below_lower", False))
    ma_narrow        = bool(latest.get("ma_narrow_near_20", False))
    macd_golden      = bool(latest.get("macd_golden", False))
    macd_golden_zero = bool(latest.get("macd_golden_zero", False))
    macd_death       = bool(latest.get("macd_death", False))
    macd_hist_flip   = bool(latest.get("macd_hist_flip", False))
    rsi_recover      = bool(latest.get("rsi_recover", False))
    rsi_bullish_div  = bool(latest.get("rsi_bullish_div", False))
    vol_breakout     = bool(latest.get("volume_breakout", False))
    healthy_pullback = bool(latest.get("healthy_pullback", False))
    price_vol_div    = bool(latest.get("price_vol_divergence", False))
    new_high         = bool(latest.get("new_high", False))
    new_high_close   = bool(latest.get("new_high_close", False))
    week_trend_bull  = bool(latest.get("week_trend_bull", False)) if _f(latest.get("week_trend_bull")) else False
    week_trend_str   = latest.get("week_trend") or "—"
    res_bull         = bool(latest.get("daily_weekly_resonance_bull", False))
    res_bear         = bool(latest.get("daily_weekly_resonance_bear", False))

    # 买入信号列表
    buy_signals = []
    if res_bull:                          buy_signals.append("日周共振多")
    if golden_cross:                      buy_signals.append("黄金交叉(确认)")
    elif golden_cross_raw:                buy_signals.append("黄金交叉(未确认)")
    if rsi_recover:                       buy_signals.append("RSI超卖回升")
    if rsi_bullish_div:                   buy_signals.append("RSI底背离")
    if _f(rsi) and rsi < cfg["rsi_oversold"]:  buy_signals.append("RSI超卖")
    if macd_golden_zero:                  buy_signals.append("MACD零上金叉")
    elif macd_golden:                     buy_signals.append("MACD金叉")
    elif macd_hist_flip:                  buy_signals.append("MACD柱翻正")
    if vol_breakout:                      buy_signals.append("放量突破")
    if boll_below:                        buy_signals.append("BOLL下轨")
    if ma_narrow:                         buy_signals.append("均线收窄靠拢20")
    if healthy_pullback:                  buy_signals.append("缩量回调")
    if new_high_close:                    buy_signals.append("收盘新高")
    elif new_high:                        buy_signals.append("盘中新高")

    multi_buy = len(buy_signals) >= 2

    result = {
        "ticker": ticker, "name": row.get("name", ticker),
        "market": market_hint or "—", "sector": row.get("sector", "—"),
        "close": round(float(close), 3), "high": round(float(high), 3),
        "pct_chg": round(float(pct_chg), 2),
        "ma_short": round(float(ma_short), 3) if _f(ma_short) else None,
        "ma_long":  round(float(ma_long),  3) if _f(ma_long)  else None,
        "rsi": round(float(rsi), 2) if _f(rsi) else None,
        "golden_cross": golden_cross, "golden_cross_raw": golden_cross_raw,
        "death_cross": death_cross, "death_cross_raw": death_cross_raw,
        "oversold": bool(rsi < cfg["rsi_oversold"]) if _f(rsi) else False,
        "overbought": bool(rsi > cfg["rsi_overbought"]) if _f(rsi) else False,
        "rsi_recover": rsi_recover, "rsi_bullish_div": rsi_bullish_div,
        "new_high": new_high, "new_high_close": new_high_close,
        "hist_high": round(float(hist_high), 3) if _f(hist_high) else None,
        "ath_days": cfg.get("ath_days", 252),
        "boll_above_upper": boll_above, "boll_below_lower": boll_below,
        "boll_upper": round(float(boll_upper), 3) if _f(boll_upper) else None,
        "boll_lower": round(float(boll_lower), 3) if _f(boll_lower) else None,
        "ma_narrow_near_20": ma_narrow,
        "macd_golden": macd_golden, "macd_golden_zero": macd_golden_zero,
        "macd_death": macd_death, "macd_hist_flip": macd_hist_flip,
        "macd_val": round(float(macd_val), 4) if _f(macd_val) else None,
        "macd_signal_val": round(float(macd_sig), 4) if _f(macd_sig) else None,
        "macd_hist_val": round(float(macd_hist), 4) if _f(macd_hist) else None,
        "volume_breakout": vol_breakout, "healthy_pullback": healthy_pullback,
        "price_vol_divergence": price_vol_div,
        "atr": round(float(atr_val), 3) if _f(atr_val) else None,
        "stop_loss_ref": round(float(stop_loss), 3) if _f(stop_loss) else None,
        "risk_pct": round(float(cfg.get("atr_stop_mult", 2.0) * atr_val / close * 100), 2)
                    if _f(atr_val) and close else None,
        "avg_daily_value": round(avg_daily_val, 0) if avg_daily_val else None,
        "week_trend": week_trend_str,
        "daily_weekly_resonance_bull": res_bull,
        "daily_weekly_resonance_bear": res_bear,
        "buy_signals": buy_signals, "multi_buy": multi_buy,
        "data_date": df.index[-1].strftime("%Y-%m-%d"),
        "error": None,
    }
    result["score"] = compute_score(result)
    return result


# ════════════════════════════════════════════════════════════════
# 并发扫描
# ════════════════════════════════════════════════════════════════
def _analyse_task(args: tuple) -> tuple[int, dict]:
    idx, row, cfg, use_mock = args
    return idx, analyse_ticker(row, cfg, use_mock)


def scan_all(watchlist: pd.DataFrame, cfg: dict, use_mock: bool,
             scan_cache: dict, workers: int) -> list[dict]:
    total   = len(watchlist)
    results = [None] * total
    tasks = []
    for i, (_, row) in enumerate(watchlist.iterrows()):
        ticker = str(row["ticker"]).strip()
        if ticker in scan_cache:
            results[i] = scan_cache[ticker]
        else:
            tasks.append((i, row, cfg, use_mock))

    if not tasks:
        return results

    print(f"  ⚡ 并发扫描 {len(tasks)} 只标的（线程数={workers}）…")
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(_analyse_task, t): t[0] for t in tasks}
        done = 0
        for future in as_completed(futures):
            idx, result = future.result()
            results[idx] = result
            scan_cache[str(watchlist.iloc[idx]["ticker"]).strip()] = result
            done += 1
            ticker = str(watchlist.iloc[idx]["ticker"]).strip()
            if result.get("error"):
                status = f"❌ {result['error']}"
            else:
                sigs = "  ".join(result.get("buy_signals", [])) or "无信号"
                status = (f"RSI={result['rsi']:.1f}  "
                          f"评分={result['score']}  "
                          f"MACD={result.get('macd_val') or '—'}  "
                          f"{sigs}")
            print(f"  [{done:>3}/{len(tasks)}] {ticker:<22} {status}")

    return results


# ════════════════════════════════════════════════════════════════
# Markdown 报告生成
# ════════════════════════════════════════════════════════════════
def fmt_pct(val: float) -> str:
    sign = "▲" if val > 0 else ("▼" if val < 0 else "—")
    return f"{sign} {abs(val):.2f}%"


def results_to_markdown(results: list[dict], cfg: dict,
                         scan_dt: datetime, use_mock: bool) -> str:
    ma_s, ma_l   = cfg["ma_short"], cfg["ma_long"]
    rsi_os, rsi_ob = cfg["rsi_oversold"], cfg["rsi_overbought"]
    ath_days     = cfg.get("ath_days", 252)
    boll_p       = cfg.get("boll_period", 20)
    title_str    = scan_dt.strftime("%Y年%m月%d日")
    min_score    = cfg.get("min_score", 0)

    valid   = [r for r in results if not r.get("error")]
    errors  = [r for r in results if r.get("error")]

    golden         = [r for r in valid if r.get("golden_cross")]
    golden_raw     = [r for r in valid if r.get("golden_cross_raw") and not r.get("golden_cross")]
    death          = [r for r in valid if r.get("death_cross")]
    oversold_list  = [r for r in valid if r.get("oversold")]
    rsi_rec        = [r for r in valid if r.get("rsi_recover")]
    rsi_div        = [r for r in valid if r.get("rsi_bullish_div")]
    overbought     = [r for r in valid if r.get("overbought")]
    new_highs      = [r for r in valid if r.get("new_high")]
    boll_above     = [r for r in valid if r.get("boll_above_upper")]
    boll_below_l   = [r for r in valid if r.get("boll_below_lower")]
    ma_narrow      = [r for r in valid if r.get("ma_narrow_near_20")]
    macd_g         = [r for r in valid if r.get("macd_golden")]
    vol_bk         = [r for r in valid if r.get("volume_breakout")]
    healthy_pb     = [r for r in valid if r.get("healthy_pullback")]
    price_div      = [r for r in valid if r.get("price_vol_divergence")]
    multi_buy      = [r for r in valid if r.get("multi_buy")]
    res_bull       = [r for r in valid if r.get("daily_weekly_resonance_bull")]
    res_bear       = [r for r in valid if r.get("daily_weekly_resonance_bear")]
    high_score     = sorted([r for r in valid if r.get("score", 0) >= 60],
                            key=lambda x: -x.get("score", 0))

    lines = []

    # ── 标题 ────────────────────────────────────────────────────
    lines += [
        f"# 📊 股票技术指标日报 — {title_str}",
        "",
        f"> **扫描时间**: {scan_dt.strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"> **数据来源**: {'⚠️ 模拟演示数据（Demo Mode）' if use_mock else 'TradingView (tvDatafeed)'}  ",
        f"> **扫描标的**: {len(results)} 只  |  **最低评分过滤**: {min_score}分",
        "",
        "---",
        "",
    ]

    # ── 信号总览 ────────────────────────────────────────────────
    lines += [
        "## 📋 信号总览",
        "",
        "| 信号类型 | 数量 |",
        "|----------|------|",
        f"| 🟢 黄金交叉—量能确认（MA{ma_s} ↑ MA{ma_l}） | **{len(golden)}** |",
        f"| 🟢 黄金交叉—未确认（MA{ma_s} ↑ MA{ma_l}） | **{len(golden_raw)}** |",
        f"| 🔴 死亡交叉—量能确认（MA{ma_s} ↓ MA{ma_l}） | **{len(death)}** |",
        f"| 🔵 RSI 超卖回升（从<{rsi_os}回升） | **{len(rsi_rec)}** |",
        f"| 🔵 RSI 底背离 | **{len(rsi_div)}** |",
        f"| 🔵 RSI 超卖（RSI < {rsi_os}） | **{len(oversold_list)}** |",
        f"| 🟡 RSI 超买（RSI > {rsi_ob}） | **{len(overbought)}** |",
        f"| ⚡ MACD 金叉 | **{len(macd_g)}** |",
        f"| 📈 突破 BOLL 上轨（{boll_p}日） | **{len(boll_above)}** |",
        f"| 📉 跌破 BOLL 下轨（{boll_p}日） | **{len(boll_below_l)}** |",
        f"| 〰️ 下行趋势均线收窄靠拢 MA20 | **{len(ma_narrow)}** |",
        f"| 🚀 放量突破 | **{len(vol_bk)}** |",
        f"| 🌊 缩量回调（健康） | **{len(healthy_pb)}** |",
        f"| ⚠️ 量价背离预警 | **{len(price_div)}** |",
        f"| 📅 日周共振（多头）| **{len(res_bull)}** |",
        f"| 📅 日周共振（空头）| **{len(res_bear)}** |",
        f"| 🏆 突破历史新高（{ath_days}日窗口）| **{len(new_highs)}** |",
        "",
        "---",
        "",
    ]

    # ── 通用表格渲染器 ────────────────────────────────────────────
    def render_table(items: list[dict], extra_cols: list[tuple] | None = None) -> list[str]:
        if not items:
            return ["> _本日无触发标的_", ""]
        extras = extra_cols or []
        header  = (f"| 市场 | 代码 | 名称 | 行业 | 最新价 | 涨跌幅 | "
                   f"MA{ma_s} | MA{ma_l} | RSI{cfg['rsi_period']} | 评分")
        divider = "|------|------|------|------|--------|--------|--------|--------|---------|------|"
        for h, _ in extras:
            header  += f" | {h}"
            divider += "--------|"
        header  += " | 数据日期 |"
        divider += "----------|"
        rows = [header, divider]
        for r in sorted(items, key=lambda x: (-x.get("score", 0), x["market"], x["ticker"])):
            mkt  = MARKET_EMOJI.get(r["market"], "") + " " + r["market"]
            line = (f"| {mkt} | `{r['ticker']}` | {r['name']} | {r['sector']} | "
                    f"{r['close']:,.3f} | {fmt_pct(r['pct_chg'])} | "
                    f"{r['ma_short']:,.3f} | {r['ma_long']:,.3f} | "
                    f"{r['rsi']:.1f} | {r.get('score', 0)}")
            for _, key_or_fn in extras:
                val = key_or_fn(r) if callable(key_or_fn) else r.get(key_or_fn, "—")
                line += f" | {val}"
            line += f" | {r['data_date']} |"
            rows.append(line)
        return rows + [""]

    # ── 高分标的 ─────────────────────────────────────────────────
    if high_score:
        lines += [
            "## 🏅 高分标的（评分 ≥ 60 / 100）",
            "",
            "*综合技术评分最高的标的，信号质量更可靠。*",
            "",
            f"| 市场 | 代码 | 名称 | 行业 | 最新价 | 涨跌幅 | 评分 | 满足信号 | 止损参考 | 风险% | 数据日期 |",
            "|------|------|------|------|--------|--------|------|----------|----------|-------|----------|",
        ]
        for r in high_score:
            mkt   = MARKET_EMOJI.get(r["market"], "") + " " + r["market"]
            sigs  = "、".join(r.get("buy_signals", []))
            stop  = f"{r['stop_loss_ref']:,.3f}" if r.get("stop_loss_ref") else "—"
            risk  = f"{r['risk_pct']:.1f}%" if r.get("risk_pct") else "—"
            score = r.get("score", 0)
            bar   = "🟩" * (score // 20) + "⬜" * (5 - score // 20)
            lines.append(
                f"| {mkt} | `{r['ticker']}` | {r['name']} | {r['sector']} | "
                f"{r['close']:,.3f} | {fmt_pct(r['pct_chg'])} | "
                f"**{score}** {bar} | {sigs} | {stop} | {risk} | {r['data_date']} |"
            )
        lines += ["", "---", ""]

    # ── 多指标共振 ─────────────────────────────────────────────
    if multi_buy:
        lines += [
            "## ⭐ 多指标共振 — 重点买入关注",
            "",
            "*同时满足 **至少 2 项** 买入类信号。*",
            "",
            "| 市场 | 代码 | 名称 | 行业 | 最新价 | 涨跌幅 | 评分 | 满足的买入信号 | 数据日期 |",
            "|------|------|------|------|--------|--------|------|----------------|----------|",
        ]
        for r in sorted(multi_buy, key=lambda x: (-x.get("score", 0), x["market"], x["ticker"])):
            mkt  = MARKET_EMOJI.get(r["market"], "") + " " + r["market"]
            sigs = "、".join(r.get("buy_signals", []))
            lines.append(
                f"| {mkt} | `{r['ticker']}` | {r['name']} | {r['sector']} | "
                f"{r['close']:,.3f} | {fmt_pct(r['pct_chg'])} | "
                f"**{r.get('score', 0)}** | **{sigs}** | {r['data_date']} |"
            )
        lines += ["", "---", ""]

    # ── 各信号详情表 ──────────────────────────────────────────────
    sections = [
        (f"## 🟢 黄金交叉（量能+趋势确认）— MA{ma_s} ↑ MA{ma_l}（{len(golden)} 只）",
         f"*当日 {ma_s}日均线向上穿越 {ma_l}日均线，量能确认+MA20斜率向上。*",
         golden, None),
        (f"## 🔴 死亡交叉（量能确认）— MA{ma_s} ↓ MA{ma_l}（{len(death)} 只）",
         f"*注意下行风险。*", death, None),
        (f"## 🔵 RSI 超卖回升（{len(rsi_rec)} 只）",
         f"*RSI 从 <{rsi_os} 回升突破超卖线。*", rsi_rec, None),
        (f"## 🔵 RSI 底背离（{len(rsi_div)} 只）",
         "*价格创近10日新低，但RSI未创新低。*", rsi_div, None),
        (f"## ⚡ MACD 金叉（{len(macd_g)} 只）",
         "*DIF 上穿 DEA。零轴上方更强。*", macd_g,
         [("MACD", lambda r: f"{r.get('macd_val') or '—'}"),
          ("DEA",  lambda r: f"{r.get('macd_signal_val') or '—'}"),
          ("零轴上", lambda r: "✅" if r.get("macd_golden_zero") else "—")]),
        (f"## 🚀 放量突破（{len(vol_bk)} 只）",
         f"*价格突破近20日高点 + 量能放大。*", vol_bk, None),
        (f"## 🌊 缩量回调（{len(healthy_pb)} 只）",
         "*上升趋势中健康回调蓄势。*", healthy_pb, None),
        (f"## 📈 突破 BOLL 上轨（{len(boll_above)} 只）",
         "*强势或超买侧。*", boll_above,
         [("BOLL上轨", lambda r: f"{r['boll_upper']:,.3f}" if r.get("boll_upper") is not None else "—")]),
        (f"## 📉 跌破 BOLL 下轨（{len(boll_below_l)} 只）",
         "*超卖侧，可能反弹。*", boll_below_l,
         [("BOLL下轨", lambda r: f"{r['boll_lower']:,.3f}" if r.get("boll_lower") is not None else "—")]),
        (f"## 〰️ 均线收窄靠拢 MA20（{len(ma_narrow)} 只）",
         "*可能酝酿企稳。*", ma_narrow, None),
        (f"## 📅 日周共振多头（{len(res_bull)} 只）",
         "*日线+周线趋势一致偏多。*", res_bull,
         [("周K趋势", lambda r: r.get("week_trend") or "—")]),
        (f"## 📅 日周共振空头（{len(res_bear)} 只）",
         "*日线+周线趋势一致偏空。*", res_bear,
         [("周K趋势", lambda r: r.get("week_trend") or "—")]),
    ]

    if price_div:
        sections.append(
            (f"## ⚠️ 量价背离预警（{len(price_div)} 只）",
             "*连续3日上涨但成交量持续萎缩。*", price_div, None))

    for title, desc, items, extras in sections:
        lines += [title, "", desc, ""]
        lines += render_table(items, extras)
        lines += ["---", ""]

    # ── 历史新高 ──────────────────────────────────────────────────
    nh_extra = [
        ("当日最高价", lambda r: f"{r['high']:,.3f}"),
        (f"前{ath_days}日高点", lambda r: f"{r['hist_high']:,.3f}" if r.get("hist_high") else "—"),
        ("收盘亦新高", lambda r: "✅" if r.get("new_high_close") else "—"),
    ]
    lines += [
        f"## 🏆 突破历史新高（{ath_days} 日窗口）（{len(new_highs)} 只）",
        "", f"*当日最高价 ≥ 前 {ath_days} 个交易日最高价。*", "",
    ]
    lines += render_table(new_highs, nh_extra)
    lines += ["---", ""]

    # ── 全量快照 ─────────────────────────────────────────────────
    lines += [
        "## 📂 全部标的快照（按评分排序）",
        "",
        f"| 市场 | 代码 | 名称 | 行业 | 最新价 | 涨跌幅 | "
        f"MA{ma_s} | MA{ma_l} | RSI | MACD | 评分 | 周K | 日周 | 🟢GC | 🔴DC | "
        f"RSI回升 | MACD金 | 放量突破 | 量价背离 | 🏆新高 | ⭐多振 | 止损参考 |",
        "|------|------|------|------|--------|--------|"
        "--------|--------|-----|------|------|-----|------|------|------|"
        "---------|--------|---------|---------|--------|--------|---------|",
    ]
    for r in sorted(valid, key=lambda x: -x.get("score", 0)):
        mkt   = MARKET_EMOJI.get(r["market"], "") + " " + r["market"]
        wk    = r.get("week_trend") or "—"
        reso  = "多" if r.get("daily_weekly_resonance_bull") else ("空" if r.get("daily_weekly_resonance_bear") else "—")
        macd_str = f"{r['macd_val']:.3f}" if r.get("macd_val") is not None else "—"
        stop  = f"{r['stop_loss_ref']:,.3f}" if r.get("stop_loss_ref") else "—"
        lines.append(
            f"| {mkt} | `{r['ticker']}` | {r['name']} | {r['sector']} | "
            f"{r['close']:,.3f} | {fmt_pct(r['pct_chg'])} | "
            f"{r['ma_short']:,.3f} | {r['ma_long']:,.3f} | "
            f"{r['rsi']:.1f} | {macd_str} | **{r.get('score',0)}** | {wk} | {reso} | "
            f"{'✅' if r.get('golden_cross')      else ('🟡' if r.get('golden_cross_raw') else '—')} | "
            f"{'✅' if r.get('death_cross')        else '—'} | "
            f"{'✅' if r.get('rsi_recover')        else ('🔵' if r.get('rsi_bullish_div') else '—')} | "
            f"{'✅' if r.get('macd_golden_zero')   else ('🟡' if r.get('macd_golden') else '—')} | "
            f"{'🚀' if r.get('volume_breakout')    else '—'} | "
            f"{'⚠️' if r.get('price_vol_divergence') else '—'} | "
            f"{'🏆' if r.get('new_high')           else '—'} | "
            f"{'⭐' if r.get('multi_buy')          else '—'} | "
            f"{stop} |"
        )
    lines += ["", "---", ""]

    # ── 失败标的 ─────────────────────────────────────────────────
    if errors:
        lines += [
            "## ⚠️ 数据获取失败", "",
            "| 代码 | 名称 | 市场 | 原因 |",
            "|------|------|------|------|",
        ]
        for r in errors:
            lines.append(f"| `{r['ticker']}` | {r.get('name','—')} | {r.get('market','—')} | {r.get('error','未知')} |")
        lines += ["", "---", ""]

    # ── 指标说明 & 免责 ──────────────────────────────────────────
    lines += [
        "## 📌 指标说明",
        "",
        "| 指标 | 说明 |",
        "|------|------|",
        f"| **MA{ma_s}** | {ma_s} 日收盘价简单移动平均 |",
        f"| **MA{ma_l}** | {ma_l} 日收盘价简单移动平均 |",
        f"| **RSI{cfg['rsi_period']}** | {cfg['rsi_period']} 日相对强弱指数（Wilder 平滑法）|",
        f"| **MACD** | ({cfg['macd_fast']},{cfg['macd_slow']},{cfg['macd_signal']}) 标准参数 |",
        f"| **BOLL** | {boll_p}日中轨 ± {cfg.get('boll_k', 2)}倍标准差 |",
        f"| **ATR 止损** | 当前价 - {cfg.get('atr_stop_mult',2.0)} × ATR({cfg.get('atr_period',14)}) |",
        f"| **综合评分** | 0-100分：趋势(40)+动量(35)+量价(25)，含负分惩罚 |",
        "",
        "> ⚠️ **免责声明**: 本报告仅供技术分析学习参考，不构成任何投资建议。",
        f"> **数据来源**: {'演示模拟数据' if use_mock else 'TradingView (tvDatafeed)'}  ",
        f"> **生成时间**: {scan_dt.strftime('%Y-%m-%d %H:%M:%S')}",
    ]

    return "\n".join(lines)


# ════════════════════════════════════════════════════════════════
# Excel 报告输出
# ════════════════════════════════════════════════════════════════
def results_to_excel(results: list[dict], out_path: Path) -> None:
    try:
        import openpyxl  # noqa
    except ImportError:
        print("  ⚠️  未安装 openpyxl，跳过 Excel 输出。")
        return

    valid = [r for r in results if not r.get("error")]
    if not valid:
        return

    cols = [
        "ticker", "name", "market", "sector", "close", "pct_chg",
        "score", "rsi", "macd_val", "macd_signal_val",
        "ma_short", "ma_long", "week_trend",
        "golden_cross", "golden_cross_raw", "death_cross",
        "rsi_recover", "rsi_bullish_div", "oversold", "overbought",
        "macd_golden", "macd_golden_zero", "macd_death",
        "volume_breakout", "healthy_pullback", "price_vol_divergence",
        "boll_above_upper", "boll_below_lower", "ma_narrow_near_20",
        "new_high", "new_high_close",
        "daily_weekly_resonance_bull", "daily_weekly_resonance_bear",
        "multi_buy", "stop_loss_ref", "risk_pct", "atr",
        "avg_daily_value", "data_date",
    ]

    df_all = pd.DataFrame(valid)
    for c in cols:
        if c not in df_all.columns:
            df_all[c] = None
    df_all = df_all[cols].sort_values("score", ascending=False)

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        df_all.to_excel(writer, sheet_name="📊全部标的", index=False)
        for name, col, val in [
            ("🏅高分≥60", "score", lambda x: x >= 60),
            ("⭐多指标共振", "multi_buy", lambda x: x == True),
            ("🚀放量突破", "volume_breakout", lambda x: x == True),
            ("🏆历史新高", "new_high", lambda x: x == True),
            ("🔵RSI回升", "rsi_recover", lambda x: x == True),
            ("⚠️量价背离", "price_vol_divergence", lambda x: x == True),
        ]:
            subset = df_all[df_all[col].apply(val)]
            if not subset.empty:
                subset.to_excel(writer, sheet_name=name, index=False)

    print(f"  📊 Excel 报告已保存: {out_path}")


# ════════════════════════════════════════════════════════════════
# 缓存
# ════════════════════════════════════════════════════════════════
def _to_serializable(obj):
    if isinstance(obj, dict):
        return {k: _to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_serializable(v) for v in obj]
    if isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj) if np.isfinite(obj) else None
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def _load_scan_cache(cache_file: Path) -> dict:
    if not cache_file.exists():
        return {}
    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "results" in data:
            if data.get("demo_run") is True:
                return {}
            lst = data["results"]
        elif isinstance(data, list):
            lst = data
        else:
            return {}
        return {r["ticker"]: r for r in lst}
    except (json.JSONDecodeError, KeyError, TypeError):
        return {}


def _save_scan_cache(cache_file: Path, cache: dict, from_demo: bool = False) -> None:
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    serializable = [_to_serializable(r) for r in cache.values()]
    payload = {"demo_run": from_demo, "results": serializable}
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=0)


# ════════════════════════════════════════════════════════════════
# CLI
# ════════════════════════════════════════════════════════════════
def parse_args():
    p = argparse.ArgumentParser(
        description="跨市场股票技术指标扫描系统 v4.0 (TradingView Edition)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--csv",          default=DEFAULTS["csv"])
    p.add_argument("--output",       default=DEFAULTS["output_dir"])
    p.add_argument("--rsi-os",       type=float, default=DEFAULTS["rsi_oversold"])
    p.add_argument("--rsi-ob",       type=float, default=DEFAULTS["rsi_overbought"])
    p.add_argument("--rsi-period",   type=int,   default=DEFAULTS["rsi_period"])
    p.add_argument("--ma-short",     type=int,   default=DEFAULTS["ma_short"])
    p.add_argument("--ma-long",      type=int,   default=DEFAULTS["ma_long"])
    p.add_argument("--lookback",     type=int,   default=DEFAULTS["lookback_days"])
    p.add_argument("--delay",        type=float, default=DEFAULTS["request_delay"])
    p.add_argument("--ath-days",     type=int,   default=DEFAULTS["ath_days"])
    p.add_argument("--workers",      type=int,   default=DEFAULTS["workers"])
    p.add_argument("--min-score",    type=int,   default=DEFAULTS["min_score"])
    p.add_argument("--excel",        action="store_true", help="同时输出 Excel 报告")
    p.add_argument("--demo",         action="store_true", help="离线演示模式")
    p.add_argument("--append",       action="store_true", help="追加到当日报告")
    p.add_argument("--force",        action="store_true", help="忽略缓存，全部重新扫描")
    return p.parse_args()


def main():
    args = parse_args()

    cfg = {
        "ma_short": args.ma_short, "ma_long": args.ma_long,
        "ma_mid": DEFAULTS["ma_mid"], "ma_trend": DEFAULTS["ma_trend"],
        "boll_period": DEFAULTS["boll_period"], "boll_k": DEFAULTS["boll_k"],
        "near_ma20_pct": DEFAULTS["near_ma20_pct"],
        "spread_narrow_ratio": DEFAULTS["spread_narrow_ratio"],
        "rsi_period": args.rsi_period,
        "rsi_oversold": args.rsi_os, "rsi_overbought": args.rsi_ob,
        "lookback_days": args.lookback, "ath_days": args.ath_days,
        "request_delay": args.delay, "timeout": DEFAULTS["timeout"],
        "macd_fast": DEFAULTS["macd_fast"], "macd_slow": DEFAULTS["macd_slow"],
        "macd_signal": DEFAULTS["macd_signal"],
        "atr_period": DEFAULTS["atr_period"], "atr_stop_mult": DEFAULTS["atr_stop_mult"],
        "vol_confirm_ratio": DEFAULTS["vol_confirm_ratio"],
        "vol_breakout_ratio": DEFAULTS["vol_breakout_ratio"],
        "vol_pullback_ratio": DEFAULTS["vol_pullback_ratio"],
        "min_score": args.min_score,
    }

    use_mock   = args.demo
    out_dir    = Path(args.output)
    date_str   = datetime.now().strftime("%Y-%m-%d")
    out_file   = out_dir / f"{date_str}_technical_scan.md"
    cache_file = out_dir / f"{date_str}_scan_cache.json"

    scan_cache = {}
    if not args.force and not use_mock:
        scan_cache = _load_scan_cache(cache_file)

    # ── 读取 watchlist ──────────────────────────────────────────
    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"❌ 找不到 CSV 文件: {csv_path}")
        sys.exit(1)

    watchlist = pd.read_csv(csv_path)
    if "ticker" not in watchlist.columns:
        print("❌ CSV 必须包含 'ticker' 列")
        sys.exit(1)
    for col in ["name", "market", "sector"]:
        if col not in watchlist.columns:
            watchlist[col] = "—"

    print("╔════════════════════════════════════════════════════════════╗")
    print("║  跨市场股票技术指标扫描系统  v4.0 (TradingView Edition)   ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"📋 加载 {len(watchlist)} 只标的")
    print(f"🔧 MA{cfg['ma_short']}/MA{cfg['ma_long']}  RSI({cfg['rsi_period']})  "
          f"超卖<{cfg['rsi_oversold']}  超买>{cfg['rsi_overbought']}  "
          f"新高窗口={cfg['ath_days']}日  最低评分={cfg['min_score']}")
    print(f"🌐 数据来源: {'模拟演示（--demo）' if use_mock else 'TradingView (tvDatafeed)'}")
    print()

    # ── 并发扫描 ────────────────────────────────────────────────
    results = scan_all(watchlist, cfg, use_mock, scan_cache, workers=args.workers)

    # ── 保存缓存 ─────────────────────────────────────────────────
    if not use_mock:
        _save_scan_cache(cache_file, scan_cache, from_demo=use_mock)

    # ── 生成报告 ─────────────────────────────────────────────────
    scan_dt  = datetime.now()
    md_text  = results_to_markdown(results, cfg, scan_dt, use_mock)

    out_dir.mkdir(parents=True, exist_ok=True)
    mode = "a" if (args.append and out_file.exists()) else "w"
    with open(out_file, mode, encoding="utf-8") as f:
        if mode == "a":
            f.write("\n\n---\n\n")
        f.write(md_text)

    action = "追加到" if mode == "a" else "已保存"
    print(f"\n✅ Markdown 报告{action}: {out_file}")

    # ── Excel 输出 ───────────────────────────────────────────────
    if args.excel:
        xlsx_file = out_dir / f"{date_str}_technical_scan.xlsx"
        results_to_excel(results, xlsx_file)

    # ── 终端摘要 ─────────────────────────────────────────────────
    valid   = [r for r in results if not r.get("error")]
    er      = sum(1 for r in results if r.get("error"))
    gc      = sum(1 for r in valid if r.get("golden_cross"))
    dc      = sum(1 for r in valid if r.get("death_cross"))
    hs      = sum(1 for r in valid if r.get("score", 0) >= 60)
    mb      = sum(1 for r in valid if r.get("multi_buy"))

    print(f"\n{'─'*58}")
    print(f"  扫描完成  {date_str}   共 {len(results)} 只（失败 {er} 只）")
    print(f"  🟢 黄金交叉: {gc}   🔴 死亡交叉: {dc}")
    print(f"  ⭐ 多指标共振: {mb}   🏅 高分≥60: {hs}")
    print(f"{'─'*58}\n")


if __name__ == "__main__":
    main()
