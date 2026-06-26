"""Yahoo movers screener + optional CoinGecko trending (stdlib HTTP)."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any

_USER_AGENT = "TaiAlphaStock/1.0 (research)"

_YAHOO_SCREENER = (
    "https://query2.finance.yahoo.com/v1/finance/screener/predefined/saved"
    "?scrIds={scr}&count={count}"
)


def _fetch_json(url: str, timeout: float = 30.0) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
        raw = resp.read()
    return json.loads(raw.decode("utf-8"))


def yahoo_movers(scr_id: str, count: int = 15) -> list[dict[str, Any]]:
    """Return list of rows from Yahoo predefined screener."""
    url = _YAHOO_SCREENER.format(scr=scr_id, count=count)
    data = _fetch_json(url)
    quotes = data.get("finance", {}).get("result", [{}])[0].get("quotes", [])
    rows: list[dict[str, Any]] = []
    for q in quotes:
        rows.append(
            {
                "symbol": q.get("symbol"),
                "name": q.get("shortName") or q.get("longName"),
                "pct": q.get("regularMarketChangePercent"),
            }
        )
    return rows


def coingecko_trending() -> list[dict[str, Any]]:
    """Public CoinGecko trending (no API key)."""
    url = "https://api.coingecko.com/api/v3/search/trending"
    data = _fetch_json(url)
    coins = data.get("coins") or []
    out: list[dict[str, Any]] = []
    for c in coins[:15]:
        item = c.get("item") or {}
        out.append(
            {
                "symbol": item.get("symbol"),
                "name": item.get("name"),
                "rank": item.get("market_cap_rank"),
            }
        )
    return out


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser(description="Yahoo movers + optional crypto trending")
    p.add_argument(
        "--scr",
        default="day_gainers",
        help="Yahoo screener id (e.g. day_gainers, day_losers, most_actives)",
    )
    p.add_argument("--count", type=int, default=15, help="Rows per Yahoo screener")
    p.add_argument(
        "--with-crypto",
        action="store_true",
        help="Append CoinGecko trending coins (extra HTTP call)",
    )
    args = p.parse_args(argv)

    try:
        y = yahoo_movers(args.scr, count=args.count)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as e:
        print(json.dumps({"error": str(e), "yahoo": []}), file=sys.stderr)
        return 1

    payload: dict[str, Any] = {"yahoo_scr": args.scr, "yahoo": y}
    if args.with_crypto:
        try:
            payload["crypto_trending"] = coingecko_trending()
        except (
            urllib.error.URLError,
            TimeoutError,
            json.JSONDecodeError,
            OSError,
        ) as e:
            payload["crypto_error"] = str(e)
    print(json.dumps(payload, indent=2, default=str))
    return 0
