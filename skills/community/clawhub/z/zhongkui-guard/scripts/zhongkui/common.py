from __future__ import annotations

import re
from pathlib import Path

SECRET_PATTERNS = [
    re.compile(r"(?i)(?:sk-[a-z0-9_-]{12,}|AIza[\w-]{20,}|gh[pousr]_[A-Za-z0-9_]{20,})"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)(authorization\s*:\s*bearer\s+)[^\s\"']+"),
]

def redact_text(text: str) -> str:
    value = text
    for pattern in SECRET_PATTERNS:
        value = pattern.sub(lambda m: (m.group(1) if m.lastindex else "") + "[REDACTED]", value)
    return value

def safe_path(path: Path) -> str:
    return redact_text(str(path.resolve()))

