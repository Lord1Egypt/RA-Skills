# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.11"
# ///
"""
Fund Vehicle Analysis
=====================
Expense ratio impact on long-term returns, tracking error calculation,
premium/discount to NAV, fund overlap analysis, and tax cost ratio.

Part of Layer 2 (Asset Classes) in the finance skills framework.
"""

import argparse
import math
import sys

import numpy as np


class ExpenseAnalysis:
    """Analyze the impact of fund expenses on long-term wealth accumulation.

    Provides static methods for computing fee drag, comparing fund costs,
    and projecting terminal values under different expense scenarios.
    """

    @staticmethod
    def fee_impact(
        initial_value: float,
        gross_return: float,
        expense_ratio: float,
        years: int,
    ) -> dict[str, float]:
        """Compute the long-term impact of an expense ratio on wealth.

        FV = PV * (1 + r - ER)^n

        Parameters
        ----------
        initial_value : float
            Starting investment amount. Must be positive.
        gross_return : float
            Annual gross return before expenses (decimal).
        expense_ratio : float
            Annual expense ratio (decimal, e.g., 0.0075 for 75bps).
        years : int
            Investment horizon in years. Must be positive.

        Returns
        -------
        dict[str, float]
            Keys: 'terminal_value' (after expenses), 'gross_terminal_value'
            (without expenses), 'total_fee_drag' (dollar amount lost to fees),
            'fee_drag_pct' (fee drag as fraction of gross terminal value).
        """
        if initial_value <= 0:
            raise ValueError(f"initial_value must be positive, got {initial_value}.")
        if years <= 0:
            raise ValueError(f"years must be positive, got {years}.")

        net_return = gross_return - expense_ratio
        terminal = initial_value * (1.0 + net_return) ** years
        gross_terminal = initial_value * (1.0 + gross_return) ** years
        fee_drag = gross_terminal - terminal

        return {
            "terminal_value": terminal,
            "gross_terminal_value": gross_terminal,
            "total_fee_drag": fee_drag,
            "fee_drag_pct": fee_drag / gross_terminal if gross_terminal > 0 else 0.0,
        }

    @staticmethod
    def compare_funds(
        initial_value: float,
        gross_return: float,
        expense_ratios: list[float],
        fund_names: list[str],
        years: int,
    ) -> list[dict]:
        """Compare the terminal value impact of multiple expense ratios.

        Parameters
        ----------
        initial_value : float
            Starting investment amount. Must be positive.
        gross_return : float
            Annual gross return before expenses (decimal).
        expense_ratios : list[float]
            Expense ratio for each fund (decimal).
        fund_names : list[str]
            Name for each fund.
        years : int
            Investment horizon in years.

        Returns
        -------
        list[dict]
            Each dict has keys: 'name', 'expense_ratio', 'terminal_value',
            'fee_drag_vs_cheapest' (dollar cost vs the lowest-cost fund).
        """
        if len(expense_ratios) != len(fund_names):
            raise ValueError("expense_ratios and fund_names must have equal length.")

        results = []
        for name, er in zip(fund_names, expense_ratios):
            net_return = gross_return - er
            terminal = initial_value * (1.0 + net_return) ** years
            results.append({
                "name": name,
                "expense_ratio": er,
                "terminal_value": terminal,
            })

        # Compute drag relative to cheapest fund
        max_terminal = max(r["terminal_value"] for r in results)
        for r in results:
            r["fee_drag_vs_cheapest"] = max_terminal - r["terminal_value"]

        return results

    @staticmethod
    def breakeven_years(
        expense_ratio_a: float,
        expense_ratio_b: float,
        alpha_a: float,
        gross_return: float = 0.08,
    ) -> float | None:
        """Compute years until a higher-cost active fund (A) breaks even vs
        a cheaper passive fund (B), given expected alpha for fund A.

        Fund A net return = gross_return + alpha_a - expense_ratio_a
        Fund B net return = gross_return - expense_ratio_b

        Break-even: (1 + net_A)^n = (1 + net_B)^n
        This only has a solution if net_A > net_B (alpha exceeds fee gap).
        If net_A <= net_B, returns None (active fund never catches up).

        Parameters
        ----------
        expense_ratio_a : float
            Expense ratio of active fund (decimal).
        expense_ratio_b : float
            Expense ratio of passive fund (decimal).
        alpha_a : float
            Expected annual alpha for the active fund (decimal).
        gross_return : float, optional
            Gross market return (decimal). Default is 0.08.

        Returns
        -------
        float or None
            Break-even years, or None if active fund never overcomes costs.
        """
        net_a = gross_return + alpha_a - expense_ratio_a
        net_b = gross_return - expense_ratio_b
        if net_a <= net_b:
            return None
        # Fund A is always ahead from year 1 if net_a > net_b
        # The "break-even" concept applies when there is an upfront cost;
        # with ongoing ER differences and alpha, A leads from the start.
        # Return 0 to indicate immediate dominance.
        return 0.0


class TrackingAnalysis:
    """Tracking error and tracking difference calculations for index funds.

    Parameters
    ----------
    fund_returns : np.ndarray
        Array of periodic fund returns (decimals).
    index_returns : np.ndarray
        Array of periodic benchmark index returns (decimals).
    periods_per_year : int, optional
        Number of periods in a year for annualization. Default is 252.
    """

    def __init__(
        self,
        fund_returns: np.ndarray,
        index_returns: np.ndarray,
        periods_per_year: int = 252,
    ):
        self.fund_returns = np.asarray(fund_returns, dtype=np.float64)
        self.index_returns = np.asarray(index_returns, dtype=np.float64)
        if len(self.fund_returns) != len(self.index_returns):
            raise ValueError(
                f"fund_returns length ({len(self.fund_returns)}) must match "
                f"index_returns length ({len(self.index_returns)})."
            )
        self.periods_per_year = periods_per_year

    def tracking_difference(self) -> float:
        """Compute cumulative tracking difference.

        Tracking Difference = Cumulative Fund Return - Cumulative Index Return

        Returns
        -------
        float
            Tracking difference (decimal). Negative means the fund
            underperformed the index.
        """
        fund_cumul = float(np.prod(1.0 + self.fund_returns) - 1.0)
        index_cumul = float(np.prod(1.0 + self.index_returns) - 1.0)
        return fund_cumul - index_cumul

    def tracking_error(self) -> float:
        """Compute annualized tracking error.

        TE = std(R_fund - R_index) * sqrt(periods_per_year)

        Returns
        -------
        float
            Annualized tracking error (decimal).
        """
        active_returns = self.fund_returns - self.index_returns
        return float(np.std(active_returns, ddof=1) * np.sqrt(self.periods_per_year))

    def mean_active_return(self) -> float:
        """Compute mean periodic active return (fund - index).

        Returns
        -------
        float
            Mean active return per period (decimal).
        """
        return float(np.mean(self.fund_returns - self.index_returns))

    def information_ratio(self) -> float:
        """Compute the annualized information ratio.

        IR = mean(active return) / std(active return) * sqrt(periods_per_year)

        Returns
        -------
        float
            Annualized information ratio.
        """
        active_returns = self.fund_returns - self.index_returns
        te = np.std(active_returns, ddof=1)
        if te == 0:
            return 0.0
        return float((np.mean(active_returns) / te) * np.sqrt(self.periods_per_year))


class NAVAnalysis:
    """Premium/discount to NAV analysis for ETFs and closed-end funds."""

    @staticmethod
    def nav_per_share(
        total_assets: float,
        liabilities: float,
        shares_outstanding: float,
    ) -> float:
        """Compute net asset value per share.

        NAV = (Total Assets - Liabilities) / Shares Outstanding

        Parameters
        ----------
        total_assets : float
            Total fund assets.
        liabilities : float
            Total fund liabilities.
        shares_outstanding : float
            Number of shares outstanding. Must be positive.

        Returns
        -------
        float
            NAV per share.
        """
        if shares_outstanding <= 0:
            raise ValueError(
                f"shares_outstanding must be positive, got {shares_outstanding}."
            )
        return (total_assets - liabilities) / shares_outstanding

    @staticmethod
    def premium_discount(market_price: float, nav: float) -> float:
        """Compute the premium or discount to NAV.

        Premium/Discount = (Market Price - NAV) / NAV

        Parameters
        ----------
        market_price : float
            Current market trading price.
        nav : float
            Net asset value per share. Must be positive.

        Returns
        -------
        float
            Premium (positive) or discount (negative) as a decimal.
        """
        if nav <= 0:
            raise ValueError(f"NAV must be positive, got {nav}.")
        return (market_price - nav) / nav

    @staticmethod
    def premium_discount_series(
        market_prices: np.ndarray,
        navs: np.ndarray,
    ) -> dict:
        """Compute premium/discount statistics over a time series.

        Parameters
        ----------
        market_prices : np.ndarray
            Array of market prices.
        navs : np.ndarray
            Array of corresponding NAVs.

        Returns
        -------
        dict
            Keys: 'premiums' (np.ndarray), 'mean_premium' (float),
            'std_premium' (float), 'max_premium' (float),
            'max_discount' (float — most negative value).
        """
        market_prices = np.asarray(market_prices, dtype=np.float64)
        navs = np.asarray(navs, dtype=np.float64)
        premiums = (market_prices - navs) / navs
        return {
            "premiums": premiums,
            "mean_premium": float(np.mean(premiums)),
            "std_premium": float(np.std(premiums, ddof=1)),
            "max_premium": float(np.max(premiums)),
            "max_discount": float(np.min(premiums)),
        }


class FundOverlap:
    """Analyze holdings overlap between two funds."""

    @staticmethod
    def overlap_coefficient(
        holdings_a: dict[str, float],
        holdings_b: dict[str, float],
    ) -> float:
        """Compute portfolio overlap using the minimum-weight method.

        Overlap = sum over all shared holdings of min(w_a_i, w_b_i)

        Parameters
        ----------
        holdings_a : dict[str, float]
            Mapping of security identifier to weight in fund A (decimals).
        holdings_b : dict[str, float]
            Mapping of security identifier to weight in fund B (decimals).

        Returns
        -------
        float
            Overlap coefficient (0 to 1). 0 = no overlap, 1 = identical.
        """
        shared = set(holdings_a) & set(holdings_b)
        return sum(min(holdings_a[s], holdings_b[s]) for s in shared)

    @staticmethod
    def overlap_detail(
        holdings_a: dict[str, float],
        holdings_b: dict[str, float],
    ) -> dict:
        """Detailed overlap analysis between two funds.

        Parameters
        ----------
        holdings_a : dict[str, float]
            Fund A holdings (security -> weight).
        holdings_b : dict[str, float]
            Fund B holdings (security -> weight).

        Returns
        -------
        dict
            Keys: 'overlap_coefficient' (float), 'shared_count' (int),
            'unique_to_a' (int), 'unique_to_b' (int),
            'total_unique' (int), 'shared_weight_a' (float — total weight
            in A of shared holdings), 'shared_weight_b' (float).
        """
        set_a = set(holdings_a)
        set_b = set(holdings_b)
        shared = set_a & set_b

        overlap = sum(min(holdings_a[s], holdings_b[s]) for s in shared)
        shared_w_a = sum(holdings_a[s] for s in shared)
        shared_w_b = sum(holdings_b[s] for s in shared)

        return {
            "overlap_coefficient": overlap,
            "shared_count": len(shared),
            "unique_to_a": len(set_a - set_b),
            "unique_to_b": len(set_b - set_a),
            "total_unique": len(set_a | set_b),
            "shared_weight_a": shared_w_a,
            "shared_weight_b": shared_w_b,
        }


class TaxEfficiency:
    """Tax cost ratio and after-tax return analysis."""

    @staticmethod
    def tax_cost_ratio(
        pretax_return: float,
        aftertax_return: float,
    ) -> float:
        """Compute the tax cost ratio.

        Tax Cost Ratio = 1 - (1 + After-Tax Return) / (1 + Pre-Tax Return)

        Alternatively: Pre-Tax Return - After-Tax Return (simplified).

        Parameters
        ----------
        pretax_return : float
            Pre-tax return over the period (decimal).
        aftertax_return : float
            After-tax return over the period (decimal).

        Returns
        -------
        float
            Tax cost ratio (decimal). Higher values indicate lower
            tax efficiency.
        """
        return 1.0 - (1.0 + aftertax_return) / (1.0 + pretax_return)

    @staticmethod
    def aftertax_return_with_distributions(
        gross_return: float,
        expense_ratio: float,
        distribution_rate: float,
        tax_rate: float,
    ) -> float:
        """Estimate after-tax return accounting for annual distributions.

        Net Return = Gross - ER - (Distribution Rate * Tax Rate)

        Parameters
        ----------
        gross_return : float
            Annual gross return (decimal).
        expense_ratio : float
            Annual expense ratio (decimal).
        distribution_rate : float
            Capital gains distribution as a fraction of NAV (decimal).
        tax_rate : float
            Tax rate on distributions (decimal).

        Returns
        -------
        float
            Estimated after-tax annual return (decimal).
        """
        return gross_return - expense_ratio - (distribution_rate * tax_rate)

    @staticmethod
    def deferred_vs_annual_tax(
        initial_value: float,
        gross_return: float,
        expense_ratio: float,
        distribution_rate: float,
        tax_rate: float,
        years: int,
    ) -> dict[str, float]:
        """Compare tax-deferred (ETF-style) vs annual distribution (mutual fund-style).

        Parameters
        ----------
        initial_value : float
            Starting investment amount.
        gross_return : float
            Annual gross return (decimal).
        expense_ratio : float
            Annual expense ratio (decimal, same for both).
        distribution_rate : float
            Annual capital gains distribution rate for the mutual fund (decimal).
        tax_rate : float
            Tax rate on capital gains (decimal).
        years : int
            Investment horizon in years.

        Both vehicles grow at (gross_return - expense_ratio) before
        distribution taxes. The ETF distributes nothing; its gain over the
        original basis is taxed once at liquidation. The mutual fund
        distributes ``distribution_rate`` of NAV at each year-end; the
        distribution is taxed at ``tax_rate`` and the after-tax remainder
        is reinvested (adding to cost basis). At liquidation the remaining
        unrealized gain (terminal value minus accumulated basis) is taxed.

        Returns
        -------
        dict[str, float]
            Keys: 'etf_pretax_terminal', 'etf_aftertax_terminal'
            (after liquidation tax), 'mf_pretax_terminal' (pre-liquidation
            value), 'mf_cost_basis', 'mf_distribution_taxes_paid',
            'mf_aftertax_terminal', 'tax_advantage' (after-tax dollar
            benefit of deferral).
        """
        net_return = gross_return - expense_ratio

        # ETF: all gains deferred until liquidation
        etf_pretax = initial_value * (1.0 + net_return) ** years
        etf_gain = etf_pretax - initial_value
        etf_aftertax = etf_pretax - (etf_gain * tax_rate)

        # Mutual fund: year-by-year distributions, taxed and reinvested
        value = initial_value
        basis = initial_value
        distribution_taxes = 0.0
        for _ in range(years):
            value *= 1.0 + net_return
            distribution = distribution_rate * value
            tax = distribution * tax_rate
            value -= tax                 # after-tax distribution reinvested
            basis += distribution - tax  # reinvestment adds to cost basis
            distribution_taxes += tax

        liquidation_tax = max(value - basis, 0.0) * tax_rate
        mf_aftertax = value - liquidation_tax

        return {
            "etf_pretax_terminal": etf_pretax,
            "etf_aftertax_terminal": etf_aftertax,
            "mf_pretax_terminal": value,
            "mf_cost_basis": basis,
            "mf_distribution_taxes_paid": distribution_taxes,
            "mf_aftertax_terminal": mf_aftertax,
            "tax_advantage": etf_aftertax - mf_aftertax,
        }


def _demo() -> None:
    """Run the demonstration calculations (bare-run default)."""
    np.random.seed(42)

    print("=" * 60)
    print("Fund Vehicle Analysis - Demo")
    print("=" * 60)

    # --- Expense Ratio Impact (Example 1 from SKILL.md) ---
    print("\n--- Expense Ratio Impact (30-year, $100,000) ---")
    impact_a = ExpenseAnalysis.fee_impact(
        initial_value=100_000, gross_return=0.08,
        expense_ratio=0.0003, years=30,
    )
    impact_b = ExpenseAnalysis.fee_impact(
        initial_value=100_000, gross_return=0.08,
        expense_ratio=0.0075, years=30,
    )
    print(f"Fund A (0.03% ER): ${impact_a['terminal_value']:,.0f}")
    print(f"Fund B (0.75% ER): ${impact_b['terminal_value']:,.0f}")
    print(f"Difference: ${impact_a['terminal_value'] - impact_b['terminal_value']:,.0f}")

    comparison = ExpenseAnalysis.compare_funds(
        initial_value=100_000, gross_return=0.08,
        expense_ratios=[0.0003, 0.0020, 0.0075, 0.0120],
        fund_names=["Vanguard (3bps)", "iShares (20bps)", "Active A (75bps)", "Active B (120bps)"],
        years=30,
    )
    print("\nFund Comparison (30 years):")
    for fund in comparison:
        print(f"  {fund['name']:25s}: ${fund['terminal_value']:>12,.0f} "
              f"(fee drag: ${fund['fee_drag_vs_cheapest']:>10,.0f})")

    # --- Tracking Error ---
    print("\n--- Tracking Error Analysis ---")
    n_days = 504
    index_rets = np.random.normal(0.0003, 0.011, n_days)
    # Fund slightly lags index due to expenses and cash drag
    fund_rets = index_rets - 0.0001 + np.random.normal(0, 0.0003, n_days)

    ta = TrackingAnalysis(
        fund_returns=fund_rets, index_returns=index_rets, periods_per_year=252
    )
    print(f"Tracking difference: {ta.tracking_difference():.4f} ({ta.tracking_difference()*100:.2f}%)")
    print(f"Tracking error (ann.): {ta.tracking_error():.4f} ({ta.tracking_error()*100:.2f}%)")
    print(f"Mean active return (daily): {ta.mean_active_return():.6f}")
    print(f"Information ratio: {ta.information_ratio():.4f}")

    # --- Premium/Discount to NAV ---
    print("\n--- NAV Premium/Discount ---")
    nav = NAVAnalysis.nav_per_share(
        total_assets=1_000_000_000, liabilities=5_000_000,
        shares_outstanding=40_000_000,
    )
    market_price = 25.10
    pd_val = NAVAnalysis.premium_discount(market_price=market_price, nav=nav)
    print(f"NAV per share: ${nav:.2f}")
    print(f"Market price:  ${market_price:.2f}")
    print(f"Premium/Discount: {pd_val:.4f} ({pd_val*100:.2f}%)")

    # Simulate premium/discount time series
    navs = 25.0 + np.cumsum(np.random.normal(0.01, 0.2, 252))
    prices = navs + np.random.normal(0.0, 0.10, 252)
    pd_stats = NAVAnalysis.premium_discount_series(market_prices=prices, navs=navs)
    print(f"\n252-day premium/discount stats:")
    print(f"  Mean:     {pd_stats['mean_premium']:.4f} ({pd_stats['mean_premium']*100:.3f}%)")
    print(f"  Std dev:  {pd_stats['std_premium']:.4f}")
    print(f"  Max prem: {pd_stats['max_premium']:.4f} ({pd_stats['max_premium']*100:.3f}%)")
    print(f"  Max disc: {pd_stats['max_discount']:.4f} ({pd_stats['max_discount']*100:.3f}%)")

    # --- Fund Overlap ---
    print("\n--- Fund Overlap Analysis ---")
    fund_spy = {"AAPL": 0.07, "MSFT": 0.06, "AMZN": 0.03, "GOOGL": 0.02,
                "NVDA": 0.03, "META": 0.02, "BRK.B": 0.02, "JPM": 0.01,
                "JNJ": 0.01, "V": 0.01}
    fund_qqq = {"AAPL": 0.12, "MSFT": 0.10, "AMZN": 0.06, "GOOGL": 0.04,
                "NVDA": 0.05, "META": 0.04, "AVGO": 0.03, "TSLA": 0.03,
                "COST": 0.02, "ADBE": 0.02}

    detail = FundOverlap.overlap_detail(holdings_a=fund_spy, holdings_b=fund_qqq)
    print(f"SPY vs QQQ (top 10 holdings each):")
    print(f"  Overlap coefficient: {detail['overlap_coefficient']:.4f}")
    print(f"  Shared holdings:     {detail['shared_count']}")
    print(f"  Unique to SPY:       {detail['unique_to_a']}")
    print(f"  Unique to QQQ:       {detail['unique_to_b']}")
    print(f"  Shared weight (SPY): {detail['shared_weight_a']:.4f}")
    print(f"  Shared weight (QQQ): {detail['shared_weight_b']:.4f}")

    # --- Tax Efficiency (Example 2 from SKILL.md) ---
    print("\n--- Tax Efficiency (ETF vs Mutual Fund) ---")
    tax_result = TaxEfficiency.deferred_vs_annual_tax(
        initial_value=100_000, gross_return=0.10,
        expense_ratio=0.0003, distribution_rate=0.02,
        tax_rate=0.20, years=20,
    )
    print(f"ETF pre-tax terminal:    ${tax_result['etf_pretax_terminal']:,.0f}")
    print(f"ETF after-tax terminal:  ${tax_result['etf_aftertax_terminal']:,.0f}")
    print(f"MF pre-liquidation:      ${tax_result['mf_pretax_terminal']:,.0f}")
    print(f"MF cost basis:           ${tax_result['mf_cost_basis']:,.0f}")
    print(f"MF distribution taxes:   ${tax_result['mf_distribution_taxes_paid']:,.0f}")
    print(f"MF after-tax terminal:   ${tax_result['mf_aftertax_terminal']:,.0f}")
    print(f"ETF tax advantage:       ${tax_result['tax_advantage']:,.0f}")

    tcr = TaxEfficiency.tax_cost_ratio(pretax_return=0.10, aftertax_return=0.092)
    print(f"\nTax cost ratio (10% pretax, 9.2% after-tax): {tcr:.4f} ({tcr*100:.2f}%)")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)


def _verify() -> None:
    """Assert demo computations against the SKILL.md worked examples."""
    checks: list[tuple[str, float, float]] = []

    # SKILL.md Example 1: $100,000, 30 years, 8% gross
    impact_a = ExpenseAnalysis.fee_impact(
        initial_value=100_000, gross_return=0.08, expense_ratio=0.0003, years=30,
    )
    impact_b = ExpenseAnalysis.fee_impact(
        initial_value=100_000, gross_return=0.08, expense_ratio=0.0075, years=30,
    )
    checks.append(("Example 1 Fund A terminal", impact_a["terminal_value"], 997_914.0))
    checks.append(("Example 1 Fund B terminal", impact_b["terminal_value"], 816_430.0))
    checks.append((
        "Example 1 difference",
        impact_a["terminal_value"] - impact_b["terminal_value"],
        181_484.0,
    ))

    # SKILL.md Example 2: ETF vs mutual fund, $100,000, 20 years
    tax_result = TaxEfficiency.deferred_vs_annual_tax(
        initial_value=100_000, gross_return=0.10,
        expense_ratio=0.0003, distribution_rate=0.02,
        tax_rate=0.20, years=20,
    )
    checks.append(("Example 2 ETF pre-tax", tax_result["etf_pretax_terminal"], 669_090.0))
    checks.append(("Example 2 ETF after-tax", tax_result["etf_aftertax_terminal"], 555_272.0))
    checks.append(("Example 2 MF pre-liquidation", tax_result["mf_pretax_terminal"], 617_549.0))
    checks.append(("Example 2 MF cost basis", tax_result["mf_cost_basis"], 195_554.0))
    checks.append((
        "Example 2 MF distribution taxes",
        tax_result["mf_distribution_taxes_paid"],
        23_888.0,
    ))
    checks.append(("Example 2 MF after-tax", tax_result["mf_aftertax_terminal"], 533_150.0))
    checks.append(("Example 2 ETF tax advantage", tax_result["tax_advantage"], 22_122.0))

    # Demo tax cost ratio: 1 - 1.092/1.10
    checks.append((
        "Demo tax cost ratio",
        TaxEfficiency.tax_cost_ratio(0.10, 0.092),
        0.0072727,
    ))

    failures = 0
    for name, got, expected in checks:
        ok = math.isclose(got, expected, rel_tol=1e-4)
        print(f"{'PASS' if ok else 'FAIL'}: {name}: got {got:,.6g}, expected {expected:,.6g}")
        failures += 0 if ok else 1
    if failures:
        print(f"FAIL: {failures} of {len(checks)} checks failed.")
        sys.exit(1)
    print(f"PASS: all {len(checks)} checks passed.")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fund_vehicles.py",
        description=(
            "Fund vehicle analysis reference implementation. Main classes: "
            "ExpenseAnalysis (fee_impact, compare_funds, breakeven_years), "
            "TrackingAnalysis (tracking_difference, tracking_error, "
            "information_ratio), NAVAnalysis (nav_per_share, "
            "premium_discount, premium_discount_series), FundOverlap "
            "(overlap_coefficient, overlap_detail), TaxEfficiency "
            "(tax_cost_ratio, aftertax_return_with_distributions, "
            "deferred_vs_annual_tax)."
        ),
        epilog=(
            "Primarily intended to be imported as a module: "
            "from fund_vehicles import ExpenseAnalysis, TrackingAnalysis, "
            "NAVAnalysis, FundOverlap, TaxEfficiency. "
            "Run with no arguments to print a demo."
        ),
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help=(
            "run the demo computations and assert key outputs match the "
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
