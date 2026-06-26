# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Aggregator Agent — Deduplicates findings, resolves conflicts, produces verdict.

The Aggregator:
1. Collects all CriticResults
2. Deduplicates findings that describe the same issue from different critics
3. Computes criteria coverage from per-critic evaluation counts
4. Assigns the final Verdict (PASS / PASS_WITH_NOTES / REVISE / REJECT)

The verdict is determined by the highest severity findings:
- REJECT:          Any CRITICAL findings present
- REVISE:          Any HIGH findings present
- PASS_WITH_NOTES: Any MEDIUM or LOW findings present
- PASS:            No findings (or all INFO)
"""

from __future__ import annotations

import logging
from difflib import SequenceMatcher

from quorum.config import QuorumConfig
from quorum.models import (
    AggregatedReport,
    CriticResult,
    Finding,
    Severity,
    TesterResult,
    Verdict,
    VerdictStatus,
    VerificationStatus,
)
from quorum.providers.base import BaseProvider

logger = logging.getLogger(__name__)

# Similarity threshold for deduplication (0.0–1.0)
# Findings with description similarity above this are considered duplicates
DEDUP_THRESHOLD = 0.72

# Severity ordering for deduplication (higher = more severe)
# Used to keep the highest-severity finding when duplicates are detected
SEVERITY_ORDER = {
    Severity.CRITICAL: 5,
    Severity.HIGH: 4,
    Severity.MEDIUM: 3,
    Severity.LOW: 2,
    Severity.INFO: 1,
}


class AggregatorAgent:
    """
    Synthesizes findings from multiple critics into a coherent verdict.

    Does NOT call the LLM for verdict assignment (uses deterministic rules).
    A future version could use the LLM for subtle conflict resolution.
    """

    def __init__(self, provider: BaseProvider, config: QuorumConfig):
        self.provider = provider
        self.config = config

    def run(self, critic_results: list[CriticResult], tester_result: TesterResult | None = None) -> Verdict:
        """
        Main entry point.

        Args:
            critic_results: List of CriticResult from each critic
            tester_result:  Optional TesterResult from Phase 3 verification

        Returns:
            Final Verdict with AggregatedReport attached
        """
        all_findings = self._collect_findings(critic_results)

        # DEC-020: Apply tester results before deduplication
        l1_excluded_count = 0
        if tester_result is not None:
            all_findings, l1_excluded_count = self._apply_tester_results(
                all_findings, tester_result,
            )

        deduped_findings, conflicts_resolved = self._deduplicate(all_findings)
        confidence = self._calculate_confidence(critic_results, deduped_findings)

        report = AggregatedReport(
            findings=deduped_findings,
            confidence=confidence,
            conflicts_resolved=conflicts_resolved,
            critic_results=critic_results,
            tester_result=tester_result,
            l1_excluded_count=l1_excluded_count,
        )

        verdict = self._assign_verdict(report, l1_excluded_count=l1_excluded_count)
        logger.info(
            "Aggregator: %d findings → %d deduped → verdict=%s (confidence=%.2f)",
            len(all_findings), len(deduped_findings), verdict.status.value, confidence,
        )
        if l1_excluded_count > 0:
            logger.info(
                "Aggregator: %d finding(s) excluded by Tester (L1 contradicted)",
                l1_excluded_count,
            )

        return verdict

    def _apply_tester_results(
        self,
        findings: list[Finding],
        tester_result: TesterResult,
    ) -> tuple[list[Finding], int]:
        """Apply DEC-020: auto-exclude L1 contradictions, annotate L2 contradictions.

        Returns (filtered_findings, l1_excluded_count).
        """
        # Build mapping: finding_id → VerificationResult
        verification_map = {
            vr.original_finding_id: vr
            for vr in tester_result.verification_results
        }

        filtered: list[Finding] = []
        l1_excluded = 0

        for finding in findings:
            vr = verification_map.get(finding.id)
            if vr is None:
                filtered.append(finding)
                continue

            if vr.status == VerificationStatus.CONTRADICTED and vr.level == 1:
                # L1 CONTRADICTED: auto-exclude from verdict
                l1_excluded += 1
                logger.debug(
                    "DEC-020: Excluding finding %s (L1 contradicted): %s",
                    finding.id, vr.explanation,
                )
                continue

            if vr.status == VerificationStatus.CONTRADICTED and vr.level == 2:
                # L2 CONTRADICTED: annotate only, keep in verdict
                annotated = finding.model_copy(
                    update={"description": f"[L2-CONTRADICTED] {finding.description}"}
                )
                filtered.append(annotated)
                logger.debug(
                    "DEC-020: Annotating finding %s (L2 contradicted): %s",
                    finding.id, vr.explanation,
                )
                continue

            filtered.append(finding)

        return filtered, l1_excluded

    def _collect_findings(self, results: list[CriticResult]) -> list[Finding]:
        """Flatten all findings from all critics into a single list."""
        findings = []
        for result in results:
            if not result.skipped:
                try:
                    if result.findings:
                        findings.extend(result.findings)
                except (TypeError, AttributeError) as e:
                    logger.warning(
                        "Skipping malformed findings from critic '%s': %s",
                        result.critic_name, e,
                    )
        return findings

    def _similarity(self, a: str, b: str) -> float:
        """String similarity ratio between two descriptions."""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def _deduplicate(
        self, findings: list[Finding]
    ) -> tuple[list[Finding], int]:
        """
        Remove duplicate findings reported by multiple critics.

        Strategy: For each pair of findings, if their descriptions are
        above DEDUP_THRESHOLD similar, keep the one with higher severity
        (or the first one if equal). Tag the survivor with all source critics.

        Returns:
            (deduplicated_findings, number_of_conflicts_resolved)
        """
        if not findings:
            return [], 0

        # Sort by severity descending for deterministic dedup regardless of input order
        sorted_findings = sorted(
            findings,
            key=lambda f: SEVERITY_ORDER.get(f.severity, 0),
            reverse=True,
        )

        kept: list[Finding] = []
        conflicts_resolved = 0

        for candidate in sorted_findings:
            is_duplicate = False
            for i, existing in enumerate(kept):
                sim = self._similarity(candidate.description, existing.description)
                if sim >= DEDUP_THRESHOLD:
                    is_duplicate = True
                    conflicts_resolved += 1
                    # Keep the higher-severity finding, merge critic attribution
                    winner = (
                        candidate
                        if SEVERITY_ORDER.get(candidate.severity, 0) > SEVERITY_ORDER.get(existing.severity, 0)
                        else existing
                    )
                    merged_source = f"{existing.critic},{candidate.critic}"
                    kept[i] = winner.model_copy(
                        update={"critic": merged_source}
                    )
                    break

            if not is_duplicate:
                kept.append(candidate)

        return kept, conflicts_resolved

    def _calculate_confidence(
        self,
        results: list[CriticResult],
        findings: list[Finding],
    ) -> float:
        """
        Calculate overall coverage from criteria counts across all critics.

        Returns the ratio of total criteria evaluated to total criteria in scope.
        Skipped critics contribute 0 evaluated out of their expected criteria.
        This is an honest coverage metric, not a fabricated probability.
        """
        total_criteria = sum(r.criteria_total for r in results)
        evaluated_criteria = sum(
            r.criteria_evaluated for r in results if not r.skipped
        )

        if total_criteria == 0:
            return 0.0

        return round(evaluated_criteria / total_criteria, 3)

    def _assign_verdict(self, report: AggregatedReport, l1_excluded_count: int = 0) -> Verdict:
        """
        Deterministic verdict assignment based on findings severity.

        Rules:
        - REJECT:          1+ CRITICAL findings
        - REVISE:          1+ HIGH findings (no CRITICAL)
        - PASS_WITH_NOTES: 1+ MEDIUM/LOW findings (no CRITICAL/HIGH)
        - PASS:            No findings above INFO level
        """
        findings = report.findings

        critical = [f for f in findings if f.severity == Severity.CRITICAL]
        high = [f for f in findings if f.severity == Severity.HIGH]
        medium = [f for f in findings if f.severity == Severity.MEDIUM]
        low = [f for f in findings if f.severity == Severity.LOW]
        info = [f for f in findings if f.severity == Severity.INFO]

        if critical:
            status = VerdictStatus.REJECT
            reasoning = (
                f"Found {len(critical)} CRITICAL issue(s) that must be resolved before acceptance. "
                f"Critical issues represent fundamental problems with the artifact."
            )
        elif high:
            status = VerdictStatus.REVISE
            reasoning = (
                f"Found {len(high)} HIGH severity issue(s) requiring rework. "
                f"Address these before the artifact can be accepted."
            )
        elif medium or low:
            status = VerdictStatus.PASS_WITH_NOTES
            total_notes = len(medium) + len(low)
            reasoning = (
                f"Artifact passes with {total_notes} note(s). "
                f"No blocking issues found; recommendations are advisory."
            )
        else:
            # INFO-only or no findings → PASS
            status = VerdictStatus.PASS
            if info:
                reasoning = (
                    f"No actionable issues found. {len(info)} informational note(s) recorded. "
                    f"The artifact meets all evaluated criteria."
                )
            else:
                reasoning = "No issues found. The artifact meets all evaluated criteria."

        # Add summary counts to reasoning
        counts = []
        if critical:
            counts.append(f"{len(critical)} CRITICAL")
        if high:
            counts.append(f"{len(high)} HIGH")
        if medium:
            counts.append(f"{len(medium)} MEDIUM")
        if low:
            counts.append(f"{len(low)} LOW")
        if info:
            counts.append(f"{len(info)} INFO")

        if counts:
            reasoning += f" Issues: {', '.join(counts)}."

        if l1_excluded_count > 0:
            reasoning += f" {l1_excluded_count} finding(s) excluded by Tester (L1 contradicted)."

        return Verdict(
            status=status,
            reasoning=reasoning,
            confidence=report.confidence,
            report=report,
        )
