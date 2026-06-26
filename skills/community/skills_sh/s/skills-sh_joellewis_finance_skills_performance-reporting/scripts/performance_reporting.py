# /// script
# dependencies = ["numpy", "scipy"]
# requires-python = ">=3.11"
# ///
"""
Performance Reporting
======================
Compute portfolio performance metrics for reporting: time-weighted returns
(modified Dietz), money-weighted returns (IRR), GIPS-compliant composite
construction, and standard period returns (MTD, QTD, YTD, inception-to-date).

Part of Layer 8 (Reporting & Communication) in the finance skills framework.
"""

import argparse
import math
import sys

import numpy as np
from scipy.optimize import brentq


class ModifiedDietz:
    """Compute time-weighted returns using the Modified Dietz method.

    The Modified Dietz method approximates the true time-weighted return
    by weighting cash flows by the fraction of the period they were invested.
    It is widely used as a GIPS-acceptable approximation when daily valuations
    are not available.

    Parameters
    ----------
    beginning_value : float
        Portfolio market value at the start of the period.
    ending_value : float
        Portfolio market value at the end of the period.
    cash_flows : np.ndarray
        External cash flows during the period (positive = contribution,
        negative = withdrawal).
    cash_flow_days : np.ndarray
        Day within the period each cash flow occurred (0 = start, D = end).
    total_days : int
        Total number of days in the measurement period.
    """

    def __init__(
        self,
        beginning_value: float,
        ending_value: float,
        cash_flows: np.ndarray,
        cash_flow_days: np.ndarray,
        total_days: int,
    ):
        self.v_start = beginning_value
        self.v_end = ending_value
        self.cf = np.asarray(cash_flows, dtype=np.float64)
        self.cf_days = np.asarray(cash_flow_days, dtype=np.float64)
        self.total_days = total_days

        if len(self.cf) != len(self.cf_days):
            raise ValueError(
                "cash_flows and cash_flow_days must have the same length."
            )

    def weights(self) -> np.ndarray:
        """Compute the time-weighting factor for each cash flow.

        Returns
        -------
        np.ndarray
            w_i = (D - d_i) / D, the fraction of the period each flow
            was invested.
        """
        return (self.total_days - self.cf_days) / self.total_days

    def weighted_cash_flows(self) -> float:
        """Compute the sum of time-weighted cash flows.

        Returns
        -------
        float
            sum(w_i * CF_i)
        """
        w = self.weights()
        return float(np.dot(w, self.cf))

    def compute_return(self) -> float:
        """Compute the Modified Dietz return.

        Returns
        -------
        float
            R = (V_end - V_start - sum(CF)) / (V_start + sum(w_i * CF_i))
        """
        total_cf = float(np.sum(self.cf))
        denominator = self.v_start + self.weighted_cash_flows()
        if abs(denominator) < 1e-12:
            return 0.0
        return (self.v_end - self.v_start - total_cf) / denominator


class TimeWeightedReturn:
    """Compute true time-weighted return by chain-linking sub-period returns.

    When portfolio valuations are available at each cash flow date, the exact
    TWR can be calculated by compounding sub-period returns. This removes
    the impact of external cash flows and measures pure investment performance.

    Parameters
    ----------
    sub_period_returns : np.ndarray
        Array of sub-period returns (decimals). Each sub-period ends at
        a valuation date (typically when an external cash flow occurs).
    """

    def __init__(self, sub_period_returns: np.ndarray):
        self.sub_returns = np.asarray(sub_period_returns, dtype=np.float64)

    def cumulative_return(self) -> float:
        """Compute the cumulative time-weighted return.

        Returns
        -------
        float
            TWR = prod(1 + r_t) - 1
        """
        return float(np.prod(1.0 + self.sub_returns) - 1.0)

    @staticmethod
    def annualize(cumulative_return: float, years: float) -> float:
        """Annualize a cumulative return.

        Only valid for periods greater than 1 year. For periods under
        1 year, report cumulative returns only (annualizing is misleading).

        Parameters
        ----------
        cumulative_return : float
            Total cumulative return over the period.
        years : float
            Number of years in the period. Must be > 0.

        Returns
        -------
        float
            Annualized return = (1 + cumulative_return)^(1/years) - 1
        """
        if years <= 0:
            raise ValueError("years must be positive.")
        return (1.0 + cumulative_return) ** (1.0 / years) - 1.0


class MoneyWeightedReturn:
    """Compute money-weighted return (internal rate of return / IRR).

    The MWR reflects the investor's actual experience, including the
    timing and size of cash flows. Use for evaluating the investor's
    outcome (vs TWR for manager skill evaluation).

    Parameters
    ----------
    cash_flows : np.ndarray
        Array of cash flows. Convention: negative = outflow from investor
        (contribution), positive = inflow to investor (withdrawal or
        ending value). The first element is typically -beginning_value
        and the last is +ending_value.
    times : np.ndarray
        Time (in years) of each cash flow. The first is typically 0.0.
    """

    def __init__(
        self,
        cash_flows: np.ndarray,
        times: np.ndarray,
    ):
        self.cf = np.asarray(cash_flows, dtype=np.float64)
        self.times = np.asarray(times, dtype=np.float64)

        if len(self.cf) != len(self.times):
            raise ValueError("cash_flows and times must have the same length.")

    def _npv(self, rate: float) -> float:
        """Compute the net present value at a given discount rate.

        Parameters
        ----------
        rate : float
            Annual discount rate.

        Returns
        -------
        float
            NPV = sum(CF_i / (1 + rate)^t_i)
        """
        return float(np.sum(self.cf / (1.0 + rate) ** self.times))

    def compute_irr(
        self,
        lower_bound: float = -0.99,
        upper_bound: float = 10.0,
    ) -> float:
        """Compute the internal rate of return via Brent's root-finding method.

        Parameters
        ----------
        lower_bound : float, optional
            Lower bound for the IRR search. Default is -0.99 (99% loss).
        upper_bound : float, optional
            Upper bound for the IRR search. Default is 10.0 (1000% return).

        Returns
        -------
        float
            The annual IRR such that NPV(IRR) = 0.

        Raises
        ------
        ValueError
            If the root-finding algorithm does not converge.
        """
        try:
            irr = brentq(self._npv, lower_bound, upper_bound, xtol=1e-12)
        except ValueError:
            raise ValueError(
                f"IRR not found in [{lower_bound}, {upper_bound}]. "
                "Check cash flow signs and magnitudes."
            )
        return float(irr)


class CompositeReturn:
    """GIPS-compliant composite construction and return calculation.

    A composite groups portfolios with similar investment mandates.
    GIPS requires asset-weighted composite returns using beginning-of-period
    values (or beginning values plus weighted cash flows for Modified Dietz).

    Parameters
    ----------
    portfolio_returns : np.ndarray
        Array of returns for each portfolio in the composite.
    portfolio_values : np.ndarray
        Beginning-of-period market values for each portfolio (used as
        weights for asset-weighted composite return).
    """

    def __init__(
        self,
        portfolio_returns: np.ndarray,
        portfolio_values: np.ndarray,
    ):
        self.returns = np.asarray(portfolio_returns, dtype=np.float64)
        self.values = np.asarray(portfolio_values, dtype=np.float64)

        if len(self.returns) != len(self.values):
            raise ValueError(
                "portfolio_returns and portfolio_values must have the same length."
            )

    def asset_weighted_return(self) -> float:
        """Compute the asset-weighted composite return.

        Returns
        -------
        float
            R_composite = sum(w_i * R_i) where w_i = V_i / sum(V_i)
        """
        total_value = np.sum(self.values)
        if total_value == 0:
            return 0.0
        weights = self.values / total_value
        return float(np.dot(weights, self.returns))

    def equal_weighted_return(self) -> float:
        """Compute the equal-weighted composite return.

        Returns
        -------
        float
            Simple average of all portfolio returns.
        """
        if len(self.returns) == 0:
            return 0.0
        return float(np.mean(self.returns))

    def internal_dispersion(self) -> float:
        """Compute the asset-weighted internal dispersion of the composite.

        Internal dispersion measures the spread of individual portfolio
        returns around the composite return. GIPS requires disclosure of
        a measure of internal dispersion for composites with >= 6 portfolios.

        Returns
        -------
        float
            Asset-weighted standard deviation of portfolio returns around
            the composite return.
        """
        if len(self.returns) < 2:
            return 0.0
        total_value = np.sum(self.values)
        if total_value == 0:
            return 0.0
        weights = self.values / total_value
        composite_ret = self.asset_weighted_return()
        variance = float(np.dot(weights, (self.returns - composite_ret) ** 2))
        return np.sqrt(variance)

    def summary(self) -> dict:
        """Compute composite statistics.

        Returns
        -------
        dict
            Contains 'asset_weighted_return', 'equal_weighted_return',
            'internal_dispersion', 'n_portfolios', 'total_assets',
            'high_return', 'low_return'.
        """
        return {
            "asset_weighted_return": self.asset_weighted_return(),
            "equal_weighted_return": self.equal_weighted_return(),
            "internal_dispersion": self.internal_dispersion(),
            "n_portfolios": len(self.returns),
            "total_assets": float(np.sum(self.values)),
            "high_return": float(np.max(self.returns)) if len(self.returns) > 0 else 0.0,
            "low_return": float(np.min(self.returns)) if len(self.returns) > 0 else 0.0,
        }


class PeriodReturns:
    """Compute standard-period returns from a daily return series.

    Provides MTD, QTD, YTD, trailing-period, and inception-to-date returns
    with proper annualization conventions (annualize only periods > 1 year).

    Parameters
    ----------
    daily_returns : np.ndarray
        Array of daily simple returns (decimals).
    periods_per_year : int, optional
        Number of trading days per year. Default is 252.
    """

    def __init__(
        self,
        daily_returns: np.ndarray,
        periods_per_year: int = 252,
    ):
        self.daily_returns = np.asarray(daily_returns, dtype=np.float64)
        self.periods_per_year = periods_per_year

    def cumulative_return(self, returns: np.ndarray | None = None) -> float:
        """Compute the cumulative return for a return series.

        Parameters
        ----------
        returns : np.ndarray or None, optional
            Return series to compound. If None, uses the full daily series.

        Returns
        -------
        float
            prod(1 + r_t) - 1
        """
        r = np.asarray(
            returns if returns is not None else self.daily_returns,
            dtype=np.float64,
        )
        return float(np.prod(1.0 + r) - 1.0)

    def annualized_return(self, returns: np.ndarray | None = None) -> float | None:
        """Compute the annualized return for a return series.

        Returns None if the period is less than 1 year (annualizing
        short periods is misleading).

        Parameters
        ----------
        returns : np.ndarray or None, optional
            Return series. If None, uses the full daily series.

        Returns
        -------
        float or None
            (1 + cumulative)^(periods_per_year / n) - 1, or None if
            the series spans less than 1 year.
        """
        r = np.asarray(
            returns if returns is not None else self.daily_returns,
            dtype=np.float64,
        )
        n = len(r)
        if n < self.periods_per_year:
            return None
        cumulative = self.cumulative_return(r)
        years = n / self.periods_per_year
        return (1.0 + cumulative) ** (1.0 / years) - 1.0

    def trailing_return(self, n_days: int) -> float:
        """Compute the trailing cumulative return over the last n_days.

        Parameters
        ----------
        n_days : int
            Number of trailing days.

        Returns
        -------
        float
            Cumulative return over the last n_days of the series.

        Raises
        ------
        ValueError
            If n_days exceeds the available data length.
        """
        if n_days > len(self.daily_returns):
            raise ValueError(
                f"Requested {n_days} trailing days but only "
                f"{len(self.daily_returns)} days available."
            )
        subset = self.daily_returns[-n_days:]
        return self.cumulative_return(subset)

    def inception_to_date(self) -> dict:
        """Compute inception-to-date return statistics.

        Returns
        -------
        dict
            Contains 'cumulative_return', 'annualized_return' (None if
            < 1 year), 'n_days', and 'years'.
        """
        n = len(self.daily_returns)
        years = n / self.periods_per_year
        cumulative = self.cumulative_return()
        annualized = self.annualized_return()

        return {
            "cumulative_return": cumulative,
            "annualized_return": annualized,
            "n_days": n,
            "years": years,
        }

    def standard_periods(self) -> dict:
        """Compute returns for standard reporting periods.

        Computes trailing 1-month (~21 days), 3-month (~63 days),
        YTD (~252 days based on available data), 1-year, 3-year,
        5-year, and inception-to-date.

        Returns
        -------
        dict
            Dictionary of period labels to return values. Periods longer
            than available data are reported as None. Annualized returns
            are included for periods >= 1 year.
        """
        n = len(self.daily_returns)
        result = {}

        # Standard trailing periods (approximate trading days)
        period_defs = [
            ("1M", 21),
            ("3M", 63),
            ("6M", 126),
            ("1Y", 252),
            ("3Y", 756),
            ("5Y", 1260),
            ("10Y", 2520),
        ]

        for label, days in period_defs:
            if days > n:
                result[label] = {"cumulative": None, "annualized": None}
            else:
                subset = self.daily_returns[-days:]
                cum_ret = self.cumulative_return(subset)
                ann_ret = self.annualized_return(subset)
                result[label] = {"cumulative": cum_ret, "annualized": ann_ret}

        # Inception-to-date
        itd = self.inception_to_date()
        result["ITD"] = {
            "cumulative": itd["cumulative_return"],
            "annualized": itd["annualized_return"],
        }

        return result


def run_demo() -> None:
    """Run the demonstration suite (default when executed with no arguments)."""
    # ----------------------------------------------------------------
    # Demo 1: Modified Dietz return
    # ----------------------------------------------------------------
    print("=" * 60)
    print("Demo 1: Modified Dietz Return")
    print("=" * 60)

    md = ModifiedDietz(
        beginning_value=1_000_000.0,
        ending_value=1_080_000.0,
        cash_flows=np.array([50_000.0, -20_000.0]),
        cash_flow_days=np.array([10.0, 25.0]),
        total_days=30,
    )

    print(f"\nBeginning value: ${md.v_start:,.2f}")
    print(f"Ending value:    ${md.v_end:,.2f}")
    print(f"Cash flows:      {md.cf}")
    print(f"Flow days:       {md.cf_days}")
    print(f"Period days:     {md.total_days}")
    print(f"\nTime weights:    {md.weights()}")
    print(f"Weighted CFs:    ${md.weighted_cash_flows():,.2f}")
    print(f"Modified Dietz:  {md.compute_return():.6f} "
          f"({md.compute_return()*100:.4f}%)")

    # ----------------------------------------------------------------
    # Demo 2: Time-weighted return (chain-linking)
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Demo 2: Time-Weighted Return (Chain-Linking)")
    print("=" * 60)

    # 4 quarterly sub-period returns
    sub_returns = np.array([0.032, -0.015, 0.048, 0.022])
    twr = TimeWeightedReturn(sub_returns)

    cum_ret = twr.cumulative_return()
    ann_ret = TimeWeightedReturn.annualize(cum_ret, years=1.0)

    print(f"\nQuarterly returns: {sub_returns}")
    print(f"Cumulative TWR:    {cum_ret:.6f} ({cum_ret*100:.4f}%)")
    print(f"Annualized (1yr):  {ann_ret:.6f} ({ann_ret*100:.4f}%)")

    # 3-year example
    np.random.seed(42)
    monthly_returns = np.random.normal(0.007, 0.035, 36)
    twr_3y = TimeWeightedReturn(monthly_returns)
    cum_3y = twr_3y.cumulative_return()
    ann_3y = TimeWeightedReturn.annualize(cum_3y, years=3.0)
    print(f"\n3-year monthly series ({len(monthly_returns)} months):")
    print(f"  Cumulative TWR:  {cum_3y:.6f} ({cum_3y*100:.2f}%)")
    print(f"  Annualized TWR:  {ann_3y:.6f} ({ann_3y*100:.2f}%)")

    # ----------------------------------------------------------------
    # Demo 3: Money-weighted return (IRR)
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Demo 3: Money-Weighted Return (IRR)")
    print("=" * 60)

    # Investor puts in $100k at t=0, adds $50k at t=0.5y, withdraws at
    # t=1y with $165k ending value
    mwr = MoneyWeightedReturn(
        cash_flows=np.array([-100_000.0, -50_000.0, 165_000.0]),
        times=np.array([0.0, 0.5, 1.0]),
    )

    irr = mwr.compute_irr()
    print(f"\nCash flows: {mwr.cf}")
    print(f"Times (yr): {mwr.times}")
    print(f"IRR:        {irr:.6f} ({irr*100:.4f}%)")

    # Verification: NPV at the IRR should be ~0
    npv_check = mwr._npv(irr)
    print(f"NPV at IRR: ${npv_check:.6f} (should be ~0)")

    # ----------------------------------------------------------------
    # Demo 4: GIPS composite construction
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Demo 4: GIPS Composite Construction")
    print("=" * 60)

    comp = CompositeReturn(
        portfolio_returns=np.array([0.082, 0.075, 0.091, 0.068, 0.078,
                                    0.085, 0.072, 0.088]),
        portfolio_values=np.array([5_000_000, 3_200_000, 8_100_000,
                                   1_500_000, 2_800_000, 4_300_000,
                                   2_100_000, 6_500_000]),
    )

    comp_result = comp.summary()
    print(f"\nComposite: {comp_result['n_portfolios']} portfolios, "
          f"${comp_result['total_assets']:,.0f} total assets")
    print(f"Asset-weighted return: {comp_result['asset_weighted_return']*100:.4f}%")
    print(f"Equal-weighted return: {comp_result['equal_weighted_return']*100:.4f}%")
    print(f"Internal dispersion:   {comp_result['internal_dispersion']*100:.4f}%")
    print(f"Highest portfolio:     {comp_result['high_return']*100:.4f}%")
    print(f"Lowest portfolio:      {comp_result['low_return']*100:.4f}%")

    # ----------------------------------------------------------------
    # Demo 5: Standard period returns
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Demo 5: Standard Period Returns")
    print("=" * 60)

    np.random.seed(123)
    # 3 years of daily returns
    n_days = 756
    daily_rets = np.random.normal(0.0003, 0.012, n_days)

    pr = PeriodReturns(daily_returns=daily_rets, periods_per_year=252)
    periods = pr.standard_periods()

    print(f"\nReturn series: {n_days} trading days "
          f"({n_days/252:.1f} years)")
    print(f"\n{'Period':<8} {'Cumulative':>12} {'Annualized':>12}")
    print("-" * 34)
    for label, vals in periods.items():
        cum_str = (f"{vals['cumulative']*100:.2f}%"
                   if vals["cumulative"] is not None else "N/A")
        ann_str = (f"{vals['annualized']*100:.2f}%"
                   if vals["annualized"] is not None else "N/A")
        print(f"{label:<8} {cum_str:>12} {ann_str:>12}")

    itd = pr.inception_to_date()
    print(f"\nInception-to-date detail:")
    print(f"  Days:       {itd['n_days']}")
    print(f"  Years:      {itd['years']:.2f}")
    print(f"  Cumulative: {itd['cumulative_return']*100:.2f}%")
    if itd["annualized_return"] is not None:
        print(f"  Annualized: {itd['annualized_return']*100:.2f}%")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)


def run_verify() -> int:
    """Re-run the demo computations and assert their key outputs.

    Returns
    -------
    int
        0 if all checks pass, 1 otherwise.
    """
    failures = 0

    def check(name: str, actual: float, expected: float,
              rel_tol: float = 1e-6, abs_tol: float = 1e-9) -> None:
        nonlocal failures
        ok = math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=abs_tol)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name}: actual={actual:.10g} expected={expected:.10g}")
        if not ok:
            failures += 1

    # Demo 1: Modified Dietz
    md = ModifiedDietz(
        beginning_value=1_000_000.0,
        ending_value=1_080_000.0,
        cash_flows=np.array([50_000.0, -20_000.0]),
        cash_flow_days=np.array([10.0, 25.0]),
        total_days=30,
    )
    check("Modified Dietz weighted cash flows", md.weighted_cash_flows(), 30_000.0)
    check("Modified Dietz return", md.compute_return(), 0.0485436893)

    # Demo 2: chain-linked TWR
    twr = TimeWeightedReturn(np.array([0.032, -0.015, 0.048, 0.022]))
    cum_ret = twr.cumulative_return()
    check("Cumulative TWR", cum_ret, 0.0887498451)
    check("Annualized TWR (1yr)", TimeWeightedReturn.annualize(cum_ret, 1.0),
          0.0887498451)

    np.random.seed(42)
    monthly_returns = np.random.normal(0.007, 0.035, 36)
    twr_3y = TimeWeightedReturn(monthly_returns)
    cum_3y = twr_3y.cumulative_return()
    check("3-year cumulative TWR (seeded)", cum_3y, 0.0285067234)
    check("3-year annualized TWR (seeded)",
          TimeWeightedReturn.annualize(cum_3y, 3.0), 0.0094133519)

    # Demo 3: IRR via Brent's method
    mwr = MoneyWeightedReturn(
        cash_flows=np.array([-100_000.0, -50_000.0, 165_000.0]),
        times=np.array([0.0, 0.5, 1.0]),
    )
    irr = mwr.compute_irr()
    check("IRR", irr, 0.1206873836)
    check("NPV at IRR", mwr._npv(irr), 0.0, abs_tol=1e-4)

    # Demo 4: GIPS composite
    comp = CompositeReturn(
        portfolio_returns=np.array([0.082, 0.075, 0.091, 0.068, 0.078,
                                    0.085, 0.072, 0.088]),
        portfolio_values=np.array([5_000_000, 3_200_000, 8_100_000,
                                   1_500_000, 2_800_000, 4_300_000,
                                   2_100_000, 6_500_000]),
    )
    check("Composite asset-weighted return", comp.asset_weighted_return(),
          0.0834686567)
    check("Composite equal-weighted return", comp.equal_weighted_return(),
          0.079875)
    check("Composite internal dispersion", comp.internal_dispersion(),
          0.0068286973)

    # Demo 5: standard period returns (seeded)
    np.random.seed(123)
    daily_rets = np.random.normal(0.0003, 0.012, 756)
    pr = PeriodReturns(daily_returns=daily_rets, periods_per_year=252)
    itd = pr.inception_to_date()
    check("ITD cumulative return (seeded)", itd["cumulative_return"],
          0.2634802003)
    check("ITD annualized return (seeded)", itd["annualized_return"],
          0.0810758028)

    if failures:
        print(f"\nFAIL: {failures} check(s) did not match expected values.")
        return 1
    print("\nPASS: all checks matched expected values.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Performance reporting calculations: Modified Dietz time-weighted "
            "returns (ModifiedDietz), chain-linked TWR (TimeWeightedReturn), "
            "IRR via Brent's method (MoneyWeightedReturn), GIPS composite "
            "returns (CompositeReturn), and standard period returns "
            "(PeriodReturns)."
        ),
        epilog=(
            "Run with no arguments to print the demo suite. "
            "Import as a module: "
            "from performance_reporting import ModifiedDietz, "
            "TimeWeightedReturn, MoneyWeightedReturn, CompositeReturn, "
            "PeriodReturns"
        ),
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="run the demo computations and assert key outputs; "
             "exits nonzero on mismatch",
    )
    args = parser.parse_args()

    if args.verify:
        sys.exit(run_verify())
    run_demo()


if __name__ == "__main__":
    main()
