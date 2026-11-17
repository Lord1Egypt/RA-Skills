"""Find the moments in the digest worth the model's attention and write the
reading packs: the only conversation text the model reads.

Candidates are hints from simple rules; the model judges each one and the
verifier checks whatever it concludes."""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from common import USER_ERROR, git_ignored, iter_files, read_text, rel
from redact import redact

WINDOW_MAX = 20
PACK_LIMIT = 120_000
RECORD_LIMIT = 4000

WRITE_CMD = re.compile(
    r"sed\s+-i|>>?\s*(?!/dev/null)[\w./~\"'-]|\btee\b|<<-?\s*['\"]?\w+|\bpsql\b"
    r"|\bsupabase\s+(?:db|migration)|\bprisma\s+(?:migrate|db)|\bfirebase\s+deploy"
    r"|\b(?:mv|cp|rm)\s|writeFile|open\([^)]*['\"][wa]\+?['\"]"
)
BYPASS = [
    ("rls_disabled", re.compile(r"disable\s+row\s+level\s+security", re.I)),
    ("policy_allows_all", re.compile(r"(?:using|with\s+check)\s*\(\s*true\s*\)", re.I)),
    ("cors_wildcard", re.compile(r"""origin\s*:\s*['"]\*['"]|Access-Control-Allow-Origin['"]?\s*[:,]\s*['"]\*|\bcors\(\s*\)""", re.I)),
    ("type_check_silenced", re.compile(r"@ts-ignore|@ts-nocheck|eslint-disable|:\s*any\b|\bas\s+any\b|#\s*type:\s*ignore|#\s*noqa")),
    ("verify_skipped", re.compile(r"--no-verify|verify\s*=\s*False|rejectUnauthorized\s*:\s*false|NODE_TLS_REJECT_UNAUTHORIZED\s*=\s*['\"]?0|InsecureSkipVerify", re.I)),
    ("service_role_used", re.compile(r"service_role", re.I)),
    ("empty_catch", re.compile(r"catch\s*(?:\([^)]*\))?\s*\{\s*\}|except[^:\n]*:\s*\n?\s*pass\b")),
    ("mock_data", re.compile(r"\b(?:mock|fake|dummy|hardcoded?)\w*", re.I)),
    ("commented_out", re.compile(r"^\s*(?://|#)\s*(?:app\.use|await\s+\w*auth|if\s*\(\s*!?\s*\w*(?:user|session|auth))", re.I | re.M)),
]
GUARD_WORD = re.compile(r"\b(auth\w*|polic\w*|verif\w*|check\w*|validat\w*|permission\w*|require\w*)", re.I)
DEFER = re.compile(
    r"for now|temporar(?:y|ily)|placeholder|\bmock(?:ed)?\b|hard-?cod(?:e|ed)|\bstub(?:bed)?\b"
    r"|in production,? you(?:'ll)? (?:should|need|want)|quick fix|workaround"
    r"|before (?:launch|deploy\w*|going live|you ship)"
    r"|暂时|先这样|之后再|后续再|以后再|临时|写死|模拟数据|先跑起来|先不管|上线前",
    re.I,
)
CLAIM = re.compile(
    r"I(?:'ve| have) (?:added|implemented|set up|secured|protected|enabled|fixed|built|created)"
    r"|now (?:protected|secure|private|requires?|only)|\b(?:is|are) now\b"
    r"|已经|已(?:实现|添加|修复|完成|开启|加)|✅",
    re.I,
)
TODO = re.compile(
    r"(?:(?:^|\s)(?://|#|--)|/\*|<!--)[^\n]*?"
    r"(?:\b(?:TODO|FIXME|HACK|XXX|for now|temporar\w*|mock\w*|placeholder|hard-?coded?)\b|暂时|临时|写死)",
    re.I,
)
TODO_EXTS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".py", ".rb", ".go",
             ".php", ".sql", ".rules", ".html", ".css"}
ROLE = {"user": "USER", "assistant": "AI", "agent": "PARENT-AGENT", "tool": "TOOL-OUTPUT"}
HEADER = (
    "# vibe-ledger reading pack {k}/{n}\n\n"
    "Project: {root}\n\n"
    "Each record starts with `[ID]`. Use that ID as `msg_id`. Copy quotes character for character "
    "from the text under the header, and never quote across a \"not shown\" marker. Candidates are "
    "hints from simple rules, not findings: judge each one.\n\n"
)


def _by_session(recs: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in recs:
        groups[r["session"]].append(r)
    for g in groups.values():
        g.sort(key=lambda r: r["seq"])
    return groups


def is_change(r: dict) -> bool:
    return r["kind"] == "edit" or (r["kind"] == "command" and bool(WRITE_CMD.search(r["text"])))


def _is_error_signal(r: dict) -> bool:
    if r["kind"] == "error":
        return True
    return r["role"] == "user" and r["kind"] == "text" and bool(USER_ERROR.search(r["text"]))


def bypass_hints(r: dict) -> list[str]:
    new = r.get("new") if r.get("new") is not None else (r["text"] if r["kind"] == "command" else "")
    old = r.get("old") or ""
    hints = [name for name, rx in BYPASS if rx.search(new or "")]
    removed = ({m.group(1).lower() for m in GUARD_WORD.finditer(old)}
               - {m.group(1).lower() for m in GUARD_WORD.finditer(new or "")})
    if removed:
        hints.append("removed_guard")
    return hints


def find_compromises(recs: list[dict]) -> list[dict]:
    spans = []  # (session, list, start, end)
    for session, L in _by_session(recs).items():
        cur = None
        for i, r in enumerate(L):
            if not _is_error_signal(r):
                continue
            end = i
            for j in range(i + 1, min(i + WINDOW_MAX, len(L) - 1) + 1):
                if L[j]["turn"] > r["turn"] + 1:
                    break
                end = j
            if cur is not None and i <= cur[3]:
                cur[3] = max(cur[3], end)
                continue
            cur = [session, L, i, end]
            spans.append(cur)
    out = []
    for session, L, start, end in spans:
        window = L[start:end + 1]
        changes = [x for x in window[1:] if is_change(x)]
        if not changes:
            continue
        hints = sorted({h for x in changes for h in bypass_hints(x)})
        out.append({"id": f"K{len(out) + 1}", "session": session, "turn": L[start]["turn"],
                    "error_id": L[start]["id"], "window_ids": [x["id"] for x in window],
                    "change_ids": [x["id"] for x in changes], "hints": hints, "priority": len(hints)})
    return out


def find_deferrals(recs: list[dict]) -> list[dict]:
    out = []
    for r in recs:
        if r["kind"] != "text" or r["role"] not in ("user", "assistant"):
            continue
        phrases = sorted({m.group(0).lower() for m in DEFER.finditer(r["text"])})
        if phrases:
            out.append({"id": f"D{len(out) + 1}", "msg_id": r["id"], "session": r["session"],
                        "turn": r["turn"], "phrases": phrases})
    return out


def find_claims(recs: list[dict]) -> list[dict]:
    out = []
    for session, L in _by_session(recs).items():
        last: dict[int, dict] = {}
        for r in L:
            if r["role"] == "assistant" and r["kind"] == "text":
                last[r["turn"]] = r
        for turn in sorted(last):
            r = last[turn]
            phrases = sorted({m.group(0) for m in CLAIM.finditer(r["text"])})
            if phrases:
                out.append({"id": f"A{len(out) + 1}", "msg_id": r["id"], "session": session,
                            "turn": turn, "phrases": phrases})
    return out


def scan_code_todos(root) -> list[dict]:
    out = []
    paths = iter_files(root, TODO_EXTS)
    ignored = git_ignored(root, (rel(p, root) for p in paths))  # generated output is not the project's
    for p in paths:
        if rel(p, root) in ignored:
            continue
        for i, line in enumerate(read_text(p).splitlines(), 1):
            if len(line) <= 500 and TODO.search(line):
                out.append({"path": rel(p, root), "line": i, "text": redact(line.strip())[:200]})
    return out


def render_record(r: dict) -> str:
    text = r["text"]
    if len(text) > RECORD_LIMIT:
        hidden = len(text) - RECORD_LIMIT
        text = text[:RECORD_LIMIT] + f"\n…[{hidden} more characters not shown — do not quote past this point]"
    return f"#### [{r['id']}] {ROLE.get(r['role'], r['role'])} · {r['ts']} · {r['kind']}\n{text.rstrip()}\n"


def _units(recs, comps, defs, claims) -> list[str]:
    groups = _by_session(recs)
    index = {r["id"]: r for r in recs}
    by_turn: dict[tuple[str, int], list[str]] = defaultdict(list)
    for session, L in groups.items():
        for r in L:
            if r["role"] == "user" and r["kind"] == "text":
                by_turn[(session, r["turn"])].append(render_record(r))
    for c in comps:
        body = "".join(render_record(index[i]) for i in c["window_ids"])
        hints = ", ".join(c["hints"]) or "none"
        by_turn[(c["session"], c["turn"])].append(
            f"**Candidate {c['id']} — an error, then a change** (bypass hints: {hints})\n\n{body}")
    for d in defs:
        by_turn[(d["session"], d["turn"])].append(
            f"**Candidate {d['id']} — put off for later?** (matched: {', '.join(d['phrases'])})\n\n"
            + render_record(index[d["msg_id"]]))
    for a in claims:
        by_turn[(a["session"], a["turn"])].append(
            f"**Candidate {a['id']} — the AI says it did something** (matched: {', '.join(a['phrases'])})\n\n"
            + render_record(index[a["msg_id"]]))
    first_ts = {s: L[0]["ts"] for s, L in groups.items()}
    units = []
    for session, turn in sorted(by_turn, key=lambda k: (first_ts[k[0]], k[1])):
        agent = groups[session][0]["agent"]
        units.append(f"### Session {session} ({agent}) · turn {turn}\n\n" + "\n".join(by_turn[(session, turn)]))
    return units


def build_packs(root, recs, comps, defs, claims, todos, limit: int = PACK_LIMIT) -> list[str]:
    groups: list[list[str]] = []
    cur: list[str] = []
    size = 0
    for unit in _units(recs, comps, defs, claims):
        if cur and size + len(unit) > limit:
            groups.append(cur)
            cur, size = [], 0
        cur.append(unit)
        size += len(unit) + 1
    groups.append(cur)
    todo_text = ""
    if todos:
        todo_text = "\n## Code comments that put work off\n\n" + "".join(
            f"- {t['path']}:{t['line']} — {t['text']}\n" for t in todos)
    packs = []
    for k, units in enumerate(groups, 1):
        body = "\n".join(units) if units else "_No conversation records were found for this project._\n"
        packs.append(HEADER.format(k=k, n=len(groups), root=root) + body + (todo_text if k == 1 else ""))
    return packs


def run(root, recs: list[dict], limit: int = PACK_LIMIT) -> dict:
    comps, defs, claims = find_compromises(recs), find_deferrals(recs), find_claims(recs)
    todos = scan_code_todos(root)
    packs = build_packs(root, recs, comps, defs, claims, todos, limit)
    return {"compromises": comps, "deferrals": defs, "claims": claims, "todos": todos,
            "packs_text": packs,
            "stats": {"compromises": len(comps), "deferrals": len(defs), "claims": len(claims),
                      "todos": len(todos), "packs": len(packs), "pack_chars": [len(p) for p in packs]}}
