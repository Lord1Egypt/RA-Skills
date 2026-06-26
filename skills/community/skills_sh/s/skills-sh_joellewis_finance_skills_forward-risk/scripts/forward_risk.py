# /// script
# dependencies = ["numpy", "scipy"]
# requires-python = ">=3.11"
# ///
"""
Forward-Looking Risk Analysis
==============================
Compute Value-at-Risk (parametric, historical, Monte Carlo), Conditional VaR
(Expected Shortfall), Component VaR, Marginal VaR, and stress testing scenario
analysis for portfolios.

Part of Layer 1b (Forward-Looking Risk) in the finance skills framework.
"""

import argparse
import sys
import numpy as np
from scipy import stats


class ForwardRisk:
    """Forward-looking risk computations for a portfolio.

    Provides parametric, historical, and Monte Carlo VaR, Expected Shortfall,
    risk decomposition (component and marginal VaR), and stress testing.

    Parameters
    ----------
    weights : np.ndarray
        Portfolio weight vector (must sum to 1.0).
    cov_matrix : np.ndarray
        Annualized covariance matrix of asset returns (n x n).
    portfolio_value : float, optional
        Portfolio market value in dollars. Default is 1_000_000.
    mean_returns : np.ndarray or None, optional
        Annualized expected return vector. Default is None (assumes zero
        expected return, appropriate for short-horizon VaR).
    """

    def __init__(
        self,
        weights: np.ndarray,
        cov_matrix: np.ndarray,
        portfolio_value: float = 1_000_000.0,
        mean_returns: np.ndarray | None = None,
    ):
        self.weights = np.asarray(weights, dtype=np.float64)
        self.cov_matrix = np.asarray(cov_matrix, dtype=np.float64)
        self.portfolio_value = portfolio_value
        self.mean_returns = (
            np.asarray(mean_returns, dtype=np.float64)
            if mean_returns is not None
            else np.zeros(len(weights), dtype=np.float64)
        )

        n = len(self.weights)
        if self.cov_matrix.shape != (n, n):
            raise ValueError(
                f"Covariance matrix shape {self.cov_matrix.shape} does not match "
                f"weight vector length {n}."
            )

    def portfolio_volatility(self, annualized: bool = True) -> float:
        """Compute portfolio volatility from the weight vector and covariance matrix.

        Parameters
        ----------
        annualized : bool, optional
            If True (default), return annualized volatility. If False, return
            daily volatility assuming 252 trading days.

        Returns
        -------
        float
            Portfolio volatility: sigma_p = sqrt(w' * Sigma * w).
        """
        variance = self.weights @ self.cov_matrix @ self.weights
        vol = np.sqrt(variance)
        if not annualized:
            vol /= np.sqrt(252)
        return float(vol)

    def parametric_var(
        self, confidence: float = 0.95, horizon_days: int = 1
    ) -> float:
        """Compute parametric (variance-covariance) VaR.

        Assumes normally distributed returns. For short horizons the expected
        return is assumed negligible (absolute VaR).

        Parameters
        ----------
        confidence : float, optional
            Confidence level. Default is 0.95 (95% VaR).
        horizon_days : int, optional
            Holding period in trading days. Default is 1.

        Returns
        -------
        float
            Dollar VaR: W * z_alpha * sigma_p_daily * sqrt(h).
            Positive value representing a potential loss.
        """
        z_alpha = stats.norm.ppf(confidence)
        sigma_daily = self.portfolio_volatility(annualized=False)
        var = self.portfolio_value * z_alpha * sigma_daily * np.sqrt(horizon_days)
        return float(var)

    def historical_var(
        self,
        historical_returns: np.ndarray,
        confidence: float = 0.95,
    ) -> float:
        """Compute historical (non-parametric) VaR from past portfolio returns.

        Parameters
        ----------
        historical_returns : np.ndarray
            Array of historical portfolio returns (or a matrix of asset returns
            with shape (T, n) which will be multiplied by weights).
        confidence : float, optional
            Confidence level. Default is 0.95.

        Returns
        -------
        float
            Dollar VaR from the empirical return distribution.
            Positive value representing a potential loss.
        """
        returns = np.asarray(historical_returns, dtype=np.float64)
        if returns.ndim == 2:
            portfolio_returns = returns @ self.weights
        else:
            portfolio_returns = returns

        percentile = (1 - confidence) * 100
        var_return = np.percentile(portfolio_returns, percentile)
        return float(-var_return * self.portfolio_value)

    def monte_carlo_var(
        self,
        confidence: float = 0.95,
        horizon_days: int = 1,
        n_simulations: int = 10_000,
        seed: int | None = None,
    ) -> float:
        """Compute Monte Carlo VaR via multivariate normal simulation.

        Uses Cholesky decomposition to generate correlated random returns.

        Parameters
        ----------
        confidence : float, optional
            Confidence level. Default is 0.95.
        horizon_days : int, optional
            Holding period in trading days. Default is 1.
        n_simulations : int, optional
            Number of simulation paths. Default is 10,000.
        seed : int or None, optional
            Random seed for reproducibility. Default is None.

        Returns
        -------
        float
            Dollar VaR from the simulated loss distribution.
            Positive value representing a potential loss.
        """
        rng = np.random.default_rng(seed)

        # Scale to daily parameters
        daily_mean = self.mean_returns / 252
        daily_cov = self.cov_matrix / 252

        # Simulate h-day returns by scaling daily parameters
        h_mean = daily_mean * horizon_days
        h_cov = daily_cov * horizon_days

        # Cholesky decomposition for correlated sampling
        try:
            chol = np.linalg.cholesky(h_cov)
        except np.linalg.LinAlgError as exc:
            raise ValueError(
                "Covariance matrix is not positive definite, so Cholesky "
                "decomposition failed. This usually means inconsistent or "
                "estimated correlations. Repair the matrix first — e.g., "
                "project to the nearest positive semi-definite matrix "
                "(clip negative eigenvalues via np.linalg.eigh, or use "
                "Higham's nearest-correlation-matrix algorithm) — then retry."
            ) from exc

        # Generate random scenarios
        z = rng.standard_normal((n_simulations, len(self.weights)))
        simulated_returns = h_mean + z @ chol.T

        # Portfolio returns for each scenario
        portfolio_returns = simulated_returns @ self.weights

        # VaR is the negative of the alpha-percentile
        percentile = (1 - confidence) * 100
        var_return = np.percentile(portfolio_returns, percentile)
        return float(-var_return * self.portfolio_value)

    def conditional_var_parametric(
        self, confidence: float = 0.95, horizon_days: int = 1
    ) -> float:
        """Compute Conditional VaR (Expected Shortfall) under normality.

        CVaR answers: given losses exceed VaR, what is the expected loss?

        For a normal distribution:
            ES_alpha = mu + sigma * phi(z_alpha) / (1 - alpha)

        For short horizons with zero expected return:
            ES_alpha = W * sigma * phi(z_alpha) / (1 - alpha)

        Parameters
        ----------
        confidence : float, optional
            Confidence level. Default is 0.95.
        horizon_days : int, optional
            Holding period in trading days. Default is 1.

        Returns
        -------
        float
            Dollar CVaR (Expected Shortfall). Positive value.
        """
        z_alpha = stats.norm.ppf(confidence)
        phi_z = stats.norm.pdf(z_alpha)
        sigma_daily = self.portfolio_volatility(annualized=False)
        sigma_h = sigma_daily * np.sqrt(horizon_days)

        es = self.portfolio_value * sigma_h * phi_z / (1 - confidence)
        return float(es)

    def conditional_var_empirical(
        self,
        historical_returns: np.ndarray,
        confidence: float = 0.95,
    ) -> float:
        """Compute Conditional VaR (Expected Shortfall) from empirical data.

        The average loss in the tail beyond VaR.

        Parameters
        ----------
        historical_returns : np.ndarray
            Array of historical portfolio returns (or T x n asset return matrix).
        confidence : float, optional
            Confidence level. Default is 0.95.

        Returns
        -------
        float
            Dollar CVaR from the empirical tail. Positive value.
        """
        returns = np.asarray(historical_returns, dtype=np.float64)
        if returns.ndim == 2:
            portfolio_returns = returns @ self.weights
        else:
            portfolio_returns = returns

        percentile = (1 - confidence) * 100
        var_threshold = np.percentile(portfolio_returns, percentile)
        tail_returns = portfolio_returns[portfolio_returns <= var_threshold]

        if len(tail_returns) == 0:
            return self.historical_var(historical_returns, confidence)

        return float(-np.mean(tail_returns) * self.portfolio_value)

    def component_var(self, confidence: float = 0.95) -> np.ndarray:
        """Compute Component VaR for each position.

        Component VaRs sum to total portfolio VaR.

            CVaR_i = w_i * beta_i * VaR_p

        where beta_i = (Sigma * w)_i / (w' * Sigma * w) is the asset's
        beta to the portfolio.

        Parameters
        ----------
        confidence : float, optional
            Confidence level. Default is 0.95.

        Returns
        -------
        np.ndarray
            Array of dollar Component VaR for each position.
            sum(component_var) = parametric_var (1-day).
        """
        z_alpha = stats.norm.ppf(confidence)
        sigma_daily = self.portfolio_volatility(annualized=False)
        daily_cov = self.cov_matrix / 252

        # (Sigma * w)_i gives covariance of asset i with portfolio
        cov_with_portfolio = daily_cov @ self.weights

        # beta_i = cov(R_i, R_p) / var(R_p)
        port_variance = self.weights @ daily_cov @ self.weights
        betas = cov_with_portfolio / port_variance

        # Component VaR_i = w_i * beta_i * VaR_p
        var_p = self.portfolio_value * z_alpha * sigma_daily
        c_var = self.weights * betas * var_p

        return c_var

    def marginal_var(self, confidence: float = 0.95) -> np.ndarray:
        """Compute Marginal VaR for each position.

        Measures the rate of change of portfolio VaR with respect to a small
        change in position weight.

            MVaR_i = z_alpha * (Sigma * w)_i / sigma_p

        Parameters
        ----------
        confidence : float, optional
            Confidence level. Default is 0.95.

        Returns
        -------
        np.ndarray
            Array of Marginal VaR per unit weight change for each asset.
            Multiply by portfolio_value to get dollar Marginal VaR.
        """
        z_alpha = stats.norm.ppf(confidence)
        daily_cov = self.cov_matrix / 252
        sigma_daily = self.portfolio_volatility(annualized=False)

        # MVaR_i = z_alpha * (Sigma * w)_i / sigma_p
        cov_w = daily_cov @ self.weights
        m_var = z_alpha * cov_w / sigma_daily

        return m_var

    @staticmethod
    def scale_var(var_1day: float, horizon_days: int) -> float:
        """Scale 1-day VaR to an h-day horizon using the square-root-of-time rule.

        Assumes i.i.d. returns.

            VaR_h = VaR_1 * sqrt(h)

        Parameters
        ----------
        var_1day : float
            1-day VaR (dollar amount).
        horizon_days : int
            Target horizon in trading days.

        Returns
        -------
        float
            h-day VaR.
        """
        return float(var_1day * np.sqrt(horizon_days))

    @staticmethod
    def stress_scenario(
        weights: np.ndarray,
        portfolio_value: float,
        scenario_returns: np.ndarray,
    ) -> float:
        """Compute portfolio P&L under a stress scenario.

        Parameters
        ----------
        weights : np.ndarray
            Portfolio weight vector.
        portfolio_value : float
            Current portfolio market value.
        scenario_returns : np.ndarray
            Hypothetical or historical return shocks per asset.

        Returns
        -------
        float
            Dollar P&L impact (negative = loss).
        """
        weights = np.asarray(weights, dtype=np.float64)
        scenario_returns = np.asarray(scenario_returns, dtype=np.float64)
        portfolio_return = weights @ scenario_returns
        return float(portfolio_value * portfolio_return)

    @staticmethod
    def factor_risk_decomposition(
        weights: np.ndarray,
        factor_loadings: np.ndarray,
        factor_cov: np.ndarray,
        idiosyncratic_var: np.ndarray,
    ) -> dict[str, float]:
        """Decompose portfolio variance into factor (systematic) and idiosyncratic risk.

            sigma^2_p = b' * Sigma_f * b + sum(w_i^2 * sigma^2_epsilon_i)

        where b = B' * w is the vector of portfolio factor exposures.

        Parameters
        ----------
        weights : np.ndarray
            Portfolio weight vector (n,).
        factor_loadings : np.ndarray
            Factor loading matrix (n x k), where n = assets, k = factors.
        factor_cov : np.ndarray
            Factor covariance matrix (k x k).
        idiosyncratic_var : np.ndarray
            Idiosyncratic variance for each asset (n,).

        Returns
        -------
        dict
            Dictionary with keys: 'total_variance', 'factor_variance',
            'idiosyncratic_variance', 'factor_pct', 'idiosyncratic_pct'.
        """
        weights = np.asarray(weights, dtype=np.float64)
        factor_loadings = np.asarray(factor_loadings, dtype=np.float64)
        factor_cov = np.asarray(factor_cov, dtype=np.float64)
        idiosyncratic_var = np.asarray(idiosyncratic_var, dtype=np.float64)

        # Portfolio factor exposures: b = B' * w
        port_factor_exposures = factor_loadings.T @ weights

        # Factor variance: b' * Sigma_f * b
        factor_var = port_factor_exposures @ factor_cov @ port_factor_exposures

        # Idiosyncratic variance: sum(w_i^2 * sigma^2_epsilon_i)
        idio_var = np.sum(weights**2 * idiosyncratic_var)

        total_var = factor_var + idio_var

        return {
            "total_variance": float(total_var),
            "factor_variance": float(factor_var),
            "idiosyncratic_variance": float(idio_var),
            "factor_pct": float(factor_var / total_var * 100) if total_var > 0 else 0.0,
            "idiosyncratic_pct": float(idio_var / total_var * 100) if total_var > 0 else 0.0,
        }


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Forward-looking risk analysis on a two-asset portfolio
    # ----------------------------------------------------------------
    np.random.seed(42)

    # Portfolio setup: 60% equities, 40% bonds
    weights = np.array([0.60, 0.40])
    portfolio_value = 1_000_000.0

    # Annualized parameters
    equity_vol = 0.18
    bond_vol = 0.05
    correlation = -0.20

    mean_returns = np.array([0.10, 0.04])

    # Build covariance matrix
    cov_matrix = np.array([
        [equity_vol**2, correlation * equity_vol * bond_vol],
        [correlation * equity_vol * bond_vol, bond_vol**2],
    ])

    fr = ForwardRisk(
        weights=weights,
        cov_matrix=cov_matrix,
        portfolio_value=portfolio_value,
        mean_returns=mean_returns,
    )

    print("=" * 60)
    print("Forward-Looking Risk Analysis - Demo")
    print("=" * 60)
    print(f"\nPortfolio: 60% Equities / 40% Bonds")
    print(f"Portfolio Value: ${portfolio_value:,.0f}")
    print(f"Equity Vol: {equity_vol:.0%}  |  Bond Vol: {bond_vol:.0%}  |  Corr: {correlation:.2f}")

    # Portfolio volatility
    ann_vol = fr.portfolio_volatility(annualized=True)
    daily_vol = fr.portfolio_volatility(annualized=False)
    print(f"\nPortfolio Volatility (annualized): {ann_vol:.4f} ({ann_vol*100:.2f}%)")
    print(f"Portfolio Volatility (daily):      {daily_vol:.6f} ({daily_vol*100:.4f}%)")

    # Parametric VaR
    print("\n--- Parametric VaR ---")
    var_95_1d = fr.parametric_var(confidence=0.95, horizon_days=1)
    var_99_1d = fr.parametric_var(confidence=0.99, horizon_days=1)
    var_95_10d = fr.parametric_var(confidence=0.95, horizon_days=10)
    print(f"  95% 1-day VaR:  ${var_95_1d:,.0f}")
    print(f"  99% 1-day VaR:  ${var_99_1d:,.0f}")
    print(f"  95% 10-day VaR: ${var_95_10d:,.0f}")
    print(f"  (sqrt-of-time check: ${ForwardRisk.scale_var(var_95_1d, 10):,.0f})")

    # Monte Carlo VaR
    print("\n--- Monte Carlo VaR (10,000 simulations) ---")
    mc_var_95 = fr.monte_carlo_var(confidence=0.95, horizon_days=1, seed=42)
    mc_var_99 = fr.monte_carlo_var(confidence=0.99, horizon_days=1, seed=42)
    print(f"  95% 1-day MC VaR: ${mc_var_95:,.0f}")
    print(f"  99% 1-day MC VaR: ${mc_var_99:,.0f}")

    # Conditional VaR (Expected Shortfall)
    print("\n--- Conditional VaR (Expected Shortfall, parametric) ---")
    cvar_95 = fr.conditional_var_parametric(confidence=0.95, horizon_days=1)
    cvar_99 = fr.conditional_var_parametric(confidence=0.99, horizon_days=1)
    print(f"  95% 1-day CVaR: ${cvar_95:,.0f}")
    print(f"  99% 1-day CVaR: ${cvar_99:,.0f}")
    print(f"  CVaR/VaR ratio (95%): {cvar_95/var_95_1d:.3f}")

    # Historical VaR from synthetic data
    print("\n--- Historical VaR (from synthetic daily returns) ---")
    n_days = 504
    daily_cov = cov_matrix / 252
    chol = np.linalg.cholesky(daily_cov)
    z = np.random.randn(n_days, 2)
    hist_returns = (mean_returns / 252) + z @ chol.T
    hist_portfolio_returns = hist_returns @ weights

    hist_var_95 = fr.historical_var(hist_portfolio_returns, confidence=0.95)
    hist_cvar_95 = fr.conditional_var_empirical(hist_portfolio_returns, confidence=0.95)
    print(f"  95% Historical VaR:  ${hist_var_95:,.0f}")
    print(f"  95% Historical CVaR: ${hist_cvar_95:,.0f}")

    # Component VaR
    print("\n--- Component VaR (1-day, 95%) ---")
    c_var = fr.component_var(confidence=0.95)
    for i, label in enumerate(["Equities", "Bonds"]):
        pct = c_var[i] / var_95_1d * 100
        print(f"  {label}: ${c_var[i]:,.0f} ({pct:.1f}% of total VaR)")
    print(f"  Sum: ${np.sum(c_var):,.0f}  (Total VaR: ${var_95_1d:,.0f})")

    # Marginal VaR
    print("\n--- Marginal VaR (1-day, 95%) ---")
    m_var = fr.marginal_var(confidence=0.95)
    for i, label in enumerate(["Equities", "Bonds"]):
        print(f"  {label}: {m_var[i]:.6f} (per unit weight change)")

    # Stress Testing
    print("\n--- Stress Testing ---")
    scenarios = {
        "Equity Crash (-30%, bonds +5%)": np.array([-0.30, 0.05]),
        "Rate Shock (equities -10%, bonds -8%)": np.array([-0.10, -0.08]),
        "Stagflation (equities -20%, bonds -3%)": np.array([-0.20, -0.03]),
        "Risk Rally (equities +15%, bonds +2%)": np.array([0.15, 0.02]),
    }
    for name, shock in scenarios.items():
        pnl = ForwardRisk.stress_scenario(weights, portfolio_value, shock)
        print(f"  {name}: ${pnl:+,.0f}")

    # Factor Risk Decomposition
    print("\n--- Factor Risk Decomposition ---")
    # Simple single-factor model (market factor)
    factor_loadings = np.array([[1.0], [0.3]])  # equity beta=1.0, bond beta=0.3
    factor_cov = np.array([[0.0225]])  # market factor variance (15% vol)
    idio_var = np.array([0.0081, 0.0016])  # idiosyncratic variances

    decomp = ForwardRisk.factor_risk_decomposition(
        weights, factor_loadings, factor_cov, idio_var
    )
    print(f"  Total Variance:         {decomp['total_variance']:.6f}")
    print(f"  Factor (Systematic):    {decomp['factor_variance']:.6f} ({decomp['factor_pct']:.1f}%)")
    print(f"  Idiosyncratic:          {decomp['idiosyncratic_variance']:.6f} ({decomp['idiosyncratic_pct']:.1f}%)")

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

    # SKILL.md Example 1: $1M, 15% annual vol, 1-day 95% VaR ~= $15,545 (z=1.645)
    fr1 = ForwardRisk(weights=np.array([1.0]), cov_matrix=np.array([[0.0225]]),
                      portfolio_value=1_000_000.0)
    _check(failures, "Ex1 1-day 95% parametric VaR", fr1.parametric_var(0.95, 1), 15545.0, 10.0)

    # SKILL.md Example 2: 60/40 portfolio analytical benchmark
    cov = np.array([[0.0324, -0.0018], [-0.0018, 0.0025]])
    fr2 = ForwardRisk(weights=np.array([0.60, 0.40]), cov_matrix=cov,
                      portfolio_value=1_000_000.0, mean_returns=np.array([0.10, 0.04]))
    ann_vol = fr2.portfolio_volatility(annualized=True)
    _check(failures, "Ex2 portfolio volatility", ann_vol, 0.105830, 1e-5)
    _check(failures, "Ex2 annual 95% VaR (z=1.645)", 1_000_000.0 * 1.645 * ann_vol, 174090.0, 100.0)

    # CVaR exceeds VaR at the same confidence level
    var95 = fr2.parametric_var(0.95, 1)
    cvar95 = fr2.conditional_var_parametric(0.95, 1)
    _check(failures, "CVaR > VaR", 1.0 if cvar95 > var95 else 0.0, 1.0, 0)

    # Component VaRs sum to total VaR
    _check(failures, "component VaRs sum to total", float(np.sum(fr2.component_var(0.95))), var95, 1e-6)

    if failures:
        print(f"\n{len(failures)} check(s) FAILED: {', '.join(failures)}")
        sys.exit(1)
    print("\nAll checks passed.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.strip().splitlines()[2] if __doc__ else "",
        epilog=(
            "Provides: ForwardRisk. "
            "For programmatic use, import this module (forward_risk) instead of running it. "
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
