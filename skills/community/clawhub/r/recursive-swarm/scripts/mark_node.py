#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from common import append_event, append_note, load_tree, now_iso, result_path, run_path, save_tree, update_run_status, write_spec


def main() -> int:
    parser = argparse.ArgumentParser(description='Update node status, confidence, notes, or result text.')
    parser.add_argument('--run', required=True, help='Run directory')
    parser.add_argument('--id', required=True, help='Node id')
    parser.add_argument('--status', choices=['planned', 'running', 'completed', 'failed', 'waiting_for_approval', 'blocked'])
    parser.add_argument('--confidence', choices=['unknown', 'low', 'medium', 'high'])
    parser.add_argument('--summary')
    parser.add_argument('--note', help='Append note text to notes.md')
    parser.add_argument('--result-file', help='Copy file contents into result.md')
    parser.add_argument('--result-text', help='Write inline text into result.md')
    args = parser.parse_args()

    run_dir = run_path(args.run)
    tree = load_tree(run_dir)
    nodes = tree['nodes']
    if args.id not in nodes:
        raise SystemExit(f'Unknown node id: {args.id}')

    node = nodes[args.id]
    previous_status = node.get('status', 'planned')
    if args.status:
        node['status'] = args.status
    if args.confidence:
        node['confidence'] = args.confidence
    if args.summary is not None:
        node['summary'] = args.summary
    node['updatedAt'] = now_iso()

    if args.note:
        append_note(run_dir, args.id, args.note)
        append_event(run_dir, 'note_recorded', args.id, {'note': args.note})
    if args.result_file:
        content = run_path(args.result_file).read_text(encoding='utf-8')
        result_path(run_dir, args.id).write_text(content, encoding='utf-8')
        append_event(run_dir, 'result_recorded', args.id, {'source': str(run_path(args.result_file))})
    elif args.result_text is not None:
        result_path(run_dir, args.id).write_text(args.result_text, encoding='utf-8')
        append_event(run_dir, 'result_recorded', args.id, {'source': 'inline'})

    write_spec(run_dir, node)
    update_run_status(tree)
    save_tree(run_dir, tree)
    append_event(
        run_dir,
        'task_status_changed' if args.status and args.status != previous_status else 'task_touched',
        args.id,
        {
            'from': previous_status,
            'to': node.get('status'),
            'confidence': node.get('confidence'),
            'summary': node.get('summary', ''),
        },
    )
    print(json.dumps(node, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
