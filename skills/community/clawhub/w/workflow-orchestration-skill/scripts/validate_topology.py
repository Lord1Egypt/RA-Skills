#!/usr/bin/env python3
"""Validate DAG topology: cycle detection, reference integrity, limits."""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def validate_topology(plan_path: str, constraints: dict = None) -> dict:
    """Validate DAG structure."""
    with open(plan_path) as f:
        plan = json.load(f)

    plan_ir = plan.get("plan_ir", {})
    nodes = plan_ir.get("nodes", [])
    edges = plan_ir.get("edges", [])
    node_ids = {n["node_id"] for n in nodes}

    errors = []
    warnings = []

    # 1. Reference integrity
    for edge in edges:
        if edge["from_node"] not in node_ids:
            errors.append(f"Edge references non-existent node: {edge['from_node']}")
        if edge["to_node"] not in node_ids:
            errors.append(f"Edge references non-existent node: {edge['to_node']}")

    # 2. Cycle detection (DFS)
    graph = defaultdict(list)
    for edge in edges:
        graph[edge["from_node"]].append(edge["to_node"])

    def has_cycle(node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.discard(node)
        return False

    visited = set()
    for node_id in node_ids:
        if node_id not in visited:
            if has_cycle(node_id, visited, set()):
                errors.append("Cycle detected in DAG")
                break

    # 3. Node count / depth / parallelism limits
    if constraints:
        if len(nodes) > constraints.get("max_nodes", 20):
            errors.append(f"Node count {len(nodes)} exceeds max {constraints['max_nodes']}")
        
        # Calculate depth via BFS
        def calc_depth():
            in_deg = defaultdict(int)
            for edge in edges:
                in_deg[edge["to_node"]] += 1
            queue = [n for n in node_ids if in_deg[n] == 0]
            d = 0
            while queue:
                d += 1
                next_queue = []
                for node in queue:
                    for neighbor in graph.get(node, []):
                        in_deg[neighbor] -= 1
                        if in_deg[neighbor] == 0:
                            next_queue.append(neighbor)
                queue = next_queue
            return d

        depth = calc_depth()
        if depth > constraints.get("max_depth", 5):
            errors.append(f"DAG depth {depth} exceeds max {constraints['max_depth']}")

        # Check max_parallelism: max nodes at any single depth level
        if constraints.get("max_parallelism"):
            def calc_level_width():
                in_deg = defaultdict(int)
                for edge in edges:
                    in_deg[edge["to_node"]] += 1
                queue = [n for n in node_ids if in_deg[n] == 0]
                max_width = len(queue) if queue else 0
                while queue:
                    next_queue = []
                    for node in queue:
                        for neighbor in graph.get(node, []):
                            in_deg[neighbor] -= 1
                            if in_deg[neighbor] == 0:
                                next_queue.append(neighbor)
                    if len(next_queue) > max_width:
                        max_width = len(next_queue)
                    queue = next_queue
                return max_width

            max_width = calc_level_width()
            if max_width > constraints["max_parallelism"]:
                errors.append(f"Max parallelism {max_width} exceeds limit {constraints['max_parallelism']}")
    else:
        depth = None

    return {
        "dag_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "depth": depth if depth is not None else "not calculated"
    }


def main():
    parser = argparse.ArgumentParser(description="Validate DAG topology")
    parser.add_argument("--plan", required=True, help="Plan JSON file")
    parser.add_argument("--max-nodes", type=int, default=20)
    parser.add_argument("--max-depth", type=int, default=5)
    args = parser.parse_args()

    constraints = {"max_nodes": args.max_nodes, "max_depth": args.max_depth}
    result = validate_topology(args.plan, constraints)

    if result["dag_valid"]:
        print("✅ DAG validation passed")
    else:
        print(f"❌ DAG validation failed ({len(result['errors'])} errors)")
        for err in result["errors"]:
            print(f"  - {err}")
    
    print(f"  Nodes: {result['node_count']}, Edges: {result['edge_count']}, Depth: {result['depth']}")

    with open(args.plan) as f:
        plan = json.load(f)
    
    if "validation_report" not in plan:
        plan["validation_report"] = {}
    plan["validation_report"]["dag_valid"] = result["dag_valid"]
    plan["validation_report"].setdefault("errors", []).extend(result["errors"])
    plan["validation_report"].setdefault("warnings", []).extend(result["warnings"])
    
    with open(args.plan, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    sys.exit(0 if result["dag_valid"] else 1)


if __name__ == "__main__":
    main()
