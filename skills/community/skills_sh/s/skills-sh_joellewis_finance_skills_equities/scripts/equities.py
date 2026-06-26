# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.11"
# ///
"""
Equity Analysis
===============
CAPM expected return, dividend discount model (Gordon growth), valuation ratios
(PEG, earnings yield), factor exposure (beta), and sector allocation analysis.

Part of Layer 2 (Asset Classes) in the finance skills framework.
"""

import argparse
import sys
import numpy as np


class EquityValuation:
    """Equity valuation models and ratio calculations.

    Provides static methods for single-stock and portfolio-level valuation
    metrics including CAPM, Gordon Growth Model, and common valuation ratios.
    """

    @staticmethod
    def capm_expected_return(
        risk_free_rate: float,
        beta: float,
        market_return: float,
    ) -> float:
        """Compute expected return using the Capital Asset Pricing Model.

        E(R_i) = R_f + beta_i * (E(R_m) - R_f)

        Parameters
        ----------
        risk_free_rate : float
            Risk-free rate (decimal, e.g., 0.04 for 4%).
        beta : float
            Asset's beta relative to the market portfolio.
        market_return : float
            Expected market return (decimal).

        Returns
        -------
        float
            CAPM expected return (decimal).
        """
        equity_risk_premium = market_return - risk_free_rate
        return risk_free_rate + beta * equity_risk_premium

    @staticmethod
    def gordon_growth_model(
        dividend: float,
        growth_rate: float,
        required_return: float,
    ) -> float:
        """Compute intrinsic value using the Gordon Growth (constant dividend growth) model.

        P = D_1 / (r - g)

        where D_1 is the next period's expected dividend.

        Parameters
        ----------
        dividend : float
            Next period's expected dividend (D_1). If you have the current
            dividend D_0, pass D_0 * (1 + growth_rate).
        growth_rate : float
            Constant dividend growth rate (decimal). Must be less than
            required_return.
        required_return : float
            Required rate of return (decimal). Must exceed growth_rate.

        Returns
        -------
        float
            Intrinsic stock price.

        Raises
        ------
        ValueError
            If growth_rate >= required_return (model is undefined).
        """
        if growth_rate >= required_return:
            raise ValueError(
                f"Growth rate ({growth_rate}) must be less than required return "
                f"({required_return}) for the Gordon Growth Model to be valid."
            )
        return dividend / (required_return - growth_rate)

    @staticmethod
    def pe_ratio(price: float, eps: float) -> float:
        """Compute the Price-to-Earnings ratio.

        Parameters
        ----------
        price : float
            Current share price.
        eps : float
            Earnings per share. Must be positive.

        Returns
        -------
        float
            P/E ratio.

        Raises
        ------
        ValueError
            If eps <= 0.
        """
        if eps <= 0:
            raise ValueError(f"EPS must be positive for P/E calculation, got {eps}.")
        return price / eps

    @staticmethod
    def earnings_yield(eps: float, price: float) -> float:
        """Compute the earnings yield (inverse of P/E).

        Earnings Yield = EPS / Price

        Parameters
        ----------
        eps : float
            Earnings per share.
        price : float
            Current share price. Must be positive.

        Returns
        -------
        float
            Earnings yield (decimal).
        """
        if price <= 0:
            raise ValueError(f"Price must be positive, got {price}.")
        return eps / price

    @staticmethod
    def peg_ratio(pe: float, earnings_growth_rate: float) -> float:
        """Compute the PEG (Price/Earnings-to-Growth) ratio.

        PEG = P/E / Earnings Growth Rate

        Parameters
        ----------
        pe : float
            Price-to-earnings ratio.
        earnings_growth_rate : float
            Expected earnings growth rate as a percentage (e.g., 15 for 15%).
            Must be positive.

        Returns
        -------
        float
            PEG ratio. Values below 1.0 are often considered attractive;
            values above 2.0 may indicate overvaluation relative to growth.

        Raises
        ------
        ValueError
            If earnings_growth_rate <= 0.
        """
        if earnings_growth_rate <= 0:
            raise ValueError(
                f"Earnings growth rate must be positive, got {earnings_growth_rate}."
            )
        return pe / earnings_growth_rate

    @staticmethod
    def dividend_yield(annual_dividend: float, price: float) -> float:
        """Compute the dividend yield.

        Dividend Yield = Annual Dividends Per Share / Price

        Parameters
        ----------
        annual_dividend : float
            Annual dividend per share.
        price : float
            Current share price. Must be positive.

        Returns
        -------
        float
            Dividend yield (decimal).
        """
        if price <= 0:
            raise ValueError(f"Price must be positive, got {price}.")
        return annual_dividend / price

    @staticmethod
    def ev_ebitda(
        market_cap: float,
        total_debt: float,
        cash: float,
        ebitda: float,
    ) -> float:
        """Compute the EV/EBITDA ratio.

        EV/EBITDA = (Market Cap + Total Debt - Cash) / EBITDA

        Parameters
        ----------
        market_cap : float
            Market capitalization.
        total_debt : float
            Total debt (short-term + long-term).
        cash : float
            Cash and cash equivalents.
        ebitda : float
            Earnings Before Interest, Taxes, Depreciation, and Amortization.
            Must be positive.

        Returns
        -------
        float
            EV/EBITDA ratio.

        Raises
        ------
        ValueError
            If ebitda <= 0.
        """
        if ebitda <= 0:
            raise ValueError(f"EBITDA must be positive, got {ebitda}.")
        enterprise_value = market_cap + total_debt - cash
        return enterprise_value / ebitda

    @staticmethod
    def total_return(
        price_begin: float,
        price_end: float,
        dividends: float,
    ) -> float:
        """Compute total return (price return + dividend return).

        Total Return = (P_end - P_begin + Dividends) / P_begin

        Parameters
        ----------
        price_begin : float
            Price at start of period. Must be positive.
        price_end : float
            Price at end of period.
        dividends : float
            Total dividends received during the period.

        Returns
        -------
        float
            Total return (decimal).
        """
        if price_begin <= 0:
            raise ValueError(f"Beginning price must be positive, got {price_begin}.")
        return (price_end - price_begin + dividends) / price_begin


class FactorAnalysis:
    """Factor exposure and style analysis for equity portfolios.

    Parameters
    ----------
    returns : np.ndarray
        Array of periodic asset or portfolio excess returns (decimals).
    factor_returns : np.ndarray
        2D array of factor returns, shape (n_periods, n_factors).
        Each column is a factor time series.
    factor_names : list[str] or None, optional
        Names for each factor. Default is None (uses F1, F2, ...).
    """

    def __init__(
        self,
        returns: np.ndarray,
        factor_returns: np.ndarray,
        factor_names: list[str] | None = None,
    ):
        self.returns = np.asarray(returns, dtype=np.float64)
        self.factor_returns = np.atleast_2d(
            np.asarray(factor_returns, dtype=np.float64)
        )
        if self.factor_returns.shape[0] != len(self.returns):
            raise ValueError(
                f"factor_returns rows ({self.factor_returns.shape[0]}) must match "
                f"returns length ({len(self.returns)})."
            )
        n_factors = self.factor_returns.shape[1]
        if factor_names is not None and len(factor_names) != n_factors:
            raise ValueError(
                f"factor_names length ({len(factor_names)}) must match number of "
                f"factors ({n_factors})."
            )
        self.factor_names = factor_names or [
            f"F{i+1}" for i in range(n_factors)
        ]

    def beta(self) -> dict[str, float]:
        """Compute beta (factor exposure) for each factor via OLS regression.

        For each factor k: beta_k = cov(R, F_k) / var(F_k)
        This is the univariate beta; for multivariate exposures use
        ols_regression.

        Returns
        -------
        dict[str, float]
            Mapping of factor name to univariate beta.
        """
        betas = {}
        for i, name in enumerate(self.factor_names):
            factor = self.factor_returns[:, i]
            cov = np.cov(self.returns, factor)
            var_f = cov[1, 1]
            if var_f == 0:
                betas[name] = 0.0
            else:
                betas[name] = float(cov[0, 1] / var_f)
        return betas

    def ols_regression(self) -> dict:
        """Multivariate OLS regression of returns on all factors.

        R = alpha + beta_1*F_1 + beta_2*F_2 + ... + epsilon

        Returns
        -------
        dict
            Keys: 'alpha' (float), 'betas' (dict[str, float]),
            'r_squared' (float), 'residual_std' (float).
        """
        n = len(self.returns)
        # Add intercept column
        x = np.column_stack([np.ones(n), self.factor_returns])
        # OLS: (X'X)^-1 X'y
        coeffs = np.linalg.lstsq(x, self.returns, rcond=None)[0]
        alpha = float(coeffs[0])
        betas = {
            name: float(coeffs[i + 1]) for i, name in enumerate(self.factor_names)
        }

        # R-squared
        fitted = x @ coeffs
        residuals = self.returns - fitted
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((self.returns - np.mean(self.returns)) ** 2)
        r_squared = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else 0.0

        return {
            "alpha": alpha,
            "betas": betas,
            "r_squared": r_squared,
            "residual_std": float(np.std(residuals, ddof=len(coeffs))),
        }


class SectorAllocation:
    """Analyze sector allocation and concentration in equity portfolios.

    Parameters
    ----------
    sector_weights : dict[str, float]
        Mapping of sector name to portfolio weight (decimals, should sum to 1).
    benchmark_weights : dict[str, float] or None, optional
        Mapping of sector name to benchmark weight. Default is None.
    """

    def __init__(
        self,
        sector_weights: dict[str, float],
        benchmark_weights: dict[str, float] | None = None,
    ):
        self.sector_weights = sector_weights
        self.benchmark_weights = benchmark_weights

    def concentration(self) -> dict:
        """Compute portfolio concentration metrics.

        Returns
        -------
        dict
            Keys: 'top_sector' (str), 'top_weight' (float),
            'herfindahl' (float — sum of squared weights, higher = more
            concentrated), 'effective_sectors' (float — 1/HHI).
        """
        weights = np.array(list(self.sector_weights.values()))
        names = list(self.sector_weights.keys())
        top_idx = int(np.argmax(weights))
        hhi = float(np.sum(weights ** 2))
        return {
            "top_sector": names[top_idx],
            "top_weight": float(weights[top_idx]),
            "herfindahl": hhi,
            "effective_sectors": float(1.0 / hhi) if hhi > 0 else 0.0,
        }

    def active_weights(self) -> dict[str, float]:
        """Compute active sector weights relative to the benchmark.

        active_weight_k = portfolio_weight_k - benchmark_weight_k

        Returns
        -------
        dict[str, float]
            Mapping of sector name to active weight.

        Raises
        ------
        ValueError
            If benchmark_weights is None.
        """
        if self.benchmark_weights is None:
            raise ValueError("Active weight calculation requires benchmark_weights.")
        all_sectors = set(self.sector_weights) | set(self.benchmark_weights)
        result = {}
        for sector in sorted(all_sectors):
            port_w = self.sector_weights.get(sector, 0.0)
            bench_w = self.benchmark_weights.get(sector, 0.0)
            result[sector] = port_w - bench_w
        return result


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Equity analysis on synthetic data
    # ----------------------------------------------------------------
    np.random.seed(42)

    print("=" * 60)
    print("Equity Analysis - Demo")
    print("=" * 60)

    # --- Valuation ---
    print("\n--- Valuation Metrics ---")

    er = EquityValuation.capm_expected_return(
        risk_free_rate=0.04, beta=1.2, market_return=0.10
    )
    print(f"CAPM Expected Return (beta=1.2): {er:.4f} ({er*100:.2f}%)")

    ggm_price = EquityValuation.gordon_growth_model(
        dividend=2.50, growth_rate=0.05, required_return=0.10
    )
    print(f"Gordon Growth Model price (D1=$2.50, g=5%, r=10%): ${ggm_price:.2f}")

    pe = EquityValuation.pe_ratio(price=150.0, eps=7.50)
    print(f"P/E Ratio ($150 / $7.50 EPS): {pe:.2f}")

    ey = EquityValuation.earnings_yield(eps=7.50, price=150.0)
    print(f"Earnings Yield: {ey:.4f} ({ey*100:.2f}%)")

    peg = EquityValuation.peg_ratio(pe=20.0, earnings_growth_rate=15.0)
    print(f"PEG Ratio (P/E=20, growth=15%): {peg:.2f}")

    dy = EquityValuation.dividend_yield(annual_dividend=3.00, price=150.0)
    print(f"Dividend Yield ($3.00 / $150): {dy:.4f} ({dy*100:.2f}%)")

    ev_ebitda = EquityValuation.ev_ebitda(
        market_cap=500e6, total_debt=100e6, cash=50e6, ebitda=75e6
    )
    print(f"EV/EBITDA: {ev_ebitda:.2f}")

    tr = EquityValuation.total_return(
        price_begin=100.0, price_end=110.0, dividends=3.0
    )
    print(f"Total Return ($100->$110, $3 div): {tr:.4f} ({tr*100:.2f}%)")

    # --- Factor Analysis ---
    print("\n--- Factor Analysis (CAPM + Fama-French) ---")

    n_months = 60
    market_excess = np.random.normal(0.005, 0.04, n_months)
    smb = np.random.normal(0.002, 0.03, n_months)
    hml = np.random.normal(0.001, 0.03, n_months)

    # Synthetic fund returns with known exposures
    alpha_true = 0.001  # 10bps monthly alpha
    fund_excess = (
        alpha_true
        + 1.1 * market_excess
        + 0.3 * smb
        - 0.2 * hml
        + np.random.normal(0, 0.01, n_months)
    )

    factor_matrix = np.column_stack([market_excess, smb, hml])
    fa = FactorAnalysis(
        returns=fund_excess,
        factor_returns=factor_matrix,
        factor_names=["Market", "SMB", "HML"],
    )

    print("\nUnivariate betas:")
    for name, b in fa.beta().items():
        print(f"  {name:10s}: {b:.4f}")

    reg = fa.ols_regression()
    print(f"\nMultivariate regression (OLS):")
    print(f"  Alpha (monthly): {reg['alpha']:.6f} ({reg['alpha']*12*100:.2f}% annualized)")
    for name, b in reg["betas"].items():
        print(f"  Beta({name:6s}):    {b:.4f}")
    print(f"  R-squared:       {reg['r_squared']:.4f}")

    # --- Sector Allocation ---
    print("\n--- Sector Allocation ---")

    portfolio_sectors = {
        "Technology": 0.30,
        "Healthcare": 0.15,
        "Financials": 0.12,
        "Consumer Disc.": 0.10,
        "Industrials": 0.10,
        "Energy": 0.08,
        "Comm. Services": 0.06,
        "Utilities": 0.04,
        "Materials": 0.03,
        "Real Estate": 0.02,
    }
    benchmark_sectors = {
        "Technology": 0.28,
        "Healthcare": 0.13,
        "Financials": 0.13,
        "Consumer Disc.": 0.11,
        "Industrials": 0.09,
        "Energy": 0.05,
        "Comm. Services": 0.08,
        "Utilities": 0.03,
        "Materials": 0.05,
        "Real Estate": 0.05,
    }

    sa = SectorAllocation(
        sector_weights=portfolio_sectors,
        benchmark_weights=benchmark_sectors,
    )

    conc = sa.concentration()
    print(f"Top sector: {conc['top_sector']} ({conc['top_weight']*100:.1f}%)")
    print(f"Herfindahl index: {conc['herfindahl']:.4f}")
    print(f"Effective sectors: {conc['effective_sectors']:.1f}")

    print("\nActive weights (portfolio - benchmark):")
    for sector, aw in sa.active_weights().items():
        direction = "OW" if aw > 0 else "UW" if aw < 0 else "  "
        print(f"  {sector:18s}: {aw:+.2%} {direction}")

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
    """Verify key outputs against the SKILL.md worked example."""
    failures: list = []

    # SKILL.md worked example: industrial company metric selection
    _check(failures, "EV/EBITDA ($550M EV / $75M EBITDA)",
           EquityValuation.ev_ebitda(500e6, 100e6, 50e6, 75e6), 7.3333, 1e-4)
    _check(failures, "P/E cross-check ($150 / $7.50)",
           EquityValuation.pe_ratio(150.0, 7.50), 20.0, 1e-12)
    _check(failures, "earnings yield (7.50 / 150)",
           EquityValuation.earnings_yield(7.50, 150.0), 0.05, 1e-12)

    # Key formulas table: CAPM and Gordon growth
    _check(failures, "CAPM (rf=4%, beta=1.2, mkt=10%)",
           EquityValuation.capm_expected_return(0.04, 1.2, 0.10), 0.112, 1e-12)
    _check(failures, "Gordon growth (D1=2.50, g=5%, r=10%)",
           EquityValuation.gordon_growth_model(2.50, 0.05, 0.10), 50.0, 1e-9)

    if failures:
        print(f"\n{len(failures)} check(s) FAILED: {', '.join(failures)}")
        sys.exit(1)
    print("\nAll checks passed.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.strip().splitlines()[2] if __doc__ else "",
        epilog=(
            "Provides: EquityValuation, FactorAnalysis, SectorAllocation. "
            "For programmatic use, import this module (equities) instead of running it. "
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
