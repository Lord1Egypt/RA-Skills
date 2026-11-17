"""Small helpers shared by the probes."""
from __future__ import annotations

import re
from pathlib import Path

CODE = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte"}
SERVER_MARKERS = ("api/", "server/", "/server", "supabase/functions", "scripts/", "migrations/",
                  ".server.", "middleware", "route.")
IMPORT = re.compile(r"""(?:from\s+|require\(\s*|import\(\s*)['"]([^'"]+)['"]""")
_EXTS = (".ts", ".tsx", ".js", ".jsx", ".mjs")


def line_at(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def line_text(text: str, lineno: int) -> str:
    lines = text.splitlines()
    return lines[lineno - 1].strip() if 0 < lineno <= len(lines) else ""


def first_code_line(text: str) -> tuple[int, str]:
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip():
            return i, line.strip()
    return 1, ""


def is_client_file(relpath: str, text: str, stacks) -> bool | None:
    """True: runs in the browser. False: server-only. None: cannot tell."""
    p = relpath.lower()
    if any(m in p for m in SERVER_MARKERS) or "'use server'" in text or '"use server"' in text:
        return False
    if "'use client'" in text or '"use client"' in text:
        return True
    if "vite" in stacks and p.startswith("src/"):
        return True
    parts = p.split("/")
    if "components" in parts or "public" in parts:
        return True
    return None


def local_imports(root, path, text: str) -> list[Path]:
    """Files inside the project that `path` imports (relative, `@/` or `~/` specifiers)."""
    root, path = Path(root).resolve(), Path(path).resolve()
    out = []
    for spec in IMPORT.findall(text):
        if spec.startswith("."):
            bases = [path.parent / spec]
        elif spec.startswith(("@/", "~/")):
            bases = [root / "src" / spec[2:], root / spec[2:]]
        else:
            continue
        for base in bases:
            cands = [base] + [base.with_name(base.name + e) for e in _EXTS] + [base / f"index{e}" for e in _EXTS]
            hit = next((c for c in cands if c.is_file()), None)
            if hit:
                out.append(hit.resolve())
                break
    return out
