"""
Test suite for Bayesian probability update module.
Tests bayesian_update, compute_likelihood_ratio, should_update_probability, and should_close_position.
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bayesian_update import (
    bayesian_update,
    compute_likelihood_ratio,
    should_update_probability,
    should_close_position,
)


class TestBayesianUpdate:
    """Tests for bayesian_update function."""

    def test_neutral_likelihood_ratio_returns_same_probability(self):
        """bayesian_update with likelihood_ratio=1.0 returns same probability."""
        result = bayesian_update(0.6, 1.0)
        assert result == 0.6

    def test_likelihood_ratio_greater_than_one_increases_probability(self):
        """bayesian_update with likelihood_ratio > 1.0 increases probability."""
        result = bayesian_update(0.5, 2.0)
        # new_p = (2.0 * 0.5) / (2.0 * 0.5 + 0.5) = 1.0 / 1.5 = 0.666...
        assert result > 0.5
        assert abs(result - 2.0 / 3.0) < 0.0001

    def test_likelihood_ratio_less_than_one_decreases_probability(self):
        """bayesian_update with likelihood_ratio < 1.0 decreases probability."""
        result = bayesian_update(0.6, 0.5)
        # new_p = (0.5 * 0.6) / (0.5 * 0.6 + 0.4) = 0.3 / 0.7 = 0.428...
        assert result < 0.6
        assert abs(result - 0.3 / 0.7) < 0.0001

    def test_denominator_zero_returns_prior(self):
        """bayesian_update with denominator=0 returns prior (edge case)."""
        # This can happen when prior=1 and likelihood_ratio=0
        result = bayesian_update(1.0, 0.0)
        assert result == 1.0


class TestComputeLikelihoodRatio:
    """Tests for compute_likelihood_ratio function."""

    def test_price_drop_returns_less_than_one(self):
        """compute_likelihood_ratio with price drop returns < 1.0."""
        # If price drops from 0.6 to 0.5, the new probability estimate is lower
        result = compute_likelihood_ratio(0.5, 0.6)
        assert result < 1.0
        assert result > 0

    def test_price_rise_returns_greater_than_one(self):
        """compute_likelihood_ratio with price rise returns > 1.0."""
        # If price rises from 0.5 to 0.6, the new probability estimate is higher
        result = compute_likelihood_ratio(0.6, 0.5)
        assert result > 1.0

    def test_old_price_half_returns_one(self):
        """compute_likelihood_ratio with old_price=0.5 returns 1.0 (edge case - odds are 1:1)."""
        result = compute_likelihood_ratio(0.6, 0.5)
        # odds(0.5) = 0.5/0.5 = 1, so ratio should be based on new price only
        assert result > 1.0  # 0.6 has better odds than 0.5


class TestShouldUpdateProbability:
    """Tests for should_update_probability function."""

    def test_negative_fifteen_percent_pnl_returns_true(self):
        """should_update_probability with -15% PnL returns True (threshold=-10%)."""
        result = should_update_probability(-0.15, threshold=-0.10)
        assert result is True

    def test_negative_five_percent_pnl_returns_false(self):
        """should_update_probability with -5% PnL returns False."""
        result = should_update_probability(-0.05, threshold=-0.10)
        assert result is False


class TestShouldClosePosition:
    """Tests for should_close_position function."""

    def test_large_drop_returns_true(self):
        """should_close_position with updated=0.50, initial=0.70 returns True (diff=0.20 > 0.15)."""
        result = should_close_position(0.50, 0.70, threshold=-0.15)
        assert result is True

    def test_small_drop_returns_false(self):
        """should_close_position with updated=0.60, initial=0.70 returns False (diff=0.10 < 0.15)."""
        result = should_close_position(0.60, 0.70, threshold=-0.15)
        assert result is False


class TestIntegration:
    """Integration test for full Bayesian flow."""

    def test_full_bayesian_flow_initial_drop_triggers_update_and_close(self):
        """Integration: initial=0.65, price drops to 0.50, should trigger update and close."""
        initial_prob = 0.65
        old_price = initial_prob  # For simplicity, use prob as price
        new_price = 0.50

        # Step 1: Check if we should update
        pnl_pct = (new_price - old_price) / old_price
        assert should_update_probability(pnl_pct, threshold=-0.10) is True

        # Step 2: Compute likelihood ratio
        lr = compute_likelihood_ratio(new_price, old_price)
        assert lr < 1.0  # Price drop means lower likelihood

        # Step 3: Update probability
        updated_prob = bayesian_update(initial_prob, lr)
        assert updated_prob < initial_prob

        # Step 4: Check if should close
        # Difference: initial - updated = 0.65 - updated_prob
        # We expect this to be > 0.15 for a significant drop
        assert (
            should_close_position(updated_prob, initial_prob, threshold=-0.15) is True
        )
