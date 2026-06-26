# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.11"
# ///
"""
Bet Sizing Toolkit
===================
Kelly criterion (discrete and continuous), fractional Kelly, growth rate
computation, volatility-scaled position sizing, and drawdown-based sizing.

Part of Layer 4 (Portfolio Construction) in the finance skills framework.
"""

import argparse
import sys
import numpy as np


class KellyCriterion:
    """Compute Kelly-optimal position sizes for discrete and continuous bets.

    This class provides static methods for the core Kelly formulas and
    instance methods for analyzing a specific investment opportunity.

    Parameters
    ----------
    expected_excess_return : float
        Expected return above the risk-free rate (mu - r_f) as a decimal.
    volatility : float
        Standard deviation of returns as a decimal.
    """

    def __init__(
        self,
        expected_excess_return: float,
        volatility: float,
    ):
        self.expected_excess_return = expected_excess_return
        self.volatility = volatility

    @staticmethod
    def discrete_kelly(
        win_prob: float,
        payoff_odds: float,
    ) -> float:
        """Compute Kelly fraction for a discrete (binary) bet.

        Parameters
        ----------
        win_prob : float
            Probability of winning (0 < p < 1).
        payoff_odds : float
            Payoff odds (b). Win returns b dollars per dollar wagered;
            loss loses the wager.

        Returns
        -------
        float
            Optimal fraction of wealth to wager: f* = (b*p - q) / b
            where q = 1 - p. Returns 0 if no positive edge exists.
        """
        q = 1.0 - win_prob
        kelly = (payoff_odds * win_prob - q) / payoff_odds
        return max(kelly, 0.0)

    def continuous_kelly(self) -> float:
        """Compute Kelly fraction for a normally distributed investment.

        Returns
        -------
        float
            Optimal fraction of wealth: f* = (mu - r_f) / sigma^2.
            Can exceed 1.0 (implying leverage).
        """
        if self.volatility == 0:
            return 0.0
        return self.expected_excess_return / (self.volatility ** 2)

    def fractional_kelly(self, fraction: float = 0.5) -> float:
        """Compute a fraction of the full Kelly bet.

        Parameters
        ----------
        fraction : float, optional
            Fraction of full Kelly to use. Default is 0.5 (half Kelly).
            Common values: 0.5 (half), 0.333 (third), 0.25 (quarter).

        Returns
        -------
        float
            Fractional Kelly allocation: f = fraction * f*.
        """
        return fraction * self.continuous_kelly()

    def growth_rate(self, allocation: float | None = None) -> float:
        """Compute the expected geometric growth rate at a given allocation.

        Parameters
        ----------
        allocation : float or None, optional
            Fraction of wealth allocated. If None, uses full Kelly.
            Default is None.

        Returns
        -------
        float
            Expected growth rate: g(f) = f*(mu-r_f) - f^2*sigma^2/2.
            At full Kelly, g* = (mu-r_f)^2 / (2*sigma^2).
        """
        if allocation is None:
            allocation = self.continuous_kelly()
        return (
            allocation * self.expected_excess_return
            - (allocation ** 2) * (self.volatility ** 2) / 2.0
        )

    def max_growth_rate(self) -> float:
        """Compute the maximum possible geometric growth rate (at full Kelly).

        Returns
        -------
        float
            g* = (mu - r_f)^2 / (2 * sigma^2).
        """
        if self.volatility == 0:
            return 0.0
        return self.expected_excess_return ** 2 / (2.0 * self.volatility ** 2)

    def growth_rate_curve(
        self,
        allocations: np.ndarray | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Compute growth rates across a range of allocations.

        Parameters
        ----------
        allocations : np.ndarray or None, optional
            Array of allocation fractions to evaluate. If None, uses
            0 to 2*f* in 100 steps. Default is None.

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            - allocations: array of allocation fractions
            - growth_rates: corresponding growth rates
        """
        if allocations is None:
            f_star = self.continuous_kelly()
            upper = max(2.0 * abs(f_star), 1.0)
            alloc = np.linspace(0.0, upper, 100)
        else:
            alloc = allocations

        growth_rates = np.array([self.growth_rate(f) for f in alloc])
        return alloc, growth_rates

    def summary(self) -> dict:
        """Compute all Kelly metrics for the investment.

        Returns
        -------
        dict
            Dictionary of metric names to values.
        """
        f_star = self.continuous_kelly()
        return {
            "full_kelly": f_star,
            "half_kelly": self.fractional_kelly(0.5),
            "third_kelly": self.fractional_kelly(1.0 / 3.0),
            "quarter_kelly": self.fractional_kelly(0.25),
            "max_growth_rate": self.max_growth_rate(),
            "growth_at_full_kelly": self.growth_rate(f_star),
            "growth_at_half_kelly": self.growth_rate(f_star / 2.0),
            "growth_at_quarter_kelly": self.growth_rate(f_star / 4.0),
        }


class PositionSizer:
    """Utility methods for position sizing based on risk targets.

    All methods are static and do not require instantiation.
    """

    @staticmethod
    def volatility_target_size(
        target_risk: float,
        asset_volatility: float,
    ) -> float:
        """Compute position size to achieve a target risk level.

        Parameters
        ----------
        target_risk : float
            Desired volatility contribution as a decimal (e.g., 0.02 for 2%).
        asset_volatility : float
            Asset's annualized volatility as a decimal.

        Returns
        -------
        float
            Position weight: w = target_risk / sigma_i.
        """
        if asset_volatility == 0:
            return 0.0
        return target_risk / asset_volatility

    @staticmethod
    def position_var(
        weight: float,
        volatility: float,
        portfolio_value: float,
        z_alpha: float = 1.645,
    ) -> float:
        """Compute position-level Value at Risk.

        Parameters
        ----------
        weight : float
            Position weight as a fraction of portfolio value.
        volatility : float
            Asset's annualized volatility as a decimal.
        portfolio_value : float
            Total portfolio value in dollars.
        z_alpha : float, optional
            Z-score for the confidence level. Default is 1.645 (95% one-sided).

        Returns
        -------
        float
            VaR_i = w_i * sigma_i * z_alpha * V.
            Dollar amount at risk.
        """
        return weight * volatility * z_alpha * portfolio_value

    @staticmethod
    def max_drawdown_size(
        max_acceptable_drawdown: float,
        asset_volatility: float,
        drawdown_multiplier: float = 2.0,
    ) -> float:
        """Compute position size based on maximum acceptable drawdown.

        Uses the heuristic that maximum drawdown is approximately
        drawdown_multiplier * volatility (empirically 2-3x for equities).

        Parameters
        ----------
        max_acceptable_drawdown : float
            Maximum drawdown the investor can tolerate as a decimal
            (e.g., 0.10 for 10%).
        asset_volatility : float
            Asset's annualized volatility as a decimal.
        drawdown_multiplier : float, optional
            Multiplier relating expected max drawdown to volatility.
            Default is 2.0.

        Returns
        -------
        float
            Position weight: w = max_dd / (multiplier * sigma).
        """
        if asset_volatility == 0:
            return 0.0
        expected_max_dd = drawdown_multiplier * asset_volatility
        return max_acceptable_drawdown / expected_max_dd

    @staticmethod
    def conviction_weighted_sizes(
        edge_scores: np.ndarray,
        certainty_scores: np.ndarray,
        max_position: float = 0.10,
    ) -> np.ndarray:
        """Compute position sizes proportional to conviction.

        Parameters
        ----------
        edge_scores : np.ndarray
            Array of edge strength scores (e.g., 1-5 scale).
        certainty_scores : np.ndarray
            Array of certainty scores (e.g., 1-5 scale).
        max_position : float, optional
            Maximum position weight for the highest-conviction idea.
            Default is 0.10 (10%).

        Returns
        -------
        np.ndarray
            Normalized position weights proportional to edge * certainty,
            scaled so the maximum weight equals max_position.
        """
        edge = np.asarray(edge_scores, dtype=np.float64)
        certainty = np.asarray(certainty_scores, dtype=np.float64)
        raw_scores = edge * certainty
        if np.max(raw_scores) == 0:
            return np.zeros_like(raw_scores)
        # Scale so max conviction = max_position
        weights = raw_scores / np.max(raw_scores) * max_position
        return weights


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Bet sizing toolkit
    # ----------------------------------------------------------------
    np.random.seed(42)

    print("=" * 60)
    print("Bet Sizing Toolkit - Demo")
    print("=" * 60)

    # --- Discrete Kelly ---
    print("\n--- Discrete Kelly Criterion ---")
    scenarios = [
        ("Even money, 55% win", 0.55, 1.0),
        ("Even money, 60% win", 0.60, 1.0),
        ("2:1 payoff, 40% win", 0.40, 2.0),
        ("3:1 payoff, 30% win", 0.30, 3.0),
    ]
    for desc, p, b in scenarios:
        f = KellyCriterion.discrete_kelly(p, b)
        print(f"  {desc:30s}: f* = {f:.4f} ({f*100:.2f}%)")

    # --- Continuous Kelly ---
    print("\n--- Continuous Kelly (Investment) ---")
    investments = [
        ("Conservative (4% excess, 10% vol)", 0.04, 0.10),
        ("Balanced (8% excess, 20% vol)", 0.08, 0.20),
        ("Aggressive (12% excess, 30% vol)", 0.12, 0.30),
    ]
    for desc, mu_excess, sigma in investments:
        kelly = KellyCriterion(mu_excess, sigma)
        summary = kelly.summary()
        print(f"\n  {desc}:")
        print(f"    Full Kelly:     {summary['full_kelly']:.4f} ({summary['full_kelly']*100:.1f}%)")
        print(f"    Half Kelly:     {summary['half_kelly']:.4f} ({summary['half_kelly']*100:.1f}%)")
        print(f"    Quarter Kelly:  {summary['quarter_kelly']:.4f} ({summary['quarter_kelly']*100:.1f}%)")
        print(f"    Max Growth Rate: {summary['max_growth_rate']:.4f} ({summary['max_growth_rate']*100:.2f}%)")
        print(f"    g(full):  {summary['growth_at_full_kelly']:.4f}")
        print(f"    g(half):  {summary['growth_at_half_kelly']:.4f} "
              f"({summary['growth_at_half_kelly']/summary['max_growth_rate']*100:.1f}% of max)")

    # --- Growth Rate Curve ---
    print("\n--- Growth Rate Curve (8% excess, 20% vol) ---")
    kelly = KellyCriterion(0.08, 0.20)
    test_fractions = [0.25, 0.50, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0]
    print(f"  {'Fraction':>10s}  {'Allocation':>12s}  {'Growth Rate':>12s}")
    f_star = kelly.continuous_kelly()
    for frac in test_fractions:
        alloc = f_star * frac
        g = kelly.growth_rate(alloc)
        print(f"  {frac:10.2f}  {alloc*100:11.1f}%  {g*100:11.4f}%")

    # --- Volatility-Targeted Sizing ---
    print("\n--- Volatility-Targeted Position Sizing ---")
    target_risk = 0.02  # 2% risk per position
    assets = [
        ("Low vol stock (12%)", 0.12),
        ("Avg vol stock (20%)", 0.20),
        ("High vol stock (35%)", 0.35),
        ("Crypto (80%)", 0.80),
    ]
    for desc, vol in assets:
        w = PositionSizer.volatility_target_size(target_risk, vol)
        print(f"  {desc:25s}: weight = {w:.4f} ({w*100:.1f}%)")

    # --- Position VaR ---
    print("\n--- Position VaR (portfolio = $1,000,000) ---")
    portfolio_value = 1_000_000
    for desc, vol in assets:
        w = PositionSizer.volatility_target_size(target_risk, vol)
        var = PositionSizer.position_var(w, vol, portfolio_value)
        print(f"  {desc:25s}: VaR(95%) = ${var:,.0f}")

    # --- Max Drawdown-Based Sizing ---
    print("\n--- Max Drawdown-Based Sizing (max DD = 10%) ---")
    max_dd = 0.10
    for desc, vol in assets:
        w = PositionSizer.max_drawdown_size(max_dd, vol)
        print(f"  {desc:25s}: weight = {w:.4f} ({w*100:.1f}%)")

    # --- Conviction Weighting ---
    print("\n--- Conviction-Weighted Position Sizes ---")
    names = ["High conviction A", "High conviction B", "Medium", "Low", "Speculative"]
    edge_scores = np.array([5, 4, 3, 2, 1])
    certainty_scores = np.array([5, 4, 3, 3, 2])
    weights = PositionSizer.conviction_weighted_sizes(edge_scores, certainty_scores, max_position=0.10)
    for name, e, c, w in zip(names, edge_scores, certainty_scores, weights):
        print(f"  {name:20s}: edge={e}, cert={c}, score={e*c:2d}, weight={w*100:.1f}%")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)

def _check(failures: list, name: str, actual: float, expected: float, tol: float) -> None:
    """Record a verification check result."""
    ok = abs(actual - expected) <= tol
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {name}: actual={actual:.6g}, expected={expected:.6g}, tol={tol:.2g}")
    if not ok:
        failures.append(name)

def _verify() -> None:
    """Verify key outputs against the SKILL.md worked examples."""
    failures: list = []

    # SKILL.md Example 1: discrete Kelly, p=0.55, even money
    _check(failures, "Ex1 discrete Kelly f*", KellyCriterion.discrete_kelly(0.55, 1.0), 0.10, 1e-12)
    # Script clamps negative-edge bets to zero (documented in SKILL.md)
    _check(failures, "negative edge clamped to 0", KellyCriterion.discrete_kelly(0.40, 1.0), 0.0, 1e-12)

    # SKILL.md Example 2: continuous Kelly, 8% excess / 20% vol
    kelly = KellyCriterion(0.08, 0.20)
    _check(failures, "Ex2 full Kelly", kelly.continuous_kelly(), 2.0, 1e-12)
    _check(failures, "Ex2 half Kelly", kelly.fractional_kelly(0.5), 1.0, 1e-12)
    _check(failures, "Ex2 max growth rate", kelly.max_growth_rate(), 0.08, 1e-12)
    _check(failures, "Ex2 growth at half Kelly (f=1.0)", kelly.growth_rate(1.0), 0.06, 1e-12)
    _check(failures, "Ex2 growth at quarter Kelly (f=0.5)", kelly.growth_rate(0.5), 0.035, 1e-12)

    if failures:
        print(f"\n{len(failures)} check(s) FAILED: {', '.join(failures)}")
        sys.exit(1)
    print("\nAll checks passed.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.strip().splitlines()[2] if __doc__ else "",
        epilog=(
            "Provides: KellyCriterion, PositionSizer. "
            "For programmatic use, import this module (bet_sizing) instead of running it. "
            "Bare run executes a demo whose printed values match the SKILL.md worked examples; "
            "--verify asserts those values and exits nonzero on mismatch."
        ),
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="run the verification checks against the SKILL.md worked-example values",
    )
    args = parser.parse_args()
    if args.verify:
        _verify()
    else:
        _demo()


if __name__ == "__main__":
    main()
