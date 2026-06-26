# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Abstract base class for all Quorum critics.

Each critic is responsible for:
1. Building a focused prompt from the rubric criteria in its domain
2. Calling the LLM to get structured findings
3. Validating that every finding has evidence
4. Returning a CriticResult
"""

from __future__ import annotations

import abc
import json
import logging
import time
from typing import Any

from quorum.config import QuorumConfig
from quorum.models import CriticResult, Evidence, Finding, Rubric, Severity
from quorum.providers.base import BaseProvider

logger = logging.getLogger(__name__)


# JSON schema that critics request from the LLM
FINDINGS_SCHEMA = {
    "type": "object",
    "required": ["findings"],
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["severity", "description", "evidence_tool", "evidence_result"],
                "properties": {
                    "severity": {
                        "type": "string",
                        "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"],
                    },
                    "description": {"type": "string"},
                    "evidence_tool": {
                        "type": "string",
                        "description": "How you verified this (grep, schema, read, analysis)",
                    },
                    "evidence_result": {
                        "type": "string",
                        "description": "The actual excerpt, match, or output that proves this finding",
                    },
                    "location": {
                        "type": "string",
                        "description": "Where in the artifact (section name, line, key path)",
                    },
                    "rubric_criterion": {
                        "type": "string",
                        "description": "The rubric criterion ID this finding addresses",
                    },
                },
            },
        }
    },
}


class BaseCritic(abc.ABC):
    """
    Abstract critic base class.

    Subclasses implement:
    - name: str — unique name for this critic
    - system_prompt: str — the critic's role definition
    - build_prompt() — constructs the evaluation prompt from artifact + rubric
    """

    name: str = "base"

    def __init__(self, provider: BaseProvider, config: QuorumConfig):
        self.provider = provider
        self.config = config

    @property
    @abc.abstractmethod
    def system_prompt(self) -> str:
        """System prompt that defines this critic's role and expertise."""
        ...

    @abc.abstractmethod
    def build_prompt(self, artifact_text: str, rubric: Rubric) -> str:
        """
        Build the user-facing evaluation prompt.

        Args:
            artifact_text: The full text of the artifact being reviewed
            rubric: The rubric to evaluate against

        Returns:
            A prompt string to send to the LLM
        """
        ...

    def evaluate(
        self,
        artifact_text: str,
        rubric: Rubric,
        extra_context: dict[str, Any] | None = None,
        mandatory_context: str | None = None,
    ) -> CriticResult:
        """
        Evaluate the artifact against the rubric.

        This is the main entry point. It:
        1. Builds the prompt
        2. Calls the LLM for structured findings
        3. Validates evidence is present for each finding
        4. Returns a CriticResult

        Args:
            artifact_text:     Full text of the artifact
            rubric:            Domain-specific rubric
            extra_context:     Optional extra context (tool results, known issues, etc.)
            mandatory_context: Known recurring patterns to prepend to the system prompt

        Returns:
            CriticResult with zero or more evidence-grounded findings
        """
        start_ms = int(time.time() * 1000)
        logger.info("[%s] Starting evaluation", self.name)

        try:
            prompt = self.build_prompt(artifact_text, rubric)
            if extra_context:
                ctx_str = json.dumps(extra_context, indent=2) if isinstance(extra_context, dict) else str(extra_context)
                prompt += f"\n\n### Additional Context\n{ctx_str}"

            system = self.system_prompt
            if mandatory_context:
                system = mandatory_context + "\n\n" + system

            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ]

            raw = self.provider.complete_json(
                messages=messages,
                model=self.config.model_tier2,  # Critics use tier 2 by default
                schema=FINDINGS_SCHEMA,
                temperature=self.config.temperature,
            )

            if raw is None:
                raise ValueError("LLM returned empty response")

            findings = self._parse_findings(raw)
            criteria_total = len(rubric.criteria)
            criteria_evaluated = self._count_criteria_evaluated(findings, rubric)
            confidence = self._compute_coverage(criteria_evaluated, criteria_total)

        except Exception as e:
            logger.exception("[%s] Evaluation failed: %s", self.name, e)
            runtime_ms = int(time.time() * 1000) - start_ms
            # Sanitize: use exception type + message, not raw str(e) which may leak paths
            err_type = type(e).__name__
            return CriticResult(
                critic_name=self.name,
                findings=[],
                confidence=0.0,
                criteria_total=0,
                criteria_evaluated=0,
                runtime_ms=runtime_ms,
                skipped=True,
                skip_reason=f"Evaluation failed ({err_type})",
            )

        runtime_ms = int(time.time() * 1000) - start_ms
        logger.info(
            "[%s] Done: %d findings, %d/%d criteria in %dms (coverage=%.0f%%)",
            self.name, len(findings), criteria_evaluated, criteria_total,
            runtime_ms, confidence * 100,
        )

        return CriticResult(
            critic_name=self.name,
            findings=findings,
            confidence=confidence,
            criteria_total=criteria_total,
            criteria_evaluated=criteria_evaluated,
            runtime_ms=runtime_ms,
        )

    def _parse_findings(self, raw: dict[str, Any]) -> list[Finding]:
        """
        Parse and validate LLM-returned findings.
        Rejects any finding that lacks evidence — this enforces the core Quorum principle.
        """
        raw_findings = raw.get("findings", [])
        valid: list[Finding] = []

        for i, f in enumerate(raw_findings):
            evidence_result = f.get("evidence_result", "").strip()
            if not evidence_result:
                logger.warning(
                    "[%s] Finding #%d rejected: no evidence provided. Description: %s",
                    self.name, i, f.get("description", "")[:80],
                )
                continue  # Reject ungrounded claims

            evidence_tool = f.get("evidence_tool", "llm-analysis")
            citation = f.get("rubric_criterion")

            # Normalize and validate severity — don't let one bad value discard all findings
            raw_severity = f.get("severity", "MEDIUM")
            try:
                severity = Severity(str(raw_severity).upper().strip())
            except (ValueError, KeyError):
                logger.warning(
                    "[%s] Finding #%d: invalid severity '%s', defaulting to MEDIUM",
                    self.name, i, raw_severity,
                )
                severity = Severity.MEDIUM

            finding = Finding(
                severity=severity,
                description=f.get("description", ""),
                evidence=Evidence(
                    tool=evidence_tool,
                    result=evidence_result,
                    citation=citation,
                ),
                location=f.get("location"),
                critic=self.name,
                rubric_criterion=citation,
            )
            valid.append(finding)

        rejected = len(raw_findings) - len(valid)
        if rejected > 0:
            logger.info("[%s] Rejected %d ungrounded findings", self.name, rejected)

        return valid

    @staticmethod
    def _count_criteria_evaluated(findings: list[Finding], rubric: Rubric) -> int:
        """
        Count rubric criteria in scope for this evaluation.

        Currently returns total criteria count because all criteria are included
        in the critic's prompt. Criteria without findings represent implicit PASS
        (the critic evaluated them and found no issues). This is an honest
        representation: the critic was asked about all criteria, so all were evaluated.
        """
        if not rubric.criteria:
            return 0
        return len(rubric.criteria)

    @staticmethod
    def _compute_coverage(criteria_evaluated: int, criteria_total: int) -> float:
        """
        Compute coverage ratio as the confidence value.

        This replaces the fabricated 0.50-0.95 formula with an honest metric:
        what fraction of the rubric criteria were in scope for this evaluation.
        """
        if criteria_total == 0:
            return 0.0
        return round(criteria_evaluated / criteria_total, 2)
