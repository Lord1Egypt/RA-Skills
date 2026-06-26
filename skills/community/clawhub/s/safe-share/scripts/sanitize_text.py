#!/usr/bin/env python3
"""Deterministically sanitize sensitive values in text for safe sharing."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Match
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


SENSITIVE_QUERY_KEYS = {
    "token",
    "key",
    "apikey",
    "api_key",
    "secret",
    "password",
    "signature",
    "session",
}

def mask_value(value: str) -> str:
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}{'*' * max(4, len(value) - 8)}{value[-4:]}"


def replacement(label: str, value: str, mode: str) -> str:
    if mode == "redact":
        return f"[REDACTED:{label}]"
    if mode == "mask":
        return mask_value(value)
    return f"<{label}>"


def luhn_valid(candidate: str) -> bool:
    digits = [int(char) for char in candidate if char.isdigit()]
    if len(digits) < 13 or len(digits) > 19:
        return False
    checksum = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    replacer: Callable[[Match[str], str], str]


def replace_query_params(text: str, mode: str) -> tuple[str, int]:
    url_pattern = re.compile(r"https?://[^\s)>\]}]+")
    count = 0

    def _replace_url(match: Match[str]) -> str:
        nonlocal count
        original = match.group(0)
        parts = urlsplit(original)
        if not parts.query:
            return original

        changed = False
        query_pairs = []
        for key, value in parse_qsl(parts.query, keep_blank_values=True):
            if key.lower() in SENSITIVE_QUERY_KEYS and value:
                count += 1
                changed = True
                query_pairs.append((key, replacement(f"QUERY_{key.upper()}", value, mode)))
            else:
                query_pairs.append((key, value))

        if not changed:
            return original
        new_query = urlencode(query_pairs, doseq=True, safe="<>[]:_")
        return urlunsplit((parts.scheme, parts.netloc, parts.path, new_query, parts.fragment))

    return url_pattern.sub(_replace_url, text), count


RULES = [
    Rule(
        "private_key_block",
        re.compile(
            r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----[\s\S]+?-----END [A-Z0-9 ]*PRIVATE KEY-----",
            re.MULTILINE,
        ),
        lambda match, mode: replacement("PRIVATE_KEY_BLOCK", match.group(0), mode),
    ),
    Rule(
        "bearer_token",
        re.compile(r"(?i)\bAuthorization:\s*Bearer\s+([A-Za-z0-9._~+/=-]{8,})"),
        lambda match, mode: f"Authorization: Bearer {replacement('BEARER_TOKEN', match.group(1), mode)}",
    ),
    Rule(
        "cookie_header",
        re.compile(r"(?im)^(Cookie|Set-Cookie):[^\r\n]+"),
        lambda match, mode: f"{match.group(1)}: {replacement('COOKIE', match.group(0), mode)}",
    ),
    Rule(
        "env_assignment",
        re.compile(
            r"(?im)\b([A-Z][A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD|PASSWD|SESSION|COOKIE)[A-Z0-9_]*)\s*=\s*([^\s#]+)"
        ),
        lambda match, mode: f"{match.group(1)}={replacement(match.group(1), match.group(2), mode)}",
    ),
    Rule(
        "quoted_assignment",
        re.compile(
            r"(?i)\b([a-z_][a-z0-9_]*(?:key|token|secret|password|passwd|session|cookie)[a-z0-9_]*)\b\s*([:=])\s*([\"']?)([^\"'\r\n]+)\3"
        ),
        lambda match, mode: (
            f"{match.group(1)}{match.group(2)}"
            f"{match.group(3)}{replacement(match.group(1).upper(), match.group(4), mode)}{match.group(3)}"
        ),
    ),
    Rule(
        "openai_api_key",
        re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
        lambda match, mode: replacement("OPENAI_API_KEY", match.group(0), mode),
    ),
    Rule(
        "github_token",
        re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}\b"),
        lambda match, mode: replacement("GITHUB_TOKEN", match.group(0), mode),
    ),
    Rule(
        "aws_access_key",
        re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
        lambda match, mode: replacement("AWS_ACCESS_KEY", match.group(0), mode),
    ),
    Rule(
        "email",
        re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
        lambda match, mode: replacement("EMAIL", match.group(0), mode),
    ),
    Rule(
        "ipv4",
        re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
        lambda match, mode: replacement("IPV4", match.group(0), mode),
    ),
    Rule(
        "ipv6",
        re.compile(r"\b(?:[0-9a-fA-F]{1,4}:){2,7}[0-9a-fA-F]{1,4}\b"),
        lambda match, mode: replacement("IPV6", match.group(0), mode),
    ),
    Rule(
        "phone_number",
        re.compile(r"(?<![\w.])(?:\+?\d[\d\s()-]{6,}\d)"),
        lambda match, mode: replacement("PHONE_NUMBER", match.group(0), mode),
    ),
]


def sanitize(text: str, mode: str) -> dict[str, object]:
    counts: Counter[str] = Counter()

    text, query_count = replace_query_params(text, mode)
    if query_count:
        counts["sensitive_query_param"] += query_count

    for rule in RULES:
        def _replacer(match: Match[str], rule: Rule = rule) -> str:
            counts[rule.name] += 1
            return rule.replacer(match, mode)

        text = rule.pattern.sub(_replacer, text)

    card_pattern = re.compile(r"\b(?:\d[ -]?){13,19}\b")

    def _replace_cards(match: Match[str]) -> str:
        value = match.group(0)
        digits = re.sub(r"\D", "", value)
        if not luhn_valid(digits):
            return value
        counts["payment_card"] += 1
        return replacement("PAYMENT_CARD", value, mode)

    text = card_pattern.sub(_replace_cards, text)

    review_notes = ["Sanitization reduces risk but may miss custom identifiers or context-specific secrets."]
    if any(key in counts for key in ("email", "phone_number", "ipv4", "ipv6")):
        review_notes.append("Review remaining personal details, names, and internal hostnames manually.")

    findings_summary = [{"type": name, "count": count} for name, count in sorted(counts.items())]
    return {
        "sanitized_text": text,
        "findings_summary": findings_summary,
        "review_notes": review_notes,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sanitize text for safe public sharing.")
    parser.add_argument("path", nargs="?", help="Optional path to a text file. Reads stdin when omitted.")
    parser.add_argument(
        "--mode",
        choices=("placeholder", "redact", "mask"),
        default="placeholder",
        help="Replacement mode.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )
    return parser.parse_args()


def read_input(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def main() -> int:
    args = parse_args()
    text = read_input(args.path)
    result = sanitize(text, args.mode)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
