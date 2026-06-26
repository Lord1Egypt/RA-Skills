from __future__ import annotations

from dataclasses import dataclass
import math
import re
from typing import Callable

import pandas as pd


def normalize_text(text: str) -> str:
    lowered = text.lower()
    return re.sub(r"[\s\u3000,，。:：;；!！?？'\"“”‘’（）()\[\]【】/\\-]+", "", lowered)


def to_float(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return None
        return float(value)
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(value):
        return None
    return value


def round_if(value, digits: int = 2):
    number = to_float(value)
    if number is None:
        return None
    return round(number, digits)


def clamp_score(score: float) -> int:
    return max(1, min(5, int(round(score))))


def strength_label(score: int) -> str:
    mapping = {
        1: "很弱",
        2: "偏弱",
        3: "中性",
        4: "较强",
        5: "很强",
    }
    return mapping[score]


def latest_value(series: pd.Series):
    cleaned = pd.to_numeric(series, errors="coerce").dropna()
    if cleaned.empty:
        return None
    return float(cleaned.iloc[-1])


def rolling_mean(series: pd.Series, window: int):
    if len(series) < window:
        return None
    value = series.rolling(window).mean().iloc[-1]
    return to_float(value)


def rolling_std(series: pd.Series, window: int):
    if len(series) < window:
        return None
    value = series.rolling(window).std(ddof=0).iloc[-1]
    return to_float(value)


def percentage_change(series: pd.Series, periods: int):
    if len(series) <= periods:
        return None
    base = to_float(series.iloc[-periods - 1])
    latest = to_float(series.iloc[-1])
    if base in (None, 0) or latest is None:
        return None
    return (latest / base - 1) * 100


def prepare_price_frame(price_df: pd.DataFrame) -> pd.DataFrame:
    if price_df is None or price_df.empty:
        return pd.DataFrame()

    frame = price_df.copy()
    if "trade_date" in frame.columns:
        frame = frame.sort_values("trade_date")

    numeric_columns = ["open", "high", "low", "close", "vol", "amount", "change", "pct_chg"]
    for column in numeric_columns:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")

    for required in ["high", "low", "close"]:
        if required not in frame.columns:
            return pd.DataFrame()

    return frame.dropna(subset=["high", "low", "close"]).reset_index(drop=True)


@dataclass(frozen=True)
class IndicatorSpec:
    key: str
    title: str
    aliases: tuple[str, ...]
    description: str
    min_periods: int
    default_enabled: bool
    compute: Callable[[pd.DataFrame], dict]


INDICATOR_REGISTRY: dict[str, IndicatorSpec] = {}


def register_indicator(
    key: str,
    *,
    title: str,
    aliases: tuple[str, ...],
    description: str,
    min_periods: int = 30,
    default_enabled: bool = True,
):
    def decorator(func):
        INDICATOR_REGISTRY[key] = IndicatorSpec(
            key=key,
            title=title,
            aliases=aliases,
            description=description,
            min_periods=min_periods,
            default_enabled=default_enabled,
            compute=func,
        )
        return func

    return decorator


def list_indicator_specs() -> list[dict]:
    return [
        {
            "key": spec.key,
            "title": spec.title,
            "aliases": list(spec.aliases),
            "description": spec.description,
            "min_periods": spec.min_periods,
            "default_enabled": spec.default_enabled,
        }
        for spec in INDICATOR_REGISTRY.values()
    ]


def select_indicator_keys(query: str) -> list[str]:
    query_norm = normalize_text(query)
    explicit = []
    for spec in INDICATOR_REGISTRY.values():
        tokens = [spec.key, spec.title, *spec.aliases]
        if any(normalize_text(token) in query_norm for token in tokens if token):
            explicit.append(spec.key)
    if explicit:
        return list(dict.fromkeys(explicit))
    return [spec.key for spec in INDICATOR_REGISTRY.values() if spec.default_enabled]


def technical_analysis_keywords() -> list[str]:
    keywords = []
    for spec in INDICATOR_REGISTRY.values():
        keywords.extend(spec.aliases)
        keywords.append(spec.title)
        keywords.append(spec.key)
    keywords.extend(["技术分析", "交易观察", "盘面", "量价", "量能"])
    return list(dict.fromkeys(keywords))


@register_indicator(
    "ma_system",
    title="均线系统",
    aliases=("均线", "ma", "ma系统", "移动平均", "均线系统"),
    description="观察价格与 5/10/20/60/120/250 日均线的相对位置及排列。",
    min_periods=60,
)
def compute_ma_system(frame: pd.DataFrame) -> dict:
    closes = frame["close"]
    latest_close = latest_value(closes)
    ma_values = {window: rolling_mean(closes, window) for window in [5, 10, 20, 60, 120, 250]}
    score = 3.0
    notes = []

    ma20 = ma_values[20]
    ma60 = ma_values[60]
    ma120 = ma_values[120]

    if latest_close is not None and ma20 is not None:
        if latest_close > ma20:
            score += 0.6
        else:
            score -= 0.6
            notes.append("收盘价低于20日均线")
    if latest_close is not None and ma60 is not None:
        if latest_close > ma60:
            score += 0.7
        else:
            score -= 0.7
            notes.append("收盘价低于60日均线")
    if ma20 is not None and ma60 is not None and ma20 > ma60:
        score += 0.6
        notes.append("20日均线高于60日均线")
    elif ma20 is not None and ma60 is not None:
        score -= 0.6
        notes.append("20日均线低于60日均线")
    if ma60 is not None and ma120 is not None and ma60 > ma120:
        score += 0.3
    elif ma60 is not None and ma120 is not None:
        score -= 0.3

    if len(closes) >= 21:
        prev_ma5 = closes.iloc[:-1].rolling(5).mean().iloc[-1]
        prev_ma20 = closes.iloc[:-1].rolling(20).mean().iloc[-1]
        ma5 = ma_values[5]
        if to_float(prev_ma5) is not None and to_float(prev_ma20) is not None and ma5 is not None and ma20 is not None:
            if prev_ma5 <= prev_ma20 and ma5 > ma20:
                score += 0.4
                notes.append("5日均线刚上穿20日均线")
            elif prev_ma5 >= prev_ma20 and ma5 < ma20:
                score -= 0.4
                notes.append("5日均线刚下穿20日均线")

    final_score = clamp_score(score)
    conclusion = f"均线系统{strength_label(final_score)}。"
    if notes:
        conclusion = f"{conclusion} 主要依据：{'、'.join(notes)}。"
    return {
        "_score": final_score,
        "信号强弱": strength_label(final_score),
        "结论": conclusion,
        "指标": {f"MA{window}": round_if(value) for window, value in ma_values.items()},
    }


@register_indicator(
    "momentum",
    title="动量",
    aliases=("动量", "momentum", "涨跌动量", "趋势动量"),
    description="观察 5/10/20/60 日涨跌幅与动量延续情况。",
    min_periods=60,
)
def compute_momentum(frame: pd.DataFrame) -> dict:
    closes = frame["close"]
    ret5 = percentage_change(closes, 5)
    ret10 = percentage_change(closes, 10)
    ret20 = percentage_change(closes, 20)
    ret60 = percentage_change(closes, 60)

    score = 3.0
    notes = []
    if ret20 is not None:
        if ret20 >= 8:
            score += 0.8
            notes.append("20日动量较强")
        elif ret20 <= -8:
            score -= 0.8
            notes.append("20日动量偏弱")
    if ret60 is not None:
        if ret60 >= 15:
            score += 0.8
            notes.append("60日动量较强")
        elif ret60 <= -15:
            score -= 0.8
            notes.append("60日动量偏弱")
    if ret5 is not None and ret20 is not None:
        if ret5 > 0 and ret20 > 0:
            score += 0.3
        elif ret5 < 0 and ret20 < 0:
            score -= 0.3

    final_score = clamp_score(score)
    conclusion = f"价格动量{strength_label(final_score)}。"
    if notes:
        conclusion = f"{conclusion} 主要依据：{'、'.join(notes)}。"
    return {
        "_score": final_score,
        "信号强弱": strength_label(final_score),
        "结论": conclusion,
        "指标": {
            "5日涨跌幅": round_if(ret5),
            "10日涨跌幅": round_if(ret10),
            "20日涨跌幅": round_if(ret20),
            "60日涨跌幅": round_if(ret60),
        },
    }


def calculate_rsi(closes: pd.Series, window: int) -> pd.Series:
    delta = closes.diff()
    gains = delta.clip(lower=0)
    losses = (-delta).clip(lower=0)
    avg_gain = gains.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    avg_loss = losses.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    rs = avg_gain / avg_loss.replace(0, pd.NA)
    return 100 - (100 / (1 + rs))


@register_indicator(
    "rsi",
    title="RSI",
    aliases=("rsi", "相对强弱", "相对强弱指数"),
    description="使用 6/14 日 RSI 判断短中期超买超卖与强弱。",
    min_periods=20,
)
def compute_rsi(frame: pd.DataFrame) -> dict:
    closes = frame["close"]
    rsi6 = calculate_rsi(closes, 6)
    rsi14 = calculate_rsi(closes, 14)
    latest6 = latest_value(rsi6)
    latest14 = latest_value(rsi14)

    score = 3.0
    notes = []
    if latest14 is not None:
        if latest14 >= 70:
            score += 1.0
            notes.append("RSI14处于强势区间，但短线略热")
        elif latest14 >= 55:
            score += 0.6
            notes.append("RSI14处于偏强区间")
        elif latest14 <= 30:
            score -= 1.0
            notes.append("RSI14处于超卖区间")
        elif latest14 <= 45:
            score -= 0.6
            notes.append("RSI14处于偏弱区间")
    if latest6 is not None and latest14 is not None:
        if latest6 > latest14:
            score += 0.2
        else:
            score -= 0.2

    final_score = clamp_score(score)
    conclusion = f"RSI 信号{strength_label(final_score)}。"
    if notes:
        conclusion = f"{conclusion} 主要依据：{'、'.join(notes)}。"
    return {
        "_score": final_score,
        "信号强弱": strength_label(final_score),
        "结论": conclusion,
        "指标": {
            "RSI6": round_if(latest6),
            "RSI14": round_if(latest14),
        },
    }


@register_indicator(
    "kdj",
    title="KDJ",
    aliases=("kdj", "随机指标"),
    description="使用 9,3,3 KDJ 判断摆动强弱、金叉死叉与高低位状态。",
    min_periods=18,
)
def compute_kdj(frame: pd.DataFrame) -> dict:
    low_n = frame["low"].rolling(9, min_periods=9).min()
    high_n = frame["high"].rolling(9, min_periods=9).max()
    rsv = (frame["close"] - low_n) / (high_n - low_n).replace(0, pd.NA) * 100
    k = rsv.ewm(alpha=1 / 3, adjust=False, min_periods=9).mean()
    d = k.ewm(alpha=1 / 3, adjust=False, min_periods=9).mean()
    j = 3 * k - 2 * d

    latest_k = latest_value(k)
    latest_d = latest_value(d)
    latest_j = latest_value(j)
    prev_k = to_float(k.dropna().iloc[-2]) if len(k.dropna()) >= 2 else None
    prev_d = to_float(d.dropna().iloc[-2]) if len(d.dropna()) >= 2 else None

    score = 3.0
    notes = []
    if latest_k is not None and latest_d is not None:
        if latest_k > latest_d:
            score += 0.5
            notes.append("K线上穿D线")
        else:
            score -= 0.5
            notes.append("K线位于D线下方")
    if latest_k is not None:
        if latest_k >= 80:
            notes.append("KDJ位于高位")
            score += 0.2
        elif latest_k <= 20:
            notes.append("KDJ位于低位")
            score -= 0.2
    if prev_k is not None and prev_d is not None and latest_k is not None and latest_d is not None:
        if prev_k <= prev_d and latest_k > latest_d:
            score += 0.4
            notes.append("刚形成金叉")
        elif prev_k >= prev_d and latest_k < latest_d:
            score -= 0.4
            notes.append("刚形成死叉")

    final_score = clamp_score(score)
    conclusion = f"KDJ 信号{strength_label(final_score)}。"
    if notes:
        conclusion = f"{conclusion} 主要依据：{'、'.join(notes)}。"
    return {
        "_score": final_score,
        "信号强弱": strength_label(final_score),
        "结论": conclusion,
        "指标": {
            "K": round_if(latest_k),
            "D": round_if(latest_d),
            "J": round_if(latest_j),
        },
    }


@register_indicator(
    "bollinger",
    title="布林线",
    aliases=("布林线", "boll", "bollinger", "布林"),
    description="观察价格相对 20 日布林通道的位置与带宽。",
    min_periods=25,
)
def compute_bollinger(frame: pd.DataFrame) -> dict:
    closes = frame["close"]
    middle = closes.rolling(20, min_periods=20).mean()
    std = closes.rolling(20, min_periods=20).std(ddof=0)
    upper = middle + 2 * std
    lower = middle - 2 * std

    latest_close = latest_value(closes)
    latest_mid = latest_value(middle)
    latest_upper = latest_value(upper)
    latest_lower = latest_value(lower)
    band_width = None
    band_position = None
    if latest_mid not in (None, 0) and latest_upper is not None and latest_lower is not None:
        band_width = (latest_upper - latest_lower) / latest_mid * 100
    if latest_upper is not None and latest_lower is not None and latest_upper != latest_lower and latest_close is not None:
        band_position = (latest_close - latest_lower) / (latest_upper - latest_lower) * 100

    score = 3.0
    notes = []
    if latest_close is not None and latest_mid is not None:
        if latest_close > latest_mid:
            score += 0.5
            notes.append("价格位于布林中轨上方")
        else:
            score -= 0.5
            notes.append("价格位于布林中轨下方")
    if band_position is not None:
        if band_position >= 90:
            score += 0.5
            notes.append("价格接近上轨，短线偏热")
        elif band_position <= 10:
            score -= 0.5
            notes.append("价格接近下轨，短线偏弱")

    final_score = clamp_score(score)
    conclusion = f"布林线信号{strength_label(final_score)}。"
    if notes:
        conclusion = f"{conclusion} 主要依据：{'、'.join(notes)}。"
    return {
        "_score": final_score,
        "信号强弱": strength_label(final_score),
        "结论": conclusion,
        "指标": {
            "中轨": round_if(latest_mid),
            "上轨": round_if(latest_upper),
            "下轨": round_if(latest_lower),
            "带宽": round_if(band_width),
            "通道位置": round_if(band_position),
        },
    }


@register_indicator(
    "macd",
    title="MACD",
    aliases=("macd", "平滑异同平均", "指数平滑异同"),
    description="观察 DIF/DEA 与柱状图方向，判断趋势延续或拐点。",
    min_periods=35,
)
def compute_macd(frame: pd.DataFrame) -> dict:
    closes = frame["close"]
    ema12 = closes.ewm(span=12, adjust=False, min_periods=12).mean()
    ema26 = closes.ewm(span=26, adjust=False, min_periods=26).mean()
    dif = ema12 - ema26
    dea = dif.ewm(span=9, adjust=False, min_periods=9).mean()
    hist = (dif - dea) * 2

    latest_dif = latest_value(dif)
    latest_dea = latest_value(dea)
    latest_hist = latest_value(hist)
    prev_hist = to_float(hist.dropna().iloc[-2]) if len(hist.dropna()) >= 2 else None

    score = 3.0
    notes = []
    if latest_dif is not None and latest_dea is not None:
        if latest_dif > latest_dea:
            score += 0.7
            notes.append("DIF位于DEA上方")
        else:
            score -= 0.7
            notes.append("DIF位于DEA下方")
    if latest_hist is not None and prev_hist is not None:
        if latest_hist > 0 and latest_hist > prev_hist:
            score += 0.5
            notes.append("红柱放大")
        elif latest_hist < 0 and latest_hist < prev_hist:
            score -= 0.5
            notes.append("绿柱放大")

    final_score = clamp_score(score)
    conclusion = f"MACD 信号{strength_label(final_score)}。"
    if notes:
        conclusion = f"{conclusion} 主要依据：{'、'.join(notes)}。"
    return {
        "_score": final_score,
        "信号强弱": strength_label(final_score),
        "结论": conclusion,
        "指标": {
            "DIF": round_if(latest_dif, 3),
            "DEA": round_if(latest_dea, 3),
            "MACD柱": round_if(latest_hist, 3),
        },
    }


def run_indicator_suite(price_df: pd.DataFrame, query: str) -> dict:
    frame = prepare_price_frame(price_df)
    if frame.empty:
        return {
            "技术评分": 3.0,
            "技术强弱": "暂无",
            "已启用指标": [],
            "指标摘要": ["价格序列不足，无法生成技术指标。"],
            "指标明细": {},
            "数据限制": ["价格序列为空或缺少 high/low/close 字段。"],
        }

    results = {}
    summaries = []
    limitations = []
    scores = []
    selected_specs = []

    for key in select_indicator_keys(query):
        spec = INDICATOR_REGISTRY[key]
        selected_specs.append(spec)
        if len(frame.index) < spec.min_periods:
            limitations.append(f"{spec.title} 至少需要 {spec.min_periods} 个交易日数据。")
            results[spec.title] = {
                "信号强弱": "暂无",
                "结论": f"当前可用交易日不足 {spec.min_periods} 天，暂不计算。",
                "指标": {},
            }
            continue

        computed = spec.compute(frame)
        score = to_float(computed.pop("_score"))
        if score is not None:
            scores.append(score)
        results[spec.title] = computed
        if computed.get("结论"):
            summaries.append(f"{spec.title}：{computed['结论']}")

    technical_score = round(sum(scores) / len(scores), 2) if scores else 3.0
    return {
        "技术评分": technical_score,
        "技术强弱": strength_label(clamp_score(technical_score)),
        "已启用指标": [spec.title for spec in selected_specs],
        "指标摘要": summaries,
        "指标明细": results,
        "数据限制": limitations,
    }
