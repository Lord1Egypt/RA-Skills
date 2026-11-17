"""
Options Play Recommender
========================
Given an ExpirationForecast (risk-neutral density + CI bands) from
expiration_model.py, generate candidate option strategies with strikes
anchored to the CI quantiles. For each play compute:

  - Probability of Profit (PoP) via integration under the BL density
  - Max profit, max loss, breakeven(s)
  - Capital intensity (cost or credit as % of spot)
  - Reward/risk ratio

Output is ranked; the top N are surfaced to the user.

Strategy universe (each tied to a market view):
  BULLISH  + tight CI → Bull Call Spread (debit)
  BULLISH  + wide CI  → Bull Put Spread (credit, benefits from IV crush)
  BEARISH  + tight CI → Bear Put Spread (debit)
  BEARISH  + wide CI  → Bear Call Spread (credit)
  NEUTRAL  + wide CI  → Iron Condor (credit, IV crush)
  NEUTRAL  + tight CI → Long Butterfly (cheap, narrow zone)
  VOLATILE + low IV   → Long Straddle (debit, pays if breakout)

Note: PoP here is the RISK-NEUTRAL probability, which underestimates the
real-world PoP for short-vol strategies (because of VRP) and overestimates
it for long-vol strategies. Treat as a relative ranking tool, not as a
calibrated real-world probability.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from scipy.integrate import trapezoid

from expiration_model import (
    ExpirationForecast, _black_scholes_call, _black_scholes_put,
    RISK_FREE_RATE, DIVIDEND_YIELD_DEFAULT,
)


@dataclass
class OptionLeg:
    action: str       # "BUY" or "SELL"
    type: str         # "CALL" or "PUT"
    strike: float
    approx_price: float  # BS price at forecast expiry
    qty: int = 1


@dataclass
class OptionsPlay:
    name: str
    bias: str             # "BULLISH", "BEARISH", "NEUTRAL", "VOLATILE"
    structure: str        # short description
    legs: list[OptionLeg]
    net_debit: float      # + = pay this; - = receive this credit (per share)
    max_profit: float | None
    max_loss: float | None
    breakevens: list[float]
    pop_risk_neutral: float  # probability of any profit under BL density
    reward_to_risk: float | None
    rationale: str
    payoff_fn: Callable[[float], float] = field(repr=False)

    def cost_label(self) -> str:
        if self.net_debit > 0:
            return f"debit ${self.net_debit:.2f}/sh (${self.net_debit*100:.0f}/contract)"
        return f"credit ${-self.net_debit:.2f}/sh (${-self.net_debit*100:.0f}/contract)"

    def format(self) -> str:
        lines = [
            f"  ► {self.name}  [{self.bias}]  — {self.structure}",
            f"    {self.cost_label()}  |  PoP (RN): {self.pop_risk_neutral:.0%}  |  "
            f"R/R: {self.reward_to_risk:.2f}" if self.reward_to_risk else
            f"    {self.cost_label()}  |  PoP (RN): {self.pop_risk_neutral:.0%}",
        ]
        for leg in self.legs:
            lines.append(
                f"      {leg.action} {leg.qty}× ${leg.strike:<7,.0f} {leg.type.upper():<4} "
                f"@ ${leg.approx_price:<5.2f}"
            )
        if self.breakevens:
            lines.append("    Breakeven(s): " + ", ".join(f"${b:,.0f}" for b in self.breakevens))
        if self.max_profit is not None:
            lines.append(f"    Max profit: ${self.max_profit*100:,.0f}/contract")
        if self.max_loss is not None:
            lines.append(f"    Max loss:   ${self.max_loss*100:,.0f}/contract")
        lines.append(f"    Why: {self.rationale}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Payoff functions (per-share, at expiration)
# ---------------------------------------------------------------------------

def _payoff_call(S: float, K: float) -> float:
    return max(S - K, 0.0)

def _payoff_put(S: float, K: float) -> float:
    return max(K - S, 0.0)


# ---------------------------------------------------------------------------
# Strategy builders
# ---------------------------------------------------------------------------

def _bs_prices(forecast: ExpirationForecast) -> tuple[dict[float, float], dict[float, float]]:
    """Compute call/put prices at every grid strike via BS using the fitted IV."""
    T = max(forecast.dte, 1) / 365.0
    r = forecast.r
    q = forecast.q
    spot = forecast.spot
    # Re-evaluate smile via the grid + density strikes (we stored fitted IVs at the grid
    # only implicitly via the call prices). For pricing new strikes we use the closest grid point's
    # IV — good enough for strategy exploration.
    # Approximate: use atm_iv for everything; skew handled by the call prices themselves.
    sigma = forecast.atm_iv
    calls = {}
    puts = {}
    grid = forecast.density_strikes
    for K in grid:
        calls[float(K)] = _black_scholes_call(spot, float(K), T, r, sigma, q)
        puts[float(K)] = _black_scholes_put(spot, float(K), T, r, sigma, q)
    return calls, puts


def _nearest_strike(grid: np.ndarray, target: float) -> float:
    idx = int(np.argmin(np.abs(grid - target)))
    return float(grid[idx])


def _integrate_pop(forecast: ExpirationForecast, payoff_fn: Callable[[float], float]) -> float:
    """Integrate the indicator(payoff > 0) under the BL density."""
    grid = forecast.density_strikes
    density = forecast.density_values
    profit_mask = np.array([payoff_fn(float(S)) > 0 for S in grid])
    return float(trapezoid(np.where(profit_mask, density, 0.0), grid))


def _build_bull_call_spread(forecast, calls: dict) -> OptionsPlay | None:
    """Buy lower-strike call, sell higher-strike call. Bullish debit spread."""
    spot = forecast.spot
    K_long = _nearest_strike(forecast.density_strikes, spot)
    K_short = _nearest_strike(forecast.density_strikes, forecast.ci_50[1])
    if K_long >= K_short:
        return None
    p_long = calls.get(K_long) or calls.get(K_long - 0.5) or 0.0
    p_short = calls.get(K_short) or 0.0
    debit = p_long - p_short
    width = K_short - K_long
    max_profit = width - debit
    max_loss = debit
    be = K_long + debit

    def payoff(S):
        return max(min(S, K_short) - K_long, 0.0) - debit

    pop = _integrate_pop(forecast, payoff)
    return OptionsPlay(
        name="Bull Call Spread",
        bias="BULLISH",
        structure=f"Bullish debit spread, profit zone ${K_long:.0f}–${K_short:.0f}+",
        legs=[
            OptionLeg("BUY", "CALL", K_long, p_long),
            OptionLeg("SELL", "CALL", K_short, p_short),
        ],
        net_debit=debit,
        max_profit=max_profit,
        max_loss=max_loss,
        breakevens=[be],
        pop_risk_neutral=pop,
        reward_to_risk=max_profit / max_loss if max_loss > 0 else None,
        rationale=(
            f"Risk-neutral median ${forecast.median:,.0f} is above spot. "
            f"Caps cost via short call at upper-50% CI (${K_short:.0f}). "
            f"PoP only counts S_T above ${be:.0f} breakeven."
        ),
        payoff_fn=payoff,
    )


def _build_bull_put_spread(forecast, puts: dict) -> OptionsPlay | None:
    """Sell higher-strike put, buy lower-strike put. Bullish credit spread."""
    K_short = _nearest_strike(forecast.density_strikes, forecast.ci_80[0])
    K_long = _nearest_strike(forecast.density_strikes, forecast.ci_95[0])
    if K_long >= K_short:
        return None
    p_short = puts.get(K_short) or 0.0
    p_long = puts.get(K_long) or 0.0
    credit = p_short - p_long
    if credit <= 0:
        return None
    width = K_short - K_long
    max_profit = credit
    max_loss = width - credit
    be = K_short - credit

    def payoff(S):
        return credit - max(min(K_short, S) - max(K_long, S), 0.0) * 0 + (
            credit - (max(K_short - S, 0.0) - max(K_long - S, 0.0))
        )

    pop = _integrate_pop(forecast, payoff)
    return OptionsPlay(
        name="Bull Put Spread",
        bias="BULLISH",
        structure=f"Bullish credit spread, profit zone ≥ ${K_short:.0f}",
        legs=[
            OptionLeg("SELL", "PUT", K_short, p_short),
            OptionLeg("BUY", "PUT", K_long, p_long),
        ],
        net_debit=-credit,
        max_profit=max_profit,
        max_loss=max_loss,
        breakevens=[be],
        pop_risk_neutral=pop,
        reward_to_risk=max_profit / max_loss if max_loss > 0 else None,
        rationale=(
            f"Bullish lean + collects premium. Both legs below lower-80% CI (${K_short:.0f}), "
            f"giving margin of safety. Wins if S_T > ${be:.0f}."
        ),
        payoff_fn=payoff,
    )


def _build_bear_put_spread(forecast, puts: dict) -> OptionsPlay | None:
    """Buy higher-strike put, sell lower-strike put. Bearish debit spread."""
    K_long = _nearest_strike(forecast.density_strikes, forecast.spot)
    K_short = _nearest_strike(forecast.density_strikes, forecast.ci_50[0])
    if K_long <= K_short:
        return None
    p_long = puts.get(K_long) or 0.0
    p_short = puts.get(K_short) or 0.0
    debit = p_long - p_short
    if debit <= 0:
        return None
    width = K_long - K_short
    max_profit = width - debit
    max_loss = debit
    be = K_long - debit

    def payoff(S):
        return max(K_long - max(K_short, S), 0.0) - debit

    pop = _integrate_pop(forecast, payoff)
    return OptionsPlay(
        name="Bear Put Spread",
        bias="BEARISH",
        structure=f"Bearish debit spread, profit zone ≤ ${K_short:.0f}",
        legs=[
            OptionLeg("BUY", "PUT", K_long, p_long),
            OptionLeg("SELL", "PUT", K_short, p_short),
        ],
        net_debit=debit,
        max_profit=max_profit,
        max_loss=max_loss,
        breakevens=[be],
        pop_risk_neutral=pop,
        reward_to_risk=max_profit / max_loss if max_loss > 0 else None,
        rationale=(
            f"Risk-neutral median ${forecast.median:,.0f} is below spot. "
            f"Caps cost via short put at lower-50% CI (${K_short:.0f})."
        ),
        payoff_fn=payoff,
    )


def _build_bear_call_spread(forecast, calls: dict) -> OptionsPlay | None:
    """Sell lower-strike call, buy higher-strike call. Bearish credit spread."""
    K_short = _nearest_strike(forecast.density_strikes, forecast.ci_80[1])
    K_long = _nearest_strike(forecast.density_strikes, forecast.ci_95[1])
    if K_long <= K_short:
        return None
    p_short = calls.get(K_short) or 0.0
    p_long = calls.get(K_long) or 0.0
    credit = p_short - p_long
    if credit <= 0:
        return None
    width = K_long - K_short
    max_profit = credit
    max_loss = width - credit
    be = K_short + credit

    def payoff(S):
        return credit - max(max(S, K_short) - min(S, K_long), 0.0) * 0 + (
            credit - (max(S - K_short, 0.0) - max(S - K_long, 0.0))
        )

    pop = _integrate_pop(forecast, payoff)
    return OptionsPlay(
        name="Bear Call Spread",
        bias="BEARISH",
        structure=f"Bearish credit spread, profit zone ≤ ${K_short:.0f}",
        legs=[
            OptionLeg("SELL", "CALL", K_short, p_short),
            OptionLeg("BUY", "CALL", K_long, p_long),
        ],
        net_debit=-credit,
        max_profit=max_profit,
        max_loss=max_loss,
        breakevens=[be],
        pop_risk_neutral=pop,
        reward_to_risk=max_profit / max_loss if max_loss > 0 else None,
        rationale=(
            f"Bearish lean + collects premium. Both legs above upper-80% CI (${K_short:.0f}). "
            f"Wins if S_T < ${be:.0f}."
        ),
        payoff_fn=payoff,
    )


def _build_iron_condor(forecast, calls: dict, puts: dict) -> OptionsPlay | None:
    """Short OTM put + short OTM call, with protective long wings. Neutral credit."""
    p_short_put = _nearest_strike(forecast.density_strikes, forecast.ci_80[0])
    p_long_put = _nearest_strike(forecast.density_strikes, forecast.ci_95[0])
    c_short_call = _nearest_strike(forecast.density_strikes, forecast.ci_80[1])
    c_long_call = _nearest_strike(forecast.density_strikes, forecast.ci_95[1])
    if p_short_put <= p_long_put or c_short_call >= c_long_call:
        return None

    sell_put_p = puts.get(p_short_put) or 0.0
    buy_put_p = puts.get(p_long_put) or 0.0
    sell_call_p = calls.get(c_short_call) or 0.0
    buy_call_p = calls.get(c_long_call) or 0.0

    credit = (sell_put_p - buy_put_p) + (sell_call_p - buy_call_p)
    if credit <= 0:
        return None
    put_width = p_short_put - p_long_put
    call_width = c_long_call - c_short_call
    max_loss = max(put_width, call_width) - credit
    max_profit = credit
    be_low = p_short_put - credit
    be_high = c_short_call + credit

    def payoff(S):
        put_loss = max(p_short_put - S, 0.0) - max(p_long_put - S, 0.0)
        call_loss = max(S - c_short_call, 0.0) - max(S - c_long_call, 0.0)
        return credit - put_loss - call_loss

    pop = _integrate_pop(forecast, payoff)
    return OptionsPlay(
        name="Iron Condor",
        bias="NEUTRAL",
        structure=f"Neutral credit; profit zone ${be_low:.0f}–${be_high:.0f}",
        legs=[
            OptionLeg("SELL", "PUT", p_short_put, sell_put_p),
            OptionLeg("BUY", "PUT", p_long_put, buy_put_p),
            OptionLeg("SELL", "CALL", c_short_call, sell_call_p),
            OptionLeg("BUY", "CALL", c_long_call, buy_call_p),
        ],
        net_debit=-credit,
        max_profit=max_profit,
        max_loss=max_loss,
        breakevens=[be_low, be_high],
        pop_risk_neutral=pop,
        reward_to_risk=max_profit / max_loss if max_loss > 0 else None,
        rationale=(
            f"Wide CI ({(forecast.ci_80[1]-forecast.ci_80[0])/forecast.spot:.0%} of spot) "
            f"and high IV ({forecast.atm_iv:.0%}) → harvest premium with defined risk. "
            f"Wins if S_T stays in 80% CI band."
        ),
        payoff_fn=payoff,
    )


def _build_butterfly(forecast, calls: dict) -> OptionsPlay | None:
    """Long ATM call butterfly: 1 long lower, 2 short middle, 1 long upper. Neutral debit."""
    K_low = _nearest_strike(forecast.density_strikes, forecast.ci_50[0])
    K_mid = _nearest_strike(forecast.density_strikes, forecast.median)
    K_high = _nearest_strike(forecast.density_strikes, forecast.ci_50[1])
    if not (K_low < K_mid < K_high):
        return None
    # Body should be near middle of wings
    if abs((K_low + K_high) / 2 - K_mid) > (K_high - K_low) * 0.1:
        return None

    p_low = calls.get(K_low) or 0.0
    p_mid = calls.get(K_mid) or 0.0
    p_high = calls.get(K_high) or 0.0
    debit = p_low - 2 * p_mid + p_high
    if debit <= 0:
        return None
    width = K_mid - K_low
    max_profit = width - debit
    max_loss = debit
    be_low = K_low + debit
    be_high = K_high - debit

    def payoff(S):
        return (
            max(S - K_low, 0.0)
            - 2 * max(S - K_mid, 0.0)
            + max(S - K_high, 0.0)
            - debit
        )

    pop = _integrate_pop(forecast, payoff)
    return OptionsPlay(
        name="Long Call Butterfly",
        bias="NEUTRAL",
        structure=f"Pin risk around ${K_mid:.0f}; profit zone ${be_low:.0f}–${be_high:.0f}",
        legs=[
            OptionLeg("BUY", "CALL", K_low, p_low),
            OptionLeg("SELL", "CALL", K_mid, p_mid, qty=2),
            OptionLeg("BUY", "CALL", K_high, p_high),
        ],
        net_debit=debit,
        max_profit=max_profit,
        max_loss=max_loss,
        breakevens=[be_low, be_high],
        pop_risk_neutral=pop,
        reward_to_risk=max_profit / max_loss if max_loss > 0 else None,
        rationale=(
            f"Tight CI around median ${K_mid:.0f}; cheap pin trade if S_T lands near body. "
            f"Higher R/R than condor, narrower profit zone."
        ),
        payoff_fn=payoff,
    )


def _build_long_straddle(forecast, calls: dict, puts: dict) -> OptionsPlay | None:
    """Long ATM call + long ATM put. Direction-agnostic vol play."""
    K = _nearest_strike(forecast.density_strikes, forecast.spot)
    c = calls.get(K) or 0.0
    p = puts.get(K) or 0.0
    debit = c + p
    if debit <= 0:
        return None
    be_low = K - debit
    be_high = K + debit
    max_loss = debit
    # Max profit is unbounded — leave as None
    def payoff(S):
        return abs(S - K) - debit
    pop = _integrate_pop(forecast, payoff)
    return OptionsPlay(
        name="Long Straddle",
        bias="VOLATILE",
        structure=f"Volatility breakout; profit below ${be_low:.0f} or above ${be_high:.0f}",
        legs=[
            OptionLeg("BUY", "CALL", K, c),
            OptionLeg("BUY", "PUT", K, p),
        ],
        net_debit=debit,
        max_profit=None,
        max_loss=max_loss,
        breakevens=[be_low, be_high],
        pop_risk_neutral=pop,
        reward_to_risk=None,
        rationale=(
            f"Use when you expect a big move but not the direction. "
            f"Needs S_T to exceed ±${debit:.0f} ({debit/forecast.spot:.1%}) from spot to profit. "
            f"Best entered when IV is low."
        ),
        payoff_fn=payoff,
    )


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def recommend_plays(forecast: ExpirationForecast, top_n: int = 4) -> list[OptionsPlay]:
    """Generate ranked options plays based on the risk-neutral forecast."""
    calls, puts = _bs_prices(forecast)

    builders = [
        lambda: _build_bull_call_spread(forecast, calls),
        lambda: _build_bull_put_spread(forecast, puts),
        lambda: _build_bear_put_spread(forecast, puts),
        lambda: _build_bear_call_spread(forecast, calls),
        lambda: _build_iron_condor(forecast, calls, puts),
        lambda: _build_butterfly(forecast, calls),
        lambda: _build_long_straddle(forecast, calls, puts),
    ]
    plays: list[OptionsPlay] = []
    for build in builders:
        try:
            p = build()
            if p is not None:
                plays.append(p)
        except Exception as e:
            # Don't fail the whole recommender because one builder broke
            continue

    # Score: weight PoP and R/R equally; downrank expensive vol plays (straddle)
    def score(p: OptionsPlay) -> float:
        pop = p.pop_risk_neutral
        rr = p.reward_to_risk if p.reward_to_risk is not None else 0.5
        # Normalize R/R: 3.0+ is excellent, 1.0 is mediocre
        rr_norm = min(rr / 3.0, 1.0)
        return pop * 0.6 + rr_norm * 0.4

    plays.sort(key=score, reverse=True)
    return plays[:top_n]


def format_play_summary(plays: list[OptionsPlay]) -> str:
    if not plays:
        return "  (no suitable strategies — IV or CI bands may be too narrow)"
    return "\n\n".join(p.format() for p in plays)
