#!/usr/bin/env python3
import argparse, json
from decimal import Decimal

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("line_items_json", help="JSON list with item, qty, rate")
    ap.add_argument("--tax", type=float, default=0.0)
    ap.add_argument("--discount", type=float, default=0.0)
    ap.add_argument("--out", default="quote.json")
    args = ap.parse_args()
    items = json.load(open(args.line_items_json, "r", encoding="utf-8"))
    subtotal = sum((item.get("qty",1) * item.get("rate",0) for item in items), 0)
    total = subtotal * (1 + args.tax/100.0) * (1 - args.discount/100.0)
    payload = {"items": items, "subtotal": round(subtotal,2), "tax_pct": args.tax, "discount_pct": args.discount, "total": round(total,2)}
    json.dump(payload, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
