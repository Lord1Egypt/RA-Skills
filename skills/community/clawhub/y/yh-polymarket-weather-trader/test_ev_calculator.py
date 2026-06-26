#!/usr/bin/env python3
"""
Tests for ev_calculator: calculate_ev, should_take_trade,
kelly_fraction, quarter_kelly_position, is_longtail_contract,
longtail_ev_adjustment.

Uses stdlib unittest only — no external dependencies.
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ev_calculator import (
    calculate_ev,
    should_take_trade,
    kelly_fraction,
    quarter_kelly_position,
    is_longtail_contract,
    longtail_ev_adjustment,
    derive_win_prob,
)


class TestCalculateEV(unittest.TestCase):
    """Tests for calculate_ev()"""

    def test_fair_odds_returns_zero_ev(self):
        """At fair odds (p=price), EV should be ~0."""
        price = 0.50
        p = 0.50  # 50% win probability = market-implied odds
        ev = calculate_ev(price, p)
        self.assertAlmostEqual(ev, 0.0, places=6)

    def test_positive_ev_favorable_trade(self):
        """When our estimate > market price, EV should be positive."""
        price = 0.50
        p = 0.55  # We think 55% but market says 50%
        ev = calculate_ev(price, p)
        self.assertGreater(ev, 0.0)

    def test_negative_ev_unfavorable_trade(self):
        """When our estimate < market price, EV should be negative."""
        price = 0.50
        p = 0.45  # We think 45% but market says 50%
        ev = calculate_ev(price, p)
        self.assertLess(ev, 0.0)

    def test_high_price_low_prob_negative_ev(self):
        """Expensive contract with low probability = very negative EV."""
        price = 0.90
        p = 0.10
        ev = calculate_ev(price, p)
        self.assertLess(ev, 0.0)
        self.assertLess(ev, -0.5)

    def test_low_price_high_prob_positive_ev(self):
        """Cheap contract with high probability = positive EV."""
        price = 0.10
        p = 0.50
        ev = calculate_ev(price, p)
        self.assertGreater(ev, 0.0)

    def test_extreme_price_bounds(self):
        """Edge cases at price boundaries."""
        with self.assertRaises(ZeroDivisionError):
            calculate_ev(0.0, 0.5)
        with self.assertRaises(ZeroDivisionError):
            calculate_ev(1.0, 0.5)


class TestShouldTakeTrade(unittest.TestCase):
    """Tests for should_take_trade()"""

    def test_positive_ev_returns_true(self):
        """EV > 0 should return True."""
        self.assertTrue(should_take_trade(price=0.50, win_prob=0.55))

    def test_negative_ev_returns_false(self):
        """EV <= 0 should return False."""
        self.assertFalse(should_take_trade(price=0.50, win_prob=0.45))

    def test_zero_ev_returns_false(self):
        """EV == 0 should return False (no edge)."""
        self.assertFalse(should_take_trade(price=0.50, win_prob=0.50))

    def test_custom_min_ev_threshold(self):
        """Custom threshold should be respected."""
        self.assertFalse(should_take_trade(price=0.50, win_prob=0.51, min_ev=0.05))
        self.assertTrue(should_take_trade(price=0.50, win_prob=0.60, min_ev=0.05))


class TestKellyFraction(unittest.TestCase):
    """Tests for kelly_fraction()"""

    def test_fair_odds_returns_zero_kelly(self):
        """At fair odds, Kelly fraction should be 0."""
        price = 0.50
        p = 0.50
        kelly = kelly_fraction(price, p)
        self.assertAlmostEqual(kelly, 0.0, places=6)

    def test_positive_edge_returns_positive_kelly(self):
        """Positive edge should return positive Kelly."""
        price = 0.50
        p = 0.55
        kelly = kelly_fraction(price, p)
        self.assertGreater(kelly, 0.0)
        self.assertLess(kelly, 1.0)

    def test_kelly_never_exceeds_one(self):
        """Kelly fraction should be capped at 1.0 (100%)."""
        price = 0.01
        p = 0.99
        kelly = kelly_fraction(price, p)
        self.assertLessEqual(kelly, 1.0)

    def test_kelly_never_negative(self):
        """Kelly fraction should never be negative."""
        price = 0.90
        p = 0.10
        kelly = kelly_fraction(price, p)
        self.assertGreaterEqual(kelly, 0.0)

    def test_zero_price_returns_zero_kelly(self):
        """Zero price should return 0 Kelly (avoid division by zero)."""
        kelly = kelly_fraction(0.0, 0.5)
        self.assertEqual(kelly, 0.0)


class TestQuarterKellyPosition(unittest.TestCase):
    """Tests for quarter_kelly_position()"""

    def test_position_below_max(self):
        """Quarter Kelly position should be less than max_pos."""
        position = quarter_kelly_position(
            price=0.50, win_prob=0.55, bankroll=100.0, max_pos=5.0
        )
        self.assertLessEqual(position, 5.0)

    def test_position_respects_bankroll(self):
        """Quarter Kelly should scale with bankroll."""
        pos_100 = quarter_kelly_position(
            price=0.50, win_prob=0.55, bankroll=100.0, max_pos=100.0
        )
        pos_200 = quarter_kelly_position(
            price=0.50, win_prob=0.55, bankroll=200.0, max_pos=100.0
        )
        self.assertGreater(pos_200, pos_100)

    def test_zero_ev_returns_zero_position(self):
        """Zero EV should return 0 position (no trade)."""
        position = quarter_kelly_position(
            price=0.50, win_prob=0.50, bankroll=100.0, max_pos=5.0
        )
        self.assertEqual(position, 0.0)

    def test_max_cap_applied(self):
        """Position should be capped at max_pos."""
        position = quarter_kelly_position(
            price=0.01, win_prob=0.99, bankroll=10000.0, max_pos=5.0
        )
        self.assertEqual(position, 5.0)


class TestIsLongtailContract(unittest.TestCase):
    """Tests for is_longtail_contract()"""

    def test_below_20_cents_taker_is_longtail(self):
        """<20¢ taker contracts are longtail."""
        self.assertTrue(is_longtail_contract(price=0.15, strategy_type="taker"))

    def test_above_20_cents_not_longtail(self):
        """>=20¢ contracts are not longtail."""
        self.assertFalse(is_longtail_contract(price=0.25, strategy_type="taker"))

    def test_exactly_20_cents_not_longtail(self):
        """Exactly 20¢ is not longtail (threshold is < 20¢)."""
        self.assertFalse(is_longtail_contract(price=0.20, strategy_type="taker"))

    def test_maker_not_flagged(self):
        """Maker strategy is not flagged as longtail even if <20¢."""
        self.assertFalse(is_longtail_contract(price=0.15, strategy_type="maker"))

    def test_1_cent_contract_is_longtail(self):
        """Very cheap contracts are longtail."""
        self.assertTrue(is_longtail_contract(price=0.01, strategy_type="taker"))


class TestLongtailEVAdjustment(unittest.TestCase):
    """Tests for longtail_ev_adjustment()"""

    def test_penalty_reduces_ev(self):
        """Longtail penalty should reduce raw EV."""
        raw_ev = 0.10
        adjusted = longtail_ev_adjustment(0.15, raw_ev)
        self.assertLess(adjusted, raw_ev)

    def test_positive_ev_can_become_negative(self):
        """Positive EV can become negative after penalty."""
        raw_ev = 0.15
        adjusted = longtail_ev_adjustment(0.15, raw_ev)
        self.assertLess(adjusted, 0.0)

    def test_high_ev_survives_penalty(self):
        """High enough EV survives the penalty."""
        raw_ev = 0.50
        adjusted = longtail_ev_adjustment(0.15, raw_ev)
        self.assertGreater(adjusted, 0.0)


class TestDeriveWinProb(unittest.TestCase):
    """Tests for derive_win_prob()"""

    def test_base_prob_at_zero_momentum(self):
        """Zero momentum and zero divergence should return base probability."""
        prob = derive_win_prob(momentum_pct=0.0, divergence=0.0, base_prob=0.50)
        self.assertAlmostEqual(prob, 0.50, places=2)

    def test_momentum_increases_prob(self):
        """Stronger momentum should increase probability above base."""
        prob = derive_win_prob(momentum_pct=1.0, divergence=0.0, base_prob=0.50)
        self.assertGreater(prob, 0.50)

    def test_divergence_increases_prob(self):
        """Larger divergence should increase probability."""
        prob_low = derive_win_prob(momentum_pct=0.0, divergence=0.05, base_prob=0.50)
        prob_high = derive_win_prob(momentum_pct=0.0, divergence=0.15, base_prob=0.50)
        self.assertGreater(prob_high, prob_low)

    def test_prob_bounded_between_0_01_and_0_99(self):
        """Probability should never go below 0.01 or above 0.99."""
        prob_min = derive_win_prob(momentum_pct=100.0, divergence=1.0, base_prob=0.50)
        self.assertLessEqual(prob_min, 0.99)
        prob_max = derive_win_prob(momentum_pct=-100.0, divergence=-1.0, base_prob=0.50)
        self.assertGreaterEqual(prob_max, 0.01)

    def test_momentum_bonus_capped_at_0_25(self):
        """Momentum bonus should be capped at 0.25."""
        prob_at_cap = derive_win_prob(momentum_pct=50.0, divergence=0.0, base_prob=0.50)
        prob_over_cap = derive_win_prob(
            momentum_pct=100.0, divergence=0.0, base_prob=0.50
        )
        self.assertAlmostEqual(
            prob_at_cap, prob_over_cap, places=2
        )  # Both capped at 0.25


if __name__ == "__main__":
    unittest.main()
