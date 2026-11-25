"""Forecast logic. Same level as the entry script; MGC's import hook routes it
after sealing.

Standard library only, so the demo shows a deliverable that needs no extra
packages in the customer's environment.

Trial builds: set TRIAL_MODE to True before sealing the trial package. The
boundary lives in the script, not in a runtime switch the customer can flip.
"""

TRIAL_MODE = False
TRIAL_MAX_HORIZON = 2

MIN_WINDOW = 2


def moving_average(values: list[float], window: int) -> float:
    """Average of the last `window` points."""
    if not values:
        raise ValueError("empty series")
    window = max(MIN_WINDOW, min(window, len(values)))
    recent = values[-window:]
    return sum(recent) / len(recent)


def growth_rate(values: list[float], lookback: int = 3) -> float:
    """Average period-over-period growth over the last `lookback` periods."""
    if len(values) < 2:
        return 0.0
    lookback = max(1, min(lookback, len(values) - 1))
    current = sum(values[-lookback:]) / lookback
    previous = sum(values[-2 * lookback:-lookback]) / lookback \
        if len(values) >= 2 * lookback else values[0]
    if previous == 0:
        return 0.0
    return (current - previous) / previous


def forecast(values: list[float], periods: int, window: int = 3) -> list[float]:
    """Moving average plus growth extrapolation, rolled forward period by period."""
    if TRIAL_MODE:
        periods = min(periods, TRIAL_MAX_HORIZON)

    series = list(values)
    base = moving_average(series, window)
    rate = growth_rate(series)
    out = []
    for _ in range(max(0, periods)):
        base = base * (1 + rate)
        out.append(round(base, 2))
        series.append(base)
    return out
