"""Firebase security rules that let anyone in."""
from __future__ import annotations

import re
from pathlib import Path

from common import iter_files, read_text, rel
from probes import Finding
from probes.util import line_at, line_text

NAME = "firebase_rules"
APPLIES_TO = {"firebase"}
ALLOW_TRUE = re.compile(r"allow\s+([\w\s,]+?)\s*:\s*if\s+true\s*;", re.I)
TEST_MODE = re.compile(r"allow\s+([\w\s,]+?)\s*:\s*if\s+request\.time\s*<\s*timestamp\.date\(", re.I)
RTDB = re.compile(r"\"\.(read|write)\"\s*:\s*(?:true|\"true\")")
READ_OPS = {"read", "get", "list"}
WRITE_OPS = {"write", "create", "update", "delete"}


def _implies(ops: str) -> list[dict]:
    names = {o.strip().lower() for o in ops.split(",")}
    out = []
    for perm, group in (("read", READ_OPS), ("write", WRITE_OPS)):
        if names & group:
            out += [{"resource": "*", "subject": s, "perm": perm, "value": "allow"} for s in ("anonymous", "signed_in")]
    return out


def run(root, stack) -> list[Finding]:
    root = Path(root).resolve()
    out: list[Finding] = []
    for p in iter_files(root):
        if not (p.suffix == ".rules" or p.name == "database.rules.json"):
            continue
        text, r = read_text(p), rel(p, root)
        for rx, msg in ((ALLOW_TRUE, "This rule lets anyone {ops} (if true)"),
                        (TEST_MODE, "This is the test-mode rule: anyone can {ops} until the date in it")):
            for m in rx.finditer(text):
                ln = line_at(text, m.start())
                out.append(Finding(NAME, "certain", r, ln, line_text(text, ln),
                                   msg.format(ops=" ".join(m.group(1).split())), _implies(m.group(1))))
        for m in RTDB.finditer(text):
            ln = line_at(text, m.start())
            out.append(Finding(NAME, "certain", r, ln, line_text(text, ln),
                               f"This Realtime Database rule lets anyone {m.group(1)} everything", _implies(m.group(1))))
    return out
