"""Theme gauges and fund-versus-basket diagnostics, independent of providers and selection."""

from __future__ import annotations

import math
from typing import Any

import measure_core as m


def basket(legs: list[dict[str, float]]) -> dict[str, float]:
    """Equal weight, daily rebalanced, on dates all constituents actually quote."""
    if not legs:
        return {}
    dates = set.intersection(*(set(leg) for leg in legs))
    return {day: sum(leg[day] for leg in legs) / len(legs) for day in dates}


def correlation(left: dict[str, float], right: dict[str, float], window: int = 252) -> float | None:
    days = sorted(set(left) & set(right))[-window:]
    if len(days) < 30:
        return None
    fit = m.ols([left[d] for d in days], [right[d] for d in days])
    if fit is None:
        return None
    return math.copysign(math.sqrt(fit[1]), fit[0])


def multi_fit(y: list[float], columns: list[list[float]]) -> tuple[list[float], float] | None:
    """Small OLS with an intercept. Singular factors produce no fit, never guessed coefficients."""
    n = len(y)
    if n < 30 or not columns or any(len(c) != n for c in columns):
        return None
    width = len(columns) + 1
    design = [[1.0, *(column[i] for column in columns)] for i in range(n)]
    rows = [
        [sum(r[a] * r[b] for r in design) for b in range(width)]
        + [sum(design[i][a] * y[i] for i in range(n))]
        for a in range(width)
    ]
    for column in range(width):
        pivot = max(range(column, width), key=lambda r: abs(rows[r][column]))
        if abs(rows[pivot][column]) < 1e-14:
            return None
        rows[column], rows[pivot] = rows[pivot], rows[column]
        for row in range(width):
            if row == column:
                continue
            factor = rows[row][column] / rows[column][column]
            for cell in range(column, width + 1):
                rows[row][cell] -= factor * rows[column][cell]
    coef = [rows[i][width] / rows[i][i] for i in range(width)]
    residual = [y[i] - sum(coef[j] * design[i][j] for j in range(width)) for i in range(n)]
    mean = sum(y) / n
    total = sum((v - mean) ** 2 for v in y)
    if total <= 0:
        return None
    return coef[1:], max(0.0, min(1.0, 1 - sum(r * r for r in residual) / total))


def resolve_gauges(series: dict, mapping: dict) -> tuple[dict[str, dict], dict[str, dict]]:
    """Map each ticker to its researched gauge. Internal baskets exclude the ticker itself."""
    if mapping.get("schema_version") != 1 or not isinstance(mapping.get("themes"), dict):
        raise m.MeasureError("benchmark map needs schema_version 1 and a themes object")
    rets = {ticker: m.returns(rows) for ticker, rows in series.items()}
    gauges, diagnostics, assigned = {}, {}, set()
    for code, row in mapping["themes"].items():
        if not isinstance(row, dict):
            raise m.MeasureError(f"{code}: theme mapping must be an object")
        members = row.get("members") or []
        legs = row.get("benchmarks") or []
        if (
            not isinstance(members, list)
            or not isinstance(legs, list)
            or any(not isinstance(t, str) for t in members + legs)
        ):
            raise m.MeasureError(f"{code}: members and benchmarks must be ticker lists")
        if len(set(members)) != len(members) or assigned.intersection(members):
            raise m.MeasureError(f"{code}: a ticker may have only one theme gauge assignment")
        assigned.update(members)
        if not members or (not legs and row.get("mode") != "peer_basket"):
            raise m.MeasureError(f"{code}: declare members and benchmarks or mode=peer_basket")
        own = [ticker for ticker in members if ticker in rets and len(rets[ticker]) >= 30]
        if legs:
            if any(t not in rets for t in legs):
                diagnostics[code] = {"fit": None, "usable": False, "reason": "missing gauge bars"}
                continue
            factor = basket([rets[t] for t in legs])
            fit = correlation(basket([rets[t] for t in own]), factor)
            usable = fit is not None and fit >= 0.30
            diagnostics[code] = {"fit": fit, "usable": usable, "benchmarks": legs}
            if not usable:
                continue
            for ticker in own:
                if ticker in legs:
                    continue  # A gauge cannot establish its own factor fit.
                gauges[ticker] = {
                    "returns": factor,
                    "legs": legs,
                    "theme": code,
                    "mode": "theme_gauge",
                    "fit": fit,
                }
        else:
            diagnostics[code] = {
                "mode": "peer_basket",
                "members": len(own),
                "usable": len(own) >= 3,
                "leave_one_out": True,
            }
            for ticker in own:
                peers = [t for t in own if t != ticker]
                if len(peers) >= 2:
                    gauges[ticker] = {
                        "returns": basket([rets[t] for t in peers]),
                        "legs": peers,
                        "theme": code,
                        "mode": "peer_basket",
                        "fit": None,
                    }
    return gauges, diagnostics


def compound(values: list[float]) -> float:
    return math.prod(1 + value for value in values) - 1


def fund_comparisons(
    series: dict, mapping: dict, windows: tuple[int, ...] = (252, 495)
) -> list[dict]:
    """Two full horizons, tracking plus excess, with the largest contributor removed once."""
    rets = {ticker: m.returns(rows) for ticker, rows in series.items()}
    themes = mapping.get("themes") or {}
    reports = []
    for fund in mapping.get("funds") or []:
        if not isinstance(fund, dict) or not fund.get("ticker") or not fund.get("themes"):
            raise m.MeasureError("fund entries require ticker and covered themes")
        if any(code not in themes for code in fund["themes"]):
            raise m.MeasureError(f"{fund['ticker']}: fund references an unknown theme")
        ticker = fund["ticker"]
        names = sorted(
            {
                t
                for code in fund["themes"]
                for t in themes[code]["members"]
                if t != ticker and t in rets
            }
        )
        row: dict[str, Any] = {"ticker": ticker, "members": names, "windows": {}}
        if ticker not in rets or len(names) < 2:
            row.update(reproduced=False, robust=False, reason="missing fund or too few members")
            reports.append(row)
            continue
        full = basket([rets[t] for t in names])
        for window in windows:
            days = sorted(set(full) & set(rets[ticker]))[-window:]
            if len(days) < window:
                row["windows"][str(window)] = {"observations": len(days), "measured": False}
                continue
            biggest = max(names, key=lambda t: compound([rets[t][d] for d in days]))
            rest = basket([rets[t] for t in names if t != biggest])
            fund_return = compound([rets[ticker][d] for d in days])
            row["windows"][str(window)] = {
                "observations": len(days),
                "measured": True,
                "correlation": correlation({d: full[d] for d in days}, rets[ticker], window),
                "excess": compound([full[d] for d in days]) - fund_return,
                "dropped": biggest,
                "leave_one_out_excess": compound([rest[d] for d in days]) - fund_return,
                "leave_one_out_correlation": correlation(
                    {d: rest[d] for d in days}, rets[ticker], window
                ),
            }
        legs = list(row["windows"].values())
        row["reproduced"] = all(
            x.get("measured") and (x["correlation"] or 0) >= 0.9 and x["excess"] > 0 for x in legs
        )
        row["robust"] = row["reproduced"] and all(
            x["leave_one_out_excess"] > 0 and (x["leave_one_out_correlation"] or 0) >= 0.9
            for x in legs
        )
        reports.append(row)
    return reports
