"""Secrets that anyone can read: browser-exposed env vars, keys written in
the code, and env files committed to git."""
from __future__ import annotations

import base64
import json
import re
from pathlib import Path, PurePosixPath

from common import CODE_EXTS, git_ls_files, iter_files, read_text, rel
from probes import Finding
from probes.util import first_code_line, line_at, line_text
from redact import find_secrets

NAME = "secrets_exposed"
APPLIES_TO = None
CLIENT_PREFIXES = ("NEXT_PUBLIC_", "VITE_", "EXPO_PUBLIC_", "REACT_APP_")
SENSITIVE_NAME = re.compile(r"SECRET|SERVICE_ROLE|PRIVATE|PASSWORD", re.I)
ENV_LINE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")
EXAMPLE_SUFFIXES = (".example", ".sample", ".template", ".dist")
TEST_FILE = re.compile(r"(?:^|/)(?:tests?|__tests__|spec|fixtures?)/|\.(?:test|spec)\.[a-z]+$")


def jwt_role(token: str) -> str | None:
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload)).get("role")
    except Exception:
        return None


def sensitive(kind: str, raw: str) -> bool:
    """Anon/publishable keys are designed to be public; everything else is not."""
    if kind == "jwt":
        return jwt_role(raw) == "service_role"
    if kind == "stripe":
        return not raw.startswith("pk_")
    # Google/Firebase browser keys are public by design (restricted per domain), like anon keys
    return kind not in ("assignment", "google")


def _is_env(name: str) -> bool:
    return name.startswith(".env") and not name.endswith(EXAMPLE_SUFFIXES)


def run(root, stack) -> list[Finding]:
    root = Path(root).resolve()
    out: list[Finding] = []
    for p in iter_files(root):
        if not _is_env(p.name):
            continue
        r = rel(p, root)
        for i, line in enumerate(read_text(p).splitlines(), 1):
            m = ENV_LINE.match(line)
            if not m:
                continue
            name, val = m.group(1), m.group(2).strip().strip("'\"")
            prefix = next((x for x in CLIENT_PREFIXES if name.startswith(x)), None)
            if not prefix or not val:
                continue
            secret = any(sensitive(k, val[s:e]) for s, e, k in find_secrets(val))
            if secret or SENSITIVE_NAME.search(name):
                out.append(Finding(NAME, "certain", r, i, line.strip(),
                                   f"{name} starts with {prefix}, so it is bundled into the browser code where anyone can read it"))
    for p in iter_files(root, CODE_EXTS):
        text = read_text(p)
        r = rel(p, root)
        for s, e, kind in find_secrets(text):
            if not sensitive(kind, text[s:e]):
                continue
            ln = line_at(text, s)
            if TEST_FILE.search(r):  # tests are full of fake keys; still worth a look, not a verdict
                out.append(Finding(NAME, "hint", r, ln, line_text(text, ln),
                                   f"A {kind} secret-shaped value is written in a test file (often a fake value)"))
            else:
                out.append(Finding(NAME, "certain", r, ln, line_text(text, ln),
                                   f"A {kind} secret is written directly in the code"))
    for t in git_ls_files(root) or []:
        f = root / t
        if _is_env(PurePosixPath(t).name) and f.is_file():
            ln, snip = first_code_line(read_text(f))
            out.append(Finding(NAME, "certain", t, ln, snip,
                               "This environment file is tracked by git; pushing the repository publishes it"))
    return out
