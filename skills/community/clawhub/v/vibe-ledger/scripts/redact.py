"""Mask secrets before anything is stored or shown.

A masked secret keeps a recognisable prefix and its last four characters
(`sk-proj-…wXyZ`), so the report can say *which* key leaked without leaking
it again. Masking is idempotent: masked text never matches a pattern again."""
from __future__ import annotations

import math
import re
from collections import Counter

ELLIPSIS = "…"
MIN_ENTROPY = 3.5
MIN_LEN = 20
_B = r"(?<![A-Za-z0-9_\-])"  # not glued to a preceding word: 'task-…' is not 'sk-…'

_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("private_key", re.compile(
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S)),
    ("url_credentials", re.compile(r"(?P<p>\b[a-z][a-z0-9+.\-]*://[^\s:/@'\"]+:)[^\s@/'\"]{3,}(?=@)", re.I)),
    ("anthropic", re.compile(_B + r"(?P<p>sk-ant-)[A-Za-z0-9_\-]{20,}")),
    ("openai", re.compile(_B + r"(?P<p>sk-(?:proj-)?)(?!ant-)[A-Za-z0-9_\-]{20,}")),
    ("stripe", re.compile(_B + r"(?P<p>(?:sk|rk|pk)_(?:live|test)_)[A-Za-z0-9]{10,}")),
    ("stripe_webhook", re.compile(_B + r"(?P<p>whsec_)[A-Za-z0-9+/=]{16,}")),
    ("google", re.compile(_B + r"(?P<p>AIza)[0-9A-Za-z_\-]{30,}")),
    ("aws", re.compile(_B + r"(?P<p>AKIA)[0-9A-Z]{16}")),
    ("github", re.compile(_B + r"(?P<p>ghp_|gho_|ghs_|github_pat_)[A-Za-z0-9_]{20,}")),
    ("slack", re.compile(_B + r"(?P<p>xox[abposr]-)[A-Za-z0-9\-]{10,}")),
    ("jwt", re.compile(_B + r"(?P<p>eyJ)[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}")),
    ("bearer", re.compile(r"(?P<p>\bBearer\s+)[A-Za-z0-9._~+/=\-]{20,}", re.I)),
]
_ASSIGN = re.compile(
    r"(?P<name>\b(?:[A-Za-z_][A-Za-z0-9_]*)?(?:key|secret|token|password|passwd)[A-Za-z0-9_]*)"
    r"(?P<sep>[\"']?\s*[:=]\s*[\"']?)(?P<val>[^\s\"'`,;<>…]{" + str(MIN_LEN) + r",})",
    re.I,
)
# Code that *names* a secret rather than holding one: `process.env.OPENAI_API_KEY`,
# `import.meta.env.VITE_KEY`, `${process.env.X}`, or an env-var name such as `STRIPE_SECRET_KEY_LIVE`.
_IDENT_PATH = re.compile(r"^(?:[A-Za-z_$][\w$]*\.)+[A-Za-z_$][\w$]*$")
_ENV_NAME = re.compile(r"^[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+$")


def _is_reference(val: str) -> bool:
    v = val.strip("${}()")
    if _ENV_NAME.match(v):
        return True
    # a dotted path counts only if one segment is a plain lowercase word (process, env, os, config …)
    return bool(_IDENT_PATH.match(v)) and any(re.fullmatch(r"[a-z]+", seg) for seg in v.split("."))


def _is_secret_value(val: str) -> bool:
    return shannon_entropy(val) >= MIN_ENTROPY and not _is_reference(val)


def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    n = len(s)
    return -sum(c / n * math.log2(c / n) for c in Counter(s).values())


def _mask(kind: str, m: re.Match) -> str:
    if kind == "private_key":
        return "[PRIVATE KEY REDACTED]"
    return f"{m.group('p')}{ELLIPSIS}{m.group(0)[-4:]}"


def find_secrets(text: str) -> list[tuple[int, int, str]]:
    """(start, end, kind) for every unmasked secret in `text`."""
    spans = []
    for kind, rx in _PATTERNS:
        for m in rx.finditer(text or ""):
            if _mask(kind, m) != m.group(0):  # an already-masked value is not a secret
                spans.append((m.start(), m.end(), kind))
    for m in _ASSIGN.finditer(text or ""):
        if _is_secret_value(m.group("val")):
            spans.append((m.start("val"), m.end("val"), "assignment"))
    return sorted(set(spans))


def redact(text: str) -> str:
    if not text:
        return text or ""
    for kind, rx in _PATTERNS:
        text = rx.sub(lambda m, k=kind: _mask(k, m), text)

    def _assign(m: re.Match) -> str:
        val = m.group("val")
        if not _is_secret_value(val):
            return m.group(0)
        return f"{m.group('name')}{m.group('sep')}{ELLIPSIS}{val[-4:]}"

    return _ASSIGN.sub(_assign, text)
