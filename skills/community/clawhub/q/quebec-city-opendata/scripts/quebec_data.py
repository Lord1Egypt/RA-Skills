#!/usr/bin/env python3
"""
Ville de Québec Open Data — CLI for the CKAN API.
No dependencies beyond stdlib. Accesses donneesquebec.ca.

Usage:
  python3 quebec_data.py <command> [args]

Commands:
  search <query>                    Search datasets by keyword
  list                              List all datasets
  info <dataset-id>                 Show dataset metadata
  fetch <dataset-id> [options]      Fetch data from CKAN datastore
  searchable                        List datasets with datastore resources
"""

import json
import sys
import os
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

CKAN_API = "https://www.donneesquebec.ca/api/3/action"
ORG_ID = "ville-de-quebec"

def api_request(endpoint, params=None):
    """Make a request to the CKAN API."""
    url = f"{CKAN_API}/{endpoint}"
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
    """Fetch the dataset list for Ville de Québec (cached for 1 hour)."""
    cache_dir = os.path.expanduser("~/.openclaw/workspace/data/quebec-city-opendata")
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, "catalog_cache.json")
    
    if os.path.exists(cache_file):
        age = datetime.now().timestamp() - os.path.getmtime(cache_file)
        if age < 3600:
            return json.loads(open(cache_file).read())
    
    data = api_request("package_search", {"fq": f"organization:{ORG_ID}", "rows": 100})
    results = data.get("result", {}).get("results", [])
    
    datasets = []
    for pkg in results:
        datasets.append({
            "name": pkg.get("name", ""),
            "title": pkg.get("title", ""),
            "notes": (pkg.get("notes") or "")[:100],
            "resources": len(pkg.get("resources", [])),
            "datastore_resources": len([r for r in pkg.get("resources", []) if r.get("datastore_active")]),
            "tags": [t.get("display_name", t.get("name", "")) for t in pkg.get("tags", [])[:5]]
        })
    
    with open(cache_file, "w") as f:
        json.dump(datasets, f)
    return datasets

# --- Commands ---

def cmd_search(query):
    """Search datasets by name or description."""
    datasets = load_catalog()
    query_lower = query.lower()
    matches = [d for d in datasets if query_lower in d.get("title", "").lower() or query_lower in d.get("name", "").lower() or query_lower in d.get("notes", "").lower()]
    
    if not matches:
        print(f"Aucun dataset trouvé pour '{query}'.")
        return
    
    print(f"\n🔍 Résultats pour '{query}' — {len(matches)} trouvé(s)\n")
    for d in matches:
        title = d.get("title", "?")
        name = d.get("name", "")
        ds_count = d.get("datastore_resources", 0)
        queryable = f" [{ds_count} requêtable]" if ds_count else ""
        print(f"  • {title}{queryable}")
        print(f"    ID: {name}")
        print(f"    https://www.donneesquebec.ca/dataset/{name}")
    print()

def cmd_list():
    """List all datasets."""
    datasets = load_catalog()
    
    print(f"\n📁 Ville de Québec — {len(datasets)} datasets\n")
    for d in sorted(datasets, key=lambda x: x.get("title", "")):
        title = d.get("title", "N/A")
        name = d.get("name", "")
        r_count = d.get("resources", 0)
        ds_count = d.get("datastore_resources", 0)
        queryable = f" [{ds_count} DS]" if ds_count else ""
        print(f"  • {title} ({r_count} res{queryable}) — {name}")
    print()

def cmd_searchable():
    """List datasets with datastore resources."""
    datasets = load_catalog()
    queryable = [d for d in datasets if d.get("datastore_resources", 0) > 0]
    
    print(f"\n📊 Datasets requêtables (CKAN Datastore) — {len(queryable)} of {len(datasets)}\n")
    for d in sorted(queryable, key=lambda x: -x.get("datastore_resources", 0)):
        title = d.get("title", "?")
        name = d.get("name", "")
        ds_count = d.get("datastore_resources", 0)
        print(f"  • {title} [{ds_count} resources]")
        print(f"    ID: {name}")
    print()

def cmd_info(dataset_id):
    """Show metadata for a dataset."""
    data = api_request("package_show", {"id": dataset_id})
    pkg = data.get("result", {})
    
    print(f"\n📊 Dataset: {pkg.get('title', 'N/A')}")
    print(f"   ID: {dataset_id}")
    print(f"   URL: https://www.donneesquebec.ca/dataset/{dataset_id}")
    print(f"   Description: {(pkg.get('notes') or 'N/A')[:400]}")
    
    tags = [t.get("display_name", "") for t in pkg.get("tags", [])]
    if tags:
        print(f"   Mots-clés: {', '.join(tags[:10])}")
    
    org = pkg.get("organization", {})
    if org:
        print(f"   Organisation: {org.get('title', '?')}")
    
    license_info = pkg.get("license_title", "")
    if license_info:
        print(f"   Licence: {license_info}")
    
    # Resources
    resources = pkg.get("resources", [])
    if resources:
        print(f"\n   Resources ({len(resources)}):")
        for r in resources:
            name = r.get("name", "?")
            fmt = r.get("format", "?")
            rid = r.get("id", "")
            ds = " [Datastore]" if r.get("datastore_active") else ""
            url = (r.get("url") or "")[:80]
            print(f"     • [{fmt}]{ds} {name}")
            print(f"       ID: {rid}")
            if url:
                print(f"       {url}")
    print()

def cmd_fetch(dataset_id, options):
    """Fetch data from CKAN datastore."""
    # Get dataset to find datastore resource
    data = api_request("package_show", {"id": dataset_id})
    pkg = data.get("result", {})
    resources = pkg.get("resources", [])
    
    # Find first datastore-enabled resource
    ds_resources = [r for r in resources if r.get("datastore_active")]
    if not ds_resources:
        print(f"Erreur: Aucune resource requêtable dans '{dataset_id}'.")
        print("Utilisez 'info' pour voir les liens de téléchargement.")
        sys.exit(1)
    
    target = ds_resources[0]
    resource_id = target["id"]
    
    # Query datastore
    params = {
        "resource_id": resource_id,
        "limit": int(options.get("limit", 10))
    }
    
    data = api_request("datastore_search", params)
    result = data.get("result", {})
    records = result.get("records", [])
    
    if not records:
        print("Aucune donnée retournée.")
        return
    
    if options.get("csv"):
        keys = list(records[0].keys())
        print(",".join(keys))
        for row in records:
            vals = [str(row.get(k, "")).replace(",", ";").replace("\n", " ") for k in keys]
            print(",".join(vals))
    else:
        print(json.dumps(records, indent=2, default=str))

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
    elif cmd == "searchable":
        cmd_searchable()
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
