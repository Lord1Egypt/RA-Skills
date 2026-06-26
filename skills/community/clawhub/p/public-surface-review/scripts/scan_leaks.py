#!/usr/bin/env python3
"""Scan a repo for common public-release leak patterns."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
TEXT_EXTENSIONS = {
    ".cer",
    ".env",
    ".ini",
    ".js",
    ".json",
    ".key",
    ".md",
    ".mjs",
    ".pem",
    ".p8",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".txt",
    ".yaml",
    ".yml",
}
TRACKED_TEXT_FILENAMES = {
    ".dockerignore",
    ".editorconfig",
    ".gitignore",
    ".npmignore",
    "dockerfile",
    "gemfile",
    "license",
    "procfile",
    "readme",
}
IGNORE_DIRS = {".git", "__pycache__", "dist", "build", "node_modules", ".venv", "venv"}
MAX_BYTES = 512_000
USER_HOME_PATTERN = r"/User" + r"s/[^/\s]+/"
LINUX_HOME_PATTERN = r"/ho" + r"me/[^/\s]+/"
WINDOWS_USER_PATTERN = r"[A-Za-z]:\\User" + r"s\\[^\\\s]+\\"
PATH_SNIPPET_PATTERN = r"(?:/User" + r"s/[^\s\"']+|/ho" + r"me/[^\s\"']+|[A-Za-z]:\\User" + r"s\\[^\s\"']+)"
PATTERNS = [
    ("absolute-path", "error", re.compile(rf"({USER_HOME_PATTERN}|{LINUX_HOME_PATTERN}|{WINDOWS_USER_PATTERN})")),
    ("websocket-endpoint", "error", re.compile(r"\bws://|\bwss://")),
    ("localhost-url", "warning", re.compile(r"(https?://(?:localhost|127\.0\.0\.1)\b|\b(?:localhost|127\.0\.0\.1):\d+)")),
    ("github-token", "error", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]+\b|\bgithub_pat_[A-Za-z0-9_]+\b")),
    ("openai-key", "error", re.compile(r"\bsk-(?:proj-[A-Za-z0-9][A-Za-z0-9_-]{12,}|[A-Za-z0-9]{12,})\b")),
    ("aws-access-key-id", "error", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("slack-token", "error", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]+\b")),
    ("private-key-block", "error", re.compile(r"-----BEGIN (?:[A-Z0-9 ]+)?PRIVATE KEY-----")),
    (
        "secret-env-var",
        "warning",
        re.compile(
            r"(?:(?:export\s+)?(OPENAI_API_KEY|ANTHROPIC_API_KEY|AZURE_OPENAI_API_KEY|GOOGLE_API_KEY|CEREBRAS_API_KEY)\s*[:=]\s*[\"']?[A-Za-z0-9._-]{6,})"
        ),
    ),
    (
        "aws-secret-access-key",
        "error",
        re.compile(r"(?:(?:export\s+)?AWS_SECRET_ACCESS_KEY\s*[:=]\s*[\"']?[A-Za-z0-9/+=]{20,})"),
    ),
    ("credential-url", "error", re.compile(r"https?://[^/\s:@]+:[^/\s:@]+@")),
]
SNIPPET_REDACTIONS = (
    (re.compile(PATH_SNIPPET_PATTERN), "<redacted-path>"),
    (re.compile(r"\bws://|\bwss://"), "<redacted-websocket>"),
    (re.compile(r"(https?://(?:localhost|127\.0\.0\.1)\b|\b(?:localhost|127\.0\.0\.1):\d+)"), "<redacted-local-url>"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9_]+\b|\bgithub_pat_[A-Za-z0-9_]+\b"), "<redacted-github-token>"),
    (re.compile(r"\bsk-(?:proj-[A-Za-z0-9][A-Za-z0-9_-]{12,}|[A-Za-z0-9]{12,})\b"), "<redacted-openai-key>"),
    (re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"), "<redacted-aws-access-key-id>"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]+\b"), "<redacted-slack-token>"),
    (re.compile(r"-----BEGIN (?:[A-Z0-9 ]+)?PRIVATE KEY-----"), "<redacted-private-key-block>"),
    (re.compile(r"(?:(?:export\s+)?AWS_SECRET_ACCESS_KEY\s*[:=]\s*[\"']?)[A-Za-z0-9/+=]{20,}"), "AWS_SECRET_ACCESS_KEY=<redacted>"),
    (re.compile(r"https?://[^/\s:@]+:[^/\s:@]+@"), "<redacted-credential-url>"),
)
SECRET_ENV_VALUE = re.compile(
    r"(?P<name>(?:OPENAI_API_KEY|ANTHROPIC_API_KEY|AZURE_OPENAI_API_KEY|GOOGLE_API_KEY|CEREBRAS_API_KEY|AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY))(?P<sep>\s*[:=]\s*[\"']?)(?P<value>[A-Za-z0-9._/+=-]{6,})"
)


def is_scannable_text_file(path: Path) -> bool:
    lower_name = path.name.lower()
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    if lower_name in TRACKED_TEXT_FILENAMES:
        return True
    return lower_name == ".env" or lower_name.startswith(".env.")


def under_size_limit(path: Path) -> bool:
    try:
        return path.stat().st_size <= MAX_BYTES
    except OSError:
        return False


def display_input_label(raw_arg: str, resolved: Path) -> str:
    raw_path = Path(raw_arg).expanduser()
    if not raw_path.is_absolute():
        return raw_path.as_posix() or "."
    return resolved.name or "."
def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORE_DIRS or part.startswith(".venv") for part in path.relative_to(root).parts[:-1]):
            continue
        if not is_scannable_text_file(path):
            continue
        if not under_size_limit(path):
            continue
        files.append(path)
    return sorted(files)


def sanitize_snippet(line: str) -> str:
    snippet = line.strip()[:220]
    for pattern, replacement in SNIPPET_REDACTIONS:
        snippet = pattern.sub(replacement, snippet)
    snippet = SECRET_ENV_VALUE.sub(r"\g<name>\g<sep><redacted>", snippet)
    return snippet


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Repo root to scan.")
    parser.add_argument("--out", required=True, help="Output JSON file.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    findings: list[dict[str, object]] = []

    for path in iter_files(root):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for line_number, line in enumerate(lines, start=1):
            for code, severity, pattern in PATTERNS:
                if pattern.search(line):
                    findings.append(
                        {
                            "code": code,
                            "severity": severity,
                            "file": str(path.relative_to(root)),
                            "line": line_number,
                            "snippet": sanitize_snippet(line),
                        }
                    )

    payload = {
        "root": display_input_label(args.root, root),
        "finding_count": len(findings),
        "error_count": sum(1 for item in findings if item["severity"] == "error"),
        "warning_count": sum(1 for item in findings if item["severity"] == "warning"),
        "findings": findings,
    }
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
