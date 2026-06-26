# /// script
# dependencies = ["numpy", "scipy"]
# requires-python = ">=3.11"
# ///
"""
Volatility Modeling
====================
Model and forecast volatility using EWMA, GARCH(1,1), realized volatility
estimators (close-to-close, Parkinson range), volatility term structure
construction, and volatility cones.

Part of Layer 1b (Forward-Looking Risk) in the finance skills framework.
"""

import argparse
import math
import sys

import numpy as np
from scipy import optimize


class VolatilityModeling:
    """Volatility modeling and forecasting from historical return data.

    Parameters
    ----------
    returns : np.ndarray
        Array of periodic (typically daily) log returns or simple returns.
        For daily returns, values are in decimals (e.g., 0.01 = 1%).
    periods_per_year : int, optional
        Number of periods in a year for annualization. Default is 252
        (trading days).
    """

    def __init__(
        self,
        returns: np.ndarray,
        periods_per_year: int = 252,
    ):
        self.returns = np.asarray(returns, dtype=np.float64)
        self.periods_per_year = periods_per_year

    def ewma_variance(
        self, lam: float = 0.94, initial_var: float | None = None
    ) -> np.ndarray:
        """Compute EWMA variance series.

            sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Parameters
        ----------
        lam : float, optional
            Decay factor. RiskMetrics standard: 0.94 (daily), 0.97 (monthly).
            Default is 0.94.
        initial_var : float or None, optional
            Initial variance estimate. If None, uses the sample variance of
            the first 20 observations (or all observations if fewer than 20).

        Returns
        -------
        np.ndarray
            Array of EWMA variance estimates, same length as returns.
        """
        n = len(self.returns)
        variances = np.empty(n, dtype=np.float64)

        if initial_var is None:
            warmup = min(20, n)
            initial_var = np.var(self.returns[:warmup], ddof=1)

        variances[0] = initial_var
        for t in range(1, n):
            variances[t] = lam * variances[t - 1] + (1 - lam) * self.returns[t - 1] ** 2

        return variances

    def ewma_volatility(
        self, lam: float = 0.94, annualized: bool = True, initial_var: float | None = None
    ) -> np.ndarray:
        """Compute EWMA volatility series.

        Parameters
        ----------
        lam : float, optional
            Decay factor. Default is 0.94.
        annualized : bool, optional
            If True (default), annualize the volatility.
        initial_var : float or None, optional
            Initial variance estimate. Default is None (auto-estimated).

        Returns
        -------
        np.ndarray
            Array of EWMA volatility estimates.
        """
        variances = self.ewma_variance(lam=lam, initial_var=initial_var)
        vol = np.sqrt(variances)
        if annualized:
            vol *= np.sqrt(self.periods_per_year)
        return vol

    @staticmethod
    def ewma_effective_window(lam: float) -> float:
        """Compute the effective lookback window for EWMA.

            effective_window ~ 1 / (1 - lambda)

        Parameters
        ----------
        lam : float
            Decay factor.

        Returns
        -------
        float
            Approximate number of observations in the effective window.
        """
        if lam >= 1.0 or lam <= 0.0:
            raise ValueError(f"Lambda must be in (0, 1), got {lam}.")
        return 1.0 / (1.0 - lam)

    def garch11_fit(
        self, initial_params: tuple[float, float, float] | None = None
    ) -> dict[str, float]:
        """Estimate GARCH(1,1) parameters via maximum likelihood.

            sigma^2_t = omega + alpha * r^2_{t-1} + beta * sigma^2_{t-1}

        Uses quasi-maximum likelihood with a normal distribution assumption.

        Parameters
        ----------
        initial_params : tuple of (omega, alpha, beta) or None, optional
            Starting values for optimization. If None, uses sensible defaults
            (omega=1e-6, alpha=0.05, beta=0.90).

        Returns
        -------
        dict
            Dictionary with keys: 'omega', 'alpha', 'beta', 'persistence',
            'long_run_variance', 'long_run_annual_vol', 'half_life',
            'log_likelihood'.
        """
        returns = self.returns
        n = len(returns)

        if initial_params is None:
            initial_params = (1e-6, 0.05, 0.90)

        def _neg_log_likelihood(params: np.ndarray) -> float:
            omega, alpha, beta = params
            if omega <= 0 or alpha < 0 or beta < 0 or alpha + beta >= 1:
                return 1e10

            variances = np.empty(n)
            variances[0] = omega / (1 - alpha - beta)

            for t in range(1, n):
                variances[t] = omega + alpha * returns[t - 1] ** 2 + beta * variances[t - 1]
                if variances[t] <= 0:
                    return 1e10

            # Gaussian log-likelihood (up to constant)
            ll = -0.5 * np.sum(np.log(variances) + returns**2 / variances)
            return -ll

        # Optimize with bounds
        result = optimize.minimize(
            _neg_log_likelihood,
            x0=np.array(initial_params),
            method="L-BFGS-B",
            bounds=[(1e-10, 1e-2), (1e-6, 0.5), (0.5, 0.9999)],
        )

        omega, alpha, beta = result.x
        persistence = alpha + beta
        long_run_var = omega / (1 - persistence) if persistence < 1 else float("inf")
        long_run_vol = np.sqrt(long_run_var * self.periods_per_year) if persistence < 1 else float("inf")
        half_life = -np.log(2) / np.log(persistence) if 0 < persistence < 1 else float("inf")

        return {
            "omega": float(omega),
            "alpha": float(alpha),
            "beta": float(beta),
            "persistence": float(persistence),
            "long_run_variance": float(long_run_var),
            "long_run_annual_vol": float(long_run_vol),
            "half_life": float(half_life),
            "log_likelihood": float(-result.fun),
        }

    @staticmethod
    def garch11_variance_series(
        returns: np.ndarray,
        omega: float,
        alpha: float,
        beta: float,
    ) -> np.ndarray:
        """Compute the GARCH(1,1) conditional variance series for given parameters.

            sigma^2_t = omega + alpha * r^2_{t-1} + beta * sigma^2_{t-1}

        Parameters
        ----------
        returns : np.ndarray
            Return series.
        omega : float
            Constant term.
        alpha : float
            Reaction coefficient (sensitivity to recent shocks).
        beta : float
            Persistence coefficient (memory of past variance).

        Returns
        -------
        np.ndarray
            Conditional variance series.
        """
        returns = np.asarray(returns, dtype=np.float64)
        n = len(returns)
        variances = np.empty(n, dtype=np.float64)

        persistence = alpha + beta
        if persistence < 1:
            variances[0] = omega / (1 - persistence)
        else:
            variances[0] = np.var(returns[:min(20, n)], ddof=1)

        for t in range(1, n):
            variances[t] = omega + alpha * returns[t - 1] ** 2 + beta * variances[t - 1]

        return variances

    @staticmethod
    def garch11_forecast(
        current_var: float,
        omega: float,
        alpha: float,
        beta: float,
        horizons: np.ndarray | list[int],
        periods_per_year: int = 252,
    ) -> np.ndarray:
        """Compute multi-step-ahead GARCH(1,1) variance forecasts.

            E[sigma^2_{t+h}] = V_L + (alpha + beta)^h * (sigma^2_t - V_L)

        Parameters
        ----------
        current_var : float
            Current conditional variance (sigma^2_t).
        omega : float
            GARCH constant term.
        alpha : float
            Reaction coefficient.
        beta : float
            Persistence coefficient.
        horizons : array-like of int
            Forecast horizons (in periods).
        periods_per_year : int, optional
            Periods per year for annualization context. Default is 252.

        Returns
        -------
        np.ndarray
            Forecast variances for each horizon. Same length as horizons.
        """
        _ = periods_per_year  # reserved for future annualization support
        horizons = np.asarray(horizons, dtype=np.float64)
        persistence = alpha + beta

        if persistence >= 1:
            # IGARCH: no mean reversion, variance grows
            return np.full(len(horizons), current_var)

        long_run_var = omega / (1 - persistence)
        forecasts = long_run_var + np.power(persistence, horizons) * (current_var - long_run_var)
        return forecasts

    @staticmethod
    def garch11_half_life(alpha: float, beta: float) -> float:
        """Compute the half-life of a volatility shock under GARCH(1,1).

            h = -ln(2) / ln(alpha + beta)

        Parameters
        ----------
        alpha : float
            Reaction coefficient.
        beta : float
            Persistence coefficient.

        Returns
        -------
        float
            Half-life in periods. Returns inf if alpha + beta >= 1.
        """
        persistence = alpha + beta
        if persistence >= 1:
            return float("inf")
        return float(-np.log(2) / np.log(persistence))

    def realized_volatility(
        self, window: int = 21, annualized: bool = True
    ) -> np.ndarray:
        """Compute rolling realized volatility (close-to-close estimator).

        Uses the standard deviation of returns over a rolling window.

        Parameters
        ----------
        window : int, optional
            Rolling window size in periods. Default is 21 (approx. 1 month).
        annualized : bool, optional
            If True (default), annualize the result.

        Returns
        -------
        np.ndarray
            Rolling realized volatility. First (window - 1) values are NaN.
        """
        n = len(self.returns)
        vol = np.full(n, np.nan, dtype=np.float64)

        for t in range(window - 1, n):
            window_returns = self.returns[t - window + 1 : t + 1]
            vol[t] = np.std(window_returns, ddof=1)

        if annualized:
            vol *= np.sqrt(self.periods_per_year)

        return vol

    @staticmethod
    def parkinson_volatility(
        highs: np.ndarray,
        lows: np.ndarray,
        window: int = 21,
        periods_per_year: int = 252,
        annualized: bool = True,
    ) -> np.ndarray:
        """Compute rolling Parkinson range-based volatility estimator.

        Uses high-low price ranges, which are more efficient than close-to-close
        because they capture intraday price information.

            sigma^2_parkinson = (1 / (4 * n * ln(2))) * sum(ln(H_i / L_i)^2)

        Parameters
        ----------
        highs : np.ndarray
            Daily high prices.
        lows : np.ndarray
            Daily low prices.
        window : int, optional
            Rolling window size. Default is 21.
        periods_per_year : int, optional
            Periods per year. Default is 252.
        annualized : bool, optional
            If True (default), annualize the result.

        Returns
        -------
        np.ndarray
            Rolling Parkinson volatility. First (window - 1) values are NaN.
        """
        highs = np.asarray(highs, dtype=np.float64)
        lows = np.asarray(lows, dtype=np.float64)
        n = len(highs)

        log_hl = np.log(highs / lows)
        log_hl_sq = log_hl ** 2

        vol = np.full(n, np.nan, dtype=np.float64)
        scale = 1.0 / (4.0 * np.log(2.0))

        for t in range(window - 1, n):
            window_data = log_hl_sq[t - window + 1 : t + 1]
            variance = scale * np.mean(window_data)
            vol[t] = np.sqrt(variance)

        if annualized:
            vol *= np.sqrt(periods_per_year)

        return vol

    def volatility_term_structure(
        self, windows: list[int] | None = None, annualized: bool = True
    ) -> dict[int, float]:
        """Compute the realized volatility term structure across multiple horizons.

        Calculates realized volatility for different lookback windows to show
        how volatility varies by measurement horizon.

        Parameters
        ----------
        windows : list of int or None, optional
            List of window sizes (in periods). Default is
            [5, 10, 21, 63, 126, 252] (1w, 2w, 1m, 3m, 6m, 1y).
        annualized : bool, optional
            If True (default), annualize all values.

        Returns
        -------
        dict
            Mapping of window size to volatility value. Windows longer than
            the data are excluded.
        """
        if windows is None:
            windows = [5, 10, 21, 63, 126, 252]

        term_structure: dict[int, float] = {}
        n = len(self.returns)

        for w in windows:
            if w > n:
                continue
            recent = self.returns[-w:]
            vol = float(np.std(recent, ddof=1))
            if annualized:
                vol *= np.sqrt(self.periods_per_year)
            term_structure[w] = vol

        return term_structure

    def volatility_cone(
        self, windows: list[int] | None = None, percentiles: list[float] | None = None
    ) -> dict[int, dict[str, float]]:
        """Compute volatility cones showing the distribution of realized
        volatility across different horizons.

        For each window, rolls through the entire history and computes
        annualized realized vol, then reports percentile statistics.

        Parameters
        ----------
        windows : list of int or None, optional
            Window sizes. Default is [5, 10, 21, 63, 126, 252].
        percentiles : list of float or None, optional
            Percentiles to compute. Default is [10, 25, 50, 75, 90].

        Returns
        -------
        dict
            Nested dict: {window: {'p10': val, 'p25': val, ...,'current': val}}.
            'current' is the most recent window's realized vol.
        """
        if windows is None:
            windows = [5, 10, 21, 63, 126, 252]
        if percentiles is None:
            percentiles = [10.0, 25.0, 50.0, 75.0, 90.0]

        n = len(self.returns)
        cone: dict[int, dict[str, float]] = {}

        for w in windows:
            if w > n:
                continue

            # Compute rolling realized vol for all possible windows
            rolling_vols = []
            for t in range(w - 1, n):
                window_returns = self.returns[t - w + 1 : t + 1]
                vol = np.std(window_returns, ddof=1) * np.sqrt(self.periods_per_year)
                rolling_vols.append(vol)

            rolling_vols_arr = np.array(rolling_vols)

            entry: dict[str, float] = {}
            for p in percentiles:
                entry[f"p{int(p)}"] = float(np.percentile(rolling_vols_arr, p))
            entry["current"] = float(rolling_vols_arr[-1])
            entry["mean"] = float(np.mean(rolling_vols_arr))

            cone[w] = entry

        return cone


def _demo() -> None:
    """Run the demonstration calculations (bare-run default)."""
    np.random.seed(42)

    # Generate 2 years of synthetic daily returns with volatility clustering
    n_days = 504
    returns = np.empty(n_days)
    true_var = 0.0002  # starting daily variance (~22.5% annualized)

    # Simulate with GARCH-like dynamics
    omega_true = 0.000002
    alpha_true = 0.08
    beta_true = 0.91

    for t in range(n_days):
        returns[t] = np.random.normal(0, np.sqrt(true_var))
        true_var = omega_true + alpha_true * returns[t] ** 2 + beta_true * true_var

    print("=" * 60)
    print("Volatility Modeling - Demo")
    print("=" * 60)
    print(f"\nSynthetic data: {n_days} daily returns with GARCH(1,1) dynamics")
    print(f"True parameters: omega={omega_true}, alpha={alpha_true}, beta={beta_true}")
    print(f"True persistence: {alpha_true + beta_true}")

    vm = VolatilityModeling(returns, periods_per_year=252)

    # EWMA
    print("\n--- EWMA Volatility ---")
    ewma_vol = vm.ewma_volatility(lam=0.94, annualized=True)
    print(f"  Lambda: 0.94 (effective window: {VolatilityModeling.ewma_effective_window(0.94):.0f} days)")
    print(f"  Current EWMA vol: {ewma_vol[-1]:.4f} ({ewma_vol[-1]*100:.2f}%)")
    print(f"  Min EWMA vol:     {np.min(ewma_vol):.4f} ({np.min(ewma_vol)*100:.2f}%)")
    print(f"  Max EWMA vol:     {np.max(ewma_vol):.4f} ({np.max(ewma_vol)*100:.2f}%)")

    ewma_vol_97 = vm.ewma_volatility(lam=0.97, annualized=True)
    print(f"\n  Lambda: 0.97 (effective window: {VolatilityModeling.ewma_effective_window(0.97):.0f} days)")
    print(f"  Current EWMA vol: {ewma_vol_97[-1]:.4f} ({ewma_vol_97[-1]*100:.2f}%)")

    # GARCH(1,1) estimation
    print("\n--- GARCH(1,1) Estimation ---")
    garch_params = vm.garch11_fit()
    print(f"  omega:              {garch_params['omega']:.8f}")
    print(f"  alpha:              {garch_params['alpha']:.4f}")
    print(f"  beta:               {garch_params['beta']:.4f}")
    print(f"  persistence (a+b):  {garch_params['persistence']:.4f}")
    print(f"  long-run annual vol: {garch_params['long_run_annual_vol']:.4f} ({garch_params['long_run_annual_vol']*100:.2f}%)")
    print(f"  half-life:          {garch_params['half_life']:.1f} days")
    print(f"  log-likelihood:     {garch_params['log_likelihood']:.2f}")

    # GARCH variance series
    garch_var = VolatilityModeling.garch11_variance_series(
        returns,
        garch_params["omega"],
        garch_params["alpha"],
        garch_params["beta"],
    )
    garch_vol = np.sqrt(garch_var) * np.sqrt(252)
    print(f"\n  Current GARCH vol:  {garch_vol[-1]:.4f} ({garch_vol[-1]*100:.2f}%)")

    # Multi-step forecasts
    print("\n--- GARCH Multi-Step Forecasts ---")
    horizons = [1, 5, 10, 21, 63, 126, 252]
    forecasts = VolatilityModeling.garch11_forecast(
        current_var=garch_var[-1],
        omega=garch_params["omega"],
        alpha=garch_params["alpha"],
        beta=garch_params["beta"],
        horizons=horizons,
    )
    for h, fv in zip(horizons, forecasts):
        ann_vol = np.sqrt(fv * 252)
        print(f"  {h:>3d}-day ahead: daily var = {fv:.8f}, ann vol = {ann_vol:.4f} ({ann_vol*100:.2f}%)")

    # Half-life
    hl = VolatilityModeling.garch11_half_life(garch_params["alpha"], garch_params["beta"])
    print(f"\n  Half-life of vol shocks: {hl:.1f} trading days (~{hl/21:.1f} months)")

    # Realized volatility
    print("\n--- Realized Volatility (close-to-close) ---")
    rv_21 = vm.realized_volatility(window=21)
    rv_63 = vm.realized_volatility(window=63)
    print(f"  21-day realized vol: {rv_21[-1]:.4f} ({rv_21[-1]*100:.2f}%)")
    print(f"  63-day realized vol: {rv_63[-1]:.4f} ({rv_63[-1]*100:.2f}%)")

    # Parkinson range-based volatility (synthetic highs/lows)
    print("\n--- Parkinson Range-Based Volatility ---")
    # Simulate synthetic high/low from returns
    close_prices = 100.0 * np.exp(np.cumsum(returns))
    daily_vol_est = np.abs(returns) + 0.005  # approximate intraday range
    highs = close_prices * (1 + daily_vol_est * 0.5)
    lows = close_prices * (1 - daily_vol_est * 0.5)

    park_vol = VolatilityModeling.parkinson_volatility(highs, lows, window=21)
    print(f"  21-day Parkinson vol: {park_vol[-1]:.4f} ({park_vol[-1]*100:.2f}%)")

    # Volatility Term Structure
    print("\n--- Volatility Term Structure ---")
    term_struct = vm.volatility_term_structure()
    for window, vol in term_struct.items():
        label = {5: "1w", 10: "2w", 21: "1m", 63: "3m", 126: "6m", 252: "1y"}.get(window, f"{window}d")
        print(f"  {label:>3s} ({window:>3d}d): {vol:.4f} ({vol*100:.2f}%)")

    # Volatility Cone
    print("\n--- Volatility Cone ---")
    cone = vm.volatility_cone()
    print(f"  {'Window':>8s}  {'P10':>8s}  {'P25':>8s}  {'P50':>8s}  {'P75':>8s}  {'P90':>8s}  {'Current':>8s}")
    for window, stats_dict in cone.items():
        label = {5: "1w", 10: "2w", 21: "1m", 63: "3m", 126: "6m", 252: "1y"}.get(window, f"{window}d")
        print(
            f"  {label:>8s}  {stats_dict['p10']:>7.2%}  {stats_dict['p25']:>7.2%}  "
            f"{stats_dict['p50']:>7.2%}  {stats_dict['p75']:>7.2%}  {stats_dict['p90']:>7.2%}  "
            f"{stats_dict['current']:>7.2%}"
        )

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)


def _verify() -> None:
    """Assert key computations against the SKILL.md worked examples."""
    checks: list[tuple[str, float, float]] = []

    # SKILL.md Example 1: EWMA update with sigma^2 = 0.0004, r = -3%, lambda = 0.94
    vm = VolatilityModeling(np.array([-0.03, 0.0]), periods_per_year=252)
    variances = vm.ewma_variance(lam=0.94, initial_var=0.0004)
    checks.append(("Example 1 EWMA variance", float(variances[1]), 0.000430))
    checks.append(("Example 1 EWMA daily vol", math.sqrt(variances[1]), 0.02074))
    checks.append((
        "EWMA effective window (lambda=0.94)",
        VolatilityModeling.ewma_effective_window(0.94),
        1.0 / 0.06,
    ))

    # SKILL.md Example 2: GARCH(1,1) with omega=0.000002, alpha=0.08, beta=0.91
    omega, alpha, beta = 0.000002, 0.08, 0.91
    long_run_var = float(
        VolatilityModeling.garch11_forecast(
            current_var=0.0004, omega=omega, alpha=alpha, beta=beta,
            horizons=[100_000],
        )[0]
    )
    checks.append(("Example 2 long-run daily variance", long_run_var, 0.0002))
    checks.append((
        "Example 2 long-run daily vol",
        math.sqrt(long_run_var),
        0.01414,
    ))
    checks.append((
        "Example 2 long-run annualized vol",
        math.sqrt(long_run_var) * math.sqrt(252),
        0.2245,
    ))
    checks.append((
        "Example 2 half-life (days)",
        VolatilityModeling.garch11_half_life(alpha, beta),
        68.97,
    ))

    failures = 0
    for name, got, expected in checks:
        ok = math.isclose(got, expected, rel_tol=1e-3)
        print(f"{'PASS' if ok else 'FAIL'}: {name}: got {got:.6g}, expected {expected:.6g}")
        failures += 0 if ok else 1
    if failures:
        print(f"FAIL: {failures} of {len(checks)} checks failed.")
        sys.exit(1)
    print(f"PASS: all {len(checks)} checks passed.")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="volatility_modeling.py",
        description=(
            "Volatility modeling reference implementation. Main class: "
            "VolatilityModeling, with methods ewma_variance, "
            "ewma_volatility, ewma_effective_window, garch11_fit, "
            "garch11_variance_series, garch11_forecast, garch11_half_life, "
            "realized_volatility, parkinson_volatility, "
            "volatility_term_structure, volatility_cone."
        ),
        epilog=(
            "Primarily intended to be imported as a module: "
            "from volatility_modeling import VolatilityModeling. "
            "Run with no arguments to print a demo on synthetic returns."
        ),
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help=(
            "run the key computations and assert outputs match the "
            "SKILL.md worked examples (exits nonzero on mismatch)"
        ),
    )
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    if args.verify:
        _verify()
    else:
        _demo()
