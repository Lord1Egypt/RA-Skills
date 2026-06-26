# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.11"
# ///
"""
Commodity Analysis
==================
Futures pricing (cost of carry), roll yield calculation, contango/backwardation
detection, and commodity index return decomposition (spot + roll + collateral).

Part of Layer 2 (Asset Classes) in the finance skills framework.
"""

import argparse
import sys
import numpy as np


class FuturesPricing:
    """Cost-of-carry model for commodity futures pricing.

    All methods are static — the cost-of-carry relationships are
    deterministic given the input parameters.
    """

    @staticmethod
    def theoretical_futures_price(
        spot: float,
        risk_free_rate: float,
        storage_cost: float,
        convenience_yield: float,
        time_to_expiry: float,
    ) -> float:
        """Compute the theoretical futures price using the cost-of-carry model.

        F = S * exp((r + u - y) * t)

        Parameters
        ----------
        spot : float
            Current spot price. Must be positive.
        risk_free_rate : float
            Annualized risk-free rate (decimal).
        storage_cost : float
            Annualized storage cost as a fraction of spot (decimal).
        convenience_yield : float
            Annualized convenience yield (decimal).
        time_to_expiry : float
            Time to futures expiry in years.

        Returns
        -------
        float
            Theoretical futures price.
        """
        if spot <= 0:
            raise ValueError(f"Spot price must be positive, got {spot}.")
        net_carry = risk_free_rate + storage_cost - convenience_yield
        return spot * np.exp(net_carry * time_to_expiry)

    @staticmethod
    def implied_convenience_yield(
        spot: float,
        futures_price: float,
        risk_free_rate: float,
        storage_cost: float,
        time_to_expiry: float,
    ) -> float:
        """Compute the implied convenience yield from observed futures price.

        y = r + u - (1/t) * ln(F/S)

        Parameters
        ----------
        spot : float
            Current spot price. Must be positive.
        futures_price : float
            Observed futures price. Must be positive.
        risk_free_rate : float
            Annualized risk-free rate (decimal).
        storage_cost : float
            Annualized storage cost as a fraction of spot (decimal).
        time_to_expiry : float
            Time to futures expiry in years. Must be positive.

        Returns
        -------
        float
            Implied convenience yield (annualized, decimal).
        """
        if spot <= 0 or futures_price <= 0:
            raise ValueError("Spot and futures prices must be positive.")
        if time_to_expiry <= 0:
            raise ValueError(f"time_to_expiry must be positive, got {time_to_expiry}.")
        return risk_free_rate + storage_cost - (1.0 / time_to_expiry) * np.log(futures_price / spot)


class CurveAnalysis:
    """Analyze the shape of the commodity futures curve.

    Parameters
    ----------
    prices : np.ndarray
        Array of futures prices ordered by expiry (front month first).
    days_between : np.ndarray or None, optional
        Array of days between consecutive contract expirations. If None,
        assumes 30 days between each contract. Length must be
        len(prices) - 1.
    """

    def __init__(
        self,
        prices: np.ndarray,
        days_between: np.ndarray | None = None,
    ):
        self.prices = np.asarray(prices, dtype=np.float64)
        if len(self.prices) < 2:
            raise ValueError("At least two futures prices are required.")
        if days_between is not None:
            self.days_between = np.asarray(days_between, dtype=np.float64)
            if len(self.days_between) != len(self.prices) - 1:
                raise ValueError(
                    f"days_between length ({len(self.days_between)}) must be "
                    f"len(prices) - 1 ({len(self.prices) - 1})."
                )
        else:
            self.days_between = np.full(len(self.prices) - 1, 30.0)

    def curve_shape(self) -> str:
        """Classify the overall futures curve shape.

        Returns
        -------
        str
            'contango' if the curve is predominantly upward-sloping,
            'backwardation' if predominantly downward-sloping,
            'mixed' if the slope changes direction along the curve.
        """
        diffs = np.diff(self.prices)
        if np.all(diffs > 0):
            return "contango"
        if np.all(diffs < 0):
            return "backwardation"
        return "mixed"

    def is_contango(self) -> bool:
        """Check if the front of the curve is in contango.

        Returns
        -------
        bool
            True if the second contract price exceeds the front contract.
        """
        return bool(self.prices[1] > self.prices[0])

    def is_backwardation(self) -> bool:
        """Check if the front of the curve is in backwardation.

        Returns
        -------
        bool
            True if the front contract price exceeds the second contract.
        """
        return bool(self.prices[0] > self.prices[1])

    def front_roll_yield(self) -> float:
        """Compute the roll yield from front to second contract.

        Roll Yield = (F_near - F_far) / F_near

        Positive in backwardation (sell expensive near, buy cheaper far),
        negative in contango (sell cheaper near, buy expensive far).

        Returns
        -------
        float
            Roll yield (decimal).
        """
        return float((self.prices[0] - self.prices[1]) / self.prices[0])

    def annualized_roll_yield(self) -> float:
        """Compute annualized roll yield from front to second contract.

        Annualized = (F_near / F_far)^(365 / days_between) - 1

        Returns
        -------
        float
            Annualized roll yield (decimal).
        """
        days = self.days_between[0]
        ratio = self.prices[0] / self.prices[1]
        return float(ratio ** (365.0 / days) - 1.0)

    def term_structure(self) -> list[dict]:
        """Compute roll yield between each pair of consecutive contracts.

        Returns
        -------
        list[dict]
            Each dict has keys: 'near_price', 'far_price', 'roll_yield',
            'annualized_roll_yield', 'days_between', 'shape'.
        """
        results = []
        for i in range(len(self.prices) - 1):
            near = self.prices[i]
            far = self.prices[i + 1]
            days = self.days_between[i]
            ry = (near - far) / near
            ann_ry = (near / far) ** (365.0 / days) - 1.0
            shape = "backwardation" if near > far else "contango" if far > near else "flat"
            results.append({
                "near_price": float(near),
                "far_price": float(far),
                "roll_yield": float(ry),
                "annualized_roll_yield": float(ann_ry),
                "days_between": float(days),
                "shape": shape,
            })
        return results


class ReturnDecomposition:
    """Decompose commodity investment returns into spot, roll, and collateral.

    Total Return = Spot Return + Roll Yield + Collateral Yield
    """

    @staticmethod
    def total_return(
        spot_return: float,
        roll_yield: float,
        collateral_yield: float,
    ) -> float:
        """Compute total commodity return from its components.

        Parameters
        ----------
        spot_return : float
            Change in spot price over the period (decimal).
        roll_yield : float
            Roll yield over the period (decimal). Negative in contango,
            positive in backwardation.
        collateral_yield : float
            Interest earned on collateral/margin (decimal). Typically
            the T-bill rate.

        Returns
        -------
        float
            Total return (decimal).
        """
        return spot_return + roll_yield + collateral_yield

    @staticmethod
    def decompose(
        spot_begin: float,
        spot_end: float,
        roll_yield: float,
        risk_free_rate: float,
    ) -> dict[str, float]:
        """Decompose a commodity investment's total return.

        Parameters
        ----------
        spot_begin : float
            Spot price at start of period. Must be positive.
        spot_end : float
            Spot price at end of period.
        roll_yield : float
            Cumulative roll yield over the period (decimal).
        risk_free_rate : float
            Risk-free rate earned on collateral over the period (decimal).

        Returns
        -------
        dict[str, float]
            Keys: 'spot_return', 'roll_yield', 'collateral_yield',
            'total_return'.
        """
        if spot_begin <= 0:
            raise ValueError(f"spot_begin must be positive, got {spot_begin}.")
        spot_ret = (spot_end - spot_begin) / spot_begin
        total = spot_ret + roll_yield + risk_free_rate
        return {
            "spot_return": spot_ret,
            "roll_yield": roll_yield,
            "collateral_yield": risk_free_rate,
            "total_return": total,
        }

    @staticmethod
    def multi_period_spot_return(prices: np.ndarray) -> float:
        """Compute cumulative spot return over multiple periods.

        Parameters
        ----------
        prices : np.ndarray
            Array of spot prices over time. Must have at least 2 entries.

        Returns
        -------
        float
            Cumulative spot return (decimal).
        """
        prices = np.asarray(prices, dtype=np.float64)
        if len(prices) < 2:
            raise ValueError("At least two prices required.")
        return float((prices[-1] - prices[0]) / prices[0])


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Commodity analysis on synthetic data
    # ----------------------------------------------------------------
    print("=" * 60)
    print("Commodity Analysis - Demo")
    print("=" * 60)

    # --- Futures Pricing ---
    print("\n--- Cost-of-Carry Futures Pricing ---")
    spot = 70.0  # crude oil
    r = 0.05     # 5% risk-free rate
    u = 0.03     # 3% storage cost
    y = 0.02     # 2% convenience yield

    f_theory = FuturesPricing.theoretical_futures_price(
        spot=spot, risk_free_rate=r, storage_cost=u,
        convenience_yield=y, time_to_expiry=0.25,
    )
    print(f"Spot: ${spot:.2f}")
    print(f"Theoretical 3-month futures (r={r}, u={u}, y={y}): ${f_theory:.2f}")

    # Implied convenience yield from market price
    market_futures = 71.50
    implied_y = FuturesPricing.implied_convenience_yield(
        spot=spot, futures_price=market_futures,
        risk_free_rate=r, storage_cost=u, time_to_expiry=0.25,
    )
    print(f"Market futures price: ${market_futures:.2f}")
    print(f"Implied convenience yield: {implied_y:.4f} ({implied_y*100:.2f}%)")

    # --- Curve Analysis (Contango example from SKILL.md) ---
    print("\n--- Futures Curve Analysis ---")
    # Contango curve: front < back
    contango_prices = np.array([50.0, 52.0, 53.5, 54.8, 55.5])
    curve = CurveAnalysis(
        prices=contango_prices,
        days_between=np.array([30, 30, 30, 30]),
    )

    print(f"Prices: {contango_prices}")
    print(f"Curve shape: {curve.curve_shape()}")
    print(f"Contango: {curve.is_contango()}, Backwardation: {curve.is_backwardation()}")

    ry = curve.front_roll_yield()
    ann_ry = curve.annualized_roll_yield()
    print(f"Front roll yield: {ry:.4f} ({ry*100:.2f}%)")
    print(f"Annualized roll yield: {ann_ry:.4f} ({ann_ry*100:.2f}%)")

    print("\nTerm structure:")
    for i, seg in enumerate(curve.term_structure()):
        print(f"  Contract {i+1}->{i+2}: ${seg['near_price']:.1f} -> ${seg['far_price']:.1f} "
              f"| roll={seg['roll_yield']:.4f} | ann={seg['annualized_roll_yield']:.4f} "
              f"| {seg['shape']}")

    # Backwardation curve
    print("\n--- Backwardation Example ---")
    backwardation_prices = np.array([80.0, 78.0, 76.5, 75.5])
    curve_back = CurveAnalysis(
        prices=backwardation_prices,
        days_between=np.array([30, 30, 30]),
    )
    print(f"Prices: {backwardation_prices}")
    print(f"Curve shape: {curve_back.curve_shape()}")
    ry_back = curve_back.front_roll_yield()
    print(f"Front roll yield: {ry_back:.4f} ({ry_back*100:.2f}%)")

    # --- Return Decomposition (example from SKILL.md) ---
    print("\n--- Return Decomposition ---")
    decomp = ReturnDecomposition.decompose(
        spot_begin=70.0, spot_end=77.0,
        roll_yield=-0.06, risk_free_rate=0.05,
    )
    print(f"Spot return:       {decomp['spot_return']:.4f} ({decomp['spot_return']*100:.2f}%)")
    print(f"Roll yield:        {decomp['roll_yield']:.4f} ({decomp['roll_yield']*100:.2f}%)")
    print(f"Collateral yield:  {decomp['collateral_yield']:.4f} ({decomp['collateral_yield']*100:.2f}%)")
    print(f"Total return:      {decomp['total_return']:.4f} ({decomp['total_return']*100:.2f}%)")

    # Multi-period spot return
    monthly_spots = np.array([70.0, 72.0, 69.0, 73.0, 75.0, 77.0])
    cumul_spot = ReturnDecomposition.multi_period_spot_return(monthly_spots)
    print(f"\nMulti-period spot return ({monthly_spots[0]} -> {monthly_spots[-1]}): "
          f"{cumul_spot:.4f} ({cumul_spot*100:.2f}%)")

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

    # SKILL.md Example 1: roll yield in contango ($50 front, $52 next)
    curve = CurveAnalysis(prices=np.array([50.0, 52.0]), days_between=np.array([30.0]))
    _check(failures, "Ex1 monthly roll yield", curve.front_roll_yield(), -0.04, 1e-12)
    _check(failures, "Ex1 annualized roll yield (365/30 days)",
           curve.annualized_roll_yield(), -0.379472, 1e-5)
    _check(failures, "Ex1 compounded 12 rolls", (50.0 / 52.0) ** 12 - 1.0, -0.375403, 1e-5)

    # SKILL.md Example 2: total return decomposition
    decomp = ReturnDecomposition.decompose(spot_begin=70.0, spot_end=77.0,
                                           roll_yield=-0.06, risk_free_rate=0.05)
    _check(failures, "Ex2 spot return", decomp["spot_return"], 0.10, 1e-12)
    _check(failures, "Ex2 total return", decomp["total_return"], 0.09, 1e-12)

    if failures:
        print(f"\n{len(failures)} check(s) FAILED: {', '.join(failures)}")
        sys.exit(1)
    print("\nAll checks passed.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.strip().splitlines()[2] if __doc__ else "",
        epilog=(
            "Provides: FuturesPricing, CurveAnalysis, ReturnDecomposition. "
            "For programmatic use, import this module (commodities) instead of running it. "
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
