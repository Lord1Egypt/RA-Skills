#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Optional

import numpy as np


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")


def normalized_discrete_entropy(
    values: np.ndarray,
    *,
    bins: int = 10,
    value_min: Optional[float] = None,
    value_max: Optional[float] = None,
) -> np.ndarray:
    """Calculate H*(t) for an ensemble array shaped [n_samples, n_timesteps]."""
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 2:
        raise ValueError("values must be a 2D array shaped [n_samples, n_timesteps]")
    if bins < 2:
        raise ValueError("bins must be >= 2")

    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return np.full(arr.shape[1], np.nan)

    lo = float(np.min(finite) if value_min is None else value_min)
    hi = float(np.max(finite) if value_max is None else value_max)
    if hi <= lo:
        return np.zeros(arr.shape[1], dtype=float)

    out = np.zeros(arr.shape[1], dtype=float)
    for idx in range(arr.shape[1]):
        col = arr[:, idx]
        col = col[np.isfinite(col)]
        if col.size == 0:
            out[idx] = np.nan
            continue
        counts, _ = np.histogram(col, bins=bins, range=(lo, hi))
        total = int(np.sum(counts))
        if total == 0:
            out[idx] = np.nan
            continue
        probs = counts[counts > 0] / total
        entropy = -float(np.sum(probs * np.log(probs)))
        out[idx] = min(1.0, max(0.0, entropy / math.log(bins)))
    return out


def ensemble_summary(values: np.ndarray) -> dict[str, list[Optional[float]]]:
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 2:
        raise ValueError("values must be a 2D array shaped [n_samples, n_timesteps]")
    return {
        "p05": _nanpercentile_list(arr, 5),
        "p50": _nanpercentile_list(arr, 50),
        "p95": _nanpercentile_list(arr, 95),
        "min": _nanmin_list(arr),
        "max": _nanmax_list(arr),
    }


def _nanpercentile_list(arr: np.ndarray, q: float) -> list[Optional[float]]:
    vals = np.nanpercentile(arr, q, axis=0)
    return [None if not np.isfinite(v) else float(v) for v in vals]


def _nanmin_list(arr: np.ndarray) -> list[Optional[float]]:
    vals = np.nanmin(arr, axis=0)
    return [None if not np.isfinite(v) else float(v) for v in vals]


def _nanmax_list(arr: np.ndarray) -> list[Optional[float]]:
    vals = np.nanmax(arr, axis=0)
    return [None if not np.isfinite(v) else float(v) for v in vals]


def calculate_entropy_record(payload: dict[str, Any], *, bins: int) -> dict[str, Any]:
    values = np.asarray(payload["values"], dtype=float)
    entropy = normalized_discrete_entropy(
        values,
        bins=bins,
        value_min=payload.get("value_min"),
        value_max=payload.get("value_max"),
    )
    return {
        "metric": payload.get("metric", "unknown"),
        "bins": bins,
        "sample_count": int(values.shape[0]),
        "time_count": int(values.shape[1]),
        "time": payload.get("time"),
        "entropy": [None if not np.isfinite(v) else float(v) for v in entropy],
        "ensemble": ensemble_summary(values),
        "interpretation": "Normalized Shannon entropy of the output ensemble. This is parameter-induced output entropy, not calibration performance.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate normalized entropy for a SWMM output ensemble JSON.")
    parser.add_argument("--ensemble-json", required=True, type=Path)
    parser.add_argument("--bins", type=int, default=10)
    parser.add_argument("--out", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = load_json(args.ensemble_json)
    write_json(args.out, calculate_entropy_record(payload, bins=args.bins))


if __name__ == "__main__":
    main()
