#!/usr/bin/env python3
import argparse, json

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="weekly_review.json")
    args = ap.parse_args()
    payload = {"wins": [], "misses": [], "metrics": {}, "blockers": [], "decisions": [], "next_week_top3": []}
    json.dump(payload, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
