"""Supabase row level security as the migrations describe it."""
from __future__ import annotations

import re
from pathlib import Path

from common import iter_files, read_text, rel
from probes import Finding
from probes.util import CODE, is_client_file, line_at, line_text

NAME = "supabase_rls"
APPLIES_TO = {"supabase"}
_T = r"(?:\"?public\"?\.)?\"?(\w+)\"?"
CREATE = re.compile(rf"create\s+table\s+(?:if\s+not\s+exists\s+)?{_T}", re.I)
RLS = re.compile(rf"alter\s+table\s+(?:if\s+exists\s+)?(?:only\s+)?{_T}\s+(enable|disable)\s+row\s+level\s+security", re.I)
POLICY = re.compile(rf"create\s+policy\s+(?:\"[^\"]*\"|\w+)\s+on\s+{_T}(?P<body>[^;]*);", re.I | re.S)
ALLOWS_ALL = re.compile(r"(?:using|with\s+check)\s*\(\s*true\s*\)", re.I)
FROM_CALL = re.compile(r"(?:supabase\w*|client|db)\s*\.from\(\s*['\"`](\w+)['\"`]\s*\)", re.I)
SERVICE_ROLE = re.compile(r"service_role", re.I)
OPEN = ("anonymous", "signed_in")


def _implies(table: str, read: bool, write: bool, subjects) -> list[dict]:
    out = []
    for s in subjects:
        if read:
            out.append({"resource": table, "subject": s, "perm": "read", "value": "allow"})
        if write:
            out.append({"resource": table, "subject": s, "perm": "write", "value": "allow"})
    return out


def _sql_files(root: Path) -> list[Path]:
    out = []
    for p in iter_files(root, {".sql"}):
        parts = rel(p, root).split("/")
        if "supabase" in parts or "migrations" in parts:
            out.append(p)
    return sorted(out, key=lambda q: rel(q, root))


def run(root, stack) -> list[Finding]:
    root = Path(root).resolve()
    out: list[Finding] = []
    tables: dict[str, dict] = {}
    for p in _sql_files(root):
        text, r = read_text(p), rel(p, root)
        events = sorted([(m.start(), "create", m) for m in CREATE.finditer(text)]
                        + [(m.start(), "rls", m) for m in RLS.finditer(text)]
                        + [(m.start(), "policy", m) for m in POLICY.finditer(text)], key=lambda e: e[0])
        for pos, kind, m in events:
            name = m.group(1).lower()
            ln = line_at(text, pos)
            snip = line_text(text, ln)
            t = tables.setdefault(name, {"created": None, "rls": None})
            if kind == "create":
                t["created"] = t["created"] or (r, ln, snip)
            elif kind == "rls":
                t["rls"] = (m.group(2).lower(), r, ln, snip)
            elif ALLOWS_ALL.search(m.group("body")):
                body = m.group("body").lower()
                cmd = re.search(r"\bfor\s+(all|select|insert|update|delete)\b", body)
                cmd = cmd.group(1) if cmd else "all"
                role = re.search(r"\bto\s+(\w+)", body)
                role = role.group(1) if role else "public"
                subjects = ("signed_in",) if role == "authenticated" else OPEN
                read, write = cmd in ("all", "select"), cmd != "select"
                perms = "/".join(x for x, on in (("read", read), ("write", write)) if on)
                who = "signed-in users" if role == "authenticated" else "everyone"
                out.append(Finding(NAME, "certain", r, ln, snip,
                                   f"A policy on table {name} lets {who} {perms} every row (using true)",
                                   _implies(name, read, write, subjects)))
    for name, t in sorted(tables.items()):
        if t["rls"] and t["rls"][0] == "disable":
            _, r, ln, snip = t["rls"]
            out.append(Finding(NAME, "certain", r, ln, snip,
                               f"Row level security is switched off for table {name}: anyone with the public "
                               "anon key can read and change every row", _implies(name, True, True, OPEN)))
        elif t["created"] and not t["rls"]:
            r, ln, snip = t["created"]
            out.append(Finding(NAME, "certain", r, ln, snip,
                               f"Table {name} is created without enabling row level security in the migrations "
                               "(if it was switched on in the Supabase dashboard, that is not visible here)"))
    defined = set(tables)
    for p in iter_files(root, CODE):
        text, r = read_text(p), rel(p, root)
        for m in FROM_CALL.finditer(text):
            name = m.group(1).lower()
            if name not in defined:
                defined.add(name)
                ln = line_at(text, m.start(1))
                out.append(Finding(NAME, "hint", r, ln, line_text(text, ln),
                                   f"Table {name} is used here but not defined in the migrations, so its row level "
                                   "security cannot be checked"))
        m = SERVICE_ROLE.search(text)
        if m:
            client = is_client_file(r, text, stack.get("stacks", []))
            if client is not False:
                ln = line_at(text, m.start())
                out.append(Finding(NAME, "certain" if client else "hint", r, ln, line_text(text, ln),
                                   "The service_role key, which bypasses every access rule, is referenced in code "
                                   "that may run in the browser"))
    return out
