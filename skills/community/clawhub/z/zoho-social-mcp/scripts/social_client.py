#!/usr/bin/env python3
"""Shared Zoho Social MCP helpers for bundled CLIs."""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path: sys.path.insert(0, str(_SCRIPTS_DIR))
from mcp_endpoint import EndpointResolutionError, EndpointSelector, add_endpoint_arguments
SERVICE = "social"
ENV_VARS = ("ZOHO_SOCIAL_MCP_URL",)
TOOL_PREFIX = "ZohoSocial_"
ENDPOINT = EndpointSelector(SERVICE, ENV_VARS)

def runtime_tool(tool):
    return tool if tool.startswith(TOOL_PREFIX) else f"{TOOL_PREFIX}{tool}"

def positive_int(value):
    try: parsed = int(value)
    except ValueError as exc: raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 1: raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed

def build_base_parser(description, include_scope=True):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--json", action="store_true", help="print JSON instead of a table")
    parser.add_argument("--timeout", type=positive_int, default=30, help="MCP timeout in seconds")
    add_endpoint_arguments(parser)
    if include_scope:
        parser.add_argument("--portal-id", metavar="ID", help="Zoho Social portal ID")
        parser.add_argument("--brand-id", metavar="ID", help="Zoho Social brand ID")
    return parser

def headers_from(args, portal=False, brand=False):
    headers = {}
    if portal:
        if not args.portal_id: raise ValueError("--portal-id is required")
        headers["portal_id"] = str(args.portal_id)
    elif getattr(args, "portal_id", None): headers["portal_id"] = str(args.portal_id)
    if brand:
        if not args.brand_id: raise ValueError("--brand-id is required")
        headers["brand_id"] = str(args.brand_id)
    elif getattr(args, "brand_id", None): headers["brand_id"] = str(args.brand_id)
    return headers

def call(tool, args, timeout=30):
    try: mcp_url = ENDPOINT.get()
    except EndpointResolutionError as exc:
        print(f"Error: {exc}", file=sys.stderr); raise SystemExit(1)
    command = ["mcporter", "call", f"{mcp_url}.{runtime_tool(tool)}", "--args", json.dumps(args, ensure_ascii=False)]
    try: result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except FileNotFoundError: return {"error": "mcporter executable not found"}
    except subprocess.TimeoutExpired: return {"error": "mcporter call timed out"}
    if result.returncode != 0: return {"error": result.stderr.strip() or "mcporter call failed"}
    try: parsed = json.loads(result.stdout)
    except json.JSONDecodeError: return {"error": result.stderr.strip() or "mcporter returned invalid JSON"}
    if not isinstance(parsed, dict): return {"data": parsed}
    nested = parsed.get("data")
    if isinstance(nested, dict) and isinstance(nested.get("error"), dict):
        err = nested["error"]; code = err.get("code") or ""; message = err.get("message") or "Zoho Social request failed"
        return {"error": f"{code}: {message}" if code else message}
    if parsed.get("status") in {"error", "failure"}: return {"error": parsed.get("message") or parsed.get("data") or "Zoho Social request failed"}
    return parsed

def rows(result):
    if not isinstance(result, dict) or "error" in result: return []
    def extract(node):
        if isinstance(node, list): return node
        if isinstance(node, dict):
            for key in ("data","portals","brands","channels","posts","drafts","schedules","media","assets","users","boards","response","result"):
                if key in node:
                    found = extract(node[key])
                    if found is not None: return found
        return None
    found = extract(result.get("data", result)); return found if found is not None else []

def field(record, candidates, default="-"):
    if not isinstance(record, dict): return default
    lowered = {str(k).lower(): k for k in record}
    for candidate in candidates:
        actual = lowered.get(candidate.lower())
        if actual is None: continue
        value = record[actual]
        if value in (None, ""): continue
        if isinstance(value, dict):
            for nested in ("name","display_name","displayName","email","id","title"):
                if value.get(nested): return str(value[nested])
        if isinstance(value, bool): return "yes" if value else "no"
        return str(value)
    return default

def paginate(tool, headers=None, params=None, page_size=20, max_records=None, timeout=30):
    collected, offset = [], 0
    while True:
        request_limit = min(page_size, max_records-len(collected)) if max_records is not None else page_size
        if request_limit <= 0: break
        query = dict(params or {}); query.update({"offset": offset, "limit": request_limit})
        result = call(tool, {"headers": dict(headers or {}), "query_params": query}, timeout=timeout)
        if "error" in result: return result
        page = rows(result); collected.extend(page)
        if not page or len(page) < request_limit: break
        offset += len(page)
    return {"data": collected[:max_records] if max_records else collected, "info": {"count": len(collected)}}

def print_table(records, columns, empty="No records found."):
    if not records: print(empty); return
    widths = {label: max(len(label), min(max((len(field(r, keys)) for r in records), default=0), 40)) for label, keys in columns}
    print(" | ".join(label.ljust(widths[label]) for label, _ in columns)); print("-+-".join("-"*widths[label] for label, _ in columns))
    for row in records:
        vals=[]
        for label, keys in columns:
            value=field(row, keys); value=value[:37]+"..." if len(value)>40 else value; vals.append(value.ljust(widths[label]))
        print(" | ".join(vals))
    print(f"\n{len(records)} record(s)")

def finish(result, records, args, columns, empty="No records found."):
    if "error" in result: print(f"Error: {result['error']}", file=sys.stderr); return 1
    if args.json: print(json.dumps(records, indent=2, ensure_ascii=False))
    else: print_table(records, columns, empty)
    return 0
