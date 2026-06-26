"""
Builders for every outbound TradingView WebSocket message.
All functions return a ready-to-send framed string.
"""

from __future__ import annotations

import json
import random
import string

from tvfetch.core.protocol import encode_json


def _rand_session_id(prefix: str, length: int = 12) -> str:
    chars = string.ascii_lowercase + string.digits
    return f"{prefix}_" + "".join(random.choices(chars, k=length))


def new_chart_session() -> str:
    """Generate a unique chart session ID."""
    return _rand_session_id("cs")


def new_quote_session() -> str:
    """Generate a unique quote session ID."""
    return _rand_session_id("qs")


# ── Authentication ─────────────────────────────────────────────────────────────

def auth(token: str = "unauthorized_user_token") -> str:
    """Authenticate. Use 'unauthorized_user_token' for anonymous access."""
    return encode_json({"m": "set_auth_token", "p": [token]})


def locale(lang: str = "en", region: str = "US") -> str:
    return encode_json({"m": "set_locale", "p": [lang, region]})


# ── Chart session ──────────────────────────────────────────────────────────────

def chart_create_session(session_id: str) -> str:
    return encode_json({"m": "chart_create_session", "p": [session_id]})


def resolve_symbol(
    session_id: str,
    symbol: str,
    adjustment: str = "splits",
    extended_session: bool = False,
) -> str:
    sym_obj: dict = {"symbol": symbol, "adjustment": adjustment}
    if extended_session:
        sym_obj["session"] = "extended"
    # The symbol JSON is passed as a string prefixed with "="
    return encode_json({
        "m": "resolve_symbol",
        "p": [session_id, "sds_sym_1", f"={json.dumps(sym_obj)}"],
    })


def create_series(
    session_id: str,
    timeframe: str,
    bars: int = 300,
    series_key: str = "sds_1",
    series_ref: str = "s1",
    sym_key: str = "sds_sym_1",
) -> str:
    return encode_json({
        "m": "create_series",
        "p": [session_id, series_key, series_ref, sym_key, timeframe, bars],
    })


def request_more_data(
    session_id: str,
    bars: int = 5000,
    series_key: str = "sds_1",
) -> str:
    return encode_json({"m": "request_more_data", "p": [session_id, series_key, bars]})


def delete_session(session_id: str) -> str:
    return encode_json({"m": "chart_delete_session", "p": [session_id]})


# ── Quote session (real-time tick data) ────────────────────────────────────────

def quote_create_session(session_id: str) -> str:
    return encode_json({"m": "quote_create_session", "p": [session_id]})


def quote_add_symbols(session_id: str, *symbols: str) -> str:
    return encode_json({"m": "quote_add_symbols", "p": [session_id, *symbols]})


def quote_remove_symbols(session_id: str, *symbols: str) -> str:
    return encode_json({"m": "quote_remove_symbols", "p": [session_id, *symbols]})
