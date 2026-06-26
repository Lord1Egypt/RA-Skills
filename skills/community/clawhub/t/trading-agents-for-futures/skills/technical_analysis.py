"""技术面分析 Skill

封装技术指标计算和规则驱动的技术面分析，为期货交易决策提供技术支持。
纯本地计算，不依赖任何外部模块。
"""

from __future__ import annotations

from typing import Dict, Any, Optional
import datetime as _dt

import numpy as np
import pandas as _pd_global

from core.core_engine import AnalysisResult


def _calc_sma(series, period):
    """简单移动平均"""
    return series.rolling(window=period).mean()


def _calc_ema(series, period):
    """指数移动平均"""
    return series.ewm(span=period, adjust=False).mean()


def _calc_macd(series, fast=12, slow=26, signal=9):
    """MACD"""
    ema_fast = _calc_ema(series, fast)
    ema_slow = _calc_ema(series, slow)
    macd_line = ema_fast - ema_slow
    signal_line = _calc_ema(macd_line, signal)
    hist = macd_line - signal_line
    return macd_line, signal_line, hist


def _calc_rsi(series, period=14):
    """RSI"""
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def _calc_bollinger(series, period=20, std=2):
    """布林带"""
    middle = _calc_sma(series, period)
    std_dev = series.rolling(window=period).std()
    upper = middle + std * std_dev
    lower = middle - std * std_dev
    return upper, middle, lower


def _calc_atr(df, period=14):
    """ATR"""
    high = df["最高"]
    low = df["最低"]
    prev_close = df["收盘"].shift(1)
    tr1 = high - low
    tr2 = abs(high - prev_close)
    tr3 = abs(low - prev_close)
    tr = _pd_global.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()


def run(
    symbol: str,
    ohlcv_data: Optional[Dict[str, Any]] = None,
    config: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> AnalysisResult:
    """执行技术面分析"""
    import pandas as pd
    import numpy as np

    result = AnalysisResult(skill_name="technical_analysis")

    try:
        if ohlcv_data is None:
            result.add_warning("未提供OHLCV数据")
            return result

        df = pd.DataFrame(ohlcv_data)
        required_cols = ["收盘", "最高", "最低", "开盘"]
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            rename_map = {
                "close": "收盘", "high": "最高", "low": "最低", "open": "开盘",
                "volume": "成交量", "open_interest": "持仓量",
            }
            df = df.rename(columns=rename_map)
            missing = [c for c in required_cols if c not in df.columns]

        if missing:
            result.add_warning(f"缺少必要列: {missing}")
            return result

        for col in required_cols + ["成交量", "持仓量"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=required_cols).reset_index(drop=True)
        if len(df) < 20:
            result.add_warning("数据量不足(少于20条)")
            return result

        close = df["收盘"]
        volume = df["成交量"] if "成交量" in df.columns else None

        # 均线
        df["MA5"] = _calc_sma(close, 5)
        df["MA20"] = _calc_sma(close, 20)
        df["MA60"] = _calc_sma(close, 60)
        df["EMA20"] = _calc_ema(close, 20)
        # RSI
        df["RSI14"] = _calc_rsi(close, 14)
        # MACD
        df["MACD"], df["MACD_Signal"], df["MACD_Hist"] = _calc_macd(close)
        # 布林带
        df["BB_Upper"], df["BB_Middle"], df["BB_Lower"] = _calc_bollinger(close)
        # ATR
        df["ATR14"] = _calc_atr(df, 14)
        # 成交量均值
        if volume is not None:
            df["VOL_MA20"] = _calc_sma(volume, 20)
        # 持仓量变化
        if "持仓量" in df.columns:
            df["OI_delta"] = df["持仓量"].diff()

        last = df.iloc[-1]
        indicators = {}
        for col in ["MA5", "MA20", "MA60", "EMA20"]:
            if col in df.columns and pd.notna(last[col]):
                indicators[col] = float(last[col])
        for col in ["MACD", "MACD_Signal", "MACD_Hist", "RSI14"]:
            if col in df.columns and pd.notna(last[col]):
                indicators[col] = float(last[col])
        for col in ["BB_Upper", "BB_Middle", "BB_Lower", "ATR14"]:
            if col in df.columns and pd.notna(last[col]):
                indicators[col] = float(last[col])
        if "VOL_MA20" in df.columns and pd.notna(last.get("VOL_MA20")):
            indicators["VOL_MA20"] = float(last["VOL_MA20"])
        if "OI_delta" in df.columns and pd.notna(last.get("OI_delta")):
            indicators["OI_delta"] = float(last["OI_delta"])
        indicators["close"] = float(last["收盘"])

        if len(df) >= 20:
            recent = df.tail(20)
            indicators["trend_20d"] = "up" if recent["收盘"].iloc[-1] > recent["收盘"].iloc[0] else "down"
            indicators["change_20d_pct"] = float(
                (recent["收盘"].iloc[-1] - recent["收盘"].iloc[0]) / recent["收盘"].iloc[0] * 100
            )

        result.add_data("indicators", indicators)
        if not indicators:
            indicators["soft_data_hint"] = (
                f"API 未返回 {symbol} 技术面数据。请 AI Agent 搜索补全："
                f"'{symbol} 期货 K线 行情 均线 MACD {_dt.datetime.now().strftime('%Y年%m月%d日')}'"
            )
            indicators["search_actions"] = [
                {"query": f"{symbol} 期货 主力合约 行情 OHLCV {_dt.datetime.now().strftime('%Y年%m月%d日')}", "source": "web", "priority": "high"},
                {"query": f"{symbol} 主力合约 技术分析 MA RSI MACD", "source": "web", "priority": "medium"},
            ]
        result.add_data("data_date", str(df.iloc[-1].get("日期", _dt.datetime.now().date())))
        result.add_data("data_points", len(df))

        signal = _rule_based_signal(indicators)
        result.add_data("rule_based_signal", signal)
        result.add_data("bullish_signals_list", signal.get("bullish_signals_list", []))
        result.add_data("bearish_signals_list", signal.get("bearish_signals_list", []))
        result.set_signal(signal.get("direction", "neutral"), signal.get("confidence", 0.3))
        result.bullets.extend(signal.get("signals", []) + signal.get("details", []))

    except Exception as e:
        result.add_error(f"技术面分析出错: {e}")

    return result


def _rule_based_signal(indicators: Dict[str, Any]) -> Dict[str, Any]:
    score = 0
    signals = []
    details = []

    close = indicators.get("close")
    ma20 = indicators.get("MA20")
    ma60 = indicators.get("MA60")

    if close and ma20:
        if close > ma20:
            score += 1
            if ma60 and close > ma60 and ma20 > ma60:
                signals.append("均线多头排列")
                details.append(f"价格({close:.0f}) > MA20({ma20:.0f}) > MA60({ma60:.0f})，趋势强势")
            else:
                signals.append("价格在MA20均线上方")
                details.append(f"价格({close:.0f})在MA20({ma20:.0f})上方，多头格局")
        else:
            score -= 1
            if ma60 and close < ma60:
                signals.append("均线空头排列")
                details.append(f"价格({close:.0f}) < MA20({ma20:.0f}) < MA60({ma60:.0f})，趋势弱势")
            else:
                signals.append("价格在MA20均线下方")
                details.append(f"价格({close:.0f})在MA20({ma20:.0f})下方，空头格局")

    macd = indicators.get("MACD")
    macd_signal = indicators.get("MACD_Signal")
    if macd is not None and macd_signal is not None:
        if macd > macd_signal:
            score += 1
            signals.append("MACD金叉")
            details.append(f"MACD({macd:.2f}) > Signal({macd_signal:.2f})，动能偏多")
        elif macd < macd_signal:
            score -= 1
            signals.append("MACD死叉")
            details.append(f"MACD({macd:.2f}) < Signal({macd_signal:.2f})，动能偏空")

    rsi = indicators.get("RSI14")
    if rsi is not None:
        if rsi > 80:
            score -= 1
            signals.append(f"RSI极度超买({rsi:.1f})")
            details.append(f"RSI(14)={rsi:.1f}>80，极度超买")
        elif rsi > 70:
            signals.append(f"RSI超买({rsi:.1f})")
            details.append(f"RSI(14)={rsi:.1f}>70，超买区域")
        elif rsi < 20:
            score += 1
            signals.append(f"RSI极度超卖({rsi:.1f})")
            details.append(f"RSI(14)={rsi:.1f}<20，极度超卖")
        elif rsi < 30:
            score += 1
            signals.append(f"RSI超卖({rsi:.1f})")
            details.append(f"RSI(14)={rsi:.1f}<30，超卖区域")

    bb_upper = indicators.get("BB_Upper")
    bb_lower = indicators.get("BB_Lower")
    if close and bb_upper and bb_lower:
        if close >= bb_upper:
            score -= 1
            signals.append("价格触及布林带上轨")
            details.append(f"价格触及上轨({bb_upper:.0f})，回调压力")
        elif close <= bb_lower:
            score += 1
            signals.append("价格触及布林带下轨")
            details.append(f"价格触及下轨({bb_lower:.0f})，反弹动力")

    atr = indicators.get("ATR14")
    if atr and close:
        details.append(f"ATR(14)={atr:.1f}，波幅约{atr/close*100:.1f}%")

    oi_delta = indicators.get("OI_delta")
    if oi_delta is not None:
        if oi_delta > 0:
            details.append(f"持仓增加({oi_delta:+.0f})，资金入场")
        elif oi_delta < 0:
            details.append(f"持仓减少({oi_delta:+.0f})，资金离场")

    trend = indicators.get("trend_20d")
    change_pct = indicators.get("change_20d_pct")
    if trend == "up" and change_pct:
        score += 1
        signals.append(f"近20日趋势向上(+{change_pct:.1f}%)")
        details.append(f"近20日累计上涨{change_pct:.1f}%")
    elif trend == "down" and change_pct:
        score -= 1
        signals.append(f"近20日趋势向下({change_pct:.1f}%)")
        details.append(f"近20日累计下跌{abs(change_pct):.1f}%")

    bullish_signals = sum(1 for s in signals if any(kw in s for kw in ["金叉", "超卖", "多头排列", "趋势向上", "反弹", "上方"]))
    bearish_signals = sum(1 for s in signals if any(kw in s for kw in ["死叉", "超买", "空头排列", "趋势向下", "回调", "下方"]))

    if score > 1:
        direction = "bullish"
        confidence = min(0.65, 0.35 + score * 0.08)
    elif score > 0:
        direction = "bullish"
        confidence = 0.5
    elif score < -1:
        direction = "bearish"
        confidence = min(0.65, 0.35 + abs(score) * 0.08)
    elif score < 0:
        direction = "bearish"
        confidence = 0.5
    else:
        direction = "neutral"
        confidence = 0.3

    if bullish_signals > 0 and bearish_signals > 0:
        details.append(f"⚠️ 多空信号交织({bullish_signals}多vs{bearish_signals}空)，价格处于转折临界区域，方向判断需谨慎")
        confidence = max(confidence - 0.15, 0.15)

    bullish_signals_list = [s for s in signals + details if any(kw in s for kw in ["金叉", "超卖", "多头排列", "趋势向上", "反弹", "上方"])]
    bearish_signals_list = [s for s in signals + details if any(kw in s for kw in ["死叉", "超买", "空头排列", "趋势向下", "回调", "下方"])]

    return {
        "direction": direction, "confidence": confidence, "score": score,
        "signals": signals + details,
        "bullish_signals_list": bullish_signals_list,
        "bearish_signals_list": bearish_signals_list,
    }
