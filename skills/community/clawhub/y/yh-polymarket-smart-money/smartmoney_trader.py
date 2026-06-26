#!/usr/bin/env python3
"""
Smart Money Signal Trader for Polymarket.

Fetches whale/trader signals from PolyClawster API and filters Polymarket
markets where smart money is positioned, then executes trades via Simmer SDK.

Usage:
    python smartmoney_trader.py              # Dry run (show opportunities, no trades)
    python smartmoney_trader.py --live       # Execute real trades on Polymarket
    python smartmoney_trader.py --min-score 8  # Only high-confidence signals (score 8+)
    python smartmoney_trader.py --status    # Show current positions and signal status

Requires:
    SIMMER_API_KEY environment variable (from .env or shell)
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Force line-buffered stdout for cron/Docker environments
sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")

# Load .env from project root
try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).resolve().parent / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
except ImportError:
    pass

from smart_money_signal import (
    fetch_smart_money_signals,
    get_signal_for_market,
    DEFAULT_MIN_SCORE,
)
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:yh-polymarket-smart-money"
SKILL_SLUG = "yh-polymarket-smart-money"


def get_client():
    """Initialize Simmer client from environment."""
    api_key = os.environ.get("SIMMER_API_KEY")
    if not api_key:
        raise RuntimeError("SIMMER_API_KEY not set. Get one at https://simmer.markets/dashboard")
    venue = os.environ.get("TRADING_VENUE", "polymarket")
    return SimmerClient(api_key=api_key, venue=venue)


def check_live_mode():
    """Return True if --live flag is set."""
    return "--live" in sys.argv or os.environ.get("TRADING_VENUE") == "polymarket_live"


def format_signal(sig):
    """Format a smart money signal for console output."""
    emoji = "🐋" if sig["smart_money_signal"].upper() == "YES" else "🦈"
    return (
        f"{emoji} [{sig['smart_money_signal'].upper()}] "
        f"Score: {sig['smart_money_score']}/10 | "
        f"{sig['smart_money_market']} @ ${sig['smart_money_price']:.3f} | "
        f"Vol: ${sig['smart_money_volume']:,.0f}"
    )


def scan_and_trade(min_score: float, dry_run: bool = True):
    """
    Main scan-and-trade loop.

    1. Fetch smart money signals from PolyClawster
    2. Search Polymarket for matching markets
    3. Buy YES/NO based on smart money signal
    """
    print(f"\n{'='*60}")
    print(f"🐋 Smart Money Trader | Score ≥ {min_score} | {'LIVE' if not dry_run else 'DRY RUN'}")
    print(f"{'='*60}\n")

    # Step 1: Fetch whale signals
    print("[1/3] Fetching smart money signals from PolyClawster...")
    signals = fetch_smart_money_signals(min_score=min_score)
    if not signals:
        print("📭 No signals above threshold.")
        return
    print(f"✅ {len(signals)} signal(s) above score {min_score}:\n")
    for sig in signals:
        print(f"  {format_signal(sig)}")

    # Step 2: Import matching markets via their slugs
    print(f"\n[2/3] Importing {len(signals)} markets via Polymarket slugs...")
    client = get_client()

    matched = []
    for sig in signals:
        slug = sig.get("smart_money_slug", "")
        if not slug:
            continue
        url = f"https://polymarket.com/event/{slug}"
        try:
            result = client.import_market(url)
            market_id = result.get("market_id")
            question = result.get("question", sig.get("smart_money_market", ""))
            if market_id:
                matched.append((sig, market_id, question))
                print(f"  ✅ {question[:60]}")
            else:
                status = result.get("status", "unknown")
                print(f"  ⚠️  {slug}: {status}")
        except Exception as e:
            print(f"  ❌ Import failed for {slug}: {e}")

    if not matched:
        print("📭 No markets could be imported.")
        return

    # Step 3: Execute trades
    print(f"\n[3/3] Executing trades ({'LIVE' if not dry_run else 'DRY RUN'})...\n")
    positions_opened = 0
    for sig, market_id, question in matched:
        # Use smart_money_side (already "YES" or "NO") for Polymarket trading
        side = sig.get("smart_money_side", "YES").lower()

        max_pos = float(os.environ.get("SIMMER_SMARTMONEY_MAX_POSITION", "10.0"))
        score_ratio = sig["smart_money_score"] / 10.0
        amount = round(max_pos * score_ratio, 2)
        amount = max(1.0, min(amount, max_pos))

        reason = (
            f"Smart Money Score {sig['smart_money_score']}/10 | "
            f"PolyClawster {sig['smart_money_side']} signal | "
            f"Bid: ${sig['smart_money_volume']:,.0f}"
        )

        mode_tag = "[LIVE] " if not dry_run else "[PAPER] "
        print(f"  {mode_tag}{side.upper()} ${amount:.2f} → {question[:60]}")

        if not dry_run:
            try:
                result = client.trade(
                    market_id=market_id,
                    side=side,
                    amount=amount,
                    source=TRADE_SOURCE,
                    skill_slug=SKILL_SLUG,
                    reasoning=reason,
                )
                if result.success:
                    print(f"    ✅ {result.shares_bought} shares @ ${result.new_price:.3f} | cost: ${result.cost:.2f}")
                else:
                    print(f"    ❌ {result.error}")
            except Exception as e:
                print(f"    ❌ Exception: {e}")
        else:
            print(f"    → Skipped (dry run)")

        positions_opened += 1
        print()

    print(f"Done. {positions_opened} position(s) processed.")


def show_positions():
    """Show current open positions."""
    client = get_client()
    positions = client.get_positions()
    if not positions:
        print("📭 No open positions.")
        return
    print(f"\n{'='*60}")
    print(f"📊 Open Positions ({len(positions)})")
    print(f"{'='*60}\n")
    for p in positions:
        print(f"  {p['market_question'][:60]}")
        print(f"  Side: {p['side'].upper()} | Shares: {p.get('shares', '?')} | Entry: ${p.get('avg_price', '?'):.3f}")


def main():
    parser = argparse.ArgumentParser(description="Smart Money Signal Trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades (default: dry run)")
    parser.add_argument("--min-score", type=float, default=DEFAULT_MIN_SCORE,
                        help=f"Minimum signal score (default: {DEFAULT_MIN_SCORE})")
    parser.add_argument("--status", action="store_true", help="Show open positions only")
    args = parser.parse_args()

    if args.status:
        show_positions()
        return

    dry_run = not args.live
    scan_and_trade(min_score=args.min_score, dry_run=dry_run)


if __name__ == "__main__":
    main()
