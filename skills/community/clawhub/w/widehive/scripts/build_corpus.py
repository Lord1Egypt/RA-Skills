#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WideHive corpus builder - consolidate finished runs into a queryable corpus.

Usage:
  python build_corpus.py --runs-root <dir> [--out <corpus_dir>]
  python build_corpus.py --runs <dir1,dir2,...> [--out <corpus_dir>]

A run dir = any directory containing plan.json (+ result/*.json).
Output (default ./corpus):
  corpus.jsonl       one JSON record per object per run (rewrite on each build)
  corpus-index.json  {"generated_at", "runs": [...], "objects", "by_slug": {...}}

Query rules live in SKILL.md ("Corpus"): answer strictly from the corpus, cite
run_id + fetched_at, disclose staleness, propose targeted re-runs for gaps.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def discover_runs(runs_root: Path):
    if not runs_root.is_dir():
        return []
    return sorted(p for p in runs_root.iterdir() if p.is_dir() and (p / "plan.json").is_file())


def main():
    ap = argparse.ArgumentParser(description="WideHive corpus builder")
    ap.add_argument("--runs-root", default=None, help="dir whose subdirs are run dirs")
    ap.add_argument("--runs", default=None, help="comma-separated explicit run dirs")
    ap.add_argument("--out", default="corpus", help="corpus output dir (default ./corpus)")
    args = ap.parse_args()

    runs = []
    if args.runs_root:
        runs = discover_runs(Path(args.runs_root))
    elif args.runs:
        runs = [Path(p.strip()) for p in args.runs.split(",") if p.strip()]
    if not runs:
        print(json.dumps({"error": "no run dirs found (need --runs-root or --runs)"},
                         ensure_ascii=False))
        sys.exit(1)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    records = []
    runs_meta = []
    by_slug = {}
    for run in runs:
        try:
            plan = json.loads((run / "plan.json").read_text(encoding="utf-8"))
        except Exception:
            continue
        scenario = plan.get("scenario", "custom")
        run_id = plan.get("run_id", run.name)
        result_dir = run / "result"
        n_objects = 0
        latest = ""
        if result_dir.is_dir():
            for f in sorted(result_dir.glob("*.json")):
                try:
                    rec = json.loads(f.read_text(encoding="utf-8"))
                except Exception:
                    continue
                slug = f.stem
                fetched = rec.get("fetched_at", "")
                latest = max(latest, fetched)
                n_objects += 1
                records.append({
                    "run_id": run_id,
                    "run_dir": str(run),
                    "scenario": scenario,
                    "slug": slug,
                    "target": rec.get("target", slug),
                    "fields": rec.get("fields", {}),
                    "sources": rec.get("sources", []),
                    "fetched_at": fetched,
                })
                ent = by_slug.setdefault(slug, {"runs": [], "latest_fetched_at": ""})
                if run_id not in ent["runs"]:
                    ent["runs"].append(run_id)
                ent["latest_fetched_at"] = max(ent["latest_fetched_at"], fetched)
        runs_meta.append({"run_id": run_id, "run_dir": str(run), "scenario": scenario,
                          "objects": n_objects, "latest_fetched_at": latest})

    corpus_path = out_dir / "corpus.jsonl"
    with corpus_path.open("w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    index = {"generated_at": now, "runs": runs_meta,
             "objects": len(records), "by_slug": by_slug}
    (out_dir / "corpus-index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"corpus": str(corpus_path), "index": str(out_dir / "corpus-index.json"),
                      "runs": len(runs_meta), "records": len(records)},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
