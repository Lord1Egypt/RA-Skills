#!/usr/bin/env python3
"""
Search records in any Zoho CRM module via mcporter.
Uses ZohoCRM_searchRecords and executeCOQLQuery.

Setup:
  export ZOHO_MCP_URL="https://your-org-zoho-crm-xxxxx.zohomcp.eu/mcp/YOUR_TOKEN/message"

Usage:
  python3 search_records.py Contacts "Smith"
  python3 search_records.py Accounts "Acme Corp"
  python3 search_records.py Deals "Project X"
  python3 search_records.py Leads "Leadname" --json
  python3 search_records.py Contacts --coql "Email != ''"
"""

import subprocess
import json
import sys
import os
import tempfile

MCP_URL = os.environ.get("ZOHO_MCP_URL", "")


def mcporter_call(tool, args):
    if not MCP_URL:
        print("Error: ZOHO_MCP_URL not set. Please set the environment variable.", file=sys.stderr)
        print("  export ZOHO_MCP_URL='https://your-org-zoho-crm-xxxxx.zohomcp.eu/mcp/YOUR_TOKEN/message'", file=sys.stderr)
        sys.exit(1)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, dir="/tmp") as f:
        f.write(json.dumps(args, ensure_ascii=False))
        tmp_path = f.name

    try:
        cmd = ["bash", "-c", f'mcporter call "{MCP_URL}.{tool}" --args "$(< {tmp_path})"']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"error": result.stdout + result.stderr}
    finally:
        os.unlink(tmp_path)


def search_module(module, search_term):
    """Search a module by name field."""
    name_field_map = {
        "Contacts": "Last_Name",
        "Accounts": "Account_Name",
        "Deals": "Deal_Name",
        "Leads": "Last_Name",
        "Products": "Product_Name",
    }
    name_field = name_field_map.get(module, "Name")
    criteria = f"({name_field}:equals:{search_term})"
    args = {
        "path_variables": {"module": module},
        "query_params": {"criteria": criteria},
    }
    return mcporter_call("ZohoCRM_searchRecords", args)


def coql_query(module, where_clause, limit=100):
    """Execute a COQL query on a module."""
    query = f"SELECT * FROM {module}"
    if where_clause:
        query += f" WHERE {where_clause}"
    query += f" LIMIT {limit}"
    return mcporter_call("ZohoCRM_executeCOQLQuery", {"body": {"select_query": query}})


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 search_records.py <Module> [--search <term>] [--coql <WHERE>] [--json]")
        print("Modules: Contacts, Accounts, Deals, Leads, Products, ...")
        sys.exit(1)

    module = sys.argv[1]
    args = sys.argv[2:]
    json_mode = "--json" in args
    search_term = None
    coql_where = None

    for i, arg in enumerate(args):
        if arg == "--search" and i + 1 < len(args):
            search_term = args[i + 1]
        elif arg == "--coql" and i + 1 < len(args):
            coql_where = args[i + 1]

    if coql_where:
        result = coql_query(module, coql_where)
    elif search_term:
        result = search_module(module, search_term)
    else:
        result = coql_query(module, "")

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    data = result.get("data", [])

    if json_mode:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        if not data:
            print(f"No {module} records found.")
            return
        keys = list(data[0].keys())[:8]
        col_widths = {k: max(len(k), min(max(len(str(row.get(k, ""))) for row in data), 40)) for k in keys}

        print(" | ".join(k.ljust(col_widths[k]) for k in keys))
        print("-+-".join("-" * col_widths[k] for k in keys))
        for row in data:
            vals = []
            for k in keys:
                v = str(row.get(k, "") or "-")
                if len(v) > 40:
                    v = v[:37] + "..."
                vals.append(v.ljust(col_widths[k]))
            print(" | ".join(vals))
        print(f"\n{len(data)} record(s)")


if __name__ == "__main__":
    main()
