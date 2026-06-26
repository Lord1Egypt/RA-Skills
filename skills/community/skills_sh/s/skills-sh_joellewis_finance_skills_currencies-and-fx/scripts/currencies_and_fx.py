# /// script
# dependencies = []
# requires-python = ">=3.11"
# ///
"""
Currencies and FX
=================
Covered interest rate parity, forward exchange rates, cross rate derivation,
currency-hedged returns, and unhedged international return decomposition.

Part of Layer 2 (Asset Classes) in the finance skills framework.
"""

import argparse
import sys


class FXForward:
    """Forward exchange rate and interest rate parity calculations.

    All methods are static — no state is required for these arbitrage-based
    pricing relationships.
    """

    @staticmethod
    def forward_rate(
        spot: float,
        domestic_rate: float,
        foreign_rate: float,
        periods: float = 1.0,
    ) -> float:
        """Compute the forward exchange rate using covered interest rate parity.

        F = S * (1 + r_d)^t / (1 + r_f)^t

        Parameters
        ----------
        spot : float
            Spot exchange rate (domestic currency per unit of foreign currency).
        domestic_rate : float
            Domestic interest rate (annualized, decimal).
        foreign_rate : float
            Foreign interest rate (annualized, decimal).
        periods : float, optional
            Time to maturity in years. Default is 1.0.

        Returns
        -------
        float
            Forward exchange rate.
        """
        return spot * ((1.0 + domestic_rate) ** periods) / ((1.0 + foreign_rate) ** periods)

    @staticmethod
    def forward_premium(
        spot: float,
        forward: float,
    ) -> float:
        """Compute the forward premium (or discount) as a fraction of spot.

        Forward Premium = (F - S) / S

        Parameters
        ----------
        spot : float
            Spot exchange rate.
        forward : float
            Forward exchange rate.

        Returns
        -------
        float
            Forward premium (positive) or discount (negative) as a decimal.
        """
        return (forward - spot) / spot

    @staticmethod
    def forward_premium_from_rates(
        domestic_rate: float,
        foreign_rate: float,
    ) -> float:
        """Compute forward premium directly from interest rate differential.

        Forward Premium = (r_d - r_f) / (1 + r_f)

        Parameters
        ----------
        domestic_rate : float
            Domestic interest rate (annualized, decimal).
        foreign_rate : float
            Foreign interest rate (annualized, decimal).

        Returns
        -------
        float
            Forward premium (decimal).
        """
        return (domestic_rate - foreign_rate) / (1.0 + foreign_rate)

    @staticmethod
    def hedging_cost(
        domestic_rate: float,
        foreign_rate: float,
    ) -> float:
        """Approximate annualized cost (or benefit) of hedging FX exposure.

        Hedging Cost ~ r_d - r_f

        When domestic rate > foreign rate, hedging earns a positive return
        (benefit). When domestic rate < foreign rate, hedging has a cost.

        Parameters
        ----------
        domestic_rate : float
            Domestic interest rate (annualized, decimal).
        foreign_rate : float
            Foreign interest rate (annualized, decimal).

        Returns
        -------
        float
            Approximate hedging cost (negative = cost, positive = benefit).
        """
        return domestic_rate - foreign_rate


class CrossRate:
    """Cross rate derivation from common-currency quotes."""

    @staticmethod
    def compute(
        rate_a_per_c: float,
        rate_b_per_c: float,
    ) -> float:
        """Derive cross rate A/B from rates quoted against a common currency C.

        A/B = (A/C) / (B/C)

        Parameters
        ----------
        rate_a_per_c : float
            Exchange rate: units of currency A per unit of currency C.
        rate_b_per_c : float
            Exchange rate: units of currency B per unit of currency C.
            Must be positive.

        Returns
        -------
        float
            Cross rate: units of A per unit of B.

        Raises
        ------
        ValueError
            If rate_b_per_c <= 0.
        """
        if rate_b_per_c <= 0:
            raise ValueError(f"rate_b_per_c must be positive, got {rate_b_per_c}.")
        return rate_a_per_c / rate_b_per_c

    @staticmethod
    def triangular_arbitrage_check(
        rate_ab: float,
        rate_bc: float,
        rate_ac: float,
        tolerance: float = 1e-6,
    ) -> dict:
        """Check for triangular arbitrage opportunity.

        If A/B * B/C != A/C (within tolerance), an arbitrage exists.

        Parameters
        ----------
        rate_ab : float
            Exchange rate A per B.
        rate_bc : float
            Exchange rate B per C.
        rate_ac : float
            Exchange rate A per C.
        tolerance : float, optional
            Maximum deviation before flagging arbitrage. Default is 1e-6.

        Returns
        -------
        dict
            Keys: 'implied_ac' (float), 'actual_ac' (float),
            'deviation' (float), 'arbitrage_exists' (bool).
        """
        implied_ac = rate_ab * rate_bc
        deviation = abs(implied_ac - rate_ac)
        return {
            "implied_ac": implied_ac,
            "actual_ac": rate_ac,
            "deviation": deviation,
            "arbitrage_exists": deviation > tolerance,
        }


class InternationalReturn:
    """Decompose and hedge international investment returns.

    An investor's return on a foreign asset comprises the local-currency
    asset return and the currency return (change in the exchange rate).
    """

    @staticmethod
    def unhedged_return(
        local_return: float,
        currency_return: float,
    ) -> float:
        """Compute unhedged return on a foreign investment.

        R_unhedged = (1 + R_local) * (1 + R_currency) - 1

        Parameters
        ----------
        local_return : float
            Asset return in local (foreign) currency (decimal).
        currency_return : float
            Change in exchange rate — positive means the foreign currency
            appreciated vs domestic (decimal).

        Returns
        -------
        float
            Unhedged return in domestic currency (decimal).
        """
        return (1.0 + local_return) * (1.0 + currency_return) - 1.0

    @staticmethod
    def currency_return(
        spot_begin: float,
        spot_end: float,
    ) -> float:
        """Compute the currency return from spot rate changes.

        R_currency = (S_end - S_begin) / S_begin

        where S is domestic currency per foreign currency.

        Parameters
        ----------
        spot_begin : float
            Spot rate at start of period. Must be positive.
        spot_end : float
            Spot rate at end of period.

        Returns
        -------
        float
            Currency return (decimal).
        """
        if spot_begin <= 0:
            raise ValueError(f"spot_begin must be positive, got {spot_begin}.")
        return (spot_end - spot_begin) / spot_begin

    @staticmethod
    def hedged_return(
        local_return: float,
        domestic_rate: float,
        foreign_rate: float,
    ) -> float:
        """Compute the hedged return on a foreign investment.

        A fully hedged investor earns the local asset return plus the
        interest rate differential (hedging benefit/cost per CIP).

        R_hedged ~ R_local + (r_d - r_f)

        Parameters
        ----------
        local_return : float
            Asset return in local (foreign) currency (decimal).
        domestic_rate : float
            Domestic interest rate for the hedging period (decimal).
        foreign_rate : float
            Foreign interest rate for the hedging period (decimal).

        Returns
        -------
        float
            Hedged return in domestic currency (decimal).
        """
        return local_return + (domestic_rate - foreign_rate)

    @staticmethod
    def return_decomposition(
        local_return: float,
        currency_return: float,
    ) -> dict[str, float]:
        """Decompose unhedged international return into components.

        R_total = R_local + R_currency + R_local * R_currency

        Parameters
        ----------
        local_return : float
            Asset return in local currency (decimal).
        currency_return : float
            Currency return (decimal).

        Returns
        -------
        dict[str, float]
            Keys: 'local_return', 'currency_return', 'interaction_term',
            'total_return'.
        """
        interaction = local_return * currency_return
        total = local_return + currency_return + interaction
        return {
            "local_return": local_return,
            "currency_return": currency_return,
            "interaction_term": interaction,
            "total_return": total,
        }


class RealExchangeRate:
    """Real exchange rate and purchasing power parity calculations."""

    @staticmethod
    def real_rate(
        nominal_rate: float,
        foreign_price_level: float,
        domestic_price_level: float,
    ) -> float:
        """Compute the real exchange rate.

        q = e * (P* / P)

        Parameters
        ----------
        nominal_rate : float
            Nominal exchange rate (domestic per foreign).
        foreign_price_level : float
            Foreign price level index. Must be positive.
        domestic_price_level : float
            Domestic price level index. Must be positive.

        Returns
        -------
        float
            Real exchange rate.
        """
        if foreign_price_level <= 0 or domestic_price_level <= 0:
            raise ValueError("Price levels must be positive.")
        return nominal_rate * (foreign_price_level / domestic_price_level)

    @staticmethod
    def ppp_implied_rate(
        domestic_price_level: float,
        foreign_price_level: float,
    ) -> float:
        """Compute the PPP-implied exchange rate.

        S_ppp = P_domestic / P_foreign

        Parameters
        ----------
        domestic_price_level : float
            Domestic price level. Must be positive.
        foreign_price_level : float
            Foreign price level. Must be positive.

        Returns
        -------
        float
            PPP-implied exchange rate (domestic per foreign).
        """
        if foreign_price_level <= 0 or domestic_price_level <= 0:
            raise ValueError("Price levels must be positive.")
        return domestic_price_level / foreign_price_level


def _demo() -> None:
    # ----------------------------------------------------------------
    # Demo: Currency and FX calculations
    # ----------------------------------------------------------------
    print("=" * 60)
    print("Currencies and FX - Demo")
    print("=" * 60)

    # --- Forward Rate (USD/JPY example from SKILL.md) ---
    print("\n--- Forward Rate Calculation ---")
    spot_usdjpy = 150.0
    us_rate = 0.05
    jp_rate = 0.005

    # Note: USD/JPY means yen per dollar. The domestic currency is JPY
    # when computing F in JPY terms.
    fwd = FXForward.forward_rate(
        spot=spot_usdjpy, domestic_rate=jp_rate, foreign_rate=us_rate, periods=1.0
    )
    print(f"USD/JPY spot: {spot_usdjpy:.2f}")
    print(f"US 1-year rate: {us_rate:.2%}, Japan 1-year rate: {jp_rate:.2%}")
    print(f"1-year forward: {fwd:.2f} JPY/USD")
    prem = FXForward.forward_premium(spot=spot_usdjpy, forward=fwd)
    print(f"Forward premium (JPY): {prem:.4f} ({prem*100:.2f}%)")

    # --- EUR investor hedging example from SKILL.md ---
    print("\n--- Hedging Cost/Benefit ---")
    spot_eurusd = 1.10
    eur_rate = 0.03
    usd_rate = 0.05

    fwd_eurusd = FXForward.forward_rate(
        spot=spot_eurusd, domestic_rate=eur_rate, foreign_rate=usd_rate
    )
    print(f"EUR/USD spot: {spot_eurusd:.4f}")
    print(f"EUR/USD forward: {fwd_eurusd:.4f}")
    hedge_cost = FXForward.hedging_cost(
        domestic_rate=eur_rate, foreign_rate=usd_rate
    )
    print(f"Hedging cost for EUR investor: {hedge_cost:.4f} ({hedge_cost*100:.2f}%)")
    hedge_benefit = (spot_eurusd - fwd_eurusd) / spot_eurusd
    print(f"Hedging benefit (from forward): {hedge_benefit:.4f} ({hedge_benefit*100:.2f}%)")

    # --- Cross Rate ---
    print("\n--- Cross Rate Derivation ---")
    eur_usd = 1.10
    gbp_usd = 1.27
    eur_gbp = CrossRate.compute(rate_a_per_c=eur_usd, rate_b_per_c=gbp_usd)
    print(f"EUR/USD = {eur_usd}, GBP/USD = {gbp_usd}")
    print(f"EUR/GBP = {eur_gbp:.4f}")

    # Triangular arbitrage check
    arb = CrossRate.triangular_arbitrage_check(
        rate_ab=eur_usd, rate_bc=1.0 / gbp_usd, rate_ac=eur_gbp
    )
    print(f"Triangular arbitrage check: deviation = {arb['deviation']:.8f}, "
          f"arbitrage = {arb['arbitrage_exists']}")

    # --- Unhedged International Return ---
    print("\n--- International Return Decomposition ---")
    local_ret = 0.08  # 8% local equity return
    fx_ret = -0.03    # Foreign currency depreciated 3%

    decomp = InternationalReturn.return_decomposition(
        local_return=local_ret, currency_return=fx_ret
    )
    print(f"Local return:      {decomp['local_return']:.4f} ({decomp['local_return']*100:.2f}%)")
    print(f"Currency return:   {decomp['currency_return']:.4f} ({decomp['currency_return']*100:.2f}%)")
    print(f"Interaction term:  {decomp['interaction_term']:.4f} ({decomp['interaction_term']*100:.2f}%)")
    print(f"Total (unhedged):  {decomp['total_return']:.4f} ({decomp['total_return']*100:.2f}%)")

    hedged = InternationalReturn.hedged_return(
        local_return=local_ret, domestic_rate=0.05, foreign_rate=0.03
    )
    print(f"Hedged return:     {hedged:.4f} ({hedged*100:.2f}%)")

    # --- Real Exchange Rate ---
    print("\n--- Real Exchange Rate ---")
    nominal = 1.10  # EUR/USD nominal
    us_cpi = 310.0
    eu_cpi = 125.0  # Eurozone HICP
    real = RealExchangeRate.real_rate(
        nominal_rate=nominal, foreign_price_level=us_cpi, domestic_price_level=eu_cpi
    )
    print(f"Nominal EUR/USD: {nominal:.2f}")
    print(f"Real EUR/USD:    {real:.4f}")

    ppp = RealExchangeRate.ppp_implied_rate(
        domestic_price_level=eu_cpi, foreign_price_level=us_cpi
    )
    print(f"PPP-implied EUR/USD: {ppp:.4f}")
    print(f"Actual vs PPP deviation: {((nominal / ppp) - 1)*100:.1f}%")

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

    # SKILL.md Example 1: USD/JPY 1-year forward
    fwd = FXForward.forward_rate(spot=150.0, domestic_rate=0.005, foreign_rate=0.05)
    _check(failures, "Ex1 1y forward JPY/USD", fwd, 143.5714, 0.01)

    # SKILL.md Example 2: EUR investor hedging USD
    fwd_eur = FXForward.forward_rate(spot=1.10, domestic_rate=0.03, foreign_rate=0.05)
    _check(failures, "Ex2 EUR/USD forward", fwd_eur, 1.0790, 1e-3)
    benefit = (1.10 - fwd_eur) / 1.10
    _check(failures, "Ex2 hedging benefit", benefit, 0.019048, 1e-4)

    # Core concept: cross rate EUR/GBP
    _check(failures, "cross rate EUR/GBP", CrossRate.compute(1.10, 1.27), 0.8661, 1e-4)

    if failures:
        print(f"\n{len(failures)} check(s) FAILED: {', '.join(failures)}")
        sys.exit(1)
    print("\nAll checks passed.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.strip().splitlines()[2] if __doc__ else "",
        epilog=(
            "Provides: FXForward, CrossRate, InternationalReturn, RealExchangeRate. "
            "For programmatic use, import this module (currencies_and_fx) instead of running it. "
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
