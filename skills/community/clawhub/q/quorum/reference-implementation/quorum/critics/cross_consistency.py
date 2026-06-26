# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect

"""
Cross-Artifact Consistency Critic — Phase 2 cross-file relationship validation.

Evaluates declared relationships between artifacts:
- implements: spec coverage verification
- documents: accuracy verification
- delegates: boundary verification
- schema_contract: structural compatibility verification

Design: docs/CROSS_ARTIFACT_DESIGN.md
"""

from __future__ import annotations

import logging
import re
import time
from typing import Any

from quorum.config import QuorumConfig
from quorum.models import CriticResult, Evidence, Finding, Locus, Severity
from quorum.providers.base import BaseProvider
from quorum.relationships import ResolvedRelationship

logger = logging.getLogger(__name__)


# Prompt templates per relationship type
RELATIONSHIP_PROMPTS = {
    "implements": """You are evaluating whether an implementation file fully and correctly implements a specification.

SPECIFICATION ({spec_role}: {spec_path}):
```
{spec_content}
```

IMPLEMENTATION ({impl_role}: {impl_path}):
```
{impl_content}
```

{scope_note}

Evaluate:
1. COVERAGE: Are all spec requirements addressed in the implementation?
2. CORRECTNESS: Does the implementation match the spec's intent (not just surface keywords)?
3. GAPS: Are there spec requirements with no corresponding implementation?
4. DRIFT: Are there implementation behaviors not specified (scope creep)?

{phase1_context}
""",

    "documents": """You are evaluating whether documentation accurately describes source code behavior.

SOURCE CODE ({source_role}: {source_path}):
```
{source_content}
```

DOCUMENTATION ({docs_role}: {docs_path}):
```
{docs_content}
```

{scope_note}

Evaluate:
1. ACCURACY: Does the documentation match what the code actually does?
2. COMPLETENESS: Are all public interfaces/behaviors documented?
3. STALENESS: Are there documented features that no longer exist in the code?
4. MISLEADING: Are there descriptions that could lead a reader to incorrect conclusions?

{phase1_context}
""",

    "delegates": """You are evaluating a delegation boundary between two artifacts.

DELEGATING ARTIFACT ({from_role}: {from_path}):
```
{from_content}
```

RECEIVING ARTIFACT ({to_role}: {to_path}):
```
{to_content}
```

Delegation scope: {scope}

Evaluate:
1. COMPLETENESS: Is the delegated scope fully covered by the receiving artifact?
2. OVERLAP: Are there topics handled by both (duplication)?
3. GAPS: Are there topics in the delegation scope handled by neither?
4. BOUNDARY CLARITY: Is it clear from reading either artifact where responsibility lies?

{phase1_context}
""",

    "schema_contract": """You are evaluating a schema contract between a producer and consumer.

PRODUCER ({producer_role}: {producer_path}):
```
{producer_content}
```

CONSUMER ({consumer_role}: {consumer_path}):
```
{consumer_content}
```

Contract: {scope}

Evaluate:
1. STRUCTURAL COMPATIBILITY: Do the producer's output types match the consumer's expected inputs?
2. FIELD COVERAGE: Does the producer populate all fields the consumer requires?
3. OPTIONAL/REQUIRED MISMATCH: Does the consumer treat optional producer fields as required (or vice versa)?
4. TYPE SAFETY: Are there type mismatches (str vs int, Optional vs required, etc.)?

{phase1_context}
""",
}


# JSON schema for cross-consistency findings
CROSS_FINDINGS_SCHEMA = {
    "type": "object",
    "required": ["findings"],
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["severity", "description", "evidence_tool", "evidence_result", "category"],
                "properties": {
                    "severity": {
                        "type": "string",
                        "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"],
                    },
                    "description": {"type": "string"},
                    "category": {
                        "type": "string",
                        "enum": [
                            "coverage_gap",
                            "accuracy_mismatch",
                            "boundary_violation",
                            "compatibility_issue",
                            "staleness",
                            "drift",
                            "overlap",
                            "missing_file",
                        ],
                    },
                    "evidence_tool": {"type": "string"},
                    "evidence_result": {"type": "string"},
                    "role_a_location": {
                        "type": "string",
                        "description": "Line range or section in role A file (e.g. 'lines 42-50' or 'section: Error Handling')",
                    },
                    "role_b_location": {
                        "type": "string",
                        "description": "Line range or section in role B file",
                    },
                    "remediation": {"type": "string"},
                    "framework_refs": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            },
        }
    },
}


SYSTEM_PROMPT = """You are Quorum's Cross-Artifact Consistency Critic.

Your job: evaluate whether declared relationships between files are maintained.
You check for coverage gaps, accuracy mismatches, boundary violations, schema
incompatibilities, staleness, and drift.

Rules:
1. EVERY finding must have specific evidence — quote the exact text from both files.
2. Reference specific line numbers or section headers where possible.
3. Do not repeat issues already flagged by Phase 1 critics (provided as context).
4. Focus on CROSS-FILE inconsistencies — things a single-file critic cannot catch.
5. If a file doesn't exist, report it as a CRITICAL finding (missing_file category).
6. Be precise about which role (spec vs impl, source vs docs, etc.) has the issue.

Respond with JSON matching the provided schema."""


class CrossConsistencyCritic:
    """
    Phase 2 critic that evaluates declared relationships between artifacts.

    Unlike single-file critics (BaseCritic), this critic:
    - Evaluates pairs of files, not individual artifacts
    - Produces multi-locus findings with role annotations
    - Runs after Phase 1 and receives Phase 1 findings as context (NOT verdicts)
    """

    name: str = "cross_consistency"

    def __init__(self, provider: BaseProvider, config: QuorumConfig):
        self.provider = provider
        self.config = config

    def evaluate(
        self,
        resolved_relationships: list[ResolvedRelationship],
        phase1_findings: list[Finding] | None = None,
    ) -> CriticResult:
        """
        Evaluate all resolved relationships.

        Args:
            resolved_relationships: Relationships with loaded file contents
            phase1_findings: Findings from Phase 1 critics (for context, NOT verdicts)

        Returns:
            CriticResult with cross-artifact findings
        """
        start_ms = int(time.time() * 1000)
        all_findings: list[Finding] = []
        evaluated_count = 0

        # Format Phase 1 findings as context (deduplification signal)
        phase1_context = self._format_phase1_context(phase1_findings or [])

        for resolved in resolved_relationships:
            rel = resolved.relationship

            # Handle missing files — report and skip to next relationship
            if not resolved.role_a_exists:
                all_findings.append(Finding(
                    severity=Severity.CRITICAL,
                    category="missing_file",
                    description=(
                        f"File not found: {rel.role_a_path} "
                        f"(role: {rel.role_a_name} in {rel.type} relationship)"
                    ),
                    evidence=Evidence(
                        tool="filesystem",
                        result=f"File does not exist: {rel.role_a_path}",
                    ),
                    critic=self.name,
                    loci=[],
                ))
                evaluated_count += 1
                continue

            if not resolved.role_b_exists:
                all_findings.append(Finding(
                    severity=Severity.CRITICAL,
                    category="missing_file",
                    description=(
                        f"File not found: {rel.role_b_path} "
                        f"(role: {rel.role_b_name} in {rel.type} relationship)"
                    ),
                    evidence=Evidence(
                        tool="filesystem",
                        result=f"File does not exist: {rel.role_b_path}",
                    ),
                    critic=self.name,
                    loci=[],
                ))
                evaluated_count += 1
                continue

            # Build and run the LLM prompt for this relationship
            try:
                findings = self._evaluate_relationship(resolved, phase1_context)
                all_findings.extend(findings)
                evaluated_count += 1
            except Exception as e:
                logger.error(
                    "Failed to evaluate %s relationship (%s ↔ %s): %s",
                    rel.type, rel.role_a_path, rel.role_b_path, e,
                    exc_info=True,
                )
                all_findings.append(Finding(
                    severity=Severity.HIGH,
                    description=(
                        f"Cross-consistency evaluation failed for {rel.type}: "
                        f"{rel.role_a_path} ↔ {rel.role_b_path}"
                    ),
                    evidence=Evidence(tool="error", result=f"{type(e).__name__}: {e}"),
                    critic=self.name,
                ))

        runtime_ms = int(time.time() * 1000) - start_ms
        criteria_total = len(resolved_relationships)
        criteria_evaluated = evaluated_count
        confidence = self._compute_coverage(criteria_evaluated, criteria_total)

        logger.info(
            "[%s] Done: %d findings across %d relationships in %dms (coverage=%.0f%%)",
            self.name, len(all_findings), len(resolved_relationships),
            runtime_ms, confidence * 100,
        )

        return CriticResult(
            critic_name=self.name,
            findings=all_findings,
            confidence=confidence,
            criteria_total=criteria_total,
            criteria_evaluated=criteria_evaluated,
            runtime_ms=runtime_ms,
        )

    def _evaluate_relationship(
        self,
        resolved: ResolvedRelationship,
        phase1_context: str,
    ) -> list[Finding]:
        """Evaluate a single relationship via LLM and return parsed findings."""
        rel = resolved.relationship
        prompt_template = RELATIONSHIP_PROMPTS.get(rel.type)

        if not prompt_template:
            logger.warning("No prompt template for relationship type: %s", rel.type)
            return []

        # Build template variables based on relationship type
        # Escape scope to prevent str.format() injection from user YAML
        escaped_scope = self._escape_braces(rel.scope) if rel.scope else ""
        template_vars: dict[str, str] = {
            "phase1_context": phase1_context,
            "scope_note": f"Scope: {escaped_scope}" if escaped_scope else "",
            "scope": escaped_scope or "(full scope)",
        }

        # Escape braces in file content to prevent str.format() injection —
        # source files routinely contain {variable} patterns (f-strings, Jinja, etc.)
        content_a = self._escape_braces(self._truncate(resolved.role_a_content))
        content_b = self._escape_braces(self._truncate(resolved.role_b_content))

        if rel.type == "implements":
            template_vars.update({
                "spec_role": rel.role_a_name, "spec_path": rel.role_a_path,
                "spec_content": content_a,
                "impl_role": rel.role_b_name, "impl_path": rel.role_b_path,
                "impl_content": content_b,
            })
        elif rel.type == "documents":
            template_vars.update({
                "source_role": rel.role_a_name, "source_path": rel.role_a_path,
                "source_content": content_a,
                "docs_role": rel.role_b_name, "docs_path": rel.role_b_path,
                "docs_content": content_b,
            })
        elif rel.type == "delegates":
            template_vars.update({
                "from_role": rel.role_a_name, "from_path": rel.role_a_path,
                "from_content": content_a,
                "to_role": rel.role_b_name, "to_path": rel.role_b_path,
                "to_content": content_b,
            })
        elif rel.type == "schema_contract":
            template_vars.update({
                "producer_role": rel.role_a_name, "producer_path": rel.role_a_path,
                "producer_content": content_a,
                "consumer_role": rel.role_b_name, "consumer_path": rel.role_b_path,
                "consumer_content": content_b,
            })

        prompt = prompt_template.format(**template_vars)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]

        raw = self.provider.complete_json(
            messages=messages,
            # Cross-artifact consistency is judgment-heavy (spec intent vs implementation
            # semantics) — use tier1 model for deeper reasoning
            model=self.config.model_tier1,
            schema=CROSS_FINDINGS_SCHEMA,
            temperature=self.config.temperature,
        )

        if raw is None:
            raise ValueError("LLM returned empty response")

        return self._parse_findings(raw, resolved)

    def _parse_findings(
        self,
        raw: dict[str, Any],
        resolved: ResolvedRelationship,
    ) -> list[Finding]:
        """Parse LLM findings into Finding objects with multi-locus support."""
        raw_findings = raw.get("findings", [])
        valid: list[Finding] = []
        rel = resolved.relationship

        for i, f in enumerate(raw_findings):
            evidence_result = f.get("evidence_result", "").strip()
            if not evidence_result:
                logger.warning("[%s] Finding #%d rejected: no evidence", self.name, i)
                continue

            # Build loci from location hints in LLM output
            loci: list[Locus] = []
            role_a_loc = f.get("role_a_location", "")
            role_b_loc = f.get("role_b_location", "")

            start_a, end_a = self._parse_line_range(role_a_loc)
            start_b, end_b = self._parse_line_range(role_b_loc)

            if resolved.role_a_exists:
                try:
                    hash_a = Locus.compute_hash_from_content(
                        resolved.role_a_content, start_a, end_a,
                    )
                except Exception as e:
                    logger.debug("Hash computation failed for %s lines %d-%d: %s", rel.role_a_path, start_a, end_a, e)
                    hash_a = ""
                loci.append(Locus(
                    file=rel.role_a_path,
                    start_line=start_a,
                    end_line=end_a,
                    role=rel.role_a_name,
                    source_hash=hash_a,
                ))

            if resolved.role_b_exists:
                try:
                    hash_b = Locus.compute_hash_from_content(
                        resolved.role_b_content, start_b, end_b,
                    )
                except Exception as e:
                    logger.debug("Hash computation failed for %s lines %d-%d: %s", rel.role_b_path, start_b, end_b, e)
                    hash_b = ""
                loci.append(Locus(
                    file=rel.role_b_path,
                    start_line=start_b,
                    end_line=end_b,
                    role=rel.role_b_name,
                    source_hash=hash_b,
                ))

            # Normalize severity — don't let one bad value discard all findings
            raw_severity = f.get("severity", "MEDIUM")
            try:
                severity = Severity(str(raw_severity).upper().strip())
            except (ValueError, KeyError):
                logger.warning("[%s] Finding #%d: invalid severity '%s', defaulting to MEDIUM", self.name, i, raw_severity)
                severity = Severity.MEDIUM

            finding = Finding(
                severity=severity,
                category=f.get("category", "coverage_gap"),
                description=f.get("description", ""),
                evidence=Evidence(
                    tool=f.get("evidence_tool", "cross-analysis"),
                    result=evidence_result,
                ),
                location=f"{rel.role_a_path} ↔ {rel.role_b_path}",
                loci=loci,
                critic=self.name,
                framework_refs=f.get("framework_refs", []),
                remediation=f.get("remediation"),
            )
            valid.append(finding)

        rejected = len(raw_findings) - len(valid)
        if rejected > 0:
            logger.info("[%s] Rejected %d ungrounded findings", self.name, rejected)

        return valid

    @staticmethod
    def _parse_line_range(location_str: str) -> tuple[int, int]:
        """
        Try to extract line numbers from a location string like 'lines 42-50'.
        Returns (start, end) or (1, 1) as fallback.
        """
        if not location_str:
            return (1, 1)

        # Try "lines X-Y" or "line X-Y" (including em-dash separator)
        match = re.search(r'lines?\s+(\d+)\s*[-–]\s*(\d+)', location_str, re.IGNORECASE)
        if match:
            return (int(match.group(1)), int(match.group(2)))

        # Try single "line X"
        match = re.search(r'line\s+(\d+)', location_str, re.IGNORECASE)
        if match:
            line = int(match.group(1))
            return (line, line)

        return (1, 1)

    @staticmethod
    def _escape_braces(text: str) -> str:
        """Escape { and } in file content so str.format() treats them as literals."""
        return text.replace("{", "{{").replace("}", "}}")

    @staticmethod
    def _truncate(text: str, max_chars: int = 30000) -> str:
        """Truncate content to fit in LLM context, preserving start and end."""
        if len(text) <= max_chars:
            return text
        half = max_chars // 2
        omitted = len(text) - max_chars
        return (
            text[:half]
            + f"\n\n... [{omitted} characters truncated] ...\n\n"
            + text[-half:]
        )

    def _format_phase1_context(self, findings: list[Finding]) -> str:
        """Format Phase 1 findings as context for the cross-consistency critic."""
        if not findings:
            return "### Phase 1 Context\nNo issues were flagged by single-file critics."

        lines = [
            "### Phase 1 Context (findings from single-file critics — do NOT duplicate these)",
            f"{len(findings)} findings from Phase 1:",
            "",
        ]
        for f in findings:
            lines.append(f"- [{f.severity.value}] {f.description[:120]}")
            if f.location:
                lines.append(f"  Location: {f.location}")
        return "\n".join(lines)

    @staticmethod
    def _compute_coverage(criteria_evaluated: int, criteria_total: int) -> float:
        """Compute coverage ratio for cross-consistency (relationships evaluated / total)."""
        if criteria_total == 0:
            return 0.0
        return round(criteria_evaluated / criteria_total, 2)
