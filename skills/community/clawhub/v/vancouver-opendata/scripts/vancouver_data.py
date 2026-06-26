#!/usr/bin/env python3
"""
City of Vancouver Open Data — CLI for the Opendatasoft API.
No dependencies beyond stdlib. Accesses opendata.vancouver.ca.

Usage:
  python3 vancouver_data.py <command> [args]

Commands:
  search <query>                    Search datasets by keyword
  list                              List all datasets
  info <dataset-id>                 Show dataset metadata
  fetch <dataset-id> [options]      Fetch data rows
"""

import json
import sys
import os
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

BASE_URL = "https://opendata.vancouver.ca/api/explore/v2.1"

def api_request(path, params=None):
    """Make a request to the Opendatasoft API."""
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"Error: HTTP {e.code} — {body[:200]}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: {e.reason}")
        sys.exit(1)

def load_catalog():
    """Fetch the full dataset catalogue (cached locally for 1 hour)."""
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, "catalog_cache.json")
    
    if os.path.exists(cache_file):
        age = datetime.now().timestamp() - os.path.getmtime(cache_file)
        if age < 3600:
            return json.loads(open(cache_file).read())
    
    # Fetch all datasets in batches
    all_datasets = []
    offset = 0
    while True:
        data = api_request("/catalog/datasets", {"limit": 100, "offset": offset, "select": "dataset_id,title"})
        results = data.get("results", [])
        all_datasets.extend(results)
        if len(results) < 100:
            break
        offset += 100
    
    with open(cache_file, "w") as f:
        json.dump(all_datasets, f)
    return all_datasets

# --- Commands ---

def cmd_search(query):
    """Search datasets by name."""
    datasets = load_catalog()
    query_lower = query.lower()
    matches = [d for d in datasets if query_lower in d.get("title", "").lower() or query_lower in d.get("dataset_id", "").lower()]
    
    if not matches:
        print(f"No datasets found matching '{query}'.")
        return
    
    print(f"\n🔍 Search results for '{query}' — {len(matches)} found\n")
    for d in matches:
        title = d.get("title", "?")
        did = d.get("dataset_id", "")
        print(f"  • {title}")
        print(f"    ID: {did}")
        print(f"    https://opendata.vancouver.ca/explore/dataset/{did}")
    print()

def cmd_list():
    """List all datasets."""
    datasets = load_catalog()
    
    print(f"\n📁 Vancouver Open Data — {len(datasets)} datasets\n")
    for d in sorted(datasets, key=lambda x: x.get("title", "")):
        title = d.get("title", "N/A")
        did = d.get("dataset_id", "")
        print(f"  • {title} — {did}")
    print()

def cmd_info(dataset_id):
    """Show metadata for a dataset."""
    data = api_request(f"/catalog/datasets/{dataset_id}")
    
    meta = data.get("dataset_metadata", data)
    title = meta.get("title", "N/A")
    desc = meta.get("description", "N/A") or "N/A"
    keywords = meta.get("keyword", [])
    publisher = meta.get("publisher", "")
    license_info = meta.get("license", "")
    
    print(f"\n📊 Dataset: {title}")
    print(f"   ID: {dataset_id}")
    print(f"   URL: https://opendata.vancouver.ca/explore/dataset/{dataset_id}")
    print(f"   Description: {desc[:400]}")
    if keywords:
        print(f"   Keywords: {', '.join(keywords[:10])}")
    if publisher:
        print(f"   Publisher: {publisher}")
    if license_info:
        print(f"   License: {license_info}")
    
    # Fields
    fields = data.get("fields", meta.get("fields", []))
    if fields:
        print(f"\n   Fields ({len(fields)}):")
        for f in fields:
            name = f.get("name", "?")
            label = f.get("label", name)
            ftype = f.get("type", "?")
            print(f"     • {label} ({name}) — {ftype}")
    
    # Alternative exports
    exports = data.get("alternative_exports", [])
    if exports:
        print(f"\n   Exports ({len(exports)}):")
        for e in exports:
            print(f"     • {e.get('title', '?')} [{e.get('mimetype', '?')}]")
    
    print()

def cmd_fetch(dataset_id, options):
    """Fetch data rows from a dataset."""
    params = {}
    if options.get("limit"):
        params["limit"] = options["limit"]
    if options.get("offset"):
        params["offset"] = options["offset"]
    if options.get("where"):
        params["where"] = options["where"]
    if options.get("select"):
        params["select"] = options["select"]
    if options.get("order_by"):
        params["order_by"] = options["order_by"]
    
    params.setdefault("limit", 10)
    
    data = api_request(f"/catalog/datasets/{dataset_id}/records", params)
    results = data.get("results", [])
    
    if not results:
        print("No data returned.")
        return
    
    # Flatten nested objects
    rows = []
    for r in results:
        # The actual data might be in a 'fields' key or directly in the result
        if "fields" in r:
            rows.append(r["fields"])
        else:
            rows.append(r)
    
    if options.get("csv"):
        keys = list(rows[0].keys())
        print(",".join(keys))
        for row in rows:
            vals = [str(row.get(k, "")).replace(",", ";").replace("\n", " ") for k in keys]
            print(",".join(vals))
    else:
        print(json.dumps(rows, indent=2, default=str))

# --- CLI ---

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "search" and len(sys.argv) >= 3:
        cmd_search(" ".join(sys.argv[2:]))
    elif cmd == "list":
        cmd_list()
    elif cmd == "info" and len(sys.argv) >= 3:
        cmd_info(sys.argv[2])
    elif cmd == "fetch" and len(sys.argv) >= 3:
        dataset_id = sys.argv[2]
        options = {}
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--limit" and i + 1 < len(args):
                options["limit"] = args[i + 1]; i += 2
            elif args[i] == "--offset" and i + 1 < len(args):
                options["offset"] = args[i + 1]; i += 2
            elif args[i] == "--where" and i + 1 < len(args):
                options["where"] = args[i + 1]; i += 2
            elif args[i] == "--select" and i + 1 < len(args):
                options["select"] = args[i + 1]; i += 2
            elif args[i] == "--order" and i + 1 < len(args):
                options["order_by"] = args[i + 1]; i += 2
            elif args[i] == "--csv":
                options["csv"] = True; i += 1
            else:
                i += 1
        cmd_fetch(dataset_id, options)
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
