"""The ledger: the only contract between the model and the scripts."""
from __future__ import annotations

import copy

from common import norm_ws

STATUSES = ("kept", "broken", "partial", "pending", "unknown")
TYPES = ("user_requirement", "ai_claim", "deferred")
QUESTIONS = ("where_data", "what_costs", "who_can_see", "what_breaks", "open_debts")
EVIDENCE_KINDS = ("transcript", "code", "probe")
LANES = ("browser", "server", "storage")
NODE_KINDS = ("page", "route", "function", "database", "storage", "third_party", "client")
SUBJECTS = ("anonymous", "signed_in", "owner")
PERMS = ("allow", "deny", "unknown")
_EVIDENCE_FIELDS = {"transcript": ("session", "msg_id", "quote"), "code": ("path", "line", "snippet"),
                    "probe": ("finding_id",)}
_PROMISE_FIELDS = ("type", "question", "plain", "source", "status", "verdict_plain", "verdict_dev", "evidence")
_COMPROMISE_FIELDS = ("id", "error", "change", "bypassed", "still_present", "now")


class LedgerError(Exception):
    def __init__(self, problems: list[str]):
        super().__init__("\n".join(problems))
        self.problems = problems


def normalise(led: dict) -> dict:
    out = copy.deepcopy(led)
    out.setdefault("compromises", [])
    out.setdefault("map", {})
    out["map"].setdefault("nodes", [])
    out["map"].setdefault("edges", [])
    out.setdefault("access", {})
    out["access"].setdefault("resources", [])
    out.setdefault("paths", [])
    return out


def validate(led: dict) -> None:
    if not isinstance(led, dict):
        raise LedgerError(["the ledger must be a JSON object"])
    p: list[str] = []
    ev = led.get("evidence")
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

    def refs(where: str, ids, kinds=None) -> None:
        if not isinstance(ids, list):
            p.append(f"{where}: must be a list of evidence ids")
            return
        for i in ids:
            if i not in ev:
                p.append(f"{where}: unknown evidence id {i}")
            elif kinds and ev[i].get("kind") not in kinds:
                p.append(f"{where}: evidence {i} must be {' or '.join(kinds)}")

    promises = led.get("promises")
    if not isinstance(promises, list):
        p.append("promises: must be a list")
        promises = []
    pids: set = set()
    for x in promises:
        pid = x.get("id")
        where = f"promise {pid}"
        if not pid or pid in pids:
            p.append(f"{where}: id missing or duplicated")
        pids.add(pid)
        for f in _PROMISE_FIELDS:
            if f not in x:
                p.append(f"{where}: missing {f}")
        if x.get("type") not in TYPES:
            p.append(f"{where}: type must be one of {', '.join(TYPES)}")
        if x.get("question") not in QUESTIONS:
            p.append(f"{where}: question must be one of {', '.join(QUESTIONS)}")
        if x.get("status") not in STATUSES:
            p.append(f"{where}: status must be one of {', '.join(STATUSES)}")
        if x.get("status") == "pending" and x.get("type") != "deferred":
            p.append(f"{where}: status pending is only for type deferred")
        if "source" in x and not x["source"]:
            p.append(f"{where}: source must list at least one transcript evidence id")
        refs(f"{where} source", x.get("source", []), ("transcript",))
        refs(f"{where} evidence", x.get("evidence", []))

    for c in led.get("compromises", []):
        where = f"compromise {c.get('id')}"
        for f in _COMPROMISE_FIELDS:
            if f not in c:
                p.append(f"{where}: missing {f}")
        refs(f"{where} error", [c["error"]] if c.get("error") else [], ("transcript",))
        refs(f"{where} change", c.get("change", []), ("transcript",))
        refs(f"{where} now", c.get("now", []), ("code", "probe"))
        if c.get("breaks") is not None and c.get("breaks") not in pids:
            p.append(f"{where}: breaks refers to unknown promise {c.get('breaks')}")
        if "still_present" in c and not isinstance(c["still_present"], bool):
            p.append(f"{where}: still_present must be true or false")

    m = led.get("map", {})
    labels = m.get("lane_labels", {})  # optional: a project that is not a web app names its own lanes
    if not isinstance(labels, dict) or any(k not in LANES or not isinstance(v, str) or not v.strip()
                                           for k, v in labels.items()):
        p.append(f"map lane_labels: keys must be among {', '.join(LANES)} and values non-empty text")
    nids: set = set()
    for n in m.get("nodes", []):
        where = f"map node {n.get('id')}"
        if not n.get("id") or n["id"] in nids:
            p.append(f"{where}: id missing or duplicated")
        nids.add(n.get("id"))
        if n.get("lane") not in LANES:
            p.append(f"{where}: lane must be one of {', '.join(LANES)}")
        if n.get("kind") not in NODE_KINDS:
            p.append(f"{where}: kind must be one of {', '.join(NODE_KINDS)}")
        if not n.get("label"):
            p.append(f"{where}: missing label")
        if not isinstance(n.get("paid", False), bool):
            p.append(f"{where}: paid must be true or false")
        refs(f"{where} evidence", n.get("evidence", []))
    for e in m.get("edges", []):
        where = f"map edge {e.get('from')}->{e.get('to')}"
        for end in ("from", "to"):
            if e.get(end) not in nids:
                p.append(f"{where}: unknown node {e.get(end)}")
        refs(f"{where} evidence", e.get("evidence", []))

    for r in led.get("access", {}).get("resources", []):
        where = f"access {r.get('name')}"
        if not r.get("name"):
            p.append(f"{where}: missing name")
        for subject, cell in (r.get("cells") or {}).items():
            if subject not in SUBJECTS:
                p.append(f"{where}: subject {subject} must be one of {', '.join(SUBJECTS)}")
                continue
            for perm in ("read", "write"):
                if cell.get(perm, "unknown") not in PERMS:
                    p.append(f"{where} {subject}: {perm} must be one of {', '.join(PERMS)}")
            refs(f"{where} {subject} evidence", cell.get("evidence", []))
        if r.get("required_by") is not None and r.get("required_by") not in pids:
            p.append(f"{where}: required_by refers to unknown promise {r.get('required_by')}")

    for i, path in enumerate(led.get("paths", []), 1):
        where = f"path {path.get('action') or '#' + str(i)}"
        if not path.get("action"):
            p.append(f"{where}: missing action (the name of what the user does, e.g. \"Save a note\")")
        for st in path.get("steps", []):
            if not st.get("label"):
                p.append(f"{where}: a step is missing its label")
            if not isinstance(st.get("evidence"), str):
                p.append(f"{where} step {st.get('label')}: evidence must be one evidence id")
            else:
                refs(f"{where} step {st.get('label')}", [st["evidence"]])

    if p:
        raise LedgerError(p)


def merge(parts: list[dict]) -> dict:
    """Combine chunk ledgers (promises + compromises only) into one ledger."""
    problems = [f"part {n}: map/access/paths belong in the main ledger, not in a part"
                for n, part in enumerate(parts, 1)
                if part.get("map", {}).get("nodes") or part.get("map", {}).get("edges")
                or part.get("access", {}).get("resources") or part.get("paths")]
    if problems:
        raise LedgerError(problems)
    out = normalise({"evidence": {}, "promises": []})
    seen: dict[tuple, dict] = {}
    for n, part in enumerate(parts, 1):
        validate(part)
        pre = f"p{n}_"
        ren = lambda i: pre + i
        for eid, e in part["evidence"].items():
            out["evidence"][ren(eid)] = copy.deepcopy(e)
        idmap: dict[str, str] = {}
        for x in part["promises"]:
            y = copy.deepcopy(x)
            y["id"] = ren(x["id"])
            y["source"] = [ren(i) for i in x["source"]]
            y["evidence"] = [ren(i) for i in x["evidence"]]
            key = (x["type"], norm_ws(part["evidence"][x["source"][0]]["quote"]))
            prev = seen.get(key)
            if prev is not None and prev["status"] == y["status"]:
                idmap[x["id"]] = prev["id"]
                continue
            if prev is not None:
                prev.setdefault("conflict_with", []).append(y["id"])
                y.setdefault("conflict_with", []).append(prev["id"])
            else:
                seen[key] = y
            idmap[x["id"]] = y["id"]
            out["promises"].append(y)
        for c in part.get("compromises", []):
            y = copy.deepcopy(c)
            y["id"] = ren(c["id"])
            y["error"] = ren(c["error"])
            y["change"] = [ren(i) for i in c["change"]]
            y["now"] = [ren(i) for i in c["now"]]
            y["breaks"] = idmap.get(c.get("breaks")) if c.get("breaks") else None
            out["compromises"].append(y)
    validate(out)
    return out
