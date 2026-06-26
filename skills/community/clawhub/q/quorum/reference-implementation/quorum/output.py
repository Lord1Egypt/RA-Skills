# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Terminal output formatter for Quorum.

Produces colored, structured output to stdout:
- Verdict banner (color-coded by status)
- Findings summary (counts by severity)
- Detailed findings list (with evidence excerpts)
- Run directory location

Uses ANSI color codes. Falls back to plain text if terminal doesn't support color.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from quorum.models import AggregatedReport, BatchVerdict, Finding, PreScreenResult, Severity, Verdict, VerdictStatus


# ANSI color codes
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[31m"
    YELLOW  = "\033[33m"
    GREEN   = "\033[32m"
    CYAN    = "\033[36m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    WHITE   = "\033[37m"
    BG_RED    = "\033[41m"
    BG_YELLOW = "\033[43m"
    BG_GREEN  = "\033[42m"
    BG_BLUE   = "\033[44m"


def _supports_color() -> bool:
    """Check if the terminal supports ANSI color codes."""
    if not sys.stdout.isatty():
        return False
    term = os.environ.get("TERM", "")
    if term in ("dumb", ""):
        return False
    return True


def _c(text: str, *codes: str) -> str:
    """Apply color codes to text (or return plain text if no color support)."""
    if not _supports_color():
        return text
    return "".join(codes) + text + Color.RESET


def _severity_color(severity: Severity) -> str:
    """Return the color code for a severity level."""
    return {
        Severity.CRITICAL: Color.RED + Color.BOLD,
        Severity.HIGH:     Color.RED,
        Severity.MEDIUM:   Color.YELLOW,
        Severity.LOW:      Color.CYAN,
        Severity.INFO:     Color.DIM,
    }.get(severity, Color.RESET)


def _verdict_color(status: VerdictStatus) -> str:
    """Return color codes for a verdict status."""
    return {
        VerdictStatus.PASS:            Color.GREEN + Color.BOLD,
        VerdictStatus.PASS_WITH_NOTES: Color.CYAN + Color.BOLD,
        VerdictStatus.REVISE:          Color.YELLOW + Color.BOLD,
        VerdictStatus.REJECT:          Color.RED + Color.BOLD,
    }.get(status, Color.RESET)


def print_prescreen_summary(prescreen: PreScreenResult) -> None:
    """
    Print a compact pre-screen summary before the main verdict.

    Shows overall pass/fail/skip counts plus a brief list of any failed checks.
    Follows the same color/formatting patterns as the rest of output.py.
    """
    total   = prescreen.total_checks
    passed  = prescreen.passed
    failed  = prescreen.failed
    skipped = prescreen.skipped

    # Header line
    if failed == 0:
        label = _c("✓ Pre-screen", Color.GREEN + Color.BOLD)
    else:
        label = _c("✗ Pre-screen", Color.YELLOW + Color.BOLD)

    summary = f"{passed}/{total} passed"
    if skipped:
        summary += f"  {skipped} skipped"
    if failed:
        summary += f"  " + _c(f"{failed} failed", Color.YELLOW + Color.BOLD)

    print(_c("── Pre-Screen ───────────────────────────────────────────────", Color.DIM))
    print()
    print(f"  {label}  {summary}  ({prescreen.runtime_ms}ms)")

    if failed:
        print()
        for check in prescreen.checks:
            if check.result != "FAIL":
                continue
            sev_color = _severity_color(check.severity)
            sev_label = _c(f"[{check.severity.value:8s}]", sev_color)
            print(f"    {sev_label} [{check.id}] {check.name}: {check.description}")
            if check.locations:
                locs = ", ".join(check.locations[:5])
                if len(check.locations) > 5:
                    locs += f" … (+{len(check.locations) - 5} more)"
                print(_c(f"             Locations: {locs}", Color.DIM))

    print()


def print_verdict(
    verdict: Verdict,
    run_dir: Path | None = None,
    verbose: bool = False,
    prescreen: PreScreenResult | None = None,
) -> None:
    """
    Print a complete verdict report to stdout.

    Args:
        verdict:  The Verdict object from the aggregator
        run_dir:  Path to the run directory (for reference)
        verbose:  If True, print full evidence for each finding
    """
    report = verdict.report
    print()

    # ── Pre-Screen Summary (if available) ──────────────────────────────────────
    if prescreen is not None:
        print_prescreen_summary(prescreen)

    # ── Verdict Banner ─────────────────────────────────────────────────────────
    status_str = verdict.status.value
    verdict_color = _verdict_color(verdict.status)
    banner = f" ◆ QUORUM VERDICT: {status_str} "
    print(_c(banner, verdict_color))
    print(_c("─" * len(banner), Color.DIM))
    print()
    print(f"  {verdict.reasoning}")
    print(f"  Confidence: {verdict.confidence:.0%}")
    print()

    if report is None:
        print(_c("  (no report data)", Color.DIM))
        return

    # ── Issue Summary ──────────────────────────────────────────────────────────
    total = len(report.findings)
    if total == 0:
        print(_c("  ✓ No issues found", Color.GREEN + Color.BOLD))
    else:
        counts = []
        if report.critical_count:
            counts.append(_c(f"{report.critical_count} CRITICAL", Color.RED + Color.BOLD))
        if report.high_count:
            counts.append(_c(f"{report.high_count} HIGH", Color.RED))
        if report.medium_count:
            counts.append(_c(f"{report.medium_count} MEDIUM", Color.YELLOW))
        if report.low_count:
            counts.append(_c(f"{report.low_count} LOW/INFO", Color.CYAN))

        print(f"  Issues: {' · '.join(counts)}  ({total} total)")

    if report.conflicts_resolved:
        print(_c(f"  ({report.conflicts_resolved} duplicate findings merged)", Color.DIM))

    print()

    # ── Findings List ──────────────────────────────────────────────────────────
    if report.findings:
        print(_c("── Findings ─────────────────────────────────────────────────", Color.DIM))
        print()

        # Sort by severity (CRITICAL first)
        severity_order = {
            Severity.CRITICAL: 0,
            Severity.HIGH: 1,
            Severity.MEDIUM: 2,
            Severity.LOW: 3,
            Severity.INFO: 4,
        }
        sorted_findings = sorted(report.findings, key=lambda f: severity_order.get(f.severity, 9))

        for i, finding in enumerate(sorted_findings, 1):
            _print_finding(i, finding, verbose=verbose)

    # ── Run Directory ──────────────────────────────────────────────────────────
    if run_dir:
        print(_c("── Outputs ──────────────────────────────────────────────────", Color.DIM))
        print()
        print(f"  Run directory: {run_dir}")
        print(f"  Detailed report: {run_dir / 'report.md'}")
        print(f"  Machine-readable: {run_dir / 'verdict.json'}")
        print()


def _print_finding(index: int, finding: Finding, verbose: bool = False) -> None:
    """Print a single finding with evidence."""
    sev_color = _severity_color(finding.severity)
    sev_label = _c(f"[{finding.severity.value:8s}]", sev_color)

    print(f"  {index:2d}. {sev_label} {finding.description}")

    if finding.location:
        print(_c(f"       Location: {finding.location}", Color.DIM))

    # Multi-locus display (cross-artifact findings)
    if finding.loci:
        for locus in finding.loci:
            loc_str = f"{locus.file}:{locus.start_line}-{locus.end_line} (role: {locus.role})"
            print(_c(f"       Locus:    {loc_str}", Color.DIM))

    if finding.critic:
        sources = finding.critic.strip(",")
        print(_c(f"       Critic:   {sources}", Color.DIM))

    if finding.rubric_criterion:
        print(_c(f"       Criterion: {finding.rubric_criterion}", Color.DIM))

    # Framework references
    if finding.framework_refs:
        print(_c(f"       Refs:     {', '.join(finding.framework_refs)}", Color.DIM))

    if verbose or finding.severity in (Severity.CRITICAL, Severity.HIGH):
        # Always show evidence for CRITICAL/HIGH; show for others only in verbose mode
        evidence_preview = finding.evidence.result.replace("\n", " ").strip()
        if len(evidence_preview) > 120:
            evidence_preview = evidence_preview[:117] + "..."
        print(_c(f"       Evidence [{finding.evidence.tool}]: {evidence_preview}", Color.DIM))

    # Remediation hint (when present)
    if finding.remediation and (verbose or finding.severity in (Severity.CRITICAL, Severity.HIGH)):
        remediation_preview = finding.remediation[:100]
        print(_c(f"       Fix:      {remediation_preview}", Color.DIM))

    print()


def print_batch_verdict(
    batch: BatchVerdict,
    batch_dir: Path | None = None,
    verbose: bool = False,
) -> None:
    """
    Print a consolidated batch verdict report to stdout.

    Args:
        batch:     The BatchVerdict from batch validation
        batch_dir: Path to the batch run directory
        verbose:   If True, print full evidence for each finding
    """
    print()

    # ── Batch Banner ───────────────────────────────────────────────────────────
    verdict_color = _verdict_color(batch.status)
    banner = f" ◆ QUORUM BATCH VERDICT: {batch.status.value} "
    print(_c(banner, verdict_color))
    print(_c("─" * len(banner), Color.DIM))
    print()
    print(f"  {batch.reasoning}")
    print(f"  Confidence: {batch.confidence:.0%}")
    print()

    # ── File Summary ───────────────────────────────────────────────────────────
    print(_c("── Per-File Results ─────────────────────────────────────────", Color.DIM))
    print()

    for fr in batch.file_results:
        name = Path(fr.file_path).name
        status_color = _verdict_color(fr.verdict.status)
        status_str = _c(fr.verdict.status.value, status_color)
        finding_count = len(fr.verdict.report.findings) if fr.verdict.report else 0

        if finding_count:
            print(f"  {status_str:>28s}  {name}  ({finding_count} findings)")
        else:
            print(f"  {status_str:>28s}  {name}")

    print()

    # ── Aggregate Findings ─────────────────────────────────────────────────────
    all_findings: list[tuple[str, Finding]] = []
    for fr in batch.file_results:
        if fr.verdict.report:
            for finding in fr.verdict.report.findings:
                all_findings.append((Path(fr.file_path).name, finding))

    if all_findings:
        # Count by severity
        sev_counts: dict[Severity, int] = {}
        for _, f in all_findings:
            sev_counts[f.severity] = sev_counts.get(f.severity, 0) + 1

        counts_parts = []
        for sev in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO]:
            count = sev_counts.get(sev, 0)
            if count:
                counts_parts.append(_c(f"{count} {sev.value}", _severity_color(sev)))

        print(f"  Total issues: {' · '.join(counts_parts)}  ({len(all_findings)} total)")
        print()

        # Show CRITICAL and HIGH findings always, others only in verbose
        severity_order = {
            Severity.CRITICAL: 0, Severity.HIGH: 1,
            Severity.MEDIUM: 2, Severity.LOW: 3, Severity.INFO: 4,
        }
        sorted_findings = sorted(all_findings, key=lambda x: severity_order.get(x[1].severity, 9))

        print(_c("── Findings ─────────────────────────────────────────────────", Color.DIM))
        print()

        for i, (filename, finding) in enumerate(sorted_findings, 1):
            show = verbose or finding.severity in (Severity.CRITICAL, Severity.HIGH)
            if not show:
                continue
            sev_color = _severity_color(finding.severity)
            sev_label = _c(f"[{finding.severity.value:8s}]", sev_color)
            print(f"  {i:2d}. {sev_label} {_c(filename, Color.CYAN)}: {finding.description[:100]}")

            if finding.location:
                print(_c(f"       Location: {finding.location}", Color.DIM))
            if verbose and finding.evidence:
                evidence_preview = finding.evidence.result.replace("\n", " ").strip()
                if len(evidence_preview) > 120:
                    evidence_preview = evidence_preview[:117] + "..."
                print(_c(f"       Evidence [{finding.evidence.tool}]: {evidence_preview}", Color.DIM))
            print()

        # Note if findings were hidden
        hidden = len(sorted_findings) - sum(
            1 for _, f in sorted_findings
            if verbose or f.severity in (Severity.CRITICAL, Severity.HIGH)
        )
        if hidden:
            print(_c(f"  ({hidden} MEDIUM/LOW/INFO findings hidden — use --verbose to show)", Color.DIM))
            print()

    else:
        print(_c("  ✓ No issues found across any files", Color.GREEN + Color.BOLD))
        print()

    # ── Run Directory ──────────────────────────────────────────────────────────
    if batch_dir:
        print(_c("── Outputs ──────────────────────────────────────────────────", Color.DIM))
        print()
        print(f"  Batch directory: {batch_dir}")
        print(f"  Batch report:    {batch_dir / 'batch-report.md'}")
        print(f"  Batch verdict:   {batch_dir / 'batch-verdict.json'}")
        print()


def print_rubric_list(names: list[str]) -> None:
    """Print available rubric names."""
    print()
    print(_c("Available built-in rubrics:", Color.BOLD))
    for name in names:
        print(f"  • {name}")
    print()


def print_error(message: str) -> None:
    """Print an error message to stderr."""
    print(_c(f"✗ Error: {message}", Color.RED), file=sys.stderr)


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(_c(f"⚠ {message}", Color.YELLOW))
