#!/usr/bin/env python3
"""Validate scoped_state_keys for each node."""

import argparse
import json
import sys
from pathlib import Path


def validate_scope(plan_path: str) -> dict:
    """Validate that each node has valid scoped_state_keys."""
    with open(plan_path) as f:
        plan = json.load(f)

    plan_ir = plan.get("plan_ir", {})
    nodes = plan_ir.get("nodes", [])

    errors = []
    warnings = []

    # Identify entry nodes (nodes that appear in entry_nodes or have no incoming edges)
    entry_node_ids = set(plan_ir.get("entry_nodes", []))
    if not entry_node_ids:
        edge_targets = {e["to_node"] for e in edges}
        entry_node_ids = {n["node_id"] for n in nodes if n["node_id"] not in edge_targets}

    # All output keys from upstream nodes
    all_available_keys = set()
    for node in nodes:
        node_id = node["node_id"]
        scoped = node.get("scoped_state_keys", [])

        # Entry nodes may have empty scoped_state_keys (no upstream dependency)
        # Non-entry nodes must declare scoped_state_keys
        if not scoped and node_id not in entry_node_ids:
            errors.append(f"Node {node_id}: scoped_state_keys is empty (non-entry node must declare state keys)")
            continue
        elif not scoped:
            # Entry node with empty scoped_state_keys — warn but don't error
            warnings.append(f"Node {node_id}: scoped_state_keys is empty (entry node, consider declaring expected outputs)")
            continue

        for key in scoped:
            all_available_keys.add(f"{node_id}.{key}")

    # Check input_mapping references
    for node in nodes:
        node_id = node["node_id"]
        input_mapping = node.get("input_mapping", {})
        for key, ref in input_mapping.items():
            if ref not in all_available_keys:
                # Check if it's a global key (no dot)
                if "." not in ref:
                    warnings.append(f"Node {node_id}: input_mapping references global key '{ref}'")
                else:
                    errors.append(f"Node {node_id}: input_mapping references non-existent key '{ref}'")

    return {
        "scope_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def main():
    parser = argparse.ArgumentParser(description="Validate scoped state keys")
    parser.add_argument("--plan", required=True, help="Plan JSON file")
    args = parser.parse_args()

    result = validate_scope(args.plan)

    if result["scope_valid"]:
        print("✅ Scope validation passed")
    else:
        print(f"❌ Scope validation failed ({len(result['errors'])} errors)")
        for err in result["errors"]:
            print(f"  - {err}")
    
    for w in result["warnings"]:
        print(f"  ⚠️ {w}")

    with open(args.plan) as f:
        plan = json.load(f)
    
    if "validation_report" not in plan:
        plan["validation_report"] = {}
    plan["validation_report"]["scope_valid"] = result["scope_valid"]
    plan["validation_report"].setdefault("errors", []).extend(result["errors"])
    plan["validation_report"].setdefault("warnings", []).extend(result["warnings"])
    
    with open(args.plan, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    sys.exit(0 if result["scope_valid"] else 1)


if __name__ == "__main__":
    main()
