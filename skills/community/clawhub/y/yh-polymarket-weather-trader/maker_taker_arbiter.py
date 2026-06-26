"""
Maker/Taker Strategy Arbiter Module.

Dynamically switches between Maker (passive limit orders) and Taker (aggressive market orders)
based on market conditions.

Strategy decision rules:
- spread < 50bps AND vol < 50% annualized → MAKER_HEAVY (65% Maker / 35% Taker)
- spread < 50bps XOR vol < 50% → BALANCED (50% Maker / 50% Taker)
- spread >= 50bps AND vol >= 50% annualized → TAKER_HEAVY (30% Maker / 70% Taker)

On strategy switch: existing positions are NOT closed, only new orders follow current mode.
"""

from enum import Enum
from dataclasses import dataclass


class StrategyMode(Enum):
    """Maker/Taker strategy modes with allocation ratios."""
    MAKER_HEAVY = "maker_heavy"   # 65% Maker / 35% Taker
    BALANCED = "balanced"          # 50% Maker / 50% Taker
    TAKER_HEAVY = "taker_heavy"    # 30% Maker / 70% Taker


@dataclass
class MarketCondition:
    """
    Market condition metrics for strategy determination.
    
    Attributes:
        spread_bps: Bid-ask spread in basis points (e.g., 30.0 = 30 bps = 0.30%)
        volatility: Annualized volatility as decimal (e.g., 0.40 = 40%)
        volume_24h: 24-hour trading volume (optional, for future use)
    """
    spread_bps: float      # Bid-ask spread in basis points
    volatility: float      # Annualized volatility (0.0 to 1.0+)
    volume_24h: float = 0.0  # Optional, for future use


def determine_strategy_mode(condition: MarketCondition) -> StrategyMode:
    """
    Determine strategy mode based on market conditions.
    
    Decision rules:
    - spread < 50bps AND volatility < 50% → MAKER_HEAVY
    - spread < 50bps XOR volatility < 50% → BALANCED  
    - spread >= 50bps AND volatility >= 50% → TAKER_HEAVY
    
    Args:
        condition: MarketCondition with spread_bps and volatility
        
    Returns:
        StrategyMode enum indicating current strategy
    """
    low_spread = condition.spread_bps < 50
    low_vol = condition.volatility < 0.50
    
    if low_spread and low_vol:
        return StrategyMode.MAKER_HEAVY
    elif low_spread != low_vol:  # XOR - one but not both
        return StrategyMode.BALANCED
    else:
        return StrategyMode.TAKER_HEAVY


def get_maker_taker_allocation(mode: StrategyMode) -> tuple[float, float]:
    """
    Get maker/taker allocation percentages for given strategy mode.
    
    Args:
        mode: StrategyMode enum
        
    Returns:
        Tuple of (maker_pct, taker_pct) as floats summing to 1.0
    """
    if mode == StrategyMode.MAKER_HEAVY:
        return (0.65, 0.35)
    elif mode == StrategyMode.BALANCED:
        return (0.50, 0.50)
    else:
        return (0.30, 0.70)
