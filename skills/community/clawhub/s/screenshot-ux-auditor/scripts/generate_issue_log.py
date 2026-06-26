#!/usr/bin/env python3
"""Turn a JSON list of issues into a compact CSV/Markdown issue log."""
import argparse, json, csv, sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issues_json", help="JSON file with [{title,category,severity,fix}]")
    ap.add_argument("--csv-out", default="issue_log.csv")
    args = ap.parse_args()
    issues = json.load(open(args.issues_json, "r", encoding="utf-8"))
    with open(args.csv_out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["title","category","severity","fix"])
        w.writeheader()
        for issue in issues:
            w.writerow({k: issue.get(k, "") for k in w.fieldnames})
    print(f"Wrote {len(issues)} issues to {args.csv_out}")

if __name__ == "__main__":
    main()
