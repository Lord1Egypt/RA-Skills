#!/usr/bin/env python3
"""Check whether a local Resume Intelligence checkout has expected files and tools."""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


REQUIRED_PATHS = {
    "readme": "README.md",
    "codex marketplace": ".agents/plugins/marketplace.json",
    "claude marketplace": ".claude-plugin/marketplace.json",
    "codex plugin manifest": "plugins/resume-intelligence/.codex-plugin/plugin.json",
    "claude plugin manifest": "plugins/resume-intelligence/.claude-plugin/plugin.json",
    "cursor plugin manifest": "plugins/resume-intelligence/.cursor-plugin/plugin.json",
    "skill file": "plugins/resume-intelligence/skills/resume-intelligence/SKILL.md",
    "templates directory": "plugins/resume-intelligence/skills/resume-intelligence/assets/templates",
    "vault templates directory": "plugins/resume-intelligence/skills/resume-intelligence/assets/vault-templates",
    "references directory": "plugins/resume-intelligence/skills/resume-intelligence/references",
    "scripts directory": "plugins/resume-intelligence/skills/resume-intelligence/scripts",
}

RECOMMENDED_COMMANDS = [
    "git",
    "python3",
    "rg",
    "gh",
    "codex",
    "claude",
    "cursor",
    "npx",
    "soffice",
]


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    detail: str


def check_required_paths(repo_root: Path) -> list[CheckResult]:
    """Return required repository path checks."""

    results: list[CheckResult] = []
    for name, relative_path in REQUIRED_PATHS.items():
        path = repo_root / relative_path
        if path.exists():
            results.append(CheckResult(name=name, status="ok", detail=relative_path))
        else:
            results.append(CheckResult(name=name, status="missing", detail=relative_path))
    return results


def check_commands(
    command_names: Iterable[str] = RECOMMENDED_COMMANDS,
    *,
    which: Callable[[str], str | None] = shutil.which,
) -> list[CheckResult]:
    """Return checks for optional local commands."""

    results: list[CheckResult] = []
    for command in command_names:
        resolved = which(command)
        if resolved:
            results.append(CheckResult(name=command, status="ok", detail=resolved))
        else:
            results.append(CheckResult(name=command, status="missing", detail="not found on PATH"))
    return results


def render_markdown(path_results: list[CheckResult], command_results: list[CheckResult]) -> str:
    lines = [
        "# Resume Intelligence Setup Doctor",
        "",
        "## Required Files",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for result in path_results:
        lines.append(f"| {result.name} | {result.status} | {result.detail} |")

    lines.extend(
        [
            "",
            "## Recommended Commands",
            "",
            "| Command | Status | Detail |",
            "| --- | --- | --- |",
        ]
    )
    for result in command_results:
        lines.append(f"| {result.name} | {result.status} | {result.detail} |")

    missing_required = [result.name for result in path_results if result.status != "ok"]
    missing_optional = [result.name for result in command_results if result.status != "ok"]
    lines.extend(["", "## Summary", ""])
    if missing_required:
        lines.append(f"- Missing required files: {', '.join(missing_required)}")
    else:
        lines.append("- Required files: ok")
    if missing_optional:
        lines.append(f"- Missing optional commands: {', '.join(missing_optional)}")
    else:
        lines.append("- Recommended commands: ok")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "repo_root",
        nargs="?",
        default=".",
        help="Path to the resume-builder repository root.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    path_results = check_required_paths(repo_root)
    command_results = check_commands()
    print(render_markdown(path_results, command_results), end="")
    return 1 if any(result.status != "ok" for result in path_results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
