# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.11"
# ///
"""
Diversification Analyzer
=========================
Compute portfolio variance, diversification ratio, HHI concentration,
correlation matrix analysis, risk contributions, and marginal contributions
to risk.

Part of Layer 4 (Portfolio Construction) in the finance skills framework.
"""

import argparse
import sys
import numpy as np


class DiversificationAnalyzer:
    """Analyze portfolio diversification using covariance-based methods.

    Parameters
    ----------
    weights : np.ndarray
        Array of portfolio weights summing to 1.0.
    cov_matrix : np.ndarray
        n x n covariance matrix of asset returns.
    asset_names : list[str] or None, optional
        Names for each asset. Default is None (uses integer indices).
    """

    def __init__(
        self,
        weights: np.ndarray,
        cov_matrix: np.ndarray,
        asset_names: list[str] | None = None,
    ):
        self.weights = np.asarray(weights, dtype=np.float64)
        self.cov_matrix = np.asarray(cov_matrix, dtype=np.float64)
        self.n_assets = len(self.weights)
        self.asset_names = asset_names or [str(i) for i in range(self.n_assets)]

        if self.cov_matrix.shape != (self.n_assets, self.n_assets):
            raise ValueError(
                f"Covariance matrix shape {self.cov_matrix.shape} does not match "
                f"number of assets ({self.n_assets})."
            )

    def asset_volatilities(self) -> np.ndarray:
        """Extract individual asset volatilities from the covariance matrix.

        Returns
        -------
        np.ndarray
            Array of asset standard deviations (volatilities).
        """
        return np.sqrt(np.diag(self.cov_matrix))

    def correlation_matrix(self) -> np.ndarray:
        """Derive the correlation matrix from the covariance matrix.

        Returns
        -------
        np.ndarray
            n x n correlation matrix where rho_ij = cov_ij / (sigma_i * sigma_j).
        """
        vols = self.asset_volatilities()
        outer_vols = np.outer(vols, vols)
        # Avoid division by zero for zero-volatility assets
        with np.errstate(divide="ignore", invalid="ignore"):
            corr = np.where(outer_vols > 0, self.cov_matrix / outer_vols, 0.0)
        return corr

    def portfolio_variance(self) -> float:
        """Compute portfolio variance: sigma^2_p = w' * Sigma * w.

        Returns
        -------
        float
            Portfolio variance.
        """
        return float(self.weights @ self.cov_matrix @ self.weights)

    def portfolio_volatility(self) -> float:
        """Compute portfolio volatility: sigma_p = sqrt(w' * Sigma * w).

        Returns
        -------
        float
            Portfolio standard deviation.
        """
        return float(np.sqrt(self.portfolio_variance()))

    def weighted_average_volatility(self) -> float:
        """Compute the weighted average of individual asset volatilities.

        Returns
        -------
        float
            sum(w_i * sigma_i). This equals portfolio volatility only when
            all pairwise correlations are 1.
        """
        vols = self.asset_volatilities()
        return float(np.sum(self.weights * vols))

    def diversification_ratio(self) -> float:
        """Compute the diversification ratio.

        Returns
        -------
        float
            DR = sum(w_i * sigma_i) / sigma_p.
            DR = 1 for perfectly correlated assets, higher for better
            diversification. A fully diversified equal-volatility portfolio
            with zero correlations has DR = sqrt(n).
        """
        port_vol = self.portfolio_volatility()
        if port_vol == 0:
            return 1.0
        return float(self.weighted_average_volatility() / port_vol)

    def diversification_benefit(self) -> float:
        """Compute the diversification benefit in volatility terms.

        Returns
        -------
        float
            sum(w_i * sigma_i) - sigma_p.
            The reduction in volatility achieved through diversification.
        """
        return float(self.weighted_average_volatility() - self.portfolio_volatility())

    def hhi_concentration(self) -> float:
        """Compute the Herfindahl-Hirschman Index of weight concentration.

        Returns
        -------
        float
            HHI = sum(w_i^2). Ranges from 1/n (equal weights) to 1 (single
            asset). Lower values indicate more diversified weight allocation.
        """
        return float(np.sum(self.weights ** 2))

    def effective_number_of_assets(self) -> float:
        """Compute the effective number of assets (inverse HHI).

        Returns
        -------
        float
            N_eff = 1 / HHI = 1 / sum(w_i^2). For equal weights, N_eff = n.
            For a single-asset portfolio, N_eff = 1.
        """
        hhi = self.hhi_concentration()
        if hhi == 0:
            return 0.0
        return float(1.0 / hhi)

    def marginal_contribution_to_risk(self) -> np.ndarray:
        """Compute marginal contribution to risk for each asset.

        Returns
        -------
        np.ndarray
            MRC_i = (Sigma * w)_i / sigma_p.
            The rate of change of portfolio volatility with respect to
            asset i's weight.
        """
        port_vol = self.portfolio_volatility()
        if port_vol == 0:
            return np.zeros(self.n_assets)
        sigma_w = self.cov_matrix @ self.weights
        return sigma_w / port_vol

    def risk_contribution(self) -> np.ndarray:
        """Compute the risk contribution of each asset to portfolio volatility.

        Returns
        -------
        np.ndarray
            RC_i = w_i * (Sigma * w)_i / sigma_p.
            The sum of all risk contributions equals portfolio volatility.
        """
        return self.weights * self.marginal_contribution_to_risk()

    def risk_contribution_pct(self) -> np.ndarray:
        """Compute the percentage risk contribution of each asset.

        Returns
        -------
        np.ndarray
            RC_i / sigma_p expressed as fractions summing to 1.0.
            Shows each asset's share of total portfolio risk.
        """
        port_vol = self.portfolio_volatility()
        if port_vol == 0:
            return np.zeros(self.n_assets)
        rc = self.risk_contribution()
        return rc / port_vol

    def minimum_variance_weights(self) -> np.ndarray:
        """Compute the unconstrained minimum variance portfolio weights.

        This is the closed-form solution with only the full-investment
        constraint (weights sum to 1). There is no long-only constraint,
        so weights may be negative (short positions).

        Returns
        -------
        np.ndarray
            w_mv = Sigma^(-1) * 1 / (1' * Sigma^(-1) * 1).
            The portfolio with the lowest possible volatility.
        """
        ones = np.ones(self.n_assets)
        inv_cov = np.linalg.inv(self.cov_matrix)
        numerator = inv_cov @ ones
        denominator = ones @ inv_cov @ ones
        return numerator / denominator

    def summary(self) -> dict:
        """Compute all diversification metrics and return as a dictionary.

        Returns
        -------
        dict
            Dictionary of metric names to values.
        """
        return {
            "portfolio_volatility": self.portfolio_volatility(),
            "weighted_avg_volatility": self.weighted_average_volatility(),
            "diversification_ratio": self.diversification_ratio(),
            "diversification_benefit": self.diversification_benefit(),
            "hhi_concentration": self.hhi_concentration(),
            "effective_n_assets": self.effective_number_of_assets(),
        }


def build_covariance_matrix(
    volatilities: np.ndarray,
    correlation_matrix: np.ndarray,
) -> np.ndarray:
    """Build a covariance matrix from volatilities and a correlation matrix.

    Parameters
    ----------
    volatilities : np.ndarray
        Array of asset standard deviations.
    correlation_matrix : np.ndarray
        n x n correlation matrix.

    Returns
    -------
    np.ndarray
        n x n covariance matrix where cov_ij = sigma_i * sigma_j * rho_ij.
    """
    vols = np.asarray(volatilities, dtype=np.float64)
    corr = np.asarray(correlation_matrix, dtype=np.float64)
    return np.outer(vols, vols) * corr


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Diversification analysis on a 4-asset portfolio
    # ----------------------------------------------------------------
    np.random.seed(42)

    # Define a 4-asset portfolio
    asset_names = ["US Equity", "Intl Equity", "US Bonds", "Commodities"]
    weights = np.array([0.40, 0.20, 0.30, 0.10])
    volatilities = np.array([0.16, 0.18, 0.04, 0.22])

    # Correlation matrix
    corr_matrix = np.array([
        [1.00, 0.75, 0.10, 0.20],
        [0.75, 1.00, 0.05, 0.25],
        [0.10, 0.05, 1.00, -0.10],
        [0.20, 0.25, -0.10, 1.00],
    ])

    # Build covariance matrix
    cov_matrix = build_covariance_matrix(volatilities, corr_matrix)

    analyzer = DiversificationAnalyzer(
        weights=weights,
        cov_matrix=cov_matrix,
        asset_names=asset_names,
    )

    print("=" * 60)
    print("Diversification Analysis - Demo")
    print("=" * 60)

    # Portfolio risk
    port_vol = analyzer.portfolio_volatility()
    wavg_vol = analyzer.weighted_average_volatility()
    print(f"\nPortfolio Volatility:          {port_vol:.4f} ({port_vol*100:.2f}%)")
    print(f"Weighted Avg Volatility:       {wavg_vol:.4f} ({wavg_vol*100:.2f}%)")
    print(f"Diversification Benefit:       {analyzer.diversification_benefit():.4f} "
          f"({analyzer.diversification_benefit()*100:.2f}% risk reduction)")
    print(f"Diversification Ratio:         {analyzer.diversification_ratio():.4f}")

    # Concentration
    print(f"\nHHI Concentration:             {analyzer.hhi_concentration():.4f}")
    print(f"Effective # of Assets:         {analyzer.effective_number_of_assets():.2f}")

    # Correlation matrix
    print("\nCorrelation Matrix:")
    corr = analyzer.correlation_matrix()
    header = "              " + "  ".join(f"{name:>12s}" for name in asset_names)
    print(header)
    for i, name in enumerate(asset_names):
        row = f"  {name:12s}" + "  ".join(f"{corr[i, j]:12.4f}" for j in range(len(asset_names)))
        print(row)

    # Risk contributions
    print("\nRisk Contributions:")
    rc = analyzer.risk_contribution()
    rc_pct = analyzer.risk_contribution_pct()
    mrc = analyzer.marginal_contribution_to_risk()
    for i, name in enumerate(asset_names):
        print(f"  {name:15s}: RC = {rc[i]:.6f}  "
              f"(%RC = {rc_pct[i]*100:6.2f}%)  "
              f"MRC = {mrc[i]:.6f}  "
              f"Weight = {weights[i]*100:.1f}%")
    print(f"  {'Sum':15s}: RC = {np.sum(rc):.6f} (should equal portfolio vol {port_vol:.6f})")

    # Minimum variance portfolio
    print("\nMinimum Variance Portfolio Weights:")
    mv_weights = analyzer.minimum_variance_weights()
    for i, name in enumerate(asset_names):
        print(f"  {name:15s}: {mv_weights[i]:7.4f} ({mv_weights[i]*100:6.2f}%)")
    mv_vol = float(np.sqrt(mv_weights @ cov_matrix @ mv_weights))
    print(f"  MV Portfolio Vol: {mv_vol:.4f} ({mv_vol*100:.2f}%)")

    # Summary
    print("\n" + "-" * 40)
    print("Summary:")
    print("-" * 40)
    summary = analyzer.summary()
    for metric, value in summary.items():
        print(f"  {metric:30s}: {value:.4f}")

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

    # SKILL.md Example 1: two-asset portfolio (60% stock @ 20% vol, 40% bond @ 5% vol, rho=0.2)
    cov = build_covariance_matrix(np.array([0.20, 0.05]),
                                  np.array([[1.0, 0.2], [0.2, 1.0]]))
    analyzer = DiversificationAnalyzer(weights=np.array([0.60, 0.40]), cov_matrix=cov)
    _check(failures, "Ex1 portfolio volatility", analyzer.portfolio_volatility(), 0.1255, 1e-4)
    _check(failures, "Ex1 weighted avg volatility", analyzer.weighted_average_volatility(), 0.14, 1e-12)
    _check(failures, "Ex1 diversification benefit", analyzer.diversification_benefit(), 0.0145, 1e-4)

    # SKILL.md Example 2: diversification ratio definition (DR = wavg vol / port vol)
    _check(failures, "Ex2 diversification ratio formula", 0.1575 / 0.105, 1.50, 1e-12)
    _check(failures, "Ex1 implied diversification ratio", analyzer.diversification_ratio(),
           0.14 / 0.125539, 1e-4)

    if failures:
        print(f"\n{len(failures)} check(s) FAILED: {', '.join(failures)}")
        sys.exit(1)
    print("\nAll checks passed.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.strip().splitlines()[2] if __doc__ else "",
        epilog=(
            "Provides: DiversificationAnalyzer, build_covariance_matrix. "
            "For programmatic use, import this module (diversification) instead of running it. "
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
