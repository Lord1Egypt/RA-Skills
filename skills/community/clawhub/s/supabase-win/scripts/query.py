#!/usr/bin/env python3
"""
Supabase Query Script - Query Supabase cloud database via REST API.
Called by AI agents to retrieve database data securely.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

# Configuration path - look for .env in references directory
SKILL_DIR = Path(__file__).parent.parent
ENV_FILE = SKILL_DIR / "references" / ".env"

# Default limits
MAX_ROWS = 200
TIMEOUT_SECONDS = 30


def load_config():
    """Load configuration from .env file."""
    config = {}
    if not ENV_FILE.exists():
        return None
    
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip().strip('"\'')
    return config


def build_api_url(project_id, table, params):
    """Build Supabase REST API URL with query parameters."""
    base_url = f"https://{project_id}.supabase.co/rest/v1/{table}"
    
    query_parts = []
    
    # Select columns
    if params.get("select"):
        query_parts.append(f"select={urllib.request.quote(params['select'])}")
    else:
        query_parts.append("select=*")
    
    # Limit (enforce max)
    limit = min(params.get("limit", MAX_ROWS), MAX_ROWS)
    query_parts.append(f"limit={limit}")
    
    # Order
    if params.get("order"):
        query_parts.append(f"order={urllib.request.quote(params['order'])}")
    
    # Equality filters (format: column:value)
    if params.get("eq"):
        for eq_filter in params["eq"]:
            if ":" in eq_filter:
                col, val = eq_filter.split(":", 1)
                query_parts.append(f"{col}=eq.{urllib.request.quote(val)}")
    
    # Greater than filters
    if params.get("gt"):
        for gt_filter in params["gt"]:
            if ":" in gt_filter:
                col, val = gt_filter.split(":", 1)
                query_parts.append(f"{col}=gt.{urllib.request.quote(val)}")
    
    # Less than filters
    if params.get("lt"):
        for lt_filter in params["lt"]:
            if ":" in lt_filter:
                col, val = lt_filter.split(":", 1)
                query_parts.append(f"{col}=lt.{urllib.request.quote(val)}")
    
    if query_parts:
        return f"{base_url}?{'&'.join(query_parts)}"
    return base_url


def execute_query(config, table, params):
    """Execute the query via Supabase REST API."""
    project_id = config.get("SUPABASE_PROJECT_ID", "")
    anon_key = config.get("SUPABASE_ANON_KEY", "")
    
    if not project_id:
        return {"success": False, "error": "Missing SUPABASE_PROJECT_ID in .env"}
    if not anon_key:
        return {"success": False, "error": "Missing SUPABASE_ANON_KEY in .env"}
    
    url = build_api_url(project_id, table, params)
    
    headers = {
        "apikey": anon_key,
        "Authorization": f"Bearer {anon_key}",
        "Accept": "application/json"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers, method="GET")
        
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            data = json.loads(response.read().decode("utf-8"))
            
            # Handle both single object and array responses
            if isinstance(data, dict):
                rows = [data]
            elif isinstance(data, list):
                rows = data
            else:
                rows = []
            
            row_count = len(rows)
            truncated = row_count >= MAX_ROWS
            
            return {
                "success": True,
                "table": table,
                "rows": rows,
                "row_count": row_count,
                "truncated": truncated,
                "max_limit": MAX_ROWS
            }
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_body)
            error_msg = error_json.get("message", error_body)
        except:
            error_msg = error_body or str(e)
        return {"success": False, "error": f"API error ({e.code}): {error_msg}"}
    except urllib.error.URLError as e:
        return {"success": False, "error": f"Connection error: {str(e.reason)}"}
    except TimeoutError:
        return {"success": False, "error": f"Request timeout ({TIMEOUT_SECONDS}s)"}
    except Exception as e:
        return {"success": False, "error": f"Execution error: {str(e)}"}


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Query Supabase via REST API")
    parser.add_argument("table", help="Table name to query")
    parser.add_argument("--select", default="*", help="Columns to select (default: *)")
    parser.add_argument("--limit", type=int, default=MAX_ROWS, help=f"Max rows (default: {MAX_ROWS})")
    parser.add_argument("--order", help="Order by column (e.g., created_at.desc)")
    parser.add_argument("--eq", action="append", help="Equality filter (format: column:value)")
    parser.add_argument("--gt", action="append", help="Greater than filter (format: column:value)")
    parser.add_argument("--lt", action="append", help="Less than filter (format: column:value)")
    
    args = parser.parse_args()
    
    # Load config
    config = load_config()
    if config is None:
        print(json.dumps({
            "success": False, 
            "error": f"Config file not found: {ENV_FILE}\nCreate it from references/.env.example"
        }, ensure_ascii=False))
        sys.exit(1)
    
    # Build params
    params = {
        "select": args.select,
        "limit": args.limit,
        "order": args.order,
        "eq": args.eq,
        "gt": args.gt,
        "lt": args.lt
    }
    
    # Execute query
    result = execute_query(config, args.table, params)
    print(json.dumps(result, ensure_ascii=False, default=str))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
