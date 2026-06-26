#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def run_path(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def tree_path(run_dir: str | Path) -> Path:
    return run_path(run_dir) / 'tree.json'


def events_path(run_dir: str | Path) -> Path:
    return run_path(run_dir) / 'events.jsonl'


def node_dir(run_dir: str | Path, node_id: str) -> Path:
    return run_path(run_dir) / 'nodes' / node_id


def spec_path(run_dir: str | Path, node_id: str) -> Path:
    return node_dir(run_dir, node_id) / 'spec.json'


def notes_path(run_dir: str | Path, node_id: str) -> Path:
    return node_dir(run_dir, node_id) / 'notes.md'


def result_path(run_dir: str | Path, node_id: str) -> Path:
    return node_dir(run_dir, node_id) / 'result.md'


def ensure_node_files(run_dir: str | Path, node_id: str) -> None:
    nd = node_dir(run_dir, node_id)
    nd.mkdir(parents=True, exist_ok=True)
    sp = spec_path(run_dir, node_id)
    np = notes_path(run_dir, node_id)
    rp = result_path(run_dir, node_id)
    if not np.exists():
        np.write_text(f'# Notes for node {node_id}\n', encoding='utf-8')
    if not rp.exists():
        rp.write_text('', encoding='utf-8')
    if not sp.exists():
        sp.write_text('{}\n', encoding='utf-8')


def load_tree(run_dir: str | Path) -> Dict[str, Any]:
    p = tree_path(run_dir)
    if not p.exists():
        raise FileNotFoundError(f'Missing tree.json at {p}')
    return json.loads(p.read_text(encoding='utf-8'))


def save_tree(run_dir: str | Path, tree: Dict[str, Any]) -> None:
    tree['updatedAt'] = now_iso()
    tree_path(run_dir).write_text(json.dumps(tree, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def update_run_status(tree: Dict[str, Any]) -> None:
    nodes = tree.get('nodes', {})
    if not nodes:
        tree['status'] = 'planned'
        return
    statuses = {n.get('status', 'planned') for n in nodes.values()}
    if statuses <= {'completed'}:
        tree['status'] = 'completed'
    elif 'waiting_for_approval' in statuses:
        tree['status'] = 'waiting_for_approval'
    elif 'running' in statuses or 'blocked' in statuses or 'planned' in statuses:
        tree['status'] = 'running'
    elif 'failed' in statuses:
        tree['status'] = 'failed'
    else:
        tree['status'] = 'planned'


def write_spec(run_dir: str | Path, node: Dict[str, Any]) -> None:
    ensure_node_files(run_dir, node['id'])
    spec_path(run_dir, node['id']).write_text(json.dumps(node, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def append_note(run_dir: str | Path, node_id: str, text: str) -> None:
    ensure_node_files(run_dir, node_id)
    with notes_path(run_dir, node_id).open('a', encoding='utf-8') as f:
        f.write(f'\n## {now_iso()}\n\n{text.rstrip()}\n')


def next_event_seq(run_dir: str | Path) -> int:
    ep = events_path(run_dir)
    if not ep.exists() or ep.stat().st_size == 0:
        return 1
    last_line = ''
    with ep.open('r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                last_line = line
    if not last_line:
        return 1
    try:
        return int(json.loads(last_line).get('seq', 0)) + 1
    except Exception:
        return 1


def append_event(run_dir: str | Path, event_type: str, task_id: str | None = None, data: Dict[str, Any] | None = None) -> Dict[str, Any]:
    ep = events_path(run_dir)
    ep.parent.mkdir(parents=True, exist_ok=True)
    event = {
        'ts': now_iso(),
        'seq': next_event_seq(run_dir),
        'type': event_type,
        'task_id': task_id,
        'data': data or {},
    }
    with ep.open('a', encoding='utf-8') as f:
        f.write(json.dumps(event, sort_keys=True) + '\n')
    return event
