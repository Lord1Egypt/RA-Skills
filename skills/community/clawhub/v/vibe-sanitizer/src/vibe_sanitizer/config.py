from __future__ import annotations

import ast
import fnmatch
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .constants import DEFAULT_CONFIG_FILE, DEFAULT_PLACEHOLDERS
from .errors import VibeSanitizerError


@dataclass(frozen=True)
class Config:
    ignore_detectors: frozenset[str]
    path_exclusions: tuple[str, ...]
    allow_patterns: tuple[str, ...]
    severity_overrides: dict[str, str]
    placeholders: dict[str, str]

    def is_path_excluded(self, relative_path: str) -> bool:
        return any(fnmatch.fnmatch(relative_path, pattern) for pattern in self.path_exclusions)

    def is_detector_ignored(self, detector_id: str) -> bool:
        return detector_id in self.ignore_detectors

    def is_allowed(self, relative_path: str, matched_text: str) -> bool:
        for pattern in self.allow_patterns:
            if re.search(pattern, matched_text) or re.search(pattern, relative_path):
                return True
        return False

    def severity_for(self, detector_id: str, default: str) -> str:
        return self.severity_overrides.get(detector_id, default)


def default_config() -> Config:
    return Config(
        ignore_detectors=frozenset(),
        path_exclusions=tuple(),
        allow_patterns=tuple(),
        severity_overrides={},
        placeholders=dict(DEFAULT_PLACEHOLDERS),
    )


def load_config(repo_root: Path, explicit_path: str | None = None) -> Config:
    config_path = Path(explicit_path).expanduser() if explicit_path else repo_root / DEFAULT_CONFIG_FILE
    if not config_path.exists():
        return default_config()

    raw_data = _parse_simple_yaml(config_path.read_text(encoding="utf-8"))
    placeholders = dict(DEFAULT_PLACEHOLDERS)
    placeholders.update(_ensure_string_map(raw_data.get("placeholders", {}), "placeholders"))

    return Config(
        ignore_detectors=frozenset(_ensure_string_list(raw_data.get("ignore_detectors", []), "ignore_detectors")),
        path_exclusions=tuple(_ensure_string_list(raw_data.get("path_exclusions", []), "path_exclusions")),
        allow_patterns=tuple(_ensure_string_list(raw_data.get("allow_patterns", []), "allow_patterns")),
        severity_overrides=_ensure_string_map(raw_data.get("severity_overrides", {}), "severity_overrides"),
        placeholders=placeholders,
    )


def write_default_config(path: Path, *, force: bool = False) -> Path:
    if path.exists() and not force:
        raise VibeSanitizerError(f"Config file already exists: {path}")

    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "ignore_detectors: []",
        "path_exclusions: []",
        "allow_patterns: []",
        "severity_overrides: {}",
        "placeholders:",
    ]
    for key, value in DEFAULT_PLACEHOLDERS.items():
        lines.append(f'  {key}: "{value}"')
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _ensure_string_list(value: Any, field_name: str) -> list[str]:
    if value in (None, []):
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise VibeSanitizerError(f"{field_name} must be a list of strings")
    return list(value)


def _ensure_string_map(value: Any, field_name: str) -> dict[str, str]:
    if value in (None, {}):
        return {}
    if not isinstance(value, dict) or not all(
        isinstance(key, str) and isinstance(item, str) for key, item in value.items()
    ):
        raise VibeSanitizerError(f"{field_name} must be a map of strings")
    return dict(value)


def _parse_scalar(raw_value: str) -> Any:
    if raw_value == "[]":
        return []
    if raw_value == "{}":
        return {}
    if raw_value.lower() in {"true", "false"}:
        return raw_value.lower() == "true"
    if raw_value.startswith(("'", '"')):
        return ast.literal_eval(raw_value)
    return raw_value


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None

    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.rstrip()
        if not stripped or stripped.lstrip().startswith("#"):
            continue

        indent = len(stripped) - len(stripped.lstrip(" "))
        content = stripped.lstrip(" ")

        if indent == 0:
            if ":" not in content:
                raise VibeSanitizerError(f"Invalid config line {line_number}: {line}")
            key, remainder = content.split(":", 1)
            key = key.strip()
            remainder = remainder.strip()
            if remainder:
                data[key] = _parse_scalar(remainder)
                current_key = None
            else:
                data[key] = None
                current_key = key
            continue

        if current_key is None:
            raise VibeSanitizerError(f"Invalid indentation on line {line_number}: {line}")

        if content.startswith("- "):
            item = _parse_scalar(content[2:].strip())
            if data[current_key] is None:
                data[current_key] = []
            if not isinstance(data[current_key], list):
                raise VibeSanitizerError(f"Expected list for {current_key} on line {line_number}")
            data[current_key].append(item)
            continue

        if ":" not in content:
            raise VibeSanitizerError(f"Invalid nested config line {line_number}: {line}")
        nested_key, nested_remainder = content.split(":", 1)
        nested_key = nested_key.strip()
        nested_remainder = nested_remainder.strip()
        if data[current_key] is None:
            data[current_key] = {}
        if not isinstance(data[current_key], dict):
            raise VibeSanitizerError(f"Expected map for {current_key} on line {line_number}")
        data[current_key][nested_key] = _parse_scalar(nested_remainder)

    return data
