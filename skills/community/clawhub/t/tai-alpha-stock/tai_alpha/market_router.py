"""Detect market (US/HK/CN) and normalize symbols for yfinance."""

from __future__ import annotations

import re
from typing import Literal

Market = Literal["us", "hk", "cn"]


def detect_market(ticker: str, explicit: str | None) -> Market:
    """
    Infer market from ticker shape; ``explicit`` overrides when not ``auto``.

    - ``.HK`` / 5-digit HK codes → hk
    - ``.SS`` / ``.SZ`` / 6-digit mainland → cn
    - else → us
    """
    if explicit and explicit.lower() != "auto":
        e = explicit.lower()
        if e in ("us", "hk", "cn"):
            return e  # type: ignore[return-value]
    t = ticker.strip().upper()
    if t.endswith(".HK"):
        return "hk"
    if t.endswith(".SS") or t.endswith(".SZ") or t.endswith(".SH"):
        return "cn"
    digits = re.sub(r"\D", "", t)
    if len(digits) == 5 and digits.isdigit():
        return "hk"
    if len(digits) == 6 and digits.isdigit():
        return "cn"
    return "us"


def normalize_for_yfinance(ticker: str, market: Market) -> str:
    """
    Return a yfinance-friendly symbol for the given market.

    HK: ``00700`` / ``700`` → ``0700.HK`` (4-digit code convention).
    CN: 6-digit → ``.SS`` (Shanghai 6/5/688…) or ``.SZ`` (else).
    US: return stripped upper symbol.
    """
    t = ticker.strip().upper()
    if t.endswith(".HK"):
        return t
    if t.endswith((".SS", ".SZ", ".SH")):
        return t.replace(".SH", ".SS") if t.endswith(".SH") else t
    if market == "hk":
        digits = re.sub(r"\D", "", t)
        if len(digits) >= 4:
            core = digits[-4:]
        elif digits:
            core = digits.zfill(4)[:4]
        else:
            return f"{t}.HK"
        return f"{core}.HK"
    if market == "cn":
        digits = re.sub(r"\D", "", t)
        if len(digits) != 6:
            return t
        if digits.startswith(("6", "5")) or digits.startswith("688"):
            return f"{digits}.SS"
        return f"{digits}.SZ"
    return t
