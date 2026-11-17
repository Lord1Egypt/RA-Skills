#!/usr/bin/env python3
"""
Search records in any Zoho CRM module via mcporter.
Uses ZohoCRM_searchRecords and executeCOQLQuery.

Setup:
  export ZOHO_MCP_URL="https://your-org-zoho-crm-xxxxx.zohomcp.eu/mcp/YOUR_TOKEN/message"

Usage:
  python3 scripts/search_records.py Contacts "Smith"
  python3 scripts/search_records.py Accounts "Acme Corp"
  python3 scripts/search_records.py Deals "Project X"
  python3 scripts/search_records.py Leads "Leadname" --json
  python3 scripts/search_records.py Contacts --coql "Email != ''"
"""

import subprocess
import json
import sys
import os

MCP_URL = os.environ.get("ZOHO_MCP_URL", "")


def mcporter_call(tool, args):
    if not MCP_URL:
        print("Error: ZOHO_MCP_URL not set. Please set the environment variable.", file=sys.stderr)
        print("  export ZOHO_MCP_URL='https://your-org-zoho-crm-xxxxx.zohomcp.eu/mcp/YOUR_TOKEN/message'", file=sys.stderr)
        sys.exit(1)

    cmd = [
        "mcporter",
        "call",
        f"{MCP_URL}.{tool}",
        "--args",
        json.dumps(args, ensure_ascii=False),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": result.stdout + result.stderr}


def normalize_crm_result(result):
    """Return a records list across CRM MCP response variants.

    Records may arrive directly under "data" as a list, or nested as
    {"data": {"data": [...], "info": {...}}}, or wrapped with a "message"
    (e.g. no records). This normalizes all of them to a plain list.
    """
    payload = result.get("data", [])
    if isinstance(payload, dict):
        if "data" in payload:
            return payload.get("data") or []
        if "message" in payload:
            return []
    if isinstance(payload, list):
        return payload
    return []


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
        elif not arg.startswith("-") and (i == 0 or args[i - 1] not in {"--search", "--coql"}):
            search_term = arg

    if coql_where:
        result = coql_query(module, coql_where)
    elif search_term:
        result = search_module(module, search_term)
    else:
        result = coql_query(module, "")

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    data = normalize_crm_result(result)

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
