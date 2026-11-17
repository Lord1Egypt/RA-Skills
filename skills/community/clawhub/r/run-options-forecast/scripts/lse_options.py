"""
LSE Options Flow Analysis Engine (refactored)
==============================================
Directional signal engine using LSE options data.

Signals computed:
  1. chain_gex       — gamma exposure from chain snapshot (volume_today × gamma)
                       replaces flow-only GEX; more comprehensive coverage of strikes
  2. premium_walls   — net premium by strike from flow (descriptor of positioning)
  3. pcr             — put/call ratio with z-scoring against ~30-day history
                       (absolute thresholds are unreliable across regimes)
  4. iv_skew         — 25-delta risk reversal with interpolated IV(Δ=±0.25)
  5. density_signal  — optional anchor from Breeden-Litzenberger risk-neutral
                       density P(close > spot). When present, this is the most
                       theoretically-grounded directional read.

Aggregator: weighted_score() — weighted log-odds style fusion with disagreement
penalty. Renamed from bayesian_aggregate (kept as alias for compatibility) since
the original implementation is not a true Bayesian update.
"""
from __future__ import annotations

import os
import ssl
import json
import urllib.request
import urllib.parse
import urllib.error
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

import numpy as np
from dotenv import load_dotenv
from scipy import stats

try:
    import certifi
    _DEFAULT_CA = certifi.where()
except ImportError:  # pragma: no cover — fall back to system CA bundle
    _DEFAULT_CA = None

load_dotenv()


# ---------------------------------------------------------------------------
# 1. LSE CLIENT
# ---------------------------------------------------------------------------

class LSEError(Exception):
    """Raised on LSE API errors. `status` is HTTP code; 0 = transport error."""

    def __init__(self, status: int, message: str):
        super().__init__(f"[{status}] {message}")
        self.status = status
        self.message = message


class LSEClient:
    """Minimal LSE vault client — flow + chain endpoints."""

    BASE = "https://api.londonstrategicedge.com/vault"
    HEADERS = {
        "User-Agent": "lse-options-engine (+https://londonstrategicedge.com)",
    }

    def __init__(self, api_key: str | None = None):
        key = api_key or os.environ.get("LONDON_STRATEGIC_EDGE_API_KEY")
        if not key:
            raise LSEError(0, "LONDON_STRATEGIC_EDGE_API_KEY not set")
        self._key = key
        self._headers = {**self.HEADERS, "x-api-key": key}
        # Use certifi's CA bundle to avoid the macOS Python "unable to get
        # local issuer certificate" failure.
        self._ssl_context = (
            ssl.create_default_context(cafile=_DEFAULT_CA)
            if _DEFAULT_CA else ssl.create_default_context()
        )

    def _call(self, path: str, params: dict[str, Any] | None = None) -> Any:
        url = f"{self.BASE}/{path}"
        if params:
            url += "?" + urllib.parse.urlencode(
                {k: v for k, v in params.items() if v is not None}
            )
        req = urllib.request.Request(url, headers=self._headers)
        try:
            with urllib.request.urlopen(req, timeout=30, context=self._ssl_context) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:500]
            try:
                detail = json.loads(body)
                msg = detail.get("detail") or detail.get("message") or body
            except json.JSONDecodeError:
                msg = body
            raise LSEError(e.code, msg) from None
        except urllib.error.URLError as e:
            raise LSEError(0, str(e)) from e

    # --- endpoints ---

    def usage(self) -> dict:
        return self._call("usage")

    def options_flow(
        self,
        underlying: str,
        limit: int = 5000,
        min_premium: int | None = None,
        start: str | None = None,
        end: str | None = None,
    ) -> list[dict]:
        """Return individual option prints with Greeks + premium."""
        return self._call(
            "options/flow",
            {
                "underlying": underlying,
                "limit": limit,
                "min_premium": min_premium,
                "start": start,
                "end": end,
            },
        )

    def options_chain(
        self,
        underlying: str,
        strike_min: float | None = None,
        strike_max: float | None = None,
        expiry: str | None = None,
        limit: int = 5000,
    ) -> list[dict]:
        """Chain snapshot. NOTE: EOD, may be stale intraday. No OI field — only
        volume_today and premium_today."""
        return self._call(
            "options/chain",
            {
                "underlying": underlying,
                "strike_min": strike_min,
                "strike_max": strike_max,
                "expiry": expiry,
                "limit": limit,
            },
        )


# ---------------------------------------------------------------------------
# 2. SIGNAL DATA STRUCTURES
# ---------------------------------------------------------------------------

@dataclass
class Signal:
    """Single signal output with direction, confidence, and raw metrics."""
    name: str
    direction: int          # +1 bullish, -1 bearish, 0 neutral
    confidence: float       # 0.0–1.0
    magnitude: float        # signal strength (signal-specific units)
    raw: dict = field(default_factory=dict)
    interpretation: str = ""

    def as_view(self) -> dict:
        return {
            "analyst": self.name,
            "direction": self.direction,
            "magnitude": self.magnitude,
            "confidence": self.confidence,
        }


@dataclass
class CompositePrediction:
    """Final fused prediction."""
    symbol: str
    spot: float
    direction: int
    confidence: float
    disagreement: float
    signals: list[Signal]
    timestamp: str

    def label(self) -> str:
        dirs = {1: "BULLISH", -1: "BEARISH", 0: "NEUTRAL"}
        return f"{dirs[self.direction]} ({self.confidence:.0%})"


# ---------------------------------------------------------------------------
# 3. SIGNAL CALCULATORS
# ---------------------------------------------------------------------------

def _filter_valid_prints(flow: list[dict]) -> list[dict]:
    """Keep only prints with populated Greeks."""
    return [p for p in flow if p.get("gamma") is not None and p.get("iv") is not None]


def _latest_spot(flow: list[dict]) -> float:
    """Extract current spot from most recent print."""
    valid = [p for p in flow if p.get("underlying_price")]
    if not valid:
        raise ValueError("No underlying_price in flow data")
    return float(valid[0]["underlying_price"])


# --- Signal 1: Chain-based GEX (replaces flow-only GEX) ---

def chain_gex(chain: list[dict], spot: float) -> Signal:
    """
    Gamma exposure from the chain snapshot (volume_today × gamma).
    More comprehensive than flow prints alone: chain covers ALL listed strikes
    even those with no flow today. NOTE: LSE chain does not expose open interest,
    so volume_today is the best OI-proxy available.

    Sign convention: dealers SHORT calls (long gamma) → positive; SHORT puts
    (short gamma) → negative. This is the standard SqueezeMetrics-style
    convention. For real OI-based GEX, integrate with an OI provider (CBOE /
    OCC) — see backtester note.

    Directional read: call-wall/put-wall asymmetry. If put wall closer to spot
    than call wall → downside supported → bullish lean.
    """
    valid = [p for p in chain
             if p.get("gamma") is not None
             and p.get("volume_today") is not None
             and float(p.get("volume_today", 0)) > 0]
    if not valid:
        return Signal("chain_gex", 0, 0.0, 0.0, {}, "No valid chain rows with Greeks")

    by_strike: dict[float, dict] = {}
    for p in valid:
        s = round(float(p["strike"]), 2)
        gamma = float(p["gamma"])
        vol = int(p.get("volume_today", 0))
        sign = 1 if p["contract_type"] == "call" else -1
        gex = gamma * vol * 100 * (spot ** 2) * 0.01 * sign
        d = by_strike.setdefault(s, {"call_gex": 0.0, "put_gex": 0.0, "total_gex": 0.0})
        if sign > 0:
            d["call_gex"] += gex
        else:
            d["put_gex"] += gex
        d["total_gex"] += gex

    total_call_gex = sum(d["call_gex"] for d in by_strike.values())
    total_put_gex = sum(d["put_gex"] for d in by_strike.values())
    net_gex = total_call_gex + total_put_gex

    # Walls
    call_items = [(k, v["call_gex"]) for k, v in by_strike.items() if v["call_gex"] > 0]
    put_items = [(k, v["put_gex"]) for k, v in by_strike.items() if v["put_gex"] < 0]
    call_wall_strike = max(call_items, key=lambda kv: kv[1])[0] if call_items else spot
    put_wall_strike = min(put_items, key=lambda kv: kv[1])[0] if put_items else spot

    dist_call = abs(call_wall_strike - spot) / spot
    dist_put = abs(put_wall_strike - spot) / spot

    if dist_put < dist_call:
        direction = 1
        magnitude = (dist_call - dist_put) / max(dist_call, 1e-9)
    elif dist_call < dist_put:
        direction = -1
        magnitude = (dist_put - dist_call) / max(dist_put, 1e-9)
    else:
        direction = 0
        magnitude = 0.0

    confidence = min(magnitude * 3.0, 0.6)

    regime = "positive (vol suppressed)" if net_gex > 0 else "negative (vol amplified)"
    interp = (
        f"Net GEX ${net_gex/1e6:+.1f}M — {regime} (chain volume_today, OI-proxy). "
        f"Call wall @{call_wall_strike} ({dist_call:.1%} above spot), "
        f"Put wall @{put_wall_strike} ({dist_put:.1%} below spot). "
        f"{'Put wall closer → downside supported' if direction > 0 else 'Call wall closer → upside capped' if direction < 0 else 'Balanced walls'}."
    )

    return Signal(
        name="chain_gex",
        direction=direction,
        confidence=confidence,
        magnitude=magnitude,
        raw={
            "by_strike": by_strike,
            "net_gex": net_gex,
            "call_wall": call_wall_strike,
            "put_wall": put_wall_strike,
            "total_call_gex": total_call_gex,
            "total_put_gex": total_put_gex,
            "source": "chain.volume_today",
        },
        interpretation=interp,
    )


def flow_gex(flow: list[dict], spot: float) -> Signal:
    """
    Legacy flow-based GEX. Kept for back-compat with streaming aggregator.
    Prefer chain_gex when chain snapshot is available.
    """
    valid = _filter_valid_prints(flow)
    if not valid:
        return Signal("flow_gex", 0, 0.0, 0.0, {}, "No valid prints")

    by_strike: dict[float, dict] = {}
    for p in valid:
        s = round(float(p["strike"]), 2)
        gamma = float(p["gamma"])
        vol = int(p.get("volume", 0))
        sign = 1 if p["contract_type"] == "call" else -1
        gex = gamma * vol * 100 * (spot ** 2) * 0.01 * sign
        d = by_strike.setdefault(s, {"call_gex": 0.0, "put_gex": 0.0, "total_gex": 0.0})
        if sign > 0:
            d["call_gex"] += gex
        else:
            d["put_gex"] += gex
        d["total_gex"] += gex

    total_call_gex = sum(d["call_gex"] for d in by_strike.values())
    total_put_gex = sum(d["put_gex"] for d in by_strike.values())
    net_gex = total_call_gex + total_put_gex

    call_items = [(k, v["call_gex"]) for k, v in by_strike.items() if v["call_gex"] > 0]
    put_items = [(k, v["put_gex"]) for k, v in by_strike.items() if v["put_gex"] < 0]
    call_wall_strike = max(call_items, key=lambda kv: kv[1])[0] if call_items else spot
    put_wall_strike = min(put_items, key=lambda kv: kv[1])[0] if put_items else spot

    dist_call = abs(call_wall_strike - spot) / spot
    dist_put = abs(put_wall_strike - spot) / spot

    if dist_put < dist_call:
        direction = 1
        magnitude = (dist_call - dist_put) / max(dist_call, 1e-9)
    elif dist_call < dist_put:
        direction = -1
        magnitude = (dist_put - dist_call) / max(dist_put, 1e-9)
    else:
        direction = 0
        magnitude = 0.0

    confidence = min(magnitude * 3.0, 0.6)
    regime = "positive (vol suppressed)" if net_gex > 0 else "negative (vol amplified)"
    interp = (
        f"Net GEX ${net_gex/1e6:+.1f}M — {regime} (flow-based; chain_gex preferred). "
        f"Call wall @{call_wall_strike} ({dist_call:.1%} above spot), "
        f"Put wall @{put_wall_strike} ({dist_put:.1%} below spot)."
    )

    return Signal(
        name="flow_gex",
        direction=direction,
        confidence=confidence,
        magnitude=magnitude,
        raw={
            "by_strike": by_strike,
            "net_gex": net_gex,
            "call_wall": call_wall_strike,
            "put_wall": put_wall_strike,
            "total_call_gex": total_call_gex,
            "total_put_gex": total_put_gex,
        },
        interpretation=interp,
    )


# --- Signal 2: Premium Walls (descriptive, not predictive) ---

def premium_walls(flow: list[dict], spot: float) -> Signal:
    """
    Net premium by strike from today's flow.

    CAUTION: 'premium at strike K' is a *descriptor* of where institutional flow
    concentrated, NOT a magnet for price. The max-pain magnet dynamic depends
    on dealer hedging of OPEN INTEREST, not intraday flow premium. Treat the
    direction output here as a soft positioning indicator, not a directional
    predictor.
    """
    by_strike: dict[float, dict] = {}
    for p in flow:
        s = round(float(p["strike"]), 2)
        prem = float(p.get("premium", 0))
        d = by_strike.setdefault(s, {"call_prem": 0.0, "put_prem": 0.0})
        if p["contract_type"] == "call":
            d["call_prem"] += prem
        else:
            d["put_prem"] += prem

    if not by_strike:
        return Signal("premium_walls", 0, 0.0, 0.0, {}, "No flow data")

    total_call = sum(d["call_prem"] for d in by_strike.values())
    total_put = sum(d["put_prem"] for d in by_strike.values())
    total = total_call + total_put

    if total == 0:
        return Signal("premium_walls", 0, 0.0, 0.0, {}, "Zero premium")

    call_weighted = sum(s * d["call_prem"] for s, d in by_strike.items()) / max(total_call, 1)
    put_weighted = sum(s * d["put_prem"] for s, d in by_strike.items()) / max(total_put, 1)

    all_prem = [(s, d["call_prem"] + d["put_prem"]) for s, d in by_strike.items()]
    magnet_strike = max(all_prem, key=lambda x: x[1])[0]

    dist = (magnet_strike - spot) / spot
    if abs(dist) < 0.005:
        direction = 0
    else:
        direction = 1 if dist > 0 else -1

    # Reduced confidence cap (was 0.55 → 0.35) since this is descriptive only.
    confidence = min(abs(dist) * 8, 0.35)

    call_share = total_call / total
    interp = (
        f"Total premium ${total/1e6:.1f}M — "
        f"{call_share:.0%} calls / {1-call_share:.0%} puts. "
        f"Heaviest-flow strike @ {magnet_strike} ({dist:+.1%} vs spot) — "
        f"descriptor, not a directional magnet."
    )

    return Signal(
        name="premium_walls",
        direction=direction,
        confidence=confidence,
        magnitude=abs(dist),
        raw={
            "by_strike": by_strike,
            "magnet_strike": magnet_strike,
            "call_weighted": call_weighted,
            "put_weighted": put_weighted,
            "total_call": total_call,
            "total_put": total_put,
        },
        interpretation=interp,
    )


# --- Signal 3: PCR with historical z-scoring ---

def _pcr_from_flow(flow: list[dict]) -> tuple[float, float]:
    """Returns (pcr_vol, pcr_prem) for a single flow slice."""
    call_vol = sum(int(p.get("volume", 0)) for p in flow if p["contract_type"] == "call")
    put_vol = sum(int(p.get("volume", 0)) for p in flow if p["contract_type"] == "put")
    call_prem = sum(float(p.get("premium", 0)) for p in flow if p["contract_type"] == "call")
    put_prem = sum(float(p.get("premium", 0)) for p in flow if p["contract_type"] == "put")
    pcr_vol = put_vol / max(call_vol, 1)
    pcr_prem = put_prem / max(call_prem, 1)
    return pcr_vol, pcr_prem


def pcr_history(client: LSEClient, underlying: str, days: int = 30) -> list[dict]:
    """
    Fetch per-day PCR over the last `days` days for z-scoring.
    Skips days with no data. Returns list of {date, pcr_vol, pcr_prem, pcr_combined}.
    """
    today = datetime.now(timezone.utc).date()
    history = []
    for d_offset in range(1, days + 1):
        day = today - timedelta(days=d_offset)
        next_day = day + timedelta(days=1)
        try:
            flow = client.options_flow(
                underlying, limit=3000,
                start=day.strftime("%Y-%m-%d"),
                end=next_day.strftime("%Y-%m-%d"),
            )
        except LSEError:
            continue
        if not flow:
            continue
        pcr_vol, pcr_prem = _pcr_from_flow(flow)
        history.append({
            "date": day.strftime("%Y-%m-%d"),
            "pcr_vol": pcr_vol,
            "pcr_prem": pcr_prem,
            "pcr_combined": (pcr_vol + pcr_prem) / 2,
        })
    return history


def pcr_signal(flow: list[dict], history: list[dict] | None = None) -> Signal:
    """
    Put/Call ratio with optional z-scoring against `history`.

    Without history: uses absolute thresholds (PCR > 1.2 = extreme fear, etc.)
    With history: z-scores today's combined PCR against the historical distribution.
    """
    pcr_vol, pcr_prem = _pcr_from_flow(flow)
    pcr_combined = (pcr_vol + pcr_prem) / 2

    call_vol = sum(int(p.get("volume", 0)) for p in flow if p["contract_type"] == "call")
    put_vol = sum(int(p.get("volume", 0)) for p in flow if p["contract_type"] == "put")
    call_prem = sum(float(p.get("premium", 0)) for p in flow if p["contract_type"] == "call")
    put_prem = sum(float(p.get("premium", 0)) for p in flow if p["contract_type"] == "put")

    if history and len(history) >= 5:
        ref = np.array([h["pcr_combined"] for h in history])
        mu = float(np.mean(ref))
        sd = float(np.std(ref)) or 1e-9
        z = (pcr_combined - mu) / sd

        # Z-score interpretation: high z (>>0) = extreme fear vs symbol's own norm
        if z > 1.5:
            direction = 1
            magnitude = abs(z)
            confidence = min(abs(z) / 3.0, 0.65)
            label = f"PCR z={z:+.2f} vs {len(history)}d mean — extreme fear → contrarian BULLISH"
        elif z < -1.5:
            direction = -1
            magnitude = abs(z)
            confidence = min(abs(z) / 3.0, 0.65)
            label = f"PCR z={z:+.2f} vs {len(history)}d mean — extreme greed → contrarian BEARISH"
        else:
            direction = 0
            magnitude = 0.0
            confidence = 0.15
            label = f"PCR z={z:+.2f} — within normal range vs {len(history)}d history"

        interp = (
            f"PCR(vol)={pcr_vol:.3f}, PCR(prem)={pcr_prem:.3f}, combined={pcr_combined:.3f}. "
            f"History μ={mu:.3f} σ={sd:.3f} (n={len(history)}). → {label}."
        )
    else:
        # Absolute threshold fallback
        if pcr_combined > 1.2:
            direction = 1
            magnitude = pcr_combined - 1.0
            confidence = min(magnitude * 1.5, 0.65)
            label = "extreme fear → contrarian BULLISH (absolute threshold; no history)"
        elif pcr_combined < 0.5:
            direction = -1
            magnitude = 1.0 - pcr_combined
            confidence = min(magnitude * 1.5, 0.65)
            label = "extreme greed → contrarian BEARISH (absolute threshold; no history)"
        else:
            direction = 0
            magnitude = 0.0
            confidence = 0.15
            label = "neutral range (absolute threshold; no history)"

        interp = (
            f"PCR(vol)={pcr_vol:.3f}, PCR(prem)={pcr_prem:.3f}, combined={pcr_combined:.3f}. "
            f"Call vol={call_vol:,}, Put vol={put_vol:,}. "
            f"Call ${call_prem/1e6:.1f}M, Put ${put_prem/1e6:.1f}M. → {label}."
        )

    return Signal(
        name="pcr",
        direction=direction,
        confidence=confidence,
        magnitude=magnitude,
        raw={
            "pcr_vol": pcr_vol,
            "pcr_prem": pcr_prem,
            "pcr_combined": pcr_combined,
            "call_vol": call_vol,
            "put_vol": put_vol,
            "call_prem": call_prem,
            "put_prem": put_prem,
            "history_n": len(history) if history else 0,
        },
        interpretation=interp,
    )


# --- Signal 4: IV Skew (25-Delta Risk Reversal, interpolated) ---

def iv_skew_signal(flow: list[dict], spot: float) -> Signal:
    """
    25-delta risk reversal = IV(25Δ call) − IV(25Δ put).

    Implementation: bin flow prints by strike, compute volume-weighted IV and
    average |delta| per strike, then linearly interpolate IV as a function of
    |delta| to read off IV at exactly 0.25. This is more accurate than the
    original "nearest print" approach when deltas are sparsely sampled.
    """
    valid = _filter_valid_prints(flow)
    if not valid:
        return Signal("iv_skew", 0, 0.0, 0.0, {}, "Insufficient data for skew")

    by_strike: dict[float, dict] = {}
    for p in valid:
        if p.get("delta") is None:
            continue
        s = round(float(p["strike"]), 2)
        d = by_strike.setdefault(s, {"iv_sum": 0.0, "vol": 0, "delta_sum": 0.0,
                                     "type": p["contract_type"]})
        v = int(p.get("volume", 1)) or 1
        d["iv_sum"] += float(p["iv"]) * v
        d["vol"] += v
        d["delta_sum"] += abs(float(p["delta"])) * v

    if len(by_strike) < 4:
        return Signal("iv_skew", 0, 0.0, 0.0, {}, "Insufficient strikes for skew")

    # Build separate |delta| → IV curves for calls and puts
    calls, puts = [], []
    for s, d in by_strike.items():
        if d["vol"] == 0:
            continue
        avg_iv = d["iv_sum"] / d["vol"]
        avg_abs_delta = d["delta_sum"] / d["vol"]
        point = (avg_abs_delta, avg_iv, s)
        if d["type"] == "call":
            calls.append(point)
        else:
            puts.append(point)

    def interp_at(curve, target_delta):
        if not curve:
            return None, None
        curve = sorted(curve, key=lambda x: x[0])
        ds = [c[0] for c in curve]
        ivs = [c[1] for c in curve]
        ks = [c[2] for c in curve]
        # Need at least 2 points spanning target_delta
        if len(curve) < 2:
            return ivs[0], ks[0]
        if target_delta < min(ds) or target_delta > max(ds):
            # Out of sample — use nearest endpoint
            idx = 0 if target_delta < min(ds) else -1
            return ivs[idx], ks[idx]
        iv_at = float(np.interp(target_delta, ds, ivs))
        k_at = float(np.interp(target_delta, ds, ks))
        return iv_at, k_at

    iv_call_25d, call_strike = interp_at(calls, 0.25)
    iv_put_25d, put_strike = interp_at(puts, 0.25)

    if iv_call_25d is None or iv_put_25d is None:
        return Signal("iv_skew", 0, 0.0, 0.0, {}, "Could not interpolate 25Δ IV")

    rr_25d = iv_call_25d - iv_put_25d

    if rr_25d > 0.02:
        direction = 1
        label = "call IV premium → bullish positioning"
    elif rr_25d < -0.05:
        direction = -1
        label = f"put IV premium → bearish positioning (RR={rr_25d:+.3f})"
    else:
        direction = 0
        label = f"balanced skew (RR={rr_25d:+.3f})"

    confidence = min(abs(rr_25d) * 5, 0.55)

    interp = (
        f"25Δ Risk Reversal = {rr_25d:+.4f} "
        f"(call IV={iv_call_25d:.3f} @ Δ=0.25 K={call_strike:.0f}, "
        f"put IV={iv_put_25d:.3f} @ |Δ|=0.25 K={put_strike:.0f}; interpolated). "
        f"→ {label}."
    )

    return Signal(
        name="iv_skew",
        direction=direction,
        confidence=confidence,
        magnitude=abs(rr_25d),
        raw={
            "rr_25d": rr_25d,
            "iv_call_25d": iv_call_25d,
            "iv_put_25d": iv_put_25d,
            "call_strike": call_strike,
            "put_strike": put_strike,
            "method": "linear_interp_on_delta",
        },
        interpretation=interp,
    )


# --- Signal 5: Density-driven direction (anchor signal) ---

def density_signal(forecast) -> Signal:
    """
    Convert the Breeden-Litzenberger risk-neutral forecast into a directional
    signal. This is the most theoretically-grounded signal available.

    NOTE: This is risk-neutral, not real-world. The variance risk premium
    systematically makes Q heavier-tailed to the left than P. Treat as a market
    sentiment read, not a calibrated probability.
    """
    p_above = forecast.prob_above_spot
    if p_above >= 0.55:
        direction = 1
    elif p_above <= 0.45:
        direction = -1
    else:
        direction = 0
    # Distance from 0.5 sets confidence
    confidence = min(abs(p_above - 0.5) * 2.0, 0.7)
    interp = (
        f"Risk-neutral Q(close > spot) = {p_above:.1%}. "
        f"Risk-neutral median ${forecast.median:,.2f} vs spot ${forecast.spot:,.2f}. "
        f"Arbitrage check: {forecast.arb_check.get('status', 'n/a')} "
        f"(mean/forward={forecast.arb_check.get('mean_to_forward', float('nan')):.3f})."
    )
    return Signal(
        name="density",
        direction=direction,
        confidence=confidence,
        magnitude=abs(p_above - 0.5) * 2,
        raw={
            "prob_above_spot": p_above,
            "median": forecast.median,
            "mean": forecast.mean,
            "forward": forecast.forward_price,
            "arb_status": forecast.arb_check.get("status"),
            "skew": forecast.skew,
        },
        interpretation=interp,
    )


# ---------------------------------------------------------------------------
# 4. AGGREGATOR (weighted score, with disagreement penalty)
# ---------------------------------------------------------------------------

# Default weights. The density signal gets the highest weight when available,
# since it is the most theoretically-grounded (BL density from the full smile).
DEFAULT_SIGNAL_WEIGHTS = {
    "chain_gex": 0.20,
    "flow_gex": 0.15,       # used when chain not available
    "premium_walls": 0.10,  # descriptive only — low weight
    "pcr": 0.20,
    "iv_skew": 0.20,
    "density": 0.30,        # anchor — risk-neutral density
}

# Legacy weights (preserved for back-compat with old callers)
LEGACY_SIGNAL_WEIGHTS = {
    "flow_gex": 0.30,
    "premium_walls": 0.25,
    "pcr": 0.25,
    "iv_skew": 0.20,
}

SIGNAL_WEIGHTS = DEFAULT_SIGNAL_WEIGHTS


def weighted_score(
    signals: list[Signal],
    weights: dict[str, float] | None = None,
) -> tuple[int, float, float]:
    """
    Combine signals via weighted log-odds with disagreement penalty.

    NOTE: This is NOT a Bayesian update — it is a weighted average of signed
    directions, scaled by confidence, with a variance-based disagreement
    penalty. For calibrated probabilities, fit a logistic regression against
    realized outcomes (see backtester.py).

    Returns: (direction, confidence, disagreement)
    """
    weights = weights or SIGNAL_WEIGHTS
    views = [s.as_view() for s in signals]
    if not views:
        return 0, 0.0, 0.0

    eff = [(v, weights.get(v["analyst"], 0.2) * v["confidence"]) for v in views]
    total_w = sum(w for _, w in eff)
    if total_w < 1e-9:
        return 0, 0.0, 0.0

    score = sum(v["direction"] * w for v, w in eff) / total_w

    signs = [v["direction"] * w for v, w in eff]
    disagreement = float(np.var(signs)) if len(signs) > 1 else 0.0

    confidence = abs(score) * max(0.0, 1.0 - 2.0 * disagreement)
    confidence = min(confidence, 0.95)

    direction = int(np.sign(score)) if abs(score) > 0.08 else 0
    return direction, confidence, disagreement


# Backwards-compatible alias. Old name implied Bayesian but the math was always
# weighted-score; new code should call weighted_score.
bayesian_aggregate = weighted_score


# ---------------------------------------------------------------------------
# 5. ORCHESTRATOR
# ---------------------------------------------------------------------------

def analyze_symbol(
    symbol: str,
    flow_limit: int = 5000,
    *,
    use_chain: bool = True,
    use_history: bool = True,
    history_days: int = 30,
    use_density: bool = True,
) -> CompositePrediction:
    """
    Run full options analysis on a symbol.

    Args:
        symbol: ticker (e.g. "MU")
        flow_limit: max flow prints to fetch
        use_chain: if True, fetch chain snapshot for chain_gex (vs flow-only)
        use_history: if True, fetch ~30 days of historical PCR for z-scoring
        history_days: number of past days to sample for PCR history
        use_density: if True, compute BL density and include as anchor signal
    """
    client = LSEClient()
    flow = client.options_flow(symbol, limit=flow_limit)

    if not flow:
        raise LSEError(0, f"No flow data for {symbol}")

    spot = _latest_spot(flow)

    signals: list[Signal] = []

    # 1. GEX — prefer chain when available
    chain_data: list[dict] = []
    if use_chain:
        try:
            chain_data = client.options_chain(symbol, limit=5000)
        except LSEError:
            pass
    if chain_data:
        signals.append(chain_gex(chain_data, spot))
    else:
        signals.append(flow_gex(flow, spot))

    # 2. Premium walls (descriptive)
    signals.append(premium_walls(flow, spot))

    # 3. PCR with optional history
    history = None
    if use_history:
        try:
            history = pcr_history(client, symbol, days=history_days)
        except LSEError:
            history = None
    signals.append(pcr_signal(flow, history))

    # 4. IV skew (interpolated)
    signals.append(iv_skew_signal(flow, spot))

    # 5. Density anchor (optional)
    if use_density:
        try:
            from expiration_model import forecast_expiration
            forecast = forecast_expiration(flow, spot)
            signals.append(density_signal(forecast))
        except Exception as e:
            # Don't fail the whole pipeline just because density is unavailable
            signals.append(Signal(
                name="density",
                direction=0,
                confidence=0.0,
                magnitude=0.0,
                raw={"error": str(e)},
                interpretation=f"Density forecast unavailable: {e}",
            ))

    direction, confidence, disagreement = weighted_score(signals)

    latest_ts = max(p.get("ts", "") for p in flow)

    return CompositePrediction(
        symbol=symbol,
        spot=spot,
        direction=direction,
        confidence=confidence,
        disagreement=disagreement,
        signals=signals,
        timestamp=latest_ts,
    )


def format_report(pred: CompositePrediction) -> str:
    """Human-readable prediction report."""
    dirs = {1: "BULLISH", -1: "BEARISH", 0: "NEUTRAL"}
    lines = [
        "=" * 72,
        f"OPTIONS ANALYSIS — {pred.symbol}",
        f"Spot: ${pred.spot:,.2f}  |  Data as of: {pred.timestamp}",
        "=" * 72,
        "",
        f"COMPOSITE PREDICTION: {dirs[pred.direction]}  (confidence: {pred.confidence:.0%}, disagreement: {pred.disagreement:.3f})",
        "",
        "SIGNAL BREAKDOWN:",
    ]
    for s in pred.signals:
        lines.append(f"\n  [{s.name.upper()}]  direction={s.direction:+d}  confidence={s.confidence:.0%}")
        lines.append(f"    {s.interpretation}")
    lines.extend(["", "=" * 72])
    return "\n".join(lines)
