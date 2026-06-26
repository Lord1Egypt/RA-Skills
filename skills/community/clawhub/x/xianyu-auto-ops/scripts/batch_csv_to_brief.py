#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path

FIELDS = [
    "sku", "name", "category", "brand", "condition", "price_target",
    "flaws", "accessories", "city", "delivery", "notes"
]

ALIASES = {
    "sku": ["sku", "id", "编号"],
    "name": ["name", "product", "title", "商品名", "名称"],
    "category": ["category", "类目", "分类"],
    "brand": ["brand", "品牌"],
    "condition": ["condition", "成色", "状态"],
    "price_target": ["price_target", "price", "价格", "目标价"],
    "flaws": ["flaws", "defects", "瑕疵"],
    "accessories": ["accessories", "bundle", "配件"],
    "city": ["city", "location", "城市"],
    "delivery": ["delivery", "shipping", "发货", "交付"],
    "notes": ["notes", "备注", "说明"],
}


def normalize_key(key: str) -> str:
    k = key.strip().lower()
    for target, aliases in ALIASES.items():
        if k in [a.lower() for a in aliases]:
            return target
    return k


def main():
    if len(sys.argv) < 2:
        print("Usage: batch_csv_to_brief.py <input.csv>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1]).expanduser()
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            item = {field: "" for field in FIELDS}
            for raw_k, v in row.items():
                if raw_k is None:
                    continue
                k = normalize_key(raw_k)
                if k in item:
                    item[k] = (v or "").strip()
            if any(item.values()):
                rows.append(item)

    payload = {
        "count": len(rows),
        "fields": FIELDS,
        "items": rows,
        "prompt_hint": (
            "Use these items in batch listing mode. For each SKU, output CN titles, a short CN description, "
            "EN summary, price idea, reply note, and image direction. Keep assumptions explicit."
        )
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
