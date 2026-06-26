"""
Bayesian probability update module for position management.

Provides functions to update probability estimates using Bayes' theorem
when positions experience significant PnL drops.
"""

from typing import Tuple


def bayesian_update(prior_prob: float, likelihood_ratio: float) -> float:
    """
    Update probability using Bayes' theorem.

    new_p = (LR × prior) / (LR × prior + (1 - prior))

    Args:
        prior_prob: Initial probability estimate (0 to 1)
        likelihood_ratio: Likelihood ratio from price movement

    Returns:
        Posterior probability after applying likelihood ratio
    """
    numerator = likelihood_ratio * prior_prob
    denominator = (likelihood_ratio * prior_prob) + (1 - prior_prob)
    if denominator == 0:
        return prior_prob
    return numerator / denominator


def compute_likelihood_ratio(new_price: float, old_price: float) -> float:
    """
    Convert price movement into likelihood ratio using odds ratio.

    Returns odds_new / odds_old where odds = p / (1 - p)

    Args:
        new_price: New probability/price estimate (0 to 1)
        old_price: Old probability/price estimate (0 to 1)

    Returns:
        Likelihood ratio (1.0 means no change)
    """
    if old_price <= 0 or old_price >= 1:
        return 1.0
    odds_new = new_price / (1 - new_price)
    odds_old = old_price / (1 - old_price)
    return odds_new / odds_old


def should_update_probability(
    position_pnl_pct: float, threshold: float = -0.10
) -> bool:
    """
    Trigger Bayesian update when PnL drops below threshold.

    Args:
        position_pnl_pct: Position PnL as decimal (e.g., -0.15 for -15%)
        threshold: PnL threshold to trigger update (default: -10%)

    Returns:
        True if PnL drop exceeds threshold
    """
    return position_pnl_pct < threshold


def should_close_position(
    updated_prob: float, initial_prob: float, threshold: float = -0.15
) -> bool:
    """
    Close if updated probability dropped more than threshold from initial.

    Args:
        updated_prob: Updated probability after Bayesian update
        initial_prob: Initial probability before update
        threshold: Maximum allowed drop (negative, e.g., -0.15 for 15%)

    Returns:
        True if probability drop exceeds threshold
    """
    # threshold is negative (e.g., -0.15), so initial_prob + threshold < initial_prob
    return updated_prob < initial_prob + threshold


def compute_new_kelly_size(
    initial_prob: float, updated_prob: float, initial_kelly_size: float
) -> float:
    """
    Compute new Kelly size based on updated probability.

    Args:
        initial_prob: Initial probability estimate
        updated_prob: Updated probability after Bayesian analysis
        initial_kelly_size: Original Kelly position size

    Returns:
        New position size scaled by probability ratio
    """
    if initial_prob <= 0 or initial_prob >= 1:
        return initial_kelly_size
    if updated_prob <= 0 or updated_prob >= 1:
        return 0.0
    # Scale Kelly by the ratio of updated to initial probability
    return initial_kelly_size * (updated_prob / initial_prob)
