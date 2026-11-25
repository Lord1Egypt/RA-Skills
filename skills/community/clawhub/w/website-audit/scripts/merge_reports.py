#!/usr/bin/env python3
"""Merge the JSON output of the other scripts into one summary with computed counts.

Usage: python merge_reports.py out1.json out2.json ... [> merged.json]

Why this exists: counts, groupings and cross-page comparisons (duplicate titles, issues
affecting N pages) are computed here by code, so the written report quotes numbers instead
of estimating them.
"""
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _http import emit, make_issue, now_iso  # noqa: E402

ORDER = ["critical", "high", "medium", "low"]


def where(d):
    return ((d.get("page") or {}).get("final_url") or d.get("final_url") or d.get("target") or "unknown")


def main():
    paths = sys.argv[1:]
    if not paths:
        print(__doc__)
        sys.exit(2)
    reports, load_errors = [], []
    for pth in paths:
        try:
            with open(pth, encoding="utf-8") as f:
                reports.append((pth, json.load(f)))
        except (OSError, ValueError) as e:
            load_errors.append({"file": pth, "error": str(e)})

    groups = {}
    not_checked, coverage, caveats = [], defaultdict(list), []
    dup = {"title": defaultdict(list), "meta_description": defaultdict(list), "h1": defaultdict(list)}

    for pth, d in reports:
        tool = d.get("tool", "unknown")
        w = where(d)
        coverage[tool].append(w)
        if d.get("status") == "not_checked" or (d.get("errors") and "issues" not in d):
            not_checked.append({"tool": tool, "where": w, "errors": d.get("errors")})
            continue
        for c in d.get("caveats", []):
            if c not in caveats:
                caveats.append(c)
        for i in d.get("issues", []):
            g = groups.setdefault(i["id"], {"id": i["id"], "category": i["category"],
                                            "severity_hint": i["severity_hint"], "message": i["message"],
                                            "confidence": set(), "affected": []})
            g["confidence"].add(i.get("confidence", "verified"))
            g["affected"].append({"where": w, "tool": tool, "count": i.get("count"),
                                  "evidence": i.get("evidence"), "examples": i.get("examples")})
        if tool == "check_html":
            seo = (d.get("measurements") or {}).get("seo") or {}
            if seo.get("title"):
                dup["title"][seo["title"]].append(w)
            if seo.get("meta_description"):
                dup["meta_description"][seo["meta_description"]].append(w)
            for h in seo.get("h1") or []:
                dup["h1"][h].append(w)

    extra = []
    sev = {"title": "medium", "meta_description": "medium", "h1": "low"}
    for field, table in dup.items():
        rep = {v: urls for v, urls in table.items() if len(set(urls)) > 1}
        if rep:
            urls_total = sum(len(set(u)) for u in rep.values())
            extra.append(make_issue("%s.duplicate" % field, "seo", sev[field],
                                    "The same %s is used on more than one audited page." % field.replace("_", " "),
                                    count=urls_total,
                                    evidence=[{"value": v, "pages": sorted(set(u))} for v, u in rep.items()]))
    for i in extra:
        groups[i["id"]] = {"id": i["id"], "category": i["category"], "severity_hint": i["severity_hint"],
                           "message": i["message"], "confidence": {"verified"},
                           "affected": [{"where": "multiple pages", "tool": "merge_reports",
                                         "count": i["count"], "evidence": i["evidence"], "examples": None}]}

    merged = []
    for g in groups.values():
        g["confidence"] = sorted(g["confidence"])
        g["pages_affected"] = len({a["where"] for a in g["affected"]})
        merged.append(g)
    merged.sort(key=lambda g: (ORDER.index(g["severity_hint"]) if g["severity_hint"] in ORDER else 9,
                               -g["pages_affected"], g["id"]))
    by_sev = {s: sum(1 for g in merged if g["severity_hint"] == s) for s in ORDER}
    by_cat = defaultdict(int)
    for g in merged:
        by_cat[g["category"]] += 1

    emit({"tool": "merge_reports", "merged_at": now_iso(), "inputs": [p for p, _ in reports],
          "input_load_errors": load_errors,
          "summary": {"distinct_issues": len(merged), "distinct_issues_by_severity_hint": by_sev,
                      "distinct_issues_by_category": dict(by_cat),
                      "note": "Counts are distinct issue types, not instances. See each issue's pages_affected and count."},
          "coverage": {t: sorted(set(w)) for t, w in coverage.items()},
          "not_checked": not_checked, "issues": merged, "caveats": caveats})


if __name__ == "__main__":
    main()
