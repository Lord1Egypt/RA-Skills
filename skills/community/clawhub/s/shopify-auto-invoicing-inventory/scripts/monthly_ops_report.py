#!/usr/bin/env python3
import csv
import sys
from collections import Counter
from pathlib import Path


def to_float(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: monthly_ops_report.py orders.csv stock.csv output.csv")
        return 1

    orders_path = Path(sys.argv[1])
    stock_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])

    if not orders_path.exists() or not stock_path.exists():
        print("Input file not found")
        return 1

    with orders_path.open("r", encoding="utf-8-sig", newline="") as f:
        orders = list(csv.DictReader(f))
    with stock_path.open("r", encoding="utf-8-sig", newline="") as f:
        stock = list(csv.DictReader(f))

    paid = 0
    pending = 0
    cancelled = 0
    revenue = 0.0
    tax_total = 0.0
    units = 0
    sku_counter = Counter()

    for row in orders:
        status = str(row.get("financial_status", "")).strip().lower()
        if status in {"paid", "authorized", "partially_paid"}:
            paid += 1
        elif "pending" in status:
            pending += 1
        elif "cancel" in status or "void" in status:
            cancelled += 1
        revenue += to_float(row.get("total") or row.get("total_price"))
        tax_total += to_float(row.get("tax") or row.get("tax_total"))
        try:
            units += int(float(row.get("quantity") or 0))
        except (TypeError, ValueError):
            pass
        sku = (row.get("sku") or "").strip()
        if sku:
            sku_counter[sku] += int(float(row.get("quantity") or 0)) if str(row.get("quantity") or "").strip() else 0

    low_stock_count = sum(1 for row in stock if str(row.get("low_stock_flag", "")).strip().lower() == "yes")
    top_skus = "; ".join(f"{sku}:{qty}" for sku, qty in sku_counter.most_common(5))

    summary = [{
        "total_orders_processed": len(orders),
        "paid_orders": paid,
        "pending_payment_orders": pending,
        "cancelled_orders": cancelled,
        "invoice_ready_orders": paid,
        "invoiced_revenue": round(revenue, 2),
        "tax_total": round(tax_total, 2),
        "units_sold": units,
        "top_skus_by_quantity": top_skus,
        "low_stock_sku_count": low_stock_count,
    }]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)

    print(f"Wrote monthly ops report: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
