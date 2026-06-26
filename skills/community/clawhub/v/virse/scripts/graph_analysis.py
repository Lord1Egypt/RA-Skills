#!/usr/bin/env python3
"""Analyze a Virse canvas as a directed graph.

Reads `get_canvas` output from stdin or file. Zero external dependencies.

Usage:
    virse_call call get_canvas '{"canvas_id":"UUID"}' | python3 graph_analysis.py
    python3 graph_analysis.py canvas_output.txt
    python3 graph_analysis.py canvas_output.txt --format json
"""
import json
import re
import sys
from collections import deque


def parse_canvas(text):
    """Parse get_canvas output into nodes and edges.

    Each element line looks like:
      [short_id] type (x,y) WxH "label..." -> target1, target2
    or without edges:
      [short_id] type (x,y) WxH "label..."
    or without label:
      [short_id] type (x,y) WxH -> target1
      [short_id] type (x,y) WxH
    """
    nodes = {}  # id -> {type, x, y, w, h, label}
    out_edges = {}  # id -> [target_ids]
    in_edges = {}  # id -> [source_ids]

    # Pattern: [id] type (x,y) WxH optionally "label" optionally -> targets
    element_re = re.compile(
        r'^\s*\[([0-9a-f]+)\]\s+'     # [short_id]
        r'(\w+)\s+'                     # type
        r'\((-?[\d]+),(-?[\d]+)\)\s+'   # (x,y)
        r'([\d]+)x([\d]+)'             # WxH
        r'(?:\s+"((?:[^"\\]|\\.)*)")?'  # optional "label"
        r'(?:\s+->\s+(.+))?$'           # optional -> targets
    )

    for line in text.splitlines():
        m = element_re.match(line)
        if not m:
            continue

        nid = m.group(1)
        ntype = m.group(2)
        x, y = int(m.group(3)), int(m.group(4))
        w, h = int(m.group(5)), int(m.group(6))
        label = m.group(7) or ""
        targets_str = m.group(8) or ""

        nodes[nid] = {
            "type": ntype,
            "x": x, "y": y,
            "w": w, "h": h,
            "label": label[:80],  # truncate for readability
        }

        targets = [t.strip() for t in targets_str.split(",") if t.strip()] if targets_str else []
        out_edges[nid] = targets

        if nid not in in_edges:
            in_edges[nid] = []
        for t in targets:
            if t not in in_edges:
                in_edges[t] = []
            in_edges[t].append(nid)

    return nodes, out_edges, in_edges


def classify_nodes(nodes, out_edges, in_edges):
    """Classify nodes into roots, sinks, hubs, and isolated."""
    roots = []
    sinks = []
    hubs = []
    isolated = []

    for nid in nodes:
        out_deg = len(out_edges.get(nid, []))
        in_deg = len(in_edges.get(nid, []))
        total = out_deg + in_deg

        if in_deg == 0 and out_deg > 0:
            roots.append(nid)
        elif out_deg == 0 and in_deg > 0:
            sinks.append(nid)

        if total >= 4:
            hubs.append(nid)

        if total == 0:
            isolated.append(nid)

    return roots, sinks, hubs, isolated


def bfs_chain(start, out_edges, nodes):
    """BFS from start node, return ordered chain of (id, depth)."""
    visited = set()
    queue = deque([(start, 0)])
    chain = []

    while queue:
        nid, depth = queue.popleft()
        if nid in visited:
            continue
        visited.add(nid)
        chain.append((nid, depth))
        for target in out_edges.get(nid, []):
            if target not in visited and target in nodes:
                queue.append((target, depth + 1))

    return chain


def find_components(nodes, out_edges, in_edges):
    """Find connected components treating edges as undirected."""
    visited = set()
    components = []

    adj = {}
    for nid in nodes:
        adj[nid] = set()
    for nid, targets in out_edges.items():
        for t in targets:
            if nid in nodes and t in nodes:
                adj[nid].add(t)
                adj[t].add(nid)

    for nid in nodes:
        if nid in visited:
            continue
        component = []
        queue = deque([nid])
        while queue:
            curr = queue.popleft()
            if curr in visited:
                continue
            visited.add(curr)
            component.append(curr)
            for neighbor in adj.get(curr, []):
                if neighbor not in visited:
                    queue.append(neighbor)
        components.append(component)

    components.sort(key=len, reverse=True)
    return components


def node_summary(nid, nodes, in_edges, out_edges):
    """One-line summary of a node."""
    n = nodes.get(nid)
    if not n:
        return f"[{nid}] (not in canvas)"
    in_deg = len(in_edges.get(nid, []))
    out_deg = len(out_edges.get(nid, []))
    label = f' "{n["label"]}"' if n["label"] else ""
    return f'[{nid}] {n["type"]} in={in_deg} out={out_deg}{label}'


def format_text(nodes, out_edges, in_edges, roots, sinks, hubs, isolated, components):
    """Human-readable text output."""
    lines = []
    total_edges = sum(len(v) for v in out_edges.values())

    lines.append("=== Canvas Graph Analysis ===")
    lines.append(f"Nodes: {len(nodes)}  Edges: {total_edges}  Components: {len(components)}")
    lines.append(f"Roots: {len(roots)}  Sinks: {len(sinks)}  Hubs: {len(hubs)}  Isolated: {len(isolated)}")
    lines.append("")

    # Roots
    if roots:
        lines.append(f"--- Roots ({len(roots)}) — workflow entry points ---")
        for nid in roots:
            lines.append(f"  {node_summary(nid, nodes, in_edges, out_edges)}")
        lines.append("")

    # Hubs
    if hubs:
        lines.append(f"--- Hubs ({len(hubs)}) — highly connected (degree >= 4) ---")
        for nid in hubs:
            lines.append(f"  {node_summary(nid, nodes, in_edges, out_edges)}")
        lines.append("")

    # Sinks
    if sinks:
        lines.append(f"--- Sinks ({len(sinks)}) — terminal nodes ---")
        for nid in sinks:
            lines.append(f"  {node_summary(nid, nodes, in_edges, out_edges)}")
        lines.append("")

    # Chains from roots
    if roots:
        lines.append(f"--- Chains from roots ---")
        for root_id in roots:
            chain = bfs_chain(root_id, out_edges, nodes)
            max_depth = max(d for _, d in chain) if chain else 0
            lines.append(f"\nRoot [{root_id}] → depth {max_depth}, {len(chain)} nodes:")
            for nid, depth in chain:
                indent = "  " + "  " * depth
                n = nodes.get(nid, {})
                label = f' "{n.get("label", "")}"' if n.get("label") else ""
                targets = out_edges.get(nid, [])
                arrow = f" -> {', '.join(targets)}" if targets else ""
                lines.append(f'{indent}[{nid}] {n.get("type", "?")}{label}{arrow}')
        lines.append("")

    # Components
    if len(components) > 1:
        lines.append(f"--- Connected components ({len(components)}) ---")
        for i, comp in enumerate(components):
            types = {}
            for nid in comp:
                t = nodes.get(nid, {}).get("type", "?")
                types[t] = types.get(t, 0) + 1
            type_str = ", ".join(f"{v} {k}" for k, v in sorted(types.items(), key=lambda x: -x[1]))
            lines.append(f"  Component {i+1}: {len(comp)} nodes ({type_str})")
        lines.append("")

    # Isolated
    if isolated:
        lines.append(f"--- Isolated ({len(isolated)}) — no connections ---")
        if len(isolated) <= 20:
            for nid in isolated:
                lines.append(f"  {node_summary(nid, nodes, in_edges, out_edges)}")
        else:
            types = {}
            for nid in isolated:
                t = nodes.get(nid, {}).get("type", "?")
                types[t] = types.get(t, 0) + 1
            type_str = ", ".join(f"{v} {k}" for k, v in sorted(types.items(), key=lambda x: -x[1]))
            lines.append(f"  ({type_str})")
            lines.append(f"  First 10:")
            for nid in isolated[:10]:
                lines.append(f"    {node_summary(nid, nodes, in_edges, out_edges)}")

    return "\n".join(lines)


def format_json(nodes, out_edges, in_edges, roots, sinks, hubs, isolated, components):
    """JSON output."""
    total_edges = sum(len(v) for v in out_edges.values())

    def node_info(nid):
        n = nodes.get(nid, {})
        return {
            "id": nid,
            "type": n.get("type", ""),
            "label": n.get("label", ""),
            "in_degree": len(in_edges.get(nid, [])),
            "out_degree": len(out_edges.get(nid, [])),
            "position": {"x": n.get("x", 0), "y": n.get("y", 0)},
            "size": {"w": n.get("w", 0), "h": n.get("h", 0)},
        }

    chains = []
    for root_id in roots:
        chain = bfs_chain(root_id, out_edges, nodes)
        max_depth = max(d for _, d in chain) if chain else 0
        chains.append({
            "root": root_id,
            "depth": max_depth,
            "node_count": len(chain),
            "nodes": [{"id": nid, "depth": d} for nid, d in chain],
        })

    result = {
        "summary": {
            "total_nodes": len(nodes),
            "total_edges": total_edges,
            "components": len(components),
            "roots": len(roots),
            "sinks": len(sinks),
            "hubs": len(hubs),
            "isolated": len(isolated),
        },
        "roots": [node_info(nid) for nid in roots],
        "hubs": [node_info(nid) for nid in hubs],
        "sinks": [node_info(nid) for nid in sinks],
        "chains": chains,
        "components": [
            {"size": len(comp), "node_ids": comp}
            for comp in components
        ],
        "isolated": [node_info(nid) for nid in isolated],
    }

    return json.dumps(result, indent=2, ensure_ascii=False)


def main():
    # Parse args
    fmt = "text"
    input_file = None

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--format" and i + 1 < len(args):
            fmt = args[i + 1]
            i += 2
        elif not args[i].startswith("-"):
            input_file = args[i]
            i += 1
        else:
            print(f"Unknown option: {args[i]}", file=sys.stderr)
            sys.exit(1)

    # Read input
    if input_file:
        with open(input_file, "r") as f:
            text = f.read()
    else:
        if sys.stdin.isatty():
            print("Reading from stdin (pipe get_canvas output or pass a file path)...", file=sys.stderr)
        text = sys.stdin.read()

    # Parse and analyze
    nodes, out_edges, in_edges = parse_canvas(text)

    if not nodes:
        print("No elements found in input.", file=sys.stderr)
        sys.exit(1)

    roots, sinks, hubs, isolated = classify_nodes(nodes, out_edges, in_edges)
    components = find_components(nodes, out_edges, in_edges)

    # Output
    if fmt == "json":
        print(format_json(nodes, out_edges, in_edges, roots, sinks, hubs, isolated, components))
    else:
        print(format_text(nodes, out_edges, in_edges, roots, sinks, hubs, isolated, components))


if __name__ == "__main__":
    main()
