# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
CSV audit report generation for Quorum validation runs.

Generates two CSV files per run:
- audit-detail.csv: one row per validated file with per-file metrics
- audit-summary.csv: single row with run-level aggregates
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from quorum.cost import CostTracker
    from quorum.models import FileResult

logger = logging.getLogger(__name__)

# CSV column definitions
DETAIL_COLUMNS = [
    "filename",
    "sha256",
    "file_size_bytes",
    "file_token_estimate",
    "analysis_start",
    "analysis_end",
    "duration_seconds",
    "input_tokens",
    "output_tokens",
    "tokens_per_second",
    "models_used",
    "verdict",
    "finding_count",
    "cost_usd",
]

SUMMARY_COLUMNS = [
    "total_files",
    "total_size_bytes",
    "total_token_estimate",
    "run_start",
    "run_end",
    "run_duration_seconds",
    "total_input_tokens",
    "total_output_tokens",
    "avg_tokens_per_second",
    "median_tokens_per_second",
    "total_critic_calls",
    "models_used",
    "total_cost_usd",
    "cost_by_model",
    "pass_count",
    "fail_count",
]

# Verdict statuses that are considered "passing"
_PASSING_STATUSES = {"PASS", "PASS_WITH_NOTES"}


def _read_run_dir(run_dir: Path) -> dict[str, Any]:
    """Read artifact, manifest, and verdict from a run directory."""
    artifact_text = ""
    artifact_path = run_dir / "artifact.txt"
    if artifact_path.exists():
        try:
            artifact_text = artifact_path.read_text(encoding="utf-8")
        except OSError:
            pass

    manifest: dict[str, Any] = {}
    manifest_path = run_dir / "run-manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass

    verdict_data: dict[str, Any] = {}
    verdict_path = run_dir / "verdict.json"
    if verdict_path.exists():
        try:
            verdict_data = json.loads(verdict_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass

    return {
        "artifact_text": artifact_text,
        "manifest": manifest,
        "verdict_data": verdict_data,
    }


def _parse_duration(start_str: str, end_str: str) -> float:
    """Parse ISO timestamps and return duration in seconds (>=0)."""
    if not start_str or not end_str:
        return 0.0
    try:
        start_dt = datetime.fromisoformat(start_str)
        end_dt = datetime.fromisoformat(end_str)
        return max(0.0, (end_dt - start_dt).total_seconds())
    except (ValueError, TypeError):
        return 0.0


def _build_detail_row(
    run_dir: Path,
    file_path_str: str,
    all_records: list,
) -> dict[str, Any]:
    """Build a single audit-detail.csv row from a run directory."""
    data = _read_run_dir(run_dir)
    artifact_text = data["artifact_text"]
    manifest = data["manifest"]
    verdict_data = data["verdict_data"]

    # File metrics
    artifact_bytes = artifact_text.encode("utf-8")
    sha256 = hashlib.sha256(artifact_bytes).hexdigest()
    file_size_bytes = len(artifact_bytes)
    file_token_estimate = len(artifact_text) // 4

    # Timing from manifest (written by pipeline at start/end of run)
    analysis_start = manifest.get("started_at", "")
    analysis_end = manifest.get("completed_at", "")
    duration_seconds = _parse_duration(analysis_start, analysis_end)

    # Token/cost data from records attributed to this file
    file_records = [r for r in all_records if r.file_path == file_path_str]
    input_tokens = sum(r.prompt_tokens for r in file_records)
    output_tokens = sum(r.completion_tokens for r in file_records)
    cost_usd = sum(r.cost_usd for r in file_records)

    # Models used for this file (sorted for determinism)
    models_used_list = sorted(set(r.model for r in file_records))

    # Tokens per second (output tokens / duration)
    tokens_per_second = output_tokens / duration_seconds if duration_seconds > 0 else 0.0

    # Verdict and findings
    verdict_status = verdict_data.get("status", "UNKNOWN")
    report = verdict_data.get("report") or {}
    findings = report.get("findings") or []
    finding_count = len(findings)

    return {
        "filename": file_path_str,
        "sha256": sha256,
        "file_size_bytes": file_size_bytes,
        "file_token_estimate": file_token_estimate,
        "analysis_start": analysis_start,
        "analysis_end": analysis_end,
        "duration_seconds": round(duration_seconds, 3),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "tokens_per_second": round(tokens_per_second, 3),
        "models_used": ",".join(models_used_list),
        "verdict": verdict_status,
        "finding_count": finding_count,
        "cost_usd": round(cost_usd, 6),
    }


def _build_summary_row(
    detail_rows: list[dict[str, Any]],
    all_records: list,
    run_start: datetime,
    run_end: datetime,
) -> dict[str, Any]:
    """Build the audit-summary.csv row from detail rows and cost records."""
    total_files = len(detail_rows)
    total_size_bytes = sum(r["file_size_bytes"] for r in detail_rows)
    total_token_estimate = sum(r["file_token_estimate"] for r in detail_rows)
    total_input_tokens = sum(r["input_tokens"] for r in detail_rows)
    total_output_tokens = sum(r["output_tokens"] for r in detail_rows)
    total_cost_usd = sum(r["cost_usd"] for r in detail_rows)
    total_critic_calls = len(all_records)

    # Run timing
    run_start_str = run_start.isoformat()
    run_end_str = run_end.isoformat()
    run_duration_seconds = max(0.0, (run_end - run_start).total_seconds())

    # Tokens per second stats (only for files with positive tps)
    tps_values = [r["tokens_per_second"] for r in detail_rows if r["tokens_per_second"] > 0]
    avg_tps = sum(tps_values) / len(tps_values) if tps_values else 0.0
    median_tps = statistics.median(tps_values) if tps_values else 0.0

    # All unique models used across the run
    all_models = sorted(set(r.model for r in all_records))

    # Cost aggregated by model
    cost_by_model: dict[str, float] = {}
    for rec in all_records:
        cost_by_model[rec.model] = round(
            cost_by_model.get(rec.model, 0.0) + rec.cost_usd, 6
        )

    # Pass/fail counts
    pass_count = sum(1 for r in detail_rows if r["verdict"] in _PASSING_STATUSES)
    fail_count = total_files - pass_count

    return {
        "total_files": total_files,
        "total_size_bytes": total_size_bytes,
        "total_token_estimate": total_token_estimate,
        "run_start": run_start_str,
        "run_end": run_end_str,
        "run_duration_seconds": round(run_duration_seconds, 3),
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "avg_tokens_per_second": round(avg_tps, 3),
        "median_tokens_per_second": round(median_tps, 3),
        "total_critic_calls": total_critic_calls,
        "models_used": ",".join(all_models),
        "total_cost_usd": round(total_cost_usd, 6),
        "cost_by_model": json.dumps(cost_by_model),
        "pass_count": pass_count,
        "fail_count": fail_count,
    }


def _write_detail_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write audit-detail.csv with header and one row per file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=DETAIL_COLUMNS,
            quoting=csv.QUOTE_MINIMAL,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)


def _write_summary_csv(path: Path, row: dict[str, Any]) -> None:
    """Write audit-summary.csv with header and single data row."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=SUMMARY_COLUMNS,
            quoting=csv.QUOTE_MINIMAL,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerow(row)


def generate_audit_reports(
    run_dir: Path,
    file_path: str,
    cost_tracker: "CostTracker",
    run_start: datetime,
    run_end: datetime,
) -> tuple[Path, Path]:
    """
    Generate audit-detail.csv and audit-summary.csv for a single-file run.

    Args:
        run_dir:      Path to the per-file run output directory.
        file_path:    Absolute/relative path to the validated file (for cost lookup).
        cost_tracker: CostTracker instance from the validation run.
        run_start:    When the run started (UTC-aware datetime).
        run_end:      When the run ended (UTC-aware datetime).

    Returns:
        (detail_csv_path, summary_csv_path)
    """
    summary = cost_tracker.summary()
    all_records = summary.records

    detail_row = _build_detail_row(run_dir, file_path, all_records)
    detail_rows = [detail_row]
    summary_row = _build_summary_row(detail_rows, all_records, run_start, run_end)

    detail_path = run_dir / "audit-detail.csv"
    summary_path = run_dir / "audit-summary.csv"

    _write_detail_csv(detail_path, detail_rows)
    _write_summary_csv(summary_path, summary_row)

    logger.info("Audit reports written: %s, %s", detail_path, summary_path)
    return detail_path, summary_path


def generate_batch_audit_reports(
    batch_dir: Path,
    file_results: list["FileResult"],
    cost_tracker: "CostTracker",
    run_start: datetime,
    run_end: datetime,
) -> tuple[Path, Path]:
    """
    Generate audit-detail.csv and audit-summary.csv for a batch run.

    Args:
        batch_dir:    Path to the batch run output directory.
        file_results: List of FileResult objects from the batch run.
        cost_tracker: Shared CostTracker instance from the batch run.
        run_start:    When the batch started (UTC-aware datetime).
        run_end:      When the batch ended (UTC-aware datetime).

    Returns:
        (detail_csv_path, summary_csv_path)
    """
    summary = cost_tracker.summary()
    all_records = summary.records

    detail_rows = []
    for result in file_results:
        run_dir = Path(result.run_dir)
        row = _build_detail_row(run_dir, result.file_path, all_records)
        detail_rows.append(row)

    summary_row = _build_summary_row(detail_rows, all_records, run_start, run_end)

    detail_path = batch_dir / "audit-detail.csv"
    summary_path = batch_dir / "audit-summary.csv"

    _write_detail_csv(detail_path, detail_rows)
    _write_summary_csv(summary_path, summary_row)

    logger.info("Batch audit reports written: %s, %s", detail_path, summary_path)
    return detail_path, summary_path
