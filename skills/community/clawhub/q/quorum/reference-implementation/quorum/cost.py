# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Cost tracking and estimation for Quorum validation runs.

Tracks LLM token usage and cost per call, with thread-safe aggregation across
parallel batch validation workers. Provides pre-run cost estimates so users
can plan before committing large validation runs.
"""

from __future__ import annotations

import logging
import threading
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# ── Time estimation calibration constants ────────────────────────────────────

# Thorough depth: per-file time in seconds by file type.
# Multipliers relative to python baseline (1.0x): docs=2.0x, config=1.5x, generic=1.2x
# Source: production runs (13 Python files → ~22 min observed; docs heavier due to critic work)
THOROUGH_SECONDS_PER_FILE: dict[str, int] = {
    "python": 100,   # observed: ~100 sec/file
    "docs": 200,     # observed range: 180-240 sec/file
    "config": 150,   # 1.5x python baseline
    "generic": 120,  # 1.2x python baseline
}

# Calibrated ranges for thorough depth per file type: (min_sec, max_sec)
_THOROUGH_RANGE: dict[str, tuple[int, int]] = {
    "python": (85, 115),
    "docs": (180, 240),
    "config": (128, 172),
    "generic": (102, 138),
}

# Quick/standard depth: (min_sec, mid_sec, max_sec) — same for all file types
_DEPTH_SECONDS: dict[str, tuple[int, int, int]] = {
    "quick": (10, 12, 15),      # pre-screen only, no LLM calls
    "standard": (45, 52, 60),
}

# ── Approximate per-token costs (USD) for common models ──────────────────────
# Format: {model_name_fragment: (input_per_1k_tokens, output_per_1k_tokens)}
# Check your provider's current pricing — these are approximate.
_MODEL_RATES: dict[str, tuple[float, float]] = {
    "claude-opus-4": (0.015, 0.075),
    "claude-opus": (0.015, 0.075),
    "claude-sonnet-4": (0.003, 0.015),
    "claude-sonnet": (0.003, 0.015),
    "claude-haiku-4": (0.00025, 0.00125),
    "claude-haiku": (0.00025, 0.00125),
    "gpt-4o-mini": (0.00015, 0.0006),
    "gpt-4o": (0.005, 0.015),
    "gpt-4-turbo": (0.01, 0.03),
    "gpt-4": (0.03, 0.06),
    "gpt-3.5-turbo": (0.0005, 0.0015),
    "gemini-1.5-pro": (0.00125, 0.005),
    "gemini-1.5-flash": (0.000075, 0.0003),
    "mistral-large": (0.003, 0.009),
    "mistral-small": (0.001, 0.003),
}

# Fallback rate for unrecognized models
_FALLBACK_RATE: tuple[float, float] = (0.001, 0.003)


class BudgetExceededError(Exception):
    """Raised when total LLM cost exceeds the configured max_cost budget."""

    def __init__(self, current: float, limit: float) -> None:
        self.current = current
        self.limit = limit
        super().__init__(
            f"Budget exceeded: ${current:.4f} spent of ${limit:.2f} limit"
        )


class CallRecord(BaseModel):
    """Record of a single LLM call."""

    call_name: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float
    file_path: str | None = None


class CostSummary(BaseModel):
    """Aggregated cost summary for a validation run."""

    total_usd: float
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    calls: int
    per_file: dict[str, float] = Field(default_factory=dict)
    records: list[CallRecord] = Field(default_factory=list)


class CostEstimate(BaseModel):
    """Pre-run cost estimate for a set of files."""

    estimated_usd: float
    estimated_calls: int
    estimated_prompt_tokens: int
    estimated_completion_tokens: int
    estimated_total_tokens: int
    files_count: int
    critics_count: int
    is_approximate: bool = True


class TimeEstimate(BaseModel):
    """Pre-run time estimate for a validation run."""

    depth: str
    files_count: int
    estimated_seconds: int
    min_seconds: int
    max_seconds: int
    recommended_timeout: int  # max_seconds * 1.2, gives a 20% buffer
    per_type_counts: dict[str, int] = Field(default_factory=dict)


class CostTracker:
    """
    Thread-safe tracker for LLM token usage and cost.

    Designed for parallel batch validation: multiple threads write to the same
    tracker concurrently. Uses threading.local() for per-thread file context so
    that concurrent file validations attribute costs to the correct file without
    race conditions.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._records: list[CallRecord] = []
        # Thread-local storage for current file path — each thread has its own
        self._local = threading.local()

    def set_current_file(self, file_path: str | None) -> None:
        """
        Set the file being validated in this thread's context.

        Call this before starting validation of a new file. Because it uses
        thread-local storage, concurrent threads don't interfere with each other.
        """
        self._local.current_file = file_path

    def track(
        self,
        call_name: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        cost: float,
    ) -> None:
        """Record a single LLM call."""
        file_path: str | None = getattr(self._local, "current_file", None)
        record = CallRecord(
            call_name=call_name,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            cost_usd=cost,
            file_path=file_path,
        )
        with self._lock:
            self._records.append(record)

    @property
    def total_cost(self) -> float:
        with self._lock:
            return sum(r.cost_usd for r in self._records)

    @property
    def total_tokens(self) -> int:
        with self._lock:
            return sum(r.total_tokens for r in self._records)

    def per_file_cost(self, file_path: str) -> float:
        """Return total cost attributed to a specific file path."""
        with self._lock:
            return sum(r.cost_usd for r in self._records if r.file_path == file_path)

    def summary(self) -> CostSummary:
        """Return aggregated cost summary across all tracked calls."""
        with self._lock:
            records = list(self._records)

        per_file: dict[str, float] = {}
        for r in records:
            if r.file_path:
                per_file[r.file_path] = per_file.get(r.file_path, 0.0) + r.cost_usd

        return CostSummary(
            total_usd=sum(r.cost_usd for r in records),
            prompt_tokens=sum(r.prompt_tokens for r in records),
            completion_tokens=sum(r.completion_tokens for r in records),
            total_tokens=sum(r.total_tokens for r in records),
            calls=len(records),
            per_file=per_file,
            records=records,
        )

    def check_budget(self, max_cost: float) -> None:
        """
        Raise BudgetExceededError if total cost exceeds max_cost.

        Raises:
            BudgetExceededError: If current total exceeds the limit.
        """
        current = self.total_cost
        if current > max_cost:
            raise BudgetExceededError(current=current, limit=max_cost)


def _get_model_rate(model: str) -> tuple[float, float]:
    """Look up per-1k-token rates for a model. Returns (input, output)."""
    model_lower = model.lower()
    # Strip provider prefix (e.g. "anthropic/claude-opus-4" → "claude-opus-4")
    if "/" in model_lower:
        model_lower = model_lower.split("/", 1)[1]

    for name, rates in _MODEL_RATES.items():
        if name in model_lower:
            return rates

    return _FALLBACK_RATE


def estimate_cost(files: list[Path], config: Any) -> CostEstimate:
    """
    Estimate the cost of running Quorum validation on a list of files.

    Calculation:
    - input tokens per call ≈ file_size_chars / 4 + 2000 (system prompt + rubric overhead)
    - output tokens per call ≈ 2000 per critic call
    - cost alternates between tier_1 and tier_2 model rates for a blended average

    This is APPROXIMATE — actual costs vary based on prompt structure, rubric
    size, and model behaviour. The estimate is shown with a disclaimer in the CLI.

    Args:
        files:  List of file paths to validate.
        config: QuorumConfig with model_tier1, model_tier2, and critics list.

    Returns:
        CostEstimate with estimated totals.
    """
    num_critics = len(config.critics)
    num_files = len(files)

    rate_t1 = _get_model_rate(config.model_tier1)
    rate_t2 = _get_model_rate(config.model_tier2)

    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_cost = 0.0

    for file_path in files:
        try:
            file_chars = len(file_path.read_text(encoding="utf-8", errors="replace"))
        except (OSError, IOError):
            file_chars = 2000  # Fallback for unreadable files

        file_tokens = file_chars // 4
        input_tokens_per_call = file_tokens + 2000
        output_tokens_per_call = 2000

        for i in range(num_critics):
            # Alternate tiers for a rough blended estimate
            input_per_1k, output_per_1k = rate_t1 if i % 2 == 0 else rate_t2
            call_cost = (
                input_tokens_per_call / 1000 * input_per_1k
                + output_tokens_per_call / 1000 * output_per_1k
            )
            total_prompt_tokens += input_tokens_per_call
            total_completion_tokens += output_tokens_per_call
            total_cost += call_cost

    return CostEstimate(
        estimated_usd=total_cost,
        estimated_calls=num_files * num_critics,
        estimated_prompt_tokens=total_prompt_tokens,
        estimated_completion_tokens=total_completion_tokens,
        estimated_total_tokens=total_prompt_tokens + total_completion_tokens,
        files_count=num_files,
        critics_count=num_critics,
        is_approximate=True,
    )


def _classify_file_type(path: Path) -> str:
    """Classify a file path into a time-estimation category."""
    suffix = path.suffix.lower()
    if suffix in {".py", ".pyx", ".pyi"}:
        return "python"
    if suffix in {".md", ".rst", ".txt"}:
        return "docs"
    if suffix in {".yaml", ".yml", ".json", ".toml"}:
        return "config"
    return "generic"


def time_estimate(files: list[Path], depth: str) -> TimeEstimate:
    """
    Estimate wall-clock time for a Quorum validation run.

    Uses calibration data from production runs:
    - quick:    ~10-15 sec/file (pre-screen only, no LLM)
    - standard: ~45-60 sec/file
    - thorough: ~85-240 sec/file depending on file type

    Args:
        files: List of file paths to validate.
        depth: Depth profile — "quick", "standard", or "thorough".

    Returns:
        TimeEstimate with mid/min/max seconds and recommended --timeout.
    """
    depth_lower = depth.lower()
    per_type: dict[str, int] = {}
    total_min = total_mid = total_max = 0

    for f in files:
        ftype = _classify_file_type(f)
        per_type[ftype] = per_type.get(ftype, 0) + 1

        if depth_lower == "thorough":
            mid = THOROUGH_SECONDS_PER_FILE[ftype]
            mn, mx = _THOROUGH_RANGE[ftype]
        else:
            mn, mid, mx = _DEPTH_SECONDS.get(depth_lower, _DEPTH_SECONDS["standard"])

        total_min += mn
        total_mid += mid
        total_max += mx

    return TimeEstimate(
        depth=depth_lower,
        files_count=len(files),
        estimated_seconds=total_mid,
        min_seconds=total_min,
        max_seconds=total_max,
        recommended_timeout=int(total_max * 1.2),
        per_type_counts=per_type,
    )
