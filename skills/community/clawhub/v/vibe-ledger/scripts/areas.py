"""The function map: what the project is made of (areas) and what moves between the parts (data flows).

The model names 2–10 areas — "配音", "渲染", "交付检查" — each with a one-line purpose and the files it covers
(folders, globs or exact paths). The script assigns EVERY file in the graph to the first area that claims it, so
an area's files are a fact, not a claim; files no area claims are shown as "other", never hidden.

Data flows say which area reads or writes which piece of data (`storyboard.json`, `out.mp4`, the trip plan).
Each flow carries one line of code: the line must be in the project as written, belong to a file of that area,
and name the data (one of the item's `match` spellings). Outside services come from the import graph, not from
the model."""
from __future__ import annotations

import fnmatch
import re
from collections import defaultdict
from pathlib import Path

from common import read_text

MIN_AREAS, MAX_AREAS = 2, 10
OPS = ("read", "write")
ITEM_KINDS = ("input", "file", "output", "store")
OTHER = "__other"
# a quoted name of a data file, e.g. "storyboard.json", 'out.mp4', f"{stem}.ics"
DATA_NAME = re.compile(r"""["'`]([\w{}$.\-/]*?\.(?:json|jsonl|mp4|mov|mp3|wav|m4a|srt|vtt|ics|html|csv|tsv|xlsx|pdf|png|jpg|jpeg|svg|md|txt|db|sqlite|yaml|yml|pptx|docx))["'`]""", re.I)
IO_HINT = re.compile(r"\b(open|read|write|load|dump|save|json\.|Path|exists|unlink|mkdir|ffmpeg|render|out_dir|readFile|writeFile|fetch)\w*", re.I)
CANDIDATE_MAX = 120


class AreasError(Exception):
    pass


def problems(doc: dict) -> list[str]:
    """Format problems in explain.json's `areas`, `items` and `flows` (all optional)."""
    p: list[str] = []
    areas = doc.get("areas")
    if areas is None:
        if doc.get("items") or doc.get("flows"):
            p.append("items/flows: need `areas` (a flow says which area reads or writes the data)")
        return p
    if not isinstance(areas, list):
        return ["areas: must be a list"]
    if not MIN_AREAS <= len(areas) <= MAX_AREAS:
        p.append(f"areas: write {MIN_AREAS}–{MAX_AREAS} areas, not {len(areas)}")
    ids = set()
    for a in areas:
        if not isinstance(a, dict):
            p.append("areas: every area must be an object")
            continue
        where = f"area {a.get('id')}"
        if not isinstance(a.get("id"), str) or not a["id"].strip() or a["id"] in ids or a["id"] == OTHER:
            p.append(f"{where}: id missing or duplicated")
        ids.add(a.get("id"))
        for f in ("name", "plain"):
            if not isinstance(a.get(f), str) or not a[f].strip():
                p.append(f"{where}: missing {f}")
        m = a.get("match")
        if not isinstance(m, list) or not m or any(not isinstance(x, str) or not x.strip() for x in m):
            p.append(f"{where}: match must list at least one folder (ending in /), glob or file path")
    items = doc.get("items", [])
    iids = set()
    if not isinstance(items, list):
        p.append("items: must be a list")
        items = []
    for it in items:
        if not isinstance(it, dict):
            p.append("items: every item must be an object")
            continue
        where = f"item {it.get('id')}"
        if not isinstance(it.get("id"), str) or not it["id"].strip() or it["id"] in iids:
            p.append(f"{where}: id missing or duplicated")
        iids.add(it.get("id"))
        if not isinstance(it.get("name"), str) or not it["name"].strip():
            p.append(f"{where}: missing name")
        if it.get("kind", "file") not in ITEM_KINDS:
            p.append(f"{where}: kind must be one of {', '.join(ITEM_KINDS)}")
        m = it.get("match", [])
        if not isinstance(m, list) or any(not isinstance(x, str) for x in m):
            p.append(f"{where}: match must be a list of text")
    flows = doc.get("flows", [])
    if not isinstance(flows, list):
        return p + ["flows: must be a list"]
    for k, fl in enumerate(flows, 1):
        where = f"flow #{k}"
        if not isinstance(fl, dict):
            p.append(f"{where}: must be an object")
            continue
        if fl.get("area") not in ids:
            p.append(f"{where}: unknown area {fl.get('area')}")
        if fl.get("item") not in iids:
            p.append(f"{where}: unknown item {fl.get('item')}")
        if fl.get("op") not in OPS:
            p.append(f"{where}: op must be one of {', '.join(OPS)}")
        if not isinstance(fl.get("path"), str) or not isinstance(fl.get("line"), int) or not isinstance(fl.get("snippet"), str):
            p.append(f"{where}: needs path, line (an integer) and snippet — the line that reads or writes it")
    return p


def _matches(pattern: str, path: str) -> bool:
    pattern = pattern.strip()
    if pattern in ("", ".", "./", "*", "**"):
        return True
    if pattern.startswith("./"):  # only the "./" prefix: ".remotion/" is a real folder name
        pattern = pattern[2:]
    if pattern.endswith("/"):
        return path.startswith(pattern)
    if any(c in pattern for c in "*?["):
        return fnmatch.fnmatchcase(path, pattern)
    return path == pattern


def assign(areas: list[dict], paths: list[str]) -> tuple[dict[str, str], dict[str, list[str]]]:
    """Every path to the first area whose match claims it (OTHER when none does); and the patterns matching nothing."""
    owner: dict[str, str] = {}
    unmatched: dict[str, list[str]] = defaultdict(list)
    for a in areas:
        for pat in a["match"]:
            hit = [p for p in paths if _matches(pat, p)]
            if not hit:
                unmatched[a["id"]].append(pat)
            for p in hit:
                owner.setdefault(p, a["id"])
    for p in paths:
        owner.setdefault(p, OTHER)
    return owner, dict(unmatched)


def verify(doc: dict, g: dict, root) -> dict | None:
    """The checked function map, or None when explain.json has no areas."""
    if not doc.get("areas"):
        return None
    from verify import check_code
    root = Path(root).resolve()
    paths = sorted(n["id"] for n in g["nodes"])
    owner, unmatched = assign(doc["areas"], paths)
    files = defaultdict(list)
    for p, a in owner.items():
        files[a].append(p)
    areas, dropped_areas = [], []
    for a in doc["areas"]:
        if not files.get(a["id"]):
            dropped_areas.append({"id": a["id"], "name": a["name"],
                                  "reason": "it claims no file (every file it matches went to an area listed earlier)"
                                  if not unmatched.get(a["id"]) or len(unmatched[a["id"]]) < len(a["match"])
                                  else "none of its folders, globs or paths matches a file in the graph"})
            continue
        areas.append({"id": a["id"], "name": a["name"], "plain": a["plain"], "files": sorted(files[a["id"]]),
                      "unmatched": unmatched.get(a["id"], [])})
    kept_ids = {a["id"] for a in areas}
    other = sorted(p for p, a in owner.items() if a not in kept_ids)
    items = {it["id"]: {"id": it["id"], "name": it["name"], "plain": it.get("plain", ""), "kind": it.get("kind", "file"),
                        "match": [m for m in it.get("match", []) if m.strip()] or [it["name"]]}
             for it in doc.get("items", [])}
    flows, rejected = [], []
    for fl in doc.get("flows", []):
        it = items.get(fl["item"])
        res = check_code({"path": fl["path"], "line": fl["line"], "snippet": fl["snippet"]}, root)
        reason = None
        if fl["area"] not in kept_ids:
            reason = f"area {fl['area']} was dropped"
        elif not res.get("ok"):
            reason = res.get("reason", "the line could not be checked")
        elif owner.get(res["path"]) != fl["area"]:
            where = owner.get(res["path"])
            reason = (f"{res['path']} belongs to area {where}, not {fl['area']}" if where and where != OTHER
                      else f"{res['path']} is not a file of area {fl['area']}")
        elif not any(m.lower() in fl["snippet"].lower() for m in it["match"]):
            reason = f"the line does not name {it['name']} (looked for: {', '.join(it['match'])})"
        if reason:
            rejected.append({**fl, "reason": reason})
            continue
        flows.append({"area": fl["area"], "item": fl["item"], "op": fl["op"], "path": res["path"], "line": res["line"],
                      "snippet": fl["snippet"]})
    used = {f["item"] for f in flows}
    out_items = [it for iid, it in items.items() if iid in used]
    dropped_items = [{"id": iid, "name": it["name"], "reason": "no flow for it passed the checks"}
                     for iid, it in items.items() if iid not in used]
    return {"areas": areas, "other": other, "items": out_items, "flows": flows, "rejected_flows": rejected,
            "dropped_areas": dropped_areas, "dropped_items": dropped_items}


def summary_lines(m: dict | None) -> list[str]:
    if m is None:
        return ["Function map: none (explain.json has no `areas`; the flowchart falls back to folders)"]
    lines = [f"Function map: {len(m['areas'])} areas, {sum(len(a['files']) for a in m['areas'])} files in them, "
             f"{len(m['other'])} in no area; {len(m['items'])} data items, {len(m['flows'])} flows kept, "
             f"{len(m['rejected_flows'])} rejected"]
    for a in m["areas"]:
        lines.append(f"  - {a['name']}: {len(a['files'])} files" + (f" (matched nothing: {', '.join(a['unmatched'])})"
                                                                   if a["unmatched"] else ""))
    lines += [f"  ✗ area {d['name']}: {d['reason']}" for d in m["dropped_areas"]]
    lines += [f"  ✗ flow {r['area']} {r['op']} {r['item']} ({r['path']}:{r['line']}): {r['reason']}" for r in m["rejected_flows"]]
    lines += [f"  ✗ item {d['name']}: {d['reason']}" for d in m["dropped_items"]]
    if m["other"]:
        lines.append(f"  files in no area (shown as “other”): {', '.join(m['other'][:12])}" + (" …" if len(m["other"]) > 12 else ""))
    return lines


def data_candidates(g: dict, root) -> list[dict]:
    """Lines that name a data file next to a read/write word: hints for the flows, ranked by how many files name it."""
    root = Path(root)
    seen: dict[str, list[dict]] = defaultdict(list)
    for n in sorted(g["nodes"], key=lambda n: n["id"]):
        try:
            lines = read_text(root / n["id"]).splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            if len(line) > 300 or not IO_HINT.search(line):
                continue
            for m in DATA_NAME.finditer(line):
                name = m.group(1).rsplit("/", 1)[-1]
                if len(seen[name]) < 6:
                    seen[name].append({"path": n["id"], "line": i, "text": line.strip()[:160]})
    ranked = sorted(seen.items(), key=lambda kv: (-len({h["path"] for h in kv[1]}), kv[0]))
    return [{"name": k, "hits": v} for k, v in ranked[:CANDIDATE_MAX]]


def pack_section(g: dict, root) -> str:
    """The part of explain_pack.md the function map is written from: every file by folder, and data candidates."""
    by_folder = defaultdict(list)
    for n in sorted(g["nodes"], key=lambda n: n["id"]):
        folder, _, name = n["id"].rpartition("/")
        by_folder[folder or "."].append(name)
    out = ["## Function map (areas, items, flows)", "",
           "Write `areas`, `items` and `flows` once, in explain.json (with groups: once the parts are merged) — "
           "references/explain-guide.md section 4. Every file below is assigned to the first area that matches it.", "",
           "### All files, by folder", ""]
    for folder, names in sorted(by_folder.items()):
        out.append(f"- `{folder}/` ({len(names)}): " + ", ".join(names[:60]) + (" …" if len(names) > 60 else ""))
    cands = data_candidates(g, root)
    out += ["", "### Data the code names (hints for `items` and `flows`; copy a line exactly as a flow's snippet)", ""]
    if not cands:
        out.append("_No line names a data file next to a read/write word._")
    for c in cands:
        out.append(f"- **{c['name']}**")
        out += [f"  - {h['path']}:{h['line']} `{h['text']}`" for h in c["hits"]]
    return "\n".join(out) + "\n"
