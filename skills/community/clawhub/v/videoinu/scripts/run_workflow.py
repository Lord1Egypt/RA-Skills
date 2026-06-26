#!/usr/bin/env python3
"""
Run a workflow definition.

Usage:
    # Run in existing graph
    python3 run_workflow.py DEFINITION_ID --graph-id GRAPH_ID --inputs '{"slot": {"type":"core_node_refs","core_node_ids":["id1"]}}'

    # Run and create a new graph
    python3 run_workflow.py DEFINITION_ID --new-graph "Result Graph" --inputs '{...}'

    # List available workflow definitions
    python3 run_workflow.py --list

Output (JSON):
    {
      "instance_id": "...",
      "graph_id": "...",
      "graph_url": "..."
    }
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import require_access_key, api_get, api_post, build_graph_url


def list_definitions():
    data = api_get("/wf/definition/list", params={"page": 1, "page_size": 50, "include_public": "true"})
    items = data.get("items", []) if isinstance(data, dict) else data
    definitions = []
    for d in (items if isinstance(items, list) else []):
        definitions.append({
            "id": d.get("id", ""),
            "name": d.get("name", ""),
            "description": d.get("description", ""),
            "public": d.get("public", False),
        })
    return definitions


def main():
    parser = argparse.ArgumentParser(description="Run a workflow")
    parser.add_argument("definition_id", nargs="?", help="Workflow definition ID")
    parser.add_argument("--list", action="store_true", help="List available workflow definitions")
    parser.add_argument("--graph-id", help="Run in existing graph")
    parser.add_argument("--new-graph", help="Create new graph with this name")
    parser.add_argument("--inputs", default="{}", help="JSON string of input values")
    parser.add_argument("--count", type=int, default=1, help="Number of runs (default 1)")
    args = parser.parse_args()

    require_access_key()

    if args.list:
        defs = list_definitions()
        print(json.dumps({"definitions": defs}, indent=2))
        return

    if not args.definition_id:
        parser.error("DEFINITION_ID is required unless --list is used")

    try:
        inputs = json.loads(args.inputs)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid --inputs JSON: {e}"}))
        sys.exit(1)

    if args.new_graph:
        data = api_post("/wf/instance/run_create_graph", body={
            "definition_id": args.definition_id,
            "inputs": inputs,
            "graph_name": args.new_graph,
        })
        result = {
            "instance_id": data.get("instance_id", ""),
            "graph_id": data.get("graph_id", ""),
            "graph_url": build_graph_url(data.get("graph_id", "")),
        }
    elif args.graph_id:
        data = api_post("/wf/instance/run_in_graph", body={
            "definition_id": args.definition_id,
            "inputs": inputs,
            "graph_id": args.graph_id,
            "count": args.count,
        })
        instance_ids = data.get("instance_ids", [])
        result = {
            "instance_ids": instance_ids,
            "graph_id": args.graph_id,
            "graph_url": build_graph_url(args.graph_id),
        }
    else:
        parser.error("Either --graph-id or --new-graph is required")
        return

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
