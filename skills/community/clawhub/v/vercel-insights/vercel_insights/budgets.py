"""Performance budgets: turn a measurement into a pass or a fail.

Reporting a number is useful to a person reading a terminal. Failing a build is
useful to a team that wants a regression caught before it ships, and that needs
one more thing: a threshold, and an exit code that means "over it".

A budget is deliberately a plain comparison against a value the user chose,
because the alternative (comparing against last week automatically) needs stored
state, and this tool writes no files by design.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from . import ConfigError

#: Exit code for "the query worked, and a budget was exceeded". Distinct from 1
#: on purpose: a failing budget is a successful run reporting bad news, and a CI
#: step usually wants to tell that apart from the API being down.
BUDGET_EXCEEDED = 3


@dataclass(frozen=True)
class Budget:
    """One threshold: a metric short name and the value it must not exceed."""

    metric: str
    limit: float

    def verdict(self, value: float | None) -> str:
        """``pass``, ``fail`` or ``no data`` for one measured value."""
        if value is None:
            return "no data"
        return "pass" if value <= self.limit else "fail"


def parse_budget(text: str, known: Sequence[str]) -> Budget:
    """Parse one ``metric=value`` budget.

    Args:
        text: The flag value as written, for example ``lcp=2500``.
        known: The metric short names this surface accepts.

    Raises:
        ConfigError: With the offending value and the accepted form.
    """
    name, separator, raw = text.partition("=")
    name = name.strip().lower()
    if not separator or not name or not raw.strip():
        raise ConfigError(
            f"--budget {text!r} is not in the form NAME=VALUE, for example "
            f"--budget lcp=2500 or --budget cls=0.1 (metrics: {', '.join(known)})"
        )
    if name not in known:
        raise ConfigError(
            f"--budget names unknown metric {name!r}; the Speed Insights "
            f"metrics are {', '.join(known)}"
        )
    try:
        limit = float(raw.strip())
    except ValueError:
        raise ConfigError(
            f"--budget {text!r} has a non-numeric limit {raw.strip()!r}; give a "
            "number in the metric's own unit, milliseconds for lcp, inp, fcp "
            "and ttfb, and an unitless score for cls"
        ) from None
    if limit <= 0:
        raise ConfigError(
            f"--budget {text!r} must be greater than zero; a budget of {limit} "
            "could never be met"
        )
    return Budget(metric=name, limit=limit)


def parse_budgets(values: Sequence[str], known: Sequence[str]) -> list[Budget]:
    """Parse every ``--budget`` flag, rejecting a metric named twice."""
    budgets: list[Budget] = []
    seen: set[str] = set()
    for value in values:
        budget = parse_budget(value, known)
        if budget.metric in seen:
            raise ConfigError(
                f"--budget names {budget.metric!r} twice; keep one limit per metric"
            )
        seen.add(budget.metric)
        budgets.append(budget)
    return budgets


def evaluate(
    budgets: Sequence[Budget],
    measured: Mapping[str, float | None],
) -> list[tuple[Budget, float | None, str]]:
    """Pair each budget with what was measured and the verdict."""
    return [(b, measured.get(b.metric), b.verdict(measured.get(b.metric))) for b in budgets]


def any_failed(results: Sequence[tuple[Budget, float | None, str]]) -> bool:
    """True when at least one budget was exceeded.

    A metric with no data is deliberately not a failure. An empty window means
    the measurement is missing, not that the site got slower, and failing a
    build on absent data would train people to ignore the check.
    """
    return any(verdict == "fail" for _budget, _value, verdict in results)


__all__ = [
    "BUDGET_EXCEEDED",
    "Budget",
    "any_failed",
    "evaluate",
    "parse_budget",
    "parse_budgets",
]
