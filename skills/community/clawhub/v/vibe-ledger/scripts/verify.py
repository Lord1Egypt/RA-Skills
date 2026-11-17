"""Check every piece of evidence in a ledger against the digest, the code and
the probes; downgrade or drop whatever cannot be shown to be true."""
from __future__ import annotations

import os
from pathlib import Path

from common import is_within, norm_ws, read_text, rel
from ledger import normalise, validate
from redact import redact

TOLERANCE = 3
MIN_QUOTE = 4
MIN_SNIPPET = 12  # shorter code fragments match almost anywhere and prove nothing


def find_snippet_lines(lines: list[str], snippet: str) -> list[int]:
    target = norm_ws(snippet)
    if not target:
        return []
    rows = [(n, norm_ws(text)) for n, text in enumerate(lines, 1)]
    rows = [(n, text) for n, text in rows if text]
    k = max(1, sum(1 for line in snippet.splitlines() if line.strip()))
    for size in (k, k + 1):
        hits = [rows[i][0] for i in range(len(rows))
                if target in " ".join(text for _, text in rows[i:i + size])]
        if hits:
            return hits
    return []


def check_transcript(e: dict, index: dict) -> dict:
    rec = index.get(e.get("msg_id"))
    if rec is None:
        return {"ok": False, "reason": "message id not found in the conversation digest"}
    quote = norm_ws(e.get("quote", ""))
    if len(quote) < MIN_QUOTE:
        return {"ok": False, "reason": f"quote is shorter than {MIN_QUOTE} characters"}
    if quote not in norm_ws(rec["text"]):
        return {"ok": False, "reason": "quote is not in that message word for word"}
    return {"ok": True, "ts": rec["ts"], "session": rec["session"], "role": rec["role"], "msg_kind": rec["kind"]}


def check_code(e: dict, root, min_len: int = MIN_SNIPPET) -> dict:
    root = Path(root).resolve()
    raw = str(e.get("path") or "")
    path = Path(raw) if os.path.isabs(raw) else root / raw
    if not raw or not is_within(path, root):
        return {"ok": False, "reason": "path is outside the project"}
    if not path.is_file():
        return {"ok": False, "reason": "file not found"}
    snippet = e.get("snippet") or ""
    if not norm_ws(snippet):
        return {"ok": False, "reason": "snippet is empty"}
    if len(norm_ws(snippet)) < min_len:
        return {"ok": False, "reason": f"snippet is too short to identify code (at least {min_len} characters)"}
    # compare masked text on both sides, so a quote copied from masked material still verifies
    hits = find_snippet_lines([redact(line) for line in read_text(path).splitlines()], redact(snippet))
    given = e.get("line") if isinstance(e.get("line"), int) else 0
    near = [n for n in hits if abs(n - given) <= TOLERANCE]
    base = {"path": rel(path, root)}
    if near:
        return {**base, "ok": True, "line": min(near, key=lambda n: abs(n - given)), "line_corrected": False}
    if len(hits) == 1:
        return {**base, "ok": True, "line": hits[0], "line_corrected": True,
                "reason": f"line corrected from {given} to {hits[0]}"}
    if hits:
        return {"ok": False, "reason": f"snippet occurs {len(hits)} times in the file and none is within "
                                       f"{TOLERANCE} lines of line {given}"}
    return {"ok": False, "reason": "snippet not found in the file"}


def check_probe(e: dict, findings: dict, root) -> dict:
    f = findings.get(e.get("finding_id"))
    if f is None:
        return {"ok": False, "reason": "probe finding not found in probes.json"}
    info = {k: f[k] for k in ("probe", "level", "message", "path", "line", "snippet")}
    code = check_code({"path": f["path"], "line": f["line"], "snippet": f["snippet"]}, root, min_len=1)
    if not code["ok"]:
        return {**info, "ok": False, "reason": "the code changed since the probe ran: " + code["reason"]}
    return {**info, "ok": True, "line": code["line"]}


STRONG = ("code", "probe")
SPEAKERS = {"user_requirement": (("user",), "a user requirement must quote something the user said"),
            "ai_claim": (("assistant",), "an AI claim must quote something the AI said")}


def _check(e: dict, index: dict, root, findings: dict) -> dict:
    if e["kind"] == "transcript":
        return check_transcript(e, index)
    if e["kind"] == "code":
        return check_code(e, root)
    return check_probe(e, findings, root)


def _apply_probe_implications(resources: list[dict], findings: list[dict]) -> int:
    had_any = bool(resources)
    conflicts = 0
    for f in findings:
        for imp in f.get("implies") or []:
            name = imp["resource"]
            targets = [r for r in resources if r["name"] == name or name == "*"]
            if not targets:
                if name == "*" and had_any:
                    continue
                new = {"name": name, "cells": {}, "required_by": None, "added_by_probe": True}
                resources.append(new)
                targets = [new]
            for r in targets:
                cell = r["cells"].setdefault(imp["subject"], {"read": "unknown", "write": "unknown", "evidence": []})
                current = cell.get(imp["perm"], "unknown")
                if current == "unknown":
                    cell[imp["perm"]] = imp["value"]
                    if f["id"] not in cell.setdefault("from_probe", []):
                        cell["from_probe"].append(f["id"])
                elif current != imp["value"]:
                    cell.setdefault("conflicts", []).append({
                        "perm": imp["perm"], "probe": f["id"], "probe_says": imp["value"],
                        "ledger_says": current, "message": f["message"]})
                    conflicts += 1
    return conflicts


def verify_ledger(led: dict, index: dict, root, probes: dict) -> dict:
    validate(led)
    out = normalise(led)
    findings = {f["id"]: f for f in probes.get("findings", [])}
    ev = out["evidence"]
    for eid, e in ev.items():
        e.update(_check(e, index, root, findings))

    def ok(i) -> bool:
        return bool(ev.get(i, {}).get("ok"))

    def strong(ids) -> list:
        return [i for i in ids if ok(i) and ev[i]["kind"] in STRONG]

    rejected, kept, downgraded = [], [], 0
    for x in out["promises"]:
        sources = [i for i in x["source"] if ok(i)]
        if not sources:
            rejected.append({**x, "reason": "none of its quotes could be found in the conversations"})
            continue
        if x["type"] in SPEAKERS:
            roles, why = SPEAKERS[x["type"]]
            sources = [i for i in sources if ev[i].get("role") in roles]
            if not sources:
                rejected.append({**x, "reason": why})
                continue
        x["source"] = sources
        if x["status"] != "unknown" and not strong(x["evidence"]):
            x["downgraded_from"], x["status"] = x["status"], "unknown"
            x["downgrade_reason"] = "no code or probe evidence passed verification"
            downgraded += 1
        kept.append(x)
    out["promises"] = kept
    pids = {x["id"] for x in kept}

    comps = []
    for c in out["compromises"]:
        if not ok(c["error"]) or not any(ok(i) for i in c["change"]):
            rejected.append({**c, "reason": "its error or its change could not be found in the conversations"})
            continue
        if c["still_present"] and not strong(c["now"]):
            c["still_present"] = None
            c["downgrade_reason"] = "no code or probe evidence that it is still in the code"
        if c.get("breaks") not in pids:
            c["breaks"] = None
        comps.append(c)
    out["compromises"] = comps
    out["rejected"] = rejected

    nodes, bad_nodes = [], []
    for n in out["map"]["nodes"]:
        (nodes if strong(n.get("evidence", [])) else bad_nodes).append(n)
    good_ids = {n["id"] for n in nodes}
    edges, bad_edges = [], []
    for e in out["map"]["edges"]:
        drawn = e["from"] in good_ids and e["to"] in good_ids and strong(e.get("evidence", []))
        (edges if drawn else bad_edges).append(e)
    out["map"] = {"nodes": nodes, "edges": edges, "unverified_nodes": bad_nodes, "unverified_edges": bad_edges,
                  "lane_labels": dict(out["map"].get("lane_labels") or {})}

    resources = out["access"]["resources"]
    for r in resources:
        for cell in r["cells"].values():
            cell.setdefault("evidence", [])
            if not strong(cell["evidence"]):
                if cell.get("read", "unknown") != "unknown" or cell.get("write", "unknown") != "unknown":
                    cell["claimed"] = {"read": cell.get("read", "unknown"), "write": cell.get("write", "unknown")}
                cell["read"] = cell["write"] = "unknown"
            cell.setdefault("read", "unknown")
            cell.setdefault("write", "unknown")
        if r.get("required_by") not in pids:
            r["required_by"] = None
    # only findings whose code is unchanged since the probe ran may speak for the matrix
    current = [f for f in findings.values() if check_probe({"finding_id": f["id"]}, findings, root)["ok"]]
    conflicts = _apply_probe_implications(resources, current)

    for path in out["paths"]:
        for st in path["steps"]:
            st["unverified"] = not strong([st["evidence"]])

    failed = [{"id": k, "reason": e.get("reason", "")} for k, e in ev.items() if not e.get("ok")]
    out["verification"] = {
        "evidence_total": len(ev), "evidence_ok": len(ev) - len(failed), "failed": failed,
        "downgraded": downgraded, "rejected": len(rejected),
        "nodes_unverified": len(bad_nodes), "edges_unverified": len(bad_edges),
        "cells_unknown": sum(1 for r in resources for c in r["cells"].values()
                             for perm in ("read", "write") if c.get(perm) == "unknown"),
        "conflicts": conflicts,
    }
    return out


def summary_lines(verified: dict) -> list[str]:
    v = verified["verification"]
    ev = verified["evidence"]
    lines = [f"Evidence: {v['evidence_total']} checked, {v['evidence_ok']} passed, {len(v['failed'])} failed"]
    for f in v["failed"]:
        e = ev[f["id"]]
        where = (f"{e.get('path')}:{e.get('line')}" if e["kind"] in ("code", "probe")
                 else f"message {e.get('msg_id')}")
        lines.append(f"  ✗ {f['id']} ({e['kind']} {where}): {f['reason']}")
    counts = {s: 0 for s in ("kept", "broken", "partial", "pending", "unknown")}
    for p in verified["promises"]:
        counts[p["status"]] += 1
    lines.append("Promises: {} in the ledger (✅{kept} ❌{broken} ⚠{partial} ⏳{pending} ❓{unknown}), "
                 "{d} downgraded to ❓, {r} rejected".format(len(verified["promises"]), d=v["downgraded"],
                                                           r=v["rejected"], **counts))
    lines.append(f"Map: {len(verified['map']['nodes'])} nodes drawn, {v['nodes_unverified']} left off as unverified; "
                 f"Access: {v['cells_unknown']} cells unknown, {v['conflicts']} conflicts with probes")
    return lines
