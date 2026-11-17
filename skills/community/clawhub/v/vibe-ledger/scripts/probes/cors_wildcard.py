"""Servers that accept calls from every website."""
from __future__ import annotations

import re
from pathlib import Path

from common import iter_files, read_text, rel
from probes import Finding
from probes.util import CODE, line_at, line_text

NAME = "cors_wildcard"
APPLIES_TO = None
RULES = [
    (re.compile(r"""origin\s*:\s*['"]\*['"]"""), "CORS allows every website ('*') to call this server"),
    (re.compile(r"""Access-Control-Allow-Origin['"]?\s*[:,]\s*['"]\*['"]""", re.I),
     "The Access-Control-Allow-Origin header is '*', so every website can call this server"),
    (re.compile(r"\bcors\(\s*\)"), "cors() with no options allows every website to call this server"),
]
CREDENTIALS = re.compile(r"credentials\s*:\s*true|Access-Control-Allow-Credentials['\"]?\s*[:,]\s*['\"]?true", re.I)


def run(root, stack) -> list[Finding]:
    root = Path(root).resolve()
    out: list[Finding] = []
    for p in iter_files(root, CODE | {".py"}):
        text, r = read_text(p), rel(p, root)
        extra = ", and it also accepts the visitor's cookies and credentials" if CREDENTIALS.search(text) else ""
        for rx, msg in RULES:
            for m in rx.finditer(text):
                ln = line_at(text, m.start())
                out.append(Finding(NAME, "certain", r, ln, line_text(text, ln), msg + extra))
    return out
