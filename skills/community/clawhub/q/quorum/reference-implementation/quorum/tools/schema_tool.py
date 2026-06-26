# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Schema validation tool — JSON and YAML structure validation.

Used by critics (especially the Completeness and Architecture critics) to
verify that configurations and data files conform to expected structure.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class SchemaViolation:
    """A single schema validation error."""
    path: str = field(default="", metadata={"description": "JSON path to the violating field"})
    message: str = field(default="")
    expected: str = field(default="")
    actual: str = field(default="")

    def format(self) -> str:
        parts = [f"At '{self.path}': {self.message}"]
        if self.expected:
            parts.append(f"  Expected: {self.expected}")
        if self.actual:
            parts.append(f"  Actual:   {self.actual}")
        return "\n".join(parts)


class SchemaTool:
    """
    Structural validation for JSON and YAML files.

    Provides two modes:
    1. Key-presence check — does the file have the required fields?
    2. Type check — do values have the expected types?

    For full JSON Schema validation, install jsonschema:
        pip install jsonschema
    """

    def load(self, file_path: Path | str) -> tuple[dict[str, Any] | None, str | None]:
        """
        Load a JSON or YAML file.

        Returns:
            (data, None) on success
            (None, error_message) on failure
        """
        path = Path(file_path)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except FileNotFoundError:
            return None, f"File not found: {file_path}"

        ext = path.suffix.lower()
        try:
            if ext in (".yaml", ".yml"):
                data = yaml.safe_load(text)
            elif ext == ".json":
                data = json.loads(text)
            else:
                # Try YAML first (superset of JSON), then JSON
                try:
                    data = yaml.safe_load(text)
                except yaml.YAMLError:
                    data = json.loads(text)

            if not isinstance(data, dict):
                return None, f"Expected a mapping at root, got {type(data).__name__}"
            return data, None

        except (yaml.YAMLError, json.JSONDecodeError) as e:
            return None, f"Parse error: {e}"

    def check_required_keys(
        self,
        data: dict[str, Any],
        required: list[str],
        prefix: str = "",
    ) -> list[SchemaViolation]:
        """
        Check that all required keys are present in the data dict.

        Args:
            data:     Parsed dict to check
            required: List of required key names (supports dot-notation for nesting)
            prefix:   Prefix for violation path display

        Returns:
            List of violations for missing keys
        """
        violations = []
        for key in required:
            parts = key.split(".")
            current = data
            found = True
            path_so_far = prefix

            for part in parts:
                path_so_far = f"{path_so_far}.{part}".lstrip(".")
                if not isinstance(current, dict) or part not in current:
                    found = False
                    violations.append(
                        SchemaViolation(
                            path=path_so_far,
                            message="Required key is missing",
                            expected=f"key '{part}' to be present",
                            actual="key absent",
                        )
                    )
                    break
                current = current[part]

        return violations

    def check_types(
        self,
        data: dict[str, Any],
        type_map: dict[str, type | tuple[type, ...]],
    ) -> list[SchemaViolation]:
        """
        Check that values at specified paths have the expected types.

        Args:
            data:     Parsed dict
            type_map: {dot-path: expected_type_or_tuple}

        Returns:
            List of type violations
        """
        violations = []
        for key_path, expected_type in type_map.items():
            parts = key_path.split(".")
            current = data
            found = True

            for part in parts:
                if not isinstance(current, dict) or part not in current:
                    found = False
                    break
                current = current[part]

            if found and not isinstance(current, expected_type):
                type_name = (
                    " | ".join(t.__name__ for t in expected_type)
                    if isinstance(expected_type, tuple)
                    else expected_type.__name__
                )
                violations.append(
                    SchemaViolation(
                        path=key_path,
                        message="Wrong type",
                        expected=type_name,
                        actual=type(current).__name__,
                    )
                )

        return violations

    def validate_with_jsonschema(
        self,
        data: dict[str, Any],
        schema: dict[str, Any],
    ) -> list[SchemaViolation]:
        """
        Full JSON Schema validation (requires jsonschema package).

        Returns empty list and logs a warning if jsonschema is not installed.
        """
        try:
            import jsonschema
        except ImportError:
            return [
                SchemaViolation(
                    path="(setup)",
                    message="jsonschema not installed; install with: pip install jsonschema",
                )
            ]

        violations = []
        validator = jsonschema.Draft7Validator(schema)
        for error in validator.iter_errors(data):
            path = ".".join(str(p) for p in error.absolute_path) or "(root)"
            violations.append(
                SchemaViolation(
                    path=path,
                    message=error.message,
                    expected=str(error.schema.get("type", "")),
                    actual=str(type(error.instance).__name__),
                )
            )
        return violations

    def format_violations(self, violations: list[SchemaViolation]) -> str:
        """Evidence-ready string from a list of violations."""
        if not violations:
            return "(no schema violations)"
        return "\n".join(v.format() for v in violations)
