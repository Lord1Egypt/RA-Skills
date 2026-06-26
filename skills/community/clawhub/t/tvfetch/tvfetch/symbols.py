"""Symbol search and validation using TradingView's REST search API."""

from __future__ import annotations

import logging
from typing import Literal

import httpx

from tvfetch.exceptions import TvConnectionError
from tvfetch.models import SymbolInfo

log = logging.getLogger(__name__)

_SEARCH_URL = "https://symbol-search.tradingview.com/symbol_search/v3/"
_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Origin": "https://www.tradingview.com",
}

SymbolType = Literal["", "stock", "futures", "forex", "crypto", "index", "bond", "cfd"]


def search(
    query: str,
    exchange: str = "",
    symbol_type: SymbolType = "",
    limit: int = 20,
) -> list[SymbolInfo]:
    """
    Search TradingView for symbols matching the query.

    Args:
        query:       Search string, e.g. "bitcoin", "AAPL", "EURUSD"
        exchange:    Optional exchange filter, e.g. "BINANCE", "NASDAQ"
        symbol_type: Optional asset type filter
        limit:       Max results to return (max 30)

    Returns:
        List of SymbolInfo objects, sorted by relevance.

    Example:
        >>> results = search("bitcoin", symbol_type="crypto")
        >>> print(results[0].symbol)
        BINANCE:BTCUSDT
    """
    params: dict = {
        "text": query,
        "hl": "1",
        "lang": "en",
        "domain": "production",
    }
    # Note: exchange and type filters are applied client-side — the API
    # returns 400 when these are passed as URL params in v3.
    if exchange:
        params["exchange"] = exchange

    try:
        resp = httpx.get(_SEARCH_URL, params=params, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise TvConnectionError(f"Symbol search failed: {exc}") from exc

    # Map user-friendly type names to what TV returns in responses
    _TYPE_MAP = {
        "crypto": {"spot", "crypto", "digital_asset"},
        "stock": {"stock", "common_stock", "dr", "fund", "structured"},
        "forex": {"forex"},
        "futures": {"futures"},
        "index": {"index"},
        "bond": {"bond"},
        "cfd": {"cfd"},
    }
    accepted_types = _TYPE_MAP.get(symbol_type, set()) if symbol_type else None

    results: list[SymbolInfo] = []
    for item in resp.json().get("symbols", []):
        sym = item.get("symbol", "")
        exch = item.get("exchange", "")
        item_type = item.get("type", "")

        # Client-side type filter
        if accepted_types and item_type not in accepted_types:
            continue

        sym_clean = _strip_html(sym)
        full = f"{exch}:{sym_clean}" if exch and ":" not in sym_clean else sym_clean
        results.append(SymbolInfo(
            symbol=full,
            description=_strip_html(item.get("description", "")),
            exchange=exch,
            type=item_type,
            currency=item.get("currency_code", ""),
        ))
        if len(results) >= limit:
            break

    return results


def _strip_html(text: str) -> str:
    """Remove HTML highlight tags that TV search returns."""
    return text.replace("<em>", "").replace("</em>", "")
