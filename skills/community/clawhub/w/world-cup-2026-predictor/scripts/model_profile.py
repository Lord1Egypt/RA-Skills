#!/usr/bin/env python3
"""Load and validate bounded football forecasting model profiles."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any


PROFILE_SCHEMA_VERSION = "1.0"
MAX_RELATIVE_CHANGE = 0.10
MAX_ZERO_BASELINE_CONFLICT_STEP = 2.5
DEFAULT_PROFILE_PATH = Path(__file__).resolve().parents[1] / "profiles" / "default.json"
REQUIRED_PROFILE_KEYS = {
    "schema_version",
    "profile_id",
    "parent_id",
    "source_weights",
    "fit_family_caps",
    "recency_weights",
    "confidence_thresholds",
    "cross_market_conflict_penalty",
}
OPTIONAL_PROFILE_KEYS = {"evolution"}
PROFILE_KEYS = REQUIRED_PROFILE_KEYS | OPTIONAL_PROFILE_KEYS
EVOLUTION_KEYS = {
    "schema_version",
    "created_at",
    "training_cutoff",
    "training_record_ids",
    "holdout_record_ids",
    "metrics",
    "parameter_diff",
    "promotion_decision",
    "evaluation_fingerprint",
}
SECTION_KEYS = {
    "source_weights": {"A", "B", "C", "D"},
    "fit_family_caps": {"1x2", "totals", "btts"},
    "recency_weights": {"0_15", "15_60", "60_180", "older"},
    "confidence_thresholds": {"high", "medium"},
}
ABSOLUTE_BOUNDS = {
    "source_weights": {
        "A": (0.1, 2.0),
        "B": (0.1, 2.0),
        "C": (0.1, 2.0),
        "D": (0.0, 0.0),
    },
    "fit_family_caps": {
        "1x2": (0.1, 2.0),
        "totals": (0.0, 2.0),
        "btts": (0.0, 2.0),
    },
    "recency_weights": {
        "0_15": (0.1, 1.0),
        "15_60": (0.0, 1.0),
        "60_180": (0.0, 1.0),
        "older": (0.0, 1.0),
    },
    "confidence_thresholds": {
        "high": (0.0, 100.0),
        "medium": (0.0, 100.0),
    },
}
CROSS_MARKET_CONFLICT_PENALTY_BOUNDS = (0.0, 25.0)
ACTIVE_PROFILE_FILENAME = "active-profile.json"
PROFILE_ARTIFACTS_DIRNAME = "profiles"
PROFILE_LOCK_FILENAME = ".active-profile.lock"
SAFE_PROFILE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def _finite_nonnegative(value: Any, field_name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be numeric")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be numeric") from exc
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{field_name} must be finite and non-negative")
    return number


def _bounded_number(value: Any, field_name: str, bounds: tuple[float, float]) -> float:
    number = _finite_nonnegative(value, field_name)
    minimum, maximum = bounds
    if number < minimum or number > maximum:
        raise ValueError(f"{field_name} must be between {minimum:g} and {maximum:g}")
    return number


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _aware_iso_timestamp(value: Any, field_name: str, *, allow_none: bool = False) -> str | None:
    if value is None and allow_none:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a timezone-aware ISO timestamp")
    text = value.strip()
    if text.endswith(("Z", "z")):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a timezone-aware ISO timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field_name} must be a timezone-aware ISO timestamp")
    return parsed.isoformat()


def _validated_json_value(value: Any, field_name: str) -> Any:
    if value is None or isinstance(value, (str, bool)):
        return copy.deepcopy(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{field_name} must not contain non-finite numbers")
        return value
    if isinstance(value, list):
        return [
            _validated_json_value(item, f"{field_name}[{index}]")
            for index, item in enumerate(value)
        ]
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise ValueError(f"{field_name} keys must be strings")
        return {
            key: _validated_json_value(value[key], f"{field_name}.{key}")
            for key in sorted(value)
        }
    raise ValueError(f"{field_name} must contain only JSON values")


def _record_id_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    normalized: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{field_name} must contain non-empty strings")
        normalized.append(item.strip())
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"{field_name} must not contain duplicates")
    return normalized


def _validate_evolution_metadata(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != EVOLUTION_KEYS:
        raise ValueError(f"evolution must contain exactly {sorted(EVOLUTION_KEYS)}")
    if value.get("schema_version") != PROFILE_SCHEMA_VERSION:
        raise ValueError("unsupported evolution schema_version")
    fingerprint = value.get("evaluation_fingerprint")
    if not isinstance(fingerprint, str) or re.fullmatch(r"[0-9a-f]{64}", fingerprint) is None:
        raise ValueError("evolution.evaluation_fingerprint must be a SHA-256 hex digest")
    metrics = value.get("metrics")
    parameter_diff = value.get("parameter_diff")
    promotion_decision = value.get("promotion_decision")
    if not isinstance(metrics, dict):
        raise ValueError("evolution.metrics must be an object")
    if not isinstance(parameter_diff, dict):
        raise ValueError("evolution.parameter_diff must be an object")
    if not isinstance(promotion_decision, dict):
        raise ValueError("evolution.promotion_decision must be an object")
    normalized = {
        "schema_version": PROFILE_SCHEMA_VERSION,
        "created_at": _aware_iso_timestamp(value.get("created_at"), "evolution.created_at"),
        "training_cutoff": _aware_iso_timestamp(
            value.get("training_cutoff"),
            "evolution.training_cutoff",
            allow_none=True,
        ),
        "training_record_ids": _record_id_list(
            value.get("training_record_ids"),
            "evolution.training_record_ids",
        ),
        "holdout_record_ids": _record_id_list(
            value.get("holdout_record_ids"),
            "evolution.holdout_record_ids",
        ),
        "metrics": _validated_json_value(metrics, "evolution.metrics"),
        "parameter_diff": _validated_json_value(
            parameter_diff,
            "evolution.parameter_diff",
        ),
        "promotion_decision": _validated_json_value(
            promotion_decision,
            "evolution.promotion_decision",
        ),
        "evaluation_fingerprint": fingerprint,
    }
    fingerprint_payload = {
        key: normalized[key]
        for key in (
            "training_cutoff",
            "training_record_ids",
            "holdout_record_ids",
            "metrics",
            "parameter_diff",
            "promotion_decision",
        )
    }
    expected_fingerprint = hashlib.sha256(
        _canonical_json(fingerprint_payload).encode("utf-8")
    ).hexdigest()
    if fingerprint != expected_fingerprint:
        raise ValueError("evolution.evaluation_fingerprint does not match evidence")
    return normalized


def _safe_profile_identifier(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty safe file identifier")
    text = value.strip()
    if "/" in text or "\\" in text or ".." in text or not SAFE_PROFILE_ID_RE.fullmatch(text):
        raise ValueError(f"{field_name} must be a safe file identifier")
    return text


def _safe_optional_profile_identifier(value: Any, field_name: str) -> str | None:
    if value is None:
        return None
    return _safe_profile_identifier(value, field_name)


def _fsync_directory(path: Path) -> None:
    try:
        descriptor = os.open(path, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    except OSError:
        pass
    finally:
        os.close(descriptor)


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
            handle.write(_canonical_json(payload))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        _fsync_directory(path.parent)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


class _ActivationLock:
    def __init__(self, data_dir: Path) -> None:
        self.path = data_dir / PROFILE_LOCK_FILENAME
        self.descriptor: int | None = None

    def __enter__(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.descriptor = os.open(
                self.path,
                os.O_CREAT | os.O_RDWR,
                0o600,
            )
            if os.name == "nt":
                import msvcrt

                if os.fstat(self.descriptor).st_size == 0:
                    os.write(self.descriptor, b"\0")
                os.lseek(self.descriptor, 0, os.SEEK_SET)
                msvcrt.locking(self.descriptor, msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(self.descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (BlockingIOError, OSError) as exc:
            if self.descriptor is not None:
                os.close(self.descriptor)
                self.descriptor = None
            raise ValueError("concurrent profile activation is already in progress") from exc
        os.ftruncate(self.descriptor, 0)
        os.lseek(self.descriptor, 0, os.SEEK_SET)
        os.write(self.descriptor, str(os.getpid()).encode("utf-8"))
        os.fsync(self.descriptor)

    def __exit__(self, exc_type, exc, exc_tb) -> None:
        if self.descriptor is not None:
            if os.name == "nt":
                import msvcrt

                os.lseek(self.descriptor, 0, os.SEEK_SET)
                msvcrt.locking(self.descriptor, msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(self.descriptor, fcntl.LOCK_UN)
            os.close(self.descriptor)
            self.descriptor = None


def validate_profile(profile: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(profile, dict):
        raise ValueError("profile must be an object")
    unknown = set(profile) - PROFILE_KEYS
    missing = REQUIRED_PROFILE_KEYS - set(profile)
    if unknown:
        raise ValueError(f"unknown profile fields: {sorted(unknown)}")
    if missing:
        raise ValueError(f"missing profile fields: {sorted(missing)}")
    if profile["schema_version"] != PROFILE_SCHEMA_VERSION:
        raise ValueError("unsupported profile schema_version")
    if not isinstance(profile["profile_id"], str) or not profile["profile_id"].strip():
        raise ValueError("profile_id must be a non-empty string")
    if profile["parent_id"] is not None and (
        not isinstance(profile["parent_id"], str) or not profile["parent_id"].strip()
    ):
        raise ValueError("parent_id must be null or a non-empty string")
    source_weights = profile.get("source_weights")
    if isinstance(source_weights, dict) and source_weights.get("D") != 0.0:
        raise ValueError("Tier D must remain zero")

    normalized = copy.deepcopy(profile)
    for section, expected_keys in SECTION_KEYS.items():
        values = profile[section]
        if not isinstance(values, dict) or set(values) != expected_keys:
            raise ValueError(f"{section} must contain exactly {sorted(expected_keys)}")
        normalized[section] = {
            key: _bounded_number(
                values[key],
                f"{section}.{key}",
                ABSOLUTE_BOUNDS[section][key],
            )
            for key in sorted(expected_keys)
        }

    if normalized["confidence_thresholds"]["high"] <= normalized["confidence_thresholds"]["medium"]:
        raise ValueError("confidence high threshold must exceed medium")
    recency = normalized["recency_weights"]
    if not (
        recency["0_15"] >= recency["15_60"] >= recency["60_180"] >= recency["older"]
    ):
        raise ValueError("recency_weights must not increase with quote age")
    normalized["cross_market_conflict_penalty"] = _bounded_number(
        profile["cross_market_conflict_penalty"],
        "cross_market_conflict_penalty",
        CROSS_MARKET_CONFLICT_PENALTY_BOUNDS,
    )
    if "evolution" in profile:
        normalized["evolution"] = _validate_evolution_metadata(profile["evolution"])
    return normalized


def load_profile(path: str | Path | None = None) -> dict[str, Any]:
    profile_path = DEFAULT_PROFILE_PATH if path is None else Path(path).expanduser()
    try:
        value = json.loads(profile_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load profile {profile_path}: {exc}") from exc
    return validate_profile(value)


def validate_challenger(
    champion: dict[str, Any],
    challenger: dict[str, Any],
) -> dict[str, Any]:
    baseline = validate_profile(champion)
    candidate = validate_profile(challenger)
    sections = (*SECTION_KEYS, "cross_market_conflict_penalty")
    for section in sections:
        old_values = baseline[section] if isinstance(baseline[section], dict) else {section: baseline[section]}
        new_values = candidate[section] if isinstance(candidate[section], dict) else {section: candidate[section]}
        for key, old_value in old_values.items():
            new_value = new_values[key]
            if old_value == 0.0:
                if section == "cross_market_conflict_penalty":
                    if new_value <= MAX_ZERO_BASELINE_CONFLICT_STEP + 1e-12:
                        continue
                    raise ValueError(
                        "cross_market_conflict_penalty exceeds 10 percent bounded first change"
                    )
                if new_value != 0.0:
                    raise ValueError(f"{section}.{key} cannot change from zero")
                continue
            relative_change = abs(new_value - old_value) / abs(old_value)
            if relative_change > MAX_RELATIVE_CHANGE + 1e-12:
                raise ValueError(f"{section}.{key} exceeds 10 percent change")
    return candidate


def resolve_data_dir(cli_value: str | Path | None) -> Path:
    if cli_value is not None:
        return Path(cli_value).expanduser()
    configured = os.environ.get("FOOTBALL_FORECASTER_DATA_DIR")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".football-forecaster"


def _pointer_path(data_dir: str | Path | None) -> Path:
    return resolve_data_dir(data_dir) / ACTIVE_PROFILE_FILENAME


def _profile_artifacts_dir(data_dir: str | Path | None) -> Path:
    return resolve_data_dir(data_dir) / PROFILE_ARTIFACTS_DIRNAME


def _profile_artifact_path(data_dir: str | Path | None, profile_id: str) -> Path:
    safe_profile_id = _safe_profile_identifier(profile_id, "profile_id")
    return _profile_artifacts_dir(data_dir) / f"{safe_profile_id}.json"


def _load_profile_artifact(data_dir: str | Path | None, profile_id: str) -> dict[str, Any]:
    default_profile = load_profile(DEFAULT_PROFILE_PATH)
    safe_profile_id = _safe_profile_identifier(profile_id, "profile_id")
    if safe_profile_id == default_profile["profile_id"]:
        return default_profile
    path = _profile_artifact_path(data_dir, safe_profile_id)
    if not path.exists():
        raise ValueError(f"unknown active profile: {safe_profile_id}")
    profile = load_profile(path)
    if profile["profile_id"] != safe_profile_id:
        raise ValueError(f"profile artifact id mismatch for {safe_profile_id}")
    return profile


def _load_pointer(data_dir: str | Path | None) -> dict[str, Any]:
    path = _pointer_path(data_dir)
    try:
        pointer = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load active-profile pointer {path}: {exc}") from exc
    if not isinstance(pointer, dict):
        raise ValueError("active-profile pointer must be an object")
    if pointer.get("schema_version") != PROFILE_SCHEMA_VERSION:
        raise ValueError("unsupported active-profile schema_version")
    if set(pointer) != {"schema_version", "profile_id", "previous_profile_id"}:
        raise ValueError("active-profile pointer fields are invalid")
    pointer["profile_id"] = _safe_profile_identifier(pointer.get("profile_id"), "profile_id")
    pointer["previous_profile_id"] = _safe_optional_profile_identifier(
        pointer.get("previous_profile_id"),
        "previous_profile_id",
    )
    return pointer


def _write_profile_artifact(data_dir: str | Path | None, profile: dict[str, Any]) -> Path:
    artifact_path = _profile_artifact_path(data_dir, profile["profile_id"])
    if artifact_path.exists():
        existing = load_profile(artifact_path)
        if _canonical_json(existing) != _canonical_json(profile):
            raise ValueError(f"profile {profile['profile_id']} already exists with conflicting content")
        return artifact_path
    _atomic_write_json(artifact_path, profile)
    return artifact_path


def load_active_profile(data_dir: str | Path | None = None) -> dict[str, Any]:
    path = _pointer_path(data_dir)
    if not path.exists():
        return load_profile(DEFAULT_PROFILE_PATH)
    pointer = _load_pointer(data_dir)
    profile = _load_profile_artifact(data_dir, pointer["profile_id"])
    if profile.get("parent_id") != pointer["previous_profile_id"]:
        raise ValueError("active-profile pointer does not match profile lineage")
    return profile


def activate_profile(data_dir: str | Path | None, profile: dict[str, Any]) -> dict[str, Any]:
    root = resolve_data_dir(data_dir)
    candidate = validate_profile(profile)
    candidate["profile_id"] = _safe_profile_identifier(candidate["profile_id"], "profile_id")
    candidate["parent_id"] = _safe_optional_profile_identifier(candidate["parent_id"], "parent_id")
    with _ActivationLock(root):
        current_profile = load_active_profile(root)
        current_profile_id = _safe_profile_identifier(
            current_profile["profile_id"],
            "current profile_id",
        )
        if candidate["profile_id"] == current_profile_id:
            if _canonical_json(candidate) != _canonical_json(current_profile):
                raise ValueError("active profile id already exists with conflicting content")
            return copy.deepcopy(current_profile)
        if candidate["parent_id"] != current_profile_id:
            raise ValueError(
                f"candidate parent_id must match active profile {current_profile_id}"
            )
        candidate = validate_challenger(current_profile, candidate)
        _write_profile_artifact(root, candidate)
        _atomic_write_json(
            _pointer_path(root),
            {
                "schema_version": PROFILE_SCHEMA_VERSION,
                "profile_id": candidate["profile_id"],
                "previous_profile_id": current_profile_id,
            },
        )
    return copy.deepcopy(candidate)


def rollback_profile(data_dir: str | Path | None) -> dict[str, Any]:
    root = resolve_data_dir(data_dir)
    with _ActivationLock(root):
        pointer_path = _pointer_path(root)
        if not pointer_path.exists():
            raise ValueError("cannot roll back without an active-profile pointer")
        pointer = _load_pointer(root)
        previous_profile_id = pointer["previous_profile_id"]
        if previous_profile_id is None:
            raise ValueError("no previous profile is available for rollback")
        previous_profile = _load_profile_artifact(root, previous_profile_id)
        _atomic_write_json(
            pointer_path,
            {
                "schema_version": PROFILE_SCHEMA_VERSION,
                "profile_id": previous_profile["profile_id"],
                "previous_profile_id": previous_profile.get("parent_id"),
            },
        )
    return copy.deepcopy(previous_profile)
