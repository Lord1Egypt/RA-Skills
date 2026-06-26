"""Report generation for evaluation results."""

from __future__ import annotations

import json

from .scoring import EvalResult


def generate_markdown_report(result: EvalResult) -> str:
    """Generate a markdown evaluation report."""
    lines: list[str] = []

    lines.append("# Evaluation Report")
    lines.append("")

    # Summary table
    lines.append("## Summary")
    lines.append("")

    # Header
    dims = list(result.dimension_averages().keys())
    header = "| Case |"
    separator = "|------|"
    for dim in dims:
        short = dim.replace("_", " ").title()
        header += f" {short} |"
        separator += "------|"
    header += " Total |"
    separator += "------|"

    lines.append(header)
    lines.append(separator)

    for case in result.cases:
        row = f"| {case.case_name} |"
        for dim in dims:
            score = next((s for s in case.scores if s.dimension == dim), None)
            if score:
                row += f" {score.percentage}% |"
            else:
                row += " N/A |"
        row += f" **{case.total_percentage}%** |"
        lines.append(row)

    # Averages row
    avgs = result.dimension_averages()
    avg_row = "| **Average** |"
    for dim in dims:
        avg_row += f" **{avgs[dim]}%** |"
    avg_row += f" **{result.aggregate_score}%** |"
    lines.append(avg_row)
    lines.append("")

    # Per-case details
    lines.append("## Details")
    lines.append("")

    for case in result.cases:
        lines.append(f"### {case.case_name}")
        lines.append("")
        for score in case.scores:
            emoji = "✅" if score.percentage >= 80 else "⚠️" if score.percentage >= 60 else "❌"
            lines.append(f"**{score.dimension}**: {score.score}/{score.max_score} ({score.percentage}%) {emoji}")
            if score.details:
                lines.append("```")
                lines.append(score.details)
                lines.append("```")
            lines.append("")

    return "\n".join(lines)


def generate_json_report(result: EvalResult) -> str:
    """Generate a JSON evaluation report."""
    return json.dumps(result.to_dict(), indent=2, ensure_ascii=False)
