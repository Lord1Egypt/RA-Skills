#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from typing import Any, Dict, List

from common import load_tree, run_path


TERMINAL_STATUSES = {'completed', 'failed', 'waiting_for_approval'}


def deps_satisfied(nodes: Dict[str, Dict[str, Any]], node: Dict[str, Any]) -> bool:
    for dep in node.get('dependsOn', []):
        if dep not in nodes or nodes[dep].get('status') != 'completed':
            return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description='List executable or mergeable nodes.')
    parser.add_argument('--run', required=True, help='Run directory')
    parser.add_argument('--include-mergeable', action='store_true', help='Include planned synthesis/review nodes whose children are complete')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    tree = load_tree(run_path(args.run))
    nodes: Dict[str, Dict[str, Any]] = tree['nodes']
    ready: List[Dict[str, Any]] = []

    for node_id in sorted(nodes.keys(), key=lambda x: [int(p) for p in x.split('.')]):
        node = nodes[node_id]
        if node.get('status') != 'planned':
            continue
        if not deps_satisfied(nodes, node):
            continue
        children = node.get('children', [])
        if not children:
            ready.append(node)
            continue
        if args.include_mergeable and node.get('type') in {'synthesis', 'review'}:
            if all(nodes[c].get('status') == 'completed' for c in children):
                ready.append(node)

    if args.limit:
        ready = ready[: args.limit]

    if args.json:
        print(json.dumps(ready, indent=2))
    else:
        for node in ready:
            print(f"{node['id']}\t{node['type']}\t{node['executor']}\t{node['goal']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
