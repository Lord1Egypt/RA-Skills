#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WideHive Watch - diff a current run against a baseline run (zero LLM).

Usage:
  python diff_results.py --baseline <prev_run_dir> --current <cur_run_dir> \
      [--compare-fields f1,f2] [--out <watch-report.json>]

Reads:
  <run_dir>/result/<slug>.json   per-object worker results
  <current>/plan.json            field template (default compare fields)

Writes:
  watch-report.json (default: <current>/watch-report.json):
  {
    "summary": {"new": n, "removed": n, "changed": n, "unchanged": n},
    "changes": [{"slug": ..., "status": "new|removed|changed",
                 "changed_fields": [{"field": ..., "old": ..., "new": ...}]}]
  }

Interpretation:
  - new/changed > 0  -> fan out workers ONLY for those slugs, carry unchanged
                        results forward, then merge as usual.
  - all unchanged    -> skip fan-out entirely; emit a no-change note.
Exit code is always 0; the JSON report is the interface.
"""
import argparse
import json
import sys
from pathlib import Path


def canon(v):
    if isinstance(v, str):
        return v.strip()
    return v


def load_results(run: Path):
    out = {}
    rd = run / "result"
    if rd.is_dir():
        for f in sorted(rd.glob("*.json")):
            try:
                out[f.stem] = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                out[f.stem] = {"__error__": "unparseable"}
    return out


def main():
    ap = argparse.ArgumentParser(description="WideHive watch diff & validate")
    ap.add_argument("--baseline", required=True, help="previous run dir")
    ap.add_argument("--current", required=True, help="current run dir")
    ap.add_argument("--compare-fields", default=None,
                    help="comma-separated field names; defaults to current plan.json fields")
    ap.add_argument("--out", default=None, help="report path (default <current>/watch-report.json)")
    args = ap.parse_args()

    bdir, cdir = Path(args.baseline), Path(args.current)
    for label, p in (("baseline", bdir), ("current", cdir)):
        if not (p / "plan.json").is_file():
            print(json.dumps({"error": f"{label} run dir invalid (plan.json missing): {p}"},
                             ensure_ascii=False))
            sys.exit(1)

    plan = json.loads((cdir / "plan.json").read_text(encoding="utf-8"))
    if args.compare_fields:
        fields = [f.strip() for f in args.compare_fields.split(",") if f.strip()]
    else:
        fields = plan.get("fields", [])

    base = load_results(bdir)
    cur = load_results(cdir)
    counts = {"new": 0, "removed": 0, "changed": 0, "unchanged": 0}
    changes = []

    def subset(rec):
        fd = rec.get("fields") if isinstance(rec.get("fields"), dict) else {}
        return {k: canon(fd.get(k)) for k in fields}

    def dumps(v):
        return json.dumps(v, sort_keys=True, ensure_ascii=False, default=str)

    for slug in sorted(set(base) | set(cur)):
        if slug not in base:
            counts["new"] += 1
            changes.append({"slug": slug, "status": "new", "changed_fields": []})
        elif slug not in cur:
            counts["removed"] += 1
            changes.append({"slug": slug, "status": "removed", "changed_fields": []})
        elif "__error__" in base[slug] or "__error__" in cur[slug]:
            counts["changed"] += 1
            changes.append({"slug": slug, "status": "changed",
                            "changed_fields": [{"field": "__file__",
                                                "old": base[slug].get("__error__", "ok"),
                                                "new": cur[slug].get("__error__", "ok")}]})
        else:
            b, c = subset(base[slug]), subset(cur[slug])
            diff = [{"field": k, "old": b.get(k), "new": c.get(k)}
                    for k in fields if dumps(b.get(k)) != dumps(c.get(k))]
            if diff:
                counts["changed"] += 1
                changes.append({"slug": slug, "status": "changed", "changed_fields": diff})
            else:
                counts["unchanged"] += 1

    out_path = Path(args.out) if args.out else cdir / "watch-report.json"
    report = {"baseline": str(bdir), "current": str(cdir),
              "compare_fields": fields, "summary": counts, "changes": changes}
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    action = ("fan out new+changed only; carry unchanged forward"
              if counts["new"] or counts["changed"] else
              "no changes - skip fan-out, emit no-change note")
    print(json.dumps({"summary": counts, "report": str(out_path), "action_hint": action},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
