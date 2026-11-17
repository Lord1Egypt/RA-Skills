#!/usr/bin/env python3
"""Summarize post-match calibration from completed forecast JSONL records."""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SELECTIONS_90M = ("home", "draw", "away")
SELECTIONS_BTTS = ("yes", "no")
SELECTIONS_TOTALS = ("over", "under")
CONFIDENCE_BUCKETS = ("low", "medium", "high")
LOG_CLIP = 1e-15
MINIMUM_OVERALL_SAMPLE = 100
MINIMUM_BUCKET_SAMPLE = 30


def _as_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be an object")
    return value


def _as_list(value: Any, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    return value


def _coerce_probability(value: Any, field_name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be numeric")
    try:
        probability = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be numeric") from exc
    if not math.isfinite(probability) or probability < 0.0 or probability > 1.0:
        raise ValueError(f"{field_name} must be between 0 and 1")
    return probability


def _coerce_nonnegative_number(value: Any, field_name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be numeric")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be numeric") from exc
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{field_name} must be non-negative")
    return number


def _validate_probability_map(
    value: Any,
    expected_keys: tuple[str, ...],
    field_name: str,
) -> dict[str, float]:
    probabilities = _as_mapping(value, field_name)
    keys = set(probabilities)
    expected = set(expected_keys)
    if keys != expected:
        raise ValueError(f"{field_name} must contain exactly {sorted(expected_keys)}")
    normalized: dict[str, float] = {}
    total = 0.0
    for key in expected_keys:
        probability = _coerce_probability(probabilities[key], f"{field_name}.{key}")
        normalized[key] = probability
        total += probability
    if not math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError(f"{field_name} must sum to 1")
    return normalized


def _validate_outcome(value: Any, expected_keys: tuple[str, ...], field_name: str) -> str:
    outcome = str(value).strip().lower()
    if outcome not in expected_keys:
        raise ValueError(f"{field_name} must be one of {sorted(expected_keys)}")
    return outcome


def _line_key(value: Any) -> str:
    if isinstance(value, bool):
        raise ValueError("totals line must be numeric")
    try:
        line = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("totals line must be numeric") from exc
    if not math.isfinite(line):
        raise ValueError("totals line must be finite")
    return format(line, "g")


def _score_key(value: Any, field_name: str) -> str:
    text = str(value).strip()
    home_text, separator, away_text = text.partition("-")
    if separator != "-" or not home_text.isdigit() or not away_text.isdigit():
        raise ValueError(f"{field_name} must use non-negative 'home-away' score keys")
    return f"{int(home_text)}-{int(away_text)}"


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def _text_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _top_pick(probabilities: dict[str, float]) -> str:
    return max(SELECTIONS_90M, key=lambda selection: probabilities[selection])


def _parse_timestamp(value: Any) -> datetime | None:
    text = _text_or_none(value)
    if text is None:
        return None
    if text.endswith(("Z", "z")):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(timezone.utc)


def _has_modern_identity(record: dict[str, Any]) -> bool:
    return _text_or_none(record.get("event_id")) is not None or _text_or_none(record.get("forecast_id")) is not None


def event_key(record: dict[str, Any], index: int) -> str:
    return _text_or_none(record.get("event_id")) or _text_or_none(record.get("forecast_id")) or f"legacy-{index}"


def _primary_record_priority(record: dict[str, Any], index: int) -> tuple[int, float, int]:
    as_of = _parse_timestamp(record.get("as_of"))
    kickoff = _parse_timestamp(record.get("kickoff"))
    if as_of is not None and kickoff is not None and as_of < kickoff:
        return 2, as_of.timestamp(), index
    return 0, float("-inf"), index


def _record_order_key(record: dict[str, Any], index: int) -> tuple[bool, float, str, str, int]:
    kickoff = _parse_timestamp(record.get("kickoff"))
    kickoff_text = _text_or_none(record.get("kickoff")) or ""
    return (
        kickoff is None,
        kickoff.timestamp() if kickoff is not None else math.inf,
        kickoff_text,
        event_key(record, index),
        index,
    )


def primary_event_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, tuple[tuple[int, float, int], int, dict[str, Any]]] = {}
    for index, record in enumerate(records):
        if _has_modern_identity(record) and _primary_record_priority(record, index)[0] == 0:
            continue
        key = event_key(record, index)
        candidate = (_primary_record_priority(record, index), index, record)
        current = grouped.get(key)
        if current is None or candidate[0] > current[0]:
            grouped[key] = candidate
    chosen = [(index, record) for _, index, record in grouped.values()]
    chosen.sort(key=lambda item: _record_order_key(item[1], item[0]))
    return [record for _, record in chosen]


def multiclass_brier(probabilities: dict[str, Any], outcome: str) -> float:
    normalized = _validate_probability_map(probabilities, SELECTIONS_90M, "probabilities_90m")
    resolved_outcome = _validate_outcome(outcome, SELECTIONS_90M, "outcome_90m")
    return sum((normalized[selection] - (1.0 if selection == resolved_outcome else 0.0)) ** 2 for selection in SELECTIONS_90M)


def log_loss(probabilities: dict[str, Any], outcome: str) -> float:
    normalized = _validate_probability_map(probabilities, SELECTIONS_90M, "probabilities_90m")
    resolved_outcome = _validate_outcome(outcome, SELECTIONS_90M, "outcome_90m")
    return -math.log(max(LOG_CLIP, normalized[resolved_outcome]))


def _binary_brier(probability_map: dict[str, Any], outcome: str, *, field_name: str, outcome_name: str) -> float:
    normalized = _validate_probability_map(probability_map, SELECTIONS_BTTS if "btts" in field_name else SELECTIONS_TOTALS, field_name)
    resolved_outcome = _validate_outcome(
        outcome,
        SELECTIONS_BTTS if "btts" in field_name else SELECTIONS_TOTALS,
        outcome_name,
    )
    positive_key = "yes" if "btts" in field_name else "over"
    observed = 1.0 if resolved_outcome == positive_key else 0.0
    return (normalized[positive_key] - observed) ** 2


def _validate_bucket(value: Any) -> str | None:
    if value is None:
        return None
    bucket = str(value).strip()
    return bucket or None


def _confidence_bucket(record: dict[str, Any]) -> str | None:
    explicit_label = None
    nested_label = None
    if record.get("confidence_bucket") is not None:
        explicit_label = str(record["confidence_bucket"]).strip().lower()
    if isinstance(record.get("confidence"), dict) and record["confidence"].get("label") is not None:
        nested_label = str(record["confidence"]["label"]).strip().lower()
    label = explicit_label or nested_label
    if label is None:
        return None
    if label not in CONFIDENCE_BUCKETS:
        raise ValueError("confidence bucket must be low, medium, or high")
    if nested_label is not None and nested_label not in CONFIDENCE_BUCKETS:
        raise ValueError("confidence bucket must be low, medium, or high")
    if explicit_label is not None and nested_label is not None and explicit_label != nested_label:
        raise ValueError("confidence_bucket and confidence.label must match")
    return label


def _score_errors(record: dict[str, Any]) -> tuple[float, float] | None:
    expected_goals = record.get("expected_goals")
    actual_score = record.get("actual_score")
    if expected_goals is None or actual_score is None:
        return None
    expected = _as_mapping(expected_goals, "expected_goals")
    actual = _as_mapping(actual_score, "actual_score")
    expected_home = _coerce_nonnegative_number(expected.get("home"), "expected_goals.home")
    expected_away = _coerce_nonnegative_number(expected.get("away"), "expected_goals.away")
    actual_home = _coerce_nonnegative_number(actual.get("home"), "actual_score.home")
    actual_away = _coerce_nonnegative_number(actual.get("away"), "actual_score.away")
    if actual_home != int(actual_home) or actual_away != int(actual_away):
        raise ValueError("actual_score values must be whole numbers")
    return abs(expected_home - actual_home), abs(expected_away - actual_away)


def _actual_score_key(record: dict[str, Any]) -> str | None:
    actual_score = record.get("actual_score")
    if actual_score is None:
        return None
    actual = _as_mapping(actual_score, "actual_score")
    home = _coerce_nonnegative_number(actual.get("home"), "actual_score.home")
    away = _coerce_nonnegative_number(actual.get("away"), "actual_score.away")
    if home != int(home) or away != int(away):
        raise ValueError("actual_score values must be whole numbers")
    return f"{int(home)}-{int(away)}"


def _score_distribution_metrics(record: dict[str, Any]) -> tuple[float, float] | None:
    distribution = record.get("score_distribution")
    if distribution is None:
        return None
    actual_score_key = _actual_score_key(record)
    if actual_score_key is None:
        raise ValueError("score_distribution requires actual_score")
    probabilities = _as_mapping(distribution, "score_distribution")
    normalized: dict[str, float] = {}
    total = 0.0
    for key, value in probabilities.items():
        score_key = _score_key(key, "score_distribution")
        if score_key in normalized:
            raise ValueError("score_distribution must not repeat score keys")
        probability = _coerce_probability(value, f"score_distribution.{score_key}")
        normalized[score_key] = probability
        total += probability
    if not math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError("score_distribution must sum to 1")
    support = set(normalized)
    support.add(actual_score_key)
    brier = sum((normalized.get(score_key, 0.0) - (1.0 if score_key == actual_score_key else 0.0)) ** 2 for score_key in support)
    logloss = -math.log(max(LOG_CLIP, normalized.get(actual_score_key, 0.0)))
    return brier, logloss


def _totals_briers(record: dict[str, Any]) -> list[float]:
    totals = record.get("totals")
    outcomes = record.get("outcome_totals")
    if totals is None and outcomes is None:
        return []
    if totals is None or outcomes is None:
        raise ValueError("totals and outcome_totals must appear together")
    entries = _as_list(totals, "totals")
    outcome_map = _as_mapping(outcomes, "outcome_totals")
    normalized_outcomes: dict[str, Any] = {}
    for key, value in outcome_map.items():
        normalized_key = _line_key(key)
        if normalized_key in normalized_outcomes:
            raise ValueError("outcome_totals lines must be unique after normalization")
        normalized_outcomes[normalized_key] = value
    entry_lines = [_line_key(_as_mapping(entry, f"totals[{index}]").get("line")) for index, entry in enumerate(entries)]
    if len(set(entry_lines)) != len(entry_lines):
        raise ValueError("totals lines must be unique")
    if set(entry_lines) != set(normalized_outcomes):
        raise ValueError("totals and outcome_totals lines must match exactly")
    scores: list[float] = []
    for index, entry in enumerate(entries):
        item = _as_mapping(entry, f"totals[{index}]")
        line_key = _line_key(item.get("line"))
        has_model_probabilities = "model_probabilities" in item and item.get("model_probabilities") is not None
        has_probabilities = "probabilities" in item and item.get("probabilities") is not None
        if has_model_probabilities == has_probabilities:
            raise ValueError(f"totals[{index}] must include exactly one of model_probabilities or probabilities")
        probabilities = item["model_probabilities"] if has_model_probabilities else item["probabilities"]
        scores.append(
            _binary_brier(
                probabilities,
                normalized_outcomes[line_key],
                field_name=f"totals[{index}]",
                outcome_name=f"outcome_totals[{line_key}]",
            )
        )
    return scores


def _btts_brier(record: dict[str, Any]) -> float | None:
    probabilities = record.get("btts")
    outcome = record.get("outcome_btts")
    if probabilities is None and outcome is None:
        return None
    if probabilities is None or outcome is None:
        raise ValueError("btts and outcome_btts must appear together")
    return _binary_brier(probabilities, outcome, field_name="btts", outcome_name="outcome_btts")


def _closing_movement(probabilities: dict[str, float], record: dict[str, Any]) -> float | None:
    closing = record.get("closing_consensus_90m")
    if closing is None:
        return None
    normalized = _validate_probability_map(closing, SELECTIONS_90M, "closing_consensus_90m")
    top_pick = _top_pick(probabilities)
    return abs(normalized[top_pick] - probabilities[top_pick]) * 100.0


def _analyze_record(record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError("record must be an object")

    probabilities = _validate_probability_map(record.get("probabilities_90m"), SELECTIONS_90M, "probabilities_90m")
    outcome = _validate_outcome(record.get("outcome_90m"), SELECTIONS_90M, "outcome_90m")
    one_x_two_brier = multiclass_brier(probabilities, outcome)
    one_x_two_log_loss = log_loss(probabilities, outcome)
    top_pick = _top_pick(probabilities)
    top_pick_probability = probabilities[top_pick]
    top_pick_hit = 1.0 if top_pick == outcome else 0.0

    bucket = _validate_bucket(record.get("bucket"))
    confidence_bucket = _confidence_bucket(record)
    btts_brier = _btts_brier(record)
    totals_briers = _totals_briers(record)
    score_errors = _score_errors(record)
    score_distribution_metrics = _score_distribution_metrics(record)
    closing_movement = _closing_movement(probabilities, record)

    return {
        "bucket": bucket,
        "confidence_bucket": confidence_bucket,
        "top_pick_probability": top_pick_probability,
        "top_pick_hit": top_pick_hit,
        "one_x_two_brier": one_x_two_brier,
        "one_x_two_log_loss": one_x_two_log_loss,
        "btts_brier": btts_brier,
        "totals_briers": totals_briers,
        "score_errors": score_errors,
        "score_distribution_metrics": score_distribution_metrics,
        "closing_movement": closing_movement,
    }


def load_completed_records(path: str | Path) -> tuple[list[dict[str, Any]], int]:
    records: list[dict[str, Any]] = []
    invalid_records = 0
    for line_number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            invalid_records += 1
            continue
        if not isinstance(value, dict):
            invalid_records += 1
            continue
        records.append(value)
    return records, invalid_records


def build_report(records: list[dict[str, Any]], initial_invalid_records: int = 0) -> dict[str, Any]:
    one_x_two_briers: list[float] = []
    one_x_two_log_losses: list[float] = []
    one_x_two_top_hits: list[float] = []
    btts_briers: list[float] = []
    totals_briers: list[float] = []
    closing_movements: list[float] = []
    score_mae_home: list[float] = []
    score_mae_away: list[float] = []
    score_distribution_briers: list[float] = []
    score_distribution_log_losses: list[float] = []
    confidence_buckets: dict[str, dict[str, float]] = {}
    alert_offsets: dict[str, dict[str, float]] = {}
    valid_records_for_gates: list[dict[str, Any]] = []
    invalid_records = initial_invalid_records

    for record in records:
        try:
            analysis = _analyze_record(record)
        except (TypeError, ValueError):
            invalid_records += 1
            continue

        valid_records_for_gates.append(record)
        one_x_two_briers.append(analysis["one_x_two_brier"])
        one_x_two_log_losses.append(analysis["one_x_two_log_loss"])
        one_x_two_top_hits.append(analysis["top_pick_hit"])

        confidence_bucket = analysis["confidence_bucket"]
        if confidence_bucket is not None:
            summary = confidence_buckets.setdefault(
                confidence_bucket,
                {"count": 0.0, "sum_top_pick_probability": 0.0, "sum_top_pick_hits": 0.0},
            )
            summary["count"] += 1.0
            summary["sum_top_pick_probability"] += analysis["top_pick_probability"]
            summary["sum_top_pick_hits"] += analysis["top_pick_hit"]

        alert_offset = _text_or_none(record.get("alert_offset"))
        if alert_offset is not None:
            summary = alert_offsets.setdefault(
                alert_offset,
                {
                    "count": 0.0,
                    "sum_brier": 0.0,
                    "sum_log_loss": 0.0,
                    "sum_top_pick_hits": 0.0,
                },
            )
            summary["count"] += 1.0
            summary["sum_brier"] += analysis["one_x_two_brier"]
            summary["sum_log_loss"] += analysis["one_x_two_log_loss"]
            summary["sum_top_pick_hits"] += analysis["top_pick_hit"]

        if analysis["btts_brier"] is not None:
            btts_briers.append(analysis["btts_brier"])

        totals_briers.extend(analysis["totals_briers"])

        if analysis["score_errors"] is not None:
            score_mae_home.append(analysis["score_errors"][0])
            score_mae_away.append(analysis["score_errors"][1])

        if analysis["score_distribution_metrics"] is not None:
            score_distribution_briers.append(analysis["score_distribution_metrics"][0])
            score_distribution_log_losses.append(analysis["score_distribution_metrics"][1])

        if analysis["closing_movement"] is not None:
            closing_movements.append(analysis["closing_movement"])

    valid_records = len(one_x_two_briers)
    distinct_records = primary_event_records(valid_records_for_gates)
    distinct_matches = len(distinct_records)
    excluded_valid_records_from_distinct_gates = valid_records - distinct_matches
    bucket_samples: dict[str, int] = {}
    bucket_missing_records = 0
    for index, record in enumerate(distinct_records):
        bucket = _validate_bucket(record.get("bucket"))
        if bucket is None:
            bucket_missing_records += 1
        else:
            bucket_samples[bucket] = bucket_samples.get(bucket, 0) + 1

    overall_eligible = distinct_matches >= MINIMUM_OVERALL_SAMPLE
    bucket_weight_change_eligibility = {
        bucket: overall_eligible and count >= MINIMUM_BUCKET_SAMPLE
        for bucket, count in sorted(bucket_samples.items())
    }
    eligible_buckets = [bucket for bucket, eligible in bucket_weight_change_eligibility.items() if eligible]
    weight_change_eligible = bool(eligible_buckets)

    confidence_bucket_report: dict[str, dict[str, float | int]] = {}
    for label in sorted(confidence_buckets):
        summary = confidence_buckets[label]
        count = int(summary["count"])
        confidence_bucket_report[label] = {
            "count": count,
            "top_pick_probability_mean": summary["sum_top_pick_probability"] / count,
            "top_pick_accuracy": summary["sum_top_pick_hits"] / count,
        }

    alert_offset_report: dict[str, dict[str, float | int]] = {}
    for label in sorted(alert_offsets):
        summary = alert_offsets[label]
        count = int(summary["count"])
        alert_offset_report[label] = {
            "count": count,
            "brier": summary["sum_brier"] / count,
            "log_loss": summary["sum_log_loss"] / count,
            "top_pick_accuracy": summary["sum_top_pick_hits"] / count,
        }

    score_mae = None
    if score_mae_home:
        home_mae = _mean(score_mae_home)
        away_mae = _mean(score_mae_away)
        score_mae = {
            "count": len(score_mae_home),
            "home": home_mae,
            "away": away_mae,
            "total": None if home_mae is None or away_mae is None else (home_mae + away_mae) / 2.0,
        }

    closing_consensus_movement = None
    if closing_movements:
        closing_consensus_movement = {
            "count": len(closing_movements),
            "mean_absolute_delta_pp": _mean(closing_movements),
        }

    return {
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "distinct_matches": distinct_matches,
        "minimum_overall_sample": MINIMUM_OVERALL_SAMPLE,
        "minimum_bucket_sample": MINIMUM_BUCKET_SAMPLE,
        "weight_change_eligible": weight_change_eligible,
        "sample_eligibility": {
            "valid_records": valid_records,
            "distinct_matches": distinct_matches,
            "excluded_valid_records_from_distinct_gates": excluded_valid_records_from_distinct_gates,
            "bucket_samples": dict(sorted(bucket_samples.items())),
            "bucket_weight_change_eligibility": bucket_weight_change_eligibility,
            "eligible_buckets": eligible_buckets,
            "bucket_missing_records": bucket_missing_records,
            "minimum_overall_sample": MINIMUM_OVERALL_SAMPLE,
            "minimum_bucket_sample": MINIMUM_BUCKET_SAMPLE,
            "weight_change_eligible": weight_change_eligible,
        },
        "metrics": {
            "1x2": {
                "count": len(one_x_two_briers),
                "brier": _mean(one_x_two_briers),
                "log_loss": _mean(one_x_two_log_losses),
                "top_pick_accuracy": _mean(one_x_two_top_hits),
            },
            "totals": {
                "count": len(totals_briers),
                "brier": _mean(totals_briers),
            },
            "btts": {
                "count": len(btts_briers),
                "brier": _mean(btts_briers),
            },
            "score_distribution": {
                "count": len(score_distribution_briers),
                "brier": _mean(score_distribution_briers),
                "log_loss": _mean(score_distribution_log_losses),
            },
        },
        "alert_offset_diagnostics": alert_offset_report,
        "confidence_bucket_calibration": confidence_bucket_report,
        "score_mae": score_mae,
        "closing_consensus_movement": closing_consensus_movement,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Completed forecast JSONL file.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args()

    try:
        records, invalid_records = load_completed_records(args.input)
    except (OSError, UnicodeDecodeError) as exc:
        parser.error(str(exc))
    report = build_report(records, initial_invalid_records=invalid_records)
    if args.pretty:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
