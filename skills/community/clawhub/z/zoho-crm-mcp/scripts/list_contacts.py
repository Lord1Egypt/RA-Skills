#!/usr/bin/env python3
"""
List Zoho CRM contacts or search by name.
Uses ZohoCRM_searchRecords (name search) and executeCOQLQuery (full list) via mcporter.

Setup:
  export ZOHO_MCP_URL="https://your-org-zoho-crm-xxxxx.zohomcp.eu/mcp/YOUR_TOKEN/message"

Usage:
  python3 scripts/list_contacts.py                          # All contacts as table
  python3 scripts/list_contacts.py --json                   # Raw JSON output
  python3 scripts/list_contacts.py --search "Smith"         # Search by last name
  python3 scripts/list_contacts.py --search "Smith" --full  # Full record data
  python3 scripts/list_contacts.py --fields First_Name,Last_Name,Email,Designation

Custom fields:
  --fields lets you list any Zoho field API names (comma-separated), including
  org-specific custom fields. Field API names are shown as-is in the table header
  unless a friendly label exists.

Default fields (table): Full_Name, Email, Mobile, Phone, Account_Name, Owner
"""

import subprocess
import json
import sys
import os

MCP_URL = os.environ.get("ZOHO_MCP_URL", "")
TOOL = "ZohoCRM_searchRecords"
COQL_TOOL = "ZohoCRM_executeCOQLQuery"

DEFAULT_FIELDS = ["Full_Name", "Email", "Mobile", "Phone", "Account_Name", "Owner"]
# Extra fields always requested via COQL so table rendering has what it needs.
COQL_BASE_FIELDS = ["First_Name", "Last_Name", "id"]

FIELD_LABELS = {
    "Full_Name": "Name",
    "First_Name": "First Name",
    "Last_Name": "Last Name",
    "Email": "Email",
    "Mobile": "Mobile",
    "Phone": "Phone",
    "Account_Name": "Company",
    "Owner": "Owner",
    "Designation": "Title",
    "id": "CRM ID",
}


def _mcporter_call(tool, args):
    """Call mcporter directly (no shell) to avoid expanding the credential-bearing URL."""
    if not MCP_URL:
        print("Error: ZOHO_MCP_URL not set. Please set the environment variable.", file=sys.stderr)
        print("  export ZOHO_MCP_URL='https://your-org-zoho-crm-xxxxx.zohomcp.eu/mcp/YOUR_TOKEN/message'", file=sys.stderr)
        sys.exit(1)

    cmd = ["mcporter", "call", f"{MCP_URL}.{tool}", "--args", json.dumps(args, ensure_ascii=False)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": result.stdout + result.stderr}


def normalize_crm_result(result):
    """Return a consistent (data, info) tuple across CRM MCP response variants.

    The Zoho CRM MCP may return records either directly under "data" as a list,
    or nested as {"data": {"data": [...], "info": {...}}}, or wrapped with a
    "message" (e.g. no records). This normalizes all of them.
    """
    if "error" in result:
        return None, None

    payload = result.get("data", [])
    if isinstance(payload, dict):
        if "data" in payload:
            return payload.get("data") or [], payload.get("info", {})
        if "message" in payload:
            return [], {}

    if isinstance(payload, list):
        return payload, result.get("info", {})

    return [], result.get("info", {})


def query_contacts_page(fields, offset=0, limit=100):
    """Fetch one contacts page using executeCOQLQuery."""
    fields_str = ", ".join(fields)
    query = (
        f"SELECT {fields_str} FROM Contacts WHERE Last_Name != '' "
        f"ORDER BY Last_Name LIMIT {offset}, {limit}"
    )
    return _mcporter_call(COQL_TOOL, {"body": {"select_query": query}})


def query_all_contacts(fields, per_page=100):
    """Fetch all contacts using paginated COQL queries."""
    all_data = []
    offset = 0

    while True:
        result = query_contacts_page(fields, offset=offset, limit=per_page)
        if "error" in result:
            return result

        data, info = normalize_crm_result(result)
        if data is None:
            return {"error": "CRM response could not be normalized"}

        all_data.extend(data)
        if not info.get("more_records") or not data:
            break

        offset += len(data)

    return {"data": all_data, "info": {"count": len(all_data), "more_records": False}}


def search_contacts_by_name(last_name):
    """Search contacts by last name using searchRecords."""
    criteria = f"(Last_Name:equals:{last_name})"
    args = {
        "path_variables": {"module": "Contacts"},
        "query_params": {"criteria": criteria, "page": 1, "per_page": 200},
    }
    return _mcporter_call(TOOL, args)


def extract_table_field(contact, field):
    """Extract a field from contact data, handling nested objects (e.g. Account_Name, Owner)."""
    val = contact.get(field, "")
    if not val:
        return "-"
    if isinstance(val, dict):
        return val.get("name", str(val))
    return str(val)


def print_table(data, fields):
    if not data:
        print("No contacts found.")
        return

    col_widths = {}
    for field in fields:
        label = FIELD_LABELS.get(field, field)
        max_val_len = max((len(extract_table_field(row, field)) for row in data), default=0)
        col_widths[field] = max(len(label), min(max_val_len, 50))

    header_parts = [FIELD_LABELS.get(f, f).ljust(col_widths[f]) for f in fields]
    print(" | ".join(header_parts))
    print("-+-".join("-" * col_widths[f] for f in fields))

    for row in data:
        parts = []
        for field in fields:
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
    custom_fields = None

    for i, arg in enumerate(args):
        if arg == "--search" and i + 1 < len(args):
            search_term = args[i + 1]
        elif arg == "--fields" and i + 1 < len(args):
            custom_fields = [f.strip() for f in args[i + 1].split(",") if f.strip()]

    table_fields = custom_fields if custom_fields else DEFAULT_FIELDS

    if search_term:
        # searchRecords returns full records; table just picks the requested fields.
        result = search_contacts_by_name(search_term)
        data, info = normalize_crm_result(result)
        if data is None:
            print(f"Error: {result.get('error')}", file=sys.stderr)
            sys.exit(1)
    else:
        # COQL needs an explicit field list; merge requested + base fields (dedup, keep order).
        coql_fields = list(dict.fromkeys(table_fields + COQL_BASE_FIELDS))
        result = query_all_contacts(coql_fields)
        if "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        data, info = normalize_crm_result(result)

    if json_mode:
        if full_mode:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            simplified = [{f: row.get(f) for f in table_fields} for row in data]
            print(json.dumps(simplified, indent=2, ensure_ascii=False))
    else:
        print_table(data, table_fields)

    if info.get("more_records"):
        print(f"\nMore records available (showing {info.get('count', '?')}).")


if __name__ == "__main__":
    main()
