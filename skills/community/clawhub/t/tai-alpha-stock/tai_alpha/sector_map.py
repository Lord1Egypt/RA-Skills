"""Yahoo Finance sector name → liquid US sector ETF ticker."""

from __future__ import annotations

SECTOR_TO_ETF: dict[str, str] = {
    "Technology": "XLK",
    "Healthcare": "XLV",
    "Financial Services": "XLF",
    "Financial": "XLF",
    "Consumer Cyclical": "XLY",
    "Consumer Defensive": "XLP",
    "Industrials": "XLI",
    "Energy": "XLE",
    "Utilities": "XLU",
    "Real Estate": "XLRE",
    "Basic Materials": "XLB",
    "Communication Services": "XLC",
}


def sector_etf(sector: str | None) -> str | None:
    if not sector:
        return None
    return SECTOR_TO_ETF.get(sector)
