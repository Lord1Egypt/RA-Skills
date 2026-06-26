#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path

FIELDS = [
    "invoice_number",
    "invoice_date",
    "order_id",
    "order_name",
    "customer_name",
    "customer_email",
    "billing_name",
    "billing_address",
    "currency",
    "subtotal",
    "shipping",
    "tax",
    "total",
    "payment_status",
    "source_order_reference",
]


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: invoice_export.py input.json output.csv")
        return 1

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    try:
        data = json.loads(input_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {input_path}: {exc}")
        return 1

    if not isinstance(data, list):
        print("Input JSON must be a list of orders")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for idx, row in enumerate(data, start=1):
            if not isinstance(row, dict):
                print("Each order entry must be a JSON object")
                return 1
            financial_status = str(row.get("financial_status", "")).strip().lower()
            if financial_status not in {"paid", "authorized", "partially_paid"}:
                continue
            billing_name = row.get("billing_name") or row.get("customer_name", "")
            out = {
                "invoice_number": row.get("invoice_number", f"DRAFT-{idx:04d}"),
                "invoice_date": row.get("invoice_date") or str(row.get("created_at", ""))[:10],
                "order_id": row.get("order_id", ""),
                "order_name": row.get("order_name", ""),
                "customer_name": row.get("customer_name", ""),
                "customer_email": row.get("customer_email", ""),
                "billing_name": billing_name,
                "billing_address": row.get("billing_address", ""),
                "currency": row.get("currency", ""),
                "subtotal": row.get("subtotal", 0),
                "shipping": row.get("shipping", 0),
                "tax": row.get("tax", 0),
                "total": row.get("total", 0),
                "payment_status": financial_status,
                "source_order_reference": row.get("order_name") or row.get("order_id", ""),
            }
            writer.writerow(out)

    print(f"Prepared invoice-ready CSV: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
