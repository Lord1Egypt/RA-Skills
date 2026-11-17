"""Compare a verified ledger with a fixture's answer key.

    python3 tests/e2e/score.py --verified <run>/ledger.verified.json --answers tests/fixtures/answers/<name>.json \
        [--graph <run>/graph.json [--explained <run>/explain.verified.json]]"""
from __future__ import annotations

import argparse
import json
import sys


def _text(item: dict) -> str:
    return " ".join(str(item.get(k, "")) for k in ("plain", "verdict_plain", "verdict_dev", "bypassed")).lower()


def _paths(item: dict, evidence: dict, keys=("evidence",)) -> list[str]:
    out = []
    for key in keys:
        for i in item.get(key, []):
            e = evidence.get(i, {})
            if e.get("ok") and e.get("kind") in ("code", "probe"):
                out.append(str(e.get("path", "")))
    return out


def score(verified: dict, answers: dict) -> list[tuple[bool, str]]:
    ev = verified["evidence"]
    results = []
    for want in answers.get("must_find", []):
        hit = any(p["status"] in want["status"]
                  and any(any(w in path for w in want["paths_any"]) for path in _paths(p, ev))
                  and any(w.lower() in _text(p) for w in want["text_any"])
                  for p in verified["promises"])
        results.append((hit, f"must find: {want['label']}"))
    for want in answers.get("must_find_compromises", []):
        hit = any(c.get("still_present") is want["still_present"]
                  and any(w.lower() in _text(c) for w in want["text_any"])
                  for c in verified["compromises"])
        results.append((hit, f"must find compromise: {want['label']}"))
    if answers.get("clean") is True:
        broken = [p["plain"] for p in verified["promises"] if p["status"] == "broken"]
        still = [c["bypassed"] for c in verified["compromises"] if c.get("still_present") is True]
        results.append((not broken and not still, f"clean app: no broken promise ({broken}) and no live compromise ({still})"))
    drawn = {n["id"] for n in verified["map"]["nodes"]}
    unverified = {n["id"] for n in verified["map"].get("unverified_nodes", [])}
    results.append((not (drawn & unverified), "no unverified node is drawn"))
    return results


def score_graph(g: dict, want: dict) -> list[tuple[bool, str]]:
    ids = {n["id"] for n in g["nodes"]}
    ext = {x["id"] for x in g["externals"]}
    entries = {e["path"] for e in g["entries"]}
    edges = {(e["from"], e["to"]) for e in g["edges"]}
    missing = [e for e in want["edges"] if tuple(e) not in edges]
    return [(ids == set(want["nodes"]), f"file nodes: want {sorted(want['nodes'])}, got {sorted(ids)}"),
            (entries == set(want["entries"]), f"entries: want {sorted(want['entries'])}, got {sorted(entries)}"),
            (ext == set(want["externals"]), f"outside services: want {sorted(want['externals'])}, got {sorted(ext)}"),
            (not missing, f"links present (missing: {missing})")]


def score_explain(explained: dict, g: dict, want: list) -> list[tuple[bool, str]]:
    chosen = {n["id"] for n in g["nodes"] if n.get("explain")}
    kept = explained["files"]
    v = explained["verification"]
    results = [(chosen <= set(kept), f"every chosen file is explained (missing: {sorted(chosen - set(kept))})"),
               (not explained["rejected"], f"no explanation rejected ({[r['path'] for r in explained['rejected']]})"),
               (v["functions_dropped"] == 0, f"no invented function names ({v['functions_dropped']} dropped)"),
               (v["unverified_purposes"] == 0, f"purposes name only real identifiers ({v['unverified_purposes']} unverified)")]
    for w in want:
        entry = kept.get(w["path"], {})
        text = f"{entry.get('purpose_plain', '')} {entry.get('purpose_dev', '')}".lower()
        results.append((any(t.lower() in text for t in w["text_any"]), f"explains {w['path']}: {w['label']}"))
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verified", required=True)
    ap.add_argument("--answers", required=True)
    ap.add_argument("--graph", help="<run>/graph.json: also score the file graph")
    ap.add_argument("--explained", help="<run>/explain.verified.json: also score the explanations (needs --graph)")
    args = ap.parse_args()
    with open(args.verified, encoding="utf-8") as fh:
        verified = json.load(fh)
    with open(args.answers, encoding="utf-8") as fh:
        answers = json.load(fh)
    results = score(verified, answers)
    if args.graph:
        with open(args.graph, encoding="utf-8") as fh:
            g = json.load(fh)
        results += score_graph(g, answers["graph"])
        if args.explained:
            with open(args.explained, encoding="utf-8") as fh:
                results += score_explain(json.load(fh), g, answers.get("explain", []))
    for ok, label in results:
        print(("PASS " if ok else "FAIL ") + label)
    return 0 if all(ok for ok, _ in results) else 1


if __name__ == "__main__":
    sys.exit(main())
