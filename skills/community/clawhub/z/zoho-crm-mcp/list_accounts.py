#!/usr/bin/env python3
"""
List Zoho CRM accounts (companies) or search by name.
Uses executeCOQLQuery via mcporter.

Setup:
  export ZOHO_MCP_URL="https://your-org-zoho-crm-xxxxx.zohomcp.eu/mcp/YOUR_TOKEN/message"

Usage:
  python3 list_accounts.py                         # All accounts as table
  python3 list_accounts.py --json                  # Raw JSON output
  python3 list_accounts.py --search "Acme"         # Search by company name
  python3 list_accounts.py --all                   # All accounts (even without website)

Fields: Account_Name, Website, Phone, Billing_City, Billing_Country, Industry, id
"""

import subprocess
import json
import sys
import os
import tempfile

MCP_URL = os.environ.get("ZOHO_MCP_URL", "")
TOOL = "ZohoCRM_executeCOQLQuery"

FIELDS = ["Account_Name", "Website", "Phone", "Billing_City", "Billing_Country", "Industry", "id"]
FIELD_LABELS = {
    "Account_Name": "Company",
    "Website": "Website",
    "Phone": "Phone",
    "Billing_City": "City",
    "Billing_Country": "Country",
    "Industry": "Industry",
    "id": "CRM ID",
}


def mcporter_call(args_json):
    if not MCP_URL:
        print("Error: ZOHO_MCP_URL not set. Please set the environment variable.", file=sys.stderr)
        print("  export ZOHO_MCP_URL='https://your-org-zoho-crm-xxxxx.zohomcp.eu/mcp/YOUR_TOKEN/message'", file=sys.stderr)
        sys.exit(1)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, dir="/tmp") as f:
        f.write(json.dumps(args_json, ensure_ascii=False))
        tmp_path = f.name

    try:
        cmd = ["bash", "-c", f'mcporter call "{MCP_URL}.{TOOL}" --args "$(< {tmp_path})"']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"error": result.stdout + result.stderr}
    finally:
        os.unlink(tmp_path)


def query_accounts(where_clause="", limit=100):
    fields_str = ", ".join(FIELDS)
    query = f"SELECT {fields_str} FROM Accounts"
    if where_clause:
        query += f" WHERE {where_clause}"
    query += f" ORDER BY Account_Name LIMIT {limit}"
    return mcporter_call({"body": {"select_query": query}})


def print_table(data):
    if not data:
        print("No records found.")
        return

    col_widths = {}
    for field in FIELDS:
        label = FIELD_LABELS.get(field, field)
        max_val_len = max((len(str(row.get(field, "") or "")) for row in data), default=0)
        col_widths[field] = max(len(label), min(max_val_len, 50))

    header_parts = [FIELD_LABELS.get(f, f).ljust(col_widths[f]) for f in FIELDS]
    print(" | ".join(header_parts))
    print("-+-".join("-" * col_widths[f] for f in FIELDS))

    for row in data:
        parts = []
        for field in FIELDS:
            val = str(row.get(field, "") or "-")
            if len(val) > 50:
                val = val[:47] + "..."
            parts.append(val.ljust(col_widths[field]))
        print(" | ".join(parts))

    print(f"\n{len(data)} record(s)")


def main():
    args = sys.argv[1:]
    json_mode = "--json" in args
    show_all = "--all" in args
    search_term = None

    for i, arg in enumerate(args):
        if arg == "--search" and i + 1 < len(args):
            search_term = args[i + 1]

    if search_term:
        where = "Account_Name != ''"
    elif show_all:
        where = "Account_Name != ''"
    else:
        where = "Website != ''"

    limit = 200 if search_term else 100
    result = query_accounts(where, limit=limit)

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    data = result.get("data", [])
    info = result.get("info", {})

    if search_term:
        search_lower = search_term.lower()
        data = [row for row in data if search_lower in (row.get("Account_Name", "") or "").lower()]

    if json_mode:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print_table(data)

    if info.get("more_records"):
        print(f"\nMore records available (showing {info.get('count', '?')}).")


if __name__ == "__main__":
    main()
