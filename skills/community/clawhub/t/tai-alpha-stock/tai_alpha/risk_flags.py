"""Structured risk flags from collect fields and headline keyword scans."""

from __future__ import annotations

from typing import Any

from tai_alpha.config_load import load_risk_keywords


def compute_risk_flags(
    data: dict[str, Any],
    *,
    deep: bool = False,
) -> list[str]:
    """
    Derive human-readable risk flags from normalized collect data.

    ``deep`` includes geopolitical keyword scans on news titles (UZI-style depth).
    """
    if data.get("error"):
        return []

    flags: list[str] = []
    rsi = float(data.get("rsi", 50))
    if rsi > 75:
        flags.append("RSI_overbought")

    vix = float(data.get("vix", 20))
    if vix > 25:
        flags.append("VIX_elevated")

    shorts = float(data.get("shortRatio", 0.1))
    if shorts > 0.15:
        flags.append("High_short_interest")

    fg = int(data.get("fear_greed", 50))
    if fg > 80:
        flags.append("FearGreed_elevated")

    kw = load_risk_keywords()
    crisis = kw.get("crisis_keywords", [])
    geo = kw.get("geopolitical_keywords", []) if deep else []

    news = data.get("news") or []
    titles = " ".join(str(n) for n in news).lower()
    for word in crisis:
        if word.lower() in titles:
            flags.append(f"News_keyword:{word.replace(' ', '_')}")
    for word in geo:
        if word.lower() in titles:
            flags.append(f"Geo_keyword:{word.replace(' ', '_')}")

    # De-duplicate while preserving order
    seen: set[str] = set()
    ordered: list[str] = []
    for f in flags:
        if f not in seen:
            seen.add(f)
            ordered.append(f)
    return ordered
