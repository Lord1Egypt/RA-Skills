# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Rubric loader — reads JSON rubric files and returns validated Rubric objects.

Rubrics ship in rubrics/builtin/ or can be provided externally.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from quorum.models import Rubric, RubricCriterion, Severity

logger = logging.getLogger(__name__)

# Path to the built-in rubrics directory (relative to this file)
BUILTIN_DIR = Path(__file__).parent / "builtin"


class RubricLoader:
    """
    Load and validate Quorum rubrics from JSON files.

    Built-in rubric names (no path needed):
    - research-synthesis
    - agent-config

    External rubrics: pass a full Path or file path string.
    """

    def load(self, name_or_path: str | Path) -> Rubric:
        """
        Load a rubric by name (built-in) or file path.

        Args:
            name_or_path: Built-in rubric name (e.g. "research-synthesis")
                          or path to a JSON rubric file

        Returns:
            Validated Rubric object

        Raises:
            FileNotFoundError: If the rubric file cannot be found
            ValueError: If the rubric file is malformed
        """
        path = self._resolve_path(name_or_path)
        return self._load_file(path)

    def list_builtin(self) -> list[str]:
        """Return names of all built-in rubrics."""
        if not BUILTIN_DIR.exists():
            return []
        return [
            p.stem
            for p in BUILTIN_DIR.glob("*.json")
            if p.is_file()
        ]

    def _resolve_path(self, name_or_path: str | Path) -> Path:
        """Resolve a name or path to an actual file path."""
        path = Path(name_or_path)

        # If it looks like a path and exists, use it directly
        if path.exists():
            return path

        # Try as a built-in name
        builtin_path = BUILTIN_DIR / f"{name_or_path}.json"
        if builtin_path.exists():
            return builtin_path

        # Try with .json extension
        with_ext = Path(f"{name_or_path}.json")
        if with_ext.exists():
            return with_ext

        raise FileNotFoundError(
            f"Rubric not found: '{name_or_path}'\n"
            f"Built-in rubrics: {self.list_builtin()}\n"
            f"Or provide a path to a JSON rubric file."
        )

    def _load_file(self, path: Path) -> Rubric:
        """Load and parse a rubric from a JSON file."""
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in rubric file {path}: {e}") from e

        # Parse criteria with Severity enum coercion
        raw_criteria = data.get("criteria", [])
        criteria = []
        for raw in raw_criteria:
            # Coerce severity string to enum — accept "severity" or "category" field
            raw_severity = (
                raw.get("severity")
                or raw.get("category")
                or "MEDIUM"
            ).upper()
            try:
                severity = Severity(raw_severity)
            except ValueError:
                logger.warning(
                    "Unknown severity '%s' in rubric %s criterion %s — defaulting to MEDIUM",
                    raw_severity, path.stem, raw.get("id", "?"),
                )
                severity = Severity.MEDIUM

            # Accept multiple field names for evidence and rationale
            evidence_required = (
                raw.get("evidence_required")
                or raw.get("evidence_instruction")
                or raw.get("evidence_type", "")
            )
            why = (
                raw.get("why")
                or raw.get("rationale")
                or ""
            )

            criteria.append(
                RubricCriterion(
                    id=raw["id"],
                    criterion=raw["criterion"],
                    severity=severity,
                    evidence_required=evidence_required,
                    why=why,
                    category=raw.get("category"),
                )
            )

        rubric = Rubric(
            name=data["name"],
            domain=data["domain"],
            version=data.get("version", "1.0"),
            description=data.get("description"),
            criteria=criteria,
        )

        logger.debug("Loaded rubric: %s v%s (%d criteria)", rubric.name, rubric.version, len(criteria))
        return rubric
