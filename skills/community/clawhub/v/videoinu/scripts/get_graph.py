#!/usr/bin/env python3
"""
Get graph details with its view nodes and core nodes.
Filters out deleted nodes and irrelevant metadata for cleaner output.

Usage:
    python3 get_graph.py GRAPH_ID [--include-deleted]

Output (JSON):
    {
      "graph": { "id": "...", "name": "...", "url": "..." },
      "view_nodes": [ ... ],
      "core_nodes": [ ... ]
    }
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import require_access_key, api_get, build_graph_url

def summarize_core_node(node: dict) -> dict:
    """Extract the useful fields from a core node."""
    data = node.get("data", {})
    summary = {
        "id": node["id"],
        "type": node.get("type", ""),
        "created_at": node.get("created_at"),
    }

    if node.get("type") == "asset":
        summary["asset_type"] = data.get("asset_type", "")
        summary["source_type"] = data.get("source_type", "")
        if data.get("url"):
            summary["url"] = data["url"]
        if data.get("content"):
            # Truncate long text content for readability
            content = data["content"]
            summary["content"] = content[:500] + "..." if len(content) > 500 else content
        if data.get("metadata"):
            meta = data["metadata"]
            # Keep useful metadata, skip internal fields
            clean_meta = {}
            for k in ("width", "height", "duration", "format", "thumbnails", "covers"):
                if k in meta:
                    clean_meta[k] = meta[k]
            if clean_meta:
                summary["metadata"] = clean_meta
    elif node.get("type") == "operation":
        summary["operator_type"] = data.get("operator_type", "")
        summary["status"] = data.get("status", "")
        if data.get("error"):
            summary["error"] = data["error"]

    if node.get("async_task_id"):
        summary["async_task_id"] = node["async_task_id"]

    return summary


def summarize_view_node(node: dict) -> dict:
    """Extract the useful fields from a view node."""
    summary = {
        "id": node["id"],
        "position": node.get("position", {}),
        "core_refs": node.get("core_refs", []),
        "selected_core_id": node.get("selected_core_id"),
    }

    ui = node.get("ui_state", {})
    if ui:
        for field in ("label", "note", "expected_type", "color", "collapsed"):
            if ui.get(field) is not None:
                summary.setdefault("ui_state", {})[field] = ui[field]

    conns = node.get("input_connections", [])
    if conns:
        summary["input_connections"] = [
            {
                "slot_name": c.get("slot_name", ""),
                "from_view_id": c.get("from_view_id", ""),
                "from_slot": c.get("from_slot", ""),
            }
            for c in conns
            if not c.get("is_deleted")
        ]

    if node.get("group_id"):
        summary["group_id"] = node["group_id"]

    return summary


def main():
    parser = argparse.ArgumentParser(description="Get graph details")
    parser.add_argument("graph_id", help="Graph ID")
    parser.add_argument("--include-deleted", action="store_true", help="Include deleted nodes")
    args = parser.parse_args()

    require_access_key()

    data = api_get(f"/graph/{args.graph_id}")

    graph_info = data.get("graph", {})
    core_nodes = data.get("core_nodes", [])
    view_nodes = graph_info.get("view_nodes", [])

    # Filter deleted nodes
    if not args.include_deleted:
        view_nodes = [n for n in view_nodes if not n.get("is_deleted")]

    result = {
        "graph": {
            "id": graph_info.get("id", args.graph_id),
            "name": graph_info.get("name", ""),
            "url": build_graph_url(args.graph_id),
            "created_at": graph_info.get("created_at", ""),
            "updated_at": graph_info.get("updated_at", ""),
        },
        "view_nodes": [summarize_view_node(n) for n in view_nodes],
        "core_nodes": [summarize_core_node(n) for n in core_nodes],
    }

    # Include groups if present
    groups = graph_info.get("view_node_groups", [])
    if groups:
        result["groups"] = [
            {"id": g["id"], "name": g.get("name", ""), "node_ids": g.get("node_ids", [])}
            for g in groups
            if not g.get("is_deleted")
        ]

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
