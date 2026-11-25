"""Report writer - terminal table + markdown report."""
from __future__ import annotations

import datetime
import os
from typing import List, Optional

from .finding import CheckResult, Finding, Severity

SEV_COLOR = {
    Severity.CRIT: "91",
    Severity.HIGH: "31",
    Severity.MED:  "33",
    Severity.LOW:  "36",
    Severity.INFO: "0",
}
SEV_ICON = {
    Severity.CRIT: "‼",
    Severity.HIGH: "▲",
    Severity.MED:  "◆",
    Severity.LOW:  "◇",
    Severity.INFO: "·",
}


def _md_cell(value: object) -> str:
    """Make a value safe for a single Markdown table cell."""
    text = str(value).replace("|", "\\|")
    return " ".join(text.split())


def _md_text(value: str) -> str:
    """Make evidence safe for inline Markdown."""
    return " ".join(value.strip().split()).replace("`", "'")[:200]


def print_report(target: str, results: List[CheckResult], color: bool,
                 show_fp: bool = False) -> None:
    def paint(c: str, s: str) -> str:
        return f"\033[{c}m{s}\033[0m" if color and c not in ("0",) else s

    print()
    print(paint("1", f"  Recon Report - {target}"))
    print(paint("1", f"  {datetime.datetime.now():%Y-%m-%d %H:%M}"))
    print(paint("2", "  " + "─" * 62))

    # per-check summary bar
    for r in results:
        if r.status == "skipped":
            print(f"  {paint('2', '⏭  ')}{r.name:<16} {r.summary}")
            continue
        if r.status == "error":
            print(f"  {paint('31', '✗  ')}{r.name:<16} ERROR: {(r.error or '')[:50]}")
            continue
        acts = [f for f in r.findings if not f.is_false_positive]
        worst = max((f.severity for f in acts), default=Severity.INFO)
        bar = paint("1", f"[{worst.name.upper():>4}]")
        fps = sum(1 for f in r.findings if f.is_false_positive)
        fps_s = f"  {paint('2', f'({fps} FP)')}" if fps else ""
        print(f"  {bar} {r.name:<16} {r.summary}{fps_s}")
    print(paint("2", "  " + "─" * 62))

    # all actionable findings, worst first
    all_findings: List[Finding] = []
    for r in results:
        all_findings.extend(f for f in r.findings if not f.is_false_positive)
    all_findings.sort(key=lambda f: -int(f.severity))
    print()
    print(paint("1", "  Actionable findings:"))
    if not all_findings:
        print("    (none)")
    for f in all_findings:
        icon = SEV_ICON.get(f.severity, "?")
        print(f"    {paint(SEV_COLOR.get(f.severity, '0'), icon + ' ')} [{f.check}] {f.title}")
        if f.evidence and len(f.evidence) < 300:
            for line in f.evidence.strip().splitlines()[:3]:
                print(f"        {paint('2', line)}")
        if f.recommendation:
            print(f"        → {paint('3', f.recommendation)}")
    print()

    # false positives (folded at bottom, or shown on request)
    fps = [f for r in results for f in r.findings if f.is_false_positive]
    if fps:
        if show_fp:
            print(paint("1", "  False positives (triaged):"))
            for f in fps:
                print(f"    {paint('2', '·')} [{f.check}] {f.title}")
            print()
        else:
            print(paint("2", f"  ({len(fps)} false-positive hits hidden - "
                             f"use --show-false-positives to see)"))
    print(paint("2", "  " + "─" * 62))
    print()


def open_report_file(path: str, overwrite: bool = False):
    """Open ``path`` for writing with exclusive-creation semantics.

    ``os.open`` is called with ``O_CREAT | O_EXCL`` so an existing file - or a
    symlink at ``path`` - is never truncated or followed. With ``overwrite``
    set (an explicit user opt-in) an existing regular file is removed first
    and the path is then created exclusively.
    """
    if overwrite and os.path.lexists(path) and not os.path.isdir(path):
        os.remove(path)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o644)
    return os.fdopen(fd, "w", encoding="utf-8")


def write_markdown(target: str, results: List[CheckResult], path: Optional[str],
                   show_fp: bool = False, overwrite: bool = False) -> Optional[str]:
    """Write audit report to a file.

    The file is created with exclusive creation (``O_CREAT | O_EXCL`` semantics,
    like ``open(path, "x")``): an existing file or symlink at ``path`` raises
    ``FileExistsError`` instead of being truncated. ``overwrite=True`` is the
    explicit opt-in that replaces an existing regular file.
    """
    if not path:
        return None
    ts = datetime.datetime.now()
    L = []
    L.append(f"# Recon Report - {target}\n")
    L.append(f"_Generated: {ts:%Y-%m-%d %H:%M} · tool: recon-cli (active, stdlib-only)_\n")
    L.append("## Summary\n")
    L.append("| Check | Status | Summary | Actionable | FP |")
    L.append("|---|---|---|---|---|")
    for r in results:
        acts = sum(1 for f in r.findings if not f.is_false_positive)
        fps = sum(1 for f in r.findings if f.is_false_positive)
        L.append(
            f"| {_md_cell(r.name)} | {_md_cell(r.status)} | "
            f"{_md_cell(r.summary)} | {acts} | {fps} |"
        )
    L.append("")
    for r in results:
        L.append(f"## {r.name}\n")
        if r.error:
            L.append(f"> **error**: {_md_text(r.error)}\n")
        for f in r.findings:
            if f.is_false_positive and not show_fp:
                continue
            marker = " (FP)" if f.is_false_positive else ""
            L.append(f"- **[{f.severity.name}{marker}]** {f.title}")
            if f.evidence:
                L.append(f"  - evidence: `{_md_text(f.evidence)}`")
            if f.recommendation:
                L.append(f"  - action: {f.recommendation}")
        L.append("")
    L.append("## False positives\n")
    if show_fp:
        fps = [f for r in results for f in r.findings if f.is_false_positive]
        if fps:
            for f in fps:
                L.append(f"- `{f.check}` {f.title}")
        else:
            L.append("(none)")
    else:
        L.append("Hidden - pass `--show-false-positives` to include them.")
    L.append("")
    with open_report_file(path, overwrite) as fh:
        fh.write("\n".join(L) + "\n")
    return path
