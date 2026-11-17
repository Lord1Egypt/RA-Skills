"""The pages and API endpoints the project defines (facts for the app map and paths)."""
from __future__ import annotations

import re
from pathlib import Path

from common import iter_files, read_text, rel
from probes import Finding
from probes.util import CODE, first_code_line, line_at, line_text

NAME = "routes"
APPLIES_TO = {"nextjs", "express"}
APP_ROUTE = re.compile(r"(?:^|/)app/(?P<dir>(?:.+/)?)route\.(?:t|j)sx?$")
APP_PAGE = re.compile(r"(?:^|/)app/(?P<dir>(?:.+/)?)page\.(?:t|j)sx?$")
PAGES = re.compile(r"(?:^|/)pages/(?P<path>.+)\.(?:t|j)sx?$")
METHOD = re.compile(r"export\s+(?:async\s+)?(?:function|const)\s+(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\b")
EXPRESS = re.compile(r"""\b(?:app|router)\.(get|post|put|patch|delete|all)\(\s*['"`]([^'"`]+)['"`]""")


def _url(directory: str) -> str:
    parts = [s for s in directory.strip("/").split("/") if s and not (s.startswith("(") and s.endswith(")"))]
    return "/" + "/".join(parts)


def run(root, stack) -> list[Finding]:
    root = Path(root).resolve()
    next_js = "nextjs" in stack.get("stacks", [])
    out: list[Finding] = []
    for p in iter_files(root, CODE):
        r, text = rel(p, root), read_text(p)
        if next_js and (m := APP_ROUTE.search(r)):
            for mm in METHOD.finditer(text):
                ln = line_at(text, mm.start())
                out.append(Finding(NAME, "fact", r, ln, line_text(text, ln), f"{mm.group(1)} {_url(m.group('dir'))}"))
            continue
        if next_js and (m := APP_PAGE.search(r)):
            ln, snip = first_code_line(text)
            out.append(Finding(NAME, "fact", r, ln, snip, f"PAGE {_url(m.group('dir'))}"))
            continue
        if next_js and (m := PAGES.search(r)):
            if r.split("/")[-1].startswith("_"):
                continue
            path = m.group("path")
            path = "" if path == "index" else path[:-len("/index")] if path.endswith("/index") else path
            kind = "API" if path == "api" or path.startswith("api/") else "PAGE"
            ln, snip = first_code_line(text)
            out.append(Finding(NAME, "fact", r, ln, snip, f"{kind} /{path}"))
            continue
        for mm in EXPRESS.finditer(text):
            ln = line_at(text, mm.start())
            out.append(Finding(NAME, "fact", r, ln, line_text(text, ln), f"{mm.group(1).upper()} {mm.group(2)}"))
    return out
