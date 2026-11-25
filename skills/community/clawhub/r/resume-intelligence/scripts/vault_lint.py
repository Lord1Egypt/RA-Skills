#!/usr/bin/env python3
"""Lint a Career Knowledge Vault for structure and provenance gaps."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


CONTENT_DIRS = ["projects", "technologies", "metrics", "interview-stories", "job-targets"]


@dataclass(frozen=True)
class VaultIssue:
    severity: str
    path: str
    message: str


@dataclass(frozen=True)
class VaultLintReport:
    ok: bool
    issues: list[VaultIssue]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def title_for_page(path: Path, text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ").title()


def index_contains_page(index_text: str, vault: Path, page: Path, text: str) -> bool:
    relative = page.relative_to(vault).with_suffix("").as_posix()
    title = title_for_page(page, text)
    return f"[[{relative}|{title}]]" in index_text or f"[[{relative}]]" in index_text


def lint_vault(vault: Path) -> VaultLintReport:
    issues: list[VaultIssue] = []
    index_path = vault / "index.md"
    index_text = read_text(index_path)

    if not index_path.exists():
        issues.append(VaultIssue("error", "index.md", "Vault is missing index.md."))
    if not (vault / "AGENTS.md").exists():
        issues.append(VaultIssue("warning", "AGENTS.md", "Vault is missing AGENTS.md schema instructions."))
    if not (vault / "log.md").exists():
        issues.append(VaultIssue("warning", "log.md", "Vault is missing log.md operation history."))

    for directory_name in CONTENT_DIRS:
        directory = vault / directory_name
        if not directory.exists():
            continue
        for page in sorted(directory.glob("*.md")):
            text = read_text(page)
            relative = page.relative_to(vault).as_posix()
            if index_text and not index_contains_page(index_text, vault, page, text):
                issues.append(
                    VaultIssue(
                        "warning",
                        relative,
                        f"{relative} is not linked from index.md.",
                    )
                )
            if directory_name in {"projects", "technologies"} and "## Evidence Links" not in text:
                issues.append(
                    VaultIssue(
                        "error",
                        relative,
                        f"{relative} is missing an Evidence Links section.",
                    )
                )
            if directory_name != "disclosure" and "private url" in text.lower():
                issues.append(
                    VaultIssue(
                        "error",
                        relative,
                        f"{relative} appears to contain a private URL reference.",
                    )
                )

    return VaultLintReport(
        ok=not any(issue.severity == "error" for issue in issues),
        issues=issues,
    )


def render_report(report: VaultLintReport) -> str:
    lines = ["# Career Knowledge Vault Lint", ""]
    if report.ok:
        lines.append("Status: ok")
    else:
        lines.append("Status: issues found")
    lines.extend(["", "| Severity | Path | Message |", "| --- | --- | --- |"])
    for issue in report.issues:
        lines.append(f"| {issue.severity} | {issue.path} | {issue.message} |")
    if not report.issues:
        lines.append("| info | vault | No issues found. |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault", help="Path to career-vault directory.")
    args = parser.parse_args()

    report = lint_vault(Path(args.vault))
    print(render_report(report), end="")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
