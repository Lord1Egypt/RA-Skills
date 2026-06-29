#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path
from typing import Any, Union


Z_95_TWO_SIDED = 1.645


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")


def _number(value: Any, *, field: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be numeric, got boolean")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be numeric, got {value!r}") from exc


Number = Union[float, int]


def _format_value(value: float, spec: dict[str, Any]) -> Number:
    value_type = str(spec.get("value_type", "")).lower()
    if value_type in {"int", "integer"}:
        return int(round(value))
    precision = spec.get("precision")
    if precision is not None:
        return round(float(value), int(precision))
    return float(value)


def _normal_sigma_from_p05_p95(p05: float, p95: float) -> float:
    sigma = (p95 - p05) / (2.0 * Z_95_TWO_SIDED)
    if sigma <= 0:
        raise ValueError("p95 must be greater than p05")
    return sigma


def sample_lognormal(spec: dict[str, Any], rng: random.Random) -> float:
    median = _number(spec.get("median", spec.get("mean")), field="median")
    p05 = _number(spec.get("p05"), field="p05")
    p95 = _number(spec.get("p95"), field="p95")
    if median <= 0 or p05 <= 0 or p95 <= 0:
        raise ValueError("lognormal median, p05, and p95 must be positive")
    sigma = (math.log(p95) - math.log(p05)) / (2.0 * Z_95_TWO_SIDED)
    if sigma <= 0:
        raise ValueError("p95 must be greater than p05")
    return rng.lognormvariate(math.log(median), sigma)


def sample_normal(spec: dict[str, Any], rng: random.Random) -> float:
    mean = _number(spec.get("mean"), field="mean")
    if "std" in spec:
        sigma = _number(spec.get("std"), field="std")
    else:
        sigma = _normal_sigma_from_p05_p95(_number(spec.get("p05"), field="p05"), _number(spec.get("p95"), field="p95"))
    if sigma <= 0:
        raise ValueError("normal std must be positive")
    return rng.gauss(mean, sigma)


def sample_truncnorm(spec: dict[str, Any], rng: random.Random) -> float:
    clip_min = _number(spec.get("clip_min", -math.inf), field="clip_min")
    clip_max = _number(spec.get("clip_max", math.inf), field="clip_max")
    if clip_min >= clip_max:
        raise ValueError("clip_min must be less than clip_max")
    for _ in range(10000):
        value = sample_normal(spec, rng)
        if clip_min <= value <= clip_max:
            return value
    raise ValueError("Could not sample truncnorm within clip bounds after 10000 attempts")


def sample_uniform(spec: dict[str, Any], rng: random.Random) -> float:
    lower = _number(spec.get("min", spec.get("lower")), field="min/lower")
    upper = _number(spec.get("max", spec.get("upper")), field="max/upper")
    if lower > upper:
        raise ValueError("uniform lower bound must be <= upper bound")
    return rng.uniform(lower, upper)


def sample_one_parameter(spec: dict[str, Any], rng: random.Random) -> Number:
    dist = str(spec.get("distribution", "uniform")).lower().strip()
    if dist == "uniform":
        value = sample_uniform(spec, rng)
    elif dist == "normal":
        value = sample_normal(spec, rng)
    elif dist == "truncnorm":
        value = sample_truncnorm(spec, rng)
    elif dist == "lognormal":
        value = sample_lognormal(spec, rng)
    else:
        raise ValueError(f"Unsupported distribution: {dist}")
    return _format_value(value, spec)


def apply_constraints(params: dict[str, Number], constraints: list[dict[str, Any]]) -> bool:
    for constraint in constraints:
        ctype = str(constraint.get("type", "")).lower().strip()
        if ctype == "bind":
            target = str(constraint["target"])
            source = str(constraint["source"])
            if source not in params:
                raise KeyError(f"Constraint source parameter not found: {source}")
            params[target] = params[source]
        elif ctype == "greater_than":
            left = str(constraint["left"])
            right = str(constraint["right"])
            margin = float(constraint.get("margin", 0.0))
            if left not in params or right not in params:
                raise KeyError(f"Constraint parameters not found: {left}, {right}")
            if not float(params[left]) > float(params[right]) + margin:
                return False
        elif ctype == "less_than":
            left = str(constraint["left"])
            right = str(constraint["right"])
            margin = float(constraint.get("margin", 0.0))
            if left not in params or right not in params:
                raise KeyError(f"Constraint parameters not found: {left}, {right}")
            if not float(params[left]) < float(params[right]) - margin:
                return False
        else:
            raise ValueError(f"Unsupported constraint type: {ctype}")
    return True


def generate_monte_carlo_parameter_sets(space: dict[str, Any], *, samples: int, seed: int) -> list[dict[str, Any]]:
    if samples <= 0:
        raise ValueError("samples must be >= 1")
    raw_params = space.get("parameters")
    if not isinstance(raw_params, dict) or not raw_params:
        raise ValueError("Monte Carlo parameter space must contain a non-empty 'parameters' object")
    constraints = space.get("constraints", [])
    if not isinstance(constraints, list):
        raise ValueError("'constraints' must be a list when provided")

    rng = random.Random(seed)
    trials: list[dict[str, Any]] = []
    max_attempts = max(samples * 100, 1000)
    attempts = 0

    while len(trials) < samples:
        attempts += 1
        if attempts > max_attempts:
            raise ValueError(f"Could not generate {samples} valid samples after {max_attempts} attempts")
        params = {name: sample_one_parameter(spec, rng) for name, spec in raw_params.items()}
        if not apply_constraints(params, constraints):
            continue
        sample_index = len(trials) + 1
        trials.append(
            {
                "name": f"mc_trial_{sample_index:04d}",
                "params": params,
                "metadata": {
                    "sample_index": sample_index,
                    "sampling_method": "monte_carlo",
                    "attempt_index": attempts,
                },
            }
        )
    return trials


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Monte Carlo SWMM parameter sets from probability distributions.")
    parser.add_argument("--parameter-space", required=True, type=Path)
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    space = load_json(args.parameter_space)
    trials = generate_monte_carlo_parameter_sets(space, samples=args.samples, seed=args.seed)
    write_json(args.out, {"parameter_sets": trials})


if __name__ == "__main__":
    main()
