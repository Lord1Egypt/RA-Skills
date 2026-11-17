"""Detector registry.

A detector is a high-precision rule that locates one class of secret or private
identifier in text. Each yields (start, end, matched_text) spans. Precision
matters more than recall here: a guard that cries wolf gets switched off, so
every detector is tuned to fire only on shapes that are very unlikely to be
anything but the real thing. Lower-confidence shapes carry an entropy gate.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Callable, Iterator, Pattern


def shannon_entropy(s: str) -> float:
    """Bits per character. Random/base64 secrets sit high (~4.5+); English prose
    and dotted paths sit low (~3.5 and below)."""
    if not s:
        return 0.0
    counts: dict[str, int] = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


@dataclass(frozen=True)
class Detector:
    name: str
    severity: str  # "high" | "medium" | "low"
    pattern: Pattern[str]
    label: str  # what the redaction placeholder says
    # optional second-stage validator on the matched secret substring
    validator: Callable[[str], bool] | None = field(default=None)
    # which regex group holds the secret itself (for redaction); 0 = whole match
    group: int = 0

    def finditer(self, text: str) -> Iterator[tuple[int, int, str]]:
        for m in self.pattern.finditer(text):
            start, end = m.span(self.group)
            secret = m.group(self.group)
            if self.validator is not None and not self.validator(secret):
                continue
            yield start, end, secret


def _entropy_at_least(threshold: float) -> Callable[[str], bool]:
    return lambda s: shannon_entropy(s) >= threshold


# --- the registry ---------------------------------------------------------
# Order is irrelevant; spans are de-duplicated by the core scanner.

DETECTORS: list[Detector] = [
    Detector(
        "anthropic_key", "high",
        re.compile(r"sk-ant-[a-zA-Z0-9_\-]{24,}"),
        "anthropic-key",
    ),
    Detector(
        "openrouter_key", "high",
        re.compile(r"sk-or-v1-[a-f0-9]{48,}"),
        "openrouter-key",
    ),
    Detector(
        "openai_key", "high",
        # sk- followed by 32+ base62 chars; excludes the sk-ant/sk-or prefixes
        re.compile(r"sk-(?!ant-|or-)(?:proj-)?[A-Za-z0-9]{32,}"),
        "openai-key",
    ),
    Detector(
        "gitlab_pat", "high",
        re.compile(r"glpat-[A-Za-z0-9_\-]{20,}"),
        "gitlab-token",
    ),
    Detector(
        "github_pat", "high",
        re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
        "github-token",
    ),
    Detector(
        "aws_access_key", "high",
        re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
        "aws-access-key",
    ),
    Detector(
        "slack_token", "high",
        re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
        "slack-token",
    ),
    Detector(
        "stripe_secret", "high",
        re.compile(r"(?:sk|rk)_live_[0-9a-zA-Z]{20,}"),
        "stripe-secret-key",
    ),
    Detector(
        "telegram_bot_token", "high",
        re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b"),
        "telegram-bot-token",
    ),
    Detector(
        "jwt", "high",
        # three base64url segments; the header almost always starts eyJ
        re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
        "jwt-or-supabase-key",
    ),
    Detector(
        "private_key_block", "high",
        re.compile(
            r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"
        ),
        "private-key-block",
    ),
    # Generic "key = <value>" assignments. Gated on entropy so prose like
    # `password: please` or `token: the next one` does not trip it.
    Detector(
        "generic_secret_assignment", "medium",
        re.compile(
            r"""(?ix)
            (?:api[_-]?key|secret|token|password|passwd|pwd|access[_-]?key)
            \s*[:=]\s*
            ['"]?(?P<val>[A-Za-z0-9/+_\-]{16,})['"]?
            """
        ),
        "secret-value",
        validator=_entropy_at_least(3.2),
        group=1,
    ),
    # Private infrastructure paths (our secrets dir + dotenv files).
    Detector(
        "private_path", "medium",
        re.compile(r"/home/workloft/secrets/[^\s'\"]*"),
        "private-path",
    ),
    # RFC1918 private IPs - harmless alone, but leak internal topology.
    Detector(
        "private_ip", "low",
        re.compile(
            r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
            r"|192\.168\.\d{1,3}\.\d{1,3}"
            r"|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"
        ),
        "private-ip",
    ),
]


def by_name(name: str) -> Detector | None:
    for d in DETECTORS:
        if d.name == name:
            return d
    return None
