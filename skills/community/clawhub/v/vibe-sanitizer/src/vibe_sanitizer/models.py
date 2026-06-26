from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MatchCandidate:
    detector_id: str
    title: str
    category: str
    severity: str
    message: str
    start_offset: int
    end_offset: int
    preview: str
    replacement_text: str | None
    editable_in_place: bool
    review_required: bool
    priority: int
    matched_text: str = field(repr=False)


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    column: int
    detector_id: str
    title: str
    category: str
    severity: str
    message: str
    preview: str
    replacement_text: str | None
    editable_in_place: bool
    review_required: bool
    start_offset: int = field(repr=False)
    end_offset: int = field(repr=False)

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "line": self.line,
            "column": self.column,
            "detector_id": self.detector_id,
            "title": self.title,
            "category": self.category,
            "severity": self.severity,
            "message": self.message,
            "preview": self.preview,
            "editable_in_place": self.editable_in_place,
            "review_required": self.review_required,
        }


@dataclass
class ScanReport:
    root: Path
    scope: str
    files_scanned: int
    files_skipped: int
    findings: list[Finding]

    @property
    def total_findings(self) -> int:
        return len(self.findings)

    @property
    def fixable_findings(self) -> int:
        return sum(1 for finding in self.findings if finding.editable_in_place)

    @property
    def review_required_findings(self) -> int:
        return sum(1 for finding in self.findings if finding.review_required)

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "root": str(self.root),
            "scope": self.scope,
            "files_scanned": self.files_scanned,
            "files_skipped": self.files_skipped,
            "total_findings": self.total_findings,
            "fixable_findings": self.fixable_findings,
            "review_required_findings": self.review_required_findings,
            "findings": [finding.to_public_dict() for finding in self.findings],
        }
