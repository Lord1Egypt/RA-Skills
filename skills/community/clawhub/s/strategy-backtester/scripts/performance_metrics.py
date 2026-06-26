from __future__ import annotations

import math
from statistics import mean, pstdev


def total_return(returns: list[float]) -> float:
    value = 1.0
    for item in returns:
        value *= 1.0 + item
    return value - 1.0


def annualized_return(returns: list[float], periods_per_year: int) -> float | None:
    if not returns:
        return None
    compounded = 1.0 + total_return(returns)
    years = len(returns) / periods_per_year
    if years <= 0 or compounded <= 0:
        return None
    return compounded ** (1.0 / years) - 1.0


def annualized_volatility(returns: list[float], periods_per_year: int) -> float | None:
    if len(returns) < 2:
        return None
    return pstdev(returns) * math.sqrt(periods_per_year)


def max_drawdown(returns: list[float]) -> float:
    value = 1.0
    peak = 1.0
    worst = 0.0
    for item in returns:
        value *= 1.0 + item
        peak = max(peak, value)
        worst = min(worst, value / peak - 1.0)
    return worst


def sharpe_ratio(
    returns: list[float],
    periods_per_year: int,
    risk_free_rate: float = 0.0,
) -> float | None:
    if len(returns) < 2:
        return None
    period_rf = risk_free_rate / periods_per_year
    excess = [item - period_rf for item in returns]
    volatility = pstdev(excess)
    if volatility == 0:
        return None
    return mean(excess) / volatility * math.sqrt(periods_per_year)


def sortino_ratio(
    returns: list[float],
    periods_per_year: int,
    risk_free_rate: float = 0.0,
) -> float | None:
    if len(returns) < 2:
        return None
    period_rf = risk_free_rate / periods_per_year
    downside = [min(0.0, item - period_rf) for item in returns]
    downside_dev = math.sqrt(mean([item * item for item in downside]))
    if downside_dev == 0:
        return None
    excess_mean = mean([item - period_rf for item in returns])
    return excess_mean / downside_dev * math.sqrt(periods_per_year)


def average_turnover(selected_history: list[set[str]]) -> float | None:
    if len(selected_history) < 2:
        return None
    turnovers = []
    for previous, current in zip(selected_history, selected_history[1:]):
        if not current:
            continue
        changed = len(current - previous)
        turnovers.append(changed / len(current))
    return mean(turnovers) if turnovers else None
