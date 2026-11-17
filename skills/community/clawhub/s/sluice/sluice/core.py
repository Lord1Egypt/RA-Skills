"""Scan and redact. The public surface is scan() and redact()."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Pattern

from .detectors import DETECTORS, Detector

Severity = str  # "high" | "medium" | "low"

_SEVERITY_RANK = {"low": 0, "medium": 1, "high": 2}


@dataclass(frozen=True)
class Finding:
    detector: str
    severity: Severity
    start: int
    end: int
    match: str
    line: int  # 1-based line number of the match start
    label: str

    @property
    def preview(self) -> str:
        """A safe-to-show fragment: never echo the full secret."""
        s = self.match
        if len(s) <= 8:
            return s[0] + "***" if s else "***"
        return f"{s[:4]}…{s[-2:]} ({len(s)} chars)"


def _line_of(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def _compile_allow(allow: Iterable[str] | None) -> list[Pattern[str]]:
    return [re.compile(a) for a in (allow or [])]


def _allowed(secret: str, allow: list[Pattern[str]]) -> bool:
    return any(p.search(secret) for p in allow)


def scan(
    text: str,
    *,
    detectors: list[Detector] | None = None,
    allow: Iterable[str] | None = None,
    min_severity: Severity = "low",
) -> list[Finding]:
    """Return findings sorted by position. Overlapping spans are resolved in
    favour of the higher-severity (then longer) detector, so a JWT inside a
    `token=` assignment is reported once, as the JWT."""
    dets = detectors if detectors is not None else DETECTORS
    allow_pats = _compile_allow(allow)
    floor = _SEVERITY_RANK[min_severity]

    raw: list[Finding] = []
    for det in dets:
        if _SEVERITY_RANK[det.severity] < floor:
            continue
        for start, end, secret in det.finditer(text):
            if _allowed(secret, allow_pats):
                continue
            raw.append(
                Finding(
                    detector=det.name,
                    severity=det.severity,
                    start=start,
                    end=end,
                    match=secret,
                    line=_line_of(text, start),
                    label=det.label,
                )
            )

    return _dedupe_overlaps(raw)


def _dedupe_overlaps(findings: list[Finding]) -> list[Finding]:
    # Prefer higher severity, then longer span, then earlier start.
    ordered = sorted(
        findings,
        key=lambda f: (-_SEVERITY_RANK[f.severity], -(f.end - f.start), f.start),
    )
    kept: list[Finding] = []
    for f in ordered:
        if any(not (f.end <= k.start or f.start >= k.end) for k in kept):
            continue  # overlaps something already kept
        kept.append(f)
    return sorted(kept, key=lambda f: f.start)


def redact(
    text: str,
    *,
    detectors: list[Detector] | None = None,
    allow: Iterable[str] | None = None,
    min_severity: Severity = "low",
    template: str = "[redacted:{label}]",
) -> str:
    """Return text with every finding replaced by its placeholder."""
    findings = scan(
        text, detectors=detectors, allow=allow, min_severity=min_severity
    )
    out = []
    cursor = 0
    for f in findings:
        out.append(text[cursor:f.start])
        out.append(template.format(label=f.label))
        cursor = f.end
    out.append(text[cursor:])
    return "".join(out)


def worst_severity(findings: list[Finding]) -> Severity | None:
    if not findings:
        return None
    return max(findings, key=lambda f: _SEVERITY_RANK[f.severity]).severity
