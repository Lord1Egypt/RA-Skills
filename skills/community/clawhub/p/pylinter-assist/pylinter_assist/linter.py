"""Orchestrate pylint + pattern checks across a set of files."""

from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pylinter_assist.checks.base import CheckResult, Severity
from pylinter_assist.checks.fastapi import FastAPIDocstringCheck
from pylinter_assist.checks.react import ReactUseEffectCheck
from pylinter_assist.checks.secrets import HardcodedSecretsCheck


@dataclass
class LintReport:
    files_checked: list[str] = field(default_factory=list)
    pylint_results: list[CheckResult] = field(default_factory=list)
    pattern_results: list[CheckResult] = field(default_factory=list)
    pylint_score: float | None = None
    errors: list[str] = field(default_factory=list)

    @property
    def all_results(self) -> list[CheckResult]:
        return self.pylint_results + self.pattern_results

    @property
    def by_severity(self) -> dict[Severity, list[CheckResult]]:
        buckets: dict[Severity, list[CheckResult]] = {s: [] for s in Severity}
        for r in self.all_results:
            buckets[r.severity].append(r)
        return buckets

    def has_errors(self) -> bool:
        return any(r.severity == Severity.ERROR for r in self.all_results)

    def has_warnings(self) -> bool:
        return any(r.severity == Severity.WARNING for r in self.all_results)


def _run_pylint(files: list[str], config: dict) -> tuple[list[CheckResult], float | None]:
    """Run pylint and parse its JSON output."""
    if not files:
        return [], None

    pylint_cfg = config.get("pylint", {})
    if not pylint_cfg.get("enabled", True):
        return [], None

    cmd = [sys.executable, "-m", "pylint", "--output-format=json"]

    max_line = pylint_cfg.get("max_line_length", 120)
    cmd += [f"--max-line-length={max_line}"]

    for msg_id in pylint_cfg.get("disable", []):
        cmd += [f"--disable={msg_id}"]
    for msg_id in pylint_cfg.get("enable", []):
        cmd += [f"--enable={msg_id}"]

    cmd += files

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        return [], None

    results: list[CheckResult] = []
    score: float | None = None

    try:
        messages = json.loads(proc.stdout) if proc.stdout.strip() else []
    except json.JSONDecodeError:
        messages = []

    sev_map = {
        "error": Severity.ERROR,
        "fatal": Severity.ERROR,
        "warning": Severity.WARNING,
        "refactor": Severity.WARNING,
        "convention": Severity.INFO,
        "info": Severity.INFO,
    }

    for msg in messages:
        sev = sev_map.get(msg.get("type", "info"), Severity.INFO)
        results.append(
            CheckResult(
                file=msg.get("path", ""),
                line=msg.get("line", 0),
                col=msg.get("column", 0) + 1,
                severity=sev,
                code=msg.get("message-id", ""),
                message=msg.get("message", ""),
                check_name="pylint",
                context=msg.get("obj", ""),
            )
        )

    # Extract score from stderr
    for line in proc.stderr.splitlines():
        if "Your code has been rated at" in line:
            try:
                score = float(line.split("rated at")[1].split("/")[0].strip())
            except (ValueError, IndexError):
                pass

    return results, score


class Linter:
    def __init__(self, config: dict):
        self.config = config
        self._pattern_checks = [
            HardcodedSecretsCheck(),
            FastAPIDocstringCheck(),
            ReactUseEffectCheck(),
        ]

    def lint_files(self, files: list[str]) -> LintReport:
        report = LintReport(files_checked=files)

        # Pylint (Python files only)
        py_files = [f for f in files if f.endswith(".py")]
        if py_files:
            report.pylint_results, report.pylint_score = _run_pylint(py_files, self.config)

        # Pattern checks (all files)
        for file_path in files:
            try:
                source = Path(file_path).read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                report.errors.append(f"Cannot read {file_path}: {exc}")
                continue

            for check in self._pattern_checks:
                try:
                    findings = check.check(file_path, source, self.config)
                    report.pattern_results.extend(findings)
                except Exception as exc:  # noqa: BLE001
                    report.errors.append(f"Check {check.name} failed on {file_path}: {exc}")

        return report

    def lint_diff(self, diff_text: str, base_dir: str = ".") -> LintReport:
        """Lint files referenced in a unified diff."""
        files = _files_from_diff(diff_text, base_dir)
        return self.lint_files(files)

    def lint_staged(self, base_dir: str = ".") -> LintReport:
        """Lint git-staged files."""
        try:
            proc = subprocess.run(
                ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                capture_output=True, text=True, cwd=base_dir,
            )
            files = [
                str(Path(base_dir) / f.strip())
                for f in proc.stdout.splitlines()
                if f.strip()
            ]
        except FileNotFoundError:
            files = []
        return self.lint_files(files)


def _files_from_diff(diff_text: str, base_dir: str) -> list[str]:
    """Extract modified file paths from a unified diff."""
    files: list[str] = []
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            rel = line[6:].strip()
            full = str(Path(base_dir) / rel)
            if full not in files:
                files.append(full)
    return files
