#!/usr/bin/env python3
"""
List the user's graphs (projects).

Usage:
    python3 list_graphs.py [--page-size N] [--tag TAG]

Output (JSON):
    {
      "graphs": [
        { "id": "...", "name": "...", "cover_url": "...", "created_at": "...", "url": "..." }
      ],
      "has_more": false
    }
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import require_access_key, api_get, build_graph_url

def main():
    parser = argparse.ArgumentParser(description="List user graphs")
    parser.add_argument("--page-size", type=int, default=20, help="Number of graphs per page (default 20)")
    parser.add_argument("--page", type=int, default=1, help="Page number (default 1)")
    parser.add_argument("--tag", type=str, default=None, help="Filter by tag")
    args = parser.parse_args()

    require_access_key()

    params = {"page": args.page, "page_size": args.page_size}
    if args.tag:
        params["tag"] = args.tag

    data = api_get("/graph/list", params=params)
    graphs = data.get("graphs", [])

    result = {
        "graphs": [
            {
                "id": g["id"],
                "name": g.get("name", "Untitled"),
                "cover_url": g.get("cover_url", ""),
                "created_at": g.get("created_at", ""),
                "updated_at": g.get("updated_at", ""),
                "url": build_graph_url(g["id"]),
            }
            for g in graphs
        ],
        "has_more": data.get("has_more", False),
    }

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
