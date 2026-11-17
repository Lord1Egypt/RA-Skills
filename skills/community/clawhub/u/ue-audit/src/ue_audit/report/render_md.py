"""Markdown report renderer."""

from __future__ import annotations

from pathlib import Path

from .model import Report, Severity, Status


def _cell(value: object) -> str:
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", " ")


def render_markdown(report: Report, path: Path) -> Path:
    data = report.to_dict()
    lines: list[str] = []
    lines.append(f"# UE project audit: {data['project'].get('name', '')}")
    lines.append("")
    lines.append(f"- Run ID: `{data['run_id']}`")
    lines.append(f"- Generated: `{data['generated_at']}`")
    lines.append(f"- Tool: `{data['tool']} {data['tool_version']}`")
    lines.append(f"- Mode: `{data['mode']}`")
    lines.append(f"- Project: `{data['project'].get('root', '')}`")
    lines.append(f"- Engine: `{data['engine'].get('engine_version', 'unknown')}`")
    if data.get("baseline"):
        lines.append(f"- Baseline: `{data['baseline'].get('manifest_sha256', '')}`")
    lines.append("")

    summary = data["summary"]
    lines.append("## Summary")
    lines.append("")
    lines.append("| Severity | Count |")
    lines.append("|---|---:|")
    for severity in Severity:
        lines.append(f"| {severity.value} | {summary['severity'][severity.value]} |")
    lines.append("")
    lines.append("| Check | Status | Summary |")
    lines.append("|---|---|---|")
    for check in data["checks"]:
        lines.append(
            f"| `{check['check_id']}` {_cell(check['title'])} | {check['status']} | {_cell(check['summary'])} |"
        )
    lines.append("")

    lines.append("## Findings")
    lines.append("")
    if not data["findings"]:
        lines.append("No findings.")
    else:
        lines.append("| ID | Check | Severity | Title | Asset | Message |")
        lines.append("|---|---|---|---|---|---|")
        for finding in data["findings"]:
            lines.append(
                "| `{id}` | `{check_id}` | {severity} | {title} | {asset} | {message} |".format(
                    id=finding["id"],
                    check_id=finding["check_id"],
                    severity=finding["severity"],
                    title=_cell(finding["title"]),
                    asset=f"`{_cell(finding['asset'])}`" if finding["asset"] else "",
                    message=_cell(finding["message"]),
                )
            )
    lines.append("")

    lines.append("## Read-only evidence")
    lines.append("")
    proof = data["readonly_proof"]
    lines.append(f"- Content equal: `{proof.get('content_equal')}`")
    lines.append(f"- Metadata equal: `{proof.get('metadata_equal')}`")
    lines.append(f"- Unknown files: `{proof.get('unknown_count')}`")
    lines.append(f"- During-write monitor: `{proof.get('during_write_monitor', 'unknown')}`")
    lines.append("")
    lines.append(f"> {proof.get('statement', '')}")
    lines.append("")

    lines.append("## Limitations")
    lines.append("")
    for limitation in data["limitations"]:
        lines.append(f"- {limitation}")
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
