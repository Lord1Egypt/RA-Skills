from __future__ import annotations

import json

from .colors import BOLD, CYAN, DIM, GREEN, MAGENTA, RED, YELLOW, colorize, severity_color, use_color
from .models import ScanReport


def format_scan_report(
    report: ScanReport,
    output_format: str,
    *,
    color_mode: str = "auto",
    is_tty: bool | None = None,
) -> str:
    if output_format == "json":
        return json.dumps(report.to_public_dict(), indent=2, sort_keys=False)
    return _format_text_report(report, color_mode=color_mode, is_tty=is_tty)


def _format_text_report(report: ScanReport, *, color_mode: str, is_tty: bool | None) -> str:
    colored = use_color(color_mode, is_tty=is_tty)
    label = lambda text: colorize(text, BOLD, CYAN, enabled=colored)
    lines = [
        f"{label('Root:')} {report.root}",
        f"{label('Scope:')} {report.scope}",
        f"{label('Files scanned:')} {report.files_scanned}",
        f"{label('Files skipped:')} {report.files_skipped}",
        f"{label('Findings:')} {colorize(str(report.total_findings), BOLD, MAGENTA, enabled=colored)}",
        f"{label('Fixable in-place:')} {colorize(str(report.fixable_findings), GREEN, enabled=colored)}",
        f"{label('Review-required:')} {colorize(str(report.review_required_findings), YELLOW, enabled=colored)}",
    ]

    if not report.findings:
        lines.append(f"{label('Status:')} {colorize('clean', BOLD, GREEN, enabled=colored)}")
        return "\n".join(lines)

    lines.append(f"{label('Status:')} {colorize('findings detected', BOLD, RED, enabled=colored)}")
    for finding in report.findings:
        edit_scope = "fixable" if finding.editable_in_place else "review-required"
        sev = colorize(finding.severity, BOLD, severity_color(finding.severity), enabled=colored)
        scope_color = GREEN if finding.editable_in_place else YELLOW
        edit = colorize(edit_scope, scope_color, enabled=colored)
        detector = colorize(finding.detector_id, BOLD, enabled=colored)
        location = colorize(f"{finding.path}:{finding.line}:{finding.column}", DIM, enabled=colored)
        lines.extend(
            [
                "",
                f"[{sev}][{edit}] {detector} {location}",
                f"  {finding.message}",
                f"  {label('Preview:')} {finding.preview}",
            ]
        )
    return "\n".join(lines)
