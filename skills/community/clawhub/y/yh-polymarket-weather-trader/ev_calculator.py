#!/usr/bin/env python3
"""
Expected Value (EV) Calculator + Kelly Criterion + Longtail Filter

Based on @Movez's Game Theory on Polymarket analysis:
- Taker loses -1.12%/trade without EV calculation
- <20¢ contracts have 16-57% systematic premium (longtail bias)
- Kelly Criterion for mathematically optimal position sizing
"""

from typing import Literal


def calculate_ev(price: float, win_prob: float) -> float:
    """
    Calculate Expected Value per dollar invested.

    EV = p × (1-price)/price - (1-p) × 1
       = p × b - q
    where:
        b = net odds = (1 - price) / price
        p = win probability (our estimate)
        q = 1 - p

    Args:
        price: Current market price (0.0 to 1.0, represents probability)
        win_prob: Our estimated win probability (0.0 to 1.0)

    Returns:
        Expected value per dollar invested. EV > 0 means favorable trade.
        EV = 0 means fair odds, EV < 0 means unfavorable.

    Raises:
        ZeroDivisionError: If price is 0.0 or 1.0
    """
    if price <= 0.0 or price >= 1.0:
        raise ZeroDivisionError("Price must be between 0.0 and 1.0")

    b = (1 - price) / price  # net odds
    p = win_prob
    q = 1 - p
    ev = p * b - q
    return ev


def should_take_trade(price: float, win_prob: float, min_ev: float = 0.0) -> bool:
    """
    Determine if a trade meets the EV threshold.

    Args:
        price: Current market price
        win_prob: Our estimated win probability
        min_ev: Minimum EV threshold to accept trade (default 0.0)

    Returns:
        True if EV > min_ev, False otherwise
    """
    try:
        ev = calculate_ev(price, win_prob)
    except ZeroDivisionError:
        return False
    return ev > min_ev


def kelly_fraction(price: float, win_prob: float) -> float:
    """
    Calculate full Kelly Criterion fraction.

    f* = (b × p - q) / b
    where:
        b = net odds = (1 - price) / price
        p = win probability
        q = 1 - p

    Args:
        price: Current market price
        win_prob: Our estimated win probability

    Returns:
        Full Kelly fraction (0.0 to 1.0). Use quarter Kelly for safety.
    """
    if price <= 0.0 or price >= 1.0:
        return 0.0

    b = (1 - price) / price
    p = win_prob
    q = 1 - p

    if b <= 0:
        return 0.0

    f_star = (b * p - q) / b
    return max(0.0, min(1.0, f_star))  # cap at 100%


def quarter_kelly_position(
    price: float, win_prob: float, bankroll: float, max_pos: float
) -> float:
    """
    Calculate position size using Quarter Kelly Criterion.

    Quarter Kelly = (full Kelly) / 4
    This provides ~2x the growth of fixed sizing while being ~75% less risky
    than full Kelly.

    Args:
        price: Current market price
        win_prob: Our estimated win probability
        bankroll: Total capital available for trading
        max_pos: Maximum position size allowed (from config)

    Returns:
        Recommended position size in USD, capped at max_pos
    """
    kelly = kelly_fraction(price, win_prob)
    if kelly <= 0.0:
        return 0.0

    quarter_kelly = kelly / 4
    position = bankroll * quarter_kelly
    return min(position, max_pos)


def is_longtail_contract(
    price: float, strategy_type: Literal["taker", "maker"] = "taker"
) -> bool:
    """
    Detect longtail contracts with systematic premium.

    Per @Movez analysis: <20¢ contracts have 16-57% systematic premium.
    These are overpriced on average and should be avoided or treated with
    higher EV requirements.

    Args:
        price: Current market price
        strategy_type: 'taker' or 'maker' (maker strategies are less affected)

    Returns:
        True if this is a longtail contract requiring special handling
    """
    return price < 0.20 and strategy_type == "taker"


def longtail_ev_adjustment(price: float, raw_ev: float) -> float:
    """
    Apply longtail bias penalty to EV calculation.

    Per @Movez analysis: <20¢ contracts have 16-57% systematic premium.
    We use a conservative 20% penalty.

    Args:
        price: Current market price
        raw_ev: Raw EV calculated without longtail adjustment

    Returns:
        Adjusted EV with longtail penalty applied
    """
    penalty = 0.20
    return raw_ev - penalty


def derive_win_prob(
    momentum_pct: float, divergence: float, base_prob: float = 0.50
) -> float:
    """
    Derive win probability from momentum strength and divergence from 50¢.

    Used by fastloop trader where win_prob is not fixed but derived from:
    - Momentum strength (stronger momentum = higher probability)
    - Divergence from 50¢ (more mispricing = more opportunity)

    Args:
        momentum_pct: Absolute momentum percentage (e.g., 0.8 for 0.8%)
        divergence: How far price is from 50¢ (absolute, e.g., 0.05 for 5¢)
        base_prob: Base probability (default 50¢ market = 0.50)

    Returns:
        Estimated win probability between 0.01 and 0.99
    """
    momentum_bonus = min(0.25, momentum_pct / 100)
    divergence_bonus = min(0.20, divergence)
    win_prob = base_prob + momentum_bonus + divergence_bonus
    return max(0.01, min(0.99, win_prob))
