#!/usr/bin/env python3
import argparse, csv, json, re
from decimal import Decimal

CATEGORY_HINTS = {
    "uber":"Travel","flight":"Travel","hotel":"Travel","taxi":"Travel",
    "lunch":"Meals","dinner":"Meals","coffee":"Meals",
    "adobe":"Software","notion":"Software","figma":"Software",
    "office":"Office","paper":"Office","printer":"Office",
}

def categorize(text):
    low = text.lower()
    for key, cat in CATEGORY_HINTS.items():
        if key in low:
            return cat
    return "Other"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items_json", help="JSON list with vendor/date/amount/description")
    ap.add_argument("--out", default="expense_ledger.csv")
    args = ap.parse_args()
    items = json.load(open(args.items_json, "r", encoding="utf-8"))
    fields = ["vendor","date","amount","currency","description","category","flag"]
    with open(args.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for item in items:
            desc = item.get("description","")
            amt = str(item.get("amount",""))
            flag = "check" if not amt else ""
            w.writerow({
                "vendor": item.get("vendor",""),
                "date": item.get("date",""),
                "amount": amt,
                "currency": item.get("currency",""),
                "description": desc,
                "category": item.get("category") or categorize(desc + " " + item.get("vendor","")),
                "flag": flag
            })
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
