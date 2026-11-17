"""
Backtester / Calibration Framework for Options Predictions
==========================================================
NOTE ON DATA: The LSE vault returns options flow + chain snapshots but does NOT
provide historical OHLC for the underlying. To score a prediction against
realized close, you must supply the realized close yourself.

Two supported modes:

  Mode A — Backtest from flow history (recommended for institutional users)
    For each past expiry E in the LSE flow archive:
      1. Slice flow to a cutoff datetime T < expiry
      2. Run analyze_symbol() / forecast_expiration() on that slice
      3. Compare predicted direction to realized direction (close_T vs close_E)
      4. Score the BL CI by whether the realized close fell inside 50/80/95% bands
    Output: hit-rate, calibration table, log-loss

  Mode B — Forward-track predictions (paper trading)
    Each time you run analyze_symbol, append (timestamp, prediction, spot) to a
    JSONL log. After the expiry settles, score predictions from that log.

This module provides the framework. Pull realized closes from your own price
source (Bloomberg, yfinance, Polygon, your prime broker, etc.) via the
`realized_close(symbol, expiry)` callback.

Usage:
  from backtest import Backtester, RealizedCloseSource
  bt = Backtester(realized=lambda sym, exp: ...))
  results = bt.run_expiry('MU', '2026-07-27')
  print(results.summary())

  # Calibrate aggregator weights from a batch:
  weights = bt.calibrate_weights([('MU', '2026-07-27'), ('MU', '2026-07-18')])
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

import numpy as np

from lse_options import LSEClient, weighted_score, Signal
from expiration_model import forecast_expiration


PREDICTION_LOG = Path(__file__).parent / "prediction_log.jsonl"


@dataclass
class ExpiryBacktestResult:
    symbol: str
    expiry: str
    cutoff: str
    spot_at_cutoff: float
    realized_close: float
    realized_direction: int           # +1 if close > spot, -1 if <, 0 if ==

    predicted_direction: int
    predicted_confidence: float
    bl_median: float
    bl_ci_50: tuple[float, float]
    bl_ci_80: tuple[float, float]
    bl_ci_95: tuple[float, float]
    realized_in_ci_50: bool
    realized_in_ci_80: bool
    realized_in_ci_95: bool

    def summary(self) -> str:
        hit = "✓" if self.predicted_direction == self.realized_direction else "✗"
        return (
            f"{self.symbol} {self.expiry} | cutoff {self.cutoff} "
            f"spot={self.spot_at_cutoff:.2f} realized={self.realized_close:.2f} "
            f"({self.realized_direction:+d}) | pred={self.predicted_direction:+d} "
            f"({self.predicted_confidence:.0%}) {hit} | "
            f"CI50 {'in' if self.realized_in_ci_50 else 'OUT'} | "
            f"CI80 {'in' if self.realized_in_ci_80 else 'OUT'} | "
            f"CI95 {'in' if self.realized_in_ci_95 else 'OUT'}"
        )


class Backtester:
    """
    Replay-style backtester. Pulls historical flow for an expiry, slices to a
    cutoff, runs the predictor, and scores against the realized close.

    Args:
        realized: callable(symbol, expiry) -> float, returning the realized
                  closing price of `symbol` on `expiry`. YOU MUST SUPPLY THIS —
                  LSE does not provide underlying OHLC.
        client: optional LSEClient (created if not supplied)
        cutoff_days_before_expiry: how many days before expiry to evaluate
                  (1 = day before expiry, 0 = expiry day using morning flow)
    """

    def __init__(
        self,
        realized: Callable[[str, str], float],
        client: LSEClient | None = None,
        cutoff_days_before_expiry: int = 1,
    ):
        self.realized = realized
        self.client = client or LSEClient()
        self.cutoff_days_before_expiry = cutoff_days_before_expiry

    def _fetch_flow_window(self, symbol: str, cutoff_date: str) -> list[dict]:
        """Fetch flow from ~10 days before the cutoff up to the cutoff."""
        cutoff = datetime.strptime(cutoff_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        start = (cutoff - timedelta(days=10)).strftime("%Y-%m-%d")
        end = cutoff_date
        return self.client.options_flow(symbol, limit=5000, start=start, end=end)

    def run_expiry(self, symbol: str, expiry: str) -> ExpiryBacktestResult:
        """Run a single backtest for one (symbol, expiry) pair."""
        exp_date = datetime.strptime(expiry, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        cutoff = exp_date - timedelta(days=self.cutoff_days_before_expiry)
        cutoff_str = cutoff.strftime("%Y-%m-%d")

        flow = self._fetch_flow_window(symbol, cutoff_str)
        if not flow:
            raise RuntimeError(f"No flow data in window for {symbol} {expiry}")

        from lse_options import _latest_spot
        spot = _latest_spot(flow)

        realized_close = self.realized(symbol, expiry)
        realized_direction = (
            1 if realized_close > spot else -1 if realized_close < spot else 0
        )

        # Run prediction using only flow up to cutoff
        signals = []
        from lse_options import (
            flow_gex, premium_walls, pcr_signal, iv_skew_signal,
        )
        signals.append(flow_gex(flow, spot))
        signals.append(premium_walls(flow, spot))
        signals.append(pcr_signal(flow, history=None))  # no nested history fetch
        signals.append(iv_skew_signal(flow, spot))

        forecast = forecast_expiration(flow, spot, target_expiry=expiry)
        from lse_options import density_signal
        signals.append(density_signal(forecast))

        pred_dir, pred_conf, _ = weighted_score(signals)

        def in_ci(lo_hi, x):
            lo, hi = lo_hi
            return lo <= x <= hi

        return ExpiryBacktestResult(
            symbol=symbol,
            expiry=expiry,
            cutoff=cutoff_str,
            spot_at_cutoff=spot,
            realized_close=realized_close,
            realized_direction=realized_direction,
            predicted_direction=pred_dir,
            predicted_confidence=pred_conf,
            bl_median=forecast.median,
            bl_ci_50=forecast.ci_50,
            bl_ci_80=forecast.ci_80,
            bl_ci_95=forecast.ci_95,
            realized_in_ci_50=in_ci(forecast.ci_50, realized_close),
            realized_in_ci_80=in_ci(forecast.ci_80, realized_close),
            realized_in_ci_95=in_ci(forecast.ci_95, realized_close),
        )

    @staticmethod
    def aggregate(results: list[ExpiryBacktestResult]) -> dict:
        """Compute aggregate accuracy + calibration stats."""
        n = len(results)
        if n == 0:
            return {"n": 0}
        hits = sum(1 for r in results if r.predicted_direction == r.realized_direction)
        non_neutral = [r for r in results if r.predicted_direction != 0]
        hit_rate = hits / n
        # Calibration: fraction of realized closes inside each CI band
        calib_50 = sum(1 for r in results if r.realized_in_ci_50) / n
        calib_80 = sum(1 for r in results if r.realized_in_ci_80) / n
        calib_95 = sum(1 for r in results if r.realized_in_ci_95) / n
        # Confidence calibration: among high-confidence calls (>50%), how often right?
        hc = [r for r in non_neutral if r.predicted_confidence > 0.5]
        hc_acc = (
            sum(1 for r in hc if r.predicted_direction == r.realized_direction) / len(hc)
            if hc else float("nan")
        )
        return {
            "n": n,
            "direction_hit_rate": hit_rate,
            "non_neutral_count": len(non_neutral),
            "ci_50_coverage": calib_50,
            "ci_80_coverage": calib_80,
            "ci_95_coverage": calib_95,
            "ci_50_target": 0.50,
            "ci_80_target": 0.80,
            "ci_95_target": 0.95,
            "high_confidence_accuracy": hc_acc,
            "high_confidence_count": len(hc),
        }

    def calibrate_weights(self, pairs: list[tuple[str, str]]) -> dict:
        """
        Logistic-regression-style weight calibration. Uses signal features
        (direction × confidence per signal) to fit a logistic model predicting
        realized direction. Returns recommended weights per signal.

        This is a sketch — for production, use a proper ML pipeline with
        walk-forward cross-validation.
        """
        from sklearn.linear_model import LogisticRegression  # type: ignore

        rows = []
        labels = []
        for symbol, expiry in pairs:
            try:
                r = self.run_expiry(symbol, expiry)
            except Exception as e:
                print(f"  skip {symbol} {expiry}: {e}")
                continue
            # Feature vector: signed confidence per signal name
            feat = {f"feat_{s.name}": s.direction * s.confidence for s in self._last_signals(r)}
            rows.append(feat)
            labels.append(max(r.realized_direction, -1))  # clamp for logistic (multi-class not needed)

        if len(rows) < 10:
            print(f"Only {len(rows)} samples — need 10+ for calibration")
            return {}

        import pandas as pd
        X = pd.DataFrame(rows).fillna(0)
        y = np.array(labels)
        # Skip if all-same class
        if len(set(y)) < 2:
            print("All-same realized direction — can't calibrate")
            return {}

        clf = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X, y)
        # |coefficient| as relative weight per signal
        coefs = {k.replace("feat_", ""): float(abs(v)) for k, v in zip(X.columns, clf.coef_[0])}
        total = sum(coefs.values()) or 1.0
        return {k: v / total for k, v in coefs.items()}

    @staticmethod
    def _last_signals(result: ExpiryBacktestResult) -> list[Signal]:
        """Placeholder — in production, store signals with the result."""
        return []


# ---------------------------------------------------------------------------
# Prediction logging (Mode B — paper trading)
# ---------------------------------------------------------------------------

def log_prediction(pred, forecast=None, path: Path = PREDICTION_LOG) -> None:
    """Append a prediction to the JSONL log for forward-track scoring."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "symbol": pred.symbol,
        "spot": pred.spot,
        "direction": pred.direction,
        "confidence": pred.confidence,
        "signals": [
            {"name": s.name, "direction": s.direction, "confidence": s.confidence}
            for s in pred.signals
        ],
    }
    if forecast is not None:
        entry["forecast"] = {
            "expiry": forecast.expiry,
            "median": forecast.median,
            "ci_50": list(forecast.ci_50),
            "ci_80": list(forecast.ci_80),
            "ci_95": list(forecast.ci_95),
            "prob_above_spot": forecast.prob_above_spot,
        }
    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def score_logged_predictions(
    realized: Callable[[str, str], float],
    path: Path = PREDICTION_LOG,
) -> list[dict]:
    """
    Score every logged prediction whose expiry has now passed.
    Returns a list of score dicts.
    """
    if not path.exists():
        return []
    scores = []
    with open(path) as f:
        for line in f:
            entry = json.loads(line)
            fc = entry.get("forecast")
            if not fc:
                continue
            exp = fc["expiry"]
            try:
                exp_date = datetime.strptime(exp, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            except ValueError:
                continue
            if exp_date > datetime.now(timezone.utc):
                continue  # not yet settled
            try:
                rc = realized(entry["symbol"], exp)
            except Exception:
                continue
            inside = {
                "ci_50": fc["ci_50"][0] <= rc <= fc["ci_50"][1],
                "ci_80": fc["ci_80"][0] <= rc <= fc["ci_80"][1],
                "ci_95": fc["ci_95"][0] <= rc <= fc["ci_95"][1],
            }
            realized_dir = 1 if rc > entry["spot"] else -1 if rc < entry["spot"] else 0
            hit = entry["direction"] == realized_dir
            scores.append({
                "ts": entry["ts"],
                "symbol": entry["symbol"],
                "expiry": exp,
                "spot": entry["spot"],
                "realized": rc,
                "predicted_direction": entry["direction"],
                "predicted_confidence": entry["confidence"],
                "realized_direction": realized_dir,
                "direction_hit": hit,
                **inside,
            })
    return scores


# ---------------------------------------------------------------------------
# CLI: print aggregate stats for logged predictions
# ---------------------------------------------------------------------------

def _main():
    import argparse
    parser = argparse.ArgumentParser(description="Backtest / score predictions")
    parser.add_argument("--score-log", action="store_true",
                        help="Score all logged predictions (requires realized close source)")
    args = parser.parse_args()

    if args.score_log:
        # REPLACE with your realized-close callback
        def realized(symbol, expiry):
            raise NotImplementedError("Supply a realized-close callback")

        scores = score_logged_predictions(realized)
        if not scores:
            print("No scored predictions yet.")
            return
        n = len(scores)
        hit_rate = sum(s["direction_hit"] for s in scores) / n
        calib_50 = sum(s["ci_50"] for s in scores) / n
        calib_80 = sum(s["ci_80"] for s in scores) / n
        calib_95 = sum(s["ci_95"] for s in scores) / n
        print(f"n={n}  direction hit-rate={hit_rate:.1%}")
        print(f"CI calibration: 50%→{calib_50:.1%} (target 50%), "
              f"80%→{calib_80:.1%} (target 80%), 95%→{calib_95:.1%} (target 95%)")


if __name__ == "__main__":
    _main()
