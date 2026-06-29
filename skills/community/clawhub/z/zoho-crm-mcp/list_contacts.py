#!/usr/bin/env python3
"""
List Zoho CRM contacts or search by name.
Uses ZohoCRM_searchRecords / executeCOQLQuery via mcporter.

Setup:
  export ZOHO_MCP_URL="https://your-org-zoho-crm-xxxxx.zohomcp.eu/mcp/YOUR_TOKEN/message"

Usage:
  python3 list_contacts.py                          # All contacts as table
  python3 list_contacts.py --json                   # Raw JSON output
  python3 list_contacts.py --search "Smith"         # Search by last name
  python3 list_contacts.py --search "Smith" --full  # Full record data

Fields (table): Full_Name, Email, Mobile, Phone, Account_Name, Owner
"""

import subprocess
import json
import sys
import os
import tempfile

MCP_URL = os.environ.get("ZOHO_MCP_URL", "")
TOOL = "ZohoCRM_searchRecords"

TABLE_FIELDS = ["Full_Name", "Email", "Mobile", "Phone", "Account_Name", "Owner"]
FIELD_LABELS = {
    "Full_Name": "Name",
    "Email": "Email",
    "Mobile": "Mobile",
    "Phone": "Phone",
    "Account_Name": "Company",
    "Owner": "Owner",
}


def mcporter_search_contacts(criteria, page=1, per_page=200):
    args = {
        "path_variables": {"module": "Contacts"},
        "query_params": {"criteria": criteria, "page": page, "per_page": per_page},
    }
    return _mcporter_call(TOOL, args)


def query_all_contacts(page=1, per_page=200):
    coql_tool = "ZohoCRM_executeCOQLQuery"
    fields = ["Full_Name", "First_Name", "Last_Name", "Email", "Mobile", "Phone", "Account_Name", "Owner", "id"]
    fields_str = ", ".join(fields)
    query = f"SELECT {fields_str} FROM Contacts WHERE Last_Name != '' ORDER BY Last_Name LIMIT {per_page}"
    args = {"body": {"select_query": query}}
    return _mcporter_call(coql_tool, args)


def search_contacts_by_name(last_name):
    criteria = f"(Last_Name:equals:{last_name})"
    return mcporter_search_contacts(criteria)


def _mcporter_call(tool, args):
    if not MCP_URL:
        print("Error: ZOHO_MCP_URL not set. Please set the environment variable.", file=sys.stderr)
        print("  export ZOHO_MCP_URL='https://your-org-zoho-crm-xxxxx.zohomcp.eu/mcp/YOUR_TOKEN/message'", file=sys.stderr)
        sys.exit(1)

    args_json = json.dumps(args, ensure_ascii=False)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, dir="/tmp") as f:
        f.write(args_json)
        tmp_path = f.name

    try:
        full_cmd = f'mcporter call "{MCP_URL}.{tool}" --args "$(< {tmp_path})"'
        result = subprocess.run(["bash", "-c", full_cmd], capture_output=True, text=True, timeout=30)
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"error": result.stdout + result.stderr}
    finally:
        os.unlink(tmp_path)


def extract_table_field(contact, field):
    val = contact.get(field, "")
    if not val:
        return "-"
    if isinstance(val, dict):
        return val.get("name", str(val))
    return str(val)


def print_table(data):
    if not data:
        print("No contacts found.")
        return

    col_widths = {}
    for field in TABLE_FIELDS:
        label = FIELD_LABELS.get(field, field)
        max_val_len = max((len(extract_table_field(row, field)) for row in data), default=0)
        col_widths[field] = max(len(label), min(max_val_len, 50))

    header_parts = [FIELD_LABELS.get(f, f).ljust(col_widths[f]) for f in TABLE_FIELDS]
    print(" | ".join(header_parts))
    print("-+-".join("-" * col_widths[f] for f in TABLE_FIELDS))

    for row in data:
        parts = []
        for field in TABLE_FIELDS:
            val = extract_table_field(row, field)
            if len(val) > 50:
                val = val[:47] + "..."
            parts.append(val.ljust(col_widths[field]))
        print(" | ".join(parts))

    print(f"\n{len(data)} contact(s)")


def main():
    args = sys.argv[1:]
    json_mode = "--json" in args
    full_mode = "--full" in args
    search_term = None

    for i, arg in enumerate(args):
        if arg == "--search" and i + 1 < len(args):
            search_term = args[i + 1]

    if search_term:
        result = search_contacts_by_name(search_term)
    else:
        result = query_all_contacts()

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    data = result.get("data", [])
    info = result.get("info", {})

    if json_mode:
        if full_mode:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            simplified = [{f: row.get(f) for f in TABLE_FIELDS} for row in data]
            print(json.dumps(simplified, indent=2, ensure_ascii=False))
    else:
        print_table(data)

    if info.get("more_records"):
        print(f"\nMore records available (showing {info.get('count', '?')}).")


if __name__ == "__main__":
    main()
