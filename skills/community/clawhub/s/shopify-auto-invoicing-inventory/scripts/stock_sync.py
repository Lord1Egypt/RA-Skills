#!/usr/bin/env python3
import csv
import sys
from pathlib import Path

OUT_FIELDS = [
    "sku",
    "product_title",
    "variant_title",
    "opening_stock",
    "quantity_sold",
    "quantity_refunded",
    "net_change",
    "closing_stock",
    "low_stock_flag",
    "reorder_note",
]


def to_int(value):
    try:
        return int(float(value or 0))
    except (TypeError, ValueError):
        return 0


def main() -> int:
    if len(sys.argv) not in {4, 5}:
        print("Usage: stock_sync.py inventory.csv orders.csv output.csv [low_stock_threshold]")
        return 1

    inventory_path = Path(sys.argv[1])
    orders_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])
    threshold = to_int(sys.argv[4]) if len(sys.argv) == 5 else 5

    if not inventory_path.exists() or not orders_path.exists():
        print("Input file not found")
        return 1

    with inventory_path.open("r", encoding="utf-8-sig", newline="") as f:
        inventory_rows = list(csv.DictReader(f))
    with orders_path.open("r", encoding="utf-8-sig", newline="") as f:
        order_rows = list(csv.DictReader(f))

    by_sku = {}
    for row in inventory_rows:
        sku = (row.get("sku") or row.get("SKU") or "").strip()
        if not sku:
            continue
        by_sku[sku] = {
            "sku": sku,
            "product_title": row.get("product_title") or row.get("Product") or "",
            "variant_title": row.get("variant_title") or row.get("Variant") or "",
            "opening_stock": to_int(row.get("opening_stock") or row.get("stock") or row.get("available")),
            "quantity_sold": 0,
            "quantity_refunded": 0,
        }

    for row in order_rows:
        sku = (row.get("sku") or row.get("SKU") or "").strip()
        if not sku:
            continue
        entry = by_sku.setdefault(sku, {
            "sku": sku,
            "product_title": row.get("product_title", ""),
            "variant_title": row.get("variant_title", ""),
            "opening_stock": 0,
            "quantity_sold": 0,
            "quantity_refunded": 0,
        })
        entry["quantity_sold"] += to_int(row.get("quantity") or row.get("quantity_sold"))
        entry["quantity_refunded"] += to_int(row.get("quantity_refunded"))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUT_FIELDS)
        writer.writeheader()
        for sku in sorted(by_sku):
            row = by_sku[sku]
            net_change = row["quantity_refunded"] - row["quantity_sold"]
            closing_stock = row["opening_stock"] + net_change
            writer.writerow({
                "sku": sku,
                "product_title": row["product_title"],
                "variant_title": row["variant_title"],
                "opening_stock": row["opening_stock"],
                "quantity_sold": row["quantity_sold"],
                "quantity_refunded": row["quantity_refunded"],
                "net_change": net_change,
                "closing_stock": closing_stock,
                "low_stock_flag": "yes" if closing_stock <= threshold else "no",
                "reorder_note": "needs_review" if closing_stock < 0 else ("reorder_soon" if closing_stock <= threshold else "ok"),
            })

    print(f"Wrote stock reconciliation CSV: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
