#!/usr/bin/env python3
import argparse, csv, json

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("records_json", help="JSON list of paper records")
    ap.add_argument("--out", default="literature_matrix.csv")
    args = ap.parse_args()
    rows = json.load(open(args.records_json, "r", encoding="utf-8"))
    fields = ["citation","problem","method","data","metric","key_result","limitation","gap"]
    with open(args.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
