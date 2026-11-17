#!/usr/bin/env python3
"""Fail closed when a public contribution contains likely private material."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


MACOS_USERS_ROOT = "/" + "Users" + "/"
LINUX_HOME_ROOT = "/" + "home" + "/"


@dataclass(frozen=True)
class Finding:
    source: str
    line: int
    column: int
    category: str
    rule: str


Rule = tuple[str, str, re.Pattern[str]]


RULES: tuple[Rule, ...] = (
    (
        "secret",
        "private-key-block",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
    (
        "secret",
        "github-token",
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    ),
    (
        "secret",
        "openai-style-key",
        re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    ),
    (
        "secret",
        "anthropic-key",
        re.compile(r"\bsk-ant-[A-Za-z0-9_-]{16,}\b"),
    ),
    (
        "secret",
        "aws-access-key",
        re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ),
    (
        "secret",
        "google-api-key",
        re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    ),
    (
        "secret",
        "slack-token",
        re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{16,}\b"),
    ),
    (
        "secret",
        "live-payment-key",
        re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{16,}\b"),
    ),
    (
        "secret",
        "bearer-token",
        re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{12,}", re.IGNORECASE),
    ),
    (
        "secret",
        "jwt",
        re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    ),
    (
        "secret",
        "credential-assignment",
        re.compile(
            r"\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|"
            r"password|private[_-]?key)\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{8,}",
            re.IGNORECASE,
        ),
    ),
    (
        "secret",
        "sensitive-url-parameter",
        re.compile(
            r"[?&](?:access_token|auth_token|api_key|client_secret|code|password|"
            r"private_key|refresh_token|state|token)=[A-Za-z0-9._~%+/=-]{8,}",
            re.IGNORECASE,
        ),
    ),
    (
        "identity",
        "macos-user-path",
        re.compile(
            re.escape(MACOS_USERS_ROOT)
            + r"(?!USER(?:/|\b)|example(?:/|\b)|<user>(?:/|\b))[^/\s]+/"
        ),
    ),
    (
        "identity",
        "linux-user-path",
        re.compile(
            re.escape(LINUX_HOME_ROOT)
            + r"(?!user(?:/|\b)|example(?:/|\b)|<user>(?:/|\b))[^/\s]+/"
        ),
    ),
    (
        "identity",
        "windows-user-path",
        re.compile(r"\b[A-Z]:\\Users\\(?!USER(?:\\|\b)|example(?:\\|\b))[^\\\s]+\\", re.IGNORECASE),
    ),
    (
        "identity",
        "email-address",
        re.compile(r"\b[A-Z0-9._%+-]+@(?!example\.(?:com|invalid)\b)[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    ),
    (
        "network",
        "private-ipv4",
        re.compile(
            r"\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|"
            r"172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b"
        ),
    ),
    (
        "identifier",
        "messaging-id",
        re.compile(
            r"\b(?:account[_-]?id|chat[_-]?id|recipient[_-]?id|sender[_-]?id)"
            r"\s*[:=]\s*[\"']?\d{6,}",
            re.IGNORECASE,
        ),
    ),
    (
        "identifier",
        "discord-snowflake",
        re.compile(r"(?<!\d)\d{17,20}(?!\d)"),
    ),
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan candidate public text for secrets and private identifiers."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["-"],
        help="UTF-8 files to scan, or - for stdin (default).",
    )
    parser.add_argument(
        "--deny-term",
        action="append",
        default=[],
        help="Case-insensitive private term to reject; repeat as needed.",
    )
    parser.add_argument(
        "--deny-file",
        action="append",
        default=[],
        help="UTF-8 file with one private term per line.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON findings.")
    return parser.parse_args(argv)


def load_deny_terms(args: argparse.Namespace) -> list[str]:
    terms = [term.strip() for term in args.deny_term if term.strip()]
    for filename in args.deny_file:
        for raw in Path(filename).read_text(encoding="utf-8").splitlines():
            term = raw.strip()
            if term and not term.startswith("#"):
                terms.append(term)
    unique: dict[str, str] = {}
    for term in terms:
        unique.setdefault(term.casefold(), term)
    return list(unique.values())


def iter_sources(paths: Iterable[str]):
    stdin_used = False
    for filename in paths:
        if filename == "-":
            if stdin_used:
                continue
            stdin_used = True
            yield "<stdin>", sys.stdin.read()
        else:
            path = Path(filename)
            yield str(path), path.read_text(encoding="utf-8")


def scan(source: str, text: str, deny_terms: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    custom = [
        (f"custom-deny-term-{index + 1}", re.compile(re.escape(term), re.IGNORECASE))
        for index, term in enumerate(deny_terms)
    ]
    for line_number, line in enumerate(text.splitlines(), start=1):
        for category, rule, pattern in RULES:
            for match in pattern.finditer(line):
                findings.append(
                    Finding(source, line_number, match.start() + 1, category, rule)
                )
        for rule, pattern in custom:
            for match in pattern.finditer(line):
                findings.append(
                    Finding(source, line_number, match.start() + 1, "private-term", rule)
                )
    return findings


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        deny_terms = load_deny_terms(args)
        findings = [
            finding
            for source, text in iter_sources(args.paths)
            for finding in scan(source, text, deny_terms)
        ]
    except (OSError, UnicodeError) as exc:
        print(f"preflight error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([asdict(finding) for finding in findings], indent=2))
    elif findings:
        for finding in findings:
            print(
                f"{finding.source}:{finding.line}:{finding.column}: "
                f"[{finding.category}] {finding.rule}"
            )
    else:
        print("Public contribution preflight: PASS")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
