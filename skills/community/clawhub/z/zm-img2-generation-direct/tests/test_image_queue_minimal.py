#!/usr/bin/env python3
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2].parent
SCRIPT = ROOT / 'skills/happy-img2-direct/scripts/image_queue.py'


def run_queue(payload, *args, expect=0):
    td = tempfile.TemporaryDirectory(prefix='imgq-test-')
    state = pathlib.Path(td.name) / 'state'
    inp = pathlib.Path(td.name) / 'tasks.json'
    inp.write_text(json.dumps(payload), encoding='utf-8')
    cmd = [sys.executable, str(SCRIPT), 'run', '--state-dir', str(state), *args, '@' + str(inp)]
    cp = subprocess.run(cmd, cwd=str(ROOT), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    assert cp.returncode == expect, (cp.returncode, cp.stdout, cp.stderr)
    return json.loads(cp.stdout), state, td


def test_max_workers_and_out_of_order_mapping():
    tasks = [{'task_name': f't{i}', 'task_key': f'k{i}', 'mock_sleep': s} for i, s in enumerate([0.4, 0.1, 0.3, 0.05, 0.2])]
    summary, state, _td = run_queue({'tasks': tasks}, '--max-workers', '2', '--max-queue-size', '10')
    assert summary['ok'] is True
    assert summary['counters']['completed'] == 5
    data = json.loads((state / 'queue_state.json').read_text())
    for task in data['tasks'].values():
        assert task['status'] == 'completed'
        assert task['task_key'].replace('k', 't') == task['task_name']
        assert task.get('worker_id')
        assert task.get('pid')
        assert pathlib.Path(task['stdout']).exists()
        assert pathlib.Path(task['stderr']).exists()
        assert pathlib.Path(task['result_json']).exists()


def test_timeout_kills_and_releases_slot():
    summary, state, _td = run_queue({'tasks': [{'task_name': 'slow', 'task_key': 'slow', 'mock_sleep': 5}]}, '--max-workers', '1', '--task-timeout-seconds', '2', expect=1)
    assert summary['ok'] is False
    assert summary['counters']['timed_out'] == 1
    data = json.loads((state / 'queue_state.json').read_text())
    task = next(iter(data['tasks'].values()))
    assert task['status'] == 'timed_out'
    assert data['running'] == {}
    assert data['workers'] == {}


def test_queue_full_rejected():
    tasks = [{'task_name': f't{i}', 'task_key': f'k{i}', 'mock_sleep': 0.01} for i in range(4)]
    summary, _state, _td = run_queue({'tasks': tasks}, '--max-workers', '1', '--max-queue-size', '2', expect=1)
    assert summary['ok'] is False
    assert summary['counters']['rejected'] == 1
    assert summary['counters']['completed'] == 3


def test_duplicate_task_key_skipped():
    tasks = [
        {'task_name': 'a', 'task_key': 'dup', 'mock_sleep': 0.01},
        {'task_name': 'b', 'task_key': 'dup', 'mock_sleep': 0.01},
    ]
    summary, _state, _td = run_queue({'tasks': tasks}, '--max-workers', '2', expect=1)
    assert summary['ok'] is False
    assert summary['counters']['skipped'] == 1
    assert summary['counters']['completed'] == 1


if __name__ == '__main__':
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    for t in tests:
        t()
        print(f'PASS {t.__name__}')
