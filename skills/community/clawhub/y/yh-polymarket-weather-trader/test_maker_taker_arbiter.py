"""
Test suite for maker_taker_arbiter module.
TDD RED phase - tests should FAIL until implementation is added.
"""

import pytest
from maker_taker_arbiter import StrategyMode, MarketCondition, determine_strategy_mode, get_maker_taker_allocation


class TestGetMakerTakerAllocation:
    """Test allocation percentages for each strategy mode."""

    def test_maker_heavy_returns_65_35(self):
        """MAKER_HEAVY mode should return 65% maker, 35% taker."""
        maker_pct, taker_pct = get_maker_taker_allocation(StrategyMode.MAKER_HEAVY)
        assert maker_pct == 0.65
        assert taker_pct == 0.35

    def test_balanced_returns_50_50(self):
        """BALANCED mode should return 50% maker, 50% taker."""
        maker_pct, taker_pct = get_maker_taker_allocation(StrategyMode.BALANCED)
        assert maker_pct == 0.50
        assert taker_pct == 0.50

    def test_taker_heavy_returns_30_70(self):
        """TAKER_HEAVY mode should return 30% maker, 70% taker."""
        maker_pct, taker_pct = get_maker_taker_allocation(StrategyMode.TAKER_HEAVY)
        assert maker_pct == 0.30
        assert taker_pct == 0.70


class TestDetermineStrategyMode:
    """Test market condition to strategy mode mapping."""

    def test_both_low_returns_maker_heavy(self):
        """spread < 50bps AND vol < 50% annualized → MAKER_HEAVY."""
        condition = MarketCondition(spread_bps=30.0, volatility=0.30)
        result = determine_strategy_mode(condition)
        assert result == StrategyMode.MAKER_HEAVY

    def test_low_spread_high_vol_returns_balanced(self):
        """spread < 50bps XOR vol < 50% → BALANCED (low spread, high vol)."""
        condition = MarketCondition(spread_bps=30.0, volatility=0.60)
        result = determine_strategy_mode(condition)
        assert result == StrategyMode.BALANCED

    def test_high_spread_low_vol_returns_balanced(self):
        """spread < 50bps XOR vol < 50% → BALANCED (high spread, low vol)."""
        condition = MarketCondition(spread_bps=60.0, volatility=0.30)
        result = determine_strategy_mode(condition)
        assert result == StrategyMode.BALANCED

    def test_both_high_returns_taker_heavy(self):
        """spread >= 50bps AND vol >= 50% annualized → TAKER_HEAVY."""
        condition = MarketCondition(spread_bps=60.0, volatility=0.60)
        result = determine_strategy_mode(condition)
        assert result == StrategyMode.TAKER_HEAVY

    def test_just_under_both_thresholds_returns_maker_heavy(self):
        """spread=49bps + vol=0.49 (just under both thresholds) → MAKER_HEAVY."""
        condition = MarketCondition(spread_bps=49.0, volatility=0.49)
        result = determine_strategy_mode(condition)
        assert result == StrategyMode.MAKER_HEAVY

    def test_exactly_at_thresholds_returns_taker_heavy(self):
        """spread=50bps + vol=0.50 (exactly at thresholds) → TAKER_HEAVY."""
        condition = MarketCondition(spread_bps=50.0, volatility=0.50)
        result = determine_strategy_mode(condition)
        assert result == StrategyMode.TAKER_HEAVY

    def test_zero_vol_with_low_spread_returns_maker_heavy(self):
        """volatility=0.0 (zero vol) with spread=30bps → MAKER_HEAVY."""
        condition = MarketCondition(spread_bps=30.0, volatility=0.0)
        result = determine_strategy_mode(condition)
        assert result == StrategyMode.MAKER_HEAVY
