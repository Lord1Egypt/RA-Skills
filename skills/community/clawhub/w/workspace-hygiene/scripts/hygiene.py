#!/usr/bin/env python3
"""Workspace hygiene audit for OpenClaw agent workspaces."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


CANONICAL_ROOT_FILES = {
    "AGENTS.md",
    "SOUL.md",
    "MEMORY.md",
    "USER.md",
    "IDENTITY.md",
    "HEARTBEAT.md",
    "TASKS.md",
    "TOOLS.md",
    "STRUCTURE.md",
}

OPTIONAL_ROOT_FILES = {
    "BUILDOUT.md",
    "MEMORY-REFERENCE.md",
    "BRAND-GUIDELINES.md",
    ".DS_Store",
    ".gitignore",
    ".gitattributes",
}

CANONICAL_ROOT_FOLDERS = {
    "docs",
    "memory",
    "scripts",
    "skills",
    "projects",
    "reference",
    "archive",
    "avatars",
    "campaigns",
    "output",
    "prompt-library",
    "research",
    ".git",
    ".clawhub",
    ".openclaw",
    ".vercel",
    ".pi",
    "assets",
    "config",
    "lead-entry-staging",
    "references",
    "tools",
}

MEMORY_TAGS = ("[DECISION]", "[FACT]", "[PROJECT]", "[RULE]", "[EVENT]", "[BLOCKER]")
TIMESTAMP_MEMORY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{4}\.md$")
DAILY_MEMORY_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")
TOPIC_MEMORY_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-[a-z0-9-]+\.md$")
WEEKLY_REVIEW_RE = re.compile(r"^weekly-review-(\d{4}-\d{2}-\d{2})\.md$")


@dataclass
class Issue:
    level: str
    message: str


@dataclass
class AuditResult:
    workspace: Path
    agent: str
    issues: List[Issue] = field(default_factory=list)
    fixes: List[str] = field(default_factory=list)
    report_path: Optional[Path] = None

    def add(self, level: str, message: str) -> None:
        self.issues.append(Issue(level=level, message=message))

    def counts(self) -> Dict[str, int]:
        counts = {"ERROR": 0, "WARN": 0, "INFO": 0}
        for issue in self.issues:
            counts[issue.level] += 1
        return counts

    def health_score(self) -> int:
        counts = self.counts()
        score = 100 - counts["ERROR"] * 10 - counts["WARN"] * 3 - counts["INFO"] * 1
        return max(score, 0)

    def grouped(self, level: str) -> List[Issue]:
        return [issue for issue in self.issues if issue.level == level]


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit an OpenClaw workspace and generate a hygiene report.")
    parser.add_argument("--workspace", required=True, help="Path to the workspace to audit.")
    parser.add_argument("--fix", action="store_true", help="Apply low-risk fixes.")
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Audit and report without applying fixes, even if --fix is also passed.",
    )
    return parser.parse_args(argv)


def detect_agent(workspace: Path) -> str:
    name = workspace.name.lower()
    if "workspace-claire" in name:
        return "claire"
    if "workspace-ari" in name:
        return "ari"
    if "workspace" == name or name.endswith("/workspace"):
        return "maggie"
    if "workspace" in name:
        suffix = name.split("workspace-", 1)
        if len(suffix) == 2 and suffix[1]:
            return suffix[1]
    return workspace.name


def list_root_entries(workspace: Path) -> Tuple[List[Path], List[Path]]:
    if not workspace.exists():
        return [], []
    files = []
    folders = []
    for entry in sorted(workspace.iterdir(), key=lambda path: path.name.lower()):
        if entry.is_dir() and not entry.is_symlink():
            folders.append(entry)
        elif entry.is_dir() and entry.is_symlink():
            folders.append(entry)
        else:
            files.append(entry)
    return files, folders


def audit_root_files(result: AuditResult) -> None:
    files, _ = list_root_entries(result.workspace)
    allowed = CANONICAL_ROOT_FILES | OPTIONAL_ROOT_FILES
    for entry in files:
        if entry.name not in allowed:
            result.add("ERROR", "Unexpected root file: {0}".format(entry.name))


def audit_root_folders(result: AuditResult) -> None:
    _, folders = list_root_entries(result.workspace)
    for entry in folders:
        if entry.name.startswith("."):
            result.add("WARN", "Unknown root folder: {0}".format(entry.name))
            continue
        if entry.name not in CANONICAL_ROOT_FOLDERS:
            result.add("WARN", "Unknown root folder: {0}".format(entry.name))

    docs_path = result.workspace / "docs"
    if result.agent in {"claire", "ari"}:
        if not docs_path.exists() and not docs_path.is_symlink():
            result.add("ERROR", "docs/ is missing for non-main workspace; expected a symlink")
        elif not docs_path.is_symlink():
            result.add("ERROR", "docs/ is not a symlink in non-main workspace")
        elif not docs_path.exists():
            result.add("ERROR", "docs/ symlink is broken in non-main workspace")
    elif docs_path.exists():
        if docs_path.is_symlink():
            result.add("INFO", "docs/ is symlinked in main workspace")
        else:
            result.add("INFO", "docs/ exists and is a regular directory")


def audit_projects(result: AuditResult) -> None:
    projects_dir = result.workspace / "projects"
    if not projects_dir.exists():
        result.add("WARN", "projects/ directory is missing")
        return
    if not projects_dir.is_dir():
        result.add("ERROR", "projects exists but is not a directory")
        return

    for project_dir in sorted((p for p in projects_dir.iterdir() if p.is_dir()), key=lambda path: path.name.lower()):
        readme_path = project_dir / "README.md"
        if not readme_path.exists():
            result.add("WARN", "Missing README.md in projects/{0}".format(project_dir.name))


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def append_memory_content(target_path: Path, source_path: Path) -> bool:
    source_text = load_text(source_path)
    if not source_text.strip():
        return False

    target_text = load_text(target_path)
    if source_text.strip() in target_text:
        return False

    if target_text and not target_text.endswith("\n"):
        target_text += "\n"

    if target_text.strip():
        merged = target_text.rstrip() + "\n\n" + source_text.strip() + "\n"
    else:
        merged = source_text.rstrip() + "\n"

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(merged, encoding="utf-8")
    return True


def collect_memory_files(memory_dir: Path) -> List[Path]:
    if not memory_dir.exists() or not memory_dir.is_dir():
        return []
    return sorted((path for path in memory_dir.iterdir() if path.is_file()), key=lambda path: path.name.lower())


def parse_memory_date(path: Path) -> Optional[dt.date]:
    name = path.name
    match = DAILY_MEMORY_RE.match(name)
    if match:
        return parse_date(match.group(1))
    match = TOPIC_MEMORY_RE.match(name)
    if match:
        return parse_date(match.group(1))
    match = WEEKLY_REVIEW_RE.match(name)
    if match:
        return parse_date(match.group(1))
    match = re.match(r"^(\d{4}-\d{2}-\d{2})-\d{4}\.md$", name)
    if match:
        return parse_date(match.group(1))
    return None


def parse_date(value: str) -> Optional[dt.date]:
    try:
        return dt.datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def business_days_missing(existing_dates: Iterable[dt.date], today: dt.date, days: int = 14) -> List[dt.date]:
    existing = set(existing_dates)
    missing = []
    for delta in range(days):
        current = today - dt.timedelta(days=delta)
        if current.weekday() >= 5:
            continue
        if current not in existing:
            missing.append(current)
    return sorted(missing)


def tagged_line_counts(paths: Iterable[Path]) -> Tuple[int, int]:
    tagged = 0
    untagged = 0
    for path in paths:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            if line.startswith("- ") or re.match(r"^\d+\.\s", line):
                content = line[2:].strip() if line.startswith("- ") else re.sub(r"^\d+\.\s*", "", line)
            else:
                content = line
            if content.startswith(MEMORY_TAGS):
                tagged += 1
            else:
                untagged += 1
    return tagged, untagged


def audit_memory(result: AuditResult, apply_fix: bool) -> None:
    memory_dir = result.workspace / "memory"
    if not memory_dir.exists():
        result.add("WARN", "memory/ directory is missing")
        return
    if not memory_dir.is_dir():
        result.add("ERROR", "memory exists but is not a directory")
        return

    memory_files = collect_memory_files(memory_dir)
    result.add("INFO", "Memory files scanned: {0}".format(len(memory_files)))

    daily_dates = []
    recent_files = []
    today = dt.date.today()

    for path in memory_files:
        daily_match = DAILY_MEMORY_RE.match(path.name)
        if TIMESTAMP_MEMORY_RE.match(path.name):
            result.add("ERROR", "Timestamp-format memory file: {0}".format(path.name))
            if apply_fix:
                date_prefix = path.name[:10]
                daily_path = memory_dir / "{0}.md".format(date_prefix)
                changed = append_memory_content(daily_path, path)
                if changed:
                    result.fixes.append(
                        "Merged contents from {0} into {1} (source retained for manual cleanup)".format(
                            path.name, daily_path.name
                        )
                    )
                else:
                    result.fixes.append(
                        "Checked {0}; no merge needed because content was empty or already present".format(path.name)
                    )

        if daily_match:
            parsed_daily = parse_date(daily_match.group(1))
            if parsed_daily:
                daily_dates.append(parsed_daily)

        parsed = parse_memory_date(path)
        if parsed:
            if (today - parsed).days <= 7:
                recent_files.append(path)

    memory_md = result.workspace / "MEMORY.md"
    if memory_md.exists():
        try:
            line_count = len(memory_md.read_text(encoding="utf-8").splitlines())
        except OSError:
            line_count = 0
        if line_count > 150:
            result.add("WARN", "MEMORY.md is {0} lines; recommended maximum is 150".format(line_count))
        else:
            result.add("INFO", "MEMORY.md line count: {0}".format(line_count))
    else:
        result.add("ERROR", "MEMORY.md is missing")

    missing_days = business_days_missing(daily_dates, today=today, days=14)
    if missing_days:
        formatted = ", ".join(day.isoformat() for day in missing_days)
        result.add("WARN", "Missing business-day memory logs in last 14 days: {0}".format(formatted))
    else:
        result.add("INFO", "No business-day gaps found in last 14 days")

    tagged, untagged = tagged_line_counts(recent_files)
    result.add(
        "INFO",
        "Recent memory tagging (last 7 days): tagged={0}, untagged={1}".format(tagged, untagged),
    )
    if untagged > tagged:
        result.add("WARN", "Recent memory entries are mostly untagged")
    elif untagged > 0:
        result.add("INFO", "Recent memory includes some untagged lines")


def audit_symlinks(result: AuditResult) -> None:
    docs_path = result.workspace / "docs"
    if result.agent not in {"claire", "ari"}:
        return
    if not docs_path.is_symlink():
        if not docs_path.exists():
            result.add("ERROR", "docs/ is missing; expected a symlink")
        return
    target = os.readlink(str(docs_path))
    resolved = docs_path.resolve(strict=False)
    if not resolved.exists():
        result.add("ERROR", "docs/ symlink is broken: {0}".format(target))
    else:
        result.add("INFO", "docs/ symlink target: {0}".format(target))


def recommended_actions(result: AuditResult) -> List[str]:
    priority = {"ERROR": 0, "WARN": 1, "INFO": 2}
    ranked = sorted(result.issues, key=lambda issue: (priority[issue.level], issue.message))
    actions = []
    for issue in ranked:
        if issue.level == "ERROR":
            actions.append(issue.message)
        elif issue.level == "WARN":
            actions.append(issue.message)
        if len(actions) == 5:
            break
    if result.fixes:
        actions.append("Review applied fixes for timestamped memory files and remove retained source files manually")
    if not actions:
        actions.append("No action needed")
    return actions


def render_report(result: AuditResult, report_date: dt.date) -> str:
    counts = result.counts()
    actions = recommended_actions(result)
    lines = [
        "# Workspace Hygiene Report — {0}".format(report_date.isoformat()),
        "Workspace: {0}".format(result.workspace),
        "Agent: {0}".format(result.agent),
        "",
        "## Summary",
        "- Errors: {0}".format(counts["ERROR"]),
        "- Warnings: {0}".format(counts["WARN"]),
        "- Info: {0}".format(counts["INFO"]),
        "- Health score: {0}/100".format(result.health_score()),
        "",
        "## Errors",
    ]

    errors = result.grouped("ERROR")
    if errors:
        lines.extend("- [ERROR] {0}".format(issue.message) for issue in errors)
    else:
        lines.append("- None")

    lines.extend(["", "## Warnings"])
    warnings = result.grouped("WARN")
    if warnings:
        lines.extend("- [WARN] {0}".format(issue.message) for issue in warnings)
    else:
        lines.append("- None")

    lines.extend(["", "## Info"])
    info_items = result.grouped("INFO")
    if info_items:
        lines.extend("- [INFO] {0}".format(issue.message) for issue in info_items)
    else:
        lines.append("- None")

    if result.fixes:
        lines.extend(["", "## Fixes Applied"])
        lines.extend("- [FIX] {0}".format(item) for item in result.fixes)

    lines.extend(["", "## Recommended Actions"])
    for index, action in enumerate(actions, start=1):
        lines.append("{0}. {1}".format(index, action))

    lines.append("")
    return "\n".join(lines)


def write_report(result: AuditResult, report_date: dt.date, report_only: bool) -> Path:
    report_dir = result.workspace / "projects" / "system"
    if not report_dir.exists() and not report_only:
        report_dir.mkdir(parents=True, exist_ok=True)
        result.fixes.append("Created report directory: projects/system")
    elif not report_dir.exists():
        report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / "hygiene-{0}.md".format(report_date.isoformat())
    report_path.write_text(render_report(result, report_date), encoding="utf-8")
    result.report_path = report_path
    return report_path


def print_summary(result: AuditResult) -> None:
    counts = result.counts()
    print("Workspace: {0}".format(result.workspace))
    print("Agent: {0}".format(result.agent))
    print(
        "Summary: errors={0} warnings={1} info={2} health={3}/100".format(
            counts["ERROR"], counts["WARN"], counts["INFO"], result.health_score()
        )
    )
    if result.report_path is not None:
        print("Report: {0}".format(result.report_path))
    if result.fixes:
        print("Fixes:")
        for item in result.fixes:
            print("- {0}".format(item))


def run_audit(workspace: Path, apply_fix: bool) -> AuditResult:
    result = AuditResult(workspace=workspace, agent=detect_agent(workspace))
    if not workspace.exists():
        result.add("ERROR", "Workspace does not exist")
        return result
    if not workspace.is_dir():
        result.add("ERROR", "Workspace path is not a directory")
        return result

    audit_root_files(result)
    audit_root_folders(result)
    audit_projects(result)
    audit_memory(result, apply_fix=apply_fix)
    audit_symlinks(result)
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    workspace = Path(args.workspace).expanduser().resolve()
    apply_fix = args.fix and not args.report_only
    report_date = dt.date.today()

    result = run_audit(workspace, apply_fix=apply_fix)
    try:
        write_report(result, report_date=report_date, report_only=args.report_only)
    except OSError as exc:
        result.add("ERROR", "Failed to write report: {0}".format(exc))

    print_summary(result)

    if result.report_path is None:
        return 1
    return 0 if not result.grouped("ERROR") else 1


if __name__ == "__main__":
    sys.exit(main())
