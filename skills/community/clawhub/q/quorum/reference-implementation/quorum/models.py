# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Core data models for Quorum.
All models use Pydantic v2 BaseModel for serialization, validation, and type safety.
"""

from __future__ import annotations

import hashlib
import uuid
from pathlib import Path
from typing import Any, Optional
from enum import Enum
from pydantic import BaseModel, Field, field_serializer, field_validator, model_validator

# Maximum file size for compute_hash (50 MB)
_MAX_HASH_FILE_SIZE = 50 * 1024 * 1024

# Display limits
_MAX_DISPLAYED_LOCATIONS = 10


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class VerdictStatus(str, Enum):
    PASS = "PASS"
    PASS_WITH_NOTES = "PASS_WITH_NOTES"
    REVISE = "REVISE"
    REJECT = "REJECT"


class Locus(BaseModel):
    """A specific location in a specific file cited as evidence."""
    file: str = Field(description="Relative path to the file")
    start_line: int = Field(ge=1, description="1-indexed start line")
    end_line: int = Field(ge=1, description="Inclusive end line")
    role: str = Field(description="Role in the relationship, e.g. 'implementation', 'specification', 'producer', 'consumer'")
    source_hash: str = Field(description="SHA-256 hex digest of raw file bytes at [start_line:end_line]")

    @model_validator(mode="after")
    def _validate_line_range(self) -> Locus:
        if self.start_line > self.end_line:
            raise ValueError(
                f"start_line ({self.start_line}) must be <= end_line ({self.end_line})"
            )
        return self

    @staticmethod
    def compute_hash(file_path: str | Path, start_line: int, end_line: int) -> str:
        """Compute SHA-256 of the raw bytes in the line range [start_line, end_line] (1-indexed, inclusive).

        Validates that the file is a regular file within size limits before reading.
        """
        path = Path(file_path).resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Not a regular file: {path.name}")
        file_size = path.stat().st_size
        if file_size > _MAX_HASH_FILE_SIZE:
            raise ValueError(
                f"File too large for hashing ({file_size} bytes, max {_MAX_HASH_FILE_SIZE})"
            )
        raw = path.read_bytes()
        return Locus._hash_byte_range(raw, start_line, end_line)

    @staticmethod
    def compute_hash_from_content(content: str, start_line: int, end_line: int) -> str:
        """Compute SHA-256 from already-loaded text content at [start_line, end_line] (1-indexed, inclusive)."""
        raw = content.encode("utf-8")
        return Locus._hash_byte_range(raw, start_line, end_line)

    @staticmethod
    def _hash_byte_range(raw: bytes, start_line: int, end_line: int) -> str:
        """Hash the raw bytes in the given line range. Shared by both compute_hash methods.

        Raises ValueError if the requested range produces an empty segment
        (out-of-bounds or reversed).
        """
        if start_line > end_line:
            raise ValueError(f"start_line ({start_line}) must be <= end_line ({end_line})")
        lines = raw.split(b"\n")
        # Re-attach newlines (split removes them); last line may not have trailing newline
        lines_with_endings = [line + b"\n" for line in lines[:-1]]
        if lines[-1]:  # Non-empty last line (no trailing newline in file)
            lines_with_endings.append(lines[-1])
        # Clamp to actual content length
        start_idx = max(0, start_line - 1)
        end_idx = min(len(lines_with_endings), end_line)
        segment = b"".join(lines_with_endings[start_idx:end_idx])
        if not segment and lines_with_endings:
            raise ValueError(
                f"Line range [{start_line}:{end_line}] is out of bounds "
                f"(file has {len(lines_with_endings)} lines)"
            )
        return hashlib.sha256(segment).hexdigest()


class Evidence(BaseModel):
    """Grounded evidence for a finding. Every finding must have this."""
    tool: str = Field(description="Tool used to gather evidence (grep, schema, llm, etc.)")
    result: str = Field(description="Raw output from the tool")
    citation: Optional[str] = Field(
        default=None,
        description="Rubric criterion ID this evidence supports (e.g. 'CRIT-001')"
    )


class Finding(BaseModel):
    """
    A single issue found by a critic.
    Evidence is mandatory — ungrounded claims are rejected by the Aggregator.
    """
    id: str = Field(default_factory=lambda: f"F-{uuid.uuid4().hex[:8]}", description="Unique finding identifier")
    severity: Severity
    category: Optional[str] = Field(default=None, description="Finding category, e.g. 'coverage_gap', 'accuracy_mismatch'")
    description: str = Field(description="Clear, actionable description of the issue")
    evidence: Evidence = Field(description="Required: tool-verified evidence for this finding")
    location: Optional[str] = Field(
        default=None,
        description="Where in the artifact the issue was found (line/section/key)"
    )
    loci: list[Locus] = Field(
        default_factory=list,
        description="Multi-locus evidence locations (cross-artifact findings)"
    )
    critic: str = Field(default="", description="Name of the critic that produced this finding")
    rubric_criterion: Optional[str] = Field(
        default=None,
        description="Rubric criterion ID this finding addresses"
    )
    framework_refs: list[str] = Field(
        default_factory=list,
        description="Framework references, e.g. ['CWE-683', 'ASVS V8.2.*']"
    )
    remediation: Optional[str] = Field(default=None, description="Suggested fix")


class CriticResult(BaseModel):
    """Output produced by a single critic after evaluating an artifact."""
    critic_name: str
    findings: list[Finding] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, description="Criteria coverage ratio (evaluated/total)")
    criteria_total: int = Field(default=0, description="Total rubric criteria in scope for this critic")
    criteria_evaluated: int = Field(default=0, description="Criteria that produced findings or were explicitly assessed")
    runtime_ms: int = Field(default=0, description="Wall-clock time the critic took")
    skipped: bool = Field(default=False, description="True if critic was skipped (e.g. not applicable)")
    skip_reason: Optional[str] = None


class AggregatedReport(BaseModel):
    """Synthesized report from all critics."""
    findings: list[Finding] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    conflicts_resolved: int = Field(default=0)
    critic_results: list[CriticResult] = Field(default_factory=list)
    tester_result: Optional["TesterResult"] = None
    l1_excluded_count: int = Field(default=0, description="Findings excluded by Tester L1 contradictions")

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == Severity.CRITICAL)

    @property
    def high_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == Severity.HIGH)

    @property
    def medium_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == Severity.MEDIUM)

    @property
    def low_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == Severity.LOW)

    @property
    def info_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == Severity.INFO)

    @property
    def low_info_count(self) -> int:
        """Combined LOW+INFO count for backward-compatible report display."""
        return self.low_count + self.info_count


class Verdict(BaseModel):
    """Final verdict on the artifact under review."""
    status: VerdictStatus
    reasoning: str = Field(description="Explanation of the verdict")
    confidence: float = Field(ge=0.0, le=1.0)
    report: Optional[AggregatedReport] = None

    @field_serializer("status")
    @classmethod
    def _serialize_status(cls, v: VerdictStatus, _info: Any) -> str:
        """Always serialize status as a plain string value, not an enum member."""
        return v.value if isinstance(v, Enum) else str(v)

    @property
    def is_actionable(self) -> bool:
        """Returns True if the artifact needs rework."""
        return self.status in (VerdictStatus.REVISE, VerdictStatus.REJECT)


class CrossArtifactVerdict(BaseModel):
    """Verdict from Phase 2 cross-artifact consistency checks."""
    status: VerdictStatus
    reasoning: str
    confidence: float = Field(ge=0.0, le=1.0)
    findings: list[Finding] = Field(default_factory=list)
    relationships_evaluated: int = 0


class FileResult(BaseModel):
    """Result for a single file in a batch validation run."""
    file_path: str
    verdict: Verdict
    run_dir: str = Field(description="Path to the per-file run directory")


class BatchVerdict(BaseModel):
    """Consolidated verdict across multiple files in a batch run."""
    status: VerdictStatus = Field(description="Worst-case status across all files")
    file_results: list[FileResult] = Field(default_factory=list)
    total_files: int = 0
    total_findings: int = 0
    files_passed: int = 0
    files_failed: int = 0
    confidence: float = Field(ge=0.0, le=1.0, default=0.0, description="Average confidence across files")
    reasoning: str = ""

    @property
    def is_actionable(self) -> bool:
        """Returns True if any file in the batch needs rework."""
        return self.status in (VerdictStatus.REVISE, VerdictStatus.REJECT)


class PreScreenCheck(BaseModel):
    """A single deterministic pre-screen check result."""

    id: str = Field(description="Check identifier, e.g. 'PS-001'")
    name: str = Field(description="Short machine-readable name, e.g. 'hardcoded_paths'")
    category: str = Field(description="Check category: security | syntax | structure | links")
    severity: Severity = Field(description="Severity level if this check fails")
    description: str = Field(description="Human-readable description of what was checked")
    result: str = Field(description="Outcome: PASS | FAIL | SKIP")
    evidence: str = Field(default="", description="Raw output or excerpt from the check")
    locations: list[str] = Field(
        default_factory=list,
        description="Line numbers or path locations where issues were found",
    )


class PreScreenResult(BaseModel):
    """Aggregated results from all deterministic pre-screen checks."""

    checks: list[PreScreenCheck] = Field(default_factory=list)
    total_checks: int = Field(default=0, description="Total number of checks attempted")
    passed: int = Field(default=0, description="Number of checks that passed")
    failed: int = Field(default=0, description="Number of checks that failed")
    skipped: int = Field(default=0, description="Number of checks skipped (not applicable)")
    runtime_ms: int = Field(default=0, description="Total wall-clock runtime in milliseconds")

    @property
    def has_failures(self) -> bool:
        """True if any check failed."""
        return self.failed > 0

    def to_evidence_block(self) -> str:
        """
        Format all check results as a structured text block for injection into
        LLM critic prompts.  Critics can reference these as pre-verified facts.
        """
        lines: list[str] = [
            "## Pre-Screen Evidence (Deterministic Checks)",
            f"Ran {self.total_checks} checks in {self.runtime_ms}ms: "
            f"{self.passed} passed, {self.failed} failed, {self.skipped} skipped.",
            "",
        ]

        failed = [c for c in self.checks if c.result == "FAIL"]
        passed = [c for c in self.checks if c.result == "PASS"]
        skipped = [c for c in self.checks if c.result == "SKIP"]

        if failed:
            lines.append("### FAILED Checks (pre-verified issues — treat as confirmed)")
            for check in failed:
                lines.append(
                    f"- [{check.id}] {check.name} "
                    f"(severity={check.severity.value}): {check.description}"
                )
                if check.locations:
                    locs = ", ".join(check.locations[:_MAX_DISPLAYED_LOCATIONS])
                    if len(check.locations) > _MAX_DISPLAYED_LOCATIONS:
                        locs += f" … (+{len(check.locations) - _MAX_DISPLAYED_LOCATIONS} more)"
                    lines.append(f"  Locations: {locs}")
                if check.evidence:
                    preview = check.evidence[:400].replace("\n", " ↵ ")
                    lines.append(f"  Evidence: {preview}")
            lines.append("")

        if passed:
            lines.append("### PASSED Checks (confirmed clean — do not re-flag these)")
            for check in passed:
                lines.append(f"- [{check.id}] {check.name}: {check.description} — OK")
            lines.append("")

        if skipped:
            lines.append("### SKIPPED Checks (not applicable to this file type)")
            for check in skipped:
                reason = check.evidence or "not applicable"
                lines.append(f"- [{check.id}] {check.name}: {reason}")
            lines.append("")

        return "\n".join(lines)


class VerificationStatus(str, Enum):
    """Outcome of the Tester critic's verification of a single finding."""
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    CONTRADICTED = "CONTRADICTED"


class VerificationResult(BaseModel):
    """Result of verifying a single finding against actual file content."""
    status: VerificationStatus
    original_finding_id: str = Field(description="ID of the finding being verified")
    explanation: str = Field(description="Why this verification status was assigned")
    verified_locus: Optional["VerifiedLocus"] = Field(
        default=None,
        description="The actual file content found at the cited location",
    )
    level: int = Field(
        default=1,
        ge=1,
        le=2,
        description="Verification level that produced this result (1=deterministic, 2=LLM)",
    )


class VerifiedLocus(BaseModel):
    """Actual content found at a cited file location during verification."""
    file_path: str = Field(description="Path to the file that was read")
    line_start: Optional[int] = Field(default=None, ge=1, description="1-indexed start line read")
    line_end: Optional[int] = Field(default=None, ge=1, description="1-indexed end line read")
    actual_content: str = Field(description="The real content found at this location")
    similarity_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Fuzzy match score between cited and actual content",
    )

    @model_validator(mode="after")
    def _validate_line_range(self) -> VerifiedLocus:
        if (self.line_start is None) != (self.line_end is None):
            raise ValueError("line_start and line_end must both be set or both be None")
        if self.line_start is not None and self.line_end is not None:
            if self.line_start > self.line_end:
                raise ValueError(
                    f"line_start ({self.line_start}) must be <= line_end ({self.line_end})"
                )
        return self


class TesterResult(BaseModel):
    """Aggregated output from the Tester critic across all verified findings."""
    verification_results: list[VerificationResult] = Field(default_factory=list)
    total_findings: int = Field(default=0, description="Total findings submitted for verification")
    verified_count: int = Field(default=0)
    unverified_count: int = Field(default=0)
    contradicted_count: int = Field(default=0)
    runtime_ms: int = Field(default=0)

    @model_validator(mode="after")
    def _validate_counts(self) -> TesterResult:
        count_sum = self.verified_count + self.unverified_count + self.contradicted_count
        if self.total_findings > 0 and count_sum != self.total_findings:
            raise ValueError(
                f"Count mismatch: verified ({self.verified_count}) + "
                f"unverified ({self.unverified_count}) + "
                f"contradicted ({self.contradicted_count}) = {count_sum}, "
                f"but total_findings = {self.total_findings}"
            )
        return self

    @property
    def verification_rate(self) -> float:
        """Fraction of findings that were VERIFIED."""
        if self.total_findings == 0:
            return 1.0
        return self.verified_count / self.total_findings

    @property
    def contradiction_rate(self) -> float:
        """Fraction of findings that were CONTRADICTED."""
        if self.total_findings == 0:
            return 0.0
        return self.contradicted_count / self.total_findings


class FixProposal(BaseModel):
    """A proposed fix for a specific finding."""
    finding_id: str = Field(description="ID of the finding this fixes")
    finding_description: str = Field(description="Brief description of the finding")
    file_path: str = Field(description="Path to the file to modify")
    original_text: str = Field(description="Exact text to find and replace")
    replacement_text: str = Field(description="Text to replace it with")
    explanation: str = Field(description="Why this change fixes the issue")
    confidence: float = Field(ge=0.0, le=1.0, description="Fixer's confidence this is correct")


class FixReport(BaseModel):
    """Results from the Fixer agent."""
    proposals: list[FixProposal] = Field(default_factory=list)
    findings_addressed: int = 0
    findings_skipped: int = 0
    skip_reasons: list[str] = Field(default_factory=list)
    loop_number: int = 1
    revalidation_verdict: Optional[str] = Field(default=None, description="Verdict after applying fixes, if re-validation ran")
    revalidation_delta: Optional[str] = Field(default=None, description="Summary of what changed after fix")


class Issue(BaseModel):
    """
    Persistent failure pattern stored in the learning memory (known_issues.json).
    High-frequency patterns automatically promote to mandatory checks.
    """
    pattern_id: str
    description: str
    domain: str
    severity: Severity
    frequency: int = Field(default=1)
    first_seen: str = Field(description="ISO date string")
    last_seen: str = Field(description="ISO date string")
    mandatory: bool = Field(
        default=False,
        description="If True, this pattern is auto-included in all future runs"
    )
    meta_lesson: Optional[str] = Field(
        default=None,
        description="Automation insight extracted from this failure pattern"
    )

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()


class UpdateResult(BaseModel):
    """Result of a learning memory update after a validation run."""
    new_patterns: int = 0
    updated_patterns: int = 0
    promoted_patterns: int = 0
    total_known: int = 0


class RubricCriterion(BaseModel):
    """A single evaluation criterion in a rubric."""
    id: str
    criterion: str = Field(description="What to evaluate")
    severity: Severity
    evidence_required: str = Field(description="What evidence must be shown to pass/fail this criterion")
    why: str = Field(description="Rationale for this criterion")
    category: Optional[str] = None


class Rubric(BaseModel):
    """Domain-specific validation rubric."""
    name: str
    domain: str
    version: str = "1.0"
    description: Optional[str] = None
    criteria: list[RubricCriterion] = Field(default_factory=list)

    @field_validator("criteria")
    @classmethod
    def criteria_not_empty(cls, v: list[RubricCriterion]) -> list[RubricCriterion]:
        if not v:
            raise ValueError("Rubric must have at least one criterion")
        return v
