# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Fixer Agent — Proposes concrete patches for CRITICAL and HIGH findings.

The Fixer:
1. Receives findings from Phase 1 critics
2. Filters to CRITICAL and HIGH only
3. For each finding, proposes a specific code/text change
4. Returns structured FixProposal objects

The Fixer does NOT apply changes — it proposes them for human review.
Fix loops (re-validation after applying proposals) are optional and capped.
"""

from __future__ import annotations

import logging
from typing import Any

from quorum.config import QuorumConfig
from quorum.models import Finding, FixProposal, FixReport, Severity
from quorum.providers.base import BaseProvider

logger = logging.getLogger(__name__)

# JSON schema for structured fix proposals from the LLM
_FIX_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["fixes"],
    "properties": {
        "fixes": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "finding_id",
                    "original_text",
                    "replacement_text",
                    "explanation",
                    "confidence",
                ],
                "properties": {
                    "finding_id": {"type": "string"},
                    "original_text": {
                        "type": "string",
                        "description": "Exact text from the artifact to replace (must match verbatim)",
                    },
                    "replacement_text": {
                        "type": "string",
                        "description": "The corrected text",
                    },
                    "explanation": {"type": "string"},
                    "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                    },
                },
            },
        }
    },
}

_SYSTEM_PROMPT = """\
You are the Fixer for Quorum, a code quality validation system.

You receive findings (issues) from independent critics along with the full artifact text.
Your job: propose EXACT text replacements that fix each issue.

Rules:
1. original_text MUST appear verbatim in the artifact — if you can't find the exact text, skip the finding
2. replacement_text should be minimal — change only what's needed to fix the issue
3. Do NOT refactor or improve code beyond what the finding requires
4. For each fix, explain WHY the replacement resolves the issue
5. Set confidence: 0.9+ if the fix is straightforward, 0.5-0.8 if the fix might have side effects, <0.5 if you're uncertain
6. Skip findings that require architectural changes, new files, or changes outside the artifact — add to skip_reasons
7. Only address CRITICAL and HIGH findings — ignore MEDIUM/LOW/INFO
"""


def _format_findings(findings: list[Finding]) -> str:
    """Format findings as a numbered list for the user prompt."""
    lines: list[str] = []
    for i, f in enumerate(findings, 1):
        lines.append(f"{i}. [{f.id}] [{f.severity.value}] {f.description}")
        if f.location:
            lines.append(f"   Location: {f.location}")
        if f.remediation:
            lines.append(f"   Suggested fix: {f.remediation}")
        lines.append("")
    return "\n".join(lines)


class FixerAgent:
    """Proposes concrete patches for CRITICAL and HIGH findings."""

    def __init__(self, provider: BaseProvider, config: QuorumConfig):
        self.provider = provider
        self.config = config

    def run(
        self,
        findings: list[Finding],
        artifact_text: str,
        artifact_path: str,
    ) -> FixReport:
        """
        Propose fixes for CRITICAL and HIGH findings.

        Uses tier1 model — fix proposals require deep understanding.

        Args:
            findings:      List of findings (should already be filtered to CRITICAL/HIGH
                           by the caller, but we double-check here)
            artifact_text: Full text of the artifact being fixed
            artifact_path: Path to the artifact (for display in proposals)

        Returns:
            FixReport with proposed fixes and any skip reasons
        """
        # Double-check: only operate on CRITICAL and HIGH
        actionable = [
            f for f in findings
            if f.severity in (Severity.CRITICAL, Severity.HIGH)
        ]

        if not actionable:
            logger.info("Fixer: no CRITICAL/HIGH findings to address")
            return FixReport(
                proposals=[],
                findings_addressed=0,
                findings_skipped=len(findings),
                skip_reasons=["All findings were below CRITICAL/HIGH threshold"],
            )

        logger.info("Fixer: proposing fixes for %d CRITICAL/HIGH findings", len(actionable))

        user_prompt = (
            f"## Artifact ({artifact_path})\n\n"
            f"```\n{artifact_text}\n```\n\n"
            f"## Findings to Fix\n\n"
            f"{_format_findings(actionable)}\n"
            f"For each finding, propose an exact text replacement. If a finding cannot be fixed\n"
            f"with a text replacement (requires new files, architectural changes, or external\n"
            f"dependencies), skip it and explain why."
        )

        messages = [
            {"role": "user", "content": user_prompt},
        ]

        try:
            raw = self.provider.complete_json(
                messages=messages,
                model=self.config.model_tier1,
                schema=_FIX_SCHEMA,
                temperature=self.config.temperature,
            )
        except Exception as e:
            logger.error("Fixer LLM call failed: %s", e)
            return FixReport(
                proposals=[],
                findings_addressed=0,
                findings_skipped=len(actionable),
                skip_reasons=[f"LLM call failed: {e}"],
            )

        # Build a lookup map: finding_id → finding
        finding_map = {f.id: f for f in actionable}

        proposals: list[FixProposal] = []
        skip_reasons: list[str] = []
        addressed_ids: set[str] = set()

        for fix_dict in raw.get("fixes", []):
            fid = fix_dict.get("finding_id", "")
            original = fix_dict.get("original_text", "")
            replacement = fix_dict.get("replacement_text", "")
            explanation = fix_dict.get("explanation", "")
            confidence = float(fix_dict.get("confidence", 0.5))

            # Validate the finding_id exists
            finding = finding_map.get(fid)
            if finding is None:
                # Try to match by partial ID (LLM sometimes drops the prefix)
                for known_id, known_finding in finding_map.items():
                    if fid in known_id or known_id in fid:
                        finding = known_finding
                        fid = known_id
                        break

            if finding is None:
                skip_reasons.append(f"Skipped unknown finding_id '{fid}'")
                continue

            # Verify original_text actually appears in the artifact
            if original and original not in artifact_text:
                skip_reasons.append(
                    f"[{fid}] original_text not found verbatim in artifact — skipped"
                )
                continue

            # Skip empty proposals
            if not original or not replacement:
                skip_reasons.append(f"[{fid}] LLM returned empty original_text or replacement_text")
                continue

            proposals.append(
                FixProposal(
                    finding_id=fid,
                    finding_description=finding.description[:200],
                    file_path=artifact_path,
                    original_text=original,
                    replacement_text=replacement,
                    explanation=explanation,
                    confidence=confidence,
                )
            )
            addressed_ids.add(fid)

        # Any findings not addressed by the LLM
        unaddressed = [f for f in actionable if f.id not in addressed_ids]
        for f in unaddressed:
            skip_reasons.append(f"[{f.id}] No fix proposed by LLM (may require architectural changes)")

        logger.info(
            "Fixer complete: %d proposals, %d skipped",
            len(proposals),
            len(skip_reasons),
        )

        return FixReport(
            proposals=proposals,
            findings_addressed=len(proposals),
            findings_skipped=len(actionable) - len(proposals),
            skip_reasons=skip_reasons,
            loop_number=1,
            revalidation_verdict=None,
            revalidation_delta=None,
        )
