"""Redaction report generation."""

from __future__ import annotations

import json

from ..models import RedactionReport


def report_to_json(report: RedactionReport) -> str:
    """Serialize redaction report to JSON string."""
    return json.dumps(report.to_dict(), indent=2, ensure_ascii=False)


def report_to_text(report: RedactionReport) -> str:
    """Human-readable summary of redaction results."""
    lines = [
        f"Redaction Report",
        f"================",
        f"Lines processed: {report.lines_processed}",
        f"Total PII found: {report.total_found}",
        f"Regex matched:   {report.regex_matched}",
        "",
    ]
    if report.replacements:
        lines.append("Replacements:")
        for m in report.replacements:
            lines.append(
                f"  Line {m.line_number}: {m.pii_type.value} "
                f"({m.original_snippet}) → {m.placeholder}"
            )
    else:
        lines.append("No PII detected.")
    return "\n".join(lines)
