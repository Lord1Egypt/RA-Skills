# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.11"
# ///
"""
Real Asset Analysis
===================
Cap rate, NOI calculation, cash-on-cash return, REIT FFO/AFFO yield,
property valuation, leverage metrics, and inflation-adjusted real return.

Part of Layer 2 (Asset Classes) in the finance skills framework.
"""

import argparse
import math
import sys

import numpy as np


class PropertyValuation:
    """Real estate property valuation using income-based methods.

    All methods are static — each calculation is self-contained.
    """

    @staticmethod
    def noi(
        gross_rental_income: float,
        operating_expenses: float,
        vacancy_rate: float = 0.0,
    ) -> float:
        """Compute Net Operating Income.

        NOI = Effective Gross Income - Operating Expenses
        Effective Gross Income = Gross Rental Income * (1 - Vacancy Rate)

        Parameters
        ----------
        gross_rental_income : float
            Annual gross potential rental income.
        operating_expenses : float
            Annual operating expenses (taxes, insurance, maintenance,
            management). Excludes debt service, capex, and depreciation.
        vacancy_rate : float, optional
            Expected vacancy rate (decimal, e.g., 0.05 for 5%). Default is 0.

        Returns
        -------
        float
            Net Operating Income.
        """
        effective_gross = gross_rental_income * (1.0 - vacancy_rate)
        return effective_gross - operating_expenses

    @staticmethod
    def cap_rate(noi: float, property_value: float) -> float:
        """Compute the capitalization rate.

        Cap Rate = NOI / Property Value

        Parameters
        ----------
        noi : float
            Net Operating Income.
        property_value : float
            Current property value or purchase price. Must be positive.

        Returns
        -------
        float
            Cap rate (decimal).
        """
        if property_value <= 0:
            raise ValueError(
                f"property_value must be positive, got {property_value}."
            )
        return noi / property_value

    @staticmethod
    def value_from_cap_rate(noi: float, cap_rate: float) -> float:
        """Compute property value using the income approach.

        Value = NOI / Cap Rate

        Parameters
        ----------
        noi : float
            Net Operating Income.
        cap_rate : float
            Capitalization rate (decimal). Must be positive.

        Returns
        -------
        float
            Estimated property value.
        """
        if cap_rate <= 0:
            raise ValueError(f"cap_rate must be positive, got {cap_rate}.")
        return noi / cap_rate

    @staticmethod
    def gross_rent_multiplier(
        property_price: float,
        gross_annual_rent: float,
    ) -> float:
        """Compute the Gross Rent Multiplier.

        GRM = Property Price / Gross Annual Rental Income

        Parameters
        ----------
        property_price : float
            Purchase price or current value.
        gross_annual_rent : float
            Gross annual rental income. Must be positive.

        Returns
        -------
        float
            Gross Rent Multiplier (lower = potentially better value).
        """
        if gross_annual_rent <= 0:
            raise ValueError(
                f"gross_annual_rent must be positive, got {gross_annual_rent}."
            )
        return property_price / gross_annual_rent

    @staticmethod
    def cash_on_cash_return(
        annual_pretax_cash_flow: float,
        total_cash_invested: float,
    ) -> float:
        """Compute the cash-on-cash return.

        Cash-on-Cash = Annual Pre-Tax Cash Flow / Total Cash Invested

        Pre-tax cash flow = NOI - Annual Debt Service.

        Parameters
        ----------
        annual_pretax_cash_flow : float
            Annual cash flow after debt service but before taxes.
        total_cash_invested : float
            Total equity invested (down payment + closing costs).
            Must be positive.

        Returns
        -------
        float
            Cash-on-cash return (decimal).
        """
        if total_cash_invested <= 0:
            raise ValueError(
                f"total_cash_invested must be positive, got {total_cash_invested}."
            )
        return annual_pretax_cash_flow / total_cash_invested


class LeverageMetrics:
    """Real estate leverage and debt coverage analysis."""

    @staticmethod
    def loan_to_value(loan_amount: float, property_value: float) -> float:
        """Compute the Loan-to-Value ratio.

        LTV = Loan Amount / Property Value

        Parameters
        ----------
        loan_amount : float
            Mortgage or loan balance.
        property_value : float
            Current property value. Must be positive.

        Returns
        -------
        float
            LTV ratio (decimal). Typical commercial range: 0.60-0.75.
        """
        if property_value <= 0:
            raise ValueError(
                f"property_value must be positive, got {property_value}."
            )
        return loan_amount / property_value

    @staticmethod
    def debt_service_coverage(
        noi: float,
        annual_debt_service: float,
    ) -> float:
        """Compute the Debt Service Coverage Ratio.

        DSCR = NOI / Annual Debt Service

        Parameters
        ----------
        noi : float
            Net Operating Income.
        annual_debt_service : float
            Total annual mortgage payments (principal + interest).
            Must be positive.

        Returns
        -------
        float
            DSCR. Lenders typically require 1.20x-1.50x minimum.
        """
        if annual_debt_service <= 0:
            raise ValueError(
                f"annual_debt_service must be positive, got {annual_debt_service}."
            )
        return noi / annual_debt_service

    @staticmethod
    def levered_vs_unlevered(
        property_value: float,
        noi: float,
        loan_amount: float,
        annual_debt_service: float,
    ) -> dict[str, float]:
        """Compare levered and unlevered returns.

        Positive leverage: cost of debt < cap rate (leverage boosts returns).
        Negative leverage: cost of debt > cap rate (leverage reduces returns).

        Parameters
        ----------
        property_value : float
            Current property value.
        noi : float
            Net Operating Income.
        loan_amount : float
            Mortgage balance.
        annual_debt_service : float
            Annual debt service (P&I).

        Returns
        -------
        dict[str, float]
            Keys: 'cap_rate', 'cash_on_cash', 'equity_invested',
            'leverage_effect' (cash_on_cash - cap_rate).
        """
        equity = property_value - loan_amount
        cap = noi / property_value if property_value > 0 else 0.0
        cash_flow = noi - annual_debt_service
        coc = cash_flow / equity if equity > 0 else 0.0
        return {
            "cap_rate": cap,
            "cash_on_cash": coc,
            "equity_invested": equity,
            "leverage_effect": coc - cap,
        }


class REITMetrics:
    """REIT-specific valuation and yield metrics."""

    @staticmethod
    def ffo(
        net_income: float,
        depreciation: float,
        gains_on_sales: float = 0.0,
    ) -> float:
        """Compute Funds From Operations.

        FFO = Net Income + Depreciation/Amortization - Gains on Property Sales

        Parameters
        ----------
        net_income : float
            GAAP net income.
        depreciation : float
            Depreciation and amortization charges.
        gains_on_sales : float, optional
            Gains on property sales. Default is 0.

        Returns
        -------
        float
            Funds From Operations.
        """
        return net_income + depreciation - gains_on_sales

    @staticmethod
    def affo(
        ffo: float,
        maintenance_capex: float,
        straight_line_rent_adj: float = 0.0,
    ) -> float:
        """Compute Adjusted Funds From Operations.

        AFFO = FFO - Maintenance Capex - Straight-Line Rent Adjustments

        Parameters
        ----------
        ffo : float
            Funds From Operations.
        maintenance_capex : float
            Recurring capital expenditures to maintain properties.
        straight_line_rent_adj : float, optional
            Straight-line rent adjustment. Default is 0.

        Returns
        -------
        float
            Adjusted Funds From Operations.
        """
        return ffo - maintenance_capex - straight_line_rent_adj

    @staticmethod
    def ffo_yield(ffo_per_share: float, price: float) -> float:
        """Compute FFO yield (inverse of P/FFO).

        FFO Yield = FFO per Share / Price

        Parameters
        ----------
        ffo_per_share : float
            FFO per share.
        price : float
            Current REIT share price. Must be positive.

        Returns
        -------
        float
            FFO yield (decimal).
        """
        if price <= 0:
            raise ValueError(f"Price must be positive, got {price}.")
        return ffo_per_share / price

    @staticmethod
    def affo_yield(affo_per_share: float, price: float) -> float:
        """Compute AFFO yield (inverse of P/AFFO).

        AFFO Yield = AFFO per Share / Price

        Parameters
        ----------
        affo_per_share : float
            AFFO per share.
        price : float
            Current REIT share price. Must be positive.

        Returns
        -------
        float
            AFFO yield (decimal).
        """
        if price <= 0:
            raise ValueError(f"Price must be positive, got {price}.")
        return affo_per_share / price

    @staticmethod
    def p_ffo(price: float, ffo_per_share: float) -> float:
        """Compute Price-to-FFO ratio (REIT equivalent of P/E).

        P/FFO = Price / FFO per Share

        Parameters
        ----------
        price : float
            Current REIT share price.
        ffo_per_share : float
            FFO per share. Must be positive.

        Returns
        -------
        float
            P/FFO ratio.
        """
        if ffo_per_share <= 0:
            raise ValueError(
                f"FFO per share must be positive, got {ffo_per_share}."
            )
        return price / ffo_per_share

    @staticmethod
    def nav_premium_discount(
        price: float,
        nav_per_share: float,
    ) -> float:
        """Compute REIT premium or discount to NAV.

        Premium/Discount = (Price - NAV) / NAV

        Parameters
        ----------
        price : float
            Current REIT share price.
        nav_per_share : float
            Estimated net asset value per share. Must be positive.

        Returns
        -------
        float
            Premium (positive) or discount (negative) as a decimal.
        """
        if nav_per_share <= 0:
            raise ValueError(
                f"NAV per share must be positive, got {nav_per_share}."
            )
        return (price - nav_per_share) / nav_per_share


class RealReturn:
    """Inflation-adjusted return calculations for real assets."""

    @staticmethod
    def inflation_adjusted_return(
        nominal_return: float,
        inflation_rate: float,
    ) -> float:
        """Compute the real (inflation-adjusted) return.

        Real Return = (1 + Nominal Return) / (1 + Inflation Rate) - 1

        Parameters
        ----------
        nominal_return : float
            Nominal return over the period (decimal).
        inflation_rate : float
            Inflation rate over the period (decimal).

        Returns
        -------
        float
            Real return (decimal).
        """
        return (1.0 + nominal_return) / (1.0 + inflation_rate) - 1.0

    @staticmethod
    def cumulative_real_return(
        nominal_returns: np.ndarray,
        inflation_rates: np.ndarray,
    ) -> float:
        """Compute cumulative real return over multiple periods.

        Parameters
        ----------
        nominal_returns : np.ndarray
            Array of periodic nominal returns (decimals).
        inflation_rates : np.ndarray
            Array of periodic inflation rates (decimals).

        Returns
        -------
        float
            Cumulative real return (decimal).
        """
        nominal_returns = np.asarray(nominal_returns, dtype=np.float64)
        inflation_rates = np.asarray(inflation_rates, dtype=np.float64)
        real_factors = (1.0 + nominal_returns) / (1.0 + inflation_rates)
        return float(np.prod(real_factors) - 1.0)

    @staticmethod
    def real_vs_nominal_comparison(
        nominal_return: float,
        inflation_rate: float,
        years: int,
        initial_value: float = 100_000.0,
    ) -> dict[str, float]:
        """Compare nominal and real wealth accumulation.

        Parameters
        ----------
        nominal_return : float
            Annual nominal return (decimal).
        inflation_rate : float
            Annual inflation rate (decimal).
        years : int
            Investment horizon in years.
        initial_value : float, optional
            Starting investment. Default is 100,000.

        Returns
        -------
        dict[str, float]
            Keys: 'nominal_terminal', 'real_terminal' (in today's dollars),
            'purchasing_power_loss' (fraction of nominal value lost to
            inflation).
        """
        nominal_terminal = initial_value * (1.0 + nominal_return) ** years
        real_return = (1.0 + nominal_return) / (1.0 + inflation_rate) - 1.0
        real_terminal = initial_value * (1.0 + real_return) ** years

        pp_loss = (nominal_terminal - real_terminal) / nominal_terminal
        return {
            "nominal_terminal": nominal_terminal,
            "real_terminal": real_terminal,
            "purchasing_power_loss": pp_loss,
        }


def _demo() -> None:
    """Run the demonstration calculations (bare-run default)."""
    np.random.seed(42)

    print("=" * 60)
    print("Real Asset Analysis - Demo")
    print("=" * 60)

    # --- Property Valuation (Example 1 from SKILL.md) ---
    print("\n--- Property Valuation ---")
    noi_val = PropertyValuation.noi(
        gross_rental_income=150_000, operating_expenses=50_000,
        vacancy_rate=0.05,
    )
    print(f"Gross rent: $150,000, OpEx: $50,000, Vacancy: 5%")
    print(f"NOI: ${noi_val:,.0f}")

    prop_value = PropertyValuation.value_from_cap_rate(noi=100_000, cap_rate=0.06)
    print(f"\nNOI = $100,000, Cap rate = 6%")
    print(f"Property value: ${prop_value:,.0f}")

    # Cap rate sensitivity
    print("\nCap rate sensitivity on $100,000 NOI:")
    for cr in [0.05, 0.06, 0.07, 0.08]:
        val = PropertyValuation.value_from_cap_rate(noi=100_000, cap_rate=cr)
        print(f"  Cap rate {cr:.0%}: ${val:,.0f}")

    cap = PropertyValuation.cap_rate(noi=100_000, property_value=prop_value)
    print(f"\nVerification cap rate: {cap:.4f} ({cap*100:.2f}%)")

    grm = PropertyValuation.gross_rent_multiplier(
        property_price=500_000, gross_annual_rent=60_000,
    )
    print(f"GRM ($500K / $60K rent): {grm:.1f}x")

    # --- Cash-on-Cash Return (Example 2 from SKILL.md) ---
    print("\n--- Cash-on-Cash Return with Leverage ---")
    noi_prop = 35_000
    debt_service = 17_000
    cash_flow = noi_prop - debt_service
    down_payment = 200_000

    coc = PropertyValuation.cash_on_cash_return(
        annual_pretax_cash_flow=cash_flow,
        total_cash_invested=down_payment,
    )
    print(f"Property: $500,000, Down payment: $200,000")
    print(f"NOI: ${noi_prop:,}, Debt service: ${debt_service:,}")
    print(f"Cash flow: ${cash_flow:,}")
    print(f"Cash-on-cash return: {coc:.4f} ({coc*100:.2f}%)")

    # --- Leverage Metrics ---
    print("\n--- Leverage Analysis ---")
    ltv = LeverageMetrics.loan_to_value(
        loan_amount=300_000, property_value=500_000,
    )
    dscr = LeverageMetrics.debt_service_coverage(
        noi=35_000, annual_debt_service=17_000,
    )
    print(f"LTV: {ltv:.2f} ({ltv*100:.0f}%)")
    print(f"DSCR: {dscr:.2f}x")

    lev = LeverageMetrics.levered_vs_unlevered(
        property_value=500_000, noi=35_000,
        loan_amount=300_000, annual_debt_service=17_000,
    )
    print(f"\nUnlevered (cap rate): {lev['cap_rate']:.4f} ({lev['cap_rate']*100:.2f}%)")
    print(f"Levered (cash-on-cash): {lev['cash_on_cash']:.4f} ({lev['cash_on_cash']*100:.2f}%)")
    print(f"Leverage effect: {lev['leverage_effect']:+.4f} ({lev['leverage_effect']*100:+.2f}%)")

    # --- REIT Metrics ---
    print("\n--- REIT Metrics ---")
    ffo_val = REITMetrics.ffo(
        net_income=50_000_000, depreciation=30_000_000, gains_on_sales=5_000_000,
    )
    affo_val = REITMetrics.affo(
        ffo=ffo_val, maintenance_capex=8_000_000, straight_line_rent_adj=2_000_000,
    )
    shares = 20_000_000
    ffo_ps = ffo_val / shares
    affo_ps = affo_val / shares
    price = 45.00

    print(f"Net Income: $50M, Depreciation: $30M, Gains: $5M")
    print(f"FFO: ${ffo_val/1e6:.1f}M (${ffo_ps:.2f}/share)")
    print(f"AFFO: ${affo_val/1e6:.1f}M (${affo_ps:.2f}/share)")
    print(f"Price: ${price:.2f}")
    print(f"P/FFO: {REITMetrics.p_ffo(price, ffo_ps):.2f}x")
    print(f"FFO yield: {REITMetrics.ffo_yield(ffo_ps, price):.4f} ({REITMetrics.ffo_yield(ffo_ps, price)*100:.2f}%)")
    print(f"AFFO yield: {REITMetrics.affo_yield(affo_ps, price):.4f} ({REITMetrics.affo_yield(affo_ps, price)*100:.2f}%)")

    nav_ps = 50.00
    pd_val = REITMetrics.nav_premium_discount(price=price, nav_per_share=nav_ps)
    print(f"\nNAV/share: ${nav_ps:.2f}")
    print(f"Premium/discount to NAV: {pd_val:.4f} ({pd_val*100:.2f}%)")

    # --- Real Return ---
    print("\n--- Inflation-Adjusted Real Return ---")
    nominal = 0.08
    inflation = 0.03
    real_ret = RealReturn.inflation_adjusted_return(
        nominal_return=nominal, inflation_rate=inflation,
    )
    print(f"Nominal return: {nominal:.2%}, Inflation: {inflation:.2%}")
    print(f"Real return: {real_ret:.4f} ({real_ret*100:.2f}%)")

    # Multi-year comparison
    comparison = RealReturn.real_vs_nominal_comparison(
        nominal_return=0.08, inflation_rate=0.03,
        years=20, initial_value=100_000,
    )
    print(f"\n20-year comparison ($100,000 initial, 8% nominal, 3% inflation):")
    print(f"  Nominal terminal: ${comparison['nominal_terminal']:,.0f}")
    print(f"  Real terminal:    ${comparison['real_terminal']:,.0f} (today's dollars)")
    print(f"  Purchasing power loss: {comparison['purchasing_power_loss']:.4f} "
          f"({comparison['purchasing_power_loss']*100:.2f}%)")

    # Cumulative real return with varying inflation
    annual_nominal = np.full(10, 0.07)
    annual_inflation = np.array([0.02, 0.03, 0.04, 0.06, 0.05, 0.03, 0.02, 0.02, 0.03, 0.02])
    cumul_real = RealReturn.cumulative_real_return(
        nominal_returns=annual_nominal, inflation_rates=annual_inflation,
    )
    cumul_nominal = float(np.prod(1.0 + annual_nominal) - 1.0)
    print(f"\n10-year cumulative (7% nominal, variable inflation):")
    print(f"  Cumulative nominal: {cumul_nominal:.4f} ({cumul_nominal*100:.2f}%)")
    print(f"  Cumulative real:    {cumul_real:.4f} ({cumul_real*100:.2f}%)")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)


def _verify() -> None:
    """Assert demo computations against the SKILL.md worked examples."""
    checks: list[tuple[str, float, float]] = []

    # SKILL.md Example 1: Value = $100,000 / 0.06 = $1,666,667
    value = PropertyValuation.value_from_cap_rate(noi=100_000, cap_rate=0.06)
    checks.append(("Example 1 property value", value, 1_666_667.0))
    checks.append((
        "Example 1 cap rate round-trip",
        PropertyValuation.cap_rate(noi=100_000, property_value=value),
        0.06,
    ))

    # SKILL.md Example 2: cash-on-cash 9.0%, unlevered cap rate 7.0%
    coc = PropertyValuation.cash_on_cash_return(
        annual_pretax_cash_flow=18_000, total_cash_invested=200_000,
    )
    checks.append(("Example 2 cash-on-cash return", coc, 0.09))
    lev = LeverageMetrics.levered_vs_unlevered(
        property_value=500_000, noi=35_000,
        loan_amount=300_000, annual_debt_service=17_000,
    )
    checks.append(("Example 2 cap rate", lev["cap_rate"], 0.07))
    checks.append(("Example 2 leverage effect", lev["leverage_effect"], 0.02))

    # Demo leverage metrics
    checks.append((
        "Demo LTV",
        LeverageMetrics.loan_to_value(300_000, 500_000),
        0.60,
    ))
    checks.append((
        "Demo DSCR",
        LeverageMetrics.debt_service_coverage(35_000, 17_000),
        35_000 / 17_000,
    ))

    # Demo REIT metrics: FFO = 50M + 30M - 5M = 75M; AFFO = 75M - 8M - 2M = 65M
    ffo_val = REITMetrics.ffo(
        net_income=50_000_000, depreciation=30_000_000, gains_on_sales=5_000_000,
    )
    checks.append(("Demo FFO", ffo_val, 75_000_000.0))
    affo_val = REITMetrics.affo(
        ffo=ffo_val, maintenance_capex=8_000_000, straight_line_rent_adj=2_000_000,
    )
    checks.append(("Demo AFFO", affo_val, 65_000_000.0))

    # Demo real return: 8% nominal, 3% inflation -> 4.854%
    checks.append((
        "Demo real return",
        RealReturn.inflation_adjusted_return(0.08, 0.03),
        0.0485437,
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
        prog="real_assets.py",
        description=(
            "Real asset analysis reference implementation. Main classes: "
            "PropertyValuation (noi, cap_rate, value_from_cap_rate, "
            "gross_rent_multiplier, cash_on_cash_return), LeverageMetrics "
            "(loan_to_value, debt_service_coverage, levered_vs_unlevered), "
            "REITMetrics (ffo, affo, ffo_yield, affo_yield, p_ffo, "
            "nav_premium_discount), RealReturn (inflation_adjusted_return, "
            "cumulative_real_return, real_vs_nominal_comparison)."
        ),
        epilog=(
            "Primarily intended to be imported as a module: "
            "from real_assets import PropertyValuation, LeverageMetrics, "
            "REITMetrics, RealReturn. Run with no arguments to print a demo."
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
