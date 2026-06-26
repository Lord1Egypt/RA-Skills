"""Adapter contract: all providers return the same normalized collect dict."""

from __future__ import annotations

from typing import Any

REQUIRED_META_KEYS = frozenset({"market", "source_used", "symbol_resolved"})


def attach_adapter_meta(
    data: dict[str, Any],
    *,
    market: str,
    source_used: str,
    symbol_resolved: str,
    fallback_level: int = 0,
) -> dict[str, Any]:
    """Mutate collect payload with routing provenance (single schema for personas)."""
    meta = data.setdefault("adapter_meta", {})
    meta["market"] = market
    meta["source_used"] = source_used
    meta["symbol_resolved"] = symbol_resolved
    meta["fallback_level"] = fallback_level
    return data
