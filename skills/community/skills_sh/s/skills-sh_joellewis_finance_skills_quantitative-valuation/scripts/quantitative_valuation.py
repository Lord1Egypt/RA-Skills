# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.11"
# ///
"""
Quantitative Valuation
=======================
DCF, dividend discount models, comparable multiples, residual income,
WACC calculation, and sensitivity analysis helpers.

Part of Layer 3 (Valuation) in the finance skills framework.
"""

import argparse
import math
import sys

import numpy as np


class DCF:
    """Discounted cash flow valuation with Gordon Growth or exit-multiple terminal value.

    Parameters
    ----------
    fcf_current : float
        Current (Year 0) free cash flow.
    growth_rates : list[float] | np.ndarray
        Annual FCF growth rates for the explicit forecast period (decimals,
        e.g., 0.15 = 15%). The length determines the number of forecast years.
    wacc : float
        Weighted average cost of capital (decimal).
    terminal_growth : float | None, optional
        Perpetual growth rate for the Gordon Growth terminal value. Provide
        exactly one of ``terminal_growth`` or ``exit_multiple``. Default is None.
    exit_multiple : float | None, optional
        EV/EBITDA (or EV/FCF) multiple applied to the final-year cash flow
        to compute terminal value. Default is None.
    """

    def __init__(
        self,
        fcf_current: float,
        growth_rates: list[float] | np.ndarray,
        wacc: float,
        terminal_growth: float | None = None,
        exit_multiple: float | None = None,
    ):
        if terminal_growth is None and exit_multiple is None:
            raise ValueError("Provide either terminal_growth or exit_multiple.")
        if terminal_growth is not None and exit_multiple is not None:
            raise ValueError(
                "Provide only one of terminal_growth or exit_multiple, not both."
            )
        if terminal_growth is not None and terminal_growth >= wacc:
            raise ValueError(
                "terminal_growth must be less than wacc for a convergent valuation."
            )

        self.fcf_current = fcf_current
        self.growth_rates = np.asarray(growth_rates, dtype=np.float64)
        self.wacc = wacc
        self.terminal_growth = terminal_growth
        self.exit_multiple = exit_multiple

    def projected_fcfs(self) -> np.ndarray:
        """Project free cash flows for each year of the explicit forecast period.

        Returns
        -------
        np.ndarray
            Array of length n with projected FCFs for years 1 through n.
        """
        fcfs = np.empty(len(self.growth_rates), dtype=np.float64)
        fcf = self.fcf_current
        for i, g in enumerate(self.growth_rates):
            fcf = fcf * (1.0 + g)
            fcfs[i] = fcf
        return fcfs

    def pv_explicit_fcfs(self) -> float:
        """Present value of cash flows during the explicit forecast period.

        Returns
        -------
        float
            PV = sum of FCF_t / (1 + WACC)^t for t = 1..n.
        """
        fcfs = self.projected_fcfs()
        years = np.arange(1, len(fcfs) + 1, dtype=np.float64)
        discount_factors = (1.0 + self.wacc) ** years
        return float(np.sum(fcfs / discount_factors))

    def terminal_value(self) -> float:
        """Compute the terminal value at the end of the explicit forecast period.

        Returns
        -------
        float
            Terminal value using Gordon Growth or exit multiple method.
        """
        fcfs = self.projected_fcfs()
        final_fcf = fcfs[-1]

        if self.terminal_growth is not None:
            # Gordon Growth: TV = FCF_n * (1 + g) / (WACC - g)
            return float(final_fcf * (1.0 + self.terminal_growth)
                         / (self.wacc - self.terminal_growth))
        else:
            # Exit multiple: TV = FCF_n * multiple
            return float(final_fcf * self.exit_multiple)

    def pv_terminal_value(self) -> float:
        """Present value of the terminal value discounted back to today.

        Returns
        -------
        float
            TV / (1 + WACC)^n.
        """
        n = len(self.growth_rates)
        tv = self.terminal_value()
        return float(tv / (1.0 + self.wacc) ** n)

    def enterprise_value(self) -> float:
        """Total enterprise value: PV of explicit FCFs plus PV of terminal value.

        Returns
        -------
        float
            Enterprise value.
        """
        return self.pv_explicit_fcfs() + self.pv_terminal_value()

    def equity_value(self, net_debt: float = 0.0) -> float:
        """Equity value derived from enterprise value minus net debt.

        Parameters
        ----------
        net_debt : float, optional
            Net debt (total debt minus cash). Default is 0.0.

        Returns
        -------
        float
            Equity value = enterprise value - net debt.
        """
        return self.enterprise_value() - net_debt

    def sensitivity_table(
        self,
        wacc_range: np.ndarray,
        growth_range: np.ndarray,
    ) -> np.ndarray:
        """Build a two-way sensitivity table varying WACC and terminal growth rate.

        Only valid when using Gordon Growth terminal value.

        Parameters
        ----------
        wacc_range : np.ndarray
            Array of WACC values to test.
        growth_range : np.ndarray
            Array of terminal growth rates to test.

        Returns
        -------
        np.ndarray
            2D array of enterprise values, shape (len(wacc_range), len(growth_range)).
        """
        if self.terminal_growth is None:
            raise ValueError(
                "Sensitivity table on terminal_growth requires Gordon Growth method."
            )

        results = np.empty((len(wacc_range), len(growth_range)), dtype=np.float64)
        original_wacc = self.wacc
        original_tg = self.terminal_growth

        for i, w in enumerate(wacc_range):
            for j, g in enumerate(growth_range):
                if g >= w:
                    results[i, j] = np.nan
                    continue
                self.wacc = w
                self.terminal_growth = g
                results[i, j] = self.enterprise_value()

        self.wacc = original_wacc
        self.terminal_growth = original_tg
        return results


class WACC:
    """Weighted average cost of capital calculator.

    Parameters
    ----------
    equity_weight : float
        Market-value weight of equity (decimal, e.g., 0.70).
    debt_weight : float
        Market-value weight of debt (decimal, e.g., 0.30).
    cost_of_equity : float
        Required return on equity (decimal).
    cost_of_debt : float
        Pre-tax cost of debt (decimal).
    tax_rate : float
        Marginal corporate tax rate (decimal).
    """

    def __init__(
        self,
        equity_weight: float,
        debt_weight: float,
        cost_of_equity: float,
        cost_of_debt: float,
        tax_rate: float,
    ):
        self.equity_weight = equity_weight
        self.debt_weight = debt_weight
        self.cost_of_equity = cost_of_equity
        self.cost_of_debt = cost_of_debt
        self.tax_rate = tax_rate

    def compute(self) -> float:
        """Compute WACC.

        Returns
        -------
        float
            WACC = w_e * r_e + w_d * r_d * (1 - tax_rate)
        """
        return float(
            self.equity_weight * self.cost_of_equity
            + self.debt_weight * self.cost_of_debt * (1.0 - self.tax_rate)
        )

    @staticmethod
    def cost_of_equity_capm(
        risk_free_rate: float,
        beta: float,
        equity_risk_premium: float,
    ) -> float:
        """Estimate cost of equity using the Capital Asset Pricing Model.

        Parameters
        ----------
        risk_free_rate : float
            Risk-free rate (decimal).
        beta : float
            Stock beta relative to the market.
        equity_risk_premium : float
            Expected market return minus risk-free rate (decimal).

        Returns
        -------
        float
            r_e = R_f + beta * ERP
        """
        return float(risk_free_rate + beta * equity_risk_premium)


class DividendDiscount:
    """Dividend discount model: Gordon Growth (single-stage) and two-stage DDM.

    All prices are per-share values.
    """

    @staticmethod
    def gordon_growth(
        dividend_next: float,
        required_return: float,
        growth_rate: float,
    ) -> float:
        """Single-stage Gordon Growth DDM.

        Parameters
        ----------
        dividend_next : float
            Expected dividend next period (D_1).
        required_return : float
            Required return on equity (decimal).
        growth_rate : float
            Constant perpetual dividend growth rate (decimal).

        Returns
        -------
        float
            P = D_1 / (r - g)
        """
        if growth_rate >= required_return:
            raise ValueError("growth_rate must be less than required_return.")
        return float(dividend_next / (required_return - growth_rate))

    @staticmethod
    def two_stage_ddm(
        dividend_current: float,
        growth_stage1: float,
        growth_stage2: float,
        required_return: float,
        years_stage1: int,
    ) -> float:
        """Two-stage DDM with high-growth phase followed by stable perpetual growth.

        Parameters
        ----------
        dividend_current : float
            Current annual dividend (D_0).
        growth_stage1 : float
            Dividend growth rate during Stage 1 (decimal).
        growth_stage2 : float
            Perpetual dividend growth rate during Stage 2 (decimal).
        required_return : float
            Required return on equity (decimal).
        years_stage1 : int
            Number of years in the high-growth phase.

        Returns
        -------
        float
            Present value of all future dividends under the two-stage model.
        """
        if growth_stage2 >= required_return:
            raise ValueError("growth_stage2 must be less than required_return.")

        # Stage 1: PV of dividends growing at g1 for years_stage1 years
        pv_stage1 = 0.0
        dividend = dividend_current
        for t in range(1, years_stage1 + 1):
            dividend = dividend * (1.0 + growth_stage1)
            pv_stage1 += dividend / (1.0 + required_return) ** t

        # Stage 2: Terminal value at end of Stage 1 using Gordon Growth
        # D_{n+1} = D_n * (1 + g2), then P_n = D_{n+1} / (r - g2)
        dividend_stage2_start = dividend * (1.0 + growth_stage2)
        terminal_price = dividend_stage2_start / (required_return - growth_stage2)
        pv_terminal = terminal_price / (1.0 + required_return) ** years_stage1

        return float(pv_stage1 + pv_terminal)


class ResidualIncome:
    """Residual income valuation model.

    Values a company as book value plus the present value of future economic profits
    (returns in excess of the cost of equity applied to book value).

    Parameters
    ----------
    book_value_initial : float
        Current book value per share (BV_0).
    roe_forecasts : list[float] | np.ndarray
        Forecasted return on equity for each explicit period (decimals).
    cost_of_equity : float
        Required return on equity (decimal).
    terminal_roe : float | None, optional
        ROE assumed in perpetuity beyond the forecast period. If None,
        residual income is assumed to be zero after the explicit period.
    terminal_growth : float, optional
        Growth rate of book value in the terminal period. Default is 0.0.
    """

    def __init__(
        self,
        book_value_initial: float,
        roe_forecasts: list[float] | np.ndarray,
        cost_of_equity: float,
        terminal_roe: float | None = None,
        terminal_growth: float = 0.0,
    ):
        self.book_value_initial = book_value_initial
        self.roe_forecasts = np.asarray(roe_forecasts, dtype=np.float64)
        self.cost_of_equity = cost_of_equity
        self.terminal_roe = terminal_roe
        self.terminal_growth = terminal_growth

    def intrinsic_value(self) -> float:
        """Compute the intrinsic value per share.

        Returns
        -------
        float
            V = BV_0 + sum((ROE_t - r) * BV_{t-1} / (1+r)^t) [+ terminal RI]
        """
        r = self.cost_of_equity
        bv = self.book_value_initial
        pv_ri = 0.0

        for t, roe in enumerate(self.roe_forecasts, start=1):
            residual_income = (roe - r) * bv
            pv_ri += residual_income / (1.0 + r) ** t
            # Update book value: BV_t = BV_{t-1} + earnings - dividends
            # Under clean surplus: BV_t = BV_{t-1} * (1 + ROE * retention)
            # Simplified: assume all excess earnings reinvested
            earnings = roe * bv
            bv = bv + earnings  # full retention for simplicity

        # Terminal residual income
        if self.terminal_roe is not None:
            n = len(self.roe_forecasts)
            terminal_ri = (self.terminal_roe - r) * bv
            if r != self.terminal_growth:
                pv_terminal = (terminal_ri / (r - self.terminal_growth)) / (1.0 + r) ** n
            else:
                pv_terminal = 0.0
            pv_ri += pv_terminal

        return float(self.book_value_initial + pv_ri)


class ComparableMultiples:
    """Relative valuation using comparable company multiples."""

    @staticmethod
    def implied_value(
        metric: float,
        peer_multiples: list[float] | np.ndarray,
        use_median: bool = True,
    ) -> float:
        """Compute implied value from peer multiples.

        Parameters
        ----------
        metric : float
            The target company's financial metric (e.g., EPS, EBITDA, revenue).
        peer_multiples : list[float] | np.ndarray
            Array of peer multiples (e.g., P/E ratios).
        use_median : bool, optional
            If True (default), use median of peer multiples. If False, use mean.

        Returns
        -------
        float
            Implied value = metric * peer aggregate multiple.
        """
        multiples = np.asarray(peer_multiples, dtype=np.float64)
        aggregate = float(np.median(multiples)) if use_median else float(np.mean(multiples))
        return float(metric * aggregate)

    @staticmethod
    def ev_to_equity(
        enterprise_value: float,
        net_debt: float,
        shares_outstanding: float,
    ) -> float:
        """Convert enterprise value to implied share price.

        Parameters
        ----------
        enterprise_value : float
            Implied enterprise value.
        net_debt : float
            Net debt (total debt minus cash).
        shares_outstanding : float
            Number of diluted shares outstanding.

        Returns
        -------
        float
            Implied share price = (EV - net_debt) / shares_outstanding.
        """
        if shares_outstanding <= 0:
            raise ValueError("shares_outstanding must be positive.")
        return float((enterprise_value - net_debt) / shares_outstanding)

    @staticmethod
    def premium_discount(
        current_price: float,
        implied_value: float,
    ) -> float:
        """Compute premium or discount of current price vs implied value.

        Parameters
        ----------
        current_price : float
            Current market price.
        implied_value : float
            Implied intrinsic value.

        Returns
        -------
        float
            (current_price / implied_value) - 1. Negative means discount,
            positive means premium.
        """
        if implied_value == 0:
            raise ValueError("implied_value must be non-zero.")
        return float(current_price / implied_value - 1.0)


def _demo() -> None:
    """Run the demonstration calculations (bare-run default)."""
    print("=" * 65)
    print("Quantitative Valuation - Demo")
    print("=" * 65)

    # --- WACC Calculation ---
    print("\n--- WACC Calculation ---")
    re = WACC.cost_of_equity_capm(
        risk_free_rate=0.04, beta=1.2, equity_risk_premium=0.055,
    )
    print(f"Cost of Equity (CAPM): {re:.4f} ({re * 100:.2f}%)")

    wacc_calc = WACC(
        equity_weight=0.70,
        debt_weight=0.30,
        cost_of_equity=re,
        cost_of_debt=0.05,
        tax_rate=0.25,
    )
    wacc_val = wacc_calc.compute()
    print(f"WACC: {wacc_val:.4f} ({wacc_val * 100:.2f}%)")

    # --- DCF Valuation ---
    print("\n--- DCF Valuation (Gordon Growth Terminal Value) ---")
    dcf = DCF(
        fcf_current=100.0,
        growth_rates=[0.15, 0.15, 0.15, 0.15, 0.15],
        wacc=0.10,
        terminal_growth=0.03,
    )

    fcfs = dcf.projected_fcfs()
    print("Projected FCFs:")
    for i, f in enumerate(fcfs, start=1):
        print(f"  Year {i}: ${f:.1f}M")

    pv_explicit = dcf.pv_explicit_fcfs()
    tv = dcf.terminal_value()
    pv_tv = dcf.pv_terminal_value()
    ev = dcf.enterprise_value()

    print(f"\nPV of Explicit FCFs:  ${pv_explicit:.1f}M")
    print(f"Terminal Value:       ${tv:.1f}M")
    print(f"PV of Terminal Value: ${pv_tv:.1f}M")
    print(f"Enterprise Value:     ${ev:.1f}M")
    print(f"Terminal % of EV:     {pv_tv / ev * 100:.1f}%")

    eq_val = dcf.equity_value(net_debt=200.0)
    print(f"Equity Value (net debt $200M): ${eq_val:.1f}M")

    # --- DCF with Exit Multiple ---
    print("\n--- DCF Valuation (Exit Multiple Terminal Value) ---")
    dcf_em = DCF(
        fcf_current=100.0,
        growth_rates=[0.15, 0.15, 0.15, 0.15, 0.15],
        wacc=0.10,
        exit_multiple=12.0,
    )
    print(f"Exit Multiple TV:     ${dcf_em.terminal_value():.1f}M")
    print(f"Enterprise Value:     ${dcf_em.enterprise_value():.1f}M")

    # --- Sensitivity Table ---
    print("\n--- Sensitivity Table (WACC vs Terminal Growth) ---")
    wacc_range = np.array([0.08, 0.09, 0.10, 0.11, 0.12])
    growth_range = np.array([0.01, 0.02, 0.03, 0.04])
    table = dcf.sensitivity_table(wacc_range, growth_range)

    header = "       " + "  ".join(f"g={g:.0%}" for g in growth_range)
    print(header)
    for i, w in enumerate(wacc_range):
        row_vals = "  ".join(
            f"${v:,.0f}M" if not np.isnan(v) else "  N/A  "
            for v in table[i]
        )
        print(f"WACC={w:.0%}  {row_vals}")

    # --- Gordon Growth DDM ---
    print("\n--- Gordon Growth DDM ---")
    d1 = 2.50
    r_ddm = 0.10
    g_ddm = 0.04
    price_gg = DividendDiscount.gordon_growth(d1, r_ddm, g_ddm)
    print(f"D1=${d1:.2f}, r={r_ddm:.0%}, g={g_ddm:.0%}")
    print(f"Implied Price: ${price_gg:.2f}")

    # --- Two-Stage DDM ---
    print("\n--- Two-Stage DDM ---")
    d0 = 2.00
    g1, g2 = 0.12, 0.04
    r_ts = 0.10
    n_stage1 = 5
    price_ts = DividendDiscount.two_stage_ddm(d0, g1, g2, r_ts, n_stage1)
    print(f"D0=${d0:.2f}, g1={g1:.0%} for {n_stage1}yr, g2={g2:.0%}, r={r_ts:.0%}")
    print(f"Implied Price: ${price_ts:.2f}")

    # --- Residual Income ---
    print("\n--- Residual Income Model ---")
    ri = ResidualIncome(
        book_value_initial=30.0,
        roe_forecasts=[0.15, 0.14, 0.13, 0.12, 0.11],
        cost_of_equity=0.10,
        terminal_roe=0.10,
        terminal_growth=0.03,
    )
    ri_val = ri.intrinsic_value()
    print(f"Book Value: $30.00, Cost of Equity: 10%")
    print(f"ROE forecasts: 15%, 14%, 13%, 12%, 11% -> terminal ROE 10%")
    print(f"Intrinsic Value: ${ri_val:.2f}")

    # --- Comparable Multiples ---
    print("\n--- Comparable Multiples ---")
    eps = 5.00
    peer_pe = [15.0, 17.0, 18.0, 19.0, 22.0]
    implied_price = ComparableMultiples.implied_value(eps, peer_pe, use_median=True)
    print(f"EPS: ${eps:.2f}, Peer P/E: {peer_pe}")
    print(f"Median P/E: {np.median(peer_pe):.1f}x")
    print(f"Implied Share Price: ${implied_price:.2f}")

    current_px = 75.0
    disc = ComparableMultiples.premium_discount(current_px, implied_price)
    print(f"Current Price: ${current_px:.2f}")
    print(f"Premium/Discount: {disc:.2%} ({'discount' if disc < 0 else 'premium'})")

    # --- EV/EBITDA Implied Price ---
    print("\n--- EV/EBITDA Implied Share Price ---")
    ebitda = 50.0
    peer_ev_ebitda = [8.0, 9.5, 10.0, 11.0, 12.5]
    implied_ev = ComparableMultiples.implied_value(ebitda, peer_ev_ebitda, use_median=True)
    share_price = ComparableMultiples.ev_to_equity(
        enterprise_value=implied_ev, net_debt=100.0, shares_outstanding=20.0,
    )
    print(f"EBITDA: ${ebitda:.1f}M, Peer EV/EBITDA: {peer_ev_ebitda}")
    print(f"Implied EV: ${implied_ev:.1f}M")
    print(f"Net Debt: $100M, Shares: 20M")
    print(f"Implied Share Price: ${share_price:.2f}")

    print("\n" + "=" * 65)
    print("Demo complete.")
    print("=" * 65)


def _verify() -> None:
    """Assert demo computations against the SKILL.md worked examples."""
    checks: list[tuple[str, float, float]] = []

    # SKILL.md Example 1: Two-stage DCF
    dcf = DCF(
        fcf_current=100.0,
        growth_rates=[0.15, 0.15, 0.15, 0.15, 0.15],
        wacc=0.10,
        terminal_growth=0.03,
    )
    checks.append(("Example 1 Year 5 FCF ($M)", float(dcf.projected_fcfs()[-1]), 201.1))
    checks.append(("Example 1 PV explicit FCFs ($M)", dcf.pv_explicit_fcfs(), 572.5))
    checks.append(("Example 1 terminal value ($M)", dcf.terminal_value(), 2959.6))
    checks.append(("Example 1 PV terminal value ($M)", dcf.pv_terminal_value(), 1837.7))
    checks.append(("Example 1 enterprise value ($M)", dcf.enterprise_value(), 2410.1))

    # SKILL.md Example 2: Comparable P/E analysis
    implied = ComparableMultiples.implied_value(
        metric=5.00, peer_multiples=[15.0, 17.0, 18.0, 19.0, 22.0], use_median=True,
    )
    checks.append(("Example 2 implied share price", implied, 90.00))
    checks.append((
        "Example 2 premium/discount at $75",
        ComparableMultiples.premium_discount(75.0, implied),
        -1.0 / 6.0,
    ))

    # Demo WACC: r_e = 4% + 1.2 * 5.5% = 10.6%; WACC = 0.7*10.6% + 0.3*5%*0.75
    re = WACC.cost_of_equity_capm(0.04, 1.2, 0.055)
    checks.append(("Demo CAPM cost of equity", re, 0.106))
    wacc_val = WACC(0.70, 0.30, re, 0.05, 0.25).compute()
    checks.append(("Demo WACC", wacc_val, 0.08545))

    # Demo Gordon Growth DDM: 2.50 / (0.10 - 0.04)
    checks.append((
        "Demo Gordon Growth DDM price",
        DividendDiscount.gordon_growth(2.50, 0.10, 0.04),
        2.50 / 0.06,
    ))

    failures = 0
    for name, got, expected in checks:
        ok = math.isclose(got, expected, rel_tol=1e-3)
        print(f"{'PASS' if ok else 'FAIL'}: {name}: got {got:,.6g}, expected {expected:,.6g}")
        failures += 0 if ok else 1
    if failures:
        print(f"FAIL: {failures} of {len(checks)} checks failed.")
        sys.exit(1)
    print(f"PASS: all {len(checks)} checks passed.")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="quantitative_valuation.py",
        description=(
            "Quantitative valuation reference implementation. Main classes: "
            "DCF (projected_fcfs, pv_explicit_fcfs, terminal_value, "
            "enterprise_value, equity_value, sensitivity_table), WACC "
            "(compute, cost_of_equity_capm), DividendDiscount "
            "(gordon_growth, two_stage_ddm), ResidualIncome "
            "(intrinsic_value), ComparableMultiples (implied_value, "
            "ev_to_equity, premium_discount)."
        ),
        epilog=(
            "Primarily intended to be imported as a module: "
            "from quantitative_valuation import DCF, WACC, DividendDiscount, "
            "ResidualIncome, ComparableMultiples. "
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
