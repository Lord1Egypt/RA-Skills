#!/usr/bin/env python3
"""Replay completed forecasts, evaluate bounded challengers, and promote or roll back profiles."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import calibrate
import forecast
import model_profile


MIN_OVERALL_SAMPLE = 100
MIN_BUCKET_SAMPLE = 30
MIN_NEW_DISTINCT_MATCHES_FOR_ROLLBACK = 30
MIN_SECONDARY_MARKET_SAMPLE = 30
MIN_RELATIVE_1X2_BRIER_IMPROVEMENT = 0.01
MAX_ELIGIBLE_BUCKET_BRIER_REGRESSION = 0.02
MAX_CALIBRATION_REGRESSION = 0.005
COORDINATE_STEP = 0.05
DEFAULT_HOLDOUT_MATCHES = 30
PROMOTION_GATE_ORDER = (
    "minimum_overall_sample",
    "minimum_bucket_sample",
    "quarantined_settlement_conflict",
    "malformed_metrics",
    "brier_improvement",
    "log_loss_regression",
    "secondary_market_regression",
    "bucket_regression",
    "calibration_regression",
)
TUNABLE_PATHS = (
    ("source_weights", "A"),
    ("source_weights", "B"),
    ("source_weights", "C"),
    ("fit_family_caps", "1x2"),
    ("fit_family_caps", "totals"),
    ("fit_family_caps", "btts"),
    ("recency_weights", "0_15"),
    ("recency_weights", "15_60"),
    ("recency_weights", "60_180"),
    ("recency_weights", "older"),
    ("confidence_thresholds", "high"),
    ("confidence_thresholds", "medium"),
    ("cross_market_conflict_penalty", None),
)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _text_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _parse_aware_timestamp(value: Any, field_name: str) -> datetime | None:
    text = _text_or_none(value)
    if text is None:
        return None
    if text.endswith(("Z", "z")):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be an ISO timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field_name} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _is_modern_record(record: dict[str, Any]) -> bool:
    return _text_or_none(record.get("event_id")) is not None or _text_or_none(record.get("forecast_id")) is not None


def _event_group_key(record: dict[str, Any], index: int) -> str:
    event_id = _text_or_none(record.get("event_id"))
    if event_id is not None:
        return event_id
    return f"legacy-{index}"


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be an object")
    return value


def _finite_metric(value: Any, field_name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be numeric")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be numeric") from exc
    if not math.isfinite(number):
        raise ValueError(f"{field_name} must be finite")
    return number


def _bounded_metric(
    value: Any,
    field_name: str,
    *,
    maximum: float | None = None,
) -> float:
    number = _finite_metric(value, field_name)
    if number < 0.0 or (maximum is not None and number > maximum):
        upper = "" if maximum is None else f" and at most {maximum:g}"
        raise ValueError(f"{field_name} must be non-negative{upper}")
    return number


def _nonnegative_int(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field_name} must be an integer")
    if value < 0:
        raise ValueError(f"{field_name} must be non-negative")
    return value


def _metric_or_none(metrics: dict[str, Any], field_name: str) -> float | None:
    if field_name not in metrics or metrics[field_name] is None:
        return None
    return _finite_metric(metrics[field_name], field_name)


def _bucket_metrics(metrics: dict[str, Any], bucket_names: list[str]) -> dict[str, float]:
    if not bucket_names:
        return {}
    raw = metrics.get("bucket_brier")
    if not isinstance(raw, dict):
        raise ValueError("bucket_brier must be an object")
    normalized: dict[str, float] = {}
    for bucket_name in bucket_names:
        if bucket_name not in raw:
            raise ValueError(f"bucket_brier.{bucket_name} is required")
        normalized[bucket_name] = _bounded_metric(
            raw[bucket_name],
            f"bucket_brier.{bucket_name}",
            maximum=2.0,
        )
    return normalized


def _normalized_metrics(metrics: Any, bucket_names: list[str]) -> dict[str, Any]:
    value = _require_mapping(metrics, "metrics")
    normalized = {
        "brier_1x2": _bounded_metric(
            value.get("brier_1x2"),
            "brier_1x2",
            maximum=2.0,
        ),
        "log_loss_1x2": _bounded_metric(
            value.get("log_loss_1x2"),
            "log_loss_1x2",
        ),
        "bucket_brier": _bucket_metrics(value, bucket_names),
    }
    for metric_name in ("totals_brier", "btts_brier"):
        count_name = metric_name.replace("_brier", "_count")
        metric_value = _metric_or_none(value, metric_name)
        if metric_value is not None and count_name not in value:
            raise ValueError(f"{count_name} is required when {metric_name} is present")
        count = _nonnegative_int(value.get(count_name, 0), count_name)
        if metric_value is None:
            if count:
                raise ValueError(f"{metric_name} is required when {count_name} is positive")
        else:
            normalized[metric_name] = _bounded_metric(
                metric_value,
                metric_name,
                maximum=2.0,
            )
        normalized[count_name] = count
    calibration_error = _metric_or_none(value, "calibration_error")
    if calibration_error is not None:
        normalized["calibration_error"] = _bounded_metric(
            calibration_error,
            "calibration_error",
            maximum=1.0,
        )
    top_pick_accuracy = _metric_or_none(value, "top_pick_accuracy")
    if top_pick_accuracy is not None:
        normalized["top_pick_accuracy"] = _bounded_metric(
            top_pick_accuracy,
            "top_pick_accuracy",
            maximum=1.0,
        )
    return normalized


def _add_gate(failed: list[str], gate: str) -> None:
    if gate not in failed:
        failed.append(gate)


def decide_promotion(sample: Any, champion: Any, challenger: Any) -> dict[str, Any]:
    failed: list[str] = []
    try:
        sample_map = _require_mapping(sample, "sample")
    except ValueError:
        return {"promote": False, "failed_gates": ["malformed_metrics"]}

    try:
        overall = _nonnegative_int(sample_map.get("overall", 0), "overall")
    except ValueError:
        overall = 0
        _add_gate(failed, "malformed_metrics")

    bucket_counts_raw = sample_map.get("affected_buckets", sample_map.get("buckets", {}))
    try:
        bucket_counts_map = _require_mapping(bucket_counts_raw, "buckets")
        bucket_counts = {}
        for bucket_name, bucket_count in bucket_counts_map.items():
            if not isinstance(bucket_name, str) or not bucket_name.strip():
                raise ValueError("bucket names must be non-empty strings")
            normalized_name = bucket_name.strip()
            if normalized_name in bucket_counts:
                raise ValueError("bucket names must be unique")
            bucket_counts[normalized_name] = _nonnegative_int(
                bucket_count,
                f"buckets.{normalized_name}",
            )
        bucket_counts = dict(sorted(bucket_counts.items()))
    except (TypeError, ValueError):
        bucket_counts = {}
        _add_gate(failed, "malformed_metrics")

    try:
        quarantined_conflicts = _nonnegative_int(sample_map.get("quarantined_conflicts", 0), "quarantined_conflicts")
    except ValueError:
        quarantined_conflicts = 0
        _add_gate(failed, "malformed_metrics")

    if overall < MIN_OVERALL_SAMPLE:
        _add_gate(failed, "minimum_overall_sample")
    if not bucket_counts or any(
        bucket_count < MIN_BUCKET_SAMPLE for bucket_count in bucket_counts.values()
    ):
        _add_gate(failed, "minimum_bucket_sample")
    if quarantined_conflicts > 0:
        _add_gate(failed, "quarantined_settlement_conflict")

    try:
        champion_metrics = _normalized_metrics(champion, list(bucket_counts))
        challenger_metrics = _normalized_metrics(challenger, list(bucket_counts))
    except ValueError:
        _add_gate(failed, "malformed_metrics")
        return {"promote": False, "failed_gates": [gate for gate in PROMOTION_GATE_ORDER if gate in failed]}

    champion_brier = champion_metrics["brier_1x2"]
    challenger_brier = challenger_metrics["brier_1x2"]
    if champion_brier <= 0.0:
        relative_improvement = math.inf if challenger_brier < champion_brier else 0.0
    else:
        relative_improvement = (champion_brier - challenger_brier) / champion_brier
    if relative_improvement < MIN_RELATIVE_1X2_BRIER_IMPROVEMENT - 1e-12:
        _add_gate(failed, "brier_improvement")
    if challenger_metrics["log_loss_1x2"] > champion_metrics["log_loss_1x2"] + 1e-12:
        _add_gate(failed, "log_loss_regression")

    secondary_regression = False
    for metric_name in ("totals_brier", "btts_brier"):
        count_name = metric_name.replace("_brier", "_count")
        champion_value = champion_metrics.get(metric_name)
        challenger_value = challenger_metrics.get(metric_name)
        champion_count = champion_metrics[count_name]
        challenger_count = challenger_metrics[count_name]
        if champion_value is None and challenger_value is None:
            continue
        if champion_value is None or challenger_value is None:
            _add_gate(failed, "malformed_metrics")
            continue
        if (
            min(champion_count, challenger_count) >= MIN_SECONDARY_MARKET_SAMPLE
            and challenger_value > champion_value + 1e-12
        ):
            secondary_regression = True
    if secondary_regression:
        _add_gate(failed, "secondary_market_regression")

    champion_calibration = champion_metrics.get("calibration_error")
    challenger_calibration = challenger_metrics.get("calibration_error")
    if champion_calibration is None or challenger_calibration is None:
        _add_gate(failed, "malformed_metrics")
    elif challenger_calibration > champion_calibration + MAX_CALIBRATION_REGRESSION + 1e-12:
        _add_gate(failed, "calibration_regression")

    for bucket_name, champion_bucket_brier in champion_metrics["bucket_brier"].items():
        challenger_bucket_brier = challenger_metrics["bucket_brier"][bucket_name]
        if champion_bucket_brier == 0.0:
            if challenger_bucket_brier > 0.0:
                _add_gate(failed, "bucket_regression")
                break
            continue
        if challenger_bucket_brier > champion_bucket_brier * (1.0 + MAX_ELIGIBLE_BUCKET_BRIER_REGRESSION) + 1e-12:
            _add_gate(failed, "bucket_regression")
            break

    return {"promote": not failed, "failed_gates": [gate for gate in PROMOTION_GATE_ORDER if gate in failed]}


def should_rollback(new_distinct_matches: Any, parent: Any, child: Any) -> bool:
    sample_size = _nonnegative_int(new_distinct_matches, "new_distinct_matches")
    parent_metrics = _normalized_metrics(parent, [])
    child_metrics = _normalized_metrics(child, [])
    return (
        sample_size >= MIN_NEW_DISTINCT_MATCHES_FOR_ROLLBACK
        and child_metrics["brier_1x2"] > parent_metrics["brier_1x2"] + 1e-12
        and child_metrics["log_loss_1x2"] > parent_metrics["log_loss_1x2"] + 1e-12
    )


def grouped_time_split(
    records: list[dict[str, Any]],
    holdout_matches: int = DEFAULT_HOLDOUT_MATCHES,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    holdout_count = _nonnegative_int(holdout_matches, "holdout_matches")
    groups: dict[str, dict[str, Any]] = {}
    for index, raw_record in enumerate(records):
        record = _require_mapping(raw_record, f"records[{index}]")
        modern = _is_modern_record(record)
        kickoff = None
        if modern:
            if _text_or_none(record.get("event_id")) is None:
                raise ValueError("modern records require event_id for grouped time split")
            kickoff = _parse_aware_timestamp(record.get("kickoff"), "kickoff")
            if kickoff is None:
                raise ValueError("kickoff is required for modern records")
        elif record.get("kickoff") is not None:
            kickoff = _parse_aware_timestamp(record.get("kickoff"), "kickoff")
        key = _event_group_key(record, index)
        group = groups.setdefault(
            key,
            {
                "event_id": key,
                "kickoff": kickoff,
                "kickoff_text": _text_or_none(record.get("kickoff")) or "",
                "first_index": index,
                "records": [],
            },
        )
        if modern and group["kickoff"] != kickoff:
            raise ValueError(f"event {key} must keep every snapshot on the same kickoff")
        as_of = None
        if record.get("as_of") is not None:
            as_of = _parse_aware_timestamp(record.get("as_of"), "as_of")
        group["records"].append((as_of, index, copy.deepcopy(record)))

    ordered_groups = sorted(
        groups.values(),
        key=lambda group: (
            group["kickoff"] is None,
            group["kickoff"].timestamp() if group["kickoff"] is not None else math.inf,
            group["kickoff_text"],
            group["event_id"],
            group["first_index"],
        ),
    )
    for group in ordered_groups:
        group["records"].sort(
            key=lambda item: (
                item[0] is None,
                item[0].timestamp() if item[0] is not None else math.inf,
                item[1],
            )
        )

    holdout_group_count = min(holdout_count, len(ordered_groups))
    holdout_groups = ordered_groups[-holdout_group_count:] if holdout_group_count else []
    train_groups = ordered_groups[:-holdout_group_count] if holdout_group_count else ordered_groups
    train = [record for group in train_groups for _, _, record in group["records"]]
    holdout = [record for group in holdout_groups for _, _, record in group["records"]]
    return train, holdout


def _candidate_profile_id(champion_profile_id: str, section: str, key: str | None, delta: float) -> str:
    material = {
        "champion": champion_profile_id,
        "section": section,
        "key": key,
        "delta": delta,
    }
    digest = hashlib.sha256(_canonical_json(material).encode("utf-8")).hexdigest()[:16]
    return f"challenger-{digest}"


def generate_coordinate_candidates(champion_profile: dict[str, Any]) -> list[dict[str, Any]]:
    champion = model_profile.validate_profile(champion_profile)
    candidates: list[dict[str, Any]] = []
    for section, key in TUNABLE_PATHS:
        current_value = champion[section] if key is None else champion[section][key]
        if current_value == 0.0:
            continue
        for delta in (-COORDINATE_STEP, COORDINATE_STEP):
            candidate = copy.deepcopy(champion)
            candidate.pop("evolution", None)
            updated_value = round(current_value * (1.0 + delta), 12)
            if key is None:
                candidate[section] = updated_value
            else:
                candidate[section][key] = updated_value
            candidate["profile_id"] = _candidate_profile_id(champion["profile_id"], section, key, delta)
            candidate["parent_id"] = champion["profile_id"]
            try:
                candidates.append(model_profile.validate_challenger(champion, candidate))
            except ValueError:
                continue
    return candidates


def load_completed_records(path: str | Path) -> list[dict[str, Any]]:
    completed_path = Path(path).expanduser()
    try:
        text = completed_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"cannot read completed records {completed_path}: {exc}") from exc
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"completed records line {line_number} is not valid JSON") from exc
        if not isinstance(value, dict):
            raise ValueError(f"completed records line {line_number} must be an object")
        records.append(value)
    return records


def _record_has_quarantined_conflict(record: dict[str, Any]) -> bool:
    reasons = {
        _text_or_none(record.get("pending_reason")),
        _text_or_none(record.get("quarantine_reason")),
        _text_or_none(record.get("review_status")),
        _text_or_none(record.get("settlement_status")),
    }
    return any(
        reason in {"source_conflict", "settlement_conflict", "quarantined"}
        for reason in reasons
        if reason is not None
    )


def _bucket_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        bucket = _text_or_none(record.get("bucket"))
        if bucket is None:
            continue
        counts[bucket] = counts.get(bucket, 0) + 1
    return dict(sorted(counts.items()))


def _calibration_error(report: dict[str, Any]) -> float | None:
    buckets = report.get("confidence_bucket_calibration")
    if not isinstance(buckets, dict) or not buckets:
        return None
    weighted_error = 0.0
    total = 0
    for label in sorted(buckets):
        metrics = _require_mapping(buckets[label], f"confidence_bucket_calibration.{label}")
        count = _nonnegative_int(metrics.get("count", 0), f"confidence_bucket_calibration.{label}.count")
        if count == 0:
            continue
        predicted = _finite_metric(
            metrics.get("top_pick_probability_mean"),
            f"confidence_bucket_calibration.{label}.top_pick_probability_mean",
        )
        actual = _finite_metric(
            metrics.get("top_pick_accuracy"),
            f"confidence_bucket_calibration.{label}.top_pick_accuracy",
        )
        weighted_error += abs(predicted - actual) * count
        total += count
    if total == 0:
        return None
    return weighted_error / total


def replay_completed_record(record: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    original = _require_mapping(record, "record")
    raw_match = _require_mapping(original.get("raw_match"), "raw_match")
    archived_input_fingerprint = _text_or_none(original.get("input_fingerprint"))
    actual_input_fingerprint = forecast.canonical_hash(raw_match)
    if archived_input_fingerprint != actual_input_fingerprint:
        raise ValueError("input_fingerprint does not match archived raw_match")
    as_of = _parse_aware_timestamp(original.get("as_of"), "as_of")
    if as_of is None:
        raise ValueError("as_of is required for replay")
    kickoff = _parse_aware_timestamp(
        original.get("kickoff", raw_match.get("kickoff")),
        "kickoff",
    )
    if kickoff is None:
        raise ValueError("kickoff is required for replay")
    if as_of >= kickoff:
        raise ValueError("as_of must be before kickoff for replay")
    analysis = forecast.analyze_v2_match(
        copy.deepcopy(raw_match),
        as_of=original.get("as_of"),
        profile=profile,
    )
    archived_event_id = _text_or_none(original.get("event_id"))
    replayed_event_id = _text_or_none(analysis["forecast_record"].get("event_id"))
    if archived_event_id is not None and archived_event_id != replayed_event_id:
        raise ValueError("event_id does not match archived raw_match")
    replayed = copy.deepcopy(original)
    replayed["source_forecast_id"] = original.get("forecast_id")
    replayed["forecast_id"] = analysis["forecast_record"]["forecast_id"]
    replayed["profile_id"] = profile["profile_id"]
    replayed["probabilities_90m"] = copy.deepcopy(analysis["probabilities_90m"])
    replayed["confidence"] = copy.deepcopy(analysis["confidence"])
    replayed["expected_goals"] = copy.deepcopy(analysis["expected_goals"])
    replayed["score_distribution"] = copy.deepcopy(analysis["forecast_record"]["score_distribution_90m"])
    if replayed.get("btts") is not None:
        replayed["btts"] = copy.deepcopy(analysis["btts"])
    if isinstance(replayed.get("totals"), list):
        totals_by_line = {
            format(float(total["line"]), "g"): {
                "line": float(total["line"]),
                "model_probabilities": copy.deepcopy(total["model_probabilities"]),
            }
            for total in analysis["totals"]
        }
        rebuilt_totals = []
        for index, original_total in enumerate(replayed["totals"]):
            total = _require_mapping(original_total, f"totals[{index}]")
            line_key = format(float(total["line"]), "g")
            if line_key not in totals_by_line:
                raise ValueError(f"replayed totals are missing line {line_key}")
            rebuilt_totals.append(totals_by_line[line_key])
        replayed["totals"] = rebuilt_totals
    return replayed


def evaluate_profile(records: list[dict[str, Any]], profile: dict[str, Any]) -> dict[str, Any]:
    replayed_records: list[dict[str, Any]] = []
    invalid_records = 0
    quarantined_conflicts = 0
    for record in records:
        if _record_has_quarantined_conflict(record):
            quarantined_conflicts += 1
            continue
        try:
            replayed = replay_completed_record(record, profile)
            validation = calibrate.build_report([replayed])
            if validation["valid_records"] != 1:
                raise ValueError("replayed completed record is invalid")
            replayed_records.append(replayed)
        except (KeyError, TypeError, ValueError):
            invalid_records += 1
    report = calibrate.build_report(replayed_records, initial_invalid_records=invalid_records)
    bucket_counts = _bucket_counts(replayed_records)
    metrics = {
        "brier_1x2": report["metrics"]["1x2"]["brier"],
        "log_loss_1x2": report["metrics"]["1x2"]["log_loss"],
        "totals_brier": report["metrics"]["totals"]["brier"] if report["metrics"]["totals"]["count"] else None,
        "totals_count": report["metrics"]["totals"]["count"],
        "btts_brier": report["metrics"]["btts"]["brier"] if report["metrics"]["btts"]["count"] else None,
        "btts_count": report["metrics"]["btts"]["count"],
        "calibration_error": _calibration_error(report),
        "top_pick_accuracy": report["metrics"]["1x2"]["top_pick_accuracy"],
        "bucket_brier": {},
    }
    for bucket_name in bucket_counts:
        bucket_records = [item for item in replayed_records if _text_or_none(item.get("bucket")) == bucket_name]
        bucket_report = calibrate.build_report(bucket_records)
        metrics["bucket_brier"][bucket_name] = bucket_report["metrics"]["1x2"]["brier"]
    return {
        "profile_id": profile["profile_id"],
        "metrics": metrics,
        "report": report,
        "replayed_records": replayed_records,
        "invalid_records": invalid_records,
        "quarantined_conflicts": quarantined_conflicts,
    }


def evaluate_evolution(completed_path: str | Path, data_dir: str | Path | None = None) -> dict[str, Any]:
    records = load_completed_records(completed_path)
    primary_records = calibrate.primary_event_records(records)
    champion_profile = model_profile.load_active_profile(data_dir)
    champion_all = evaluate_profile(primary_records, champion_profile)
    valid_primary_records = champion_all["replayed_records"]
    train_records, holdout_records = grouped_time_split(
        valid_primary_records,
        holdout_matches=DEFAULT_HOLDOUT_MATCHES,
    )
    holdout_bucket_counts = _bucket_counts(holdout_records)
    affected_buckets = {
        bucket: count
        for bucket, count in holdout_bucket_counts.items()
        if count >= MIN_BUCKET_SAMPLE
    }
    sample = {
        "overall": len(valid_primary_records),
        "buckets": _bucket_counts(valid_primary_records),
        "holdout_buckets": holdout_bucket_counts,
        "affected_buckets": affected_buckets,
        "invalid_records": champion_all["invalid_records"],
        "quarantined_conflicts": champion_all["quarantined_conflicts"],
    }
    champion_holdout = evaluate_profile(holdout_records, champion_profile)
    candidate_profiles = generate_coordinate_candidates(champion_profile)
    candidate_train_scores: list[dict[str, Any]] = []
    selected_candidate_profile = candidate_profiles[0] if candidate_profiles else champion_profile
    selected_train_brier = math.inf
    for candidate_profile in candidate_profiles:
        train_evaluation = evaluate_profile(train_records, candidate_profile)
        train_brier = train_evaluation["metrics"]["brier_1x2"]
        if train_brier is None:
            comparable_brier = math.inf
        else:
            comparable_brier = train_brier
        candidate_train_scores.append(
            {
                "profile_id": candidate_profile["profile_id"],
                "parent_id": candidate_profile["parent_id"],
                "train_brier_1x2": train_brier,
            }
        )
        if comparable_brier < selected_train_brier - 1e-12 or (
            math.isclose(comparable_brier, selected_train_brier, rel_tol=0.0, abs_tol=1e-12)
            and candidate_profile["profile_id"] < selected_candidate_profile["profile_id"]
        ):
            selected_candidate_profile = candidate_profile
            selected_train_brier = comparable_brier
    challenger_holdout = evaluate_profile(holdout_records, selected_candidate_profile)
    decision = decide_promotion(sample, champion_holdout["metrics"], challenger_holdout["metrics"])
    return {
        "sample": sample,
        "split": {
            "train_distinct_events": len(train_records),
            "holdout_distinct_events": len(holdout_records),
            "train_record_ids": [
                _record_identifier(record, index)
                for index, record in enumerate(train_records)
            ],
            "holdout_record_ids": [
                _record_identifier(record, index)
                for index, record in enumerate(holdout_records)
            ],
            "holdout_event_ids": [
                _text_or_none(record.get("event_id")) or _record_identifier(record, index)
                for index, record in enumerate(holdout_records)
            ],
            "training_cutoff": _latest_kickoff(train_records),
        },
        "candidates": candidate_train_scores,
        "evaluation": {
            "champion": champion_holdout["metrics"],
            "challenger": challenger_holdout["metrics"],
        },
        "decision": decision,
        "selected_candidate_profile": selected_candidate_profile,
    }


def _record_identifier(record: dict[str, Any], index: int) -> str:
    for field_name in ("review_id", "source_forecast_id", "event_id", "forecast_id"):
        identifier = _text_or_none(record.get(field_name))
        if identifier is not None:
            return identifier
    return f"legacy-{index}-{hashlib.sha256(_canonical_json(record).encode('utf-8')).hexdigest()[:16]}"


def _latest_kickoff(records: list[dict[str, Any]]) -> str | None:
    values = [
        parsed
        for parsed in (
            _parse_aware_timestamp(record.get("kickoff"), "kickoff")
            for record in records
        )
        if parsed is not None
    ]
    return max(values).isoformat() if values else None


def _profile_parameter_diff(
    champion: dict[str, Any],
    challenger: dict[str, Any],
) -> dict[str, dict[str, float]]:
    changes: dict[str, dict[str, float]] = {}
    for section, key in TUNABLE_PATHS:
        old = champion[section] if key is None else champion[section][key]
        new = challenger[section] if key is None else challenger[section][key]
        if not math.isclose(old, new, rel_tol=0.0, abs_tol=1e-12):
            label = section if key is None else f"{section}.{key}"
            changes[label] = {"from": old, "to": new}
    return changes


def _finalize_candidate_profile(
    report: dict[str, Any],
    champion_profile: dict[str, Any],
) -> dict[str, Any]:
    candidate = copy.deepcopy(report["selected_candidate_profile"])
    candidate.pop("evolution", None)
    if candidate.get("parent_id") != champion_profile.get("profile_id"):
        raise ValueError("selected candidate parent_id no longer matches active profile")
    created_at = datetime.now(timezone.utc).isoformat()
    evidence = {
        "training_cutoff": report.get("split", {}).get("training_cutoff"),
        "training_record_ids": report.get("split", {}).get("train_record_ids", []),
        "holdout_record_ids": report.get("split", {}).get("holdout_record_ids", []),
        "metrics": copy.deepcopy(report.get("evaluation", {})),
        "parameter_diff": _profile_parameter_diff(champion_profile, candidate),
        "promotion_decision": copy.deepcopy(report["decision"]),
    }
    fingerprint = hashlib.sha256(_canonical_json(evidence).encode("utf-8")).hexdigest()
    base_profile_id = candidate["profile_id"]
    version_digest = hashlib.sha256(
        f"{fingerprint}:{created_at}".encode("utf-8")
    ).hexdigest()[:12]
    candidate["profile_id"] = f"{base_profile_id[:114]}-{version_digest}"
    candidate["evolution"] = {
        "schema_version": model_profile.PROFILE_SCHEMA_VERSION,
        "created_at": created_at,
        **evidence,
        "evaluation_fingerprint": fingerprint,
    }
    return model_profile.validate_challenger(champion_profile, candidate)


def _atomic_write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(_canonical_json(payload) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        try:
            directory_descriptor = os.open(path.parent, os.O_RDONLY)
        except OSError:
            directory_descriptor = None
        if directory_descriptor is not None:
            try:
                os.fsync(directory_descriptor)
            finally:
                os.close(directory_descriptor)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def _write_audit_artifacts(data_dir: Path, report: dict[str, Any]) -> Path:
    audit_dir = data_dir / "evolution"
    _atomic_write_json(
        audit_dir / "candidates.json",
        {
            "candidates": report["candidates"],
            "selected_candidate_profile": report.get("selected_candidate_profile"),
        },
    )
    _atomic_write_json(
        audit_dir / "evaluation.json",
        {"sample": report.get("sample", {}), "split": report.get("split", {}), **report.get("evaluation", {})},
    )
    _atomic_write_json(audit_dir / "decision.json", report["decision"])
    return audit_dir


def execute_mode(completed_path: str | Path | None, data_dir: str | Path | None, *, mode: str) -> dict[str, Any]:
    resolved_data_dir = model_profile.resolve_data_dir(data_dir)
    if mode == "rollback":
        rolled_back_to = model_profile.rollback_profile(resolved_data_dir)
        return {"mode": mode, "rolled_back_to": rolled_back_to["profile_id"]}
    if completed_path is None:
        raise ValueError("--completed is required for evaluate and promote")
    report = evaluate_evolution(completed_path, resolved_data_dir)
    if mode == "promote" and report["decision"]["promote"]:
        champion_profile = model_profile.load_active_profile(resolved_data_dir)
        report["selected_candidate_profile"] = _finalize_candidate_profile(
            report,
            champion_profile,
        )
    _write_audit_artifacts(resolved_data_dir, report)
    if mode == "promote" and report["decision"]["promote"]:
        activated = model_profile.activate_profile(resolved_data_dir, report["selected_candidate_profile"])
        report["activation"] = {"activated_profile_id": activated["profile_id"]}
    return report


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--completed", help="Completed-review JSONL path.")
    parser.add_argument("--data-dir", help="Data directory for profiles and evolution audits.")
    parser.add_argument(
        "--mode",
        choices=("evaluate", "promote", "rollback"),
        default="evaluate",
        help="Evaluate candidates, promote a challenger, or roll back to the previous profile.",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args(argv)
    if args.mode in {"evaluate", "promote"} and not args.completed:
        parser.error("--completed is required for evaluate and promote")

    try:
        result = execute_mode(args.completed, args.data_dir, mode=args.mode)
    except (KeyError, OSError, TypeError, ValueError) as exc:
        parser.exit(2, f"{parser.prog}: error: {exc}\n")

    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
