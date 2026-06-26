#!/usr/bin/env python3
from __future__ import annotations

import argparse

from common import load_tree, run_path


def sort_key(node_id: str):
    return [int(p) for p in node_id.split('.')]


def main() -> int:
    parser = argparse.ArgumentParser(description='Render a readable task tree from tree.json.')
    parser.add_argument('--run', required=True, help='Run directory')
    args = parser.parse_args()

    tree = load_tree(run_path(args.run))
    nodes = tree['nodes']

    print(f"# Run {tree['runId']}")
    print(f"Task: {tree['task']}")
    print(f"Mode: {tree['mode']} | Status: {tree['status']} | Max depth: {tree['maxDepth']}")
    print()

    for node_id in sorted(nodes.keys(), key=sort_key):
        node = nodes[node_id]
        indent = '  ' * node.get('depth', 0)
        print(
            f"{indent}- {node_id} [{node.get('status')}] "
            f"{node.get('type')}/{node.get('executor')} "
            f"conf={node.get('confidence', 'unknown')} "
            f"goal={node.get('goal', '')}"
        )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
