# /// script
# dependencies = ["numpy", "scipy"]
# requires-python = ">=3.11"
# ///
"""
Fixed Income — Sovereign
=========================
Bond pricing, yield curve construction (bootstrap), duration, convexity,
yield-to-maturity (Newton's method), forward rates, and DV01.

Part of Layer 2 (Asset Classes) in the finance skills framework.
"""

import argparse
import sys
import numpy as np
from scipy.optimize import brentq


class SovereignBond:
    """Analyze a fixed-coupon government bond with semi-annual payments.

    Parameters
    ----------
    face : float
        Face (par) value of the bond. Default is 1000.
    coupon_rate : float
        Annual coupon rate as a decimal (e.g., 0.04 = 4%).
    maturity_years : float
        Time to maturity in years.
    frequency : int
        Number of coupon payments per year. Default is 2 (semi-annual).
    """

    def __init__(
        self,
        face: float = 1000.0,
        coupon_rate: float = 0.04,
        maturity_years: float = 5.0,
        frequency: int = 2,
    ):
        self.face = face
        self.coupon_rate = coupon_rate
        self.maturity_years = maturity_years
        self.frequency = frequency
        self.n_periods = int(maturity_years * frequency)
        self.coupon = face * coupon_rate / frequency

    def cash_flows(self) -> np.ndarray:
        """Return the vector of cash flows (coupon payments + final principal).

        Returns
        -------
        np.ndarray
            Array of length n_periods. Each element is the coupon payment,
            with the face value added to the final period.
        """
        cfs = np.full(self.n_periods, self.coupon)
        cfs[-1] += self.face
        return cfs

    def period_times(self) -> np.ndarray:
        """Return the time (in periods) of each cash flow.

        Returns
        -------
        np.ndarray
            Array [1, 2, ..., n_periods].
        """
        return np.arange(1, self.n_periods + 1, dtype=np.float64)

    def price(self, ytm: float) -> float:
        """Compute the clean price from a yield to maturity.

        Parameters
        ----------
        ytm : float
            Annual yield to maturity as a decimal.

        Returns
        -------
        float
            P = sum(C / (1+y)^t) + F / (1+y)^n
            where y = ytm / frequency and t = period index.
        """
        y = ytm / self.frequency
        cfs = self.cash_flows()
        t = self.period_times()
        discount = (1.0 + y) ** t
        return float(np.sum(cfs / discount))

    def current_yield(self, market_price: float) -> float:
        """Compute the current yield.

        Parameters
        ----------
        market_price : float
            Market price of the bond.

        Returns
        -------
        float
            Current Yield = Annual Coupon / Price.
        """
        annual_coupon = self.face * self.coupon_rate
        return float(annual_coupon / market_price)

    def ytm(self, market_price: float, tol: float = 1e-10) -> float:
        """Solve for yield to maturity using Brent's method.

        Finds the yield y such that price(y) = market_price.

        Parameters
        ----------
        market_price : float
            Observed market price of the bond.
        tol : float, optional
            Convergence tolerance. Default is 1e-10.

        Returns
        -------
        float
            Annual yield to maturity as a decimal.
        """
        def objective(ytm_guess: float) -> float:
            return self.price(ytm_guess) - market_price

        # Search between -5% and 100% annual yield
        return float(brentq(objective, -0.05, 1.0, xtol=tol))

    def macaulay_duration(self, ytm: float) -> float:
        """Compute Macaulay duration in years.

        Parameters
        ----------
        ytm : float
            Annual yield to maturity as a decimal.

        Returns
        -------
        float
            D_mac = (1/P) * sum(t * CF_t / (1+y)^t), converted to years.
        """
        y = ytm / self.frequency
        cfs = self.cash_flows()
        t = self.period_times()
        discount = (1.0 + y) ** t
        p = np.sum(cfs / discount)
        # Weighted average of period times, converted to years
        weighted_sum = np.sum(t * cfs / discount)
        return float(weighted_sum / p / self.frequency)

    def modified_duration(self, ytm: float) -> float:
        """Compute modified duration.

        Parameters
        ----------
        ytm : float
            Annual yield to maturity as a decimal.

        Returns
        -------
        float
            D_mod = D_mac / (1 + y/m), where m = frequency.
        """
        d_mac = self.macaulay_duration(ytm)
        return float(d_mac / (1.0 + ytm / self.frequency))

    def convexity(self, ytm: float) -> float:
        """Compute convexity of the bond.

        Parameters
        ----------
        ytm : float
            Annual yield to maturity as a decimal.

        Returns
        -------
        float
            C = (1/P) * sum(t*(t+1) * CF_t / (1+y)^(t+2)) / m^2
        """
        y = ytm / self.frequency
        cfs = self.cash_flows()
        t = self.period_times()
        discount = (1.0 + y) ** t
        p = np.sum(cfs / discount)
        conv_sum = np.sum(t * (t + 1) * cfs / ((1.0 + y) ** (t + 2)))
        return float(conv_sum / p / self.frequency ** 2)

    def dv01(self, ytm: float) -> float:
        """Compute DV01 (dollar value of a basis point).

        Parameters
        ----------
        ytm : float
            Annual yield to maturity as a decimal.

        Returns
        -------
        float
            DV01 = D_mod * P * 0.0001
        """
        p = self.price(ytm)
        d_mod = self.modified_duration(ytm)
        return float(d_mod * p * 0.0001)

    def price_change_estimate(self, ytm: float, delta_y: float) -> dict:
        """Estimate price change using duration and convexity.

        Parameters
        ----------
        ytm : float
            Current annual yield to maturity.
        delta_y : float
            Change in yield as a decimal (e.g., 0.005 = +50bp).

        Returns
        -------
        dict
            Dictionary with keys: 'duration_effect', 'convexity_effect',
            'total_pct_change', 'estimated_new_price'.
        """
        p = self.price(ytm)
        d_mod = self.modified_duration(ytm)
        conv = self.convexity(ytm)

        duration_effect = -d_mod * delta_y
        convexity_effect = 0.5 * conv * delta_y ** 2
        total_pct = duration_effect + convexity_effect

        return {
            "duration_effect": float(duration_effect),
            "convexity_effect": float(convexity_effect),
            "total_pct_change": float(total_pct),
            "estimated_new_price": float(p * (1.0 + total_pct)),
        }

    def summary(self, ytm: float) -> dict:
        """Compute all analytics for the bond at a given yield.

        Parameters
        ----------
        ytm : float
            Annual yield to maturity as a decimal.

        Returns
        -------
        dict
            Dictionary of all computed metrics.
        """
        return {
            "price": self.price(ytm),
            "current_yield": self.current_yield(self.price(ytm)),
            "ytm": ytm,
            "macaulay_duration": self.macaulay_duration(ytm),
            "modified_duration": self.modified_duration(ytm),
            "convexity": self.convexity(ytm),
            "dv01": self.dv01(ytm),
        }


class YieldCurve:
    """Bootstrap a zero-coupon (spot) curve and derive forward rates.

    Parameters
    ----------
    maturities : np.ndarray
        Maturities in years (e.g., [0.5, 1.0, 1.5, 2.0]).
    par_yields : np.ndarray
        Par yields (annual, decimal) for each maturity. Assumes semi-annual
        coupon bonds priced at par.
    """

    def __init__(
        self,
        maturities: np.ndarray,
        par_yields: np.ndarray,
    ):
        self.maturities = np.asarray(maturities, dtype=np.float64)
        self.par_yields = np.asarray(par_yields, dtype=np.float64)
        self.spot_rates = self._bootstrap()

    def _bootstrap(self) -> np.ndarray:
        """Bootstrap zero-coupon spot rates from par yields.

        Spot rates are semi-annually compounded (bond-equivalent yields).
        Each par bond pays coupons every six months, so intermediate coupon
        dates generally fall *between* curve nodes. Those coupons are
        discounted at spot rates linearly interpolated between the
        already-bootstrapped nodes and the (unknown) spot at the current
        maturity, which is solved with a root-finder so the par bond
        reprices exactly to 1.0.

        Returns
        -------
        np.ndarray
            Spot rates (annual, semi-annually compounded) for each maturity.
        """
        spots: list[float] = []
        known_maturities: list[float] = []

        for mat, par_y in zip(self.maturities, self.par_yields):
            n_periods = int(round(mat * 2))  # semi-annual
            coupon = par_y / 2.0  # semi-annual coupon per $1 face
            times = np.arange(1, n_periods + 1) * 0.5

            def par_pricing_error(s_candidate: float) -> float:
                curve_mats = np.array(known_maturities + [mat])
                curve_spots = np.array(spots + [s_candidate])
                s_t = np.interp(times, curve_mats, curve_spots)
                dfs = (1.0 + s_t / 2.0) ** -(2.0 * times)
                pv = coupon * np.sum(dfs[:-1]) + (1.0 + coupon) * dfs[-1]
                return pv - 1.0

            s_i = brentq(par_pricing_error, -0.5, 1.0, xtol=1e-12)
            spots.append(float(s_i))
            known_maturities.append(float(mat))

        return np.array(spots)

    def forward_rate(self, t1: float, t2: float) -> float:
        """Compute the implied forward rate between two future dates.

        Consistent with the bootstrapped curve, spot rates are treated as
        semi-annually compounded. The forward is derived from discount
        factors and returned on the same semi-annual (bond-equivalent)
        convention:

            f(t1,t2) = 2 * [ (DF(t1)/DF(t2))^(1/(2*(t2-t1))) - 1 ]

        Parameters
        ----------
        t1 : float
            Start of the forward period in years.
        t2 : float
            End of the forward period in years. Must be > t1.

        Returns
        -------
        float
            Annualized forward rate (semi-annually compounded).
        """
        if t2 <= t1:
            raise ValueError(f"t2 ({t2}) must be greater than t1 ({t1}).")

        df1 = self.discount_factor(t1)
        df2 = self.discount_factor(t2)
        fwd = 2.0 * ((df1 / df2) ** (1.0 / (2.0 * (t2 - t1))) - 1.0)
        return float(fwd)

    def discount_factor(self, t: float) -> float:
        """Compute the discount factor for a given maturity.

        Uses the semi-annual compounding convention of the bootstrapped
        spot curve.

        Parameters
        ----------
        t : float
            Maturity in years.

        Returns
        -------
        float
            DF = 1 / (1 + s_t/2)^(2t)
        """
        s = float(np.interp(t, self.maturities, self.spot_rates))
        return float(1.0 / (1.0 + s / 2.0) ** (2.0 * t))

    def price_par_bond(self, maturity: float, par_yield: float) -> float:
        """Price a semi-annual par-coupon bond off the bootstrapped curve.

        Used as a sanity check: pricing each input par bond should return
        approximately 1.0 (par).

        Parameters
        ----------
        maturity : float
            Bond maturity in years.
        par_yield : float
            Annual coupon rate (decimal) of the par bond.

        Returns
        -------
        float
            Price per $1 face.
        """
        n_periods = int(round(maturity * 2))
        coupon = par_yield / 2.0
        times = np.arange(1, n_periods + 1) * 0.5
        dfs = np.array([self.discount_factor(t) for t in times])
        return float(coupon * np.sum(dfs[:-1]) + (1.0 + coupon) * dfs[-1])

    def summary(self) -> dict:
        """Return the bootstrapped curve data.

        Returns
        -------
        dict
            Dictionary with maturities, par_yields, and spot_rates.
        """
        return {
            "maturities": self.maturities.tolist(),
            "par_yields": self.par_yields.tolist(),
            "spot_rates": self.spot_rates.tolist(),
        }


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Sovereign bond analytics and yield curve bootstrapping
    # ----------------------------------------------------------------
    print("=" * 60)
    print("Fixed Income Sovereign — Demo")
    print("=" * 60)

    # ----- Bond Pricing and Analytics -----
    print("\n--- Bond Pricing and Analytics ---")
    bond = SovereignBond(
        face=1000.0,
        coupon_rate=0.04,
        maturity_years=5.0,
        frequency=2,
    )

    ytm = 0.05
    price = bond.price(ytm)
    print(f"\n5-Year 4% Semi-Annual Bond at 5% YTM:")
    print(f"  Price:              ${price:.2f}")
    print(f"  Current Yield:      {bond.current_yield(price)*100:.3f}%")
    print(f"  Macaulay Duration:  {bond.macaulay_duration(ytm):.4f} years")
    print(f"  Modified Duration:  {bond.modified_duration(ytm):.4f} years")
    print(f"  Convexity:          {bond.convexity(ytm):.4f}")
    print(f"  DV01:               ${bond.dv01(ytm):.4f}")

    # Verify YTM solver round-trips
    solved_ytm = bond.ytm(price)
    print(f"\n  YTM solver verification:")
    print(f"    Input YTM:  {ytm*100:.4f}%")
    print(f"    Solved YTM: {solved_ytm*100:.4f}%")

    # Price change estimate for +50bp
    print(f"\n  Price change estimate for +50bp yield increase:")
    estimate = bond.price_change_estimate(ytm, 0.005)
    print(f"    Duration effect:   {estimate['duration_effect']*100:.4f}%")
    print(f"    Convexity effect:  {estimate['convexity_effect']*100:.4f}%")
    print(f"    Total change:      {estimate['total_pct_change']*100:.4f}%")
    print(f"    Estimated price:   ${estimate['estimated_new_price']:.2f}")
    actual_new_price = bond.price(ytm + 0.005)
    print(f"    Actual price:      ${actual_new_price:.2f}")
    print(f"    Approximation error: ${abs(estimate['estimated_new_price'] - actual_new_price):.4f}")

    # ----- Yield Curve Bootstrapping -----
    print("\n\n--- Yield Curve Bootstrapping ---")
    maturities = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 5.0, 7.0, 10.0])
    par_yields = np.array([0.042, 0.043, 0.044, 0.045, 0.046, 0.047, 0.048, 0.049, 0.050])

    curve = YieldCurve(maturities=maturities, par_yields=par_yields)

    print("\n  Maturity   Par Yield   Spot Rate   Discount Factor")
    print("  " + "-" * 52)
    for mat, par_y, spot in zip(maturities, par_yields, curve.spot_rates):
        df = curve.discount_factor(mat)
        print(f"  {mat:6.1f}y    {par_y*100:6.3f}%     {spot*100:6.3f}%     {df:.6f}")

    # Sanity check: every input par bond should reprice to ~1.0 off the curve
    reprice_errors = [
        abs(curve.price_par_bond(m, py) - 1.0)
        for m, py in zip(maturities, par_yields)
    ]
    print(f"\n  Bootstrap sanity check: max par-bond repricing error = "
          f"{max(reprice_errors):.2e} (should be ~0)")

    # Forward rates
    print("\n  Selected Forward Rates (semi-annual convention):")
    forwards = [(0.5, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 5.0), (5.0, 10.0)]
    for t1, t2 in forwards:
        fwd = curve.forward_rate(t1, t2)
        print(f"    f({t1:.1f}, {t2:.1f}) = {fwd*100:.3f}%")

    # Full summary
    print("\n  Full Summary:")
    summary = bond.summary(ytm)
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"    {key:25s}: {value:.6f}")

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

    # SKILL.md Example 1: 5y 4% semi-annual bond at 5% YTM prices at 956.24
    bond = SovereignBond(face=1000.0, coupon_rate=0.04, maturity_years=5.0, frequency=2)
    price = bond.price(0.05)
    _check(failures, "Ex1 bond price", price, 956.24, 0.01)
    _check(failures, "YTM solver round trip", bond.ytm(price), 0.05, 1e-8)

    # SKILL.md Example 2 pattern: duration/convexity price-change estimate is close to actual
    est = bond.price_change_estimate(0.05, 0.005)
    actual = bond.price(0.055)
    _check(failures, "Ex2 duration+convexity estimate vs actual reprice",
           est["estimated_new_price"], actual, 0.05)

    # Bootstrap sanity check: input par bonds reprice to par off the curve
    maturities = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 5.0, 7.0, 10.0])
    par_yields = np.array([0.042, 0.043, 0.044, 0.045, 0.046, 0.047, 0.048, 0.049, 0.050])
    curve = YieldCurve(maturities=maturities, par_yields=par_yields)
    max_err = max(abs(curve.price_par_bond(m, py) - 1.0)
                  for m, py in zip(maturities, par_yields))
    _check(failures, "bootstrap par-bond repricing max error", max_err, 0.0, 1e-8)
    _check(failures, "10y spot above 10y par on upward curve", curve.spot_rates[-1], 0.050398, 5e-5)

    if failures:
        print(f"\n{len(failures)} check(s) FAILED: {', '.join(failures)}")
        sys.exit(1)
    print("\nAll checks passed.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.strip().splitlines()[2] if __doc__ else "",
        epilog=(
            "Provides: SovereignBond, YieldCurve. "
            "For programmatic use, import this module (fixed_income_sovereign) instead of running it. "
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
