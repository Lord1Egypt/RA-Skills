# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.11"
# ///
"""
Fixed Income — Municipal
=========================
Tax-equivalent yield (TEY), after-tax yield comparison, de minimis tax
calculation, AMT adjustment, and muni-to-Treasury ratio analysis.

Part of Layer 2 (Asset Classes) in the finance skills framework.
"""

import argparse
import sys
import numpy as np


class MunicipalBondTax:
    """Tax-equivalent yield and after-tax comparison for municipal bonds.

    Provides static methods for all tax-related muni calculations.
    """

    @staticmethod
    def tax_equivalent_yield_federal(
        muni_yield: float,
        federal_rate: float,
    ) -> float:
        """Compute tax-equivalent yield using federal tax rate only.

        Parameters
        ----------
        muni_yield : float
            Tax-exempt municipal bond yield as a decimal (e.g., 0.035 = 3.5%).
        federal_rate : float
            Federal marginal tax rate as a decimal (e.g., 0.37 = 37%).

        Returns
        -------
        float
            TEY = Muni Yield / (1 - federal_rate)
        """
        if federal_rate >= 1.0:
            raise ValueError("Federal rate must be less than 1.0.")
        return float(muni_yield / (1.0 - federal_rate))

    @staticmethod
    def tax_equivalent_yield_full(
        muni_yield: float,
        federal_rate: float,
        state_rate: float,
    ) -> float:
        """Compute tax-equivalent yield with federal and state tax benefit.

        For an in-state municipal bond exempt from both federal and state tax.

        Parameters
        ----------
        muni_yield : float
            Tax-exempt municipal bond yield as a decimal.
        federal_rate : float
            Federal marginal tax rate as a decimal.
        state_rate : float
            State marginal tax rate as a decimal.

        Returns
        -------
        float
            TEY = Muni Yield / (1 - federal_rate - state_rate * (1 - federal_rate))
        """
        combined = 1.0 - federal_rate - state_rate * (1.0 - federal_rate)
        if combined <= 0:
            raise ValueError(
                "Combined tax factor is non-positive. Check rate inputs."
            )
        return float(muni_yield / combined)

    @staticmethod
    def after_tax_yield(
        taxable_yield: float,
        federal_rate: float,
        state_rate: float = 0.0,
    ) -> float:
        """Compute the after-tax yield of a taxable bond.

        Parameters
        ----------
        taxable_yield : float
            Pre-tax yield of the taxable bond as a decimal.
        federal_rate : float
            Federal marginal tax rate as a decimal.
        state_rate : float, optional
            State marginal tax rate as a decimal. Default is 0.0.

        Returns
        -------
        float
            After-tax yield = taxable_yield * (1 - federal_rate - state_rate * (1 - federal_rate))
        """
        combined_factor = 1.0 - federal_rate - state_rate * (1.0 - federal_rate)
        return float(taxable_yield * combined_factor)

    @staticmethod
    def compare_muni_vs_taxable(
        muni_yield: float,
        taxable_yield: float,
        federal_rate: float,
        state_rate: float = 0.0,
    ) -> dict:
        """Compare a muni bond to a taxable bond on an after-tax basis.

        Parameters
        ----------
        muni_yield : float
            Tax-exempt muni yield as a decimal.
        taxable_yield : float
            Pre-tax taxable bond yield as a decimal.
        federal_rate : float
            Federal marginal tax rate.
        state_rate : float, optional
            State marginal tax rate. Default is 0.0.

        Returns
        -------
        dict
            Dictionary with TEY, after-tax taxable yield, muni advantage,
            and recommendation.
        """
        if state_rate > 0:
            tey = MunicipalBondTax.tax_equivalent_yield_full(
                muni_yield, federal_rate, state_rate
            )
        else:
            tey = MunicipalBondTax.tax_equivalent_yield_federal(
                muni_yield, federal_rate
            )

        after_tax = MunicipalBondTax.after_tax_yield(
            taxable_yield, federal_rate, state_rate
        )
        advantage = muni_yield - after_tax

        return {
            "muni_yield": muni_yield,
            "taxable_yield": taxable_yield,
            "tax_equivalent_yield": tey,
            "after_tax_taxable_yield": after_tax,
            "muni_advantage": advantage,
            "prefer_muni": advantage > 0,
        }


class DeMinimis:
    """De minimis tax rule calculations for discount municipal bonds.

    The de minimis rule determines when the discount on a muni bond
    loses its tax-exempt treatment and is taxed as ordinary income.
    """

    @staticmethod
    def threshold_price(
        par: float,
        years_to_maturity: float,
        rate_per_year: float = 0.0025,
    ) -> float:
        """Compute the de minimis threshold price.

        Parameters
        ----------
        par : float
            Par (face) value of the bond.
        years_to_maturity : float
            Years remaining to maturity.
        rate_per_year : float, optional
            De minimis rate per year. Default is 0.0025 (0.25% per year).

        Returns
        -------
        float
            Threshold = Par - (rate_per_year * years_to_maturity * Par)
            Bonds purchased below this price have the discount taxed as
            ordinary income.
        """
        return float(par * (1.0 - rate_per_year * years_to_maturity))

    @staticmethod
    def is_de_minimis(
        purchase_price: float,
        par: float,
        years_to_maturity: float,
        rate_per_year: float = 0.0025,
    ) -> bool:
        """Determine whether a purchase price triggers the de minimis rule.

        Parameters
        ----------
        purchase_price : float
            Price paid for the bond.
        par : float
            Par value.
        years_to_maturity : float
            Years remaining to maturity.
        rate_per_year : float, optional
            De minimis rate. Default is 0.0025.

        Returns
        -------
        bool
            True if purchase price is below the de minimis threshold
            (discount is taxed as ordinary income).
        """
        threshold = DeMinimis.threshold_price(par, years_to_maturity, rate_per_year)
        return purchase_price < threshold

    @staticmethod
    def taxable_gain(
        purchase_price: float,
        par: float,
        years_to_maturity: float,
        rate_per_year: float = 0.0025,
    ) -> float:
        """Compute the portion of the discount taxed as ordinary income.

        Parameters
        ----------
        purchase_price : float
            Price paid for the bond.
        par : float
            Par value.
        years_to_maturity : float
            Years remaining to maturity.
        rate_per_year : float, optional
            De minimis rate. Default is 0.0025.

        Returns
        -------
        float
            If de minimis applies, the full discount (par - price) is taxed.
            If not, returns 0.0 (the discount retains tax-exempt treatment).
        """
        if DeMinimis.is_de_minimis(
            purchase_price, par, years_to_maturity, rate_per_year
        ):
            return float(par - purchase_price)
        return 0.0


class AMTAdjustment:
    """AMT (Alternative Minimum Tax) adjustment for private activity bonds."""

    @staticmethod
    def amt_adjusted_yield(
        muni_yield: float,
        amt_rate: float,
    ) -> float:
        """Compute the effective yield on an AMT-subject private activity bond.

        For a taxpayer subject to AMT, the interest is included in AMT
        income, reducing the tax benefit. Only the AMT rate matters here;
        the regular federal rate does not enter this calculation.

        Parameters
        ----------
        muni_yield : float
            Stated yield on the AMT-subject muni as a decimal.
        amt_rate : float
            AMT rate as a decimal (e.g., 0.28 = 28%).

        Returns
        -------
        float
            Effective after-AMT yield = muni_yield * (1 - amt_rate).
            This represents the after-tax yield for an AMT-affected taxpayer.
        """
        return float(muni_yield * (1.0 - amt_rate))

    @staticmethod
    def amt_tax_equivalent_yield(
        muni_yield: float,
        federal_rate: float,
        amt_rate: float,
    ) -> float:
        """Compute the TEY for an AMT-subject bond.

        The AMT-subject bond's effective after-tax yield needs a different
        TEY than a fully exempt bond.

        Parameters
        ----------
        muni_yield : float
            Stated yield on the AMT-subject muni.
        federal_rate : float
            Regular federal marginal rate.
        amt_rate : float
            AMT rate.

        Returns
        -------
        float
            TEY accounting for AMT: the taxable yield equivalent of the
            AMT-reduced muni yield.
        """
        after_amt = AMTAdjustment.amt_adjusted_yield(muni_yield, amt_rate)
        # Convert the after-AMT yield to a pre-tax equivalent
        if federal_rate >= 1.0:
            raise ValueError("Federal rate must be less than 1.0.")
        return float(after_amt / (1.0 - federal_rate))


class MuniRatio:
    """Muni-to-Treasury yield ratio analysis."""

    @staticmethod
    def yield_ratio(
        muni_yield: float,
        treasury_yield: float,
    ) -> float:
        """Compute the muni-to-Treasury yield ratio.

        Parameters
        ----------
        muni_yield : float
            Municipal bond yield as a decimal.
        treasury_yield : float
            Treasury yield of comparable maturity as a decimal.

        Returns
        -------
        float
            Ratio = muni_yield / treasury_yield. Expressed as a decimal
            (e.g., 0.80 = 80%).
        """
        if treasury_yield == 0:
            raise ValueError("Treasury yield cannot be zero.")
        return float(muni_yield / treasury_yield)

    @staticmethod
    def relative_value_assessment(
        muni_yield: float,
        treasury_yield: float,
        historical_average: float = 0.80,
    ) -> dict:
        """Assess muni relative value vs Treasuries.

        Parameters
        ----------
        muni_yield : float
            Municipal bond yield.
        treasury_yield : float
            Treasury yield of comparable maturity.
        historical_average : float, optional
            Historical average muni/Treasury ratio. Default is 0.80 (80%).

        Returns
        -------
        dict
            Dictionary with ratio, deviation from historical average,
            and valuation assessment.
        """
        ratio = MuniRatio.yield_ratio(muni_yield, treasury_yield)
        deviation = ratio - historical_average

        if ratio > 0.85:
            assessment = "cheap"
        elif ratio < 0.70:
            assessment = "rich"
        else:
            assessment = "fair"

        return {
            "muni_yield": muni_yield,
            "treasury_yield": treasury_yield,
            "ratio": ratio,
            "ratio_pct": ratio * 100,
            "historical_average": historical_average,
            "deviation": deviation,
            "assessment": assessment,
        }

    @staticmethod
    def ratio_curve(
        muni_yields: np.ndarray,
        treasury_yields: np.ndarray,
        maturities: np.ndarray,
    ) -> np.ndarray:
        """Compute the muni/Treasury ratio at each maturity point.

        Parameters
        ----------
        muni_yields : np.ndarray
            Muni yields across maturities.
        treasury_yields : np.ndarray
            Treasury yields across maturities.
        maturities : np.ndarray
            Corresponding maturities in years.

        Returns
        -------
        np.ndarray
            Array of muni/Treasury ratios for each maturity.
        """
        muni = np.asarray(muni_yields, dtype=np.float64)
        tsy = np.asarray(treasury_yields, dtype=np.float64)
        if np.any(tsy == 0):
            raise ValueError("Treasury yields must be non-zero at all maturities.")
        return muni / tsy


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Municipal bond tax analysis
    # ----------------------------------------------------------------
    print("=" * 60)
    print("Fixed Income Municipal — Demo")
    print("=" * 60)

    # ----- Tax-Equivalent Yield -----
    print("\n--- Tax-Equivalent Yield ---")

    muni_yield = 0.035  # 3.5%
    fed_rate = 0.37
    state_rate = 0.05

    tey_fed = MunicipalBondTax.tax_equivalent_yield_federal(muni_yield, fed_rate)
    tey_full = MunicipalBondTax.tax_equivalent_yield_full(
        muni_yield, fed_rate, state_rate
    )

    print(f"\n  Muni Yield:                 {muni_yield*100:.2f}%")
    print(f"  Federal Rate:               {fed_rate*100:.0f}%")
    print(f"  State Rate:                 {state_rate*100:.0f}%")
    print(f"  TEY (federal only):         {tey_fed*100:.2f}%")
    print(f"  TEY (federal + state):      {tey_full*100:.2f}%")
    print(f"  State tax benefit:          {(tey_full - tey_fed)*10000:.0f} bp")

    # ----- After-Tax Comparison -----
    print("\n--- Muni vs Taxable Comparison ---")

    taxable_yield = 0.055  # 5.5%
    comparison = MunicipalBondTax.compare_muni_vs_taxable(
        muni_yield=muni_yield,
        taxable_yield=taxable_yield,
        federal_rate=fed_rate,
        state_rate=state_rate,
    )

    print(f"\n  Muni Yield:              {comparison['muni_yield']*100:.2f}%")
    print(f"  Taxable Yield:           {comparison['taxable_yield']*100:.2f}%")
    print(f"  Tax-Equivalent Yield:    {comparison['tax_equivalent_yield']*100:.2f}%")
    print(f"  After-Tax Taxable Yield: {comparison['after_tax_taxable_yield']*100:.2f}%")
    print(f"  Muni Advantage:          {comparison['muni_advantage']*10000:.0f} bp")
    print(f"  Prefer Muni:             {comparison['prefer_muni']}")

    # ----- TEY Across Tax Brackets -----
    print("\n--- TEY Across Tax Brackets ---")
    brackets = [0.10, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37]
    print(f"\n  Muni Yield = {muni_yield*100:.2f}%")
    print(f"  {'Bracket':>10s}  {'TEY (fed)':>10s}  {'TEY (fed+state)':>16s}")
    print(f"  {'-'*10}  {'-'*10}  {'-'*16}")
    for bracket in brackets:
        t_fed = MunicipalBondTax.tax_equivalent_yield_federal(muni_yield, bracket)
        t_full = MunicipalBondTax.tax_equivalent_yield_full(
            muni_yield, bracket, state_rate
        )
        print(f"  {bracket*100:9.0f}%  {t_fed*100:9.2f}%  {t_full*100:15.2f}%")

    # ----- De Minimis Rule -----
    print("\n--- De Minimis Tax Rule ---")

    par = 1000.0
    years = 10.0
    threshold = DeMinimis.threshold_price(par, years)
    print(f"\n  Par = ${par:.0f}, Maturity = {years:.0f} years")
    print(f"  De minimis threshold: ${threshold:.2f}")

    test_prices = [990.0, 975.0, 960.0, 940.0]
    for price in test_prices:
        triggered = DeMinimis.is_de_minimis(price, par, years)
        gain = DeMinimis.taxable_gain(price, par, years)
        status = "TAXABLE" if triggered else "exempt"
        print(f"  Price ${price:.0f}: {status}, taxable gain = ${gain:.2f}")

    # ----- AMT Adjustment -----
    print("\n--- AMT Adjustment ---")

    amt_muni_yield = 0.038  # 3.8% private activity bond
    amt_rate = 0.28

    after_amt = AMTAdjustment.amt_adjusted_yield(amt_muni_yield, amt_rate)
    amt_tey = AMTAdjustment.amt_tax_equivalent_yield(
        amt_muni_yield, fed_rate, amt_rate
    )

    print(f"\n  AMT-subject muni yield:     {amt_muni_yield*100:.2f}%")
    print(f"  AMT rate:                   {amt_rate*100:.0f}%")
    print(f"  After-AMT effective yield:  {after_amt*100:.2f}%")
    print(f"  AMT-adjusted TEY:           {amt_tey*100:.2f}%")

    # Compare to non-AMT muni
    non_amt_tey = MunicipalBondTax.tax_equivalent_yield_federal(muni_yield, fed_rate)
    print(f"\n  Non-AMT muni (3.50%) TEY:   {non_amt_tey*100:.2f}%")
    print(f"  AMT muni (3.80%) AMT-TEY:   {amt_tey*100:.2f}%")

    # ----- Muni/Treasury Ratio -----
    print("\n--- Muni-to-Treasury Ratio ---")

    muni_y = 0.032
    tsy_y = 0.040
    assessment = MuniRatio.relative_value_assessment(muni_y, tsy_y)

    print(f"\n  Muni Yield:   {assessment['muni_yield']*100:.2f}%")
    print(f"  Treasury:     {assessment['treasury_yield']*100:.2f}%")
    print(f"  Ratio:        {assessment['ratio_pct']:.1f}%")
    print(f"  Assessment:   {assessment['assessment']}")

    # Ratio curve
    print("\n  Ratio Curve Across Maturities:")
    maturities = np.array([1, 2, 3, 5, 7, 10, 20, 30], dtype=np.float64)
    muni_yields = np.array([0.028, 0.030, 0.031, 0.033, 0.035, 0.038, 0.042, 0.044])
    tsy_yields = np.array([0.042, 0.043, 0.044, 0.045, 0.046, 0.048, 0.050, 0.051])
    ratios = MuniRatio.ratio_curve(muni_yields, tsy_yields, maturities)

    print(f"  {'Maturity':>10s}  {'Muni':>8s}  {'Treasury':>10s}  {'Ratio':>8s}")
    print(f"  {'-'*10}  {'-'*8}  {'-'*10}  {'-'*8}")
    for mat, m_y, t_y, r in zip(maturities, muni_yields, tsy_yields, ratios):
        print(f"  {mat:9.0f}y  {m_y*100:7.2f}%  {t_y*100:9.2f}%  {r*100:7.1f}%")

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

    # SKILL.md Example 1: TEY with federal and state tax
    tey_full = MunicipalBondTax.tax_equivalent_yield_full(0.035, 0.37, 0.05)
    _check(failures, "Ex1 TEY (fed+state)", tey_full, 0.05848, 1e-5)
    tey_fed = MunicipalBondTax.tax_equivalent_yield_federal(0.035, 0.37)
    _check(failures, "Ex1 TEY (federal only)", tey_fed, 0.055556, 1e-5)

    # De minimis threshold: par 1000, 10 years
    _check(failures, "de minimis threshold", DeMinimis.threshold_price(1000.0, 10.0), 975.0, 1e-9)

    # AMT adjustment (federal_rate no longer needed for the effective yield)
    _check(failures, "AMT-adjusted yield (3.8% at 28% AMT)",
           AMTAdjustment.amt_adjusted_yield(0.038, 0.28), 0.02736, 1e-9)

    # Muni/Treasury ratio
    _check(failures, "muni/Treasury ratio", MuniRatio.yield_ratio(0.032, 0.040), 0.80, 1e-12)

    if failures:
        print(f"\n{len(failures)} check(s) FAILED: {', '.join(failures)}")
        sys.exit(1)
    print("\nAll checks passed.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.strip().splitlines()[2] if __doc__ else "",
        epilog=(
            "Provides: MunicipalBondTax, DeMinimis, AMTAdjustment, MuniRatio. "
            "For programmatic use, import this module (fixed_income_municipal) instead of running it. "
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
