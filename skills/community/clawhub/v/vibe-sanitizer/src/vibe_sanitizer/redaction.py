from __future__ import annotations

from collections import defaultdict

from .models import Finding


def apply_replacements(text: str, findings: list[Finding], *, in_place_only: bool) -> str:
    applicable = [
        finding
        for finding in findings
        if finding.replacement_text is not None and (finding.editable_in_place or not in_place_only)
    ]
    if not applicable:
        return text

    updated = text
    for finding in sorted(applicable, key=lambda item: item.start_offset, reverse=True):
        updated = (
            updated[: finding.start_offset]
            + finding.replacement_text
            + updated[finding.end_offset :]
        )
    return updated


def findings_by_path(findings: list[Finding]) -> dict[str, list[Finding]]:
    grouped: dict[str, list[Finding]] = defaultdict(list)
    for finding in findings:
        grouped[finding.path].append(finding)
    for path_findings in grouped.values():
        path_findings.sort(key=lambda item: item.start_offset)
    return dict(grouped)
