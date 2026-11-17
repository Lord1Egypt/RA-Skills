#!/usr/bin/env python3
"""Validate final football results and settle archived forecast markets."""

from __future__ import annotations

import argparse
import copy
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

import forecast
import model_profile


RESULT_SCHEMA_VERSION = "1.0"
FINAL_STATUS = "final"
PENDING_STATUSES = {"postponed", "abandoned", "suspended"}
CAUSE_TEXT = {
    "zh": {
        "settlement_scope_error": "历史结算使用了错误的比赛周期或比分",
        "closing_market_moved_against_forecast": "临场收盘共识明显背离赛前所选方向",
        "high_impact_match_event": "已核实且被明确标记为改变比赛状态的高影响事件",
        "late_information_missed": "预测后、开赛前出现了已核实的重要阵容或伤停信息",
        "cross_market_conflict_underweighted": "赛前已记录跨盘口冲突，但置信度仍然偏高",
        "overconfidence": "历史校准显示该置信度分桶存在高估",
        "repeated_model_bias_candidate": "相同方向误差已达到重复偏差候选条件",
        "evidence_unavailable": "至少一条提供的相关证据无法验证，或缺少证明因果关系所需的字段",
        "probabilistic_miss": "较低概率结果发生，未发现足以证明模型缺陷的证据",
    },
    "en": {
        "settlement_scope_error": "A prior settlement used the wrong match period or score",
        "closing_market_moved_against_forecast": "The closing consensus moved materially against the selected direction",
        "high_impact_match_event": "A verified event was explicitly documented as materially changing match state",
        "late_information_missed": "Verified lineup or availability information appeared after the forecast and before kickoff",
        "cross_market_conflict_underweighted": "A recorded cross-market conflict was paired with excessive confidence",
        "overconfidence": "Historical calibration shows overconfidence in this bucket",
        "repeated_model_bias_candidate": "The same directional error meets the repeated-bias candidate rule",
        "evidence_unavailable": "At least one supplied event is unverifiable or lacks fields needed to establish causation",
        "probabilistic_miss": "A lower-probability outcome occurred without evidence of a model defect",
    },
}


def _mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be an object")
    return value


def _nonempty_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _timezone_timestamp(value: Any, field_name: str) -> str:
    text = _nonempty_text(value, field_name)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field_name} must be an ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field_name} must include a timezone")
    return parsed.isoformat()


def _score(value: Any, field_name: str) -> dict[str, int]:
    score = _mapping(value, field_name)
    if set(score) != {"home", "away"}:
        raise ValueError(f"{field_name} must contain exactly home and away")
    normalized = {}
    for side in ("home", "away"):
        goals = score[side]
        if isinstance(goals, bool) or not isinstance(goals, (int, float)):
            raise ValueError(f"{field_name}.{side} must be a non-negative whole number")
        if not math.isfinite(float(goals)) or goals < 0 or int(goals) != goals:
            raise ValueError(f"{field_name}.{side} must be a non-negative whole number")
        normalized[side] = int(goals)
    return normalized


def _validate_sources(
    value: Any,
    *,
    score_90m: dict[str, int] | None,
    final: bool,
) -> tuple[list[dict[str, Any]], str]:
    if not final and (value is None or value == ()):
        return [], "pending"
    if not isinstance(value, list) or not value:
        raise ValueError("result sources must be a non-empty list")
    sources = []
    score_conflict = False
    for index, raw_source in enumerate(value):
        source = _mapping(raw_source, f"sources[{index}]")
        normalized = copy.deepcopy(source)
        normalized["name"] = _nonempty_text(source.get("name"), f"sources[{index}].name")
        if type(source.get("official")) is not bool:
            raise ValueError(f"sources[{index}].official must be a bool")
        normalized["official"] = source["official"]
        normalized["observed_at"] = _timezone_timestamp(
            source.get("observed_at"),
            f"sources[{index}].observed_at",
        )
        if not str(source.get("url", "")).strip() and not str(source.get("identifier", "")).strip():
            raise ValueError(f"sources[{index}] requires url or identifier")
        if source.get("score_90m") is not None:
            normalized["score_90m"] = _score(source["score_90m"], f"sources[{index}].score_90m")
            if score_90m is not None and normalized["score_90m"] != score_90m:
                score_conflict = True
        sources.append(normalized)

    if final and not any(source["official"] for source in sources):
        for index, source in enumerate(sources):
            if source.get("reputable") is not True:
                raise ValueError(f"sources[{index}] must explicitly be reputable")
            source["independent_id"] = _nonempty_text(
                source.get("independent_id"),
                f"sources[{index}].independent_id",
            )
            if source.get("score_90m") is None:
                raise ValueError(f"sources[{index}].score_90m is required")
        independent_ids = {source["independent_id"].casefold() for source in sources}
        if len(independent_ids) < 2:
            raise ValueError("final result requires an official source or two independent sources")
    return sources, "conflict" if score_conflict else "verified"


def validate_result(result: dict[str, Any]) -> dict[str, Any]:
    value = _mapping(result, "result")
    event_id = _nonempty_text(value.get("event_id"), "event_id")
    status = _nonempty_text(value.get("status"), "status").lower()
    if status not in {FINAL_STATUS, *PENDING_STATUSES}:
        raise ValueError(f"unsupported result status: {status}")
    schema_version = value.get("schema_version")
    if schema_version is None and status in PENDING_STATUSES:
        schema_version = RESULT_SCHEMA_VERSION
    if schema_version != RESULT_SCHEMA_VERSION:
        raise ValueError("unsupported result schema_version")

    normalized = copy.deepcopy(value)
    normalized["schema_version"] = schema_version
    normalized["event_id"] = event_id
    normalized["status"] = status
    if status in PENDING_STATUSES:
        normalized["sources"], _ = _validate_sources(
            value.get("sources"),
            score_90m=None,
            final=False,
        )
        normalized["settlement_status"] = "pending"
        return normalized

    score_90m = _score(value.get("score_90m"), "score_90m")
    normalized["score_90m"] = score_90m
    if value.get("score_after_extra_time") is not None:
        extra_time_score = _score(value["score_after_extra_time"], "score_after_extra_time")
        if any(extra_time_score[side] < score_90m[side] for side in ("home", "away")):
            raise ValueError("extra-time score cannot decrease from score_90m")
        normalized["score_after_extra_time"] = extra_time_score
    if value.get("penalty_score") is not None:
        normalized["penalty_score"] = _score(value["penalty_score"], "penalty_score")
    if value.get("qualified") is not None:
        normalized["qualified"] = _nonempty_text(value["qualified"], "qualified")
    normalized["sources"], source_status = _validate_sources(
        value.get("sources"),
        score_90m=score_90m,
        final=True,
    )
    if source_status == "conflict":
        normalized["settlement_status"] = "pending"
        normalized["pending_reason"] = "source_conflict"
        return normalized
    normalized["settlement_status"] = "ready"
    return normalized


def _quarter_line(value: Any, field_name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be numeric")
    try:
        line = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be numeric") from exc
    if not math.isfinite(line) or not math.isclose(line * 4.0, round(line * 4.0), abs_tol=1e-9):
        raise ValueError(f"{field_name} must be a finite quarter line")
    return line


def split_quarter_line(line: float) -> tuple[float, ...]:
    resolved = _quarter_line(line, "line")
    doubled = resolved * 2.0
    if math.isclose(doubled, round(doubled), abs_tol=1e-9):
        return (resolved,)
    lower = math.floor(doubled) / 2.0
    return (lower, lower + 0.5)


def _single_verdict(edge: float) -> str:
    if edge > 1e-12:
        return "win"
    if edge < -1e-12:
        return "loss"
    return "push"


def _combine_verdicts(verdicts: tuple[str, ...]) -> str:
    if len(verdicts) == 1 or len(set(verdicts)) == 1:
        return verdicts[0]
    pair = frozenset(verdicts)
    if pair == {"win", "push"}:
        return "half_win"
    if pair == {"loss", "push"}:
        return "half_loss"
    if pair == {"win", "loss"}:
        return "push"
    raise ValueError(f"unsupported split settlement: {verdicts}")


def settle_total(selection: str, line: float, home_goals: int, away_goals: int) -> str:
    side = str(selection).strip().lower()
    if side not in {"over", "under"}:
        raise ValueError("total selection must be over or under")
    score = _score({"home": home_goals, "away": away_goals}, "score")
    total_goals = score["home"] + score["away"]
    verdicts = []
    for half_line in split_quarter_line(line):
        edge = total_goals - half_line if side == "over" else half_line - total_goals
        verdicts.append(_single_verdict(edge))
    return _combine_verdicts(tuple(verdicts))


def settle_handicap(selection: str, line: float, home_goals: int, away_goals: int) -> str:
    side = str(selection).strip().lower()
    if side not in {"home", "away"}:
        raise ValueError("handicap selection must be home or away")
    score = _score({"home": home_goals, "away": away_goals}, "score")
    goal_difference = (
        score["home"] - score["away"]
        if side == "home"
        else score["away"] - score["home"]
    )
    verdicts = tuple(
        _single_verdict(goal_difference + half_line)
        for half_line in split_quarter_line(line)
    )
    return _combine_verdicts(verdicts)


def _require_period(market: dict[str, Any], expected: str, field_name: str) -> None:
    if str(market.get("period", "")).strip().lower() != expected:
        raise ValueError(f"{field_name} period must be {expected}")


def _pick_verdict(pick: Any, verdicts: dict[str, str], field_name: str) -> str | None:
    if pick is None:
        return None
    normalized = str(pick).strip()
    if normalized not in verdicts:
        raise ValueError(f"{field_name} pick is not a valid selection")
    return verdicts[normalized]


def _total_outcome(verdicts: dict[str, str]) -> str:
    positive = {"win", "half_win"}
    if verdicts["over"] in positive:
        return "over"
    if verdicts["under"] in positive:
        return "under"
    if verdicts["over"] == verdicts["under"] == "push":
        return "push"
    raise ValueError(f"incoherent total settlement: {verdicts}")


def _score_key(value: Any, field_name: str) -> str:
    text = _nonempty_text(value, field_name)
    home_text, separator, away_text = text.partition("-")
    if separator != "-" or not home_text.isdigit() or not away_text.isdigit():
        raise ValueError(f"{field_name} must use non-negative home-away format")
    return f"{int(home_text)}-{int(away_text)}"


def settle_forecast(
    forecast_record: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    record = _mapping(forecast_record, "forecast_record")
    event_id = _nonempty_text(record.get("event_id"), "forecast_record.event_id")
    settled_result = validate_result(result)
    if event_id != settled_result["event_id"]:
        raise ValueError("forecast and result event_id must match")
    if settled_result["settlement_status"] != "ready":
        return {
            "schema_version": "1.0",
            "forecast_id": record.get("forecast_id"),
            "event_id": event_id,
            "settlement_status": "pending",
            "result_status": settled_result["status"],
            "pending_reason": settled_result.get("pending_reason", settled_result["status"]),
        }

    teams = record.get("teams")
    if not isinstance(teams, list) or len(teams) != 2 or any(not str(team).strip() for team in teams):
        raise ValueError("forecast_record.teams must contain two teams")
    teams = [str(team).strip() for team in teams]
    score_90m = settled_result["score_90m"]
    if score_90m["home"] > score_90m["away"]:
        outcome_90m = "home"
    elif score_90m["home"] < score_90m["away"]:
        outcome_90m = "away"
    else:
        outcome_90m = "draw"

    markets = _mapping(record.get("markets"), "forecast_record.markets")
    one_x_two = _mapping(markets.get("1x2"), "1x2")
    _require_period(one_x_two, "90m", "1x2")
    one_x_two_verdicts = {
        selection: "win" if selection == outcome_90m else "loss"
        for selection in ("home", "draw", "away")
    }

    totals_output = {}
    totals = markets.get("totals", [])
    if not isinstance(totals, list):
        raise ValueError("totals must be a list")
    for index, total in enumerate(totals):
        item = _mapping(total, f"totals[{index}]")
        _require_period(item, "90m", f"totals[{index}]")
        line = _quarter_line(item.get("line"), f"totals[{index}].line")
        line_key = format(line, "g")
        if line_key in totals_output:
            raise ValueError(f"duplicate totals line {line_key}")
        verdicts = {
            selection: settle_total(
                selection,
                line,
                score_90m["home"],
                score_90m["away"],
            )
            for selection in ("over", "under")
        }
        totals_output[line_key] = {
            "period": "90m",
            "line": line,
            "score_used": dict(score_90m),
            "outcome": _total_outcome(verdicts),
            "verdicts": verdicts,
            "pick": item.get("pick"),
            "pick_verdict": _pick_verdict(item.get("pick"), verdicts, f"totals[{index}]"),
        }

    btts = _mapping(markets.get("btts"), "btts")
    _require_period(btts, "90m", "btts")
    btts_outcome = "yes" if score_90m["home"] > 0 and score_90m["away"] > 0 else "no"
    btts_verdicts = {
        selection: "win" if selection == btts_outcome else "loss"
        for selection in ("yes", "no")
    }

    handicap_output = {}
    handicaps = markets.get("asian_handicap", [])
    if not isinstance(handicaps, list):
        raise ValueError("asian_handicap must be a list")
    for index, handicap in enumerate(handicaps):
        item = _mapping(handicap, f"asian_handicap[{index}]")
        _require_period(item, "90m", f"asian_handicap[{index}]")
        home_line = _quarter_line(item.get("home_line"), f"asian_handicap[{index}].home_line")
        away_line = _quarter_line(item.get("away_line"), f"asian_handicap[{index}].away_line")
        if not math.isclose(home_line, -away_line, abs_tol=1e-9):
            raise ValueError("asian handicap lines must be mirrored")
        key = f"home{home_line:+g}"
        if key in handicap_output:
            raise ValueError(f"duplicate asian handicap line {key}")
        verdicts = {
            "home": settle_handicap("home", home_line, score_90m["home"], score_90m["away"]),
            "away": settle_handicap("away", away_line, score_90m["home"], score_90m["away"]),
        }
        handicap_output[key] = {
            "period": "90m",
            "home_line": home_line,
            "away_line": away_line,
            "score_used": dict(score_90m),
            "verdicts": verdicts,
            "pick": item.get("pick"),
            "pick_verdict": _pick_verdict(item.get("pick"), verdicts, f"asian_handicap[{index}]"),
        }

    correct_score = _mapping(markets.get("correct_score"), "correct_score")
    _require_period(correct_score, "90m", "correct_score")
    actual_score = f"{score_90m['home']}-{score_90m['away']}"
    displayed = correct_score.get("displayed", [])
    if not isinstance(displayed, list):
        raise ValueError("correct_score.displayed must be a list")
    displayed_verdicts = {}
    for index, raw_item in enumerate(displayed):
        item = _mapping(raw_item, f"correct_score.displayed[{index}]")
        score_key = _score_key(
            item.get("score"),
            f"correct_score.displayed[{index}].score",
        )
        if score_key in displayed_verdicts:
            raise ValueError(f"duplicate correct score {score_key}")
        displayed_verdicts[score_key] = "win" if score_key == actual_score else "loss"

    qualification_output = None
    qualification = markets.get("qualification")
    if qualification is not None:
        qualification = _mapping(qualification, "qualification")
        _require_period(qualification, "qualification", "qualification")
        qualified = _nonempty_text(settled_result.get("qualified"), "qualified")
        if qualified not in teams:
            raise ValueError("qualified team must match a forecast team")
        verdicts = {team: "win" if team == qualified else "loss" for team in teams}
        pick = qualification.get("favorite")
        qualification_output = {
            "period": "qualification",
            "score_used": None,
            "qualified": qualified,
            "verdicts": verdicts,
            "pick": pick,
            "pick_verdict": _pick_verdict(pick, verdicts, "qualification"),
        }

    return {
        "schema_version": "1.0",
        "forecast_id": record.get("forecast_id"),
        "event_id": event_id,
        "settlement_status": "settled",
        "result_timeline": {
            "score_90m": dict(score_90m),
            "score_after_extra_time": settled_result.get("score_after_extra_time"),
            "penalty_score": settled_result.get("penalty_score"),
            "qualified": settled_result.get("qualified"),
        },
        "1x2": {
            "period": "90m",
            "score_used": dict(score_90m),
            "outcome": outcome_90m,
            "verdicts": one_x_two_verdicts,
            "pick": one_x_two.get("pick"),
            "pick_verdict": _pick_verdict(one_x_two.get("pick"), one_x_two_verdicts, "1x2"),
        },
        "totals": totals_output,
        "btts": {
            "period": "90m",
            "score_used": dict(score_90m),
            "outcome": btts_outcome,
            "verdicts": btts_verdicts,
            "pick": btts.get("pick"),
            "pick_verdict": _pick_verdict(btts.get("pick"), btts_verdicts, "btts"),
        },
        "asian_handicap": handicap_output,
        "correct_score": {
            "period": "90m",
            "score_used": dict(score_90m),
            "outcome": actual_score,
            "displayed_verdicts": displayed_verdicts,
        },
        "qualification": qualification_output,
    }


def _probability_map(
    value: Any,
    keys: tuple[str, ...],
    field_name: str,
) -> dict[str, float]:
    probabilities = _mapping(value, field_name)
    if set(probabilities) != set(keys):
        raise ValueError(f"{field_name} must contain exactly {sorted(keys)}")
    normalized = {}
    for key in keys:
        probability = probabilities[key]
        if isinstance(probability, bool) or not isinstance(probability, (int, float)):
            raise ValueError(f"{field_name}.{key} must be a probability")
        probability = float(probability)
        if not math.isfinite(probability) or not 0.0 <= probability <= 1.0:
            raise ValueError(f"{field_name}.{key} must be between 0 and 1")
        normalized[key] = probability
    if not math.isclose(sum(normalized.values()), 1.0, abs_tol=1e-9):
        raise ValueError(f"{field_name} must sum to 1")
    return normalized


def _multiclass_brier(probabilities: dict[str, float], outcome: str) -> float:
    return sum(
        (probability - (1.0 if selection == outcome else 0.0)) ** 2
        for selection, probability in probabilities.items()
    )


def _log_loss(probabilities: dict[str, float], outcome: str) -> float:
    return -math.log(max(1e-15, probabilities[outcome]))


def _binary_brier(probability: float, observed: bool) -> float:
    return (probability - (1.0 if observed else 0.0)) ** 2


def _verified_event(event: Any) -> bool:
    return (
        isinstance(event, dict)
        and event.get("verified") is True
        and isinstance(event.get("source"), str)
        and bool(event["source"].strip())
    )


def _event_between_forecast_and_kickoff(
    event: dict[str, Any],
    forecast_record: dict[str, Any],
) -> bool:
    observed_at = event.get("observed_at")
    if observed_at is None:
        return False
    try:
        observed = datetime.fromisoformat(str(observed_at).replace("Z", "+00:00"))
        forecast_time = datetime.fromisoformat(str(forecast_record.get("as_of")).replace("Z", "+00:00"))
        kickoff = datetime.fromisoformat(str(forecast_record.get("kickoff")).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return False
    if observed.tzinfo is None or forecast_time.tzinfo is None or kickoff.tzinfo is None:
        return False
    return forecast_time < observed < kickoff


def _event_evidence_unavailable(
    event: dict[str, Any],
    high_impact_types: set[str],
    late_information_types: set[str],
) -> bool:
    if not _verified_event(event):
        return True
    event_type = str(event.get("type", "")).strip().lower()
    if event_type in high_impact_types:
        return type(event.get("material_impact")) is not bool
    if event_type in late_information_types:
        try:
            _timezone_timestamp(event.get("observed_at"), "event.observed_at")
        except ValueError:
            return True
        return False
    return True


def _closing_movement(
    forecast_record: dict[str, Any],
    closing: dict[str, Any] | None,
) -> tuple[float | None, bool]:
    if closing is None:
        return None, False
    closing_value = _mapping(closing, "closing")
    _timezone_timestamp(closing_value.get("observed_at"), "closing.observed_at")
    closing_probabilities = _probability_map(
        closing_value.get("probabilities_90m"),
        ("home", "draw", "away"),
        "closing.probabilities_90m",
    )
    one_x_two = _mapping(
        _mapping(forecast_record.get("markets"), "forecast_record.markets").get("1x2"),
        "forecast_record.markets.1x2",
    )
    probabilities = _probability_map(
        one_x_two.get("probabilities"),
        ("home", "draw", "away"),
        "forecast_record.markets.1x2.probabilities",
    )
    pick = str(one_x_two.get("pick", "")).strip()
    if pick not in probabilities:
        raise ValueError("1x2 pick is not a valid selection")
    delta_pp = (closing_probabilities[pick] - probabilities[pick]) * 100.0
    return delta_pp, delta_pp <= -3.0


def _market_table(settlement: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "market": "1x2",
            "period": "90m",
            "pick": settlement["1x2"]["pick"],
            "outcome": settlement["1x2"]["outcome"],
            "verdict": settlement["1x2"]["pick_verdict"],
        }
    ]
    for line, item in settlement["totals"].items():
        rows.append(
            {
                "market": f"total:{line}",
                "period": "90m",
                "pick": item["pick"],
                "outcome": item["outcome"],
                "verdict": item["pick_verdict"],
            }
        )
    rows.append(
        {
            "market": "btts",
            "period": "90m",
            "pick": settlement["btts"]["pick"],
            "outcome": settlement["btts"]["outcome"],
            "verdict": settlement["btts"]["pick_verdict"],
        }
    )
    for line, item in settlement["asian_handicap"].items():
        rows.append(
            {
                "market": f"asian_handicap:{line}",
                "period": "90m",
                "pick": item["pick"],
                "outcome": item["verdicts"],
                "verdict": item["pick_verdict"],
            }
        )
    correct_verdicts = settlement["correct_score"]["displayed_verdicts"]
    if correct_verdicts:
        first_score = next(iter(correct_verdicts))
        rows.append(
            {
                "market": "correct_score",
                "period": "90m",
                "pick": first_score,
                "outcome": settlement["correct_score"]["outcome"],
                "verdict": correct_verdicts[first_score],
            }
        )
    if settlement["qualification"] is not None:
        item = settlement["qualification"]
        rows.append(
            {
                "market": "qualification",
                "period": "qualification",
                "pick": item["pick"],
                "outcome": item["qualified"],
                "verdict": item["pick_verdict"],
            }
        )
    return rows


def _cause_tags(
    forecast_record: dict[str, Any],
    settlement: dict[str, Any],
    market_table: list[dict[str, Any]],
    *,
    closing_moved_against: bool,
    events: list[dict[str, Any]],
    calibration: dict[str, Any] | None,
    previous_settlement: dict[str, Any] | None,
) -> list[str]:
    losing_verdicts = {"loss", "half_loss"}
    has_miss = any(row.get("verdict") in losing_verdicts for row in market_table)
    tags = []
    if previous_settlement is not None:
        previous_score = _score(previous_settlement.get("score_used"), "previous_settlement.score_used")
        current_score = settlement["1x2"]["score_used"]
        if previous_score != current_score:
            tags.append("settlement_scope_error")

    high_impact_types = {"red_card", "penalty", "goalkeeper_injury"}
    late_information_types = {
        "confirmed_injury",
        "confirmed_suspension",
        "starting_lineup_change",
        "goalkeeper_change",
    }
    if any(
        _event_evidence_unavailable(event, high_impact_types, late_information_types)
        for event in events
    ):
        tags.append("evidence_unavailable")
    if not has_miss:
        return tags
    if closing_moved_against:
        tags.append("closing_market_moved_against_forecast")
    if any(
        _verified_event(event)
        and event.get("material_impact") is True
        and str(event.get("type", "")).strip().lower() in high_impact_types
        for event in events
    ):
        tags.append("high_impact_match_event")
    if any(
        _verified_event(event)
        and str(event.get("type", "")).strip().lower() in late_information_types
        and _event_between_forecast_and_kickoff(event, forecast_record)
        for event in events
    ):
        tags.append("late_information_missed")
    if forecast_record.get("cross_market_conflicts") and forecast_record.get("confidence", {}).get("label") == "high":
        tags.append("cross_market_conflict_underweighted")
    if calibration and calibration.get("overconfident") is True:
        tags.append("overconfidence")
    if calibration and calibration.get("repeated_bias") is True:
        tags.append("repeated_model_bias_candidate")
    if not tags:
        tags.append("probabilistic_miss")
    return tags


def _localized_market_name(market: str, language: str) -> str:
    if language == "en":
        if market == "1x2":
            return "90-minute 1X2"
        if market == "btts":
            return "BTTS"
        if market == "qualification":
            return "qualification"
        if market == "correct_score":
            return "correct score"
        if market.startswith("total:"):
            return f"total {market.split(':', 1)[1]}"
        if market.startswith("asian_handicap:"):
            selection_line = market.split(":", 1)[1]
            for side in ("home", "away"):
                if selection_line.startswith(side):
                    return f"Asian handicap {side} {selection_line[len(side):]}"
            return f"Asian handicap {selection_line}"
        return market
    if market == "1x2":
        return "90分钟胜平负"
    if market == "btts":
        return "双方进球"
    if market == "qualification":
        return "晋级"
    if market == "correct_score":
        return "比分"
    if market.startswith("total:"):
        return f"大小球 {market.split(':', 1)[1]}"
    if market.startswith("asian_handicap:"):
        selection_line = market.split(":", 1)[1]
        for side, label in (("home", "主队"), ("away", "客队")):
            if selection_line.startswith(side):
                return f"亚洲让球 {label}{selection_line[len(side):]}"
        return f"亚洲让球 {selection_line}"
    return market


def _localized_value(value: Any, language: str) -> str:
    tokens = {
        "zh": {
            "home": "主队",
            "draw": "平局",
            "away": "客队",
            "yes": "是",
            "no": "否",
            "over": "大",
            "under": "小",
            "win": "命中",
            "half_win": "半赢",
            "push": "走盘",
            "half_loss": "半输",
            "loss": "未命中",
        },
        "en": {
            "half_win": "half win",
            "half_loss": "half loss",
        },
    }[language]

    def token(item: Any) -> str:
        text = str(item)
        return tokens.get(text.strip().lower(), text)

    if isinstance(value, dict):
        delimiter = "；" if language == "zh" else "; "
        separator = "：" if language == "zh" else ": "
        return delimiter.join(
            f"{token(key)}{separator}{token(item)}"
            for key, item in value.items()
        )
    return token(value)


def _localized_sections(
    market_table: list[dict[str, Any]],
    cause_tags: list[str],
    closing_delta: float | None,
    metrics: dict[str, Any],
    language: str,
    evolution_status: str,
) -> dict[str, Any]:
    verdict_text = {
        "zh": {
            "win": "命中",
            "half_win": "半赢",
            "push": "走盘",
            "half_loss": "半输",
            "loss": "未命中",
            None: "未结算",
        },
        "en": {
            "win": "win",
            "half_win": "half win",
            "push": "push",
            "half_loss": "half loss",
            "loss": "loss",
            None: "unsettled",
        },
    }[language]

    def describe(row: dict[str, Any]) -> str:
        market = _localized_market_name(row["market"], language)
        verdict = verdict_text.get(row.get("verdict"), str(row.get("verdict")))
        pick = _localized_value(row.get("pick"), language)
        outcome = _localized_value(row.get("outcome"), language)
        if language == "zh":
            return f"{market}：预测 {pick}，结果 {outcome}（{verdict}）"
        return f"{market}: pick {pick}, outcome {outcome} ({verdict})"

    right = [describe(row) for row in market_table if row.get("verdict") in {"win", "half_win"}]
    wrong = [describe(row) for row in market_table if row.get("verdict") in {"loss", "half_loss"}]
    unsettled = [describe(row) for row in market_table if row.get("verdict") in {None, "push"}]
    causes = [CAUSE_TEXT[language][tag] for tag in cause_tags]
    if closing_delta is None:
        closing_text = "未提供收盘共识，无法比较临场变化。" if language == "zh" else "Closing consensus is unavailable."
    elif language == "zh":
        closing_text = f"收盘时所选方向概率变化 {closing_delta:+.1f} 个百分点。"
    else:
        closing_text = f"Closing probability for the selected direction changed {closing_delta:+.1f} percentage points."
    if language == "zh":
        calibration_text = (
            f"本场校准影响：1X2 Brier {metrics['1x2_brier']:.4f}，"
            f"log loss {metrics['1x2_log_loss']:.4f}；单场不触发权重更新。"
        )
    else:
        calibration_text = (
            f"Calibration impact: 1X2 Brier {metrics['1x2_brier']:.4f}, "
            f"log loss {metrics['1x2_log_loss']:.4f}; one match cannot update weights."
        )
    evolution_text = {
        "zh": {
            "model_unchanged": "模型未更改（model_unchanged）",
            "challenger_pending": "挑战模型待验证（challenger_pending）",
            "champion_promoted": "挑战模型已晋升（champion_promoted）",
            "champion_rolled_back": "冠军模型已回滚（champion_rolled_back）",
        },
        "en": {
            "model_unchanged": "model unchanged (model_unchanged)",
            "challenger_pending": "challenger pending (challenger_pending)",
            "champion_promoted": "champion promoted (champion_promoted)",
            "champion_rolled_back": "champion rolled back (champion_rolled_back)",
        },
    }[language].get(evolution_status, evolution_status)
    probability_reminder = (
        "概率判断即使校准合理，单场仍可能出现未命中的结果。"
        if language == "zh"
        else "Well-calibrated probabilities can still lose individual matches."
    )
    return {
        "right": right,
        "wrong": wrong,
        "unsettled": unsettled,
        "causes": causes,
        "closing": closing_text,
        "calibration": calibration_text,
        "evolution": evolution_text,
        "probability_reminder": probability_reminder,
    }


def _review_message(summary: str, sections: dict[str, Any], language: str) -> str:
    if language == "zh":
        return "\n".join(
            [
                summary,
                "正确：" + ("；".join(sections["right"]) or "无"),
                "错误：" + ("；".join(sections["wrong"]) or "无"),
                "未结算/走盘：" + ("；".join(sections["unsettled"]) or "无"),
                "原因：" + ("；".join(sections["causes"]) or "未发现需要归因的错误"),
                "收盘：" + sections["closing"],
                "校准：" + sections["calibration"],
                "模型状态：" + sections["evolution"],
                "概率提醒：" + sections["probability_reminder"],
            ]
        )
    return "\n".join(
        [
            summary,
            "Right: " + ("; ".join(sections["right"]) or "none"),
            "Wrong: " + ("; ".join(sections["wrong"]) or "none"),
            "Unsettled/push: " + ("; ".join(sections["unsettled"]) or "none"),
            "Causes: " + ("; ".join(sections["causes"]) or "no error requires attribution"),
            "Closing: " + sections["closing"],
            "Calibration: " + sections["calibration"],
            "Evolution status: " + sections["evolution"],
            "Probability reminder: " + sections["probability_reminder"],
        ]
    )


def _completed_record(
    forecast_record: dict[str, Any],
    settlement: dict[str, Any],
    review_id: str,
    closing: dict[str, Any] | None,
) -> dict[str, Any]:
    markets = _mapping(forecast_record.get("markets"), "forecast_record.markets")
    one_x_two = _mapping(markets.get("1x2"), "forecast_record.markets.1x2")
    probabilities_90m = _probability_map(
        one_x_two.get("probabilities"),
        ("home", "draw", "away"),
        "forecast_record.markets.1x2.probabilities",
    )
    completed_totals = []
    outcome_totals = {}
    settlement_totals = settlement["totals"]
    for index, raw_total in enumerate(markets.get("totals", [])):
        total = _mapping(raw_total, f"forecast_record.markets.totals[{index}]")
        line_key = format(_quarter_line(total.get("line"), "totals.line"), "g")
        outcome = settlement_totals[line_key]["outcome"]
        if outcome == "push":
            continue
        probabilities = total.get("model_probabilities", total.get("probabilities"))
        completed_totals.append(
            {
                "line": float(total["line"]),
                "model_probabilities": _probability_map(
                    probabilities,
                    ("over", "under"),
                    f"forecast_record.markets.totals[{index}].model_probabilities",
                ),
            }
        )
        outcome_totals[line_key] = outcome

    btts = _mapping(markets.get("btts"), "forecast_record.markets.btts")
    completed = {
        "schema_version": "1.0",
        "review_id": review_id,
        "event_id": forecast_record.get("event_id"),
        "forecast_id": forecast_record.get("forecast_id"),
        "kickoff": forecast_record.get("kickoff"),
        "as_of": forecast_record.get("as_of"),
        "alert_offset": forecast_record.get("alert_offset"),
        "profile_id": forecast_record.get("profile_id"),
        "input_fingerprint": forecast_record.get("input_fingerprint"),
        "bucket": forecast_record.get("bucket") or "football|1x2",
        "probabilities_90m": probabilities_90m,
        "outcome_90m": settlement["1x2"]["outcome"],
        "confidence": copy.deepcopy(forecast_record.get("confidence")),
        "expected_goals": copy.deepcopy(forecast_record.get("expected_goals")),
        "actual_score": copy.deepcopy(settlement["1x2"]["score_used"]),
        "score_distribution": copy.deepcopy(forecast_record.get("score_distribution_90m")),
        "totals": completed_totals,
        "outcome_totals": outcome_totals,
        "btts": _probability_map(
            btts.get("probabilities"),
            ("yes", "no"),
            "forecast_record.markets.btts.probabilities",
        ),
        "outcome_btts": settlement["btts"]["outcome"],
        "raw_match": copy.deepcopy(forecast_record.get("raw_match")),
    }
    if closing is not None:
        completed["closing_consensus_90m"] = _probability_map(
            closing.get("probabilities_90m"),
            ("home", "draw", "away"),
            "closing.probabilities_90m",
        )
    return completed


def build_review(
    forecast_record: dict[str, Any],
    result: dict[str, Any],
    *,
    closing: dict[str, Any] | None = None,
    events: list[dict[str, Any]] | None = None,
    language: str = "en",
    calibration: dict[str, Any] | None = None,
    previous_settlement: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if language not in {"zh", "en"}:
        raise ValueError("language must be zh or en")
    normalized_events = [] if events is None else events
    if not isinstance(normalized_events, list) or any(not isinstance(item, dict) for item in normalized_events):
        raise ValueError("events must be a list of objects")

    settlement = settle_forecast(forecast_record, result)
    review_identity = {
        "forecast_id": forecast_record.get("forecast_id"),
        "result": validate_result(result),
    }
    review_id = f"review-{forecast.canonical_hash(review_identity)[:24]}"
    if settlement["settlement_status"] != "settled":
        return {
            "schema_version": "1.0",
            "review_id": review_id,
            "event_id": settlement["event_id"],
            "forecast_id": settlement.get("forecast_id"),
            "review_status": "pending",
            "pending_reason": settlement["pending_reason"],
            "evolution_status": "model_unchanged",
            "language": language,
        }

    table = _market_table(settlement)
    closing_delta, closing_moved_against = _closing_movement(forecast_record, closing)
    tags = _cause_tags(
        forecast_record,
        settlement,
        table,
        closing_moved_against=closing_moved_against,
        events=normalized_events,
        calibration=calibration,
        previous_settlement=previous_settlement,
    )
    score = settlement["result_timeline"]["score_90m"]
    score_text = f"{score['home']}-{score['away']}"
    aet = settlement["result_timeline"].get("score_after_extra_time")
    aet_text = None if aet is None else f"{aet['home']}-{aet['away']}"
    one_x_two_hit = settlement["1x2"]["pick_verdict"] == "win"
    qualification = settlement.get("qualification")
    qualification_hit = qualification is not None and qualification["pick_verdict"] == "win"
    if language == "zh":
        timeline = f"90分钟 {score_text}" + (f"，加时后 {aet_text}" if aet_text else "")
        result_text = "90分钟赛果预测命中" if one_x_two_hit else "90分钟赛果预测未命中"
        qualification_text = "" if qualification is None else ("；晋级预测命中" if qualification_hit else "；晋级预测未命中")
        summary = f"{timeline}；{result_text}{qualification_text}。单场复盘不会直接修改模型。"
        lesson = "正确或错误的一场比赛都只增加证据，不会单独改变模型权重。"
    else:
        timeline = f"90 minutes {score_text}" + (f", after extra time {aet_text}" if aet_text else "")
        result_text = "the 90-minute result pick was correct" if one_x_two_hit else "the 90-minute result pick missed"
        qualification_text = "" if qualification is None else ("; the qualification pick was correct" if qualification_hit else "; the qualification pick missed")
        summary = f"{timeline}; {result_text}{qualification_text}. One review does not change the model."
        lesson = "One match, whether correct or wrong, adds evidence but cannot change model weights by itself."

    probabilities_90m = _probability_map(
        forecast_record["markets"]["1x2"]["probabilities"],
        ("home", "draw", "away"),
        "forecast_record.markets.1x2.probabilities",
    )
    outcome_90m = settlement["1x2"]["outcome"]
    metrics = {
        "1x2_brier": _multiclass_brier(probabilities_90m, outcome_90m),
        "1x2_log_loss": _log_loss(probabilities_90m, outcome_90m),
    }
    markets = _mapping(forecast_record.get("markets"), "forecast_record.markets")
    btts_probabilities = _probability_map(
        _mapping(markets.get("btts"), "forecast_record.markets.btts").get("probabilities"),
        ("yes", "no"),
        "forecast_record.markets.btts.probabilities",
    )
    metrics["btts_brier"] = _binary_brier(
        btts_probabilities["yes"],
        settlement["btts"]["outcome"] == "yes",
    )
    totals_brier = {}
    for index, raw_total in enumerate(markets.get("totals", [])):
        total = _mapping(raw_total, f"forecast_record.markets.totals[{index}]")
        line_key = format(_quarter_line(total.get("line"), "totals.line"), "g")
        outcome = settlement["totals"][line_key]["outcome"]
        if outcome == "push":
            continue
        probabilities = _probability_map(
            total.get("model_probabilities", total.get("probabilities")),
            ("over", "under"),
            f"forecast_record.markets.totals[{index}].model_probabilities",
        )
        totals_brier[line_key] = _binary_brier(
            probabilities["over"],
            outcome == "over",
        )
    metrics["totals_brier"] = totals_brier

    distribution_value = _mapping(
        forecast_record.get("score_distribution_90m"),
        "score_distribution_90m",
    )
    distribution = {}
    for raw_score, raw_probability in distribution_value.items():
        score_key = _score_key(raw_score, "score_distribution_90m score")
        if score_key in distribution:
            raise ValueError(f"duplicate score_distribution_90m score {score_key}")
        if isinstance(raw_probability, bool) or not isinstance(raw_probability, (int, float)):
            raise ValueError(f"score_distribution_90m.{score_key} must be a probability")
        probability = float(raw_probability)
        if not math.isfinite(probability) or not 0.0 <= probability <= 1.0:
            raise ValueError(f"score_distribution_90m.{score_key} must be between 0 and 1")
        distribution[score_key] = probability
    if not math.isclose(sum(distribution.values()), 1.0, abs_tol=1e-9):
        raise ValueError("score_distribution_90m must sum to 1")
    actual_score_key = settlement["correct_score"]["outcome"]
    support = set(distribution) | {actual_score_key}
    metrics["score_brier"] = sum(
        (distribution.get(score_key, 0.0) - (1.0 if score_key == actual_score_key else 0.0)) ** 2
        for score_key in support
    )
    metrics["score_log_loss"] = -math.log(max(1e-15, distribution.get(actual_score_key, 0.0)))
    evolution_status = "model_unchanged"
    localized_sections = _localized_sections(
        table,
        tags,
        closing_delta,
        metrics,
        language,
        evolution_status,
    )
    review = {
        "schema_version": "1.0",
        "review_id": review_id,
        "event_id": settlement["event_id"],
        "forecast_id": settlement.get("forecast_id"),
        "review_status": "completed",
        "language": language,
        "summary": summary,
        "message": _review_message(summary, localized_sections, language),
        "lesson": lesson,
        "market_table": table,
        "cause_tags": tags,
        "cause_explanations": localized_sections["causes"],
        "localized_sections": localized_sections,
        "settlement": settlement,
        "metrics": metrics,
        "closing_movement_pp": closing_delta,
        "evolution_status": evolution_status,
    }
    review["completed_record"] = _completed_record(
        forecast_record,
        settlement,
        review_id,
        closing,
    )
    return review


def append_completed(path: str | Path, review: dict[str, Any]) -> bool:
    if review.get("review_status") != "completed" or not isinstance(review.get("completed_record"), dict):
        raise ValueError("only completed reviews can enter the completed ledger")
    return forecast.append_unique_jsonl(
        path,
        review["completed_record"],
        "review_id",
    )


def _read_json(path: str | Path, field_name: str) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {field_name}: {exc}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--forecast", required=True, help="Archived forecast record JSON.")
    parser.add_argument("--result", required=True, help="Verified result JSON.")
    parser.add_argument("--closing", help="Optional closing consensus JSON.")
    parser.add_argument("--events", help="Optional verified match-events JSON list.")
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    parser.add_argument("--completed-out", help="Completed-review JSONL path.")
    parser.add_argument("--data-dir", help="Data directory for completed.jsonl.")
    parser.add_argument("--no-record", action="store_true", help="Do not write the completed ledger.")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    if args.no_record and (args.completed_out or args.data_dir):
        parser.error("--no-record cannot be combined with --completed-out or --data-dir")

    try:
        forecast_record = _read_json(args.forecast, "forecast")
        result = _read_json(args.result, "result")
        closing = None if args.closing is None else _read_json(args.closing, "closing")
        events = [] if args.events is None else _read_json(args.events, "events")
        if isinstance(events, dict):
            events = events.get("events")
        review = build_review(
            forecast_record,
            result,
            closing=closing,
            events=events,
            language=args.language,
        )
        if not args.no_record and review["review_status"] == "completed":
            completed_path = (
                Path(args.completed_out).expanduser()
                if args.completed_out
                else model_profile.resolve_data_dir(args.data_dir) / "completed.jsonl"
            )
            append_completed(completed_path, review)
    except (TypeError, ValueError) as exc:
        parser.error(str(exc))

    print(json.dumps(review, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
