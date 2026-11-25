#!/usr/bin/env python3
"""Build an Obsidian-friendly career knowledge vault from evidence JSON."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


PRIVATE_DISCLOSURE_LEVELS = {
    "confidential",
    "internal-summary-only",
    "unknown",
}

APPROVAL_RESUME_USES = {
    "include-sanitized",
    "needs-confirmation",
    "exclude",
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "untitled"


def yaml_list(values: list[str]) -> str:
    return "[" + ", ".join(values) + "]"


def escape_cell(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ").strip()


def normalize_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return []


def load_records(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        return data["records"]
    if isinstance(data, dict) and isinstance(data.get("evidence"), list):
        return data["evidence"]
    raise ValueError("Expected a JSON list or an object with a records/evidence list.")


def group_records_by_project(records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        project = str(record.get("project") or record.get("project_name") or "").strip()
        grouped[project or "Uncategorized Evidence"].append(record)
    return dict(grouped)


def collect_technologies(records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        for technology in normalize_list(record.get("technologies")):
            grouped[technology].append(record)
    return dict(grouped)


def project_link(project_name: str) -> str:
    return f"[[projects/{slugify(project_name)}|{project_name}]]"


def technology_link(technology_name: str) -> str:
    return f"[[technologies/{slugify(technology_name)}|{technology_name}]]"


def render_agents_md() -> str:
    return """# Career Knowledge Vault Instructions

This vault is a derived knowledge layer for Resume Intelligence. Raw sources remain the source of truth and must not be modified here.

## Rules

- Read `index.md` first before answering vault questions.
- Preserve YAML frontmatter, summaries, tags, and Obsidian `[[links]]`.
- Keep every career claim tied to an evidence link or source context.
- Do not add unsupported resume claims.
- Treat private source contexts as approval-required unless the disclosure page says otherwise.
- Update `log.md` whenever pages are generated, linted, or substantially changed.

## Maintenance Workflow

1. Ingest evidence from approved `evidence.json`, `evidence.md`, `detailed-resume.md`, or `run-summary.md`.
2. Update project, technology, metric, interview-story, job-target, and disclosure pages.
3. Update `index.md` and append `log.md`.
4. Run `vault_lint.py` and fix orphan pages, missing evidence links, stale summaries, and disclosure risks.
"""


def render_project_page(project: str, records: list[dict[str, Any]], run_name: str) -> str:
    technologies = sorted(
        {technology for record in records for technology in normalize_list(record.get("technologies"))}
    )
    disclosure_levels = sorted({str(record.get("disclosure_level") or "unknown") for record in records})
    confidence_levels = sorted({str(record.get("confidence") or "unknown") for record in records})
    tech_links = ", ".join(technology_link(technology) for technology in technologies) or "None recorded"

    lines = [
        "---",
        "tags: [project, resume-intelligence]",
        f"project: {project}",
        f"run: {run_name}",
        f"disclosure_levels: {yaml_list(disclosure_levels)}",
        f"confidence_levels: {yaml_list(confidence_levels)}",
        "---",
        "",
        f"# {project}",
        "",
        f"**Summary**: Evidence-backed career project page for {project}.",
        "",
        "## Technologies",
        "",
        tech_links,
        "",
        "## Claims",
        "",
        "| Claim | Confidence | Disclosure | Resume Use |",
        "| --- | --- | --- | --- |",
    ]
    for record in records:
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_cell(record.get("claim")),
                    escape_cell(record.get("confidence")),
                    escape_cell(record.get("disclosure_level")),
                    escape_cell(record.get("resume_use")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Evidence Links",
            "",
            "| Source Context | Evidence Reference | Resume Use |",
            "| --- | --- | --- |",
        ]
    )
    for record in records:
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_cell(record.get("source_context_id")),
                    escape_cell(record.get("evidence_reference")),
                    escape_cell(record.get("resume_use")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Interview Notes",
            "",
            "- 30-second pitch:",
            "- Architecture/tradeoff angle:",
            "- Metrics to confirm:",
            "- Sensitive details to anonymize:",
        ]
    )
    return "\n".join(lines) + "\n"


def render_technology_page(technology: str, records: list[dict[str, Any]]) -> str:
    projects = sorted(
        {
            str(record.get("project") or record.get("project_name") or "Uncategorized Evidence")
            for record in records
        }
    )
    lines = [
        "---",
        "tags: [technology, resume-intelligence]",
        f"technology: {technology}",
        "---",
        "",
        f"# {technology}",
        "",
        f"**Summary**: Career evidence and interview preparation notes for {technology}.",
        "",
        "## Related Projects",
        "",
    ]
    for project in projects:
        lines.append(f"- {project_link(project)}")
    lines.extend(
        [
            "",
            "## Evidence Links",
            "",
            "| Project | Source Context | Evidence Reference | Confidence |",
            "| --- | --- | --- | --- |",
        ]
    )
    for record in records:
        project = str(record.get("project") or record.get("project_name") or "Uncategorized Evidence")
        lines.append(
            "| "
            + " | ".join(
                [
                    project_link(project),
                    escape_cell(record.get("source_context_id")),
                    escape_cell(record.get("evidence_reference")),
                    escape_cell(record.get("confidence")),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def needs_disclosure_approval(record: dict[str, Any]) -> bool:
    disclosure = str(record.get("disclosure_level") or "unknown").lower()
    resume_use = str(record.get("resume_use") or "").lower()
    confidence = str(record.get("confidence") or "").lower()
    return (
        disclosure in PRIVATE_DISCLOSURE_LEVELS
        or resume_use in APPROVAL_RESUME_USES
        or confidence == "low"
    )


def render_disclosure_page(records: list[dict[str, Any]]) -> str:
    lines = [
        "---",
        "tags: [disclosure, resume-intelligence]",
        "---",
        "",
        "# Disclosure Approval Needed",
        "",
        "| Project | Claim | Source Context | Disclosure | Resume Use | Proposed Treatment |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for record in records:
        project = str(record.get("project") or record.get("project_name") or "Uncategorized Evidence")
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_cell(project),
                    escape_cell(record.get("claim")),
                    escape_cell(record.get("source_context_id")),
                    escape_cell(record.get("disclosure_level")),
                    escape_cell(record.get("resume_use")),
                    "Ask or sanitize before final public use",
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def render_index(
    project_names: list[str],
    technology_names: list[str],
    run_name: str,
    run_date: str,
) -> str:
    lines = [
        "# Career Knowledge Vault Index",
        "",
        f"**Summary**: Obsidian-friendly career knowledge base for {run_name}.",
        f"**Last Updated**: {run_date}",
        "",
        "## Projects",
        "",
    ]
    for project in sorted(project_names):
        lines.append(f"- {project_link(project)}")
    lines.extend(["", "## Technologies", ""])
    for technology in sorted(technology_names):
        lines.append(f"- {technology_link(technology)}")
    lines.extend(
        [
            "",
            "## Disclosure",
            "",
            "- [[disclosure/approval-needed|Disclosure Approval Needed]]",
            "",
            "## Operations",
            "",
            "- Read `AGENTS.md` for vault maintenance rules.",
            "- Review `log.md` for ingest and lint history.",
        ]
    )
    return "\n".join(lines) + "\n"


def append_log(vault: Path, run_name: str, run_date: str, record_count: int) -> None:
    log_path = vault / "log.md"
    if not log_path.exists():
        log_path.write_text("# Career Knowledge Vault Log\n\n", encoding="utf-8")
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(
            f"## [{run_date}] ingest | {run_name}\n\n"
            f"- Records processed: {record_count}\n"
            "- Updated index, project pages, technology pages, and disclosure queue.\n\n"
        )


def build_vault(
    *,
    evidence_path: Path,
    output_dir: Path,
    run_name: str,
    run_date: str,
) -> Path:
    records = load_records(evidence_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    for directory in ["projects", "technologies", "metrics", "interview-stories", "job-targets", "disclosure", "raw-sources"]:
        (output_dir / directory).mkdir(exist_ok=True)

    grouped_projects = group_records_by_project(records)
    grouped_technologies = collect_technologies(records)

    (output_dir / "AGENTS.md").write_text(render_agents_md(), encoding="utf-8")
    for project, project_records in grouped_projects.items():
        (output_dir / "projects" / f"{slugify(project)}.md").write_text(
            render_project_page(project, project_records, run_name),
            encoding="utf-8",
        )
    for technology, technology_records in grouped_technologies.items():
        (output_dir / "technologies" / f"{slugify(technology)}.md").write_text(
            render_technology_page(technology, technology_records),
            encoding="utf-8",
        )

    approval_records = [record for record in records if needs_disclosure_approval(record)]
    (output_dir / "disclosure" / "approval-needed.md").write_text(
        render_disclosure_page(approval_records),
        encoding="utf-8",
    )
    (output_dir / "index.md").write_text(
        render_index(
            project_names=list(grouped_projects),
            technology_names=list(grouped_technologies),
            run_name=run_name,
            run_date=run_date,
        ),
        encoding="utf-8",
    )
    append_log(output_dir, run_name, run_date, len(records))
    return output_dir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence_json", help="Structured evidence JSON input.")
    parser.add_argument("--output-dir", default="career-vault", help="Vault output directory.")
    parser.add_argument("--run-name", default="Resume Intelligence", help="Run or target-role name.")
    parser.add_argument("--run-date", required=True, help="Run date in YYYY-MM-DD format.")
    args = parser.parse_args()

    vault = build_vault(
        evidence_path=Path(args.evidence_json),
        output_dir=Path(args.output_dir),
        run_name=args.run_name,
        run_date=args.run_date,
    )
    print(vault)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
