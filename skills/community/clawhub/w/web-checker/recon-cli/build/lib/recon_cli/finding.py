"""Finding model + severity.

A Finding is the atomic unit a check emits. Severity is an enum so reports
and future tooling can sort/filter consistently.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import List, Optional


class Severity(IntEnum):
    """Ordered so you can compare: INFO < LOW < MED < HIGH < CRIT."""
    INFO = 0
    LOW = 1
    MED = 2
    HIGH = 3
    CRIT = 4

    @property
    def label(self) -> str:
        return {
            0: "INFO",
            1: "LOW",
            2: "MED",
            3: "HIGH",
            4: "CRIT",
        }[self]

    @property
    def icon(self) -> str:
        return {
            0: "•",
            1: "⚠",
            2: "▲",
            3: "■",
            4: "●",
        }[self]


@dataclass
class Finding:
    check: str                     # e.g. "headers", "js_bundle"
    title: str                     # short human summary
    severity: Severity = Severity.INFO
    evidence: str = ""             # command + raw output (short)
    recommendation: str = ""       # what to do about it (if applicable)
    is_false_positive: bool = False  # triaged away (kept for the audit trail)
    extra: dict = field(default_factory=dict)

    def as_line(self) -> str:
        if self.is_false_positive:
            return f"  {self.severity.icon} [FP] {self.title}"
        return f"  {self.severity.icon} {self.severity.label:<4} {self.title}"


@dataclass
class CheckResult:
    """All findings for one check + a short status line."""
    name: str
    status: str = "ok"             # ok | skipped | error
    findings: List[Finding] = field(default_factory=list)
    summary: str = ""              # one-line human summary for the stdout view
    error: Optional[str] = None

    @property
    def actionable(self) -> List[Finding]:
        return [f for f in self.findings if not f.is_false_positive]

    @property
    def worst(self) -> Optional[Severity]:
        acts = self.actionable
        if not acts:
            return None
        return max(f.severity for f in acts)
