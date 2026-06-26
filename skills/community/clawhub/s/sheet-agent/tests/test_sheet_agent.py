#!/usr/bin/env python3
"""
sheet-agent test suite

Usage:
python test_sheet_agent.py
"""

import csv
import os
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


def test_read_csv():
    print("🧪 Test: read CSV")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["Name", "Phone", "Follow Up Date", "Status"])
        writer.writeheader()
        writer.writerows(
            [
                {
                    "Name": "Alice",
                    "Phone": "13800001111",
                    "Follow Up Date": "2026-03-20",
                    "Status": "In progress",
                },
                {
                    "Name": "Bob",
                    "Phone": "13800002222",
                    "Follow Up Date": "2026-03-25",
                    "Status": "Pending",
                },
            ]
        )
        csv_path = Path(handle.name)

    from sheet_agent import get_table_info, read_table

    df = read_table(csv_path)
    assert len(df) == 2, f"Expected 2 rows, got {len(df)}"
    info = get_table_info(df)
    assert info["rows"] == 2
    assert info["table_type"] == "Sales leads"
    os.unlink(csv_path)
    print("  ✅ Passed")


def test_read_excel():
    print("🧪 Test: read Excel")
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as handle:
        xlsx_path = Path(handle.name)

    pd.DataFrame(
        [
            {"Product": "Bluetooth Earbuds", "Inventory": 100, "Price": 199},
            {"Product": "Phone Case", "Inventory": -5, "Price": 39},
        ]
    ).to_excel(xlsx_path, index=False, engine="openpyxl")

    from sheet_agent import get_table_info, read_table

    df = read_table(xlsx_path)
    assert len(df) == 2
    info = get_table_info(df)
    assert info["table_type"] == "Inventory"
    os.unlink(xlsx_path)
    print("  ✅ Passed")


def test_anomaly_detection():
    print("🧪 Test: anomaly detection")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["Product", "Inventory", "Price", "Order ID"])
        writer.writeheader()
        writer.writerows(
            [
                {"Product": "Headphones", "Inventory": -5, "Price": 199, "Order ID": "A1"},
                {"Product": "Phone Case", "Inventory": 50, "Price": "", "Order ID": "A2"},
                {"Product": "Cable", "Inventory": 9999, "Price": 9, "Order ID": "A3"},
                {"Product": "Cable", "Inventory": 20, "Price": 9, "Order ID": "A3"},
            ]
        )
        csv_path = Path(handle.name)

    from sheet_agent import detect_anomalies

    df = pd.read_csv(csv_path)
    anomaly_types = [item["type"] for item in detect_anomalies(df)]
    assert "Negative value" in anomaly_types, f"Expected a negative-value anomaly, got {anomaly_types}"
    assert "Missing value" in anomaly_types, f"Expected a missing-value anomaly, got {anomaly_types}"
    assert "Duplicate ID" in anomaly_types, f"Expected a duplicate-ID anomaly, got {anomaly_types}"
    os.unlink(csv_path)
    print("  ✅ Passed")


def test_natural_query_overdue():
    print("🧪 Test: natural-language overdue query")
    rows = [
        {"Name": "Alice", "Follow Up Date": "2026-03-15", "Amount": 1000},
        {"Name": "Bob", "Follow Up Date": "2026-03-28", "Amount": 2000},
        {"Name": "Cara", "Follow Up Date": "2026-03-25", "Amount": 1500},
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        csv_path = Path(handle.name)

    from sheet_agent import execute_query, parse_natural_query, read_table

    df = read_table(csv_path)
    plan = parse_natural_query(df, "Which leads have not been followed up for more than 3 days?")
    assert plan["action"] == "query", f"Expected query action, got {plan['action']}"
    assert plan["days"] == 3
    result = execute_query(df, plan)
    assert len(result) >= 1, f"Expected at least 1 overdue record, got {len(result)}"
    os.unlink(csv_path)
    print("  ✅ Passed")


def test_change_preview():
    print("🧪 Test: change preview without writing")
    rows = [
        {"Name": "Alice", "Customer Tier": "Regular"},
        {"Name": "Bob", "Customer Tier": "VIP"},
        {"Name": "Cara", "Customer Tier": "Regular"},
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        csv_path = Path(handle.name)

    from sheet_agent import build_change_preview, read_table

    df = read_table(csv_path)
    preview = build_change_preview(df, 2, "Customer Tier", "VIP")
    assert "preview" in preview
    assert preview["preview"]["old_value"] == "Regular"
    assert preview["preview"]["new_value"] == "VIP"
    os.unlink(csv_path)
    print("  ✅ Passed")


def test_report_generation():
    print("🧪 Test: report generation")
    rows = [
        {"Product": "Bluetooth Earbuds", "Quantity": 10, "Amount": 1990},
        {"Product": "Phone Case", "Quantity": 5, "Amount": 195},
        {"Product": "Charging Cable", "Quantity": 8, "Amount": 320},
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        csv_path = Path(handle.name)

    from sheet_agent import generate_report, read_table

    df = read_table(csv_path)
    report = generate_report(df, "weekly")
    assert "Operations Summary" in report or "Daily Summary" in report
    assert "Total records" in report
    os.unlink(csv_path)
    print("  ✅ Passed")


def test_table_type_inference():
    print("🧪 Test: table type inference")
    from sheet_agent import infer_table_type

    df_order = pd.DataFrame({"Order ID": ["A1"], "Amount": [100], "Date": ["2026-03-01"]})
    assert infer_table_type(df_order) == "Orders"

    df_inventory = pd.DataFrame({"Product": ["Earbuds"], "Inventory": [10], "Price": [199]})
    assert infer_table_type(df_inventory) == "Inventory"

    df_lead = pd.DataFrame({"Name": ["Alice"], "Phone": ["138"], "Follow Up Date": ["2026-03-01"]})
    assert infer_table_type(df_lead) == "Sales leads"

    print("  ✅ Passed")


def run_all():
    print("=" * 50)
    print("🧪 sheet-agent test suite")
    print("=" * 50)
    print()

    tests = [
        test_table_type_inference,
        test_read_csv,
        test_read_excel,
        test_anomaly_detection,
        test_natural_query_overdue,
        test_change_preview,
        test_report_generation,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as exc:
            print(f"  ❌ Failed: {exc}")
            import traceback

            traceback.print_exc()
            failed += 1

    print()
    print("=" * 50)
    print(f"Result: {passed} passed, {failed} failed")
    print("=" * 50)
    return failed == 0


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
