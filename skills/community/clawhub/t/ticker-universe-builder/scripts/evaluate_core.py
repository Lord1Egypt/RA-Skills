#!/usr/bin/env python3
"""Measure a universe after the fact, from a price table covering the window it lived through.

Every threshold in this skill is a guess. The guidance ranges, `BETA_FULL_SCALE`, the
listing-age bands, the score weights, the breadth factors, the theme weights — all set by
judgement, and none of them has ever been checked against an outcome. That is the largest gap in
the design, and it is worse for a declared market, whose numbers were invented at run time by an
agent rather than judged once by a person.

This is not a backtest and does not produce one. A universe is an observation instrument, not a
portfolio, so the question is never "what did it return" — it is whether the instrument saw what
happened. Every section below is tied to one constant it would recalibrate:

| Section | Recalibrates |
|---|---|
| `survival` | the freshness window and the review cadence |
| `coverage` | the per-market guidance ranges — was the universe wide enough to see the move |
| `rejections` | the eligibility rules, by exclusion code |
| `themes` | the theme `weight`s — whether the taxonomy is weighted where the moves were |
| `metrics` | `SCORE_WEIGHTS` — which metric actually ordered anything |
| `independence` | the declared factor redundancy against the realised one |
| `redundancy` | whether two members turned out to be the same observation post |

Reads the same CSV `measure` does. Standard library only.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import measure_core  # noqa: E402

# An evaluation window is often short — one review cycle — so this is looser than the 30 bars a
# measured statistic needs. Below it, a ticker is reported as unobservable rather than scored.
MIN_OBSERVATIONS = 10
TOP_N = (10, 25, 50)
# Below this many scored members a rank correlation is noise dressed as a finding.
MIN_FOR_CORRELATION = 8
# A member whose history covers less than this share of the window cannot join the pairwise
# grid without shortening it for everyone, so it is named and set aside instead.
MIN_HISTORY_SHARE = 0.5
# How many of the most correlated pairs to print. Long enough to show a cluster, short enough
# that a reader looks at all of it.
REDUNDANT_PAIRS = 15
# Not a threshold anything is judged against — nothing here gates. It is the line above which
# the count of pairs is worth putting in the summary beside the median.
HIGH_CORRELATION = 0.9
ANNUALISATION = 252


class EvaluateError(Exception):
    pass


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def _stdev(values: list[float]) -> float | None:
    if len(values) < 2:
        return None
    average = _mean(values)
    return math.sqrt(sum((value - average) ** 2 for value in values) / (len(values) - 1))


def _pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    mx, my = _mean(xs), _mean(ys)
    dx = [x - mx for x in xs]
    dy = [y - my for y in ys]
    denominator = math.sqrt(sum(v * v for v in dx)) * math.sqrt(sum(v * v for v in dy))
    if denominator == 0:
        return None
    return sum(a * b for a, b in zip(dx, dy, strict=True)) / denominator


def _ranks(values: list[float]) -> list[float]:
    """Average ranks, so ties do not invent an ordering the data does not carry."""
    order = sorted(range(len(values)), key=lambda index: values[index])
    ranks = [0.0] * len(values)
    position = 0
    while position < len(order):
        end = position
        while end + 1 < len(order) and values[order[end + 1]] == values[order[position]]:
            end += 1
        shared = (position + end) / 2 + 1
        for index in range(position, end + 1):
            ranks[order[index]] = shared
        position = end + 1
    return ranks


def _spearman(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < MIN_FOR_CORRELATION:
        return None
    return _pearson(_ranks(xs), _ranks(ys))


def _round(value: float | None, places: int = 4) -> float | None:
    return None if value is None else round(value, places)


def window_stats(
    series: dict[str, list[tuple[str, float, float | None]]],
) -> dict[str, dict[str, Any]]:
    """Total return, realised volatility and the daily series, per ticker."""
    stats: dict[str, dict[str, Any]] = {}
    for ticker, rows in series.items():
        if len(rows) < MIN_OBSERVATIONS:
            continue
        daily = measure_core.returns(rows)
        if not daily:
            continue
        values = list(daily.values())
        deviation = _stdev(values)
        stats[ticker] = {
            "observations": len(rows),
            "first": rows[0][0],
            "last": rows[-1][0],
            "total_return": rows[-1][1] / rows[0][1] - 1.0,
            "volatility": None if deviation is None else deviation * math.sqrt(ANNUALISATION),
            "daily": daily,
        }
    return stats


def _survival(members: list[dict], stats: dict[str, dict]) -> dict[str, Any]:
    """A member that stopped printing is a dead sensor, whatever it did before it stopped."""
    missing = sorted(item["ticker"] for item in members if item["ticker"] not in stats)
    observed = len(members) - len(missing)
    return {
        "members": len(members),
        "observed": observed,
        "rate": _round(observed / len(members)) if members else None,
        "unobservable": missing,
    }


def _coverage(
    members: list[dict], stats: dict[str, dict], tops: tuple[int, ...]
) -> dict[str, Any]:
    """Of the largest moves in the table, how many did the instrument have a sensor on.

    This is the whole question a universe exists to answer, and it is only answerable if the
    price table is wider than the universe — the audit's rejected candidates at least. A table
    holding nothing but members makes every number here 1.0, so the share is reported beside it.
    """
    held = {item["ticker"] for item in members}
    ranked = sorted(stats, key=lambda t: -abs(stats[t]["total_return"]))
    result: dict[str, Any] = {
        "pool": len(ranked),
        "members_in_pool": len(held & set(ranked)),
        "member_share_of_pool": _round(len(held & set(ranked)) / len(ranked)) if ranked else None,
        "top": {},
    }
    for top in tops:
        window = ranked[:top]
        if len(window) < top:
            continue
        inside = sum(1 for ticker in window if ticker in held)
        result["top"][str(top)] = {
            "covered": inside,
            "rate": _round(inside / top),
            "missed": [ticker for ticker in window if ticker not in held],
        }
    return result


def _rejections(
    audit: list[dict], stats: dict[str, dict], members: list[dict], top: int
) -> dict[str, Any]:
    """Did the candidates that lost their slot move more than the ones that kept it?

    Broken down by exclusion code, because that is the actionable form. "Some rejections were
    expensive" changes nothing; "every candidate dropped for insufficient_liquidity was in the
    top ten movers" changes a threshold.
    """
    held = {item["ticker"] for item in members}
    ranked = set(sorted(stats, key=lambda t: -abs(stats[t]["total_return"]))[:top])
    by_code: dict[str, list[str]] = {}
    for entry in audit:
        ticker = str(entry.get("ticker", ""))
        if ticker in held or ticker not in stats:
            continue
        for reason in entry.get("reasons") or []:
            by_code.setdefault(str(reason).split(":", 1)[0].strip(), []).append(ticker)
    codes = {}
    for code, tickers in sorted(by_code.items()):
        moves = [abs(stats[ticker]["total_return"]) for ticker in tickers]
        inside = sorted(ticker for ticker in tickers if ticker in ranked)
        codes[code] = {
            "observed": len(tickers),
            "median_absolute_move": _round(_median(moves)),
            f"in_top_{top}": inside,
        }
    member_moves = [abs(stats[t]["total_return"]) for t in held if t in stats]
    return {
        "selected_median_absolute_move": _round(_median(member_moves)),
        "by_code": codes,
    }


def _themes(members: list[dict], stats: dict[str, dict]) -> dict[str, Any]:
    """Where the realised volatility actually sat, against how the taxonomy spread its slots."""
    buckets: dict[str, list[float]] = {}
    for item in members:
        entry = stats.get(item["ticker"])
        if entry and entry["volatility"] is not None:
            buckets.setdefault(item["theme_code"], []).append(entry["volatility"])
    if not buckets:
        return {"themes": {}, "most_volatile": None}
    rows = {
        code: {"members": len(values), "mean_volatility": _round(_mean(values))}
        for code, values in sorted(buckets.items())
    }
    total = sum(row["mean_volatility"] * row["members"] for row in rows.values())
    for row in rows.values():
        row["share_of_volatility"] = (
            _round(row["mean_volatility"] * row["members"] / total) if total else None
        )
    hottest = max(rows, key=lambda code: rows[code]["mean_volatility"])
    return {"themes": rows, "most_volatile": hottest}


def _metrics(members: list[dict], stats: dict[str, dict]) -> dict[str, Any]:
    """Which metric ordered anything, and which one was decoration.

    A metric carrying weight in `SCORE_WEIGHTS` and showing no rank relationship to either the
    size of the move or its volatility is a weight spent on nothing. The answer is not "drop it"
    — `quality` is not supposed to predict a move — but the number should be looked at before
    the next weight is chosen.
    """
    fields: dict[str, Any] = {}
    names: set[str] = set()
    for item in members:
        names.update((item.get("metrics") or {}).keys())
    for name in sorted(names):
        pairs = [
            (float((item.get("metrics") or {})[name]), stats[item["ticker"]])
            for item in members
            if item["ticker"] in stats
            and (item.get("metrics") or {}).get(name) is not None
        ]
        volatile = [(value, entry["volatility"]) for value, entry in pairs
                    if entry["volatility"] is not None]
        fields[name] = {
            "scored": len(pairs),
            "vs_absolute_move": _round(_spearman(
                [value for value, _ in pairs],
                [abs(entry["total_return"]) for _, entry in pairs],
            )),
            "vs_volatility": _round(_spearman(
                [value for value, _ in volatile], [vol for _, vol in volatile]
            )),
        }
    return fields


def _independence(
    members: list[dict],
    stats: dict[str, dict],
    benchmarks: list[str],
    series: dict[str, list[tuple[str, float, float | None]]],
) -> dict[str, Any]:
    """The declared redundancy against the realised one.

    Price independence is auxiliary in coverage-first and a selection metric in legacy replay.
    Compare it to the observed window without turning measurement error into an admission gate.
    """
    if not benchmarks:
        return {"benchmarks": [], "note": "pass --benchmark to compare declared independence"}
    missing = [ticker for ticker in benchmarks if ticker not in series]
    if missing:
        raise EvaluateError(f"benchmark not in the price table: {', '.join(sorted(missing))}")
    factor = measure_core.factor_returns(series, benchmarks)
    if not factor:
        raise EvaluateError("the benchmark legs share no dates")
    rows = []
    for item in members:
        entry = stats.get(item["ticker"])
        declared = (item.get("metrics") or {}).get("independence")
        if entry is None or declared is None:
            continue
        shared = sorted(set(entry["daily"]) & set(factor))
        if len(shared) < MIN_OBSERVATIONS:
            continue
        fit = measure_core.ols([entry["daily"][d] for d in shared], [factor[d] for d in shared])
        if fit is None:
            continue
        realised = round(100.0 * (1.0 - fit[1]), 1)
        rows.append({
            "ticker": item["ticker"],
            "role": item["role"],
            "declared_independence": float(declared),
            "realised_independence": realised,
            "error": round(realised - float(declared), 1),
        })
    rows.sort(key=lambda row: -abs(row["error"]))
    return {
        "benchmarks": sorted(benchmarks),
        "compared": len(rows),
        "mean_absolute_error": _round(_mean([abs(row["error"]) for row in rows]), 2)
        if rows else None,
        "largest_errors": rows[:10],
    }


def _redundancy(members: list[dict], stats: dict[str, dict]) -> dict[str, Any]:
    """Which two members turned out to be the same observation post.

    `factor_r2` measures a member against the factor complex and `independence` measures it
    against the benchmark basket. Neither compares two members to each other, so the one error
    this instrument cannot see is the one it can least afford: the breadth floor already spends
    over half the budget, and a duplicated hill costs a seat that no other theme can get back.

    Disclosure, not a gate. Two names can be highly correlated and both belong — one market
    moving one way is what a sector is — and a reader with the pair in front of them is far
    better placed to judge that than a threshold would be.
    """
    observed = [item for item in members if item["ticker"] in stats]
    if len(observed) < 2:
        return {"compared": 0, "note": "fewer than two members are observable in this window"}
    union: set[str] = set()
    for item in observed:
        union |= set(stats[item["ticker"]]["daily"])
    # One newly listed member would otherwise cut the shared grid down to its own short history
    # and make every correlation in the report a different, weaker statistic.
    kept = [
        item for item in observed
        if len(stats[item["ticker"]]["daily"]) >= MIN_HISTORY_SHARE * len(union)
    ]
    short = sorted(
        item["ticker"] for item in observed
        if len(stats[item["ticker"]]["daily"]) < MIN_HISTORY_SHARE * len(union)
    )
    grid = sorted(set.intersection(*(set(stats[item["ticker"]]["daily"]) for item in kept))) \
        if len(kept) >= 2 else []
    if len(grid) < MIN_OBSERVATIONS:
        return {
            "compared": 0,
            "short_history": short,
            "note": f"members share fewer than {MIN_OBSERVATIONS} dates; no pair is comparable",
        }
    # Standardised once per member, so a correlation is a dot product and a Heavy universe does
    # not turn one command into a coffee break.
    unit: dict[str, list[float]] = {}
    flat: list[str] = []
    for item in kept:
        series = stats[item["ticker"]]["daily"]
        values = [series[day] for day in grid]
        mean = _mean(values)
        norm = math.sqrt(sum((value - mean) ** 2 for value in values))
        if norm > 0:
            unit[item["ticker"]] = [(value - mean) / norm for value in values]
        else:
            # A member that did not move has no correlation with anything — the statistic is
            # undefined, not zero. Naming it matters more than the pair it cannot form: a
            # sensor printing a flat line is a dead sensor, and nothing else in the report
            # would say so.
            flat.append(item["ticker"])
    theme = {item["ticker"]: item["theme_code"] for item in kept}
    role = {item["ticker"]: item["role"] for item in kept}
    tickers = sorted(unit)
    pairs = []
    for index, left in enumerate(tickers):
        for right in tickers[index + 1:]:
            correlation = sum(a * b for a, b in zip(unit[left], unit[right], strict=True))
            pairs.append({
                "pair": [left, right],
                "correlation": _round(correlation),
                "themes": [theme[left], theme[right]],
                "same_theme": theme[left] == theme[right],
                "roles": [role[left], role[right]],
            })
    pairs.sort(key=lambda row: (-row["correlation"], row["pair"]))
    values = [row["correlation"] for row in pairs]
    return {
        "compared": len(tickers),
        "observations": len(grid),
        "pairs": len(pairs),
        "short_history": short,
        "no_variation": sorted(flat),
        "median_correlation": _round(_median(values)),
        "above_high": sum(1 for value in values if value >= HIGH_CORRELATION),
        "high_correlation": HIGH_CORRELATION,
        "most_correlated": pairs[:REDUNDANT_PAIRS],
    }


def evaluate(
    *,
    universe: dict[str, Any],
    prices: str | Path,
    benchmarks: list[str] | None = None,
    top: int | None = None,
) -> dict[str, Any]:
    members = universe.get("members") or []
    if not members:
        raise EvaluateError("universe has no members to evaluate")
    # Evaluation is forward observation. In-sample bars must not leak into its outcome window.
    if not universe.get("as_of"):
        raise EvaluateError("universe as_of is required for forward evaluation")
    try:
        series = measure_core.read_bars(prices, after=universe["as_of"])
    except measure_core.MeasureError as exc:
        raise EvaluateError(f"no usable forward price table: {exc}") from exc
    stats = window_stats(series)
    if not stats:
        raise EvaluateError(
            f"no ticker in the price table has {MIN_OBSERVATIONS} observations"
        )
    tops = tuple(sorted({top})) if top else TOP_N
    window = sorted(entry["first"] for entry in stats.values())[0], \
        sorted(entry["last"] for entry in stats.values())[-1]
    return {
        "schema_version": 1,
        "universe": {
            "market": universe.get("market"),
            "profile": universe.get("profile"),
            "version_hash": universe.get("version_hash"),
            "as_of": universe.get("as_of"),
            "market_spec_declared": bool(universe.get("market_spec")),
        },
        "window": {"from": window[0], "to": window[1]},
        "survival": _survival(members, stats),
        "coverage": _coverage(members, stats, tops),
        "rejections": _rejections(
            universe.get("selection_audit") or [], stats, members, max(tops)
        ),
        "themes": _themes(members, stats),
        "metrics": _metrics(members, stats),
        "independence": _independence(members, stats, benchmarks or [], series),
        "redundancy": _redundancy(members, stats),
    }
