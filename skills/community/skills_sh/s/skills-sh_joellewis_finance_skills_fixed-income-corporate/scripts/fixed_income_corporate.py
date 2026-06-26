# /// script
# dependencies = ["numpy", "scipy"]
# requires-python = ">=3.11"
# ///
"""
Fixed Income — Corporate
=========================
Credit spread calculation (G-spread, Z-spread, OAS approximation), expected
loss from default probability and recovery rate, and credit migration
probability analysis.

Part of Layer 2 (Asset Classes) in the finance skills framework.
"""

import argparse
import sys
import numpy as np
from scipy.optimize import brentq


class CreditSpread:
    """Compute credit spread measures for a corporate bond.

    All spread calculations require the bond's cash flows, market price,
    and a risk-free yield curve (spot rates).

    Parameters
    ----------
    cash_flows : np.ndarray
        Array of cash flows (coupon + principal at maturity).
    cash_flow_times : np.ndarray
        Array of times (in years) corresponding to each cash flow.
    market_price : float
        Observed market price of the corporate bond.
    spot_rates : np.ndarray
        Risk-free spot (zero-coupon) rates for each cash flow time,
        as annual decimals.
    """

    def __init__(
        self,
        cash_flows: np.ndarray,
        cash_flow_times: np.ndarray,
        market_price: float,
        spot_rates: np.ndarray,
    ):
        self.cash_flows = np.asarray(cash_flows, dtype=np.float64)
        self.cash_flow_times = np.asarray(cash_flow_times, dtype=np.float64)
        self.market_price = market_price
        self.spot_rates = np.asarray(spot_rates, dtype=np.float64)

    def risk_free_price(self) -> float:
        """Compute the price using the risk-free spot curve (no spread).

        Returns
        -------
        float
            Sum of cash flows discounted at the corresponding spot rates.
        """
        discount = (1.0 + self.spot_rates) ** self.cash_flow_times
        return float(np.sum(self.cash_flows / discount))

    def g_spread(self, bond_ytm: float, treasury_ytm: float) -> float:
        """Compute the G-spread (Government spread).

        Parameters
        ----------
        bond_ytm : float
            Yield to maturity of the corporate bond (annual, decimal).
        treasury_ytm : float
            Interpolated Treasury yield at the same maturity (annual, decimal).

        Returns
        -------
        float
            G-spread = bond_ytm - treasury_ytm, in decimal.
        """
        return float(bond_ytm - treasury_ytm)

    def z_spread(self, tol: float = 1e-10) -> float:
        """Compute the Z-spread (zero-volatility spread).

        The constant spread added to each risk-free spot rate such that
        the discounted cash flows equal the market price.

        Parameters
        ----------
        tol : float, optional
            Convergence tolerance. Default is 1e-10.

        Returns
        -------
        float
            Z-spread as an annual decimal.
        """
        def objective(spread: float) -> float:
            discount = (1.0 + self.spot_rates + spread) ** self.cash_flow_times
            pv = np.sum(self.cash_flows / discount)
            return pv - self.market_price

        lo, hi = -0.05, 1.0
        try:
            return float(brentq(objective, lo, hi, xtol=tol))
        except ValueError as exc:
            raise ValueError(
                f"Z-spread root not bracketed in [{lo:.0%}, {hi:.0%}]: the "
                f"market price ({self.market_price}) is inconsistent with the "
                "cash flows and spot curve (PV at the bracket endpoints does "
                "not straddle the price). Check that cash flows, times, spot "
                "rates, and price are on consistent scales."
            ) from exc

    def oas(self, z_spread: float, option_cost: float) -> float:
        """Compute the Option-Adjusted Spread.

        Parameters
        ----------
        z_spread : float
            Z-spread of the bond (annual, decimal).
        option_cost : float
            Value of the embedded option in spread terms (annual, decimal).
            Positive for callable bonds (issuer benefits from the option).

        Returns
        -------
        float
            OAS = Z-spread - option_cost
        """
        return float(z_spread - option_cost)

    def summary(self, bond_ytm: float, treasury_ytm: float,
                option_cost: float = 0.0) -> dict:
        """Compute all spread measures.

        Parameters
        ----------
        bond_ytm : float
            YTM of the corporate bond.
        treasury_ytm : float
            Interpolated Treasury YTM for the same maturity.
        option_cost : float, optional
            Embedded option cost in spread terms. Default 0.0 (bullet bond).

        Returns
        -------
        dict
            Dictionary of spread measures.
        """
        z_spd = self.z_spread()
        return {
            "g_spread": self.g_spread(bond_ytm, treasury_ytm),
            "z_spread": z_spd,
            "oas": self.oas(z_spd, option_cost),
            "risk_free_price": self.risk_free_price(),
            "market_price": self.market_price,
        }


class CreditRisk:
    """Expected loss and default probability analysis.

    Provides static methods for credit loss calculations.
    """

    @staticmethod
    def expected_loss(
        probability_of_default: float,
        loss_given_default: float,
        exposure_at_default: float,
    ) -> float:
        """Compute expected credit loss.

        Parameters
        ----------
        probability_of_default : float
            PD as a decimal (e.g., 0.02 = 2%).
        loss_given_default : float
            LGD as a decimal (e.g., 0.60 = 60%).
        exposure_at_default : float
            EAD in dollar terms.

        Returns
        -------
        float
            EL = PD * LGD * EAD
        """
        return float(probability_of_default * loss_given_default * exposure_at_default)

    @staticmethod
    def recovery_rate(loss_given_default: float) -> float:
        """Compute recovery rate from LGD.

        Parameters
        ----------
        loss_given_default : float
            LGD as a decimal.

        Returns
        -------
        float
            RR = 1 - LGD
        """
        return float(1.0 - loss_given_default)

    @staticmethod
    def implied_default_probability(
        credit_spread: float,
        loss_given_default: float,
    ) -> float:
        """Estimate market-implied default probability from spread and LGD.

        Uses the simple approximation: spread ~ PD * LGD.

        Parameters
        ----------
        credit_spread : float
            Credit spread as a decimal (e.g., 0.015 = 150bp).
        loss_given_default : float
            LGD as a decimal.

        Returns
        -------
        float
            Implied PD = spread / LGD.
        """
        if loss_given_default == 0:
            raise ValueError("LGD cannot be zero for implied PD calculation.")
        return float(credit_spread / loss_given_default)

    @staticmethod
    def cumulative_default_probability(
        annual_pd: float,
        years: int,
    ) -> float:
        """Compute cumulative default probability over multiple years.

        Assumes constant annual PD and independence across years.

        Parameters
        ----------
        annual_pd : float
            Annual probability of default as a decimal.
        years : int
            Number of years.

        Returns
        -------
        float
            Cumulative PD = 1 - (1 - annual_pd)^years
        """
        return float(1.0 - (1.0 - annual_pd) ** years)

    @staticmethod
    def yield_to_worst(
        ytm: float,
        ytc_values: list[float],
    ) -> float:
        """Compute yield-to-worst.

        Parameters
        ----------
        ytm : float
            Yield to maturity.
        ytc_values : list[float]
            List of yield-to-call values for each call date.

        Returns
        -------
        float
            min(YTM, YTC_1, YTC_2, ...)
        """
        all_yields = [ytm] + list(ytc_values)
        return float(min(all_yields))


class MigrationMatrix:
    """Credit rating transition (migration) matrix analysis.

    Parameters
    ----------
    matrix : np.ndarray
        Square transition matrix where element (i,j) is the probability
        of migrating from rating i to rating j over one period.
        Rows must sum to 1.0. The last column represents default.
    rating_labels : list[str]
        Labels for each rating state (e.g., ['AAA', 'AA', ..., 'D']).
    """

    def __init__(
        self,
        matrix: np.ndarray,
        rating_labels: list[str],
    ):
        self.matrix = np.asarray(matrix, dtype=np.float64)
        self.rating_labels = rating_labels
        if self.matrix.shape[0] != self.matrix.shape[1]:
            raise ValueError("Transition matrix must be square.")
        if len(rating_labels) != self.matrix.shape[0]:
            raise ValueError("Number of labels must match matrix dimension.")

    def transition_probability(self, from_rating: str, to_rating: str) -> float:
        """Look up the 1-period transition probability.

        Parameters
        ----------
        from_rating : str
            Starting rating label.
        to_rating : str
            Ending rating label.

        Returns
        -------
        float
            Probability of transitioning from from_rating to to_rating.
        """
        i = self.rating_labels.index(from_rating)
        j = self.rating_labels.index(to_rating)
        return float(self.matrix[i, j])

    def multi_period_matrix(self, periods: int) -> np.ndarray:
        """Compute the multi-period transition matrix via matrix exponentiation.

        Parameters
        ----------
        periods : int
            Number of periods.

        Returns
        -------
        np.ndarray
            M^periods, the cumulative transition matrix.
        """
        result = np.linalg.matrix_power(self.matrix, periods)
        return result

    def upgrade_probability(self, rating: str) -> float:
        """Probability of any upgrade from the given rating.

        Parameters
        ----------
        rating : str
            Current rating label.

        Returns
        -------
        float
            Sum of probabilities of moving to any higher-rated state.
        """
        idx = self.rating_labels.index(rating)
        # Ratings are ordered from highest to lowest; upgrade = move left
        return float(np.sum(self.matrix[idx, :idx]))

    def downgrade_probability(self, rating: str) -> float:
        """Probability of any downgrade from the given rating.

        Parameters
        ----------
        rating : str
            Current rating label.

        Returns
        -------
        float
            Sum of probabilities of moving to any lower-rated state.
        """
        idx = self.rating_labels.index(rating)
        # Downgrade = move right (excluding the stay-in-place diagonal)
        return float(np.sum(self.matrix[idx, idx + 1:]))

    def default_probability(self, rating: str) -> float:
        """Probability of defaulting from the given rating (1-period).

        Parameters
        ----------
        rating : str
            Current rating label.

        Returns
        -------
        float
            Probability of transitioning to the default state (last column).
        """
        idx = self.rating_labels.index(rating)
        return float(self.matrix[idx, -1])


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Corporate bond credit analysis
    # ----------------------------------------------------------------
    print("=" * 60)
    print("Fixed Income Corporate — Demo")
    print("=" * 60)

    # ----- Z-spread and G-spread -----
    print("\n--- Credit Spread Analysis ---")

    # 7-year corporate bond, semi-annual coupons
    face = 1000.0
    coupon_rate = 0.058  # 5.8% coupon
    n_periods = 14  # 7 years, semi-annual
    coupon = face * coupon_rate / 2.0

    cash_flows = np.full(n_periods, coupon)
    cash_flows[-1] += face
    times = np.arange(1, n_periods + 1) * 0.5  # 0.5, 1.0, ..., 7.0

    # Upward-sloping spot curve
    spot_rates = np.array([
        0.040, 0.041, 0.042, 0.043, 0.044, 0.045, 0.046,
        0.047, 0.048, 0.049, 0.050, 0.051, 0.052, 0.053,
    ])

    market_price = 985.0  # trading below par

    spreads = CreditSpread(
        cash_flows=cash_flows,
        cash_flow_times=times,
        market_price=market_price,
        spot_rates=spot_rates,
    )

    bond_ytm = 0.058
    treasury_ytm = 0.045
    g_spd = spreads.g_spread(bond_ytm, treasury_ytm)
    z_spd = spreads.z_spread()

    print(f"\n  7-Year Corporate Bond (5.8% coupon, price = ${market_price:.2f}):")
    print(f"    G-spread:          {g_spd*10000:.1f} bp")
    print(f"    Z-spread:          {z_spd*10000:.1f} bp")
    print(f"    Risk-free price:   ${spreads.risk_free_price():.2f}")

    # OAS for a callable bond
    option_cost = 0.0015  # 15bp option cost
    oas_value = spreads.oas(z_spd, option_cost)
    print(f"    OAS (15bp option):  {oas_value*10000:.1f} bp")

    # ----- Expected Loss -----
    print("\n--- Expected Loss Calculation ---")

    pd = 0.02  # 2% annual PD
    lgd = 0.60  # 60% LGD
    ead = 1_000_000.0

    el = CreditRisk.expected_loss(pd, lgd, ead)
    rr = CreditRisk.recovery_rate(lgd)
    print(f"\n  PD = {pd*100:.1f}%, LGD = {lgd*100:.0f}%, EAD = ${ead:,.0f}")
    print(f"    Expected Loss:     ${el:,.0f}")
    print(f"    Recovery Rate:     {rr*100:.0f}%")
    print(f"    EL as % of EAD:   {el/ead*100:.2f}%")

    # Implied PD from spread
    spread_for_impl = 0.015  # 150bp
    implied_pd = CreditRisk.implied_default_probability(spread_for_impl, lgd)
    print(f"\n  Implied PD from 150bp spread (LGD=60%): {implied_pd*100:.2f}%")

    # Cumulative PD
    for years in [1, 3, 5, 10]:
        cum_pd = CreditRisk.cumulative_default_probability(pd, years)
        print(f"    Cumulative PD ({years:2d}yr): {cum_pd*100:.2f}%")

    # Yield-to-worst
    ytw = CreditRisk.yield_to_worst(
        ytm=0.058,
        ytc_values=[0.055, 0.052, 0.057],
    )
    print(f"\n  YTM = 5.80%, YTCs = [5.50%, 5.20%, 5.70%]")
    print(f"    Yield-to-Worst:    {ytw*100:.2f}%")

    # ----- Migration Matrix -----
    print("\n--- Credit Migration Matrix ---")

    labels = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC", "D"]
    # Simplified 1-year transition matrix (illustrative, not empirical)
    migration = np.array([
        [0.9080, 0.0830, 0.0060, 0.0012, 0.0006, 0.0002, 0.0000, 0.0010],
        [0.0070, 0.9070, 0.0740, 0.0060, 0.0014, 0.0011, 0.0002, 0.0033],
        [0.0009, 0.0227, 0.9105, 0.0552, 0.0074, 0.0026, 0.0001, 0.0006],
        [0.0002, 0.0033, 0.0595, 0.8693, 0.0530, 0.0117, 0.0012, 0.0018],
        [0.0003, 0.0014, 0.0067, 0.0773, 0.8053, 0.0884, 0.0100, 0.0106],
        [0.0000, 0.0011, 0.0024, 0.0043, 0.0648, 0.8346, 0.0407, 0.0521],
        [0.0022, 0.0000, 0.0022, 0.0130, 0.0238, 0.1124, 0.6486, 0.1978],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000],
    ])

    mm = MigrationMatrix(matrix=migration, rating_labels=labels)

    for rating in ["AAA", "A", "BBB", "BB", "B"]:
        stay = mm.transition_probability(rating, rating)
        upgrade = mm.upgrade_probability(rating)
        downgrade = mm.downgrade_probability(rating)
        default = mm.default_probability(rating)
        print(f"\n  {rating}:")
        print(f"    Stay:      {stay*100:.2f}%")
        print(f"    Upgrade:   {upgrade*100:.2f}%")
        print(f"    Downgrade: {downgrade*100:.2f}%")
        print(f"    Default:   {default*100:.2f}%")

    # Multi-period (5-year cumulative)
    m5 = mm.multi_period_matrix(5)
    bbb_idx = labels.index("BBB")
    print(f"\n  BBB 5-year cumulative default probability: {m5[bbb_idx, -1]*100:.2f}%")

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

    # SKILL.md Example 1: G-spread = 5.8% - 4.5% = 130bp
    cash_flows = np.full(14, 29.0)
    cash_flows[-1] += 1000.0
    times = np.arange(1, 15) * 0.5
    spot_rates = np.array([0.040, 0.041, 0.042, 0.043, 0.044, 0.045, 0.046,
                           0.047, 0.048, 0.049, 0.050, 0.051, 0.052, 0.053])
    spreads = CreditSpread(cash_flows, times, market_price=985.0, spot_rates=spot_rates)
    _check(failures, "Ex1 G-spread", spreads.g_spread(0.058, 0.045), 0.013, 1e-12)

    # Z-spread round trip: price the bond with a known 118bp spread, then recover it
    known_spread = 0.0118
    price = float(np.sum(cash_flows / (1.0 + spot_rates + known_spread) ** times))
    roundtrip = CreditSpread(cash_flows, times, market_price=price, spot_rates=spot_rates)
    _check(failures, "Z-spread round trip (118bp)", roundtrip.z_spread(), known_spread, 1e-8)

    # SKILL.md Example 2: expected loss
    _check(failures, "Ex2 expected loss", CreditRisk.expected_loss(0.02, 0.60, 1_000_000), 12000.0, 1e-9)
    _check(failures, "recovery rate (LGD 60%)", CreditRisk.recovery_rate(0.60), 0.40, 1e-12)
    _check(failures, "yield-to-worst", CreditRisk.yield_to_worst(0.058, [0.055, 0.052, 0.057]), 0.052, 1e-12)

    if failures:
        print(f"\n{len(failures)} check(s) FAILED: {', '.join(failures)}")
        sys.exit(1)
    print("\nAll checks passed.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.strip().splitlines()[2] if __doc__ else "",
        epilog=(
            "Provides: CreditSpread, CreditRisk, MigrationMatrix. "
            "For programmatic use, import this module (fixed_income_corporate) instead of running it. "
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
