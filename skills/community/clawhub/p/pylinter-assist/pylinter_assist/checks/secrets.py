"""Check for hardcoded secrets, URLs, and IP addresses."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from pylinter_assist.checks.base import CheckResult, Severity

# Patterns that strongly suggest hardcoded credentials
_SECRET_PATTERNS: list[tuple[str, str, re.Pattern]] = [
    (
        "HCS001",
        "Possible hardcoded password/secret",
        re.compile(
            r'(?:password|passwd|pwd|secret|api[_-]?key|auth[_-]?token|access[_-]?token'
            r'|private[_-]?key|client[_-]?secret)\s*=\s*["\'][^"\']{4,}["\']',
            re.IGNORECASE,
        ),
    ),
    (
        "HCS002",
        "Hardcoded URL with credentials",
        re.compile(r'https?://[^@\s]+:[^@\s]+@', re.IGNORECASE),
    ),
    (
        "HCS003",
        "Possible hardcoded IP address (should be in .env)",
        re.compile(
            r'(?<![.\d])(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}'
            r'(?:25[0-5]|2[0-4]\d|[01]?\d\d?)(?![.\d])',
        ),
    ),
    (
        "HCS004",
        "Hardcoded localhost URL (use config/env variable)",
        re.compile(r'["\']https?://localhost(?::\d+)?[^"\']*["\']', re.IGNORECASE),
    ),
    (
        "HCS005",
        "Possible AWS/GCP/Azure access key",
        re.compile(r'(?:AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}'),
    ),
]

# Lines/contexts that are false-positive-prone — skip them
_SAFE_PATTERNS = re.compile(
    r'(?:#.*|os\.environ|getenv|settings\.|config\.|\.env|example|placeholder'
    r'|your[_-]?(?:key|secret|token)|<[A-Z_]+>|\$\{[A-Z_]+\})',
    re.IGNORECASE,
)

# IP patterns that are clearly non-sensitive
_SAFE_IPS = re.compile(
    r'^(?:127\.0\.0\.1|0\.0\.0\.0|255\.255\.255\.255|192\.168\.|10\.|172\.(?:1[6-9]|2\d|3[01])\.)'
)


@dataclass
class HardcodedSecretsCheck:
    name: str = "hardcoded-secrets"
    enabled: bool = True

    def check(self, file_path: str, source: str, config: dict) -> list[CheckResult]:
        if not self.enabled:
            return []

        cfg = config.get("hardcoded_secrets", {})
        if cfg.get("enabled") is False:
            return []

        skip_ip_check = cfg.get("skip_ip_check", False)
        results: list[CheckResult] = []
        lines = source.splitlines()

        for lineno, line in enumerate(lines, start=1):
            # Skip commented lines and obvious safe patterns
            stripped = line.strip()
            if stripped.startswith("#") or _SAFE_PATTERNS.search(line):
                continue

            for code, message, pattern in _SECRET_PATTERNS:
                if code == "HCS003" and skip_ip_check:
                    continue

                for match in pattern.finditer(line):
                    matched_text = match.group(0)

                    # Extra filtering for IPs — skip private/loopback ranges
                    if code == "HCS003" and _SAFE_IPS.match(matched_text):
                        continue

                    results.append(
                        CheckResult(
                            file=file_path,
                            line=lineno,
                            col=match.start() + 1,
                            severity=Severity.ERROR,
                            code=code,
                            message=f"{message}: {matched_text!r}",
                            check_name=self.name,
                            context=stripped[:120],
                        )
                    )

        return results
