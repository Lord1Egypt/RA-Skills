#!/usr/bin/env python3
"""
Smart Money Signal Module for Polymarket Trading.

Fetches AI-generated trading signals from PolyClawster's public signals API
and converts them into standardized signal_data compatible with the existing
EV framework.

API: https://polyclawster.com/api/signals
Source: https://github.com/al1enjesus/polyclawster (MIT-0 License)

Usage:
    from smart_money_signal import fetch_smart_money_signals, get_signal_for_market

    # Fetch all signals above score threshold
    signals = fetch_smart_money_signals(min_score=7)

    # Get signal for a specific market slug
    signal = get_signal_for_market(signals, "will-bitcoin-hit-100k")
"""

import json
import os
import sys
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# Force UTF-8 stdout on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Default configuration
DEFAULT_API_URL = os.environ.get(
    "SMART_MONEY_API_URL", "https://polyclawster.com/api/signals"
)
DEFAULT_MIN_SCORE = float(os.environ.get("SMART_MONEY_MIN_SCORE", "7"))
REQUEST_TIMEOUT = 15  # seconds


def fetch_raw_signals(api_url=None):
    """
    Fetch raw signals from PolyClawster API.

    Args:
        api_url: API endpoint URL (defaults to DEFAULT_API_URL)

    Returns:
        List of signal dicts, or empty list on failure
    """
    url = api_url or DEFAULT_API_URL
    try:
        req = Request(url, headers={"User-Agent": "yh-polymarket-smart-money/1.0"})
        with urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok") and data.get("signals"):
                return data["signals"]
            return []
    except (HTTPError, URLError, json.JSONDecodeError, TimeoutError) as e:
        print(f"⚠️  Smart Money API error: {e}", file=sys.stderr)
        return []


def filter_signals(signals, min_score=None):
    """
    Filter signals by minimum score threshold.

    Args:
        signals: List of signal dicts from fetch_raw_signals()
        min_score: Minimum score threshold (0-10), defaults to DEFAULT_MIN_SCORE

    Returns:
        Filtered list of signals with score >= min_score
    """
    threshold = min_score if min_score is not None else DEFAULT_MIN_SCORE
    return [s for s in signals if float(s.get("score", 0)) >= threshold]


def normalize_signal(signal):
    """
    Convert a raw PolyClawster signal into standardized signal_data format
    compatible with the existing EV framework.

    Args:
        signal: Raw signal dict from PolyClawster API

    Returns:
        Normalized signal_data dict with standardized field names
    """
    score = float(signal.get("score", 0))
    price = float(signal.get("price", 0.5))
    side = signal.get("side", "YES").upper()

    # Convert 0-10 score to 0-1 confidence
    confidence = score / 10.0

    # Derive implied probability from side and price
    if side == "YES":
        implied_prob = price
    else:
        implied_prob = 1.0 - price

    return {
        # Core fields
        "smart_money_signal": "bullish" if side == "YES" else "bearish",
        "smart_money_score": score,
        "smart_money_confidence": round(confidence, 2),
        "smart_money_side": side,
        "smart_money_price": price,
        "smart_money_implied_prob": round(implied_prob, 4),
        # Market identification
        "smart_money_market": signal.get("market", ""),
        "smart_money_slug": signal.get("slug", ""),
        "smart_money_condition_id": signal.get("conditionId", ""),
        "smart_money_token_id_yes": signal.get("tokenIdYes", ""),
        "smart_money_token_id_no": signal.get("tokenIdNo", ""),
        # Metadata
        "smart_money_volume": float(signal.get("volume", 0)),
        "smart_money_source": signal.get("source", "polyclawster"),
        "smart_money_timestamp": signal.get("timestamp", ""),
        "smart_money_fetched_at": datetime.now(timezone.utc).isoformat(),
    }


def fetch_smart_money_signals(min_score=None, api_url=None):
    """
    Fetch and filter Smart Money signals, returning normalized signal_data.

    This is the main entry point for integrating Smart Money signals into
    the existing EV framework.

    Args:
        min_score: Minimum score threshold (0-10), defaults to DEFAULT_MIN_SCORE
        api_url: API endpoint URL, defaults to DEFAULT_API_URL

    Returns:
        List of normalized signal_data dicts
    """
    raw_signals = fetch_raw_signals(api_url)
    filtered = filter_signals(raw_signals, min_score)
    return [normalize_signal(s) for s in filtered]


def get_signal_for_market(signals, market_slug):
    """
    Find a Smart Money signal matching a specific market slug.

    Args:
        signals: List of normalized signal_data dicts
        market_slug: Market slug to match against

    Returns:
        Matching signal_data dict, or None if not found
    """
    if not market_slug:
        return None
    for signal in signals:
        if signal.get("smart_money_slug") == market_slug:
            return signal
    return None


def merge_signal_data(base_signal_data, smart_money_signal):
    """
    Merge Smart Money signal into existing EV framework signal_data.

    The Smart Money signal is added as supplementary data — it does NOT
    override the core EV edge or confidence values.

    Args:
        base_signal_data: Existing signal_data dict from EV framework
        smart_money_signal: Normalized Smart Money signal_data dict

    Returns:
        Merged signal_data dict with both EV and Smart Money data
    """
    if not smart_money_signal:
        return base_signal_data

    merged = dict(base_signal_data)
    merged.update(smart_money_signal)

    # Add combined confidence hint (weighted average, EV gets 70% weight)
    ev_confidence = base_signal_data.get("confidence", 0.5)
    sm_confidence = smart_money_signal.get("smart_money_confidence", 0.5)
    merged["combined_confidence"] = round(0.7 * ev_confidence + 0.3 * sm_confidence, 4)

    return merged


if __name__ == "__main__":
    # CLI: fetch and display signals
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch Smart Money signals from PolyClawster"
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=DEFAULT_MIN_SCORE,
        help=f"Minimum signal score (default: {DEFAULT_MIN_SCORE})",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--market", type=str, help="Filter by market slug")
    args = parser.parse_args()

    signals = fetch_smart_money_signals(min_score=args.min_score)

    if args.market:
        signals = [s for s in signals if args.market in s.get("smart_money_slug", "")]

    if args.json:
        print(json.dumps(signals, indent=2, ensure_ascii=False))
    elif signals:
        print(
            f"🐋 Smart Money Signals ({len(signals)} signals, score ≥ {args.min_score}):\n"
        )
        for s in signals:
            print(
                f"  [{s['smart_money_signal'].upper()}] Score: {s['smart_money_score']}/10"
            )
            print(f"  Market: {s['smart_money_market']}")
            print(f"  Side: {s['smart_money_side']} @ ${s['smart_money_price']:.3f}")
            print(f"  Volume: ${s['smart_money_volume']:,.0f}")
            print(f"  Slug: {s['smart_money_slug']}")
            print()
    else:
        print("📭 No Smart Money signals above threshold.")
