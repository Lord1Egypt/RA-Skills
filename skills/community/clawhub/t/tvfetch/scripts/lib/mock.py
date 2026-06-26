"""
Fixture-based mock mode for offline testing and CI.

When --mock is passed to any script, data is loaded from fixtures/ instead
of making real network calls. This allows the skill to work without internet.

Fixture naming convention:
  {action}_{symbol_safe}_{timeframe}_{N}bars.json
  {action}_{symbol_safe}_{timeframe}.json
  {action}_default.json

Symbol safe: replace ":" with "_", lowercase (e.g., binance_btcusdt)
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone

from tvfetch.models import Bar, FetchResult

# Default fixtures dir is relative to the skill root
_SKILL_DIR = Path(__file__).resolve().parent.parent.parent
FIXTURES_DIR = _SKILL_DIR / "fixtures"


def _symbol_safe(symbol: str) -> str:
    """Convert EXCHANGE:TICKER to exchange_ticker for filenames."""
    return symbol.replace(":", "_").lower()


def find_fixture(
    symbol: str,
    timeframe: str,
    bars: int,
    action: str = "fetch",
    fixtures_dir: Path | None = None,
) -> Path | None:
    """
    Find the best matching fixture file. Tries exact match first,
    then without bar count, then default.
    """
    fdir = fixtures_dir or FIXTURES_DIR
    if not fdir.is_dir():
        return None

    safe = _symbol_safe(symbol)

    # 1. Exact match
    exact = fdir / f"{action}_{safe}_{timeframe}_{bars}bars.json"
    if exact.is_file():
        return exact

    # 2. Without bar count
    partial = fdir / f"{action}_{safe}_{timeframe}.json"
    if partial.is_file():
        return partial

    # 2b. Any bar count for same symbol+timeframe (glob)
    import glob
    pattern = str(fdir / f"{action}_{safe}_{timeframe}_*bars.json")
    matches = sorted(glob.glob(pattern))
    if matches:
        return Path(matches[0])

    # 3. Symbol only
    sym_only = fdir / f"{action}_{safe}.json"
    if sym_only.is_file():
        return sym_only

    # 4. Default
    default = fdir / f"{action}_default.json"
    if default.is_file():
        return default

    return None


def load_fixture(
    symbol: str,
    timeframe: str,
    bars: int,
    action: str = "fetch",
    fixtures_dir: Path | None = None,
) -> FetchResult | None:
    """
    Load a fixture file and return a FetchResult, or None if no fixture found.
    """
    path = find_fixture(symbol, timeframe, bars, action, fixtures_dir)
    if path is None:
        return None

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    bar_list = []
    for b in data.get("bars", []):
        bar_list.append(Bar(
            timestamp=datetime.fromtimestamp(b["ts"], tz=timezone.utc),
            open=b["o"],
            high=b["h"],
            low=b["l"],
            close=b["c"],
            volume=b["v"],
        ))

    # Trim to requested bar count
    if len(bar_list) > bars:
        bar_list = bar_list[-bars:]

    return FetchResult(
        symbol=data.get("symbol", symbol),
        timeframe=data.get("timeframe", timeframe),
        bars=bar_list,
        source="mock",
        auth_mode="anonymous",
    )


def create_fixture_json(result: FetchResult) -> dict:
    """Convert a FetchResult to fixture JSON format (for generating fixtures)."""
    return {
        "symbol": result.symbol,
        "timeframe": result.timeframe,
        "source": "mock",
        "auth_mode": result.auth_mode,
        "bars": [
            {
                "ts": int(b.timestamp.timestamp()),
                "o": b.open,
                "h": b.high,
                "l": b.low,
                "c": b.close,
                "v": b.volume,
            }
            for b in sorted(result.bars, key=lambda x: x.timestamp)
        ],
    }
