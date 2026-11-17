from __future__ import annotations

from statistics import mean

from models import Bar, StockQuote, StockScore


def moving_average(values: list[float], window: int) -> float | None:
    if len(values) < window:
        return None
    return mean(values[-window:])


def ema(values: list[float], span: int) -> list[float]:
    if not values:
        return []
    alpha = 2 / (span + 1)
    result = [values[0]]
    for value in values[1:]:
        result.append(alpha * value + (1 - alpha) * result[-1])
    return result


def calculate_macd(closes: list[float]) -> tuple[float, float, float]:
    if len(closes) < 35:
        return 0.0, 0.0, 0.0
    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)
    dif = [short - long for short, long in zip(ema12, ema26, strict=False)]
    dea = ema(dif, 9)
    macd = (dif[-1] - dea[-1]) * 2
    return dif[-1], dea[-1], macd


def calculate_volume_ratio(bars: list[Bar], current_volume: float) -> float:
    if len(bars) < 6:
        return 1.0
    base = [bar.volume for bar in bars[-6:-1] if bar.volume > 0]
    if not base:
        return 1.0
    return max(0.1, current_volume / mean(base))


def classify_flow(pct_chg: float, volume_ratio: float, score: float) -> tuple[str, int]:
    signal = pct_chg * 0.7 + (volume_ratio - 1) * 2.0 + (score - 50) / 20
    if signal >= 3:
        return "main_inflow", 2
    if signal >= 1:
        return "slight_inflow", 1
    if signal <= -3:
        return "main_outflow", -2
    if signal <= -1:
        return "slight_outflow", -1
    return "balanced", 0


FLOW_LABEL_CN = {
    "main_inflow": "\u4e3b\u529b\u6d41\u5165",
    "slight_inflow": "\u5fae\u6d41\u5165",
    "balanced": "\u5e73\u8861",
    "slight_outflow": "\u5fae\u6d41\u51fa",
    "main_outflow": "\u4e3b\u529b\u6d41\u51fa",
}


def heat_label(score: float) -> str:
    if score >= 70:
        return "strong"
    if score >= 55:
        return "recovering"
    if score >= 40:
        return "oscillating"
    if score >= 30:
        return "sluggish"
    return "weak"


HEAT_LABEL_CN = {
    "strong": "\u5f3a\u52bf",
    "recovering": "\u56de\u6696",
    "oscillating": "\u9707\u8361",
    "sluggish": "\u4f4e\u8ff7",
    "weak": "\u5f31\u52bf",
}


def score_stock(quote: StockQuote, bars: list[Bar]) -> StockScore:
    closes = [bar.close for bar in bars if bar.close > 0]
    price = quote.price
    score = 20.0
    details: list[str] = []

    ma5 = moving_average(closes, 5)
    ma10 = moving_average(closes, 10)
    ma20 = moving_average(closes, 20)
    ma60 = moving_average(closes, 60)

    if ma5 and ma10 and ma20 and ma5 > ma10 > ma20:
        score += 22
        details.append("MA多头排列+22")
    elif ma5 and ma20 and ma5 > ma20:
        score += 12
        details.append("MA5站上MA20+12")
    elif ma5 and ma20 and ma5 < ma20:
        score -= 6
        details.append("短线弱于MA20-6")

    if ma60:
        if price >= ma60:
            score += 12
            details.append("站上60日线+12")
        else:
            score -= 8
            details.append("跌破60日线-8")

    dif, dea, macd = calculate_macd(closes)
    if dif > dea and macd > 0:
        score += 15
        details.append("MACD金叉+15")
    elif dif < dea and macd < 0:
        score -= 8
        details.append("MACD走弱-8")

    volume_ratio = calculate_volume_ratio(bars, quote.volume)
    if volume_ratio >= 1.8 and quote.pct_chg > 0:
        score += 14
        details.append(f"放量上涨{volume_ratio:.1f}x+14")
    elif volume_ratio >= 1.2:
        score += 7
        details.append(f"温和放量{volume_ratio:.1f}x+7")
    elif volume_ratio < 0.6:
        score -= 4
        details.append(f"缩量{volume_ratio:.1f}x-4")

    if quote.pct_chg >= 5:
        score += 14
        details.append("强势涨幅+14")
    elif quote.pct_chg >= 2:
        score += 8
        details.append("红盘走强+8")
    elif quote.pct_chg > 0:
        score += 4
        details.append("红盘+4")
    elif quote.pct_chg <= -5:
        score -= 12
        details.append("跌幅偏大-12")
    elif quote.pct_chg <= -2:
        score -= 6
        details.append("绿盘走弱-6")

    if len(closes) >= 20:
        recent_high = max(closes[-20:])
        recent_low = min(closes[-20:])
        if recent_high > recent_low:
            position = (price - recent_low) / (recent_high - recent_low)
            if position >= 0.8:
                score += 8
                details.append("20日高位强势+8")
            elif position <= 0.25:
                score -= 5
                details.append("20日低位承压-5")

    final_score = round(max(0, min(100, score)), 1)
    flow_key, flow_level = classify_flow(quote.pct_chg, volume_ratio, final_score)
    if not details:
        details.append("数据不足，按基础行情评分")

    return StockScore(
        code=quote.code,
        name=quote.name,
        price=round(price, 2),
        pct_chg=round(quote.pct_chg, 2),
        score=final_score,
        flow_label=FLOW_LABEL_CN.get(flow_key, flow_key),
        flow_level=flow_level,
        volume_ratio=round(volume_ratio, 2),
        details=details,
    )
