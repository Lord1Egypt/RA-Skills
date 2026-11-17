"""The file-flowchart tab: page data (masked) and the static skeleton graph.js fills."""
from __future__ import annotations

import json
from collections import defaultdict
import re
from pathlib import Path, PurePosixPath

from common import read_text
from graph import folder_groups
from ledger_report.bits import GLYPH, fit, fmt_date, h
from ledger_report.i18n import STR, probe_message, t
from ledger_report.requirements_html import panel_data
from redact import redact

VENDOR_DIR = Path(__file__).resolve().parent / "vendor"
SNIPPET_LINES = 8
LABEL_UNITS = 22  # what fits on a 236 px card at 14 px bold
SUB_UNITS = 28  # the same card's second line at 11.5 px
BAD_STATUSES = ("broken",)
WARN_STATUSES = ("partial", "pending")


def dagre_source() -> str:
    text = (VENDOR_DIR / "dagre.min.js").read_text(encoding="utf-8")
    return "\n".join(line for line in text.splitlines() if "sourceMappingURL" not in line)


def _mask(value):
    if isinstance(value, str):
        return redact(value)
    if isinstance(value, list):
        return [_mask(v) for v in value]
    if isinstance(value, dict):
        return {k: _mask(v) for k, v in value.items()}
    return value


def data_script(data: dict) -> str:
    # no "<" reaches the HTML tokenizer: "</script>" would end the element and "<!--<script" would stop the real
    # end tag from ending it; JSON.parse reads \u003c back as "<"
    payload = (json.dumps(_mask(data), ensure_ascii=False).replace("<", "\\u003c")
               .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))
    return f'<script type="application/json" id="vl-data">{payload}</script>'


def _evidence_paths(ids, evidence) -> set:
    return {evidence[i]["path"] for i in ids if evidence.get(i, {}).get("ok")
            and evidence[i].get("kind") in ("code", "probe") and evidence[i].get("path")}


def _file_risks(ledger: dict, probes: dict, lang: str) -> tuple[dict, dict]:
    risks: dict[str, list] = defaultdict(list)
    promises: dict[str, list] = defaultdict(list)
    for f in probes.get("findings", []):
        if f.get("level") in ("certain", "hint"):
            risks[f["path"]].append({"level": "bad" if f["level"] == "certain" else "warn",
                                     "text": probe_message(f.get("message", ""), lang), "where": f"{f['path']}:{f.get('line', '')}"})
    ev = ledger.get("evidence", {})
    for p in ledger.get("promises", []):
        for path in _evidence_paths(p.get("evidence", []), ev):
            promises[path].append({"id": p["id"], "status": p["status"], "glyph": GLYPH[p["status"]], "plain": p["plain"]})
            if p["status"] in BAD_STATUSES or p["status"] in WARN_STATUSES:
                risks[path].append({"level": "bad" if p["status"] in BAD_STATUSES else "warn",
                                    "text": f"{GLYPH[p['status']]} {p['plain']}", "where": path})
    for c in ledger.get("compromises", []):
        if c.get("still_present") is True:
            for path in _evidence_paths(c.get("now", []), ev):
                risks[path].append({"level": "bad", "text": f"{t(lang, 'g_compromise')}: {c.get('bypassed', '')}", "where": path})
    return risks, promises


def _state(items) -> tuple[str, int, int]:
    bad = sum(1 for r in items if r["level"] == "bad")
    warn = sum(1 for r in items if r["level"] == "warn")
    return ("bad" if bad else "warn" if warn else "ok"), bad, warn


def _badge(lang, state, bad, warn) -> str:
    if state == "bad":
        return t(lang, "g_badge_bad", n=bad)
    if state == "warn":
        return t(lang, "g_badge_warn", n=warn)
    return ""


def _snippets(root: Path, path: str, functions) -> list[dict]:
    lines = read_text(root / path).splitlines()
    return [{"name": f["name"], "line": f["line"],
             "code": "\n".join(lines[f["line"] - 1:f["line"] - 1 + SNIPPET_LINES])} for f in functions]


def page_data(g: dict, explained: dict, ledger: dict, probes: dict, root, lang: str, has_transcripts: bool,
              diff: dict | None = None, requirements: dict | None = None) -> dict:
    root = Path(root).resolve()
    reqs = panel_data(requirements, lang)
    fmap = explained.get("function_map")
    area_of = {p: a for a in (fmap or {}).get("areas", []) for p in a["files"]}
    risks, promises = _file_risks(ledger, probes, lang)
    calls, called_by = defaultdict(list), defaultdict(list)
    call_names, caller_names = defaultdict(dict), defaultdict(dict)  # which names each link imports (developer view)
    for e in g["edges"]:
        calls[e["from"]].append(e["to"])
        called_by[e["to"]].append(e["from"])
        if e["names"]:
            call_names[e["from"]][e["to"]] = e["names"]
            caller_names[e["to"]][e["from"]] = e["names"]
    entry_reason = {e["path"]: e["reason"] for e in g["entries"]}
    exp_files = explained.get("files", {})
    exp_evidence = explained.get("evidence", {})
    labels_by_id = {n["id"]: n["label"] for n in g["nodes"]} | {x["id"]: x["label"] for x in g["externals"]}
    node_ids = {n["id"] for n in g["nodes"]}
    journeys, positions = [], defaultdict(list)
    for j in explained.get("journeys", []):
        steps = [{"file": st["file"], "plain": st["plain"], "linked": st.get("linked", True),
                  **({"from": st["from"]} if "from" in st else {}),
                  **({"function": st["function"], "line": st["line"]} if "function" in st else {})}
                 for st in j["steps"] if st["file"] in node_ids]
        if len(steps) < 2:
            continue
        journeys.append({"id": j["id"], "title": j["title"], "outcome": j.get("outcome", ""), "steps": steps})
        for k, st in enumerate(steps, 1):
            positions[st["file"]].append({"journey": j["id"], "text": t(lang, "g_position_step", title=j["title"], k=k,
                                                                          n=len(steps), plain=st["plain"])})
    nodes, state_of = [], {}
    for n in g["nodes"]:
        fid = n["id"]
        state, bad, warn = _state(risks.get(fid, []))
        state_of[fid] = state
        exp = exp_files.get(fid)
        names = ", ".join(x["name"] for x in n["exports"][:5])
        auto = (t(lang, "g_auto_entry", reason=entry_reason[fid]) if fid in entry_reason else "")
        auto += (t(lang, "g_auto_exports", n=len(n["exports"]), names=names) if n["exports"] else t(lang, "g_auto_noexports"))
        auto += t(lang, "g_auto_used", n=len(called_by[fid]))
        history = []
        for item in (exp or {}).get("history", []):
            e = exp_evidence.get(item["evidence"][0], {})
            history.append({"plain": item["plain"], "date": fmt_date(e.get("ts")), "quote": e.get("quote", "")})
        edits = n.get("edits")
        card = {
            "path": fid, "label": n["label"], "folder": n["folder"], "role": n["role"],
            "role_label": t(lang, "g_role_" + n["role"]), "lines": t(lang, "g_lines", n=n["lines"]),
            "explained": exp is not None,
            "purpose_plain": exp["purpose_plain"] if exp else "", "purpose_dev": exp.get("purpose_dev", "") if exp else "",
            "purpose_unverified": bool(exp and exp.get("purpose_unverified")),
            "unverified_note": t(lang, "g_unverified", ids=", ".join(exp["missing_identifiers"]))
            if exp and exp.get("purpose_unverified") else "",
            "auto": auto, "calls": calls[fid], "called_by": called_by[fid],
            "call_names": call_names.get(fid, {}), "caller_names": caller_names.get(fid, {}),
            "functions": [{"name": f["name"], "line": f["line"], "plain": f["plain"]} for f in (exp or {}).get("functions", [])],
            "exports": n["exports"], "risks": risks.get(fid, []), "promises": promises.get(fid, []),
            "history": history,
            "history_note": "" if history else (t(lang, "g_no_history") if has_transcripts else t(lang, "g_no_history_tx")),
            "edits": t(lang, "g_edits", count=edits["count"], first=fmt_date(edits["first"])[:10],
                       last=fmt_date(edits["last"])[:10]) if edits else "",
            "snippets": _snippets(root, fid, (exp or {}).get("functions", [])),
            "positions": positions.get(fid, []),
            "requirements": reqs["by_file"].get(fid, []) if reqs else [],
            "area": {"name": area_of[fid]["name"], "plain": area_of[fid]["plain"]} if fid in area_of else None,
        }
        sub = (exp["purpose_plain"] if exp else n["folder"] or "")
        card["diff_notes"] = _diff_notes(fid, diff, labels_by_id, lang)
        nodes.append({"id": fid, "label": n["label"], "short": fit(n["label"], LABEL_UNITS), "sub": fit(sub, SUB_UNITS),
                      "role": n["role"], "state": state, "diff": _diff_flag(fid, diff),
                      "badge": _badge(lang, state, bad, warn), "folder": n["folder"], "card": card})
    for x in g["externals"]:
        users = called_by[x["id"]]
        card = {"path": x["id"], "label": x["label"], "folder": "", "role": x["kind"],
                "role_label": t(lang, "g_role_" + x["kind"]), "auto": t(lang, "g_auto_external", label=x["label"], n=len(users)),
                "called_by": users, "calls": [], "evidence": [{"where": f"{e['path']}:{e['line']}", "code": e["snippet"]}
                                                              for e in x["evidence"]]}
        nodes.append({"id": x["id"], "label": x["label"], "short": fit(x["label"], LABEL_UNITS),
                      "sub": t(lang, "g_role_" + x["kind"]), "role": x["kind"],
                      "state": "ok", "badge": "", "folder": "", "card": card,
                      "diff": "new" if diff and x["id"] in diff["services"]["added"] else None})
    folders = []
    for f in g.get("folders", []):
        state, bad, warn = _state([r for fid in f["files"] for r in risks.get(fid, [])])
        folders.append({"id": f["id"], "files": f["files"], "state": state, "badge": _badge(lang, state, bad, warn),
                        "label": f["id"], "short": fit(f["id"].rsplit("/", 1)[-1], LABEL_UNITS - 2) + " ▸",
                        "sub": t(lang, "g_folder_files", n=len(f["files"]))})
    edges = [{"from": e["from"], "to": e["to"], "names": e["names"],
              "risky": state_of.get(e["from"]) == "bad" or state_of.get(e["to"]) == "bad"} for e in g["edges"]]
    ranked = sorted((n for n in nodes if n["state"] != "ok" and not n["id"].startswith("ext:")),
                    key=lambda n: (-sum(r["level"] == "bad" for r in n["card"]["risks"]),
                                   -sum(r["level"] == "warn" for r in n["card"]["risks"]), n["id"]))
    paid = sum(1 for x in g["externals"] if x["kind"] == "paid")
    return {"lang": lang, "project": Path(root).name, "strings": {k: v for k, v in STR.get(lang, STR["en"]).items() if k.startswith("g_")},
            "nodes": nodes, "edges": edges, "folders": folders, "collapsed": bool(g.get("collapsed")),
            "entries": [e["path"] for e in g["entries"]],
            "summary": t(lang, "g_summary", files=len(g["nodes"]), entries=len(g["entries"]), ext=len(g["externals"]), paid=paid),
            "howto": [t(lang, "g_howto_1"), t(lang, "g_howto_2"), t(lang, "g_howto_3")],
            "top": [n["id"] for n in ranked[:3]],
            "coverage": {"excluded": g.get("excluded", {}), "unresolved": g.get("unresolved", []),
                         "rejected": explained.get("rejected", []),
                         "dropped": [{"path": p, "name": d["name"], "reason": d["reason"]}
                                     for p, f in sorted(exp_files.items()) for d in f.get("dropped_functions", [])]
                         + [{"path": j["title"], "name": d["file"], "reason": d["reason"]}
                            for j in explained.get("journeys", []) for d in j.get("dropped_steps", [])]
                         + [{"path": r["title"], "name": "", "reason": r["reason"]}
                            for r in explained.get("rejected_journeys", [])]},
            "journeys": journeys, "has_journeys": bool(journeys),
            "diff": _diff_summary(diff, labels_by_id, lang) if diff else None,
            "modules": _modules(g, risks, lang), "data_flow": _data_flow(g, ledger),
            "requirements": {"line": reqs["line"], "unaccounted": reqs["unaccounted"]} if reqs else None,
            **_function_map(fmap, g, risks, lang)}


def _modules(g: dict, risks: dict, lang: str) -> list[dict]:
    """Every file in a module (for the module view): the folder split the flowchart uses for big projects, then the
    rest grouped by their own folder when it holds two or more of them; a file alone in its folder stays a card."""
    paths = sorted(n["id"] for n in g["nodes"])
    groups = {f["id"]: f["files"] for f in folder_groups(paths)}
    placed = {p for files in groups.values() for p in files}
    rest: dict[str, list[str]] = defaultdict(list)
    for p in paths:
        if p not in placed:
            rest[PurePosixPath(p).parent.as_posix()].append(p)
    for parent, files in rest.items():
        if parent != "." and len(files) >= 2 and parent not in groups:
            groups[parent] = sorted(files)
    out = []
    for mid, files in sorted(groups.items()):
        state, bad, warn = _state([r for fid in files for r in risks.get(fid, [])])
        out.append({"id": mid, "files": files, "state": state, "badge": _badge(lang, state, bad, warn), "label": mid,
                    "short": fit(mid.rsplit("/", 1)[-1], LABEL_UNITS - 2) + " ▸", "sub": t(lang, "g_folder_files", n=len(files))})
    return out


def _function_map(fmap: dict | None, g: dict, risks: dict, lang: str) -> dict:
    """The map view's groups (one per area, plus "other"), the data links drawn between areas, and the data view's
    nodes and edges. Empty when explain.json has no areas: the page then keeps the folder views."""
    if not fmap or not fmap.get("areas"):
        return {"areas": None, "area_links": [], "flow": None}
    groups = []
    for a in fmap["areas"] + ([{"id": "__other", "name": t(lang, "g_area_other_name"), "plain": t(lang, "g_area_other_plain"),
                                "files": fmap["other"]}] if fmap["other"] else []):
        state, bad, warn = _state([r for fid in a["files"] for r in risks.get(fid, [])])
        groups.append({"id": a["id"], "files": a["files"], "state": state, "badge": _badge(lang, state, bad, warn),
                       "label": a["name"], "plain": a["plain"], "count": len(a["files"]),
                       "short": fit(a["name"], LABEL_UNITS - 2) + " ▸",
                       "sub": fit(t(lang, "g_area_sub", n=len(a["files"]), plain=a["plain"]), SUB_UNITS)})
    items = {it["id"]: it for it in fmap["items"]}
    names = {a["id"]: a["name"] for a in fmap["areas"]}
    writes, reads = defaultdict(list), defaultdict(list)
    for f in fmap["flows"]:
        (writes if f["op"] == "write" else reads)[f["item"]].append(f)
    links: dict[tuple, dict] = {}
    for iid, ws in writes.items():
        for w in ws:
            for r in reads.get(iid, []):
                if w["area"] == r["area"]:
                    continue
                link = links.setdefault((w["area"], r["area"]), {"from": w["path"], "to": r["path"], "carries": []})
                if items[iid]["name"] not in link["carries"]:
                    link["carries"].append(items[iid]["name"])
    externals = {x["id"]: x for x in g["externals"]}
    owner = area_of_path(fmap)
    # a page calls its server by API path: on the map that link says which paths, like a data link says which data
    for e in g["edges"]:
        a, b = owner.get(e["from"]), owner.get(e["to"])
        if e["from"].endswith(".html") and e.get("names") and a and b and a != b:
            link = links.setdefault((a, b), {"from": e["from"], "to": e["to"], "carries": []})
            link["carries"] += [n for n in e["names"] if n not in link["carries"]]
    io = defaultdict(lambda: {"reads": [], "writes": [], "calls": []})
    for f in fmap["flows"]:
        side = io[f["area"]]["writes" if f["op"] == "write" else "reads"]
        if items[f["item"]]["name"] not in side:
            side.append(items[f["item"]]["name"])
    edges = []
    for f in fmap["flows"]:
        a, b = ("item:" + f["item"], f["path"]) if f["op"] == "read" else (f["path"], "item:" + f["item"])
        edges.append({"from": a, "to": b, "names": [], "risky": False})
    for e in g["edges"]:
        if e["to"] in externals and e["from"] in owner:
            edges.append({"from": e["from"], "to": e["to"], "names": [], "risky": False})
            label = externals[e["to"]]["label"]
            calls = io[owner[e["from"]]]["calls"]
            if label not in calls:
                calls.append(label)
    kind_label = {k: t(lang, "g_kind_" + k) for k in ("input", "file", "output", "store")}
    item_nodes = []
    for it in fmap["items"]:
        w = [{"area": names[f["area"]], "where": f"{f['path']}:{f['line']}", "code": f["snippet"]} for f in writes.get(it["id"], [])]
        r = [{"area": names[f["area"]], "where": f"{f['path']}:{f['line']}", "code": f["snippet"]} for f in reads.get(it["id"], [])]
        item_nodes.append({"id": "item:" + it["id"], "label": it["name"], "short": fit(it["name"], LABEL_UNITS),
                           "sub": fit(it["plain"] or kind_label[it["kind"]], SUB_UNITS), "role": "item", "state": "ok",
                           "badge": "", "kind": kind_label[it["kind"]], "plain": it["plain"], "writes": w, "reads": r})
    flow_areas = sorted({f["area"] for f in fmap["flows"]} | {owner[e["from"]] for e in edges
                                                              if e["from"] in owner and e["to"] in externals})
    return {"areas": groups,
            "area_links": [{"from": v["from"], "to": v["to"], "carries": v["carries"]} for v in links.values()],
            "area_io": {k: v for k, v in io.items()},
            "flow": {"items": item_nodes, "edges": edges, "areas": flow_areas}}


def area_of_path(fmap: dict) -> dict:
    return {p: a["id"] for a in fmap["areas"] for p in a["files"]}


def _norm_service(name: str) -> str:
    """"OpenAI API" → "openai", "chrome.storage" → "chromestorage"; "api" only as a word, so "rapid" stays."""
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]", "", re.sub(r"\bapi\b", "", name.lower()))


def _data_flow(g: dict, ledger: dict) -> dict:
    """The data view: files on a path from an entry to a file that reaches a data store or an outside service, and
    what each such link carries when the verified ledger's app map says so."""
    out_edges, in_edges = defaultdict(list), defaultdict(list)
    touching = set()
    for e in g["edges"]:
        if e["to"].startswith("ext:"):
            touching.add(e["from"])
        else:
            out_edges[e["from"]].append(e["to"])
            in_edges[e["to"]].append(e["from"])

    def reach(starts, step):
        seen, todo = set(starts), list(starts)
        while todo:
            for nxt in step[todo.pop()]:
                if nxt not in seen:
                    seen.add(nxt)
                    todo.append(nxt)
        return seen
    entries = [e["path"] for e in g["entries"]]
    back = reach(touching, in_edges)
    files = sorted(reach(entries, out_edges) & back) if entries else sorted(back)
    ev, mnodes = ledger.get("evidence", {}), {n["id"]: n for n in ledger.get("map", {}).get("nodes", [])}
    paths_of = lambda ids: {ev[i]["path"] for i in ids if ev.get(i, {}).get("ok") and ev[i].get("path")}  # noqa: E731
    services = {x["id"]: _norm_service(x["label"]) for x in g["externals"]}
    data_kind = {x["id"] for x in g["externals"] if x["kind"] == "data"}
    ext_edges = [(e["from"], e["to"]) for e in g["edges"] if e["to"].startswith("ext:")]
    labels = {}
    for me in ledger.get("map", {}).get("edges", []):
        target = mnodes.get(me.get("to"))
        if not target or not me.get("carries"):
            continue
        name, where = _norm_service(target.get("label", "")), paths_of(me.get("evidence", [])) | paths_of(target.get("evidence", []))
        for a, b in ext_edges:
            if a not in where:
                continue
            same_name = bool(name) and bool(services[b]) and (name in services[b] or services[b] in name)
            # a store the map names in words ("Chrome 会话存储") and the code by its API (chrome.storage): the same
            # thing when it is a store on both sides and the map's own evidence points at this file
            same_store = (target.get("kind") in ("database", "storage") and b in data_kind
                          and [y for x, y in ext_edges if x == a and y in data_kind] == [b])
            if same_name or same_store:
                labels[a + "\u0001" + b] = me["carries"]
    return {"files": files, "labels": labels}


def _diff_flag(fid: str, diff: dict | None):
    if not diff:
        return None
    return "new" if fid in diff["files"]["added"] else "changed" if fid in diff["files"]["changed"] else None


def _diff_notes(fid: str, diff: dict | None, labels: dict, lang: str) -> list[str]:
    """A file's "since the last run" lines for the panel."""
    if not diff:
        return []
    if fid in diff["files"]["added"]:
        return [t(lang, "g_diff_note_new")]
    notes = [t(lang, "g_diff_note_changed")] if fid in diff["files"]["changed"] else []
    now = [labels.get(b, b) for a, b in diff["links"]["added"] if a == fid]
    gone = [labels.get(b, b.split("/")[-1]) for a, b in diff["links"]["removed"] if a == fid]
    if now:
        notes.append(t(lang, "g_diff_note_calls", names=", ".join(now)))
    if gone:
        notes.append(t(lang, "g_diff_note_uncalls", names=", ".join(gone)))
    return notes


def _diff_summary(diff: dict, labels: dict, lang: str) -> dict:
    files, current = diff["files"], set(labels)
    quiet = not (files["added"] or files["changed"] or files["removed"] or diff["risks"]["new"] or diff["risks"]["resolved"]
                 or any(diff["promises"].values()) or diff["services"]["added"] or diff["services"]["removed"])
    return {
        "quiet": quiet,
        "title": t(lang, "g_diff_title", date=fmt_date(diff["since"])[:10] or diff["prev_run"]),
        "counts": {k: len(files[k]) for k in ("added", "changed", "removed")},
        "counts_text": t(lang, "g_diff_counts", added=len(files["added"]), changed=len(files["changed"]),
                         removed=len(files["removed"])),
        "sha_known": diff["sha_known"], "removed": files["removed"],
        "services": t(lang, "g_diff_services", added=", ".join(labels.get(x, x) for x in diff["services"]["added"]) or "—",
                      removed=", ".join(x.removeprefix("ext:") for x in diff["services"]["removed"]) or "—")
        if diff["services"]["added"] or diff["services"]["removed"] else "",
        "new_risks": diff["risks"]["new"], "resolved_risks": diff["risks"]["resolved"],
        "promises": [t(lang, "g_diff_promise", plain=p["plain"], before=GLYPH.get(p["before"], p["before"]),
                       after=GLYPH.get(p["after"], p["after"])) for p in diff["promises"]["changed"]]
        + [t(lang, "g_diff_promise_new", plain=p["plain"], status=GLYPH.get(p["status"], p["status"]))
           for p in diff["promises"]["new"]]
        + [t(lang, "g_diff_promise_gone", plain=p["plain"]) for p in diff["promises"]["gone"]],
        # links drawn in the compare view: new ones green, and gone ones dashed when both ends still exist
        "added_links": diff["links"]["added"],
        "removed_links": [l for l in diff["links"]["removed"] if l[0] in current and l[1] in current],
    }


def render_graph_tab(lang: str, function_map: bool = False) -> str:
    legend = "".join(f'<span class="vlg-legend-item k-{k}">{h(t(lang, key))}</span>'
                     for k, key in (("bad", "g_legend_bad"), ("warn", "g_legend_warn"), ("paid", "g_legend_paid"),
                                    ("folder", "g_legend_folder")))
    tools = "".join(f'<button type="button" data-act="{act}" title="{h(t(lang, key))}">{label}</button>'
                    for act, key, label in (("zoom-in", "g_zoom_in", "+"), ("zoom-out", "g_zoom_out", "−"),
                                            ("fit", "g_fit", h(t(lang, "g_fit")))))
    folder_tools = "".join(f'<button type="button" data-act="{act}" hidden>{h(t(lang, key))}</button>'
                           for act, key in (("expand-all", "g_expand_all"), ("collapse-all", "g_collapse_all"),
                                            ("compare", "g_compare")))
    # with a function map: one layered map (areas that open into their files) and the data view; else the folder views
    choices = ((("map", "g_mode_map"), ("data", "g_mode_flow")) if function_map else
               (("files", "g_mode_files"), ("modules", "g_mode_modules"), ("data", "g_mode_data")))
    on = ' class="on"'  # no backslash inside an f-string expression: Python before 3.12 rejects it
    modes = "".join(f'<button type="button" data-mode="{m}"{on if i == 0 else ""}>{h(t(lang, key))}</button>'
                    for i, (m, key) in enumerate(choices))
    export = (f'<button type="button" data-act="export">{h(t(lang, "g_export"))}</button>'
              '<div class="vlg-export-menu" hidden>'
              f'<button type="button" data-fmt="png">{h(t(lang, "g_export_png"))}</button>'
              f'<button type="button" data-fmt="svg">{h(t(lang, "g_export_svg"))}</button></div>')
    return (f'<div class="vlg" id="vlg"><a class="vlg-skip" href="#vlg-panel">{h(t(lang, "g_skip"))}</a>'
            '<div class="vlg-canvas" id="vlg-canvas">'
            '<svg id="vlg-svg" xmlns="http://www.w3.org/2000/svg" role="img"><g id="vlg-viewport"></g></svg>'
            f'<div class="vlg-modes">{modes}</div>'
            f'<div class="vlg-tools">{tools}{folder_tools}{export}</div><div class="vlg-legend">{legend}</div></div>'
            '<aside class="vlg-panel" id="vlg-panel" tabindex="-1" aria-live="polite"></aside></div>')
