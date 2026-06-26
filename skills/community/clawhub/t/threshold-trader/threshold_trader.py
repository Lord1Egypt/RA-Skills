#!/usr/bin/env python3
"""
Threshold Trader - A simple probability-threshold trading skill.

Trades when market prices diverge from your configured probability threshold.
Remix this with your own model predictions, external data, or custom signals.
"""

import os
import sys
import argparse
from typing import Optional, Dict, Any

from simmer_sdk import SimmerClient
from simmer_sdk.sizing import size_position


# Skill configuration
SKILL_SLUG = "threshold-trader"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"

# User-configurable parameters (via env vars)
THRESHOLD_PROBABILITY = float(os.getenv("THRESHOLD_PROBABILITY", "0.70"))
TRADE_SIDE = os.getenv("TRADE_SIDE", "YES").upper()
SIMMER_VENUE = os.getenv("SIMMER_VENUE", "sim")  # "sim" or "polymarket"
MIN_EV = float(os.getenv("SIMMER_MIN_EV", "0.03"))  # 3% minimum edge
KELLY_MULTIPLIER = float(os.getenv("SIMMER_KELLY_MULTIPLIER", "0.25"))  # Quarter Kelly
MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "100.0"))


# Global client singleton
_client = None


def get_client() -> SimmerClient:
    """Get or create the SimmerClient singleton."""
    global _client
    if _client is None:
        api_key = os.environ.get("SIMMER_API_KEY")
        if not api_key:
            raise ValueError("SIMMER_API_KEY environment variable is required")
        
        _client = SimmerClient(
            api_key=api_key,
            venue=SIMMER_VENUE
        )
    return _client


def get_bankroll() -> float:
    """Get current bankroll for the configured venue."""
    client = get_client()
    briefing = client.get_briefing()
    
    venue_data = briefing.get("venues", {}).get(SIMMER_VENUE, {})
    balance = venue_data.get("balance", 0)
    
    print(f"💰 Bankroll ({SIMMER_VENUE}): ${balance:.2f}")
    return balance


def should_trade(market: Dict[str, Any], current_price: float) -> tuple[bool, str]:
    """
    Determine if we should trade based on threshold probability.
    
    This is the core signal logic — REMIX THIS with your own model!
    
    Args:
        market: Market data from Simmer
        current_price: Current market price for the outcome
        
    Returns:
        (should_trade, reasoning) tuple
    """
    # Calculate edge: difference between your probability and market price
    if TRADE_SIDE == "YES":
        edge = THRESHOLD_PROBABILITY - current_price
        direction = "higher"
    else:  # NO
        # For NO trades, we compare against (1 - current_price)
        edge = THRESHOLD_PROBABILITY - (1 - current_price)
        direction = "lower"
    
    edge_pct = edge * 100
    
    # Only trade if edge exceeds minimum threshold
    if edge < MIN_EV:
        return False, f"Edge {edge_pct:.1f}% below minimum {MIN_EV*100}%"
    
    reasoning = (
        f"Market at {current_price:.2%}, threshold {THRESHOLD_PROBABILITY:.2%} — "
        f"edge {edge_pct:.1f}% {direction}. Trading {TRADE_SIDE}."
    )
    
    return True, reasoning


def check_safety(market_id: str, current_price: float) -> tuple[bool, str]:
    """
    Check market context for safety warnings.
    
    Returns:
        (is_safe, reason) tuple
    """
    client = get_client()
    
    # Get market context with our probability for edge analysis
    context = client.get_market_context(
        market_id,
        my_probability=THRESHOLD_PROBABILITY
    )
    
    # Check flip-flop warnings
    trading = context.get("trading", {})
    flip_flop = trading.get("flip_flop_warning", "")
    if flip_flop and "SEVERE" in flip_flop:
        return False, f"Flip-flop warning: {flip_flop}"
    
    # Check slippage
    slippage = context.get("slippage", {})
    slippage_pct = slippage.get("slippage_pct", 0)
    if slippage_pct > 0.15:  # 15% slippage threshold
        return False, f"Slippage too high: {slippage_pct:.1%}"
    
    # Check edge analysis recommendation
    edge = context.get("edge_analysis", {})
    recommendation = edge.get("recommendation", "")
    if recommendation == "HOLD":
        reason = edge.get("reason", "Edge below threshold")
        return False, f"Edge analysis says HOLD: {reason}"
    
    return True, "All safety checks passed"


def execute_trade(
    market: Dict[str, Any],
    bankroll: float,
    live_mode: bool = False
) -> bool:
    """
    Execute a trade on the given market.
    
    Args:
        market: Market data from Simmer
        bankroll: Current bankroll
        live_mode: If True, execute real trades; if False, dry-run
        
    Returns:
        True if trade was executed, False otherwise
    """
    client = get_client()
    market_id = market.get("id")
    title = market.get("title", "Unknown")
    
    # Get current price for the outcome we want to trade
    outcome = TRADE_SIDE
    prices = market.get("prices", {})
    current_price = prices.get(outcome.lower(), prices.get("yes", 0.5))
    
    print(f"\n📊 Evaluating: {title}")
    print(f"   Current price: {current_price:.2%}")
    
    # Check if we should trade based on threshold
    should, reasoning = should_trade(market, current_price)
    if not should:
        print(f"   ⏭️  Skipping: {reasoning}")
        return False
    
    # Run safety checks
    is_safe, safety_msg = check_safety(market_id, current_price)
    if not is_safe:
        print(f"   ⚠️  Safety check failed: {safety_msg}")
        return False
    
    # Calculate position size using Kelly criterion
    p_win = THRESHOLD_PROBABILITY if TRADE_SIDE == "YES" else (1 - THRESHOLD_PROBABILITY)
    
    amount = size_position(
        p_win=p_win,
        market_price=current_price,
        bankroll=bankroll,
        min_ev=MIN_EV,
        kelly_multiplier=KELLY_MULTIPLIER
    )
    
    # Cap at max position size
    amount = min(amount, MAX_POSITION_SIZE)
    
    if amount <= 0:
        print(f"   ⏭️  Position size too small: ${amount:.2f}")
        return False
    
    # Execute trade
    mode_str = "🔴 LIVE" if live_mode else "📄 DRY-RUN"
    print(f"   {mode_str} Trading ${amount:.2f} on {TRADE_SIDE}")
    print(f"   Reasoning: {reasoning}")
    
    try:
        result = client.trade(
            market_id=market_id,
            side="BUY",
            outcome=outcome,
            amount=amount,
            source=TRADE_SOURCE,
            skill_slug=SKILL_SLUG,
            reasoning=reasoning,
            dry_run=not live_mode
        )
        
        if result.get("success"):
            shares = result.get("shares_delta", amount / current_price)
            print(f"   ✅ Trade executed: {shares:.2f} shares")
            return True
        else:
            error = result.get("error", "Unknown error")
            print(f"   ❌ Trade failed: {error}")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception during trade: {e}")
        return False


def auto_redeem():
    """Automatically redeem winning positions."""
    client = get_client()
    
    print("\n💸 Checking for redeemable positions...")
    try:
        results = client.auto_redeem()
        if not results:
            print("   No positions to redeem")
            return
        
        for r in results:
            if r.get("success"):
                market_id = r.get("market_id", "unknown")
                tx_hash = r.get("tx_hash", "")
                print(f"   ✅ Redeemed {market_id}: {tx_hash[:16]}...")
            else:
                error = r.get("error", "Unknown error")
                print(f"   ❌ Redemption failed: {error}")
                
    except Exception as e:
        print(f"   ⚠️  Auto-redeem error (non-critical): {e}")


def scan_and_trade(live_mode: bool = False):
    """
    Main trading loop: scan markets and execute trades.
    
    Args:
        live_mode: If True, execute real trades; if False, dry-run
    """
    client = get_client()
    
    print(f"\n{'='*60}")
    print(f"🎯 Threshold Trader - {SIMMER_VENUE.upper()} mode")
    print(f"{'='*60}")
    print(f"Configuration:")
    print(f"  Threshold: {THRESHOLD_PROBABILITY:.2%}")
    print(f"  Side: {TRADE_SIDE}")
    print(f"  Min Edge: {MIN_EV:.1%}")
    print(f"  Kelly Multiplier: {KELLY_MULTIPLIER}")
    print(f"  Max Position: ${MAX_POSITION_SIZE:.2f}")
    print(f"  Mode: {'LIVE 🔴' if live_mode else 'DRY-RUN 📄'}")
    print(f"{'='*60}")
    
    # Get current bankroll
    bankroll = get_bankroll()
    if bankroll <= 0:
        print("❌ Insufficient bankroll. Please fund your account.")
        return
    
    # Redeem any winning positions first
    auto_redeem()
    
    # Scan active markets
    print(f"\n🔍 Scanning active markets on {SIMMER_VENUE}...")
    try:
        markets_response = client.get_markets(
            venue=SIMMER_VENUE,
            status="active",
            limit=20
        )
        
        markets = markets_response.get("markets", [])
        if not markets:
            print("   No active markets found")
            return
        
        print(f"   Found {len(markets)} active markets")
        
        # Evaluate each market
        trades_executed = 0
        for market in markets:
            if execute_trade(market, bankroll, live_mode):
                trades_executed += 1
        
        print(f"\n{'='*60}")
        print(f"✅ Scan complete: {trades_executed} trades executed")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"❌ Error during market scan: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Threshold Trader - Simple probability-threshold trading skill"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Execute real trades (default: dry-run mode)"
    )
    
    args = parser.parse_args()
    
    # Validate configuration
    if TRADE_SIDE not in ("YES", "NO"):
        print(f"❌ Invalid TRADE_SIDE: {TRADE_SIDE}. Must be YES or NO.")
        sys.exit(1)
    
    if not 0 <= THRESHOLD_PROBABILITY <= 1:
        print(f"❌ Invalid THRESHOLD_PROBABILITY: {THRESHOLD_PROBABILITY}. Must be 0.0-1.0.")
        sys.exit(1)
    
    if SIMMER_VENUE not in ("sim", "polymarket", "kalshi"):
        print(f"❌ Invalid SIMMER_VENUE: {SIMMER_VENUE}. Must be sim, polymarket, or kalshi.")
        sys.exit(1)
    
    # Run the trading loop
    scan_and_trade(live_mode=args.live)


if __name__ == "__main__":
    main()
