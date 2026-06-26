"""Metric extraction: named strategies + regex fallback.

Inspired by autoresearch's approach to parsing experiment output.
"""

import re
from typing import Callable

from sal.exceptions import MetricParseError

# Built-in named strategies
BUILTIN_PARSERS: dict[str, Callable[[str], float]] = {
    "last_line_float": lambda out: float(out.strip().splitlines()[-1]),
    "pytest_passed": lambda out: float(
        re.search(r"(\d+) passed", out).group(1)  # type: ignore[union-attr]
    ),
    "pytest_failed": lambda out: float(
        re.search(r"(\d+) failed", out).group(1)  # type: ignore[union-attr]
    ),
    "coverage_percent": lambda out: float(
        re.search(r"(\d+\.?\d*)%", out).group(1)  # type: ignore[union-attr]
    ),
    "val_bpb": lambda out: float(
        re.search(r"^val_bpb:\s+([\d.]+)", out, re.M).group(1)  # type: ignore[union-attr]
    ),
    "benchmark_ms": lambda out: float(
        re.search(r"([\d.]+)\s*ms", out).group(1)  # type: ignore[union-attr]
    ),
}


def get_parser(spec: str) -> Callable[[str], float]:
    """Resolve metric_parser spec to a callable.

    Resolution order:
    1. Named strategy (e.g. "pytest_passed")
    2. Regex with first capture group (e.g. r"score: ([\\d.]+)")
    3. ValueError if neither works

    Args:
        spec: Named strategy name or regex pattern with one capture group.

    Returns:
        A callable that takes command output (str) and returns a float.

    Raises:
        ValueError: If spec is not a named strategy and not a valid regex
                    with exactly one capture group.
    """
    if spec in BUILTIN_PARSERS:
        return BUILTIN_PARSERS[spec]

    # Treat as regex — must have exactly one capture group
    try:
        pattern = re.compile(spec)
        if pattern.groups != 1:
            raise ValueError(
                f"Regex must have exactly 1 capture group, got {pattern.groups}: '{spec}'"
            )
        return lambda out, p=pattern: float(p.search(out).group(1))  # type: ignore[union-attr]
    except re.error as e:
        raise ValueError(
            f"metric_parser '{spec}' is not a named strategy or valid regex: {e}"
        ) from e


def extract_metric(output: str, spec: str) -> float:
    """Convenience: parse + extract in one call.

    Args:
        output: Raw command stdout/stderr.
        spec: Named strategy or regex.

    Returns:
        Extracted float metric value.

    Raises:
        MetricParseError: If extraction fails.
    """
    parser = get_parser(spec)
    try:
        return parser(output)
    except (AttributeError, ValueError, IndexError) as e:
        raise MetricParseError(
            f"Failed to extract metric with '{spec}' from output: {e}\n"
            f"Output (last 200 chars): ...{output[-200:]}"
        ) from e
