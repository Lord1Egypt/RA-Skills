#!/usr/bin/env python3
"""Compute the window statistics the snapshot contract refuses to accept as judgement.

`liquidity`, `factor_r2`, `beta_strength` and `beta_stability` cannot be declared `judged`: a
model that has not run the computation does not have the number. That rule is only honest if
there is a legal way to satisfy it, which is what this module is. It reads a local table of daily
bars and returns the four metrics plus the `measurement` declarations that describe how they were
produced.

It is deliberately small. It does not fetch anything, it does not know about providers, and it
takes no view on what the numbers mean — that stays with the snapshot the agent writes.
"""

from __future__ import annotations

import csv
import hashlib
import math
from bisect import bisect_left, bisect_right
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

MIN_OBSERVATIONS = 30
# Beta is scaled so that twice the factor's move reads as a full score. The cap matters more than
# the constant: past 2.0 a satellite is not more informative about the factor, only more levered.
BETA_FULL_SCALE = 2.0
REQUIRED_COLUMNS = ("date", "ticker", "close")


class MeasureError(ValueError):
    pass


def read_bars(
    path: str | Path, *, as_of: str | None = None, after: str | None = None
) -> dict[str, list[tuple[str, float, float | None]]]:
    """Read `date,ticker,close[,volume][,turnover]` into per-ticker series sorted by date."""
    series: dict[str, list[tuple[str, float, float | None]]] = defaultdict(list)
    seen: set[tuple[str, str]] = set()
    for bound in (as_of, after):
        if bound is not None:
            try:
                if date.fromisoformat(bound).isoformat() != bound:
                    raise ValueError("noncanonical date")
            except ValueError as exc:
                raise MeasureError(f"invalid date boundary {bound!r}") from exc
    try:
        with Path(path).open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            missing = [name for name in REQUIRED_COLUMNS if name not in (reader.fieldnames or [])]
            if missing:
                raise MeasureError(f"{path}: price table needs columns {', '.join(missing)}")
            for line, row in enumerate(reader, start=2):
                ticker = str(row["ticker"]).strip().upper()
                if not ticker:
                    continue
                day = str(row["date"]).strip()
                try:
                    if date.fromisoformat(day).isoformat() != day:
                        raise ValueError("noncanonical date")
                except ValueError as exc:
                    raise MeasureError(f"{path}:{line}: date must be ISO YYYY-MM-DD") from exc
                if (as_of and day > as_of) or (after and day <= after):
                    continue
                if (ticker, day) in seen:
                    raise MeasureError(f"{path}:{line}: duplicate ticker/date {ticker} {day}")
                seen.add((ticker, day))
                try:
                    close = float(row["close"])
                except (TypeError, ValueError) as exc:
                    raise MeasureError(f"{path}:{line}: close is not a number") from exc
                if not math.isfinite(close) or close <= 0:
                    raise MeasureError(f"{path}:{line}: close must be finite and positive")
                try:
                    turnover = _optional_float(row.get("turnover"))
                    volume = _optional_float(row.get("volume"))
                except MeasureError as exc:
                    raise MeasureError(f"{path}:{line}: {exc}") from exc
                if turnover is None:
                    turnover = None if volume is None else close * volume
                if turnover is not None and (not math.isfinite(turnover) or turnover < 0):
                    raise MeasureError(f"{path}:{line}: turnover must be finite and nonnegative")
                series[ticker].append((day, close, turnover))
    except OSError as exc:
        raise MeasureError(f"cannot read price table {path}: {exc}") from exc
    if not series:
        raise MeasureError(f"{path}: no rows")
    for rows in series.values():
        rows.sort(key=lambda row: row[0])
    return dict(series)


def _optional_float(value: Any) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise MeasureError("nonblank turnover/volume must be numeric") from exc


def returns(rows: list[tuple[str, float, float | None]]) -> dict[str, float]:
    """Simple daily returns keyed by date. Non-positive closes break the series rather than
    producing a number that looks like a return."""
    out: dict[str, float] = {}
    for (_, previous, _), (day, close, _) in zip(rows, rows[1:], strict=False):
        if previous > 0 and close > 0:
            out[day] = close / previous - 1.0
    return out


def factor_returns(
    series: dict[str, list[tuple[str, float, float | None]]], benchmarks: list[str]
) -> dict[str, float]:
    """Equal-weighted mean return of the benchmark legs, over dates every leg quotes."""
    legs = []
    for ticker in benchmarks:
        rows = series.get(ticker.strip().upper())
        if not rows:
            raise MeasureError(f"benchmark {ticker} is absent from the price table")
        legs.append(returns(rows))
    shared = set(legs[0])
    for leg in legs[1:]:
        shared &= set(leg)
    return {day: sum(leg[day] for leg in legs) / len(legs) for day in shared}


def ols(y: list[float], x: list[float]) -> tuple[float, float] | None:
    """Return (beta, r_squared) of y on x, or None when x does not vary."""
    count = len(x)
    if count < 2:
        return None
    mean_x = sum(x) / count
    mean_y = sum(y) / count
    sxx = sum((value - mean_x) ** 2 for value in x)
    if sxx <= 0:
        return None
    sxy = sum((a - mean_x) * (b - mean_y) for a, b in zip(x, y, strict=True))
    syy = sum((value - mean_y) ** 2 for value in y)
    beta = sxy / sxx
    r2 = 0.0 if syy <= 0 else min(1.0, max(0.0, (sxy * sxy) / (sxx * syy)))
    return beta, r2


def _score(value: float) -> int:
    return int(round(min(100.0, max(0.0, value))))


def beta_scores(
    own: dict[str, float], factor: dict[str, float], window: int
) -> tuple[int | None, int | None]:
    """Strength is scaled positive beta; stability compares the two half-window estimates.

    Stability asks whether the relationship held, not whether it was strong. A satellite whose
    beta halves between the first and second half of the window is not a stable read on the
    factor even if both estimates are large.
    """
    days = sorted(set(own) & set(factor))[-window:]
    if len(days) < MIN_OBSERVATIONS:
        return None, None
    fit = ols([own[day] for day in days], [factor[day] for day in days])
    if fit is None:
        return None, None
    strength = _score(fit[0] / BETA_FULL_SCALE * 100)
    half = len(days) // 2
    halves = []
    for chunk in (days[:half], days[half:]):
        if len(chunk) < MIN_OBSERVATIONS // 2:
            return strength, None
        piece = ols([own[day] for day in chunk], [factor[day] for day in chunk])
        if piece is None:
            return strength, None
        halves.append(piece[0])
    spread = abs(halves[0] - halves[1])
    scale = abs(halves[0]) + abs(halves[1])
    stability = 0 if scale <= 0 else _score((1 - spread / scale) * 100)
    return strength, stability


def liquidity_scores(
    series: dict[str, list[tuple[str, float, float | None]]], window: int
) -> tuple[dict[str, int], list[str]]:
    """Cross-sectional percentile of mean daily turnover.

    A percentile, not a level: the number has to be comparable inside one market and meaningless
    across markets, which is what the score is used for. A ticker with no turnover column gets no
    score rather than a low one.
    """
    averages: dict[str, float] = {}
    notes: list[str] = []
    for ticker, rows in series.items():
        window_rows = rows[-window:]
        values = [turnover for _, _, turnover in window_rows if turnover is not None]
        if len(values) < min(MIN_OBSERVATIONS, window):
            notes.append(f"{ticker}: no liquidity score, {len(values)} sessions carry turnover")
            continue
        averages[ticker] = sum(values) / len(values)
    if not averages:
        return {}, notes
    ordered = sorted(averages.values())
    total = len(ordered)
    scores: dict[str, int] = {}
    for ticker, value in averages.items():
        below = bisect_left(ordered, value)
        ties = bisect_right(ordered, value) - below
        if total == 1:
            scores[ticker] = 100
            continue
        scores[ticker] = _score(100.0 * (below + (ties - 1) / 2) / (total - 1))
    return scores, notes


def measure(
    *,
    prices: str | Path,
    benchmarks: list[str],
    source: str,
    window: int = 180,
    liquidity_window: int = 30,
    as_of: str | None = None,
    benchmark_map: dict | None = None,
    factor_model: str = "basket",
) -> dict[str, Any]:
    from theme_metrics import fund_comparisons, multi_fit, resolve_gauges

    if not source.startswith(("http://", "https://")):
        raise MeasureError("source must be the http(s) URL the price table came from")
    if not benchmarks and not benchmark_map:
        raise MeasureError("at least one benchmark leg or a benchmark map is required")
    if window < MIN_OBSERVATIONS or liquidity_window < 1:
        raise MeasureError(f"window must be at least {MIN_OBSERVATIONS} sessions")
    if factor_model not in ("basket", "multivariate"):
        raise MeasureError("factor_model must be basket or multivariate")
    if benchmark_map and factor_model != "basket":
        raise MeasureError("theme maps already declare their factor model; use basket")
    series = read_bars(prices, as_of=as_of)
    fallback = factor_returns(series, benchmarks) if benchmarks else {}
    gauges, theme_checks = resolve_gauges(series, benchmark_map) if benchmark_map else ({}, {})
    liquidity, notes = liquidity_scores(series, liquidity_window)
    latest = max(day for rows in series.values() for day, _, _ in rows)
    digest = hashlib.sha256(Path(prices).read_bytes()).hexdigest()
    metrics, records = {}, {}
    for ticker, rows in sorted(series.items()):
        own = returns(rows)
        gauge = gauges.get(ticker)
        # An unfit or absent theme gauge never falls back to a broad index.
        factor = (gauge or {}).get("returns", {}) if benchmark_map else fallback
        legs = (gauge or {}).get("legs", []) if benchmark_map else benchmarks
        days = sorted(set(own) & set(factor))[-window:]
        fit = (
            ols([own[d] for d in days], [factor[d] for d in days])
            if (len(days) >= MIN_OBSERVATIONS)
            else None
        )
        r2 = None if fit is None else fit[1]
        model = (gauge or {}).get("mode", factor_model)
        if factor_model == "multivariate" and not benchmark_map and days:
            fit_many = multi_fit(
                [own[d] for d in days], [[returns(series[t])[d] for d in days] for t in benchmarks]
            )
            r2 = None if fit_many is None else fit_many[1]
        if fit is None or r2 is None:
            notes.append(
                f"{ticker}: no factor statistics, {len(days)} sessions overlap a usable gauge"
            )
        strength, stability = beta_scores(own, factor, window)
        entry = {
            "liquidity": liquidity.get(ticker),
            "factor_r2": None if r2 is None else _score(r2 * 100),
            "beta_strength": strength if r2 is not None else None,
            "beta_stability": stability if r2 is not None else None,
        }
        metrics[ticker] = {key: value for key, value in entry.items() if value is not None}
        records[ticker] = {
            "as_of": as_of or latest,
            "source": source,
            "data_sha256": digest,
            "first_session": rows[0][0],
            "last_session": rows[-1][0],
            "observations": len(days),
            "liquidity_observations": sum(r[2] is not None for r in rows[-liquidity_window:]),
            "benchmarks": legs,
            "factor_model": model,
            "theme": (gauge or {}).get("theme"),
            "gauge_fit": (gauge or {}).get("fit"),
        }
    label = (
        "per-ticker theme gauge (measurement_record)" if benchmark_map else " + ".join(benchmarks)
    )
    declared = declarations(label, source, window, liquidity_window, len(liquidity))
    if factor_model == "multivariate":
        declared["factor_r2"]["method"] = "multivariate OLS with intercept on " + label
    return {
        "schema_version": 1,
        "as_of": as_of or latest,
        "benchmark": benchmarks,
        "measurement": declared,
        "metrics": metrics,
        "records": records,
        "coverage": {
            "price_tickers": len(series),
            "liquidity_tickers": len(liquidity),
            "factor_tickers": sum("factor_r2" in row for row in metrics.values()),
            "data_sha256": digest,
        },
        "theme_checks": theme_checks,
        "fund_comparisons": fund_comparisons(series, benchmark_map) if benchmark_map else [],
        "notes": sorted(set(notes)),
    }


def declarations(
    label: str, source: str, window: int, liquidity_window: int, population: int
) -> dict[str, dict[str, Any]]:
    span = f"{window}d"
    return {
        # `population` is what the percentile was taken against. Without it a rank is not
        # comparable to the same rank in another universe of the same market.
        "liquidity": {
            "basis": "measured",
            "method": (
                f"cross-sectional percentile of mean daily turnover over {liquidity_window} "
                "sessions"
            ),
            "window": f"{liquidity_window}d",
            "source": source,
            "population": population,
        },
        "factor_r2": {
            "basis": "measured",
            "method": f"OLS R-squared of daily returns on {label}",
            "window": span,
            "source": source,
        },
        "independence": {
            "basis": "measured",
            "method": "derived as 100 - factor_r2 by the builder",
            "window": span,
            "source": source,
        },
        "beta_strength": {
            "basis": "measured",
            "method": (
                f"positive OLS beta against {label}, scaled so beta {BETA_FULL_SCALE} reads 100"
            ),
            "window": span,
            "source": source,
        },
        "beta_stability": {
            "basis": "measured",
            "method": f"agreement of the beta estimate across the two halves of the {span} window",
            "window": span,
            "source": source,
        },
    }


MEASURED_KEYS = ("liquidity", "factor_r2", "beta_strength", "beta_stability")


def merge_into_snapshot(snapshot: dict[str, Any], bundle: dict[str, Any]) -> dict[str, Any]:
    """Replace measured fields atomically; an uncovered refresh never launders old values."""
    merged = dict(snapshot)
    metrics_by_ticker = bundle.get("metrics") or {}
    candidates, uncovered = [], []
    for raw in snapshot.get("candidates") or []:
        candidate = dict(raw)
        ticker = str(candidate.get("ticker", "")).strip().upper()
        measured = metrics_by_ticker.get(ticker) or {}
        metrics = {
            key: value
            for key, value in (candidate.get("metrics") or {}).items()
            if key not in (*MEASURED_KEYS, "independence")
        }
        metrics.update(measured)
        candidate["metrics"] = metrics
        candidate["measurement_record"] = (bundle.get("records") or {}).get(ticker)
        if not measured:
            uncovered.append(ticker)
        candidates.append(candidate)
    merged["candidates"] = candidates
    declared = {
        key: value
        for key, value in (snapshot.get("measurement") or {}).items()
        if key not in (*MEASURED_KEYS, "independence")
    }
    declared.update(bundle.get("measurement") or {})
    merged["measurement"] = declared
    merged["measurement_audit"] = {
        "as_of": bundle.get("as_of"),
        "theme_checks": bundle.get("theme_checks") or {},
        "fund_comparisons": bundle.get("fund_comparisons") or [],
    }
    merged["coverage"] = dict(bundle.get("coverage") or {}, uncovered_candidates=uncovered)
    merged["notes"] = sorted(
        set(list(snapshot.get("notes") or []) + list(bundle.get("notes") or []))
        | {f"{ticker}: not covered by the price table" for ticker in uncovered}
    )
    # Keep a researched as_of; measured data after it is refused by the builder.
    # Eligible uncovered members make the research incomplete, rather than silently surviving.
    if any(c.get("eligible") and c["ticker"] in uncovered for c in candidates):
        merged["complete"] = False
    return merged
