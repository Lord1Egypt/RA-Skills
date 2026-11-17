#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WideHive Stage 4 - programmatic merge & validation (zero LLM).

Usage:
  python merge_results.py --run-dir <run_dir> [--required-fields f1,f2] [--max-field-len 4000]

Inputs:
  <run_dir>/plan.json     {"scenario": ..., "fields": [...], ...}
  <run_dir>/targets.json  [{"slug": ..., "name": ..., "url": ...}, ...]
  <run_dir>/result/*.json one file per object (written by workers)

Outputs:
  <run_dir>/merged.json   merged full records
  <run_dir>/merged.csv    flattened table (UTF-8-SIG, opens directly in Excel)
  stdout: JSON verdict report
          {total_targets, with_results, ok, missing_files, defects, verdict}

verdict: PASS        = every object has a result and no defects
        NEEDS_RETRY  = missing/defective objects, send them back to the retry queue
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

URL_RE = re.compile(r"^https?://\S+$", re.I)


def main():
    ap = argparse.ArgumentParser(description="WideHive merge & validate")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--required-fields", default=None,
                    help="comma-separated field names; defaults to plan.json fields")
    ap.add_argument("--max-field-len", type=int, default=4000)
    args = ap.parse_args()

    run = Path(args.run_dir)
    if not run.is_dir():
        print(json.dumps({"error": f"run dir not found: {run}"}, ensure_ascii=False))
        sys.exit(1)

    plan = json.loads((run / "plan.json").read_text(encoding="utf-8"))
    targets = json.loads((run / "targets.json").read_text(encoding="utf-8"))
    if args.required_fields:
        fields = [f.strip() for f in args.required_fields.split(",") if f.strip()]
    else:
        fields = plan.get("fields", [])
    scenario = plan.get("scenario", "custom")

    result_dir = run / "result"
    defects, rows, records, missing = [], [], [], []

    for t in targets:
        slug = t.get("slug", "")
        if not slug:
            defects.append({"slug": "?", "issues": ["target_without_slug"]})
            continue
        f = result_dir / f"{slug}.json"
        if not f.exists():
            missing.append(slug)
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            defects.append({"slug": slug, "issues": [f"json_parse_error: {e}"]})
            continue

        issues = []
        fd = data.get("fields") if isinstance(data.get("fields"), dict) else {}
        if data.get("error"):
            issues.append(f"worker_error: {data.get('error')}")
        for k in fields:
            v = fd.get(k)
            if v is None or (isinstance(v, str) and not v.strip()):
                issues.append(f"missing_field: {k}")
            elif isinstance(v, str) and len(v) > args.max_field_len:
                issues.append(f"field_too_long: {k} ({len(v)} chars)")
        for s in data.get("sources") or []:
            u = s.get("url") if isinstance(s, dict) else None
            if u and not URL_RE.match(str(u)):
                issues.append(f"bad_source_url: {u}")
        if issues:
            defects.append({"slug": slug, "issues": issues})

        row = {"slug": slug,
               "name": t.get("name", data.get("target", "")),
               "scenario": scenario}
        for k in fields:
            v = fd.get(k)
            if isinstance(v, (list, dict)):
                row[k] = json.dumps(v, ensure_ascii=False)
            else:
                row[k] = "" if v is None else v
        row["n_sources"] = len(data.get("sources") or [])
        rows.append(row)
        records.append(data)

    out_json = run / "merged.json"
    out_csv = run / "merged.csv"
    out_json.write_text(
        json.dumps({"scenario": scenario, "fields": fields, "records": records},
                   ensure_ascii=False, indent=2),
        encoding="utf-8")
    if rows:
        cols = ["slug", "name", "scenario"] + fields + ["n_sources"]
        with out_csv.open("w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            for r in rows:
                w.writerow(r)

    report = {
        "total_targets": len(targets),
        "with_results": len(rows),
        "ok": len(rows) - len(defects),
        "missing_files": missing,
        "defects": defects,
        "merged_csv": str(out_csv) if rows else None,
        "merged_json": str(out_json),
        "verdict": ("PASS" if rows and not defects and not missing else "NEEDS_RETRY"),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
