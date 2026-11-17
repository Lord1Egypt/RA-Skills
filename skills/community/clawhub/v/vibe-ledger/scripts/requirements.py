"""Requirement coverage: every request the user typed, checked against the code.

`start` writes the request packs (every message the user typed, oldest first, each with the end of the
AI message it answers). The model writes requirements.json; `verify` checks every quote and snippet,
re-runs the searches behind a "missing" verdict, and accounts for every user message: each one is
either the source of a requirement or listed as skipped, and the rest are reported as unaccounted."""
from __future__ import annotations

import copy
import re
from collections import defaultdict
from pathlib import Path

from common import git_ignored, git_ls_files, iter_files, norm_ws, read_text, rel
from ledger import _EVIDENCE_FIELDS, EVIDENCE_KINDS

STATUSES = ("done", "partial", "missing", "changed", "superseded", "unknown")
ORDER = ("missing", "partial", "changed", "unknown", "done", "superseded")
SKIP_REASONS = ("ack", "process", "question", "not_project")
FIXABLE = ("missing", "partial")
NEEDS_CODE = ("done", "partial", "changed")
# what the harness writes into the user's turn, not something the user typed
NOISE = re.compile(r"^\s*(?:\[Request interrupted by user|<command-(?:name|message|args)>|<local-command-|Caveat: The messages below)")
CONTEXT_CHARS = 400
RECORD_LIMIT = 4000
PACK_LIMIT = 120_000
MIN_TERM = 4
HEADER = (
    "# vibe-ledger — what the user asked, {k}/{n}\n\n"
    "Project: {root}\n\n"
    "Every message the user typed in the conversations that built this project, oldest first. Each starts with "
    "`[ID]`: use it as `msg_id`, and copy quotes character for character from the text under the header. "
    "\"AI before this\" is the end of the AI message the user was answering — context for short replies such as "
    "\"yes, do 2 and 3\"; it is cut, so quote it only from what is shown. Account for every `[ID]` in "
    "requirements.json: as the `source` of a requirement, or under `skipped`.\n\n"
)


class RequirementsError(Exception):
    def __init__(self, problems: list[str]):
        super().__init__("\n".join(problems))
        self.problems = problems


# ---- the request packs ----

def user_messages(recs: list[dict]) -> list[dict]:
    """The messages the user typed, in conversation order (harness notes left out)."""
    first: dict[str, str] = {}
    for r in recs:
        first.setdefault(r["session"], r["ts"] or "")
        first[r["session"]] = min(first[r["session"]], r["ts"] or first[r["session"]])
    out = [r for r in recs if r["role"] == "user" and r["kind"] == "text" and r["text"].strip()
           and not NOISE.match(r["text"])]
    return sorted(out, key=lambda r: (first[r["session"]], r["session"], r["seq"]))


def noise_count(recs: list[dict]) -> int:
    return sum(1 for r in recs if r["role"] == "user" and r["kind"] == "text" and NOISE.match(r["text"]))


def _context(recs: list[dict]) -> dict[str, str]:
    """For each user message, the end of the last AI text before it in the same conversation."""
    by_session: dict[str, list[dict]] = defaultdict(list)
    for r in recs:
        by_session[r["session"]].append(r)
    out = {}
    for L in by_session.values():
        last = ""
        for r in sorted(L, key=lambda r: r["seq"]):
            if r["role"] == "assistant" and r["kind"] == "text" and r["text"].strip():
                last = r["text"]
            elif r["role"] == "user" and r["kind"] == "text":
                out[r["id"]] = last
                last = ""
    return out


def _entry(r: dict, ctx: str) -> str:
    text = r["text"].rstrip()
    if len(text) > RECORD_LIMIT:
        text = text[:RECORD_LIMIT] + f"\n…[{len(r['text']) - RECORD_LIMIT} more characters not shown — do not quote past this point]"
    out = f"#### [{r['id']}] USER · {r['ts']} · turn {r['turn']}\n{text}\n"
    ctx = ctx.strip()
    if ctx:
        tail = ctx[-CONTEXT_CHARS:]
        cut = "…" if len(ctx) > CONTEXT_CHARS else ""
        out += "> AI before this: " + cut + " ".join(tail.split()) + "\n"
    return out


def build_packs(root, recs: list[dict], limit: int = PACK_LIMIT) -> tuple[list[str], dict]:
    msgs = user_messages(recs)
    ctx = _context(recs)
    units, cur_session = [], None
    for r in msgs:
        head = ""
        if r["session"] != cur_session:
            cur_session = r["session"]
            head = f"### Session {r['session']} ({r['agent']})\n\n"
        units.append(head + _entry(r, ctx.get(r["id"], "")))
    groups: list[list[str]] = []
    cur: list[str] = []
    size = 0
    for u in units:
        if cur and size + len(u) > limit:
            groups.append(cur)
            cur, size = [], 0
        cur.append(u)
        size += len(u) + 1
    groups.append(cur)
    packs = []
    for k, g in enumerate(groups, 1):
        body = "\n".join(g) if g else "_No messages from the user were found for this project._\n"
        packs.append(HEADER.format(k=k, n=len(groups), root=root) + body)
    info = {"messages": len(msgs), "noise": noise_count(recs), "sessions": len({r["session"] for r in msgs}),
            "chars": [len(p) for p in packs]}
    return packs, info


# ---- the file the model writes ----

def _ids(where: str, ids, ev: dict, problems: list, kinds=None) -> None:
    if not isinstance(ids, list):
        problems.append(f"{where}: must be a list of evidence ids")
        return
    for i in ids:
        if i not in ev:
            problems.append(f"{where}: unknown evidence id {i}")
        elif kinds and ev[i].get("kind") not in kinds:
            problems.append(f"{where}: evidence {i} must be {' or '.join(kinds)}")


def validate(doc: dict) -> None:
    if not isinstance(doc, dict):
        raise RequirementsError(["requirements.json must be a JSON object"])
    p: list[str] = []
    ev = doc.get("evidence")
    if not isinstance(ev, dict):
        p.append("evidence: must be an object mapping ids to evidence")
        ev = {}
    for eid, e in ev.items():
        kind = e.get("kind") if isinstance(e, dict) else None
        if kind not in EVIDENCE_KINDS:
            p.append(f"evidence {eid}: kind must be one of {', '.join(EVIDENCE_KINDS)}")
            continue
        for f in _EVIDENCE_FIELDS[kind]:
            if f not in e:
                p.append(f"evidence {eid}: missing {f}")
        if kind == "code" and "line" in e and not isinstance(e["line"], int):
            p.append(f"evidence {eid}: line must be an integer")
    reqs = doc.get("requirements")
    if not isinstance(reqs, list):
        p.append("requirements: must be a list")
        reqs = []
    seen: set = set()
    for x in reqs:
        if not isinstance(x, dict):
            p.append("requirements: every item must be an object")
            continue
        rid = x.get("id")
        where = f"requirement {rid}"
        if not rid or rid in seen:
            p.append(f"{where}: id missing or duplicated")
        seen.add(rid)
        for f in ("plain", "verdict_plain", "verdict_dev"):
            if not isinstance(x.get(f), str) or not x[f].strip():
                p.append(f"{where}: missing {f}")
        if "area" in x and not isinstance(x["area"], str):
            p.append(f"{where}: area must be text")
        status = x.get("status")
        if status not in STATUSES:
            p.append(f"{where}: status must be one of {', '.join(STATUSES)}")
        if not x.get("source"):
            p.append(f"{where}: source must list at least one transcript evidence id (the user's message)")
        _ids(f"{where} source", x.get("source", []), ev, p, ("transcript",))
        _ids(f"{where} evidence", x.get("evidence", []), ev, p)
        _ids(f"{where} agreed_in", x.get("agreed_in", []), ev, p, ("transcript",))
        if status == "changed" and not (isinstance(x.get("changed_to"), str) and x["changed_to"].strip()):
            p.append(f"{where}: status changed needs changed_to (what was built instead)")
        if status == "superseded":
            sb = x.get("superseded_by")
            if not isinstance(sb, str) or sb not in ev or ev[sb].get("kind") != "transcript":
                p.append(f"{where}: status superseded needs superseded_by: the transcript evidence id of the user's later message")
        searched = x.get("searched", [])
        if not isinstance(searched, list) or any(not isinstance(s, str) for s in searched):
            p.append(f"{where}: searched must be a list of text")
    skipped = doc.get("skipped", {})
    if not isinstance(skipped, dict):
        p.append("skipped: must be an object {reason: [message ids]}")
    else:
        for reason, ids in skipped.items():
            if reason not in SKIP_REASONS:
                p.append(f"skipped: reason {reason} must be one of {', '.join(SKIP_REASONS)}")
            if not isinstance(ids, list) or any(not isinstance(i, str) for i in ids):
                p.append(f"skipped {reason}: must be a list of message ids")
    if p:
        raise RequirementsError(p)


def merge(parts: list[dict]) -> dict:
    """Combine req_NN.json parts (one per request pack) into one requirements.json."""
    out = {"evidence": {}, "requirements": [], "skipped": {}}
    for n, part in enumerate(parts, 1):
        validate(part)
        ren = lambda i, n=n: f"r{n}_{i}"  # noqa: E731
        for eid, e in part["evidence"].items():
            out["evidence"][ren(eid)] = copy.deepcopy(e)
        for x in part["requirements"]:
            y = copy.deepcopy(x)
            y["id"] = ren(x["id"])
            for key in ("source", "evidence", "agreed_in"):
                if key in y:
                    y[key] = [ren(i) for i in y[key]]
            if y.get("superseded_by"):
                y["superseded_by"] = ren(y["superseded_by"])
            out["requirements"].append(y)
        for reason, ids in (part.get("skipped") or {}).items():
            out["skipped"].setdefault(reason, []).extend(i for i in ids if i not in out["skipped"].get(reason, []))
    validate(out)
    return out


# ---- verification ----

def _project_texts(root: Path) -> list[tuple[str, list[str]]]:
    files = git_ls_files(root)
    paths = [root / f for f in files] if files is not None else iter_files(root)
    rels = [rel(p, root) for p in paths]
    ignored = git_ignored(root, rels)
    out = []
    for p, r in zip(paths, rels):
        if r in ignored or not p.is_file() or p.is_symlink():
            continue
        try:
            if p.stat().st_size > 1_000_000:
                continue
            with open(p, "rb") as fh:
                if b"\0" in fh.read(8192):
                    continue
        except OSError:
            continue
        out.append((r, read_text(p).splitlines()))
    return out


def search_terms(terms: list[str], texts: list[tuple[str, list[str]]]) -> dict:
    """Where each term occurs in the project (case-insensitive), first hit only."""
    hits = {}
    for term in terms:
        needle = norm_ws(term).lower()
        for path, lines in texts:
            found = next((n for n, line in enumerate(lines, 1) if needle in norm_ws(line).lower()), None)
            if found:
                hits[term] = f"{path}:{found}"
                break
    return hits


def verify(doc: dict, recs: list[dict], root, probes: dict) -> dict:
    import verify as V  # the ledger's evidence checks, unchanged
    validate(doc)
    root = Path(root).resolve()
    out = copy.deepcopy(doc)
    out.setdefault("skipped", {})
    index = {r["id"]: r for r in recs}
    findings = {f["id"]: f for f in probes.get("findings", [])}
    ev = out["evidence"]
    for e in ev.values():
        e.update(V._check(e, index, root, findings))

    def ok(i) -> bool:
        return bool(ev.get(i, {}).get("ok"))

    def by_user(i) -> bool:
        return ok(i) and ev[i].get("role") == "user"

    def strong(ids) -> list:
        return [i for i in ids if ok(i) and ev[i]["kind"] in V.STRONG]

    texts = None
    kept, rejected, downgraded = [], [], 0
    for x in out["requirements"]:
        x.setdefault("area", "")
        x.setdefault("evidence", [])
        sources = [i for i in x["source"] if by_user(i)]
        if not sources:
            why = ("none of its quotes could be found in the conversations" if not any(ok(i) for i in x["source"])
                   else "a requirement must quote something the user said")
            rejected.append({**x, "reason": why})
            continue
        # the user's words first; the AI message they approved (when cited) stays on record after them
        x["source"] = sources + [i for i in x["source"] if ok(i) and i not in sources]
        x["said_at"] = min(ev[i].get("ts") or "" for i in sources)
        x["agreed_in"] = [i for i in x.get("agreed_in", []) if by_user(i)]
        reason = None
        status = x["status"]
        if status in NEEDS_CODE and not strong(x["evidence"]):
            reason = "no code or probe evidence passed verification"
        elif status == "missing" and not strong(x["evidence"]):
            terms = [t for t in x.get("searched", []) if len(norm_ws(t)) >= MIN_TERM]
            if not terms:
                reason = f"no code evidence, and no search term of at least {MIN_TERM} characters to show it is absent"
            else:
                texts = texts if texts is not None else _project_texts(root)
                hits = search_terms(terms, texts)
                x["searched"] = terms
                if hits:
                    reason = "searched terms are in the project: " + "; ".join(f"{k} at {v}" for k, v in hits.items())
                else:
                    x["absent_verified"] = True
        elif status == "superseded":
            sb = x.get("superseded_by")
            if not by_user(sb):
                reason = "the later message that changed it could not be found, or the user did not write it"
            elif (ev[sb].get("ts") or "") <= x["said_at"]:
                reason = "the message that changed it is not later than the requirement"
        if reason:
            x["downgraded_from"], x["status"], x["downgrade_reason"] = status, "unknown", reason
            downgraded += 1
        x["files"] = sorted({ev[i]["path"] for i in strong(x["evidence"]) if ev[i].get("path")})
        kept.append(x)
    out["requirements"] = kept
    out["rejected"] = rejected

    msgs = user_messages(recs)
    msg_ids = {r["id"] for r in msgs}
    cited = {i for x in kept for i in x["source"]} | {i for x in kept for i in x.get("agreed_in", [])}
    cited |= {x["superseded_by"] for x in kept if x["status"] == "superseded"}
    cited_msgs = {ev[i]["msg_id"] for i in cited if i in ev}
    skipped_ok: dict[str, list] = {}
    stray, seen = [], set(cited_msgs)  # a message cited by a requirement is not also skipped; each counts once
    for reason, ids in out["skipped"].items():
        skipped_ok[reason] = []
        for i in ids:
            if i not in msg_ids:
                stray.append(i)
            elif i not in seen:
                seen.add(i)
                skipped_ok[reason].append(i)
    skipped_ids = {i for ids in skipped_ok.values() for i in ids}
    unaccounted = [{"id": r["id"], "session": r["session"], "ts": r["ts"], "text": r["text"][:300]}
                   for r in msgs if r["id"] not in cited_msgs and r["id"] not in skipped_ids]
    sessions = defaultdict(int)
    for r in msgs:
        if r["id"] in cited_msgs:
            sessions[r["session"]] += 1
    out["skipped"] = skipped_ok
    out["coverage"] = {
        "messages": len(msgs), "noise": noise_count(recs), "cited": len(cited_msgs & msg_ids),
        "skipped": {k: len(v) for k, v in skipped_ok.items() if v}, "stray_skipped": stray,
        "unaccounted": unaccounted,
        "sessions_without": sorted({r["session"] for r in msgs} - set(sessions)),
    }
    failed = [{"id": k, "reason": e.get("reason", "")} for k, e in ev.items() if not e.get("ok")]
    out["verification"] = {"evidence_total": len(ev), "evidence_ok": len(ev) - len(failed), "failed": failed,
                           "downgraded": downgraded, "rejected": len(rejected)}
    return out


def counts(doc: dict) -> dict:
    c = {s: 0 for s in ORDER}
    for x in doc.get("requirements", []):
        c[x["status"]] += 1
    return c


GLYPH = {"done": "✅", "partial": "⚠️", "missing": "❌", "changed": "🔀", "superseded": "↩️", "unknown": "❓"}


def summary_lines(v: dict) -> list[str]:
    ver, cov = v["verification"], v["coverage"]
    lines = [f"Requirements evidence: {ver['evidence_total']} checked, {ver['evidence_ok']} passed, {len(ver['failed'])} failed"]
    for f in ver["failed"]:
        e = v["evidence"][f["id"]]
        where = f"{e.get('path')}:{e.get('line')}" if e["kind"] in ("code", "probe") else f"message {e.get('msg_id')}"
        lines.append(f"  ✗ {f['id']} ({e['kind']} {where}): {f['reason']}")
    c = counts(v)
    lines.append(f"Requirements: {len(v['requirements'])} (" + " ".join(f"{GLYPH[s]}{c[s]}" for s in ORDER)
                 + f"), {ver['downgraded']} downgraded to ❓, {ver['rejected']} rejected")
    for x in v["requirements"]:
        if x.get("downgrade_reason"):
            lines.append(f"  ❓ {x['id']} ({x['downgraded_from']} → unknown): {x['downgrade_reason']}")
    for x in v["rejected"]:
        lines.append(f"  ✗ {x.get('id')}: {x['reason']}")
    skipped = sum(cov["skipped"].values())
    lines.append(f"User messages: {cov['messages']}; {cov['cited']} cited by a requirement, {skipped} skipped, "
                 f"{len(cov['unaccounted'])} unaccounted")
    for u in cov["unaccounted"][:15]:
        lines.append(f"  · {u['id']}: {' '.join(u['text'].split())[:100]}")
    if len(cov["unaccounted"]) > 15:
        lines.append(f"  · … and {len(cov['unaccounted']) - 15} more")
    if cov["stray_skipped"]:
        lines.append(f"  skipped ids that are not user messages (ignored): {', '.join(cov['stray_skipped'][:10])}")
    return lines
