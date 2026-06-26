#!/usr/bin/env python3
"""
Create a new graph (project).

Usage:
    python3 create_graph.py "My Graph Name" [--tag TAG ...]

Output (JSON):
    {
      "id": "...",
      "name": "...",
      "url": "..."
    }
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import require_access_key, api_post, build_graph_url


def main():
    parser = argparse.ArgumentParser(description="Create a new graph")
    parser.add_argument("name", help="Graph name")
    parser.add_argument("--tag", action="append", default=[], help="Tags (can be repeated)")
    args = parser.parse_args()

    require_access_key()

    tags = ["free-mode"] + args.tag
    body = {"name": args.name, "tags": tags}

    data = api_post("/graph", body=body)

    graph = data.get("graph", data) if isinstance(data, dict) else {}
    graph_id = graph.get("id", "")

    result = {
        "id": graph_id,
        "name": args.name,
        "url": build_graph_url(graph_id) if graph_id else "",
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
