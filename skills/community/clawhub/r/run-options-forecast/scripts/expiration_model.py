"""
Expiration Risk-Neutral Density Model (refactored)
==================================================
Predicts the **risk-neutral** distribution of a stock's close at option
expiration via Breeden-Litzenberger density extraction from the IV smile.

IMPORTANT — "risk-neutral" vs "real-world":
  The Breeden-Litzenberger formula f(K) = e^(rT)·∂²C/∂K² yields the
  **risk-neutral** density Q, not the real-world (physical) density P.
  The two differ by the market price of risk and the variance risk premium
  (VRP). Options systematically price in heavier downside tails than
  historically realize. Treat outputs as market-implied, not as calibrated
  real-world probabilities. See `vrp_proxy` field for a coarse adjustment.

Methodology:
  1. Extract volume-weighted IV smile for the nearest expiry from flow data
  2. Fit a PCHIP (monotone cubic Hermite) spline in log-forward-moneyness;
     monotonicity-preserving fit avoids the spurious oscillations that a
     quadratic polynomial produces in the wings.
  3. Compute BS call prices on a dense strike grid spanning ±3σ
  4. Apply Breeden-Litzenberger: f(K) = e^((r−q)T) · ∂²C/∂K²
  5. Enforce no-arb: density ≥ 0, mean(density) ≈ forward F = S·e^((r−q)T)
  6. Normalize to a probability density, integrate to a CDF
  7. Invert CDF for 50%/80%/95% confidence intervals

Also reports:
  - 1σ expected move from ATM IV (for comparison with the density median)
  - Premium-weighted strike (heaviest flow, NOT a directional predictor)
  - 25Δ risk-reversal skew
  - VRP proxy: ATM_IV² − recent_realized_var (when historical flow available)
  - Risk-neutral direction: P(close > spot) mapped to a signed score
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

import numpy as np
from scipy.integrate import trapezoid
from scipy.interpolate import PchipInterpolator
from scipy.stats import norm

# Term-matched short rate proxy.
# As of mid-2026, ~5.0% (3-month T-bill / SOFR) is closer than 4.5%.
# Override via env var RISK_FREE_RATE for term-matching.
import os
RISK_FREE_RATE = float(os.environ.get("RISK_FREE_RATE", "0.050"))

# Continuous dividend yield. Pass in per-symbol for dividend-paying stocks.
# MU recently yielded ~0.3-0.5% annually; default 0 for safety.
DIVIDEND_YIELD_DEFAULT = 0.0


@dataclass
class ExpirationForecast:
    """Risk-neutral density forecast for close at nearest expiration."""
    expiry: str
    dte: int
    spot: float
    atm_iv: float
    expected_move_1sigma: float
    median: float           # risk-neutral median
    mean: float             # risk-neutral mean (should ≈ forward if no-arb holds)
    forward_price: float    # F = S · e^((r−q)T)
    ci_50: tuple[float, float]
    ci_80: tuple[float, float]
    ci_95: tuple[float, float]
    prob_above_spot: float  # risk-neutral P(close > spot)
    rn_direction: int       # +1/0/−1 derived from prob_above_spot
    skew: float
    density_strikes: np.ndarray
    density_values: np.ndarray
    premium_magnet: float | None
    r: float                # risk-free rate used
    q: float                # dividend yield used
    arb_check: dict         # no-arbitrage diagnostics
    vrp_proxy: float | None = None
    interpretation: str = ""

    def summary(self) -> str:
        lines = [
            f"Expiration: {self.expiry} ({self.dte}d)",
            f"Spot: ${self.spot:,.2f}   Forward: ${self.forward_price:,.2f}  (r={self.r:.2%}, q={self.q:.2%})",
            f"ATM IV: {self.atm_iv:.1%}",
            f"Expected move (1σ, lognormal): ±${self.expected_move_1sigma:,.2f} ({self.expected_move_1sigma/self.spot:.1%})",
            f"",
            f"Risk-Neutral Density Forecast (market-implied, NOT real-world):",
            f"  Median close: ${self.median:,.2f}",
            f"  Mean close:   ${self.mean:,.2f}  (forward = ${self.forward_price:,.2f}; "
            f"gap {self.mean - self.forward_price:+.2f})",
            f"  Q(close > spot) = {self.prob_above_spot:.1%}   direction → {['NEUTRAL','BULLISH','BEARISH'][self.rn_direction]}",
            f"",
            f"Confidence Intervals (risk-neutral quantiles):",
            f"  50% CI: ${self.ci_50[0]:,.2f} – ${self.ci_50[1]:,.2f}",
            f"  80% CI: ${self.ci_80[0]:,.2f} – ${self.ci_80[1]:,.2f}",
            f"  95% CI: ${self.ci_95[0]:,.2f} – ${self.ci_95[1]:,.2f}",
        ]
        if self.premium_magnet:
            lines.append(f"  Heaviest flow strike: ${self.premium_magnet:,.2f}  (descriptor, not a predictor)")
        if self.vrp_proxy is not None:
            lines.append(f"  VRP proxy (IV² − recent realized var): {self.vrp_proxy:+.4f}")
        lines.append(f"\nSkew (25Δ RR): {self.skew:+.4f}")
        arb = self.arb_check
        lines.append(
            f"No-arb check: density≥0={arb.get('density_nonneg')}, "
            f"mean/forward ratio={arb.get('mean_to_forward', float('nan')):.3f}, "
            f"status={arb.get('status')}"
        )
        if self.interpretation:
            lines.append(f"\n{self.interpretation}")
        return "\n".join(lines)


def _black_scholes_call(S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0) -> float:
    """Black-Scholes-Merton call option price with continuous dividend yield q."""
    if T <= 0 or sigma <= 0:
        return max(S * math.exp(-q * T) - K, 0.0)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)


def _black_scholes_put(S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0) -> float:
    """Black-Scholes-Merton put option price with continuous dividend yield q."""
    if T <= 0 or sigma <= 0:
        return max(K - S * math.exp(-q * T), 0.0)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return K * math.exp(-r * T) * norm.cdf(-d2) - S * math.exp(-q * T) * norm.cdf(-d1)


def _extract_iv_smile(flow: list[dict], spot: float, target_expiry: str) -> dict:
    """
    Extract volume-weighted IV per strike for a given expiry.
    Filters to near-money (spot × 0.50 – spot × 1.50) for density stability.
    Falls back to wider window if too few strikes survive.
    """
    lo, hi = spot * 0.50, spot * 1.50

    expiry_flow = [
        p for p in flow
        if p.get("expiry") == target_expiry
        and p.get("iv") is not None and 0.0 < float(p["iv"]) < 5.0
        and lo <= float(p["strike"]) <= hi
    ]

    if len(expiry_flow) < 5:
        expiry_flow = [
            p for p in flow
            if p.get("expiry") == target_expiry
            and p.get("iv") is not None and 0.0 < float(p["iv"]) < 5.0
        ]

    if not expiry_flow:
        return {}

    by_strike: dict[float, list] = {}
    for p in expiry_flow:
        s = round(float(p["strike"]), 2)
        by_strike.setdefault(s, []).append(p)

    smile = {}
    for strike, prints in by_strike.items():
        total_vol = sum(int(p.get("volume", 1)) for p in prints) or 1
        weighted_iv = sum(float(p["iv"]) * int(p.get("volume", 1)) for p in prints) / total_vol

        deltas = [float(p["delta"]) for p in prints if p.get("delta") is not None]
        avg_delta = sum(deltas) / len(deltas) if deltas else None

        is_call = prints[0]["contract_type"] == "call"
        is_otm = (is_call and strike > spot) or (not is_call and strike < spot)

        smile[strike] = {
            "iv": weighted_iv,
            "delta": avg_delta,
            "type": "call" if is_call else "put",
            "otm": is_otm,
            "volume": total_vol,
        }

    otm_smile = {k: v for k, v in smile.items() if v["otm"]}
    return otm_smile if len(otm_smile) >= 5 else smile


def _fit_pchip_smile(
    smile: dict, spot: float, T: float, r: float, q: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, "PchipInterpolator", float]:
    """
    Fit IV as a PCHIP (monotone cubic Hermite) interpolator in log-forward-moneyness.

    PCHIP preserves monotonicity in regions where the data is monotone and does
    not introduce spurious oscillations — important for stable BL second-derivatives.

    Returns: (strikes_raw, ivs_raw, fitted_ivs_on_grid, grid, pchip, forward)
    """
    strikes_raw = np.array(sorted(smile.keys()))
    ivs_raw = np.array([smile[s]["iv"] for s in strikes_raw])

    F = spot * math.exp((r - q) * T)
    moneyness = np.log(strikes_raw / F)

    # Sort by moneyness (required by PCHIP)
    order = np.argsort(moneyness)
    m_sorted = moneyness[order]
    iv_sorted = ivs_raw[order]

    # De-duplicate moneyness values (PCHIP requires unique x)
    m_unique, unique_idx = np.unique(m_sorted, return_index=True)
    iv_unique = iv_sorted[unique_idx]

    if len(m_unique) < 4:
        raise ValueError(
            f"Insufficient unique moneyness points ({len(m_unique)}) for PCHIP smile fit"
        )

    pchip = PchipInterpolator(m_unique, iv_unique, extrapolate=True)

    # Grid spanning ±3σ around spot for tail coverage
    sigma = float(ivs_raw[len(ivs_raw) // 2]) * math.sqrt(T)  # rough ATM vol
    grid_lo = max(spot * (1 - 3 * sigma), strikes_raw.min() * 0.9)
    grid_hi = min(spot * (1 + 3 * sigma), strikes_raw.max() * 1.1)
    step = max(spot * 0.002, 1.0)
    grid = np.arange(grid_lo, grid_hi, step)

    grid_moneyness = np.log(grid / F)
    fitted_ivs = pchip(grid_moneyness)
    fitted_ivs = np.clip(fitted_ivs, 0.03, 5.0)

    return strikes_raw, ivs_raw, fitted_ivs, grid, pchip, F


def _nearest_expiry(flow: list[dict]) -> tuple[str, int]:
    """Find nearest non-expired expiration in the flow data."""
    from collections import Counter
    expiry_counts = Counter(p.get("expiry") for p in flow if p.get("expiry"))
    if not expiry_counts:
        raise ValueError("No expiry data in flow")

    today = datetime.now(timezone.utc)
    future_expiries = []
    for exp_str in expiry_counts:
        try:
            exp_date = datetime.strptime(exp_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            dte = (exp_date - today).days
            if dte >= 0:
                future_expiries.append((exp_str, dte, expiry_counts[exp_str]))
        except ValueError:
            continue

    if not future_expiries:
        all_expiries = []
        for exp_str in expiry_counts:
            try:
                exp_date = datetime.strptime(exp_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                dte = (exp_date - today).days
                all_expiries.append((exp_str, dte, expiry_counts[exp_str]))
            except ValueError:
                continue
        if not all_expiries:
            raise ValueError("No parseable expiry dates")
        all_expiries.sort(key=lambda x: abs(x[1]))
        chosen = all_expiries[0]
    else:
        future_expiries.sort(key=lambda x: x[1])
        chosen = future_expiries[0]

    return chosen[0], max(chosen[1], 0)


def _no_arb_check(density: np.ndarray, strikes: np.ndarray, forward: float, r: float, T: float) -> dict:
    """
    Verify the extracted density is internally arbitrage-free.
      1. density ≥ 0 everywhere
      2. ∫ K · f(K) dK = forward · e^(-rT) (martingale condition for call prices)
         Equivalently, mean of density in forward units ≈ 1.
    """
    nonneg = bool((density >= 0).all())
    mean_K = float(trapezoid(strikes * density, strikes))
    # Risk-neutral mean of S_T should equal forward F = S·e^((r−q)T)
    # But our density is on strikes K, which IS S_T.
    # So mean(K) should equal forward F.
    ratio = mean_K / forward if forward > 0 else float("nan")
    status = "OK" if (nonneg and 0.97 <= ratio <= 1.03) else "FAIL"
    return {
        "density_nonneg": nonneg,
        "mean_to_forward": float(ratio),
        "mean": mean_K,
        "forward": forward,
        "status": status,
    }


def forecast_expiration(
    flow: list[dict],
    spot: float,
    target_expiry: str | None = None,
    *,
    r: float | None = None,
    q: float | None = None,
    realized_variance: float | None = None,
) -> ExpirationForecast:
    """
    Compute risk-neutral density and confidence intervals from options flow.

    Args:
        flow: list of option print dicts from LSE
        spot: current underlying price
        target_expiry: specific expiry "YYYY-MM-DD". If None, picks nearest.
        r: risk-free rate override (default: RISK_FREE_RATE)
        q: continuous dividend yield override (default: DIVIDEND_YIELD_DEFAULT)
        realized_variance: optional historical realized variance for VRP diagnostic
    """
    if target_expiry:
        today = datetime.now(timezone.utc)
        try:
            exp_date = datetime.strptime(target_expiry, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            dte = max((exp_date - today).days, 0)
        except ValueError:
            raise ValueError(f"Invalid expiry format: {target_expiry}")
        expiry = target_expiry
    else:
        expiry, dte = _nearest_expiry(flow)

    smile_data = _extract_iv_smile(flow, spot, expiry)
    if len(smile_data) < 5:
        raise ValueError(
            f"Insufficient IV data for {expiry}: only {len(smile_data)} strikes. "
            f"Need at least 5 for density extraction."
        )

    T = max(dte, 1) / 365.0
    r_used = RISK_FREE_RATE if r is None else r
    q_used = DIVIDEND_YIELD_DEFAULT if q is None else q

    strikes_raw, ivs_raw, iv_grid, grid, pchip, F_forward = _fit_pchip_smile(smile_data, spot, T, r_used, q_used)

    # ATM IV: use the smile value at spot (interpolated), not the noisiest raw print.
    atm_idx = int(np.argmin(np.abs(strikes_raw - spot)))
    atm_iv_raw = float(ivs_raw[atm_idx])
    # Re-read fitted value at the strike closest to spot for a smoother ATM IV
    atm_grid_idx = int(np.argmin(np.abs(grid - spot)))
    atm_iv = float(iv_grid[atm_grid_idx])

    expected_move_1sigma = spot * atm_iv * math.sqrt(T)
    forward_price = spot * math.exp((r_used - q_used) * T)

    # Compute BS call prices on the dense grid using fitted IVs
    call_prices = np.array([
        _black_scholes_call(spot, k, T, r_used, sigma, q_used)
        for k, sigma in zip(grid, iv_grid)
    ])

    # Single light smoothing pass — do NOT double-smooth.
    # sigma=1-2 is enough to suppress grid-scale noise without flattening features.
    from scipy.ndimage import gaussian_filter1d
    smooth_sigma = 1.5
    call_smooth = gaussian_filter1d(call_prices, sigma=smooth_sigma)

    # Second derivative via central differences at grid spacing.
    # We use a 3-point stencil scaled by `stencil` for stability, but
    # since we've already lightly smoothed, stencil=1 is appropriate.
    dk = grid[1] - grid[0]
    second_deriv = np.zeros_like(call_smooth)
    second_deriv[1:-1] = (
        call_smooth[:-2] - 2 * call_smooth[1:-1] + call_smooth[2:]
    ) / (dk ** 2)
    # Edges: replicate nearest interior value
    second_deriv[0] = second_deriv[1]
    second_deriv[-1] = second_deriv[-2]

    # Breeden-Litzenberger: f(K) = e^((r−q)T) · ∂²C/∂K²
    density = np.maximum(second_deriv * math.exp((r_used - q_used) * T), 0)

    # Drop negligible density (numerical noise) — keep tail coverage
    mask = density > density.max() * 1e-5
    density[~mask] = 0

    total = trapezoid(density, grid)
    if total > 0:
        density = density / total

    cdf = np.cumsum(density) * dk
    if cdf[-1] > 0:
        cdf = np.clip(cdf / cdf[-1], 0, 1)

    def invert_cdf(probability: float) -> float:
        idx = int(np.searchsorted(cdf, probability))
        idx = min(idx, len(grid) - 1)
        return float(grid[idx])

    median = invert_cdf(0.50)
    ci_50 = (invert_cdf(0.25), invert_cdf(0.75))
    ci_80 = (invert_cdf(0.10), invert_cdf(0.90))
    ci_95 = (invert_cdf(0.025), invert_cdf(0.975))

    mean = float(trapezoid(grid * density, grid))

    spot_idx = min(int(np.searchsorted(grid, spot)), len(cdf) - 1)
    prob_above_spot = 1.0 - float(cdf[spot_idx])

    # Risk-neutral direction from density
    if prob_above_spot >= 0.55:
        rn_direction = 1
    elif prob_above_spot <= 0.45:
        rn_direction = -1
    else:
        rn_direction = 0

    # Skew: interpolate IV at exactly 25-delta call and put using the fitted smile.
    def bs_delta_call(K: float, sigma: float) -> float:
        if T <= 0 or sigma <= 0:
            return 1.0 if K < spot else 0.0
        d1 = (math.log(spot / K) + (r_used - q_used + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        return math.exp(-q_used * T) * norm.cdf(d1)

    def iv_at_strike(K: float) -> float:
        m = math.log(K / F_forward)
        return float(np.clip(pchip(m), 0.03, 5.0))

    def strike_for_call_delta(target_delta: float, side: str) -> tuple[float, float]:
        # side='call' → look for OTM call (K > spot), delta in (0, 0.5)
        # side='put'  → look for OTM put (K < spot), put delta in (-0.5, 0)
        best_K, best_err, best_iv = spot, 1.0, atm_iv
        for K in grid:
            sigma_K = iv_at_strike(float(K))
            d_call = bs_delta_call(float(K), sigma_K)
            d_eff = d_call - math.exp(-q_used * T) if side == "put" else d_call
            err = abs(d_eff - target_delta)
            if err < best_err:
                best_K, best_err, best_iv = float(K), err, sigma_K
        return best_K, best_iv

    K_call25, iv_call_25 = strike_for_call_delta(0.25, "call")
    K_put25, iv_put_25 = strike_for_call_delta(-0.25, "put")
    skew = iv_call_25 - iv_put_25

    # Heaviest flow strike (descriptor only)
    premium_by_strike: dict[float, float] = {}
    for p in flow:
        if p.get("expiry") != expiry:
            continue
        s = round(float(p["strike"]), 2)
        premium_by_strike[s] = premium_by_strike.get(s, 0) + float(p.get("premium", 0))
    premium_magnet = max(premium_by_strike, key=premium_by_strike.get) if premium_by_strike else None

    # VRP proxy (variance risk premium): IV² − realized var
    vrp_proxy = (atm_iv ** 2 - realized_variance) if realized_variance is not None else None

    arb_check = _no_arb_check(density, grid, forward_price, r_used, T)

    median_vs_spot = (median - spot) / spot
    skew_direction = "left-skewed (downside risk)" if skew < -0.03 else \
                     "right-skewed (upside potential)" if skew > 0.03 else \
                     "roughly symmetric"
    lean = "below" if median < spot else "above" if median > spot else "at"

    interpretation = (
        f"Risk-neutral distribution is {skew_direction}. "
        f"Risk-neutral median ${median:,.0f} is {abs(median_vs_spot):.1%} {lean} spot. "
        f"Q(close above spot) = {prob_above_spot:.0%}. "
        f"NOTE: this is the market-implied (risk-neutral) distribution, not a "
        f"calibrated real-world forecast."
    )
    if premium_magnet:
        magnet_dist = (premium_magnet - spot) / spot
        interpretation += (
            f" Heaviest flow strike ${premium_magnet:,.0f} "
            f"({magnet_dist:+.1%} vs spot) — descriptor of where flow concentrated, "
            f"not a directional predictor."
        )
    if abs(skew) > 0.05:
        interpretation += (
            f" 25Δ RR of {skew:+.3f} → "
            f"{'elevated put demand (bearish hedging)' if skew < 0 else 'elevated call demand'}."
        )
    if vrp_proxy is not None and vrp_proxy > 0:
        interpretation += (
            f" Positive VRP proxy ({vrp_proxy:.4f}) → options price in more variance "
            f"than has realized; risk-neutral tails are likely overstated vs physical."
        )

    return ExpirationForecast(
        expiry=expiry,
        dte=dte,
        spot=spot,
        atm_iv=atm_iv,
        expected_move_1sigma=expected_move_1sigma,
        median=median,
        mean=mean,
        forward_price=forward_price,
        ci_50=ci_50,
        ci_80=ci_80,
        ci_95=ci_95,
        prob_above_spot=prob_above_spot,
        rn_direction=rn_direction,
        skew=skew,
        density_strikes=grid,
        density_values=density,
        premium_magnet=premium_magnet,
        r=r_used,
        q=q_used,
        arb_check=arb_check,
        vrp_proxy=vrp_proxy,
        interpretation=interpretation,
    )
