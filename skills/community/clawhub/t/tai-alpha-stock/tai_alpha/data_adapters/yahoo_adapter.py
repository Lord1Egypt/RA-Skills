"""Yahoo Finance via yfinance — US/HK/CN after symbol normalization."""

from __future__ import annotations

from typing import Any

from tai_alpha.collect import fetch_collect_data
from tai_alpha.data_adapters.base import attach_adapter_meta


def fetch_via_yahoo(
    symbol_for_yfinance: str,
    *,
    market: str,
    fast: bool = False,
    display_ticker: str | None = None,
) -> dict[str, Any]:
    """
    Fetch normalized collect data using ``fetch_collect_data`` (yfinance).

    ``symbol_for_yfinance`` must already be router-normalized (e.g. ``0700.HK``).
    ``display_ticker`` overrides stored ``ticker`` for reporting (user input).
    """
    data = fetch_collect_data(symbol_for_yfinance, fast=fast)
    if display_ticker:
        data["ticker"] = display_ticker.upper().strip()
    if not data.get("error"):
        attach_adapter_meta(
            data,
            market=market,
            source_used="yahoo_yfinance",
            symbol_resolved=symbol_for_yfinance,
            fallback_level=0,
        )
    else:
        data.setdefault("adapter_meta", {})
        data["adapter_meta"].update(
            {
                "market": market,
                "source_used": "yahoo_yfinance",
                "symbol_resolved": symbol_for_yfinance,
                "fallback_level": 0,
            }
        )
    return data
