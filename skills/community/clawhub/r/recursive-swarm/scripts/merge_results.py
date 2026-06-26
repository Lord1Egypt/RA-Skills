#!/usr/bin/env python3
from __future__ import annotations

import argparse

from common import append_event, load_tree, node_dir, result_path, run_path


def main() -> int:
    parser = argparse.ArgumentParser(description='Bundle child result.md files into one merge input document.')
    parser.add_argument('--run', required=True, help='Run directory')
    parser.add_argument('--id', required=True, help='Parent node id')
    parser.add_argument('--out', help='Optional output path; defaults to nodes/<id>/merged-children.md')
    args = parser.parse_args()

    run_dir = run_path(args.run)
    tree = load_tree(run_dir)
    nodes = tree['nodes']
    if args.id not in nodes:
        raise SystemExit(f'Unknown node id: {args.id}')
    node = nodes[args.id]
    children = node.get('children', [])
    if not children:
        raise SystemExit('Node has no children to merge')

    out_path = run_path(args.out) if args.out else node_dir(run_dir, args.id) / 'merged-children.md'
    parts = [f"# Merged child results for node {args.id}\n", f"Parent goal: {node.get('goal', '')}\n"]
    for child_id in children:
        parts.append(f"\n## Child {child_id} — {nodes[child_id].get('goal', '')}\n")
        rp = result_path(run_dir, child_id)
        if rp.exists() and rp.read_text(encoding='utf-8').strip():
            parts.append(rp.read_text(encoding='utf-8'))
        else:
            parts.append('_No result.md content found._\n')

    out_path.write_text('\n'.join(parts).rstrip() + '\n', encoding='utf-8')
    append_event(run_dir, 'results_merged', args.id, {
        'out': str(out_path.relative_to(run_dir)),
        'children': children,
    })
    print(out_path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
