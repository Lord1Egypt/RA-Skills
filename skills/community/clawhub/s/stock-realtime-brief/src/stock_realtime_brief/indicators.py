"""
技术指标计算 — 均线、止损位、综合评分。
"""
from __future__ import annotations

from typing import Any


# ====== 均线 ======

def calc_ma(closes: list[float], n: int) -> float | None:
    """N 日均线"""
    if len(closes) < n:
        return None
    return round(sum(closes[-n:]) / n, 2)


def calc_all_mas(closes: list[float]) -> dict[str, float | None]:
    """常用均线: MA5/10/20/30"""
    return {
        "ma5": calc_ma(closes, 5),
        "ma10": calc_ma(closes, 10),
        "ma20": calc_ma(closes, 20),
        "ma30": calc_ma(closes, 30),
    }


def calc_drawdown(closes: list[float]) -> dict[str, Any] | None:
    """v2.7: 回撤分析
    
    返回:
        max_drawdown_pct: 最大回撤（全区间峰谷最大跨跌幅%）
        current_drawdown_pct: 当前回撤（现价距全局高点跨幅%）
        peak_price: 全局高点
        days_since_peak: 距高点多少交易日
        risk_level: 风险等级文本
    """
    if not closes or len(closes) < 2:
        return None
    try:
        peak = closes[0]
        max_dd = 0.0
        max_dd_peak = peak
        for c in closes[1:]:
            if c > peak:
                peak = c
            dd = (peak - c) / peak * 100
            if dd > max_dd:
                max_dd = dd
                max_dd_peak = peak
        peak_global = max(closes)
        peak_idx = closes.index(peak_global)
        current_dd = (peak_global - closes[-1]) / peak_global * 100
        days_since = len(closes) - 1 - peak_idx
        return {
            "max_drawdown_pct": round(max_dd, 2),
            "max_drawdown_peak": round(max_dd_peak, 2),
            "current_drawdown_pct": round(current_dd, 2),
            "peak_price": round(peak_global, 2),
            "days_since_peak": days_since,
            "risk_level": _drawdown_risk_level(current_dd),
        }
    except Exception:
        return None


def _drawdown_risk_level(dd_pct: float | None) -> str:
    """根据当前回撤幅度返回风险等级"""
    if dd_pct is None:
        return "?"
    if dd_pct < 5:
        return "🟢 新高附近"
    elif dd_pct < 10:
        return "🟢 健康回调"
    elif dd_pct < 20:
        return "🟡 中度回调"
    elif dd_pct < 30:
        return "🟠 深度回调"
    elif dd_pct < 50:
        return "🔴 重度下跌"
    else:
        return "⚫ 腰斩级"


def calc_history_features(df) -> dict[str, Any]:
    """从 K 线 DataFrame 提取关键指标"""
    if df is None or df.empty:
        return {}
    closes = df["收盘"].tolist()
    last = closes[-1] if closes else None
    mas = calc_all_mas(closes)
    # 40 日涨幅
    pct_40d = None
    if len(closes) >= 40:
        pct_40d = round((closes[-1] - closes[-40]) / closes[-40] * 100, 2)
    # 量能
    vols = df["成交量"].tolist() if "成交量" in df.columns else []
    avg_vol5 = round(sum(vols[-5:]) / 5, 0) if len(vols) >= 5 else None
    # v2.7: 回撤分析
    drawdown = calc_drawdown(closes)
    return {
        "last": last,
        **mas,
        "high_n": round(max(closes), 2) if closes else None,
        "low_n": round(min(closes), 2) if closes else None,
        "avg_vol5": avg_vol5,
        "pct_40d": pct_40d,
        "drawdown": drawdown,  # v2.7
    }


# ====== 止损位 ======

def derive_stop_loss(
    realtime: dict | None,
    hist: dict | None,
    is_heavy: bool = False,
    has_margin: bool = False,
    cost: float | None = None,
) -> dict[str, Any] | None:
    """三档硬止损 + 利润保护位

    规则:
    - 预警线 = MA5（强势）/ MA10（重仓）+ 利润保护位 取较高
    - 风控线 = MA10（一般）/ MA20（重仓）/ max(MA20, 成本-15%)（重仓亏损）
    - 清仓线 = MA20 / 成本-25%（亏损股）
    - 盈利 > 30% 提供利润保护位（现价回吐 25% 利润）
    - 融资股: 所有止损位上提 3%
    """
    last = realtime.get("price") if realtime else None
    if not last or not hist:
        return None
    ma5 = hist.get("ma5")
    ma10 = hist.get("ma10")
    ma20 = hist.get("ma20")

    pnl_pct = ((last - cost) / cost * 100) if cost else 0
    is_profit = pnl_pct > 30
    is_loss = pnl_pct < 0

    # 预警线
    warn = ma10 if is_heavy else ma5
    warn = warn or ma5 or ma10

    # 风控线
    if is_loss and is_heavy and cost:
        risk = max(round(cost * 0.85, 2), ma20 or 0)
    else:
        risk = ma20 or ma10

    # 清仓线
    if is_loss and cost:
        cut = round(cost * 0.75, 2)
    else:
        cut = ma20 or ma10
        if risk and cut and cut >= risk:
            cut = round(risk * 0.97, 2)

    # 利润保护位
    profit_lock = None
    if is_profit and cost:
        give_back = (last - cost) * 0.25
        profit_lock = round(last - give_back, 2)
        if warn and profit_lock > warn:
            warn = profit_lock

    # 融资股加 3%
    if has_margin:
        if warn:
            warn = round(warn * 1.03, 2)
        if risk:
            risk = round(risk * 1.03, 2)

    return {
        "warn_line": warn, "warn_action": "减 1/3",
        "risk_line": risk, "risk_action": "再减 1/3",
        "cut_line": cut, "cut_action": "清掉剩余",
        "profit_lock": profit_lock,
    }


def derive_operation_levels(realtime: dict | None, hist: dict | None) -> dict | None:
    """单股操作位 (模式 S 用)"""
    last = realtime.get("price") if realtime else None
    if not last or not hist:
        return None
    return {
        "介入位": hist.get("ma10"),
        "加仓位": hist.get("high_n"),
        "止损位": hist.get("ma20"),
        "止盈位_短线": round(last * 1.10, 2),
        "止盈位_波段": round(last * 1.20, 2),
    }


# ====== 综合评分 (模式 M 用) ======

def calc_composite_score(realtime: dict | None, hist: dict | None) -> float:
    """多股对比的轻量综合打分"""
    if not realtime or not hist or not hist.get("last"):
        return 0
    last = hist["last"]
    score = 0
    # 当日涨跌幅 ÷ 2
    pct = realtime.get("pct_change") or 0
    score += pct / 2
    # MA5 偏离度 × 1.5（短期强弱）
    if hist.get("ma5"):
        score += (last - hist["ma5"]) / hist["ma5"] * 100 * 1.5
    # MA20 偏离度 × 1（中期趋势）
    if hist.get("ma20"):
        score += (last - hist["ma20"]) / hist["ma20"] * 100
    # 量价共振分
    vol = realtime.get("volume") or 0
    avg_v5 = hist.get("avg_vol5") or 1
    vol_ratio = vol / avg_v5 if avg_v5 else 1
    if pct > 0 and vol_ratio > 1.2:
        score += 2
    elif pct < 0 and vol_ratio > 1.2:
        score -= 2
    return round(score, 2)


def judge_stance(realtime: dict | None, hist: dict | None) -> str:
    """态势速判（一句话）"""
    if not realtime or not hist:
        return "数据不足"
    last = realtime.get("price")
    pct = realtime.get("pct_change") or 0
    ma5, ma10, ma20 = hist.get("ma5"), hist.get("ma10"), hist.get("ma20")
    if not all([last, ma5, ma10, ma20]):
        return "数据不全，谨慎判断"
    if last > ma5 > ma10 > ma20:
        if pct > 3:
            return "🚀 强势上攻，多头排列加速"
        return "📈 多头排列，趋势向上"
    if last < ma5 < ma10 < ma20:
        if pct < -3:
            return "⚠️ 加速下跌，空头排列扩散"
        return "📉 空头排列，趋势向下"
    if last > ma20 and ma5 > ma10:
        return "🔵 中期向上，短期偏强"
    if abs(pct) < 1 and ma20 and abs(last - ma20) / ma20 < 0.02:
        return "⚪ 低波动震荡"
    return "🟡 多空交错，方向不明"
