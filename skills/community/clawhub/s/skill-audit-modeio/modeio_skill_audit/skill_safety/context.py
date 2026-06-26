from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Tuple

from .json_utils import extract_first_json_object

ENV_VALUES = {"local-dev", "ci", "staging", "production", "unknown"}
MODE_VALUES = {"read-only", "build-test", "install", "deploy", "mutating", "unknown"}
TOLERANCE_VALUES = {"strict", "balanced", "permissive"}
SENSITIVITY_VALUES = {"public", "internal", "sensitive", "regulated", "unknown"}


@dataclass(frozen=True)
class ContextProfile:
    environment: str = "unknown"
    execution_mode: str = "unknown"
    risk_tolerance: str = "balanced"
    data_sensitivity: str = "unknown"

    def to_dict(self) -> Dict[str, str]:
        return {
            "environment": self.environment,
            "execution_mode": self.execution_mode,
            "risk_tolerance": self.risk_tolerance,
            "data_sensitivity": self.data_sensitivity,
        }


def _parse_json_source(raw_text: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    payload: Optional[Dict[str, Any]] = None
    try:
        parsed = json.loads(raw_text)
        if isinstance(parsed, dict):
            payload = parsed
    except ValueError:
        payload = None

    if payload is not None:
        return payload, None

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, flags=re.IGNORECASE | re.DOTALL)
    candidate = fenced.group(1) if fenced else extract_first_json_object(raw_text)
    if not candidate:
        return None, "Could not parse context profile JSON payload."
    try:
        parsed = json.loads(candidate)
    except ValueError as exc:
        return None, f"Invalid context profile JSON: {exc}"
    if not isinstance(parsed, dict):
        return None, "Context profile JSON root must be an object."
    return parsed, None


def _normalize_choice(
    payload: Dict[str, Any],
    key: str,
    allowed_values: Sequence[str],
    default_value: str,
    errors: list[str],
) -> str:
    raw = payload.get(key, default_value)
    if not isinstance(raw, str):
        errors.append(f"context.{key} must be a string")
        return default_value
    value = raw.strip().lower()
    allowed = set(allowed_values)
    if value not in allowed:
        errors.append(f"context.{key} must be one of {', '.join(sorted(allowed))}")
        return default_value
    return value


def parse_context_profile(
    context_json: Optional[str] = None,
    context_file: Optional[str] = None,
) -> Tuple[ContextProfile, list[str]]:
    errors: list[str] = []
    if not context_json and not context_file:
        return ContextProfile(), errors

    raw_payload: Optional[str] = None
    if context_json:
        raw_payload = context_json
    elif context_file:
        path = Path(context_file).expanduser().resolve()
        try:
            raw_payload = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"Failed reading context profile file: {exc}")
            return ContextProfile(), errors

    assert raw_payload is not None
    payload, parse_error = _parse_json_source(raw_payload)
    if parse_error:
        errors.append(parse_error)
        return ContextProfile(), errors

    assert payload is not None
    profile = ContextProfile(
        environment=_normalize_choice(payload, "environment", ENV_VALUES, "unknown", errors),
        execution_mode=_normalize_choice(payload, "execution_mode", MODE_VALUES, "unknown", errors),
        risk_tolerance=_normalize_choice(payload, "risk_tolerance", TOLERANCE_VALUES, "balanced", errors),
        data_sensitivity=_normalize_choice(payload, "data_sensitivity", SENSITIVITY_VALUES, "unknown", errors),
    )
    return profile, errors


def classify_finding_surface(file_path: str, tags: Sequence[str]) -> str:
    path = file_path.replace("\\", "/").lower()
    tag_set = {str(tag).lower() for tag in tags}

    if "install-hook" in tag_set:
        return "install-hook"
    if path.startswith(".github/workflows/") or "workflow" in tag_set:
        return "workflow"
    if path.endswith("/skill.md") or path == "skill.md" or "/.claude/skills/" in f"/{path}":
        return "skill-instruction"
    if any(part in path for part in ["/tests/", "test_", "/spec/", "/fixtures/"]):
        return "test-fixture"
    if any(part in path for part in ["/examples/", "/example/"]):
        return "example"
    if path.endswith((".md", ".txt")) or any(part in path for part in ["/docs/", "/prompts/"]):
        return "docs"
    return "runtime"


def context_multiplier(profile: ContextProfile, surface: str) -> float:
    value = 1.0

    if surface in {"docs", "example", "test-fixture"}:
        value *= 0.35
    elif surface == "skill-instruction":
        value *= 1.05
    elif surface == "install-hook":
        value *= 1.20
    elif surface == "workflow":
        value *= 1.10

    if profile.execution_mode == "read-only":
        if surface in {"docs", "example", "test-fixture"}:
            value *= 0.70
        else:
            value *= 0.90
    elif profile.execution_mode == "build-test":
        if surface in {"install-hook", "workflow"}:
            value *= 1.10
    elif profile.execution_mode == "install":
        if surface == "install-hook":
            value *= 1.35
        elif surface in {"workflow", "runtime"}:
            value *= 1.10
    elif profile.execution_mode in {"deploy", "mutating"}:
        if surface in {"workflow", "runtime", "install-hook"}:
            value *= 1.25

    if profile.environment == "production":
        value *= 1.20
    elif profile.environment == "staging":
        value *= 1.10

    if profile.risk_tolerance == "strict":
        value *= 1.15
    elif profile.risk_tolerance == "permissive":
        value *= 0.85

    if profile.data_sensitivity == "sensitive":
        value *= 1.15
    elif profile.data_sensitivity == "regulated":
        value *= 1.25

    return max(0.15, min(2.5, round(value, 2)))
