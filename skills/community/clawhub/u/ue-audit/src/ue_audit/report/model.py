"""Report data model for ue-audit."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable

from ..util import SCHEMA_VERSION, TOOL_NAME, TOOL_VERSION, utc_now


class Severity(str, Enum):
    BLOCKER = "blocker"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class Status(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"
    SKIP = "skip"
    UNKNOWN = "unknown"
    ERROR = "error"


class Confidence(str, Enum):
    FACT = "fact"
    RULE = "rule"
    AI = "ai"


class Provenance(str, Enum):
    AI = "ai"
    MANUAL = "manual"
    UNKNOWN = "unknown"
    TOOLCHAIN = "toolchain"


SEVERITY_ORDER = {
    Severity.BLOCKER: 0,
    Severity.ERROR: 1,
    Severity.WARNING: 2,
    Severity.INFO: 3,
}


@dataclass
class Finding:
    check_id: str
    severity: Severity
    status: Status
    title: str
    message: str
    asset: str = ""
    evidence: list[str] = field(default_factory=list)
    recommendation: str = ""
    provenance: Provenance = Provenance.UNKNOWN
    confidence: Confidence = Confidence.FACT
    finding_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.finding_id,
            "check_id": self.check_id,
            "severity": self.severity.value,
            "status": self.status.value,
            "title": self.title,
            "message": self.message,
            "asset": self.asset,
            "evidence": list(self.evidence),
            "recommendation": self.recommendation,
            "provenance": self.provenance.value,
            "confidence": self.confidence.value,
        }


@dataclass
class CheckResult:
    check_id: str
    title: str
    status: Status
    severity: Severity = Severity.INFO
    summary: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)
    started_at: str = ""
    duration_ms: int = 0

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "title": self.title,
            "status": self.status.value,
            "severity": self.severity.value,
            "summary": self.summary,
            "details": self.details,
            "findings": [finding.to_dict() for finding in self.findings],
            "started_at": self.started_at,
            "duration_ms": self.duration_ms,
        }


@dataclass
class Report:
    mode: str = "audit"
    project: dict[str, Any] = field(default_factory=dict)
    engine: dict[str, Any] = field(default_factory=dict)
    baseline: dict[str, Any] | None = None
    checks: list[CheckResult] = field(default_factory=list)
    readonly_proof: dict[str, Any] = field(default_factory=dict)
    limitations: list[str] = field(default_factory=list)
    evidence: dict[str, str] = field(default_factory=dict)
    fail_on: str = "warning"
    schema_version: int = SCHEMA_VERSION
    tool: str = TOOL_NAME
    tool_version: str = TOOL_VERSION
    run_id: str = ""
    generated_at: str = ""

    def add_check(self, check: CheckResult) -> None:
        self.checks.append(check)

    def all_findings(self) -> list[Finding]:
        findings: list[Finding] = []
        for check in self.checks:
            findings.extend(check.findings)
        return findings

    def compute_summary(self) -> dict[str, Any]:
        findings = self.all_findings()
        severity_counts = {severity.value: 0 for severity in Severity}
        status_counts = {status.value: 0 for status in Status}
        for finding in findings:
            severity_counts[finding.severity.value] += 1
            status_counts[finding.status.value] += 1
        check_counts = {status.value: 0 for status in Status}
        for check in self.checks:
            check_counts[check.status.value] += 1
        return {
            "check_count": len(self.checks),
            "finding_count": len(findings),
            "severity": severity_counts,
            "finding_status": status_counts,
            "check_status": check_counts,
            "has_blocker": severity_counts[Severity.BLOCKER.value] > 0,
            "has_error": severity_counts[Severity.ERROR.value] > 0,
            "has_warning": severity_counts[Severity.WARNING.value] > 0,
        }

    def exit_code(self, fail_on: str | None = None) -> int:
        threshold = (fail_on or self.fail_on or "warning").lower()
        if threshold not in {"warning", "error", "blocker"}:
            threshold = "warning"
        findings = self.all_findings()
        severe = {Severity.ERROR, Severity.BLOCKER}
        if any(finding.severity in severe for finding in findings):
            return 2
        if threshold == "warning" and any(
            finding.severity == Severity.WARNING for finding in findings
        ):
            return 1
        if threshold in {"warning", "error"} and any(
            check.status in (Status.FAIL, Status.ERROR) for check in self.checks
        ):
            return 2
        if threshold == "warning" and any(
            check.status == Status.WARN for check in self.checks
        ):
            return 1
        return 0

    def finalize(self) -> "Report":
        if not self.generated_at:
            self.generated_at = utc_now()
        for index, finding in enumerate(self.all_findings(), start=1):
            if not finding.finding_id:
                finding.finding_id = f"UEA-{index:04d}"
        return self

    def to_dict(self) -> dict[str, Any]:
        self.finalize()
        findings = self.all_findings()
        findings.sort(
            key=lambda item: (
                SEVERITY_ORDER.get(item.severity, 99),
                item.check_id,
                item.finding_id,
            )
        )
        return {
            "schema_version": self.schema_version,
            "tool": self.tool,
            "tool_version": self.tool_version,
            "run_id": self.run_id,
            "generated_at": self.generated_at,
            "mode": self.mode,
            "fail_on": self.fail_on,
            "project": self.project,
            "engine": self.engine,
            "baseline": self.baseline,
            "summary": self.compute_summary(),
            "checks": [check.to_dict() for check in self.checks],
            "findings": [finding.to_dict() for finding in findings],
            "readonly_proof": self.readonly_proof,
            "limitations": list(self.limitations),
            "evidence": dict(self.evidence),
        }


def sort_findings(findings: Iterable[Finding]) -> list[Finding]:
    return sorted(
        findings,
        key=lambda item: (
            SEVERITY_ORDER.get(item.severity, 99),
            item.check_id,
            item.finding_id,
        ),
    )
