#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from common import append_event, ensure_node_files, load_tree, now_iso, result_path, run_path, save_tree, spec_path, update_run_status, write_spec


def parse_csv(values: list[str] | None) -> list[str]:
    if not values:
        return []
    out: list[str] = []
    for value in values:
        for piece in value.split(','):
            piece = piece.strip()
            if piece:
                out.append(piece)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description='Create or update a node in tree.json.')
    parser.add_argument('--run', required=True, help='Run directory')
    parser.add_argument('--id', required=True, help='Node id, e.g. 1.2')
    parser.add_argument('--parent-id')
    parser.add_argument('--goal')
    parser.add_argument('--type', choices=['research', 'coding', 'ops', 'browser', 'synthesis', 'review'])
    parser.add_argument('--executor')
    parser.add_argument('--status', choices=['planned', 'running', 'completed', 'failed', 'waiting_for_approval', 'blocked'])
    parser.add_argument('--depth', type=int)
    parser.add_argument('--confidence', choices=['unknown', 'low', 'medium', 'high'])
    parser.add_argument('--workspace-mode', choices=['artifacts', 'worktree'])
    parser.add_argument('--approval-required', action='store_true')
    parser.add_argument('--depends-on', action='append')
    parser.add_argument('--summary')
    parser.add_argument('--artifact', action='append')
    args = parser.parse_args()

    run_dir = run_path(args.run)
    tree = load_tree(run_dir)
    nodes: Dict[str, Dict[str, Any]] = tree['nodes']
    existing = nodes.get(args.id, {})
    creating = args.id not in nodes

    parent_id = args.parent_id if args.parent_id is not None else existing.get('parentId')
    if args.depth is not None:
        depth = args.depth
    elif parent_id:
        if parent_id not in nodes:
            raise SystemExit(f'Unknown parent id: {parent_id}')
        depth = nodes[parent_id]['depth'] + 1
    else:
        depth = existing.get('depth', 0)

    depends_on = parse_csv(args.depends_on) or existing.get('dependsOn', [])
    artifacts = list(dict.fromkeys((existing.get('artifacts', []) + (args.artifact or []))))
    if not artifacts:
        artifacts = [
            str(spec_path(run_dir, args.id).relative_to(run_dir)),
            str(result_path(run_dir, args.id).relative_to(run_dir)),
        ]

    node = {
        'id': args.id,
        'parentId': parent_id,
        'goal': args.goal if args.goal is not None else existing.get('goal', ''),
        'type': args.type if args.type is not None else existing.get('type', 'research'),
        'executor': args.executor if args.executor is not None else existing.get('executor', 'subagent'),
        'status': args.status if args.status is not None else existing.get('status', 'planned'),
        'depth': depth,
        'children': existing.get('children', []),
        'dependsOn': depends_on,
        'confidence': args.confidence if args.confidence is not None else existing.get('confidence', 'unknown'),
        'approvalRequired': args.approval_required or existing.get('approvalRequired', False),
        'workspaceMode': args.workspace_mode if args.workspace_mode is not None else existing.get('workspaceMode', 'artifacts'),
        'artifacts': artifacts,
        'createdAt': existing.get('createdAt', now_iso()),
        'updatedAt': now_iso(),
        'summary': args.summary if args.summary is not None else existing.get('summary', ''),
    }

    if not node['goal']:
        raise SystemExit('--goal is required when creating a new node')
    if depth > tree.get('maxDepth', 2):
        raise SystemExit(f'Node depth {depth} exceeds maxDepth {tree.get("maxDepth")}')
    max_nodes = int(tree.get('defaults', {}).get('maxNodes', 9))
    if creating and len(nodes) >= max_nodes:
        raise SystemExit(f'Adding node would exceed maxNodes {max_nodes}')

    nodes[args.id] = node
    ensure_node_files(run_dir, args.id)
    write_spec(run_dir, node)

    if parent_id:
        parent = nodes[parent_id]
        children = list(parent.get('children', []))
        if args.id not in children:
            children.append(args.id)
        parent['children'] = children
        parent['updatedAt'] = now_iso()
        write_spec(run_dir, parent)

    update_run_status(tree)
    save_tree(run_dir, tree)
    append_event(
        run_dir,
        'task_added' if creating else 'task_updated',
        args.id,
        {
            'goal': node['goal'],
            'type': node['type'],
            'executor': node['executor'],
            'depth': node['depth'],
            'parentId': node['parentId'],
            'status': node['status'],
            'workspaceMode': node['workspaceMode'],
            'approvalRequired': node['approvalRequired'],
        },
    )
    print(json.dumps(node, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
