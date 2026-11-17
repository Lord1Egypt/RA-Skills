"""UE log error and crash scan."""

from __future__ import annotations

import os
import re
import time
from pathlib import Path
from typing import Any

from .base import AuditContext, finish_check, make_finding, new_check
from ..report.model import Severity, Status


ERROR_PATTERNS: list[re.Pattern[str]] = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bFatal error\b",
        r"\bError:\s",
        r"LogWindows:\s*Error",
        r"LogOutputDevice:\s*Error",
        r"Assertion failed",
        r"Unhandled Exception",
        r"Access violation",
        r"Ensure condition failed",
        r"\[Error\]",
    )
]
WARNING_PATTERNS: list[re.Pattern[str]] = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bWarning:\s",
        r"LogScript:\s*Warning",
    )
]
# Known noisy categories. They are still counted, but warning-only lines do not
# become findings, because they are usually not actionable in a project audit.
NOISE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"LogHttp:",
        r"LogStreaming:",
        r"LogDerivedDataCache:",
        r"LogPakFile:",
    )
]
# Some bridge/plugin messages use "Error:" for status text. These are not
# project errors and should not become findings.
IGNORE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"GameThread tick worker\s+(已启动|已停止|started|stopped)",
        r"LogPython:\s*Error:\s*\[[^\]]*\]\s*GameThread tick worker",
    )
]
STACK_START_PATTERN = re.compile(
    r"=== Handled ensure: ===|Unhandled Exception|Access violation", re.IGNORECASE
)
TIMESTAMP_PATTERN = re.compile(r"^\[\d{4}\.\d{2}\.\d{2}-")
MAX_LOG_BYTES = 32 * 1024 * 1024


def _find_logs(project_root: Path, max_logs: int, since_hours: int) -> list[Path]:
    log_dir = project_root / "Saved" / "Logs"
    if not log_dir.is_dir():
        return []
    cutoff = time.time() - since_hours * 3600 if since_hours > 0 else None
    logs: list[Path] = []
    for path in log_dir.glob("*.log"):
        try:
            stat = path.stat()
        except OSError:
            continue
        if cutoff is not None and stat.st_mtime < cutoff:
            continue
        logs.append(path)
    logs.sort(key=lambda item: item.stat().st_mtime, reverse=True)
    return logs[: max(0, max_logs)]


def _is_noise(line: str) -> bool:
    return any(pattern.search(line) for pattern in NOISE_PATTERNS)


def _is_ignored(line: str) -> bool:
    return any(pattern.search(line) for pattern in IGNORE_PATTERNS)


def _is_related_stack_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith("[Callstack]"):
        return True
    if stripped.startswith("Stack:"):
        return True
    if re.match(r"^\s", line) and not TIMESTAMP_PATTERN.match(line):
        return True
    if "LogOutputDevice: Error:" in line and not STACK_START_PATTERN.search(line):
        return True
    return False


def check_logs(ctx: AuditContext):
    check = new_check("LOG001", "Log errors and crashes")
    logs = _find_logs(ctx.project.root, ctx.options.max_logs, ctx.options.log_since_hours)
    if not logs:
        check.status = Status.UNKNOWN
        check.summary = "No logs found under Saved/Logs."
        check.details = {
            "logs_scanned": 0,
            "reason": "no_logs",
            "log_dir": str(ctx.project.root / "Saved" / "Logs"),
        }
        check.add(
            make_finding(
                "LOG001",
                Severity.INFO,
                Status.UNKNOWN,
                "No UE logs available",
                "The audit could not evaluate runtime or editor errors because no logs were found.",
                evidence=[],
                recommendation="Run the editor or provide a log directory, then audit again.",
            )
        )
        return finish_check(check)

    error_count = 0
    warning_count = 0
    noise_warning_count = 0
    fatal_count = 0
    grouped_error_count = 0
    findings_added = 0
    log_details: list[dict[str, Any]] = []
    evidence_files: list[str] = []

    for log_path in logs:
        truncated = False
        try:
            size = log_path.stat().st_size
            if size > MAX_LOG_BYTES:
                with log_path.open("rb") as handle:
                    handle.seek(-MAX_LOG_BYTES, os.SEEK_END)
                    text = handle.read().decode("utf-8", "replace")
                truncated = True
            else:
                text = log_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            check.add(
                make_finding(
                    "LOG001",
                    Severity.WARNING,
                    Status.WARN,
                    "Cannot read log",
                    f"{log_path}: {exc}",
                    asset=str(log_path),
                )
            )
            continue
        lines = text.splitlines()
        log_error_count = 0
        log_warning_count = 0
        index = 0
        while index < len(lines):
            line = lines[index]
            number = index + 1
            index += 1
            if _is_ignored(line):
                continue
            if any(pattern.search(line) for pattern in ERROR_PATTERNS):
                log_error_count += 1
                error_count += 1
                if re.search(
                    r"\bFatal error\b|Unhandled Exception|Access violation",
                    line,
                    re.IGNORECASE,
                ):
                    fatal_count += 1
                if STACK_START_PATTERN.search(line):
                    related = 0
                    while index < len(lines) and _is_related_stack_line(lines[index]):
                        related_line = lines[index]
                        if any(pattern.search(related_line) for pattern in ERROR_PATTERNS):
                            log_error_count += 1
                            error_count += 1
                        related += 1
                        index += 1
                    grouped_error_count += 1
                    if findings_added < 50:
                        suffix = f" (+{related} related stack/context lines)" if related else ""
                        check.add(
                            make_finding(
                                "LOG001",
                                Severity.ERROR,
                                Status.FAIL,
                                "Log error group",
                                f"{log_path.name}:{number}: {line.strip()[:240]}{suffix}",
                                asset=str(log_path),
                                recommendation="Open the log around this line and fix the underlying error.",
                            )
                        )
                        findings_added += 1
                    continue
                if findings_added < 50:
                    check.add(
                        make_finding(
                            "LOG001",
                            Severity.ERROR,
                            Status.FAIL,
                            "Log error",
                            f"{log_path.name}:{number}: {line.strip()[:300]}",
                            asset=str(log_path),
                            recommendation="Open the log around this line and fix the underlying error.",
                        )
                    )
                    findings_added += 1
                continue
            if any(pattern.search(line) for pattern in WARNING_PATTERNS):
                log_warning_count += 1
                warning_count += 1
                if _is_noise(line):
                    noise_warning_count += 1
        log_details.append(
            {
                "path": str(log_path),
                "lines": len(lines),
                "errors": log_error_count,
                "warnings": log_warning_count,
                "truncated": truncated,
            }
        )
        evidence_files.append(str(log_path))

    if error_count > findings_added:
        check.add(
            make_finding(
                "LOG001",
                Severity.INFO,
                Status.PASS,
                "Additional log errors omitted",
                f"{error_count - findings_added} more error lines were not listed individually.",
            )
        )

    check.details = {
        "logs_scanned": len(logs),
        "error_count": error_count,
        "warning_count": warning_count,
        "noise_warning_count": noise_warning_count,
        "fatal_count": fatal_count,
        "grouped_error_count": grouped_error_count,
        "logs": log_details,
        "evidence_files": evidence_files,
    }
    check.summary = (
        f"logs={len(logs)}, errors={error_count}, warnings={warning_count}, "
        f"fatal={fatal_count}, grouped={grouped_error_count}"
    )
    return finish_check(check)
