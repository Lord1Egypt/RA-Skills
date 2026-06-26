"""Multi-format report rendering: text, JSON, Markdown."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Literal

from pylinter_assist.checks.base import Severity
from pylinter_assist.linter import LintReport

OutputFormat = Literal["text", "json", "markdown"]

_SEVERITY_EMOJI = {
    Severity.ERROR: "🔴",
    Severity.WARNING: "🟡",
    Severity.INFO: "🔵",
}

_SEVERITY_LABEL = {
    Severity.ERROR: "ERROR",
    Severity.WARNING: "WARNING",
    Severity.INFO: "INFO",
}


def render(report: LintReport, fmt: OutputFormat = "markdown", include_info: bool = True) -> str:
    if fmt == "json":
        return _render_json(report, include_info)
    if fmt == "text":
        return _render_text(report, include_info)
    return _render_markdown(report, include_info)


# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------

def _render_text(report: LintReport, include_info: bool) -> str:
    lines: list[str] = []
    results = report.all_results
    if not include_info:
        results = [r for r in results if r.severity != Severity.INFO]

    if not results and not report.errors:
        lines.append("No issues found.")
    else:
        for r in sorted(results, key=lambda x: (x.file, x.line)):
            lines.append(str(r))

    if report.pylint_score is not None:
        lines.append(f"\nPylint score: {report.pylint_score:.2f}/10")

    if report.errors:
        lines.append("\nErrors during linting:")
        for e in report.errors:
            lines.append(f"  {e}")

    total = len(results)
    errs = sum(1 for r in results if r.severity == Severity.ERROR)
    warns = sum(1 for r in results if r.severity == Severity.WARNING)
    lines.append(f"\nTotal: {total} ({errs} errors, {warns} warnings)")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON
# ---------------------------------------------------------------------------

def _render_json(report: LintReport, include_info: bool) -> str:
    results = report.all_results
    if not include_info:
        results = [r for r in results if r.severity != Severity.INFO]

    payload = {
        "summary": {
            "files_checked": len(report.files_checked),
            "total": len(results),
            "errors": sum(1 for r in results if r.severity == Severity.ERROR),
            "warnings": sum(1 for r in results if r.severity == Severity.WARNING),
            "info": sum(1 for r in results if r.severity == Severity.INFO),
            "pylint_score": report.pylint_score,
        },
        "results": [
            {
                "file": r.file,
                "line": r.line,
                "col": r.col,
                "severity": r.severity.value,
                "code": r.code,
                "message": r.message,
                "check": r.check_name,
                "context": r.context,
            }
            for r in sorted(results, key=lambda x: (x.file, x.line))
        ],
        "errors": report.errors,
    }
    return json.dumps(payload, indent=2)


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

def _render_markdown(report: LintReport, include_info: bool) -> str:
    results = report.all_results
    if not include_info:
        results = [r for r in results if r.severity != Severity.INFO]

    errs = [r for r in results if r.severity == Severity.ERROR]
    warns = [r for r in results if r.severity == Severity.WARNING]
    infos = [r for r in results if r.severity == Severity.INFO]

    lines: list[str] = ["## Pylint Assist Report\n"]

    # Summary badges
    score_str = f" | Pylint score: **{report.pylint_score:.2f}/10**" if report.pylint_score is not None else ""
    lines.append(
        f"**Files checked:** {len(report.files_checked)}{score_str}  \n"
        f"🔴 {len(errs)} errors &nbsp; 🟡 {len(warns)} warnings &nbsp; 🔵 {len(infos)} info\n"
    )

    if not results and not report.errors:
        lines.append("✅ **No issues found.**\n")
        return "\n".join(lines)

    for severity, bucket in [(Severity.ERROR, errs), (Severity.WARNING, warns), (Severity.INFO, infos)]:
        if not bucket:
            continue
        if severity == Severity.INFO and not include_info:
            continue

        emoji = _SEVERITY_EMOJI[severity]
        label = _SEVERITY_LABEL[severity]
        lines.append(f"<details open>\n<summary>{emoji} {label}S ({len(bucket)})</summary>\n")
        lines.append("| File | Line | Code | Message |")
        lines.append("|------|------|------|---------|")

        for r in sorted(bucket, key=lambda x: (x.file, x.line)):
            file_link = f"`{r.file}:{r.line}`"
            msg = r.message.replace("|", "\\|")
            lines.append(f"| {file_link} | {r.line} | `{r.code}` | {msg} |")

        lines.append("</details>\n")

    if report.errors:
        lines.append("<details>\n<summary>⚠️ Linter errors</summary>\n")
        for e in report.errors:
            lines.append(f"- `{e}`")
        lines.append("</details>\n")

    return "\n".join(lines)
