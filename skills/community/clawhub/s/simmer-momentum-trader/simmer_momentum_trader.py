#!/usr/bin/env python3
"""
Simmer Momentum Trader
Momentum-based prediction market trading skill for Simmer.
Default signal: probability divergence from recent average.
Remix by replacing calculate_signal() with your own alpha.
"""

import os
import sys
import time
import argparse
from typing import Optional

try:
    from simmer_sdk import SimmerClient
except ImportError:
    print("ERROR: simmer-sdk not installed. Run: pip install simmer-sdk")
    sys.exit(1)

# ── Config ──────────────────────────────────────────────────────────────────

SKILL_SLUG = "simmer-momentum-trader"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"
DIVERGENCE_THRESHOLD = float(os.environ.get("DIVERGENCE_THRESHOLD", "0.08"))
TRADE_AMOUNT = float(os.environ.get("TRADE_AMOUNT", "5.0"))
MARKET_IDS = [m.strip() for m in os.environ.get("MARKET_IDS", "").split(",") if m.strip()]

_client = None


def get_client() -> SimmerClient:
    global _client
    if _client is None:
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue="polymarket",
        )
    return _client


# ── Signal ──────────────────────────────────────────────────────────────────

def calculate_signal(market_id: str) -> Optional[dict]:
    """
    Default signal: probability divergence from recent average.

    Returns:
        {"side": "yes"|"no", "divergence": float, "reasoning": str} or None

    Remix this function to implement your own strategy.
    """
    client = get_client()

    try:
        context = client.get_market_context(market_id)
    except Exception as e:
        print(f"  Could not fetch context for {market_id}: {e}")
        return None

    market = context.get("market", {})
    current_prob = market.get("probability")
    if current_prob is None:
        print(f"  No probability data for {market_id}")
        return None

    # Use available price history or context data for momentum
    # In practice, you'd fetch historical prices; here we use the context
    # endpoint's built-in signals if available
    trading = context.get("trading", {})
    edge = context.get("edge_analysis", {})

    # Simple divergence: if edge analysis suggests different probability
    edge_prob = edge.get("estimated_probability")
    if edge_prob is None:
        # Fallback: compare current prob to a neutral 0.5 baseline
        divergence = current_prob - 0.5
    else:
        divergence = current_prob - edge_prob

    abs_div = abs(divergence)

    if abs_div < DIVERGENCE_THRESHOLD:
        return None

    # If current prob is HIGH and above our estimate → market might be
    # overpriced → but momentum says it could continue. We buy the side
    # with momentum (trend following).
    if divergence > 0:
        side = "yes"
        reasoning = (
            f"Momentum signal: probability {current_prob:.2f} diverges +{divergence:.2f} "
            f"above estimate {edge_prob or 0.5:.2f} (threshold: {DIVERGENCE_THRESHOLD})"
        )
    else:
        side = "no"
        reasoning = (
            f"Momentum signal: probability {current_prob:.2f} diverges {divergence:.2f} "
            f"below estimate {edge_prob or 0.5:.2f} (threshold: {DIVERGENCE_THRESHOLD})"
        )

    return {"side": side, "divergence": divergence, "reasoning": reasoning}


# ── Context checks ─────────────────────────────────────────────────────────

def should_skip_market(market_id: str, my_probability: float = None) -> Optional[str]:
    """
    Check market context for flip-flop warnings, slippage, and edge.
    Returns reason string if we should skip, None if OK to trade.
    """
    client = get_client()
    try:
        params = {}
        if my_probability is not None:
            params["my_probability"] = my_probability
        context = client.get_market_context(market_id, **params)
    except Exception:
        return None  # Can't check context, proceed with caution

    # Flip-flop detection
    trading = context.get("trading", {})
    flip_flop = trading.get("flip_flop_warning")
    if flip_flop and "SEVERE" in flip_flop:
        return f"Flip-flop warning: {flip_flop}"

    # Slippage check
    slippage = context.get("slippage", {})
    if slippage.get("slippage_pct", 0) > 0.15:
        return f"Slippage too high: {slippage.get('slippage_pct'):.1%}"

    # Edge analysis
    edge = context.get("edge_analysis", {})
    if edge.get("recommendation") == "HOLD":
        return "Edge below threshold — HOLD recommended"

    return None


# ── Execution ───────────────────────────────────────────────────────────────

def execute_trade(market_id: str, signal: dict, live: bool = False):
    """Execute a trade based on signal. Defaults to dry-run."""
    client = get_client()

    mode = "LIVE" if live else "DRY-RUN"
    print(f"[{mode}] Market {market_id}: {signal['side'].upper()} ${TRADE_AMOUNT:.2f}")
    print(f"  Reasoning: {signal['reasoning']}")

    if not live:
        print("  (Dry run — no order placed. Pass --live to execute.)")
        return

    try:
        result = client.trade(
            market_id=market_id,
            side=signal["side"],
            amount=TRADE_AMOUNT,
            source=TRADE_SOURCE,
            skill_slug=SKILL_SLUG,
            reasoning=signal["reasoning"],
        )
        print(f"  Order placed: {result}")
    except Exception as e:
        print(f"  Trade failed: {e}")


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Simmer Momentum Trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades (default: dry-run)")
    parser.add_argument("--market", type=str, help="Single market ID to check (overrides MARKET_IDS env)")
    parser.add_argument("--threshold", type=float, default=DIVERGENCE_THRESHOLD,
                        help=f"Divergence threshold (default: {DIVERGENCE_THRESHOLD})")
    args = parser.parse_args()

    global DIVERGENCE_THRESHOLD
    DIVERGENCE_THRESHOLD = args.threshold

    market_ids = [args.market] if args.market else MARKET_IDS
    if not market_ids:
        print("No markets specified. Set MARKET_IDS env var or use --market.")
        sys.exit(1)

    print(f"Simmer Momentum Trader — monitoring {len(market_ids)} market(s)")
    print(f"Threshold: {DIVERGENCE_THRESHOLD}, Amount: ${TRADE_AMOUNT:.2f}")
    print()

    for market_id in market_ids:
        print(f"Market: {market_id}")

        # Check context safeguards
        skip_reason = should_skip_market(market_id)
        if skip_reason:
            print(f"  SKIPPED: {skip_reason}")
            print()
            continue

        # Calculate signal
        signal = calculate_signal(market_id)
        if signal is None:
            print("  No signal — below divergence threshold")
            print()
            continue

        # Execute
        execute_trade(market_id, signal, live=args.live)
        print()


if __name__ == "__main__":
    main()
