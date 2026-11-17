#!/usr/bin/env python3
"""Build a repeatable World Cup odds forecast scaffold from structured input."""

from __future__ import annotations

import argparse
import copy
import errno
import functools
import hashlib
import json
import math
import os
import tempfile
from collections.abc import Mapping
from collections import defaultdict
from contextlib import contextmanager
from decimal import Decimal, InvalidOperation
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType
from typing import Any

import model_profile

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows uses msvcrt.
    fcntl = None

try:
    import msvcrt
except ImportError:  # pragma: no cover - POSIX uses fcntl.
    msvcrt = None


def _freeze_default_profile(profile: dict[str, Any]) -> Mapping[str, Any]:
    frozen_sections = {
        section: MappingProxyType(dict(profile[section]))
        for section in (
            "source_weights",
            "fit_family_caps",
            "recency_weights",
            "confidence_thresholds",
        )
    }
    return MappingProxyType({**profile, **frozen_sections})


DEFAULT_MODEL_PROFILE = _freeze_default_profile(model_profile.load_profile())
SOURCE_WEIGHTS = DEFAULT_MODEL_PROFILE["source_weights"]
MOVEMENT_TOLERANCE = 1e-6
MATCH_TYPES = {
    "league_or_group",
    "single_leg_knockout",
    "two_leg_first",
    "two_leg_second",
    "friendly",
    "unknown",
}
FIT_GRID_MIN = 0.15
FIT_GRID_MAX = 4.00
FIT_GRID_STEP = 0.05
FIT_MAX_GOALS = 10
FIT_FAMILY_CAPS = DEFAULT_MODEL_PROFILE["fit_family_caps"]
RECENCY_WEIGHTS = DEFAULT_MODEL_PROFILE["recency_weights"]
CONFIDENCE_THRESHOLDS = DEFAULT_MODEL_PROFILE["confidence_thresholds"]
DEFAULT_DISPERSION = 0.05
FIT_PROBABILITY_SUM_TOLERANCE = 1e-9
MIN_FULL_FORECAST_BOOKS = 3
AGGREGATOR_SOURCES = {"aggregator", "odds_aggregator", "comparison_site"}
FORECAST_RECORD_SCHEMA_VERSION = "1.0"
FORECAST_ENGINE_VERSION = "2.1.0"
ALERT_OFFSETS = {190: "T-3h10", 130: "T-2h10", 70: "T-1h10", 10: "T-10min"}


def _json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    return value


def _canonical_json(value: Any) -> str:
    return json.dumps(
        _json_ready(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


@contextmanager
def _exclusive_file_lock(path: Path):
    lock_path = path.with_name(f"{path.name}.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as handle:
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            lock_backend = "fcntl"
        elif msvcrt is not None:
            handle.seek(0, os.SEEK_END)
            if handle.tell() == 0:
                handle.write(b"\0")
                handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            lock_backend = "msvcrt"
        else:
            raise RuntimeError("no supported cross-process lock is available")
        try:
            yield
        finally:
            if lock_backend == "fcntl":
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            else:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)


def _read_jsonl_records(path: Path, id_field: str) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL at line {line_number}") from exc
        if not isinstance(item, dict) or not str(item.get(id_field, "")).strip():
            raise ValueError(f"invalid {id_field} at line {line_number}")
        records.append(item)
    return records


def _fsync_directory(path: Path) -> None:
    if os.name != "posix":
        return
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    try:
        directory_fd = os.open(path, flags)
    except OSError as exc:
        if exc.errno in {errno.EINVAL, errno.ENOTSUP, errno.EBADF}:
            return
        raise
    try:
        os.fsync(directory_fd)
    except OSError as exc:
        if exc.errno not in {errno.EINVAL, errno.ENOTSUP, errno.EBADF}:
            raise
    finally:
        os.close(directory_fd)


def _write_jsonl_atomic(path: Path, records: list[dict[str, Any]]) -> None:
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as handle:
            for item in records:
                handle.write(_canonical_json(item) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
        _fsync_directory(path.parent)
    finally:
        Path(temporary_name).unlink(missing_ok=True)


def append_unique_jsonl_batch(
    path: str | Path,
    records: list[dict[str, Any]],
    id_field: str,
) -> list[bool]:
    destination = Path(path).expanduser()
    destination.parent.mkdir(parents=True, exist_ok=True)
    canonical_batch: dict[str, str] = {}
    for record in records:
        if not isinstance(record, dict) or not str(record.get(id_field, "")).strip():
            raise ValueError(f"record requires non-empty {id_field}")
        record_id = str(record[id_field])
        serialized = _canonical_json(record)
        if record_id in canonical_batch and canonical_batch[record_id] != serialized:
            raise ValueError(f"conflicting batch record for {id_field}={record_id}")
        canonical_batch[record_id] = serialized

    with _exclusive_file_lock(destination):
        existing = _read_jsonl_records(destination, id_field)
        existing_by_id: dict[str, str] = {}
        for item in existing:
            record_id = str(item[id_field])
            serialized = _canonical_json(item)
            if record_id in existing_by_id and existing_by_id[record_id] != serialized:
                raise ValueError(f"conflicting existing records for {id_field}={record_id}")
            existing_by_id[record_id] = serialized

        results = []
        additions = []
        added_ids: set[str] = set()
        for record in records:
            record_id = str(record[id_field])
            serialized = canonical_batch[record_id]
            if record_id in existing_by_id:
                if existing_by_id[record_id] != serialized:
                    raise ValueError(f"conflicting record for {id_field}={record_id}")
                results.append(False)
            elif record_id in added_ids:
                results.append(False)
            else:
                additions.append(record)
                added_ids.add(record_id)
                results.append(True)

        if additions:
            _write_jsonl_atomic(destination, [*existing, *additions])
        return results


def append_unique_jsonl(
    path: str | Path,
    record: dict[str, Any],
    id_field: str,
) -> bool:
    return append_unique_jsonl_batch(path, [record], id_field)[0]


def _parse_number(value: Any) -> float:
    text = str(value).strip()
    if text.startswith("+"):
        text = text[1:]
    return float(text)


def _normalize_odds_format(odds_format: str | None) -> str:
    if odds_format is None or not str(odds_format).strip():
        raise ValueError("odds_format is required")

    fmt = str(odds_format).strip().lower().replace("-", "_").replace(" ", "_")
    if fmt in {"decimal", "eu", "european"}:
        return "decimal"
    if fmt in {"american", "us"}:
        return "american"
    if fmt in {"fractional", "uk"}:
        return "fractional"
    if fmt in {"hong_kong", "hongkong", "hk", "asian"}:
        return "hong_kong"
    if fmt in {"malay", "malaysian"}:
        return "malay"
    if fmt in {"indo", "indonesian"}:
        return "indonesian"
    raise ValueError(f"unsupported odds format: {odds_format}")


def odds_to_decimal(value: Any, odds_format: str | None) -> float:
    fmt = _normalize_odds_format(odds_format)
    if value is None or str(value).strip() == "":
        raise ValueError("odds value is required")

    if fmt == "fractional":
        text = str(value).strip()
        parts = text.split("/", 1)
        if len(parts) != 2:
            raise ValueError(f"invalid fractional odds: {value}")
        try:
            numerator = float(parts[0])
            denominator = float(parts[1])
        except ValueError as exc:
            raise ValueError(f"invalid fractional odds: {value}") from exc
        if numerator <= 0 or denominator <= 0:
            raise ValueError(f"invalid fractional odds: {value}")
        return 1.0 + (numerator / denominator)

    try:
        number = _parse_number(value)
    except ValueError as exc:
        raise ValueError(f"invalid odds value: {value}") from exc

    if fmt == "decimal":
        if number <= 1.0:
            raise ValueError(f"decimal odds must be greater than 1: {value}")
        return number
    if fmt == "american":
        if number == 0:
            raise ValueError("american odds cannot be zero")
        if number > 0:
            return 1.0 + (number / 100.0)
        return 1.0 + (100.0 / abs(number))
    if fmt == "hong_kong":
        if number <= 0:
            raise ValueError(f"hong kong odds must be positive: {value}")
        return 1.0 + number
    if fmt == "malay":
        if number == 0 or abs(number) >= 1:
            raise ValueError(f"malay odds must be between -1 and 1, excluding 0: {value}")
        if number > 0:
            return 1.0 + number
        return 1.0 + (1.0 / abs(number))
    if fmt == "indonesian":
        if number == 0 or abs(number) < 1:
            raise ValueError(f"indonesian odds must be <= -1 or >= 1: {value}")
        if number > 0:
            return 1.0 + number
        return 1.0 + (1.0 / abs(number))

    raise ValueError(f"unsupported odds format: {odds_format}")


def implied_probability(value: Any, odds_format: str | None) -> float:
    return 1.0 / odds_to_decimal(value, odds_format)


def _normalize_probability_inputs(raw: list[float]) -> list[float]:
    if not raw:
        raise ValueError("raw probabilities are required")

    probabilities = [float(value) for value in raw]
    if any(not math.isfinite(value) or value <= 0 for value in probabilities):
        raise ValueError("raw probabilities must be positive finite numbers")
    return probabilities


def _normalize_probabilities(raw: list[float]) -> list[float]:
    total = sum(raw)
    if total <= 0:
        raise ValueError("probabilities must sum to a positive number")
    return [value / total for value in raw]


def devig_probabilities(raw: list[float], method: str = "power") -> list[float]:
    probabilities = _normalize_probability_inputs(raw)
    normalized_method = str(method).strip().lower()
    if normalized_method in {"", "proportional"} or len(probabilities) != 3:
        return _normalize_probabilities(probabilities)

    if normalized_method != "power":
        raise ValueError(f"unsupported devig method: {method}")

    def powered_total(exponent: float) -> float:
        return sum(value**exponent for value in probabilities)

    low = 0.0
    high = 1.0
    if math.isclose(powered_total(high), 1.0, rel_tol=0.0, abs_tol=1e-12):
        return _normalize_probabilities([value**high for value in probabilities])
    if powered_total(high) > 1.0:
        for _ in range(32):
            high *= 2.0
            if powered_total(high) <= 1.0:
                break
        else:
            return _normalize_probabilities(probabilities)

    for _ in range(80):
        midpoint = (low + high) / 2.0
        total = powered_total(midpoint)
        if math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-12):
            return _normalize_probabilities([value**midpoint for value in probabilities])
        if total > 1.0:
            low = midpoint
        else:
            high = midpoint

    candidate = [value ** ((low + high) / 2.0) for value in probabilities]
    total = sum(candidate)
    if not math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-9):
        return _normalize_probabilities(probabilities)
    return _normalize_probabilities(candidate)


def _coerce_datetime(value: Any) -> datetime | None:
    if value in {None, ""}:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    text = str(value).strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    parsed = datetime.fromisoformat(text)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _quote_period(quote: dict[str, Any]) -> str:
    period = quote.get("period")
    return str(period).strip() if period not in {None, ""} else "90m"


def _quote_snapshot(quote: dict[str, Any]) -> str:
    snapshot = quote.get("snapshot")
    return str(snapshot).strip().lower() if snapshot not in {None, ""} else "current"


def _quote_market(quote: dict[str, Any]) -> str:
    market = quote.get("market")
    if market in {None, ""}:
        raise ValueError("market is required")
    return str(market).strip().lower()


def _quote_underlying_bookmaker(quote: dict[str, Any]) -> str:
    source = str(quote.get("source", "direct")).strip().lower()
    underlying_value = quote.get("underlying_bookmaker")
    underlying_bookmaker = "" if underlying_value is None else str(underlying_value).strip()
    if source in AGGREGATOR_SOURCES and not underlying_bookmaker:
        raise ValueError("underlying_bookmaker is required for aggregator quotes")
    bookmaker = underlying_bookmaker or quote.get("bookmaker")
    if bookmaker in {None, ""}:
        raise ValueError("bookmaker is required")
    normalized = str(bookmaker).strip()
    if not normalized:
        raise ValueError("bookmaker is required")
    return normalized


def _quote_selection(quote: dict[str, Any]) -> str:
    selection = quote.get("selection")
    if selection in {None, ""}:
        raise ValueError("selection is required")
    return str(selection).strip().lower()


def _market_requires_line(market: str) -> bool:
    return market in {"totals", "total", "asian_handicap", "handicap", "spread"}


def _canonicalize_line_value(value: Any) -> str:
    try:
        decimal_value = Decimal(str(value).strip())
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"invalid market line: {value}") from exc
    if not decimal_value.is_finite():
        raise ValueError(f"invalid market line: {value}")

    normalized = format(decimal_value.normalize(), "f")
    if "." in normalized:
        normalized = normalized.rstrip("0").rstrip(".")
    return normalized or "0"


def _quote_line(quote: dict[str, Any]) -> Any:
    market = _quote_market(quote)
    line = quote.get("line")
    if line in {None, ""}:
        if _market_requires_line(market):
            raise ValueError(f"line is required for market: {market}")
        return None
    if _market_requires_line(market):
        if market in {"asian_handicap", "handicap", "spread"}:
            return _canonicalize_line_value(abs(_coerce_quarter_line(line, "line")))
        return _canonicalize_line_value(line)
    return line


def _quote_key(quote: dict[str, Any]) -> tuple[str, str, str, Any, str, str]:
    return (
        _quote_underlying_bookmaker(quote),
        _quote_market(quote),
        _quote_period(quote),
        _quote_line(quote),
        _quote_selection(quote),
        _quote_snapshot(quote),
    )


def _source_weight(
    quote: dict[str, Any],
    source_weights: Mapping[str, float] | None = None,
) -> float:
    tier = str(quote.get("source_tier", "D")).strip().upper()
    weights = SOURCE_WEIGHTS if source_weights is None else source_weights
    return float(weights.get(tier, 0.0))


def _tie_break_identity(quote: dict[str, Any]) -> tuple[Any, ...]:
    source = str(quote.get("source", "")).strip().lower()
    bookmaker = str(quote.get("bookmaker", "")).strip().lower()
    direct_rank = 0 if source == "direct" else 1
    return (direct_rank, source, bookmaker, json.dumps(quote, sort_keys=True, default=str))


def deduplicate_quotes(
    quotes: list[dict[str, Any]],
    source_weights: Mapping[str, float] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    kept_by_key: dict[
        tuple[str, str, str, Any, str, str], tuple[int, dict[str, Any], float, datetime, tuple[Any, ...]]
    ] = {}
    first_positions: dict[tuple[str, str, str, Any, str, str], int] = {}

    for index, quote in enumerate(quotes):
        key = _quote_key(quote)
        observed_at = _coerce_datetime(quote.get("observed_at")) or datetime.min.replace(tzinfo=timezone.utc)
        candidate = (
            index,
            quote,
            _source_weight(quote, source_weights),
            observed_at,
            _tie_break_identity(quote),
        )
        current = kept_by_key.get(key)
        if current is None:
            kept_by_key[key] = candidate
            first_positions[key] = index
            continue

        _, _, current_weight, current_observed_at, current_identity = current
        if candidate[2] > current_weight:
            kept_by_key[key] = candidate
            continue
        if math.isclose(candidate[2], current_weight) and candidate[3] > current_observed_at:
            kept_by_key[key] = candidate
            continue
        if (
            math.isclose(candidate[2], current_weight)
            and candidate[3] == current_observed_at
            and candidate[4] < current_identity
        ):
            kept_by_key[key] = candidate

    ordered_keys = sorted(first_positions, key=lambda key: first_positions[key])
    kept = [kept_by_key[key][1] for key in ordered_keys]
    diagnostics = {
        "duplicates_removed": len(quotes) - len(kept),
        "kept_quotes": len(kept),
        "raw_quotes": len(quotes),
    }
    return kept, diagnostics


def _validate_asian_handicap_pairs(quotes: list[dict[str, Any]]) -> None:
    pair_groups: dict[tuple[str, str, str, str, str], dict[str, float]] = defaultdict(dict)
    for quote in quotes:
        market = _quote_market(quote)
        if market not in {"asian_handicap", "handicap", "spread"}:
            continue
        signed_line = _coerce_quarter_line(quote.get("line"), "line")
        line_key = _canonicalize_line_value(abs(signed_line))
        key = (
            _quote_underlying_bookmaker(quote),
            market,
            _quote_period(quote),
            _quote_snapshot(quote),
            line_key,
        )
        pair_groups[key][_quote_selection(quote)] = signed_line

    orientations: dict[tuple[str, str, str, str], set[float]] = defaultdict(set)
    for key in sorted(pair_groups):
        selections = pair_groups[key]
        if set(selections) != {"home", "away"} or not math.isclose(
            selections["home"],
            -selections["away"],
            rel_tol=0.0,
            abs_tol=1e-12,
        ):
            raise ValueError(
                "asian_handicap requires mirrored home/away lines per bookmaker, period, snapshot, and line"
            )
        _, market, period, snapshot, line_key = key
        orientations[(market, period, snapshot, line_key)].add(selections["home"])

    if any(len(home_lines) != 1 for home_lines in orientations.values()):
        raise ValueError("asian_handicap requires consistent mirrored home/away lines across bookmakers")


def _required_selections(market: str) -> tuple[str, ...]:
    if market == "1x2":
        return ("home", "draw", "away")
    if market in {"asian_handicap", "handicap", "spread"}:
        return ("home", "away")
    if market in {"btts", "both_teams_to_score"}:
        return ("yes", "no")
    if market in {"qualification", "to_qualify"}:
        return ()
    if market in {"draw_no_bet", "dnb"}:
        return ("home", "away")
    if market in {"totals", "total"}:
        return ("over", "under")
    return ()


def _market_liquidity_weight(market: str) -> float:
    if market == "1x2":
        return 1.0
    if market in {"asian_handicap", "handicap", "spread"}:
        return 0.9
    if market in {"draw_no_bet", "dnb", "qualification", "to_qualify"}:
        return 0.9
    if market in {"totals", "total", "btts", "both_teams_to_score"}:
        return 0.85
    return 0.8


def _recency_weight(
    snapshot: str,
    observed_at: datetime | None,
    as_of: datetime | None,
    recency_weights: Mapping[str, float] | None = None,
) -> float:
    weights = RECENCY_WEIGHTS if recency_weights is None else recency_weights
    if snapshot == "opening" or observed_at is None or as_of is None:
        return 1.0
    age_seconds = max(0.0, (as_of - observed_at).total_seconds())
    age_minutes = age_seconds / 60.0
    if age_minutes < 15.0:
        return float(weights["0_15"])
    if age_minutes < 60.0:
        return float(weights["15_60"])
    if age_minutes < 180.0:
        return float(weights["60_180"])
    return float(weights["older"])


def _median(values: list[float]) -> float:
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2.0


def _scaled_mad(values: list[float], median_value: float | None = None) -> float:
    if not values:
        return 0.0
    median_value = _median(values) if median_value is None else median_value
    deviations = [abs(value - median_value) for value in values]
    return _median(deviations) * 1.4826


def _weighted_median(entries: list[tuple[float, float, str]]) -> float | None:
    usable = [(value, weight, label) for value, weight, label in entries if weight > 0]
    if not usable:
        return None
    usable.sort(key=lambda item: (item[0], item[2]))
    total_weight = sum(weight for _, weight, _ in usable)
    threshold = total_weight / 2.0
    cumulative = 0.0
    for value, weight, _ in usable:
        cumulative += weight
        if cumulative >= threshold:
            return value
    return usable[-1][0]


def _market_group_key(quote: dict[str, Any]) -> tuple[str, str, Any, str]:
    return (_quote_market(quote), _quote_period(quote), _quote_line(quote), _quote_snapshot(quote))


def _market_group_name(key: tuple[str, str, Any, str]) -> str:
    market, period, line, snapshot = key
    return f"{market}|{period}|{line}|{snapshot}"


def _resolve_required_selections(
    market: str, book_groups: dict[str, dict[str, dict[str, Any]]]
) -> tuple[str, ...]:
    base = _required_selections(market)
    if base or market not in {"qualification", "to_qualify"}:
        return base

    available = sorted(
        {
            selection
            for selection_quotes in book_groups.values()
            for selection in selection_quotes
        }
    )
    binary_present = any(selection in {"yes", "no"} for selection in available)
    named_present = any(selection not in {"yes", "no"} for selection in available)
    if binary_present and named_present:
        raise ValueError(f"mixed qualification selection schemes: {available}")
    if binary_present:
        return ("yes", "no")
    if len(available) == 2:
        return tuple(available)
    if len(available) > 2:
        raise ValueError(f"invalid qualification selection scheme: {available}")
    return ()


def build_consensus(
    quotes: list[dict[str, Any]],
    as_of: datetime | str | None = None,
    *,
    source_weights: Mapping[str, float] | None = None,
    recency_weights: Mapping[str, float] | None = None,
) -> dict[str, dict[str, Any]]:
    normalized_as_of = _coerce_datetime(as_of)
    deduped_quotes, dedupe_diagnostics = deduplicate_quotes(quotes, source_weights)
    _validate_asian_handicap_pairs(deduped_quotes)
    raw_group_counts: dict[tuple[str, str, Any, str], int] = defaultdict(int)
    for quote in quotes:
        raw_group_counts[_market_group_key(quote)] += 1

    groups: dict[tuple[str, str, Any, str], dict[str, dict[str, dict[str, Any]]]] = defaultdict(dict)
    for quote in deduped_quotes:
        group_key = _market_group_key(quote)
        bookmaker = _quote_underlying_bookmaker(quote)
        groups[group_key].setdefault(bookmaker, {})
        groups[group_key][bookmaker][_quote_selection(quote)] = quote

    result: dict[str, dict[str, Any]] = {}
    for group_key in sorted(groups, key=_market_group_name):
        market, period, line, snapshot = group_key
        book_groups = groups[group_key]
        required = _resolve_required_selections(market, book_groups)
        asian_home_line = None
        if market in {"asian_handicap", "handicap", "spread"}:
            home_lines = {
                _coerce_quarter_line(selection_quotes["home"].get("line"), "line")
                for selection_quotes in book_groups.values()
            }
            if len(home_lines) != 1:
                raise ValueError("asian_handicap requires consistent mirrored home/away lines across bookmakers")
            asian_home_line = next(iter(home_lines))
        raw_source_count = raw_group_counts[group_key]
        kept_quote_count = sum(len(selection_quotes) for selection_quotes in book_groups.values())

        book_entries: list[dict[str, Any]] = []
        complete_entries: list[dict[str, Any]] = []
        overrounds: list[float] = []

        for bookmaker in sorted(book_groups):
            selection_quotes = book_groups[bookmaker]
            observed_times = [
                _coerce_datetime(quote.get("observed_at"))
                for quote in selection_quotes.values()
                if _coerce_datetime(quote.get("observed_at")) is not None
            ]
            observed_at = max(observed_times) if observed_times else None
            raw_probabilities = {
                selection: implied_probability(
                    quote.get("odds", quote.get("price")),
                    quote.get("odds_format"),
                )
                for selection, quote in selection_quotes.items()
            }

            if required:
                present_required = [selection for selection in required if selection in raw_probabilities]
                completeness_ratio = len(present_required) / len(required)
            else:
                present_required = list(raw_probabilities)
                completeness_ratio = 1.0 if raw_probabilities else 0.0
            is_complete = bool(required) and len(present_required) == len(required)

            if is_complete:
                ordered_raw = [raw_probabilities[selection] for selection in required]
                method = "power" if market == "1x2" else "proportional"
                devigged = devig_probabilities(ordered_raw, method=method)
                probabilities = dict(zip(required, devigged))
                overround = sum(ordered_raw)
                overrounds.append(overround)
                unvigged = True
                completeness_weight = 1.0
            else:
                present_values = [raw_probabilities[selection] for selection in present_required]
                probabilities = dict(zip(present_required, _normalize_probabilities(present_values))) if present_values else {}
                overround = None
                unvigged = False
                completeness_weight = min(0.5, completeness_ratio)

            source_weight = max(
                0.0,
                _source_weight(next(iter(selection_quotes.values())), source_weights),
            )
            recency_weight = _recency_weight(
                snapshot,
                observed_at,
                normalized_as_of,
                recency_weights,
            )
            market_weight = _market_liquidity_weight(market)
            total_weight = source_weight * recency_weight * completeness_weight * market_weight

            entry = {
                "bookmaker": bookmaker,
                "probabilities": probabilities,
                "is_complete": is_complete,
                "unvigged": unvigged,
                "weight": total_weight,
                "source_weight": source_weight,
                "recency_weight": recency_weight,
                "completeness_weight": completeness_weight,
                "liquidity_weight": market_weight,
                "overround": overround,
                "observed_at": observed_at.isoformat() if observed_at else None,
            }
            book_entries.append(entry)
            if is_complete and total_weight > 0:
                complete_entries.append(entry)

        outlier_diagnostics: list[dict[str, Any]] = []
        excluded_books: set[str] = set()
        if len(complete_entries) >= 5 and required:
            selection_stats: dict[str, tuple[float, float]] = {}
            for selection in required:
                values = [entry["probabilities"][selection] for entry in complete_entries]
                selection_median = _median(values)
                selection_scaled_mad = _scaled_mad(values, selection_median)
                selection_stats[selection] = (selection_median, selection_scaled_mad)

            candidates: list[tuple[float, float, str, dict[str, Any]]] = []
            for entry in complete_entries:
                bookmaker = entry["bookmaker"]
                strongest: tuple[float, float, dict[str, Any]] | None = None
                for selection in required:
                    median_value, scaled_mad = selection_stats[selection]
                    probability = entry["probabilities"][selection]
                    absolute_diff = abs(probability - median_value)
                    ratio = absolute_diff / scaled_mad if scaled_mad > 0 else (math.inf if absolute_diff > 0 else 0.0)
                    diagnostic = {
                        "bookmaker": bookmaker,
                        "selection": selection,
                        "probability": probability,
                        "median": median_value,
                        "absolute_diff": absolute_diff,
                        "scaled_mad": scaled_mad,
                        "ratio": ratio,
                        "candidate": absolute_diff > 0.06 and (scaled_mad == 0 or ratio > 3.0),
                    }
                    outlier_diagnostics.append(diagnostic)
                    if diagnostic["candidate"]:
                        if strongest is None or (ratio, absolute_diff) > strongest[:2]:
                            strongest = (ratio, absolute_diff, diagnostic)
                if strongest is not None:
                    ratio, absolute_diff, diagnostic = strongest
                    candidates.append((ratio, absolute_diff, bookmaker, diagnostic))

            max_exclusions = int(len(complete_entries) * 0.2)
            if max_exclusions > 0:
                candidates.sort(key=lambda item: (-item[0], -item[1], item[2]))
                for _, _, bookmaker, _ in candidates[:max_exclusions]:
                    excluded_books.add(bookmaker)

            for diagnostic in outlier_diagnostics:
                diagnostic["excluded"] = diagnostic["bookmaker"] in excluded_books and diagnostic["candidate"]
        else:
            for entry in complete_entries:
                for selection, probability in entry["probabilities"].items():
                    outlier_diagnostics.append(
                        {
                            "bookmaker": entry["bookmaker"],
                            "selection": selection,
                            "probability": probability,
                            "candidate": False,
                            "excluded": False,
                        }
                    )

        usable_complete_entries = [
            entry for entry in complete_entries if entry["bookmaker"] not in excluded_books and entry["weight"] > 0
        ]
        usable_books = sorted(entry["bookmaker"] for entry in usable_complete_entries)

        complete_support = {
            selection: any(selection in entry["probabilities"] for entry in usable_complete_entries)
            for selection in required
        }
        has_complete_anchor = bool(required) and bool(usable_complete_entries) and all(complete_support.values())

        probabilities: dict[str, float] = {}
        selections = required
        if has_complete_anchor:
            for selection in selections:
                weighted_entries = [
                    (entry["probabilities"][selection], entry["weight"], entry["bookmaker"])
                    for entry in usable_complete_entries
                    if selection in entry["probabilities"]
                ]
                selection_probability = _weighted_median(weighted_entries)
                if selection_probability is not None:
                    probabilities[selection] = selection_probability

            if probabilities:
                probabilities = dict(zip(probabilities.keys(), _normalize_probabilities(list(probabilities.values()))))

        dispersion_range: dict[str, float] = {}
        dispersion_mad: dict[str, float] = {}
        for selection in selections:
            values = [
                entry["probabilities"][selection]
                for entry in usable_complete_entries
                if selection in entry["probabilities"]
            ]
            if values:
                dispersion_range[selection] = max(values) - min(values)
                dispersion_mad[selection] = _scaled_mad(values)

        completeness = {
            "required_selections": list(required),
            "complete_books": len(complete_entries),
            "incomplete_books": sum(1 for entry in book_entries if not entry["is_complete"]),
            "anchor_ready": has_complete_anchor,
        }

        market_result = {
            "market": market,
            "period": period,
            "line": line,
            "snapshot": snapshot,
            "raw_source_count": raw_source_count,
            "independent_books": len(book_groups),
            "usable_books": usable_books,
            "usable_book_count": len(usable_books),
            "probabilities": probabilities,
            "dispersion": {"range": dispersion_range, "mad": dispersion_mad},
            "overround_range": {
                "min": min(overrounds) if overrounds else None,
                "max": max(overrounds) if overrounds else None,
            },
            "unvigged": bool(complete_entries),
            "completeness": completeness,
            "deduplication": {
                "raw_quotes": raw_source_count,
                "kept_quotes": kept_quote_count,
                "duplicates_removed": raw_source_count - kept_quote_count,
                "overall": dedupe_diagnostics,
            },
            "outliers": outlier_diagnostics,
        }
        if asian_home_line is not None:
            market_result["home_line"] = asian_home_line
            market_result["away_line"] = -asian_home_line
        result[_market_group_name(group_key)] = market_result

    return result


def _coerce_finite_float(value: Any, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite number")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not math.isfinite(number):
        raise ValueError(f"{name} must be a finite number")
    return number


def _coerce_nonnegative_float(value: Any, name: str) -> float:
    number = _coerce_finite_float(value, name)
    if number < 0:
        raise ValueError(f"{name} must be non-negative")
    return number


def _coerce_nonnegative_int(value: Any, name: str) -> int:
    if type(value) is not int:
        raise ValueError(f"{name} must be a non-negative integer")
    if value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return value


def _coerce_probability_value(value: Any, name: str) -> float:
    probability = _coerce_finite_float(value, name)
    if probability < 0 or probability > 1:
        raise ValueError(f"{name} must be between 0 and 1")
    return probability


def poisson_prob(rate: float, goals: int) -> float:
    validated_rate = _coerce_nonnegative_float(rate, "rate")
    validated_goals = _coerce_nonnegative_int(goals, "goals")
    return math.exp(-validated_rate) * (validated_rate**validated_goals) / math.factorial(validated_goals)


def _poisson_vector(rate: float, max_goals: int) -> list[float]:
    validated_rate = _coerce_nonnegative_float(rate, "rate")
    validated_max_goals = _coerce_nonnegative_int(max_goals, "max_goals")
    probabilities = [
        math.exp(-validated_rate) * (validated_rate**goals) / math.factorial(goals)
        for goals in range(validated_max_goals + 1)
    ]
    total = sum(probabilities)
    if total <= 0:
        raise ValueError("poisson mass must be positive")
    return [probability / total for probability in probabilities]


@functools.lru_cache(maxsize=16)
def _fit_grid_rates(min_value: float, max_value: float, step_value: float) -> tuple[float, ...]:
    min_rate = _coerce_nonnegative_float(min_value, "grid minimum")
    max_rate = _coerce_nonnegative_float(max_value, "grid maximum")
    step = _coerce_nonnegative_float(step_value, "grid step")
    if step == 0:
        raise ValueError("grid step must be positive")
    if max_rate < min_rate:
        raise ValueError("grid maximum must be at least grid minimum")
    return tuple(
        round(min_rate + (index * step), 10)
        for index in range(int(round((max_rate - min_rate) / step)) + 1)
    )


@functools.lru_cache(maxsize=8192)
def _cached_model_state(
    home_xg: float,
    away_xg: float,
    max_goals: int,
) -> tuple[tuple[tuple[float, ...], ...], Mapping[str, float]]:
    home_vector = tuple(_poisson_vector(home_xg, max_goals))
    away_vector = tuple(_poisson_vector(away_xg, max_goals))
    matrix = tuple(
        tuple(home_probability * away_probability for away_probability in away_vector)
        for home_probability in home_vector
    )
    return matrix, MappingProxyType(metrics_from_matrix(matrix))


def poisson_matrix(home_xg: float, away_xg: float, max_goals: int = 10) -> list[list[float]]:
    home_probabilities = _poisson_vector(home_xg, max_goals)
    away_probabilities = _poisson_vector(away_xg, max_goals)
    return [
        [home_probability * away_probability for away_probability in away_probabilities]
        for home_probability in home_probabilities
    ]


def _normalize_matrix(matrix: Any) -> list[list[float]]:
    if not isinstance(matrix, (list, tuple)) or not matrix:
        raise ValueError("matrix must be a non-empty rectangular grid")

    normalized_rows: list[list[float]] = []
    expected_width: int | None = None
    total = 0.0
    for row in matrix:
        if not isinstance(row, (list, tuple)) or not row:
            raise ValueError("matrix must be a non-empty rectangular grid")
        if expected_width is None:
            expected_width = len(row)
        elif len(row) != expected_width:
            raise ValueError("matrix must be rectangular")

        normalized_row: list[float] = []
        for value in row:
            probability = _coerce_nonnegative_float(value, "matrix value")
            normalized_row.append(probability)
            total += probability
        normalized_rows.append(normalized_row)

    if total <= 0:
        raise ValueError("matrix must have positive total mass")
    if math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-12):
        return normalized_rows
    return [[value / total for value in row] for row in normalized_rows]


def metrics_from_matrix(matrix: list[list[float]]) -> dict[str, float]:
    normalized_matrix = _normalize_matrix(matrix)
    metrics = {
        "home": 0.0,
        "draw": 0.0,
        "away": 0.0,
        "over_2_5": 0.0,
        "under_2_5": 0.0,
        "over_3_5": 0.0,
        "under_3_5": 0.0,
        "btts_yes": 0.0,
        "btts_no": 0.0,
        "home_win_by_1": 0.0,
        "home_win_by_2": 0.0,
        "home_win_by_3_plus": 0.0,
        "away_win_by_1": 0.0,
        "away_win_by_2": 0.0,
        "away_win_by_3_plus": 0.0,
    }

    for home_goals, row in enumerate(normalized_matrix):
        for away_goals, probability in enumerate(row):
            goal_diff = home_goals - away_goals
            total_goals = home_goals + away_goals

            if goal_diff > 0:
                metrics["home"] += probability
            elif goal_diff < 0:
                metrics["away"] += probability
            else:
                metrics["draw"] += probability

            if total_goals >= 3:
                metrics["over_2_5"] += probability
            else:
                metrics["under_2_5"] += probability

            if total_goals >= 4:
                metrics["over_3_5"] += probability
            else:
                metrics["under_3_5"] += probability

            if home_goals > 0 and away_goals > 0:
                metrics["btts_yes"] += probability
            else:
                metrics["btts_no"] += probability

            if goal_diff == 1:
                metrics["home_win_by_1"] += probability
            elif goal_diff == 2:
                metrics["home_win_by_2"] += probability
            elif goal_diff >= 3:
                metrics["home_win_by_3_plus"] += probability
            elif goal_diff == -1:
                metrics["away_win_by_1"] += probability
            elif goal_diff == -2:
                metrics["away_win_by_2"] += probability
            elif goal_diff <= -3:
                metrics["away_win_by_3_plus"] += probability

    metrics["home_win_by_2_plus"] = metrics["home_win_by_2"] + metrics["home_win_by_3_plus"]
    metrics["away_win_by_2_plus"] = metrics["away_win_by_2"] + metrics["away_win_by_3_plus"]
    return metrics


def _coerce_quarter_line(value: Any, name: str = "line") -> float:
    line = _coerce_finite_float(value, name)
    quarter_steps = round(line * 4.0)
    if not math.isclose(line * 4.0, quarter_steps, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError(f"{name} must be a multiple of 0.25")
    return quarter_steps / 4.0


def _half_lines(line: float) -> tuple[float, ...]:
    quarter_steps = round(line * 4.0)
    if abs(quarter_steps) % 2 == 1:
        lower = math.floor(line * 2.0) / 2.0
        return (lower, lower + 0.5)
    return (line,)


def _single_bet_outcome(edge: float, tolerance: float = 1e-12) -> str:
    if edge > tolerance:
        return "win"
    if edge < -tolerance:
        return "loss"
    return "push"


def _combine_split_outcomes(first: str, second: str) -> str:
    if first == second:
        return first
    pair = frozenset({first, second})
    if pair == {"win", "push"}:
        return "half_win"
    if pair == {"loss", "push"}:
        return "half_loss"
    if pair == {"win", "loss"}:
        return "push"
    raise ValueError(f"unsupported split settlement: {first}, {second}")


def _blank_settlement() -> dict[str, float]:
    return {"win": 0.0, "half_win": 0.0, "push": 0.0, "half_loss": 0.0, "loss": 0.0}


def settle_asian_handicap(matrix: list[list[float]], side: str, line: float) -> dict[str, float]:
    normalized_matrix = _normalize_matrix(matrix)
    normalized_side = str(side).strip().lower()
    if normalized_side not in {"home", "away"}:
        raise ValueError("side must be 'home' or 'away'")
    normalized_line = _coerce_quarter_line(line)
    split_lines = _half_lines(normalized_line)
    settlement = _blank_settlement()

    for home_goals, row in enumerate(normalized_matrix):
        for away_goals, probability in enumerate(row):
            margin = home_goals - away_goals if normalized_side == "home" else away_goals - home_goals
            if len(split_lines) == 1:
                outcome = _single_bet_outcome(margin + split_lines[0])
            else:
                outcome = _combine_split_outcomes(
                    _single_bet_outcome(margin + split_lines[0]),
                    _single_bet_outcome(margin + split_lines[1]),
                )
            settlement[outcome] += probability
    return settlement


def settle_total(matrix: list[list[float]], side: str, line: float) -> dict[str, float]:
    normalized_matrix = _normalize_matrix(matrix)
    normalized_side = str(side).strip().lower()
    if normalized_side not in {"over", "under"}:
        raise ValueError("side must be 'over' or 'under'")
    normalized_line = _coerce_quarter_line(line)
    split_lines = _half_lines(normalized_line)
    settlement = _blank_settlement()

    for home_goals, row in enumerate(normalized_matrix):
        for away_goals, probability in enumerate(row):
            total_goals = home_goals + away_goals
            if len(split_lines) == 1:
                edge = total_goals - split_lines[0] if normalized_side == "over" else split_lines[0] - total_goals
                outcome = _single_bet_outcome(edge)
            else:
                first_edge = total_goals - split_lines[0] if normalized_side == "over" else split_lines[0] - total_goals
                second_edge = total_goals - split_lines[1] if normalized_side == "over" else split_lines[1] - total_goals
                outcome = _combine_split_outcomes(
                    _single_bet_outcome(first_edge),
                    _single_bet_outcome(second_edge),
                )
            settlement[outcome] += probability
    return settlement


def _selection_probability_from_settlement(settlement: dict[str, float]) -> float:
    if not isinstance(settlement, dict):
        raise ValueError("settlement must be a dict")

    required_keys = ("win", "half_win", "push", "half_loss", "loss")
    values: dict[str, float] = {}
    for key in required_keys:
        if key not in settlement:
            raise ValueError(f"settlement is missing {key}")
        values[key] = _coerce_nonnegative_float(settlement[key], f"settlement.{key}")

    favorable = values["win"] + (0.5 * values["half_win"])
    unfavorable = values["loss"] + (0.5 * values["half_loss"])
    decisive_total = favorable + unfavorable
    if decisive_total <= 0:
        raise ValueError("settlement has no decisive outcomes")
    return favorable / decisive_total


def _mean_dispersion(entry: dict[str, Any]) -> float:
    dispersion = entry.get("dispersion")
    if not isinstance(dispersion, dict):
        return DEFAULT_DISPERSION
    mad = dispersion.get("mad")
    if not isinstance(mad, dict):
        return DEFAULT_DISPERSION

    values = []
    for value in mad.values():
        try:
            number = _coerce_nonnegative_float(value, "dispersion")
        except ValueError:
            continue
        values.append(number)
    return sum(values) / len(values) if values else DEFAULT_DISPERSION


def _entry_quality(entry: dict[str, Any]) -> dict[str, float]:
    try:
        independent_books = _coerce_nonnegative_float(entry.get("independent_books", 0), "independent_books")
    except ValueError:
        independent_books = 0.0
    coverage = min(independent_books, 5.0) / 5.0
    dispersion = _mean_dispersion(entry)
    dispersion_factor = 1.0 / (1.0 + (25.0 * dispersion))
    return {
        "coverage": coverage,
        "dispersion": dispersion,
        "quality": coverage * dispersion_factor,
    }


def _validated_probability_map(entry: dict[str, Any], keys: tuple[str, ...]) -> dict[str, float] | None:
    probabilities = entry.get("probabilities")
    if not isinstance(probabilities, dict):
        return None

    extracted: dict[str, float] = {}
    for key in keys:
        if key not in probabilities:
            return None
        try:
            extracted[key] = _coerce_probability_value(probabilities[key], f"probabilities.{key}")
        except ValueError:
            return None
    if not math.isclose(
        sum(extracted.values()),
        1.0,
        rel_tol=0.0,
        abs_tol=FIT_PROBABILITY_SUM_TOLERANCE,
    ):
        return None
    return extracted


def _fit_groups_from_consensus(
    consensus: dict[str, Any],
    family_caps: Mapping[str, float] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, float]]:
    resolved_caps = FIT_FAMILY_CAPS if family_caps is None else family_caps
    if set(resolved_caps) != set(FIT_FAMILY_CAPS):
        raise ValueError(f"family_caps must contain exactly {sorted(FIT_FAMILY_CAPS)}")
    groups: list[dict[str, Any]] = []
    family_weights = {family: 0.0 for family in resolved_caps}

    for market_key in sorted(consensus):
        entry = consensus.get(market_key)
        if not isinstance(entry, dict):
            continue
        if str(entry.get("period")).strip() != "90m":
            continue
        if str(entry.get("snapshot")).strip().lower() != "current":
            continue
        completeness = entry.get("completeness")
        if not isinstance(completeness, dict):
            continue
        if completeness.get("anchor_ready") is not True or type(completeness.get("anchor_ready")) is not bool:
            continue
        if entry.get("unvigged") is not True or type(entry.get("unvigged")) is not bool:
            continue

        market = str(entry.get("market", "")).strip().lower()
        quality = _entry_quality(entry)
        if quality["quality"] <= 0:
            continue

        if market == "1x2":
            probabilities = _validated_probability_map(entry, ("home", "draw", "away"))
            if probabilities is None:
                continue
            groups.append(
                {
                    "family": "1x2",
                    "label": "1x2",
                    "quality": quality,
                    "targets": [
                        {"metric": "home", "target": probabilities["home"]},
                        {"metric": "draw", "target": probabilities["draw"]},
                        {"metric": "away", "target": probabilities["away"]},
                    ],
                }
            )
            continue

        if market in {"totals", "total"}:
            try:
                line = _coerce_quarter_line(entry.get("line"), "line")
            except ValueError:
                continue
            probabilities = _validated_probability_map(entry, ("over", "under"))
            if probabilities is None:
                continue

            groups.append(
                {
                    "family": "totals",
                    "label": f"totals:{line:g}:over",
                    "quality": quality,
                    "targets": [
                        {"metric": "total", "selection": "over", "line": line, "target": probabilities["over"]}
                    ],
                }
            )
            continue

        if market in {"btts", "both_teams_to_score"}:
            probabilities = _validated_probability_map(entry, ("yes", "no"))
            if probabilities is None:
                continue
            groups.append(
                {
                    "family": "btts",
                    "label": "btts",
                    "quality": quality,
                    "targets": [{"metric": "btts_yes", "target": probabilities["yes"]}],
                }
            )

    weighted_targets: list[dict[str, Any]] = []
    for family, cap in resolved_caps.items():
        family_groups = [group for group in groups if group["family"] == family]
        if not family_groups:
            continue
        average_quality = sum(group["quality"]["quality"] for group in family_groups) / len(family_groups)
        family_total_weight = cap * min(1.0, average_quality)
        family_weights[family] = family_total_weight
        quality_total = sum(group["quality"]["quality"] for group in family_groups)
        if family_total_weight <= 0 or quality_total <= 0:
            continue
        for group in family_groups:
            group_weight = family_total_weight * (group["quality"]["quality"] / quality_total)
            target_weight = group_weight / len(group["targets"])
            for target in group["targets"]:
                weighted_targets.append(
                    {
                        **target,
                        "family": family,
                        "label": group["label"],
                        "weight": target_weight,
                        "coverage": group["quality"]["coverage"],
                        "dispersion": group["quality"]["dispersion"],
                    }
                )

    if not weighted_targets:
        raise ValueError("no valid current 90m 1X2, totals, or BTTS targets")
    return weighted_targets, family_weights


def _target_model_probability(matrix: Any, metrics: Mapping[str, float], target: dict[str, Any]) -> float:
    metric = target["metric"]
    if metric in {"home", "draw", "away", "btts_yes"}:
        return metrics[metric]
    if metric == "total":
        settlement = settle_total(matrix, side=target["selection"], line=target["line"])
        return _selection_probability_from_settlement(settlement)
    raise ValueError(f"unsupported target metric: {metric}")


def fit_expected_goals(
    consensus: dict[str, Any],
    *,
    family_caps: Mapping[str, float] | None = None,
) -> dict[str, Any]:
    if not isinstance(consensus, dict):
        raise ValueError("consensus must be a dict")

    targets, family_weights = _fit_groups_from_consensus(consensus, family_caps)
    total_weight = sum(target["weight"] for target in targets)
    if total_weight <= 0:
        raise ValueError("no valid current 90m 1X2, totals, or BTTS targets")

    grid = _fit_grid_rates(FIT_GRID_MIN, FIT_GRID_MAX, FIT_GRID_STEP)

    best_result: dict[str, Any] | None = None
    for home_xg in grid:
        for away_xg in grid:
            matrix, metrics = _cached_model_state(home_xg, away_xg, FIT_MAX_GOALS)

            weighted_sum_sq = 0.0
            weighted_abs = 0.0
            for target in targets:
                model_probability = _target_model_probability(matrix, metrics, target)
                error = model_probability - target["target"]
                weighted_sum_sq += target["weight"] * (error**2)
                weighted_abs += target["weight"] * abs(error)

            weighted_mse = weighted_sum_sq / total_weight
            residual = math.sqrt(weighted_mse)
            candidate = {
                "home_xg": home_xg,
                "away_xg": away_xg,
                "matrix": matrix,
                "metrics": metrics,
                "weighted_mse": weighted_mse,
                "weighted_mae": weighted_abs / total_weight,
                "residual": residual,
            }
            if best_result is None:
                best_result = candidate
                continue
            if weighted_mse < best_result["weighted_mse"] - 1e-15:
                best_result = candidate
                continue
            if math.isclose(weighted_mse, best_result["weighted_mse"], rel_tol=0.0, abs_tol=1e-15):
                if candidate["weighted_mae"] < best_result["weighted_mae"] - 1e-15:
                    best_result = candidate

    if best_result is None:
        raise ValueError("unable to fit expected goals")

    diagnostics_targets = []
    for target in targets:
        model_probability = _target_model_probability(best_result["matrix"], best_result["metrics"], target)
        diagnostics_targets.append(
            {
                "family": target["family"],
                "label": target["label"],
                "metric": target["metric"],
                "selection": target.get("selection"),
                "line": target.get("line"),
                "target": target["target"],
                "model": model_probability,
                "error": model_probability - target["target"],
                "weight": target["weight"],
                "coverage": target["coverage"],
                "dispersion": target["dispersion"],
            }
        )

    return {
        "home_xg": best_result["home_xg"],
        "away_xg": best_result["away_xg"],
        "residual": best_result["residual"],
        "objective": {
            "weighted_mse": best_result["weighted_mse"],
            "weighted_rmse": best_result["residual"],
            "weighted_mae": best_result["weighted_mae"],
            "weight_total": total_weight,
        },
        "diagnostics": {
            "grid": {
                "min": FIT_GRID_MIN,
                "max": FIT_GRID_MAX,
                "step": FIT_GRID_STEP,
                "candidates": len(grid),
                "max_goals": FIT_MAX_GOALS,
            },
            "family_weights": family_weights,
            "targets": diagnostics_targets,
        },
        "metrics": dict(best_result["metrics"]),
    }


def _finite_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def _nonnegative_metric(value: Any) -> tuple[float, bool]:
    number = _finite_number(value)
    if number is None or number < 0:
        return 0.0, False
    return number, True


def _movement_direction(delta: float | None, tolerance: float = MOVEMENT_TOLERANCE) -> str:
    if delta is None:
        return "unknown"
    if delta > tolerance:
        return "strengthened"
    if delta < -tolerance:
        return "weakened"
    return "stable"


def _normalize_match_type(match_type: Any) -> str:
    return str(match_type).strip() if match_type not in {None, ""} else "unknown"


def _require_bool(flag_name: str, value: Any) -> bool:
    if type(value) is not bool:
        raise ValueError(f"{flag_name} must be a bool")
    return value


def classify_movement(
    previous_favorite_probability: Any,
    current_favorite_probability: Any,
    previous_favorite_asian_line: Any = None,
    current_favorite_asian_line: Any = None,
    *,
    tolerance: float = MOVEMENT_TOLERANCE,
) -> dict[str, Any]:
    previous_probability = _finite_number(previous_favorite_probability)
    current_probability = _finite_number(current_favorite_probability)
    probability_delta = None
    if previous_probability is not None and current_probability is not None:
        probability_delta = current_probability - previous_probability

    previous_asian_line = _finite_number(previous_favorite_asian_line)
    current_asian_line = _finite_number(current_favorite_asian_line)
    asian_delta = None
    if previous_asian_line is not None and current_asian_line is not None:
        asian_delta = previous_asian_line - current_asian_line

    return {
        "probability_change_pp": None if probability_delta is None else probability_delta * 100.0,
        "price_direction": _movement_direction(probability_delta, tolerance=tolerance),
        "asian_direction": _movement_direction(asian_delta, tolerance=tolerance),
        "tolerance": tolerance,
    }


def validate_match_context(match: dict[str, Any] | None) -> list[str]:
    candidate = match or {}
    errors: list[str] = []
    match_type = _normalize_match_type(candidate.get("match_type"))
    if match_type not in MATCH_TYPES:
        errors.append("invalid_match_type")
    aggregate_score = candidate.get("aggregate_score")
    aggregate_missing = aggregate_score is None or (
        isinstance(aggregate_score, str) and not aggregate_score.strip()
    )
    if match_type == "two_leg_second" and aggregate_missing:
        errors.append("aggregate_score_required")
    tiebreak_rules = candidate.get("tiebreak_rules")
    tiebreak_missing = tiebreak_rules is None or (
        isinstance(tiebreak_rules, str) and not tiebreak_rules.strip()
    ) or (isinstance(tiebreak_rules, (list, tuple, dict)) and not tiebreak_rules)
    if match_type == "two_leg_second" and not aggregate_missing and tiebreak_missing:
        errors.append("tiebreak_rules_required")

    teams = candidate.get("teams")
    normalized_teams: list[str] = []
    ambiguous_team_identity = False
    if not isinstance(teams, (list, tuple)) or len(teams) != 2:
        ambiguous_team_identity = True
    else:
        for team in teams:
            if team in {None, ""}:
                ambiguous_team_identity = True
                break
            normalized = " ".join(str(team).strip().casefold().split())
            if not normalized or normalized in {"team a", "team b", "home", "away", "unknown", "tbd"}:
                ambiguous_team_identity = True
                break
            normalized_teams.append(normalized)
        if len(normalized_teams) == 2 and normalized_teams[0] == normalized_teams[1]:
            ambiguous_team_identity = True
    if ambiguous_team_identity:
        errors.append("ambiguous_team_identity")
    return errors


def _books_score(independent_books: Any) -> float:
    count, valid = _nonnegative_metric(independent_books)
    return min(count, 5.0) * 5.0 if valid else 0.0


def _freshness_score(freshest_age_minutes: Any) -> float:
    age_minutes, valid = _nonnegative_metric(freshest_age_minutes)
    if not valid:
        return 0.0
    if age_minutes <= 15:
        return 20.0
    if age_minutes <= 60:
        return 18.0
    if age_minutes <= 180:
        return 14.0
    return 8.0


def _market_family_score(market_families: Any) -> float:
    count, valid = _nonnegative_metric(market_families)
    return min(count, 5.0) * 4.0 if valid else 0.0


def _dispersion_score(max_dispersion: Any) -> float:
    dispersion, valid = _nonnegative_metric(max_dispersion)
    if not valid:
        return 0.0
    if dispersion <= 0.02:
        return 15.0
    if dispersion <= 0.04:
        return 10.0
    if dispersion <= 0.06:
        return 5.0
    return 0.0


def _agreement_score(fit_residual: Any) -> float:
    residual, valid = _nonnegative_metric(fit_residual)
    if not valid:
        return 0.0
    if residual <= 0.02:
        return 15.0
    if residual <= 0.04:
        return 10.0
    if residual <= 0.08:
        return 5.0
    return 0.0


def _evidence_label(
    score: float,
    thresholds: Mapping[str, float] | None = None,
) -> str:
    resolved = CONFIDENCE_THRESHOLDS if thresholds is None else thresholds
    if score >= float(resolved["high"]):
        return "high"
    if score >= float(resolved["medium"]):
        return "medium"
    return "low"


def score_evidence(
    *,
    independent_books: Any,
    freshest_age_minutes: Any,
    market_families: Any,
    max_dispersion: Any,
    fit_residual: Any,
    lineup_confirmed: bool,
    match_started: bool,
    has_live_quotes: bool,
    match_type: str = "unknown",
    near_kickoff: bool = True,
    match: dict[str, Any] | None = None,
    context_errors: list[str] | None = None,
    confidence_thresholds: Mapping[str, float] | None = None,
) -> dict[str, Any]:
    lineup_confirmed = _require_bool("lineup_confirmed", lineup_confirmed)
    match_started = _require_bool("match_started", match_started)
    has_live_quotes = _require_bool("has_live_quotes", has_live_quotes)
    near_kickoff = _require_bool("near_kickoff", near_kickoff)

    resolved_match_type = _normalize_match_type(match_type)
    if match is not None:
        context_match = dict(match)
        context_match.setdefault("match_type", resolved_match_type)
        resolved_match_type = _normalize_match_type(context_match.get("match_type"))
        errors = list(context_errors) if context_errors is not None else validate_match_context(context_match)
    elif context_errors is not None:
        errors = list(context_errors)
    else:
        errors = [] if resolved_match_type in MATCH_TYPES else ["invalid_match_type"]

    components = {
        "independent_books": _books_score(independent_books),
        "freshness": _freshness_score(freshest_age_minutes),
        "market_families": _market_family_score(market_families),
        "dispersion": _dispersion_score(max_dispersion),
        "agreement": _agreement_score(fit_residual),
        "lineup": 5.0 if lineup_confirmed else 0.0,
    }

    raw_score = min(100.0, sum(components.values()))
    penalties: dict[str, float] = {}
    if resolved_match_type == "friendly":
        penalties["friendly"] = 10.0

    score = max(0.0, raw_score - sum(penalties.values()))
    context_limitations = ["unknown_match_type"] if resolved_match_type == "unknown" else []

    abstain_reasons: list[str] = []
    if any(
        error in {"invalid_match_type", "aggregate_score_required", "tiebreak_rules_required"}
        for error in errors
    ):
        abstain_reasons.append("invalid_context")
    if "ambiguous_team_identity" in errors:
        abstain_reasons.append("ambiguous_match")

    usable_books, usable_books_valid = _nonnegative_metric(independent_books)
    if not usable_books_valid or usable_books < MIN_FULL_FORECAST_BOOKS:
        abstain_reasons.append("insufficient_books")

    freshness_age, freshness_valid = _nonnegative_metric(freshest_age_minutes)
    if near_kickoff and (not freshness_valid or freshness_age > 60):
        abstain_reasons.append("stale_near_kickoff")

    if match_started and not has_live_quotes:
        abstain_reasons.append("already_started")

    return {
        "score": int(score) if float(score).is_integer() else score,
        "score_before_penalties": int(raw_score) if float(raw_score).is_integer() else raw_score,
        "label": _evidence_label(score, confidence_thresholds),
        "components": {
            key: int(value) if float(value).is_integer() else value
            for key, value in components.items()
        },
        "penalties": {
            key: int(value) if float(value).is_integer() else value
            for key, value in penalties.items()
        },
        "abstain": bool(abstain_reasons),
        "abstain_reasons": abstain_reasons,
        "context_errors": errors,
        "context_limitations": context_limitations,
        "match_type": resolved_match_type,
    }


def apply_cross_market_conflict_penalty(
    evidence: dict[str, Any],
    conflicts: list[dict[str, Any]],
    penalty: float,
    confidence_thresholds: Mapping[str, float] | None = None,
) -> dict[str, Any]:
    if not conflicts or penalty <= 0.0:
        return evidence
    adjusted = {
        **evidence,
        "penalties": dict(evidence.get("penalties", {})),
    }
    adjusted["penalties"]["cross_market_conflict"] = (
        int(penalty) if float(penalty).is_integer() else penalty
    )
    score = max(0.0, float(evidence["score"]) - penalty)
    adjusted["score"] = int(score) if score.is_integer() else score
    adjusted["label"] = _evidence_label(score, confidence_thresholds)
    return adjusted


def _display_team_selection(selection: str, teams: tuple[str, str]) -> str:
    normalized = str(selection).strip().casefold()
    if normalized == "home":
        return teams[0]
    if normalized == "away":
        return teams[1]
    if normalized == "draw":
        return "draw"
    for team in teams:
        if normalized == team.casefold():
            return team
    return str(selection)


def _display_probability_map(probabilities: dict[str, Any], teams: tuple[str, str]) -> dict[str, float]:
    display: dict[str, float] = {}
    for selection, probability in probabilities.items():
        display[_display_team_selection(selection, teams)] = float(probability)
    return display


def _consensus_identity(entry: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(entry.get("market", "")).strip().lower(),
        str(entry.get("period", "")).strip(),
        str(entry.get("line")),
    )


def _snapshot_priority(snapshot: str) -> int:
    ranking = {"current": 3, "t-10min": 2, "t-1h10": 1, "opening": 0}
    return ranking.get(str(snapshot).strip().lower(), -1)


def _latest_snapshot_entries(
    consensus: dict[str, dict[str, Any]],
    *,
    period: str | None = "90m",
) -> dict[tuple[str, str, str], dict[str, Any]]:
    latest: dict[tuple[str, str, str], dict[str, Any]] = {}
    for entry in consensus.values():
        if not isinstance(entry, dict):
            continue
        if period is not None and str(entry.get("period")).strip() != period:
            continue
        snapshot = str(entry.get("snapshot", "")).strip().lower()
        if snapshot not in {"current", "t-10min"}:
            continue
        identity = _consensus_identity(entry)
        current = latest.get(identity)
        if current is None or _snapshot_priority(snapshot) > _snapshot_priority(str(current.get("snapshot", ""))):
            latest[identity] = entry
    return latest


def _fit_consensus_from_latest(consensus: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    fit_consensus: dict[str, dict[str, Any]] = {}
    for identity, entry in _latest_snapshot_entries(consensus).items():
        market = identity[0]
        if market not in {"1x2", "totals", "total", "btts", "both_teams_to_score"}:
            continue
        normalized = dict(entry)
        normalized["snapshot"] = "current"
        fit_consensus[_market_group_name((market, "90m", entry.get("line"), "current"))] = normalized
    return fit_consensus


def _latest_timestamp(quotes: list[dict[str, Any]]) -> datetime | None:
    observed = [_coerce_datetime(quote.get("observed_at")) for quote in quotes]
    usable = [value for value in observed if value is not None]
    return max(usable) if usable else None


def _freshest_age_minutes(as_of: datetime | None, quotes: list[dict[str, Any]]) -> float | None:
    latest = _latest_timestamp(quotes)
    if as_of is None or latest is None:
        return None
    return max(0.0, (as_of - latest).total_seconds() / 60.0)


def _market_family_name(market: str) -> str:
    normalized = str(market).strip().lower()
    if normalized in {"totals", "total"}:
        return "totals"
    if normalized in {"btts", "both_teams_to_score"}:
        return "btts"
    if normalized in {"asian_handicap", "handicap", "spread"}:
        return "asian_handicap"
    if normalized in {"qualification", "to_qualify"}:
        return "to_qualify"
    return normalized


def _available_market_families(latest_entries: dict[tuple[str, str, str], dict[str, Any]]) -> set[str]:
    families = set()
    for entry in latest_entries.values():
        probabilities = entry.get("probabilities")
        if isinstance(probabilities, dict) and probabilities:
            families.add(_market_family_name(str(entry.get("market", ""))))
    return families


def _mean_market_dispersion(entries: list[dict[str, Any]]) -> float:
    values = [_mean_dispersion(entry) for entry in entries]
    return max(values) if values else DEFAULT_DISPERSION


def _supported_latest_quote(quote: dict[str, Any]) -> bool:
    snapshot = str(quote.get("snapshot", "")).strip().lower()
    if snapshot not in {"current", "t-10min"}:
        return False
    market = _market_family_name(str(quote.get("market", "")))
    if market not in {"1x2", "totals", "btts", "asian_handicap", "to_qualify"}:
        return False
    period = str(quote.get("period", "")).strip()
    return period in {"90m", "qualification"}


def _usable_independent_books(quotes: list[dict[str, Any]]) -> int:
    return len(
        {
            _quote_underlying_bookmaker(quote)
            for quote in quotes
            if _supported_latest_quote(quote)
        }
    )


def _deepest_usable_books_by_family(
    latest_entries: dict[tuple[str, str, str], dict[str, Any]],
    families: set[str],
) -> dict[str, list[str]]:
    books_by_family: dict[str, list[str]] = {}
    for entry in latest_entries.values():
        family = _market_family_name(str(entry.get("market", "")))
        if family not in families:
            continue
        probabilities = entry.get("probabilities")
        completeness = entry.get("completeness")
        usable_books = entry.get("usable_books")
        if (
            not isinstance(probabilities, dict)
            or not probabilities
            or not isinstance(completeness, dict)
            or completeness.get("anchor_ready") is not True
            or not isinstance(usable_books, list)
        ):
            continue
        candidate = sorted({str(book) for book in usable_books if str(book).strip()})
        current = books_by_family.get(family, [])
        if len(candidate) > len(current) or (len(candidate) == len(current) and candidate < current):
            books_by_family[family] = candidate
    return {family: books_by_family[family] for family in sorted(books_by_family)}


def _core_90m_source_coverage(
    latest_entries: dict[tuple[str, str, str], dict[str, Any]],
) -> tuple[int, dict[str, list[str]]]:
    books_by_family = _deepest_usable_books_by_family(latest_entries, {"1x2", "totals", "btts"})
    independent_books = max((len(books) for books in books_by_family.values()), default=0)
    return independent_books, books_by_family


def _qualification_source_coverage(
    latest_entries: dict[tuple[str, str, str], dict[str, Any]],
) -> tuple[int, list[str]]:
    books_by_family = _deepest_usable_books_by_family(latest_entries, {"to_qualify"})
    books = books_by_family.get("to_qualify", [])
    return len(books), books


def _missing_market_fields(
    latest_entries: dict[tuple[str, str, str], dict[str, Any]],
    *,
    match_type: str,
) -> list[str]:
    available = {_market_family_name(identity[0]) for identity in latest_entries}
    required_90m = ("1x2", "totals", "btts", "asian_handicap")
    missing = [f"current:{market}:90m" for market in required_90m if market not in available]
    if match_type == "single_leg_knockout" and "to_qualify" not in available:
        missing.append("current:to_qualify:qualification")
    return missing


def _movement_report(consensus: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    opening = [
        entry
        for entry in consensus.values()
        if isinstance(entry, dict) and str(entry.get("snapshot", "")).strip().lower() == "opening"
    ]
    latest = list(_latest_snapshot_entries(consensus, period=None).values())

    opening_by_identity = {_consensus_identity(entry): entry for entry in opening}
    latest_by_identity = {_consensus_identity(entry): entry for entry in latest}
    matched_opening: set[int] = set()
    matched_latest: set[int] = set()

    changed: list[dict[str, Any]] = []
    unchanged: list[dict[str, Any]] = []
    missing_snapshots: list[dict[str, Any]] = []
    def record_pair(previous: dict[str, Any], current: dict[str, Any]) -> None:
        market, period, line = _consensus_identity(current)
        opening_line = previous.get("line")
        previous_probabilities = previous.get("probabilities")
        current_probabilities = current.get("probabilities")
        descriptor = {
            "market": market,
            "period": period,
            "line": None if line == "None" else line,
            "opening_line": None if opening_line in {None, "None"} else opening_line,
        }
        if not isinstance(previous_probabilities, dict) or not isinstance(current_probabilities, dict):
            missing_snapshots.append({**descriptor, "missing": ["probabilities"]})
            return
        selections = sorted(set(previous_probabilities) & set(current_probabilities))
        if not selections:
            missing_snapshots.append({**descriptor, "missing": ["shared_selection_probabilities"]})
            return

        deltas = {
            selection: float(current_probabilities[selection]) - float(previous_probabilities[selection])
            for selection in selections
        }
        item = {
            **descriptor,
            "from_snapshot": "opening",
            "to_snapshot": str(current.get("snapshot")).strip().lower(),
            "deltas": deltas,
            "max_abs_delta": max(abs(delta) for delta in deltas.values()),
        }
        if item["max_abs_delta"] > MOVEMENT_TOLERANCE:
            changed.append(item)
        else:
            unchanged.append(item)

    for identity in sorted(set(opening_by_identity) & set(latest_by_identity)):
        previous = opening_by_identity[identity]
        current = latest_by_identity[identity]
        matched_opening.add(id(previous))
        matched_latest.add(id(current))
        record_pair(previous, current)

    fallback_markets = {"asian_handicap"}
    for market in fallback_markets:
        previous_candidates = [
            entry
            for entry in opening
            if id(entry) not in matched_opening and _market_family_name(str(entry.get("market", ""))) == market
        ]
        current_candidates = [
            entry
            for entry in latest
            if id(entry) not in matched_latest and _market_family_name(str(entry.get("market", ""))) == market
        ]
        previous_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        current_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for entry in previous_candidates:
            previous_groups[str(entry.get("period", "")).strip()].append(entry)
        for entry in current_candidates:
            current_groups[str(entry.get("period", "")).strip()].append(entry)

        for period in sorted(set(previous_groups) & set(current_groups)):
            previous_group = previous_groups[period]
            current_group = current_groups[period]
            if len(previous_group) == 1 and len(current_group) == 1:
                previous = previous_group[0]
                current = current_group[0]
                matched_opening.add(id(previous))
                matched_latest.add(id(current))
                record_pair(previous, current)

    for entry in opening:
        if id(entry) in matched_opening:
            continue
        market, period, line = _consensus_identity(entry)
        missing_snapshots.append(
            {
                "market": market,
                "period": period,
                "line": None if line == "None" else line,
                "missing": ["current", "t-10min"],
            }
        )
    for entry in latest:
        if id(entry) in matched_latest:
            continue
        market, period, line = _consensus_identity(entry)
        missing_snapshots.append(
            {
                "market": market,
                "period": period,
                "line": None if line == "None" else line,
                "missing": ["opening"],
            }
        )
    return {
        "changed": changed,
        "unchanged": unchanged,
        "missing_snapshots": missing_snapshots,
    }


def _classify_news_item(item: dict[str, Any]) -> str:
    explicit = str(item.get("category") or item.get("classification") or "").strip().lower()
    if explicit in {"confirmed", "credible_unconfirmed", "narrative"}:
        return explicit
    if item.get("confirmed") is True:
        return "confirmed"
    if item.get("credible") is True:
        return "credible_unconfirmed"
    return "narrative"


def _normalize_news_items(news: Any) -> list[dict[str, Any]]:
    if not isinstance(news, list):
        return []
    normalized = []
    for item in news:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                **item,
                "classification": _classify_news_item(item),
            }
        )
    return normalized


def _sorted_score_matrix(matrix: Any) -> list[dict[str, Any]]:
    normalized = _normalize_matrix(matrix)
    scores = []
    for home_goals, row in enumerate(normalized):
        for away_goals, probability in enumerate(row):
            scores.append(
                {
                    "score": f"{home_goals}-{away_goals}",
                    "home_goals": home_goals,
                    "away_goals": away_goals,
                    "probability": probability,
                }
            )
    scores.sort(key=lambda item: (-item["probability"], item["home_goals"], item["away_goals"]))
    return scores


def _score_ladder(matrix: Any) -> list[dict[str, Any]]:
    candidates = _sorted_score_matrix(matrix)
    buckets = (
        ("low-score", lambda item: item["home_goals"] + item["away_goals"] <= 2),
        (
            "central",
            lambda item: 1 <= item["home_goals"] + item["away_goals"] <= 3 and abs(item["home_goals"] - item["away_goals"]) <= 1,
        ),
        ("high-variance", lambda item: item["home_goals"] + item["away_goals"] >= 4 or abs(item["home_goals"] - item["away_goals"]) >= 2),
    )
    used_scores: set[str] = set()
    ladder: list[dict[str, Any]] = []
    for label, predicate in buckets:
        chosen = next((item for item in candidates if predicate(item) and item["score"] not in used_scores), None)
        if chosen is None:
            chosen = next(item for item in candidates if item["score"] not in used_scores)
        used_scores.add(chosen["score"])
        ladder.append({"label": label, "score": chosen["score"], "probability": chosen["probability"]})
    return ladder


def _selection_probability(probabilities: dict[str, Any], key: str) -> float | None:
    value = probabilities.get(key)
    return None if value is None else float(value)


def _qualification_output(consensus: dict[str, dict[str, Any]], teams: tuple[str, str]) -> dict[str, Any] | None:
    candidates = [
        entry
        for entry in consensus.values()
        if isinstance(entry, dict)
        and _market_family_name(str(entry.get("market", ""))) == "to_qualify"
        and str(entry.get("snapshot", "")).strip().lower() in {"current", "t-10min"}
    ]
    if not candidates:
        return None
    entry = max(candidates, key=lambda item: _snapshot_priority(str(item.get("snapshot", ""))))
    probabilities = entry.get("probabilities")
    if not isinstance(probabilities, dict) or not probabilities:
        return None
    display_probabilities = _display_probability_map(probabilities, teams)
    favorite = max(display_probabilities.items(), key=lambda item: item[1])[0]
    return {
        "favorite": favorite,
        "probabilities": display_probabilities,
        "snapshot": entry.get("snapshot"),
        "period": entry.get("period"),
        "independent_books": entry.get("independent_books"),
    }


def _totals_output(
    latest_entries: dict[tuple[str, str, str], dict[str, Any]],
    matrix: Any,
) -> list[dict[str, Any]]:
    totals = []
    for identity in sorted(latest_entries):
        entry = latest_entries[identity]
        if _market_family_name(identity[0]) != "totals":
            continue
        line = _coerce_quarter_line(entry.get("line"), "line")
        over_settlement = settle_total(matrix, side="over", line=line)
        under_settlement = settle_total(matrix, side="under", line=line)
        totals.append(
            {
                "line": line,
                "snapshot": entry.get("snapshot"),
                "independent_books": entry.get("independent_books"),
                "market_probabilities": {
                    "over": _selection_probability(entry.get("probabilities", {}), "over"),
                    "under": _selection_probability(entry.get("probabilities", {}), "under"),
                },
                "model_probabilities": {
                    "over": _selection_probability_from_settlement(over_settlement),
                    "under": _selection_probability_from_settlement(under_settlement),
                },
                "settlement": {"over": over_settlement, "under": under_settlement},
            }
        )
    return totals


def _asian_handicap_output(
    latest_entries: dict[tuple[str, str, str], dict[str, Any]],
    matrix: Any,
) -> list[dict[str, Any]]:
    handicaps = []
    for identity in sorted(latest_entries):
        entry = latest_entries[identity]
        if _market_family_name(identity[0]) != "asian_handicap":
            continue
        line = abs(_coerce_quarter_line(entry.get("line"), "line"))
        market_probabilities = entry.get("probabilities", {})
        home_line = _coerce_quarter_line(entry.get("home_line", -line), "home_line")
        away_line = _coerce_quarter_line(entry.get("away_line", -home_line), "away_line")
        if not math.isclose(home_line, -away_line, rel_tol=0.0, abs_tol=1e-12) or not math.isclose(
            abs(home_line), line, rel_tol=0.0, abs_tol=1e-12
        ):
            raise ValueError("asian_handicap consensus requires mirrored home/away lines")
        home_settlement = settle_asian_handicap(matrix, side="home", line=home_line)
        away_settlement = settle_asian_handicap(matrix, side="away", line=away_line)
        handicaps.append(
            {
                "line": line,
                "home_line": home_line,
                "away_line": away_line,
                "snapshot": entry.get("snapshot"),
                "independent_books": entry.get("independent_books"),
                "market_probabilities": {
                    "home": _selection_probability(market_probabilities, "home"),
                    "away": _selection_probability(market_probabilities, "away"),
                },
                "model_probabilities": {
                    "home": _selection_probability_from_settlement(home_settlement),
                    "away": _selection_probability_from_settlement(away_settlement),
                },
                "settlement": {
                    "home": home_settlement,
                    "away": away_settlement,
                },
            }
        )
    return handicaps


def _cross_market_conflicts(
    probabilities_90m: dict[str, float],
    asian_handicap: list[dict[str, Any]],
    movement: dict[str, list[dict[str, Any]]],
    teams: tuple[str, str],
) -> list[dict[str, Any]]:
    favorite = max(probabilities_90m, key=probabilities_90m.__getitem__)
    if favorite not in {"home", "away"} or probabilities_90m[favorite] < 0.5:
        return []

    result_movement = next(
        (
            item
            for item in movement.get("changed", [])
            if _market_family_name(str(item.get("market", ""))) == "1x2"
            and str(item.get("period", "")) == "90m"
        ),
        None,
    )
    if result_movement is None:
        return []
    favorite_delta = _finite_number(result_movement.get("deltas", {}).get(favorite))
    if favorite_delta is None or favorite_delta <= MOVEMENT_TOLERANCE:
        return []

    favorite_line_key = f"{favorite}_line"
    current_handicap = next(
        (
            entry
            for entry in asian_handicap
            if (_finite_number(entry.get(favorite_line_key)) or 0.0) < 0.0
        ),
        None,
    )
    if current_handicap is None:
        return []

    current_line = _finite_number(current_handicap.get(favorite_line_key))
    handicap_movement = next(
        (
            item
            for item in movement.get("changed", [])
            if _market_family_name(str(item.get("market", ""))) == "asian_handicap"
            and item.get("opening_line") is not None
            and item.get("line") is not None
        ),
        None,
    )
    if current_line is None or handicap_movement is None:
        return []

    opening_magnitude = _finite_number(handicap_movement.get("opening_line"))
    current_magnitude = _finite_number(handicap_movement.get("line"))
    if (
        opening_magnitude is None
        or current_magnitude is None
        or abs(current_magnitude) + MOVEMENT_TOLERANCE >= abs(opening_magnitude)
    ):
        return []

    favorite_name = teams[0] if favorite == "home" else teams[1]
    return [
        {
            "code": "favorite_win_but_cover_risk",
            "favorite": favorite_name,
            "result_signal": {
                "probability": probabilities_90m[favorite],
                "movement_pp": favorite_delta * 100.0,
            },
            "handicap_signal": {
                "opening_line": -abs(opening_magnitude),
                "current_line": current_line,
                "direction": "weakened",
            },
            "read": (
                "favorite result probability strengthened while the handicap weakened; "
                "prefer a narrow-win or failed-cover interpretation over a blowout"
            ),
        }
    ]


def _forecast_event_id(
    match: dict[str, Any],
    teams: list[str],
    kickoff: Any,
) -> str:
    explicit = match.get("event_id")
    if explicit is not None:
        if not isinstance(explicit, str) or not explicit.strip():
            raise ValueError("event_id must be a non-empty string")
        return explicit.strip()
    identity = {
        "competition": match.get("competition"),
        "match": match.get("match"),
        "teams": teams,
        "kickoff": kickoff,
    }
    return f"event-{canonical_hash(identity)[:24]}"


def _forecast_alert_offset(
    match: dict[str, Any],
    kickoff: Any,
    as_of: Any,
) -> str:
    explicit = match.get("alert_offset")
    if explicit is not None:
        if not isinstance(explicit, str) or not explicit.strip():
            raise ValueError("alert_offset must be a non-empty string")
        return explicit.strip()
    kickoff_time = _coerce_datetime(kickoff)
    forecast_time = _coerce_datetime(as_of)
    if kickoff_time is None or forecast_time is None:
        return "unknown"
    minutes = (kickoff_time - forecast_time).total_seconds() / 60.0
    if minutes < 0:
        return "started"
    nearest = min(ALERT_OFFSETS, key=lambda candidate: abs(candidate - minutes))
    if abs(nearest - minutes) <= 15.0:
        return ALERT_OFFSETS[nearest]
    return f"T-{int(round(minutes))}min"


def build_forecast_record(
    match: dict[str, Any],
    analysis: dict[str, Any],
    matrix: list[list[float]],
    profile: Mapping[str, Any],
) -> dict[str, Any]:
    raw_match = _json_ready(copy.deepcopy(match))
    profile_snapshot = _json_ready(profile)
    input_fingerprint = canonical_hash(raw_match)
    profile_fingerprint = canonical_hash(profile_snapshot)
    event_id = _forecast_event_id(match, analysis["teams"], analysis.get("kickoff"))
    alert_offset = _forecast_alert_offset(match, analysis.get("kickoff"), analysis.get("as_of"))
    score_distribution = {
        f"{home_goals}-{away_goals}": probability
        for home_goals, row in enumerate(matrix)
        for away_goals, probability in enumerate(row)
    }

    probabilities_90m = dict(analysis["probabilities_90m"])
    one_x_two_pick = max(probabilities_90m, key=probabilities_90m.__getitem__)
    totals = []
    for item in analysis["totals"]:
        normalized = _json_ready(item)
        probabilities = normalized.get("model_probabilities", {})
        normalized["period"] = "90m"
        normalized["pick"] = max(probabilities, key=probabilities.__getitem__) if probabilities else None
        totals.append(normalized)
    handicaps = []
    for item in analysis["asian_handicap"]:
        normalized = _json_ready(item)
        probabilities = normalized.get("model_probabilities", {})
        normalized["period"] = "90m"
        normalized["pick"] = max(probabilities, key=probabilities.__getitem__) if probabilities else None
        handicaps.append(normalized)

    qualification = _json_ready(analysis.get("qualification"))
    if qualification is not None:
        qualification["period"] = "qualification"

    forecast_identity = {
        "event_id": event_id,
        "as_of": analysis.get("as_of"),
        "alert_offset": alert_offset,
        "input_fingerprint": input_fingerprint,
        "profile_fingerprint": profile_fingerprint,
        "engine_version": FORECAST_ENGINE_VERSION,
    }
    return {
        "schema_version": FORECAST_RECORD_SCHEMA_VERSION,
        "forecast_id": f"forecast-{canonical_hash(forecast_identity)[:24]}",
        "event_id": event_id,
        "match": analysis["match"],
        "competition": match.get("competition"),
        "teams": list(analysis["teams"]),
        "kickoff": analysis.get("kickoff"),
        "match_type": analysis.get("match_type"),
        "as_of": analysis.get("as_of"),
        "alert_offset": alert_offset,
        "forecast_status": analysis.get("forecast_status"),
        "actionable_forecast": analysis.get("actionable_forecast"),
        "markets": {
            "1x2": {
                "period": "90m",
                "probabilities": probabilities_90m,
                "pick": one_x_two_pick,
            },
            "qualification": qualification,
            "totals": totals,
            "btts": {
                "period": "90m",
                "probabilities": _json_ready(analysis["btts"]),
                "pick": max(analysis["btts"], key=analysis["btts"].__getitem__),
            },
            "asian_handicap": handicaps,
            "correct_score": {
                "period": "90m",
                "displayed": _json_ready(analysis["exact_scores"]),
            },
        },
        "probabilities_90m": probabilities_90m,
        "expected_goals": _json_ready(analysis["expected_goals"]),
        "score_distribution_90m": score_distribution,
        "score_ladder": _json_ready(analysis["score_ladder"]),
        "confidence": _json_ready(analysis["confidence"]),
        "source_coverage": _json_ready(analysis["source_coverage"]),
        "cross_market_conflicts": _json_ready(analysis["cross_market_conflicts"]),
        "profile_id": str(profile["profile_id"]),
        "profile_fingerprint": profile_fingerprint,
        "profile": profile_snapshot,
        "engine_version": FORECAST_ENGINE_VERSION,
        "input_fingerprint": input_fingerprint,
        "raw_match": raw_match,
    }


def analyze_v2_match(
    match: dict[str, Any],
    *,
    as_of: datetime | str | None = None,
    profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(match, dict):
        raise ValueError("match must be an object")
    active_profile = (
        DEFAULT_MODEL_PROFILE
        if profile is None
        else model_profile.validate_profile(profile)
    )
    quotes = match.get("quotes")
    if not isinstance(quotes, list) or not quotes:
        raise ValueError("quotes are required for v2 analysis")
    lineup_confirmed = _require_bool("lineup_confirmed", match.get("lineup_confirmed"))

    teams_list = match.get("teams") if isinstance(match.get("teams"), list) else ["Team A", "Team B"]
    teams = (
        teams_list[0] if len(teams_list) > 0 else "Team A",
        teams_list[1] if len(teams_list) > 1 else "Team B",
    )
    kickoff = _coerce_datetime(match.get("kickoff"))
    latest_quote_time = _latest_timestamp(quotes)
    resolved_as_of = _coerce_datetime(as_of) or _coerce_datetime(match.get("observed_at")) or latest_quote_time

    context_errors = validate_match_context(match)
    deduped_quotes, dedupe_diagnostics = deduplicate_quotes(
        quotes,
        active_profile["source_weights"],
    )
    live_quote_count = sum(
        1
        for quote in deduped_quotes
        if str(quote.get("snapshot", "")).strip().lower() == "live"
    )
    consensus = build_consensus(
        quotes,
        as_of=resolved_as_of,
        source_weights=active_profile["source_weights"],
        recency_weights=active_profile["recency_weights"],
    )
    latest_entries = _latest_snapshot_entries(consensus)
    latest_entries_all = _latest_snapshot_entries(consensus, period=None)
    fit_consensus = _fit_consensus_from_latest(consensus)
    if not fit_consensus and live_quote_count:
        raise ValueError(
            "live-only snapshots are unsupported by the pre-match model; "
            "provide current or t-10min pre-match quotes"
        )
    fit = fit_expected_goals(
        fit_consensus,
        family_caps=active_profile["fit_family_caps"],
    )
    matrix = poisson_matrix(fit["home_xg"], fit["away_xg"], FIT_MAX_GOALS)
    metrics = fit["metrics"]

    match_type = _normalize_match_type(match.get("match_type"))
    usable_independent_books, core_90m_books_by_family = _core_90m_source_coverage(latest_entries)
    qualification_independent_books, qualification_books = _qualification_source_coverage(latest_entries_all)
    missing_fields = _missing_market_fields(latest_entries_all, match_type=match_type)
    market_families = _available_market_families(latest_entries_all)
    confidence_market_families = {
        family
        for family, books in core_90m_books_by_family.items()
        if len(books) >= 2
    }
    pre_match_evidence_quotes = [
        quote for quote in deduped_quotes if _supported_latest_quote(quote)
    ]
    freshest_age_minutes = _freshest_age_minutes(resolved_as_of, pre_match_evidence_quotes)
    max_dispersion = _mean_market_dispersion(list(latest_entries_all.values()))
    match_started = bool(kickoff is not None and resolved_as_of is not None and resolved_as_of >= kickoff)
    near_kickoff = bool(
        kickoff is not None
        and resolved_as_of is not None
        and (kickoff - resolved_as_of).total_seconds() <= (3 * 60 * 60)
    )

    confidence = score_evidence(
        independent_books=usable_independent_books,
        freshest_age_minutes=freshest_age_minutes,
        market_families=len(confidence_market_families),
        max_dispersion=max_dispersion,
        fit_residual=fit["residual"],
        lineup_confirmed=lineup_confirmed,
        match_started=match_started,
        # This engine has no score/minute state, so supplied live quotes are never
        # treated as evidence that can revive an already-started pre-match forecast.
        has_live_quotes=False,
        match_type=match_type,
        near_kickoff=near_kickoff,
        match=match,
        context_errors=context_errors,
        confidence_thresholds=active_profile["confidence_thresholds"],
    )

    probabilities_90m = {
        "home": metrics["home"],
        "draw": metrics["draw"],
        "away": metrics["away"],
    }
    favorite_90m = max(probabilities_90m.items(), key=lambda item: item[1])[0]
    qualification = _qualification_output(consensus, teams)
    news = _normalize_news_items(match.get("news"))
    totals = _totals_output(latest_entries, matrix)
    asian_handicap = _asian_handicap_output(latest_entries, matrix)
    movement = _movement_report(consensus)
    cross_market_conflicts = _cross_market_conflicts(
        probabilities_90m,
        asian_handicap,
        movement,
        teams,
    )
    confidence = apply_cross_market_conflict_penalty(
        confidence,
        cross_market_conflicts,
        active_profile["cross_market_conflict_penalty"],
        active_profile["confidence_thresholds"],
    )

    result = {
        "schema_version": "2.0",
        "as_of": resolved_as_of.isoformat() if resolved_as_of else None,
        "match": match.get("match") or f"{teams[0]} vs {teams[1]}",
        "teams": [teams[0], teams[1]],
        "kickoff": match.get("kickoff"),
        "forecast_mode": "frozen_pre_match" if match_started else "pre_match",
        "forecast_status": "no_forecast_edge" if confidence["abstain"] else "forecast",
        "actionable_forecast": not confidence["abstain"],
        "match_type": match_type,
        "lineup_confirmed": lineup_confirmed,
        "probabilities_90m": probabilities_90m,
        "favorite_90m": _display_team_selection(favorite_90m, teams),
        "expected_goals": {"home": fit["home_xg"], "away": fit["away_xg"]},
        "btts": {"yes": metrics["btts_yes"], "no": metrics["btts_no"]},
        "totals": totals,
        "asian_handicap": asian_handicap,
        "cross_market_conflicts": cross_market_conflicts,
        "qualification": qualification,
        "exact_scores": _sorted_score_matrix(matrix)[:5],
        "score_ladder": _score_ladder(matrix),
        "movement": movement,
        "source_coverage": {
            "independent_books": usable_independent_books,
            "core_90m_books_by_family": core_90m_books_by_family,
            "qualification_independent_books": qualification_independent_books,
            "qualification_books": qualification_books,
            "freshest_age_minutes": freshest_age_minutes,
            "market_families": len(market_families),
            "confidence_market_families": len(confidence_market_families),
            "confidence_market_family_names": sorted(confidence_market_families),
            "raw_quotes": len(quotes),
            "deduped_quotes": len(deduped_quotes),
        },
        "confidence": confidence,
        "abstention": {
            "abstain": confidence["abstain"],
            "reasons": confidence["abstain_reasons"],
        },
        "news": news,
        "missing_fields": missing_fields,
        "diagnostics": {
            "context_errors": context_errors,
            "deduplication": dedupe_diagnostics,
            "consensus": consensus,
            "fit": {
                "residual": fit["residual"],
                "objective": fit["objective"],
                "family_weights": fit["diagnostics"]["family_weights"],
                "targets": fit["diagnostics"]["targets"],
            },
            "live_quotes": {
                "provided": live_quote_count,
                "used": 0,
                "policy": "unsupported by the pre-match model and ignored",
            },
            "missing_markets": missing_fields,
            "score_evidence": confidence,
        },
    }
    result["forecast_record"] = build_forecast_record(
        match,
        result,
        matrix,
        active_profile,
    )
    return result


def american_to_prob(odds: float) -> float:
    if odds < 0:
        return abs(odds) / (abs(odds) + 100.0)
    return 100.0 / (odds + 100.0)


def decimal_to_prob(odds: float) -> float:
    return 1.0 / odds


def to_prob(value: Any) -> float | None:
    if value is None or value == "":
        return None
    if isinstance(value, str):
        value = value.strip()
        if value.startswith("+"):
            value = value[1:]
        if "/" in value:
            try:
                numerator, denominator = value.split("/", 1)
                fractional = float(numerator) / float(denominator)
            except ValueError:
                return None
            return 1.0 / (fractional + 1.0)
        try:
            number = float(value)
        except ValueError:
            return None
    else:
        number = float(value)
    if number <= 0:
        return american_to_prob(number)
    if number >= 100:
        return american_to_prob(number)
    if number > 1:
        return decimal_to_prob(number)
    return number


def pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.1f}%"


def water_odds_to_prob(value: Any, odds_format: str = "hong_kong") -> float | None:
    if value is None or value == "":
        return None
    try:
        odds = float(str(value).strip())
    except ValueError:
        return None

    fmt = odds_format.lower().replace("-", "_").replace(" ", "_")
    if fmt in {"hong_kong", "hk", "asian"}:
        if odds <= 0:
            return None
        return 1.0 / (1.0 + odds)
    if fmt in {"decimal", "eu", "european"}:
        return decimal_to_prob(odds) if odds > 1 else None
    if fmt in {"american", "us"}:
        return american_to_prob(odds)
    if fmt in {"malay", "malaysian"}:
        if odds > 0:
            return 1.0 / (1.0 + odds)
        return abs(odds) / (1.0 + abs(odds))
    if fmt in {"indo", "indonesian"}:
        if odds > 1:
            return 1.0 / (1.0 + odds)
        if odds < -1:
            return abs(odds) / (1.0 + abs(odds))
        return None
    return None


def movement(opening: float | None, current: float | None, team: str) -> str:
    if opening is None or current is None:
        return f"{team}: missing opening/current odds; cannot infer movement."
    delta = current - opening
    if abs(delta) < 0.015:
        return f"{team}: stable price; no strong movement signal."
    if delta > 0:
        return f"{team}: implied probability up {delta * 100:.1f} pp; market support strengthened."
    return f"{team}: implied probability down {abs(delta) * 100:.1f} pp; drift warning."


def analyze_asian_handicap(match: dict[str, Any], favorite: str | None) -> dict[str, Any] | None:
    asian = match.get("asian_handicap") or match.get("ah")
    if not asian:
        return None

    ah_favorite = asian.get("favorite") or favorite
    opening_line = asian.get("opening_line")
    current_line = asian.get("current_line")
    opening_odds = asian.get("opening_odds")
    current_odds = asian.get("current_odds")
    odds_format = asian.get("odds_format", "hong_kong")

    try:
        opening_line_num = float(opening_line) if opening_line is not None else None
        current_line_num = float(current_line) if current_line is not None else None
    except ValueError:
        opening_line_num = None
        current_line_num = None

    opening_prob = water_odds_to_prob(opening_odds, odds_format)
    current_prob = water_odds_to_prob(current_odds, odds_format)

    line_movement = "unknown"
    if opening_line_num is not None and current_line_num is not None:
        if abs(current_line_num - opening_line_num) < 0.01:
            line_movement = "stable"
        elif current_line_num < opening_line_num:
            line_movement = "strengthened"
        else:
            line_movement = "weakened"

    odds_movement = "unknown"
    if opening_prob is not None and current_prob is not None:
        if abs(current_prob - opening_prob) < 0.015:
            odds_movement = "stable"
        elif current_prob > opening_prob:
            odds_movement = "support_strengthened"
        else:
            odds_movement = "support_weakened"

    cover_read = "neutral"
    if line_movement == "strengthened" and odds_movement != "support_weakened":
        cover_read = "favorite_cover_confirmed"
    elif line_movement == "weakened" or odds_movement == "support_weakened":
        cover_read = "favorite_win_but_cover_risk"
    elif line_movement == "stable" and current_line_num is not None and current_line_num <= -1.25:
        cover_read = "deep_line_needs_confirmation"

    return {
        "favorite": ah_favorite,
        "opening_line": opening_line,
        "current_line": current_line,
        "odds_format": odds_format,
        "opening_implied_probability": pct(opening_prob),
        "current_implied_probability": pct(current_prob),
        "line_movement": line_movement,
        "odds_movement": odds_movement,
        "cover_read": cover_read,
    }


def score_hints(total_lean: str, btts_lean: str, favorite_firm: bool, draw_live: bool) -> list[str]:
    total = total_lean.lower()
    btts = btts_lean.lower()
    if "under" in total and "yes" in btts:
        base = ["1-1", "1-0", "0-0"]
    elif "under" in total and "no" in btts:
        base = ["1-0", "2-0", "0-0"]
    elif "over" in total and "yes" in btts:
        base = ["2-1", "2-2", "3-1"]
    elif "over" in total:
        base = ["2-0", "3-0", "3-1"]
    else:
        base = ["2-1", "1-1", "1-0"]
    if draw_live and "1-1" not in base:
        base.insert(0, "1-1")
    if favorite_firm and "2-0" not in base and "under" in total:
        base.insert(1, "2-0")
    return base[:3]


def analyze_match(match: dict[str, Any]) -> dict[str, Any]:
    teams = match.get("teams", ["Team A", "Team B"])
    home, away = teams[0], teams[1]
    ml = match.get("moneyline", {})
    opening = ml.get("opening", {})
    current = ml.get("current", {})
    home_open = to_prob(opening.get(home) or opening.get("home"))
    away_open = to_prob(opening.get(away) or opening.get("away"))
    draw_open = to_prob(opening.get("draw"))
    home_now = to_prob(current.get(home) or current.get("home"))
    away_now = to_prob(current.get(away) or current.get("away"))
    draw_now = to_prob(current.get("draw"))

    favorite = None
    if home_now is not None and away_now is not None:
        favorite = home if home_now >= away_now else away
    favorite_prob = max([p for p in [home_now, away_now] if p is not None], default=None)
    draw_live = bool(draw_now is not None and draw_now >= 0.27)

    fav_open = home_open if favorite == home else away_open
    fav_now = home_now if favorite == home else away_now
    favorite_firm = bool(fav_open is not None and fav_now is not None and fav_now >= fav_open + 0.015)
    favorite_drift = bool(fav_open is not None and fav_now is not None and fav_now <= fav_open - 0.015)

    total_lean = match.get("totals", {}).get("lean", "unknown")
    btts_lean = match.get("btts", {}).get("lean", "unknown")
    scores = score_hints(total_lean, btts_lean, favorite_firm, draw_live or favorite_drift)
    asian_read = analyze_asian_handicap(match, favorite)

    risk_flags: list[str] = []
    if favorite_drift:
        risk_flags.append("热门退盘: 防平/冷门/受让方向。")
    if draw_live:
        risk_flags.append("平局概率不低: 淘汰赛需防加时或点球。")
    if "under" in str(total_lean).lower():
        risk_flags.append("小球倾向: 让球穿盘风险上升。")
    if match.get("news_risk"):
        risk_flags.append("消息面可能偏情绪盘，需看让球和大小球是否确认。")
    if asian_read and asian_read["cover_read"] == "favorite_win_but_cover_risk":
        risk_flags.append("亚盘不支持深盘穿盘: 热门可胜但让球有风险。")
    if asian_read and asian_read["cover_read"] == "deep_line_needs_confirmation":
        risk_flags.append("亚盘深盘未继续强化: 大胜需要临场确认。")

    market_read = {
        "favorite_firm": favorite_firm,
        "favorite_drift": favorite_drift,
        "draw_live": draw_live,
        "totals": total_lean,
        "btts": btts_lean,
    }
    if asian_read:
        market_read["asian_handicap"] = asian_read

    return {
        "match": f"{home} vs {away}",
        "kickoff": match.get("kickoff"),
        "implied_probabilities": {
            home: pct(home_now),
            "draw": pct(draw_now),
            away: pct(away_now),
        },
        "movement": [
            movement(home_open, home_now, home),
            movement(draw_open, draw_now, "Draw"),
            movement(away_open, away_now, away),
        ],
        "favorite": favorite,
        "favorite_probability": pct(favorite_prob),
        "market_read": market_read,
        "score_ladder": scores,
        "risk_flags": risk_flags or ["No major market warning from provided data."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="JSON file with a match object or {matches:[...]}.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    parser.add_argument("--as-of", help="ISO timestamp used to score freshness for V2 inputs.")
    parser.add_argument("--profile", help="Validated model profile JSON. Defaults to the packaged profile.")
    parser.add_argument("--record-out", help="Append V2 forecast records to this JSONL ledger.")
    parser.add_argument(
        "--data-dir",
        help="Data directory used for forecasts.jsonl when --record-out is omitted.",
    )
    parser.add_argument(
        "--no-record",
        action="store_true",
        help="Return the forecast without writing a ledger record.",
    )
    args = parser.parse_args()
    if args.no_record and (args.record_out or args.data_dir):
        parser.error("--no-record cannot be combined with --record-out or --data-dir")

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    matches = data.get("matches") if isinstance(data, dict) else None
    if matches is None:
        matches = [data]
    active_profile = model_profile.load_profile(args.profile) if args.profile else None
    analyzed_matches = []
    for match in matches:
        if isinstance(match, Mapping) and isinstance(match.get("quotes"), list):
            analyzed_matches.append(
                analyze_v2_match(match, as_of=args.as_of, profile=active_profile)
            )
        else:
            analyzed_matches.append(analyze_match(match))

    if args.no_record:
        record_path = None
    elif args.record_out:
        record_path = Path(args.record_out).expanduser()
    else:
        record_path = model_profile.resolve_data_dir(args.data_dir) / "forecasts.jsonl"
    if record_path is not None:
        records = [
            analyzed["forecast_record"]
            for analyzed in analyzed_matches
            if isinstance(analyzed.get("forecast_record"), dict)
        ]
        if records:
            append_unique_jsonl_batch(record_path, records, "forecast_id")

    result = {"matches": analyzed_matches}
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
