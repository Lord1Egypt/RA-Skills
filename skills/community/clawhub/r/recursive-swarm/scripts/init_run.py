#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re

from common import append_event, ensure_node_files, events_path, now_iso, result_path, run_path, save_tree, spec_path, tree_path, write_spec


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')[:48] or 'run'


def main() -> int:
    parser = argparse.ArgumentParser(description='Initialize a recursive-swarm run folder.')
    parser.add_argument('task', help='Root task / user request')
    parser.add_argument('--runs-dir', default='.', help='Directory that will contain the run folder')
    parser.add_argument('--run-id', help='Optional explicit run id')
    parser.add_argument('--mode', default='mixed', choices=['research', 'coding', 'ops', 'browser', 'mixed'])
    parser.add_argument('--max-depth', type=int, default=2)
    parser.add_argument('--fanout', type=int, default=3)
    parser.add_argument('--concurrency', type=int, default=3)
    parser.add_argument('--max-nodes', type=int, default=9)
    parser.add_argument('--root-type', default='synthesis', choices=['research', 'coding', 'ops', 'browser', 'synthesis', 'review'])
    parser.add_argument('--root-executor', default='subagent')
    args = parser.parse_args()

    if args.max_depth < 1 or args.max_depth > 3:
        raise SystemExit('--max-depth must be between 1 and 3')
    if args.fanout < 1 or args.fanout > 5:
        raise SystemExit('--fanout must be between 1 and 5')
    if args.concurrency < 1 or args.concurrency > 5:
        raise SystemExit('--concurrency must be between 1 and 5')
    if args.max_nodes < 1 or args.max_nodes > 15:
        raise SystemExit('--max-nodes must be between 1 and 15')

    run_id = args.run_id or f"{now_iso().replace(':', '').replace('-', '').lower()}-{slugify(args.task)}"
    run_dir = run_path(args.runs_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / 'nodes').mkdir(parents=True, exist_ok=True)
    events_path(run_dir).write_text('', encoding='utf-8')

    root_node = {
        'id': '1',
        'parentId': None,
        'goal': args.task,
        'type': args.root_type,
        'executor': args.root_executor,
        'status': 'planned',
        'depth': 0,
        'children': [],
        'dependsOn': [],
        'confidence': 'unknown',
        'approvalRequired': False,
        'workspaceMode': 'artifacts',
        'artifacts': [
            str(spec_path(run_dir, '1').relative_to(run_dir)),
            str(result_path(run_dir, '1').relative_to(run_dir)),
        ],
        'createdAt': now_iso(),
        'updatedAt': now_iso(),
        'summary': '',
    }

    tree = {
        'version': 1,
        'runId': run_id,
        'task': args.task,
        'mode': args.mode,
        'status': 'planned',
        'rootNodeId': '1',
        'maxDepth': args.max_depth,
        'createdAt': now_iso(),
        'updatedAt': now_iso(),
        'defaults': {
            'fanout': args.fanout,
            'concurrency': args.concurrency,
            'maxNodes': args.max_nodes,
            'workspaceMode': 'artifacts',
            'allowWorktrees': True,
        },
        'nodes': {'1': root_node},
    }

    ensure_node_files(run_dir, '1')
    write_spec(run_dir, root_node)
    (run_dir / 'summary.md').write_text(f'# Run {run_id}\n\nTask: {args.task}\n', encoding='utf-8')
    save_tree(run_dir, tree)
    append_event(run_dir, 'run_initialized', None, {
        'runId': run_id,
        'task': args.task,
        'mode': args.mode,
        'maxDepth': args.max_depth,
        'fanout': args.fanout,
        'concurrency': args.concurrency,
        'maxNodes': args.max_nodes,
    })
    append_event(run_dir, 'task_added', '1', {
        'goal': args.task,
        'type': args.root_type,
        'executor': args.root_executor,
        'depth': 0,
    })

    print(json.dumps({
        'runDir': str(run_dir),
        'tree': str(tree_path(run_dir)),
        'events': str(events_path(run_dir)),
    }, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
