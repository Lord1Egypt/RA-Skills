#!/usr/bin/env python3
"""Controlled queue/worker pool for happy-img2-direct.

This runner intentionally keeps the existing run.py/generate-image.js direct path intact.
It provides an observable bounded queue for callers that want controlled concurrency.
"""
import argparse
import concurrent.futures
import json
import os
import pathlib
import queue
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
import uuid
from collections import Counter

SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
WORKSPACE = pathlib.Path(os.environ.get('OPENCLAW_WORKSPACE', os.getcwd())).resolve()
RUNNER = SKILL_DIR / 'scripts/run.py'
DEFAULT_STATE_DIR = pathlib.Path(os.environ.get('OPENCLAW_IMAGE_QUEUE_DIR', '~/.openclaw/image-queue')).expanduser()
DEFAULT_OUTPUT_DIR = pathlib.Path(os.environ.get('OPENCLAW_IMAGE_QUEUE_OUTPUT_DIR', '~/.openclaw/generated-images')).expanduser()
DEFAULT_MAX_WORKERS = 4
MAX_WORKERS_LIMIT = 4
DEFAULT_TASK_TIMEOUT_SECONDS = 600
DEFAULT_MAX_QUEUE_SIZE = 100
HISTORY_LIMIT_DEFAULT = 200
ACTIVE_STATUSES = {'queued', 'running'}
TERMINAL_STATUSES = {'completed', 'failed', 'timed_out', 'rejected', 'skipped', 'orphan_late_output', 'cancelled'}
BAD_STATUSES = {'failed', 'timed_out', 'rejected', 'discarded', 'skipped', 'orphan_late_output', 'orphaned', 'cancelled', 'stuck'}
SECRET_PATTERNS = [
    (re.compile(r'sk-[A-Za-z0-9_\-]{8,}'), 'sk-***'),
    (re.compile(r'Bearer\s+[A-Za-z0-9_\.\-]+', re.I), 'Bearer ***'),
    (re.compile(r'(app_secret|appSecret|apiKey|api_key|token|secret)["\']?\s*[:=]\s*["\'][^"\']+', re.I), r'\1:"[redacted]'),
]


def iso_now():
    return time.strftime('%Y-%m-%dT%H:%M:%S%z')


def now_ts():
    return time.time()


def safe_text(value, limit=4000):
    s = str(value if value is not None else '')
    for pat, repl in SECRET_PATTERNS:
        s = pat.sub(repl, s)
    return s[-limit:]


def safe_name(value, default='task'):
    s = re.sub(r'[^A-Za-z0-9._-]+', '-', str(value or default)).strip('-._')
    return s[:80] or default


def prompt_summary(prompt, limit=180):
    s = re.sub(r'\s+', ' ', str(prompt or '')).strip()
    return s[:limit] + ('…' if len(s) > limit else '')


def read_json(path, default=None):
    try:
        return json.loads(pathlib.Path(path).read_text(encoding='utf-8'))
    except Exception:
        return default


def write_json(path, data):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f'.tmp-{os.getpid()}-{uuid.uuid4().hex[:6]}')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    os.replace(tmp, path)


def append_jsonl(path, data):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, sort_keys=True) + '\n')


def load_jsonl(path, limit=100):
    path = pathlib.Path(path)
    if not path.exists():
        return []
    with path.open('r', encoding='utf-8') as f:
        lines = f.readlines()
    rows = []
    for line in lines[-limit:]:
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
    return rows



def tail_text(path, limit=4000):
    path = pathlib.Path(path)
    if not path.exists():
        return ''
    try:
        with path.open('rb') as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - limit))
            data = f.read()
        return data.decode('utf-8', errors='replace')
    except Exception as e:
        return f'[tail failed: {e}]'


def find_task(state, ident):
    tasks = state.get('tasks') or {}
    if ident in tasks:
        return tasks[ident]
    for t in tasks.values():
        if t.get('task_key') == ident:
            return t
    return None

def bounded_int(value, default, lower, upper=None):
    try:
        n = int(value if value is not None else default)
    except Exception:
        n = default
    n = max(lower, n)
    return min(upper, n) if upper is not None else n


def task_id_for(task):
    return f"t-{time.strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:10]}"


def load_task_input(arg):
    if not arg:
        return {}
    if arg.startswith('@'):
        return read_json(arg[1:], {})
    p = pathlib.Path(arg)
    if p.exists():
        return read_json(p, {})
    return json.loads(arg)


def normalize_images(task):
    images = []
    for key in ('input_image', 'image', 'reference_image'):
        if task.get(key):
            images.append(str(task[key]))
    for key in ('input_images', 'images'):
        val = task.get(key)
        if not val:
            continue
        if isinstance(val, list):
            images.extend(str(x) for x in val)
        else:
            try:
                parsed = json.loads(str(val))
                if isinstance(parsed, list):
                    images.extend(str(x) for x in parsed)
                else:
                    images.append(str(parsed))
            except Exception:
                images.extend(x.strip() for x in str(val).split(',') if x.strip())
    return images


def normalize_task(raw, defaults, index=0):
    task = dict(raw or {})
    tid = task.get('task_id') or task_id_for(task)
    task_name = safe_name(task.get('task_name') or task.get('task-name') or task.get('name') or tid)
    task_key = str(task.get('task_key') or task.get('task-key') or task_name)
    prompt = task.get('prompt') or ''
    input_images = normalize_images(task)
    task_timeout_seconds = bounded_int(task.get('task_timeout_seconds') or task.get('timeout_seconds'), defaults['task_timeout_seconds'], 1, None)
    timeout_ms = bounded_int(task.get('timeout_ms') or task.get('timeout-ms'), task_timeout_seconds * 1000, 1, None)
    output_dir = pathlib.Path(os.path.expanduser(str(task.get('output_dir') or task.get('output-dir') or defaults['output_dir']))).resolve()
    normalized = {
        'task_id': tid,
        'task_key': task_key,
        'task_name': task_name,
        'index': index,
        'prompt': prompt,
        'prompt_summary': prompt_summary(prompt),
        'provider': task.get('provider') or defaults.get('provider') or 'happy',
        'model': task.get('model') or defaults.get('model') or 'gpt-image-2',
        'size': task.get('size') or defaults.get('size') or '1024x1024',
        'timeout_ms': timeout_ms,
        'task_timeout_seconds': task_timeout_seconds,
        'output_dir': str(output_dir),
        'input_images': input_images,
        'max_attempts': bounded_int(task.get('max_attempts') or task.get('max-attempts'), defaults.get('max_attempts', 3), 1, 5),
        'no_send': bool(task.get('no_send', task.get('no-send', defaults.get('no_send', True)))),
        'raw': bool(task.get('raw', defaults.get('raw', False))),
        'mock_command': task.get('mock_command'),
        'mock_sleep': task.get('mock_sleep'),
        'mock_exit_code': int(task.get('mock_exit_code', 0) or 0),
        'mock_output_text': task.get('mock_output_text', ''),
    }
    if task.get('command'):
        normalized['command'] = task['command']
    return normalized


class QueueRunner:
    def __init__(self, state_dir, max_workers=DEFAULT_MAX_WORKERS, task_timeout_seconds=DEFAULT_TASK_TIMEOUT_SECONDS, max_queue_size=DEFAULT_MAX_QUEUE_SIZE, overflow_policy='reject'):
        self.state_dir = pathlib.Path(state_dir).expanduser().resolve()
        self.max_workers = bounded_int(max_workers, DEFAULT_MAX_WORKERS, 1, MAX_WORKERS_LIMIT)
        self.task_timeout_seconds = bounded_int(task_timeout_seconds, DEFAULT_TASK_TIMEOUT_SECONDS, 1, None)
        self.max_queue_size = bounded_int(max_queue_size, DEFAULT_MAX_QUEUE_SIZE, 0, None)
        self.overflow_policy = overflow_policy if overflow_policy in {'reject', 'discard'} else 'reject'
        self.state_path = self.state_dir / 'queue_state.json'
        self.tasks_jsonl = self.state_dir / 'tasks.jsonl'
        self.events_jsonl = self.state_dir / 'events.jsonl'
        self.tasks_dir = self.state_dir / 'tasks'
        self.logs_dir = self.state_dir / 'logs'
        self.locks_dir = self.state_dir / 'locks'
        self._lock = threading.RLock()
        self._thread_worker_ids = {}
        self._next_worker_number = 1
        self.state = {
            'queue_id': f'q-{time.strftime("%Y%m%d%H%M%S")}-{uuid.uuid4().hex[:6]}',
            'started_at': iso_now(),
            'updated_at': iso_now(),
            'max_workers': self.max_workers,
            'task_timeout_seconds': self.task_timeout_seconds,
            'max_queue_size': self.max_queue_size,
            'overflow_policy': self.overflow_policy,
            'status': 'running',
            'counters': {},
            'running': {},
            'queued': [],
            'workers': {},
            'tasks': {},
        }
        for d in (self.state_dir, self.tasks_dir, self.logs_dir, self.locks_dir):
            d.mkdir(parents=True, exist_ok=True)

    def event(self, event, **data):
        payload = {'ts': iso_now(), 'event': event, **data}
        append_jsonl(self.events_jsonl, payload)

    def persist(self):
        counts = Counter(t.get('status', 'unknown') for t in self.state['tasks'].values())
        self.state['counters'] = dict(counts)
        self.state['updated_at'] = iso_now()
        write_json(self.state_path, self.state)

    def task_dir(self, task_id):
        return self.tasks_dir / safe_name(task_id, 'task')

    def task_artifact_update(self, task_id, **fields):
        tdir = self.task_dir(task_id)
        meta_path = tdir / 'task.json'
        meta = read_json(meta_path, {}) or {}
        meta.update(fields)
        write_json(meta_path, meta)

    def reject_task(self, task, reason, status='rejected'):
        task = dict(task)
        task['status'] = status
        task['accepted'] = False
        task['error'] = reason
        task['created_at'] = task.get('created_at') or iso_now()
        task['ended_at'] = iso_now()
        with self._lock:
            self.state['tasks'][task['task_id']] = task
            self.persist()
        append_jsonl(self.tasks_jsonl, task)
        self.event('task_rejected', task_id=task['task_id'], task_key=task.get('task_key'), reason=reason, status=status)
        fields = dict(task)
        fields.pop('task_id', None)
        self.task_artifact_update(task['task_id'], **fields)
        return task

    def accept_tasks(self, tasks):
        accepted = []
        active_keys = set()
        with self._lock:
            for existing in self.state['tasks'].values():
                if existing.get('status') in ACTIVE_STATUSES and existing.get('task_key'):
                    active_keys.add(existing['task_key'])
        for task in tasks:
            task['created_at'] = iso_now()
            task['accepted'] = True
            if not task.get('prompt') and not task.get('mock_command') and task.get('mock_sleep') is None and not task.get('command'):
                self.reject_task(task, 'missing prompt or mock command', 'rejected')
                continue
            if len(task.get('input_images') or []) > 5:
                self.reject_task(task, 'too many input images: max 5', 'rejected')
                continue
            if task.get('task_key') in active_keys:
                self.reject_task(task, f"duplicate active task_key: {task.get('task_key')}", 'skipped')
                continue
            if len(accepted) >= self.max_workers + self.max_queue_size:
                self.reject_task(task, f'queue full: max_workers={self.max_workers}, max_queue_size={self.max_queue_size}', 'rejected')
                continue
            active_keys.add(task.get('task_key'))
            accepted.append(task)
        for pos, task in enumerate(accepted):
            status = 'running' if pos < self.max_workers else 'queued'
            task['status'] = status
            task['queued_at'] = iso_now()
            tdir = self.task_dir(task['task_id'])
            tdir.mkdir(parents=True, exist_ok=True)
            task['task_dir'] = str(tdir)
            write_json(tdir / 'task.json', task)
            with self._lock:
                self.state['tasks'][task['task_id']] = task
                if status == 'queued':
                    self.state['queued'].append(task['task_id'])
                self.persist()
            self.event('task_accepted', task_id=task['task_id'], task_key=task.get('task_key'), status=status)
        return accepted

    def build_command(self, task, tdir):
        if task.get('mock_command'):
            cmd = task['mock_command']
            return cmd if isinstance(cmd, list) else ['bash', '-lc', str(cmd)]
        if task.get('command'):
            cmd = task['command']
            return cmd if isinstance(cmd, list) else ['bash', '-lc', str(cmd)]
        if task.get('mock_sleep') is not None:
            script = "import json, pathlib, sys, time; sleep=float(sys.argv[1]); out=sys.argv[2]; code=int(sys.argv[3]); text=sys.argv[4]; time.sleep(sleep); pathlib.Path(out).write_text(text or ('mock output '+out), encoding='utf-8'); print(json.dumps({'ok': code==0, 'stage':'mock_done', 'output': out, 'sleep': sleep})); sys.exit(code)"
            output = str(tdir / 'mock-output.txt')
            return [sys.executable, '-c', script, str(task.get('mock_sleep') or 0), output, str(task.get('mock_exit_code', 0)), str(task.get('mock_output_text') or '')]
        cmd = [
            sys.executable, str(RUNNER),
            '--prompt', task['prompt'],
            '--task-name', task['task_name'],
            '--provider', task['provider'],
            '--model', task['model'],
            '--size', task['size'],
            '--timeout-ms', str(task['timeout_ms']),
            '--output-dir', task['output_dir'],
            '--max-attempts', str(task['max_attempts']),
        ]
        if task.get('no_send', True):
            cmd.append('--no-send')
        if task.get('raw'):
            cmd.append('--raw')
        for img in task.get('input_images') or []:
            cmd += ['--input-image', img]
        return cmd

    def mark_running(self, task, worker_id, thread_id, proc, cmd):
        started_at = iso_now()
        record = {
            'task_id': task['task_id'],
            'task_key': task.get('task_key'),
            'worker_id': worker_id,
            'thread_id': thread_id,
            'pid': proc.pid,
            'output_dir': task.get('output_dir'),
            'task_dir': task.get('task_dir'),
            'started_at': started_at,
            'command': cmd,
        }
        with self._lock:
            current = self.state['tasks'].get(task['task_id'])
            if not current or current.get('status') not in {'queued', 'running'}:
                return False
            self.state['running'][task['task_id']] = record
            self.state['workers'][worker_id] = record
            current.update({'status': 'running', 'started_at': started_at, 'worker_id': worker_id, 'thread_id': thread_id, 'pid': proc.pid, 'command': cmd})
            if task['task_id'] in self.state['queued']:
                self.state['queued'].remove(task['task_id'])
            self.persist()
        self.event('task_started', **record)
        update_fields = dict(self.state['tasks'][task['task_id']])
        update_fields.pop('task_id', None)
        self.task_artifact_update(task['task_id'], **update_fields)
        return True

    def finish_task(self, task, worker_id, result):
        task_id = task['task_id']
        with self._lock:
            binding = self.state['workers'].get(worker_id)
            if not binding or binding.get('task_id') != task_id:
                result.update({'ok': False, 'status': 'orphan_late_output', 'stage': 'worker_binding_mismatch', 'error': 'worker no longer bound to this task_id; late result ignored'})
                self.event('orphan_late_output', task_id=task_id, worker_id=worker_id, binding=binding)
            current = self.state['tasks'].get(task_id, {})
            current.update(result)
            current['ended_at'] = iso_now()
            if 'elapsed_seconds' not in current:
                start = current.get('_start_ts')
                if start:
                    current['elapsed_seconds'] = round(now_ts() - start, 3)
            self.state['tasks'][task_id] = current
            self.state['running'].pop(task_id, None)
            if self.state['workers'].get(worker_id, {}).get('task_id') == task_id:
                self.state['workers'].pop(worker_id, None)
            self.persist()
        append_jsonl(self.tasks_jsonl, self.state['tasks'][task_id])
        self.event('task_finished', task_id=task_id, task_key=task.get('task_key'), worker_id=worker_id, status=self.state['tasks'][task_id].get('status'))
        update_fields = dict(self.state['tasks'][task_id])
        update_fields.pop('task_id', None)
        self.task_artifact_update(task_id, **update_fields)
        return self.state['tasks'][task_id]

    def worker_id_for_current_thread(self):
        thread_id = threading.get_ident()
        with self._lock:
            if thread_id not in self._thread_worker_ids:
                self._thread_worker_ids[thread_id] = f'worker-{self._next_worker_number}'
                self._next_worker_number += 1
            return self._thread_worker_ids[thread_id]

    def run_one(self, task, worker_id=None):
        worker_id = self.worker_id_for_current_thread()
        task_id = task['task_id']
        tdir = self.task_dir(task_id)
        tdir.mkdir(parents=True, exist_ok=True)
        stdout_path = tdir / 'stdout.txt'
        stderr_path = tdir / 'stderr.txt'
        result_path = tdir / 'result.json'
        cmd = self.build_command(task, tdir)
        write_json(tdir / 'command.json', {'task_id': task_id, 'task_key': task.get('task_key'), 'worker_id': worker_id, 'command': cmd, 'input_images': task.get('input_images') or [], 'prompt_summary': task.get('prompt_summary')})
        start_ts = now_ts()
        with self._lock:
            self.state['tasks'][task_id]['_start_ts'] = start_ts
            self.persist()
        proc = subprocess.Popen(cmd, cwd=str(WORKSPACE), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        thread_id = threading.get_ident()
        if not self.mark_running(task, worker_id, thread_id, proc, cmd):
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except Exception:
                proc.terminate()
            return self.finish_task(task, worker_id, {'ok': False, 'status': 'orphan_late_output', 'stage': 'not_bound', 'error': 'task was no longer active at process start'})
        stdout = ''
        stderr = ''
        timed_out = False
        try:
            stdout, stderr = proc.communicate(timeout=task.get('task_timeout_seconds') or self.task_timeout_seconds)
        except subprocess.TimeoutExpired as e:
            timed_out = True
            stdout = e.stdout if isinstance(e.stdout, str) else ''
            stderr = e.stderr if isinstance(e.stderr, str) else ''
            self.event('task_timeout_kill_start', task_id=task_id, worker_id=worker_id, pid=proc.pid)
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except Exception:
                proc.terminate()
            try:
                more_out, more_err = proc.communicate(timeout=5)
                stdout += more_out or ''
                stderr += more_err or ''
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except Exception:
                    proc.kill()
                more_out, more_err = proc.communicate(timeout=5)
                stdout += more_out or ''
                stderr += more_err or ''
            self.event('task_timeout_kill_done', task_id=task_id, worker_id=worker_id, pid=proc.pid, returncode=proc.returncode)
        stdout_path.write_text(stdout or '', encoding='utf-8')
        stderr_path.write_text(stderr or '', encoding='utf-8')
        elapsed = round(now_ts() - start_ts, 3)
        parsed = None
        if stdout.strip():
            try:
                parsed = json.loads(stdout.strip().splitlines()[-1])
            except Exception:
                parsed = None
        if timed_out:
            result = {'ok': False, 'status': 'timed_out', 'stage': 'task_timeout', 'error': f'task exceeded {task.get("task_timeout_seconds") or self.task_timeout_seconds}s and was killed', 'exit_code': proc.returncode, 'elapsed_seconds': elapsed}
        elif proc.returncode == 0 and (not parsed or parsed.get('ok', True)):
            result = {'ok': True, 'status': 'completed', 'stage': (parsed or {}).get('stage', 'done'), 'exit_code': proc.returncode, 'elapsed_seconds': elapsed}
        else:
            result = {'ok': False, 'status': 'failed', 'stage': (parsed or {}).get('stage', 'process_failed'), 'error': safe_text((parsed or {}).get('error') or stderr or stdout), 'exit_code': proc.returncode, 'elapsed_seconds': elapsed}
        if parsed:
            result['result'] = parsed
            if parsed.get('output'):
                result['output'] = parsed.get('output')
            if parsed.get('run_dir'):
                result['run_dir'] = parsed.get('run_dir')
        if timed_out:
            late_files = [str(p) for p in tdir.glob('*') if p.name not in {'task.json', 'command.json', 'stdout.txt', 'stderr.txt', 'result.json'}]
            if late_files:
                result['late_output'] = late_files
                result['orphan_late_output'] = True
        result.update({'task_id': task_id, 'task_key': task.get('task_key'), 'worker_id': worker_id, 'thread_id': thread_id, 'pid': proc.pid, 'stdout': str(stdout_path), 'stderr': str(stderr_path), 'result_json': str(result_path)})
        finished = self.finish_task(task, worker_id, result)
        write_json(result_path, finished)
        return finished

    def run(self, tasks):
        accepted = self.accept_tasks(tasks)
        if not accepted:
            with self._lock:
                self.state['status'] = 'done'
                self.persist()
            return self.summary()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix='imgq') as ex:
            futs = []
            for task in accepted:
                futs.append(ex.submit(self.run_one, task))
            for fut in concurrent.futures.as_completed(futs):
                fut.result()
        with self._lock:
            self.state['status'] = 'done'
            self.persist()
        return self.summary()

    def summary(self):
        counts = Counter(t.get('status', 'unknown') for t in self.state['tasks'].values())
        bad_count = sum(counts.get(s, 0) for s in BAD_STATUSES)
        return {
            'ok': bad_count == 0,
            'queue_id': self.state['queue_id'],
            'state_dir': str(self.state_dir),
            'max_workers': self.max_workers,
            'task_timeout_seconds': self.task_timeout_seconds,
            'max_queue_size': self.max_queue_size,
            'counters': dict(counts),
            'running': self.state.get('running', {}),
            'queued': self.state.get('queued', []),
            'tasks_total': len(self.state['tasks']),
        }


def make_tasks_from_cli(args):
    defaults = {
        'task_timeout_seconds': args.task_timeout_seconds,
        'output_dir': args.output_dir,
        'provider': args.provider,
        'model': args.model,
        'size': args.size,
        'max_attempts': args.max_attempts,
        'no_send': args.no_send,
        'raw': args.raw,
    }
    if args.input:
        data = load_task_input(args.input)
        raw_tasks = data.get('tasks') if isinstance(data, dict) and isinstance(data.get('tasks'), list) else [data]
        if isinstance(data, dict):
            defaults.update({k: data[k] for k in ('provider', 'model', 'size', 'output_dir', 'max_attempts') if k in data})
        return [normalize_task(t, defaults, i) for i, t in enumerate(raw_tasks)]
    raw = {
        'prompt': args.prompt,
        'task_name': args.task_name,
        'task_key': args.task_key or args.task_name,
        'provider': args.provider,
        'model': args.model,
        'size': args.size,
        'timeout_ms': args.timeout_ms,
        'output_dir': args.output_dir,
        'input_images': args.input_image or [],
        'max_attempts': args.max_attempts,
        'no_send': args.no_send,
        'raw': args.raw,
        'mock_sleep': args.mock_sleep,
        'mock_exit_code': args.mock_exit_code,
        'mock_output_text': args.mock_output_text,
        'mock_command': args.mock_command,
    }
    return [normalize_task(raw, defaults, 0)]


def load_state(state_dir):
    return read_json(pathlib.Path(state_dir).expanduser() / 'queue_state.json', {}) or {}


def print_status(args):
    state_dir = pathlib.Path(args.state_dir).expanduser()
    state = load_state(state_dir)
    tasks = state.get('tasks') or {}
    counts = Counter(t.get('status', 'unknown') for t in tasks.values())
    out = {
        'state_dir': str(state_dir),
        'queue_id': state.get('queue_id'),
        'status': state.get('status', 'unknown'),
        'max_workers': state.get('max_workers'),
        'running_count': len(state.get('running') or {}),
        'queued_count': len(state.get('queued') or []),
        'completed': counts.get('completed', 0),
        'failed': counts.get('failed', 0),
        'timed_out': counts.get('timed_out', 0),
        'rejected': counts.get('rejected', 0),
        'discarded': counts.get('discarded', 0),
        'skipped': counts.get('skipped', 0),
        'running': state.get('running') or {},
        'workers': state.get('workers') or {},
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def print_list(args):
    state_dir = pathlib.Path(args.state_dir).expanduser()
    state = load_state(state_dir)
    tasks = list((state.get('tasks') or {}).values())
    tasks.sort(key=lambda x: (x.get('index', 999999), x.get('created_at', '')))
    rows = []
    for t in tasks:
        if args.status and t.get('status') != args.status:
            continue
        rows.append({
            'task_id': t.get('task_id'),
            'task_key': t.get('task_key'),
            'status': t.get('status'),
            'worker_id': t.get('worker_id'),
            'thread_id': t.get('thread_id'),
            'pid': t.get('pid'),
            'started_at': t.get('started_at'),
            'ended_at': t.get('ended_at'),
            'elapsed_seconds': t.get('elapsed_seconds'),
            'output_dir': t.get('output_dir'),
            'output': t.get('output'),
            'error': t.get('error'),
            'stdout': t.get('stdout'),
            'stderr': t.get('stderr'),
            'result_json': t.get('result_json'),
        })
    print(json.dumps({'state_dir': str(state_dir), 'count': len(rows), 'tasks': rows}, ensure_ascii=False, indent=2))



def print_get(args):
    state_dir = pathlib.Path(args.state_dir).expanduser()
    state = load_state(state_dir)
    task = find_task(state, args.task_id)
    if not task:
        print(json.dumps({'ok': False, 'error': 'task not found', 'task_id': args.task_id, 'state_dir': str(state_dir)}, ensure_ascii=False, indent=2))
        sys.exit(1)
    out = dict(task)
    out['ok'] = task.get('status') == 'completed' and bool(task.get('ok', False))
    stdout = task.get('stdout') or (state_dir / 'tasks' / safe_name(task.get('task_id'), 'task') / 'stdout.txt')
    stderr = task.get('stderr') or (state_dir / 'tasks' / safe_name(task.get('task_id'), 'task') / 'stderr.txt')
    result_json = task.get('result_json') or (state_dir / 'tasks' / safe_name(task.get('task_id'), 'task') / 'result.json')
    out['stdout_tail'] = tail_text(stdout, args.tail_bytes)
    out['stderr_tail'] = tail_text(stderr, args.tail_bytes)
    out['result_path'] = str(result_json)
    out['artifacts'] = {
        'task_dir': task.get('task_dir'),
        'stdout': str(stdout),
        'stderr': str(stderr),
        'result_json': str(result_json),
        'output': task.get('output'),
        'run_dir': task.get('run_dir'),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def print_cancel(args):
    # Minimal non-daemon cancel: can mark queued tasks cancelled in persisted state.
    # Running cancellation requires a live supervising runner; use OS tools only by explicit operator action.
    state_dir = pathlib.Path(args.state_dir).expanduser()
    state_path = state_dir / 'queue_state.json'
    state = load_state(state_dir)
    task = find_task(state, args.task_id)
    if not task:
        print(json.dumps({'ok': False, 'error': 'task not found', 'task_id': args.task_id, 'state_dir': str(state_dir)}, ensure_ascii=False, indent=2))
        sys.exit(1)
    if task.get('status') == 'queued':
        task.update({'ok': False, 'status': 'cancelled', 'cancelled_at': iso_now(), 'ended_at': iso_now(), 'error': 'cancelled before start'})
        queued = state.get('queued') or []
        state['queued'] = [x for x in queued if x != task.get('task_id')]
        state.setdefault('tasks', {})[task['task_id']] = task
        state['updated_at'] = iso_now()
        state['counters'] = dict(Counter(t.get('status', 'unknown') for t in state.get('tasks', {}).values()))
        write_json(state_path, state)
        append_jsonl(state_dir / 'tasks.jsonl', task)
        write_json(state_dir / 'tasks' / safe_name(task.get('task_id'), 'task') / 'task.json', task)
        print(json.dumps({'ok': True, 'cancelled': task.get('task_id'), 'status': 'cancelled'}, ensure_ascii=False, indent=2))
        return
    print(json.dumps({'ok': False, 'status': task.get('status'), 'error': 'minimal runner can only cancel queued tasks from CLI; running task is supervised in-process and will timeout/terminate automatically', 'task_id': task.get('task_id'), 'pid': task.get('pid')}, ensure_ascii=False, indent=2))
    sys.exit(2)

def print_history(args):
    state_dir = pathlib.Path(args.state_dir).expanduser()
    rows = load_jsonl(state_dir / 'tasks.jsonl', args.limit)
    print(json.dumps({'state_dir': str(state_dir), 'count': len(rows), 'history': rows}, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description='Bounded image generation queue for happy-img2-direct')
    sub = ap.add_subparsers(dest='cmd', required=True)

    def add_common(p):
        p.add_argument('--state-dir', default=str(DEFAULT_STATE_DIR))

    runp = sub.add_parser('run', help='Run a JSON task file/string or one CLI task through the bounded queue')
    add_common(runp)
    runp.add_argument('input', nargs='?', help='JSON string, path, or @path. May contain {tasks:[...]}')
    runp.add_argument('--max-workers', type=int, default=DEFAULT_MAX_WORKERS)
    runp.add_argument('--task-timeout-seconds', type=int, default=DEFAULT_TASK_TIMEOUT_SECONDS)
    runp.add_argument('--max-queue-size', type=int, default=DEFAULT_MAX_QUEUE_SIZE)
    runp.add_argument('--overflow-policy', choices=['reject', 'discard'], default='reject')
    runp.add_argument('--prompt', default='')
    runp.add_argument('--task-name', default='happy-img2-queue')
    runp.add_argument('--task-key', default='')
    runp.add_argument('--provider', default=os.environ.get('OPENCLAW_IMAGE_PROVIDER', 'happy'))
    runp.add_argument('--model', default=os.environ.get('OPENCLAW_IMAGE_MODEL', 'gpt-image-2'))
    runp.add_argument('--size', default='1024x1024')
    runp.add_argument('--timeout-ms', type=int, default=600000)
    runp.add_argument('--output-dir', default=str(DEFAULT_OUTPUT_DIR))
    runp.add_argument('--input-image', action='append', default=[])
    runp.add_argument('--max-attempts', type=int, default=3)
    runp.add_argument('--no-send', action='store_true', default=True)
    runp.add_argument('--raw', action='store_true')
    runp.add_argument('--mock-sleep', type=float, default=None, help='test only: run a sleeping mock task instead of image API')
    runp.add_argument('--mock-exit-code', type=int, default=0)
    runp.add_argument('--mock-output-text', default='')
    runp.add_argument('--mock-command', default='')

    statusp = sub.add_parser('status', help='Show queue counters and running worker mappings')
    add_common(statusp)
    listp = sub.add_parser('list', help='List tasks with task_id/task_key/worker/pid/artifacts')
    add_common(listp)
    listp.add_argument('--status', default='')
    histp = sub.add_parser('history', aliases=['runs'], help='Show recent JSONL task history')
    add_common(histp)
    histp.add_argument('-n', '--limit', type=int, default=HISTORY_LIMIT_DEFAULT)
    getp = sub.add_parser('get', help='Show one task with stdout/stderr tail and artifact paths')
    add_common(getp)
    getp.add_argument('task_id', help='task_id or task_key')
    getp.add_argument('--tail-bytes', type=int, default=4000)
    cancelp = sub.add_parser('cancel', help='Cancel a queued task in persisted state (minimal non-daemon mode)')
    add_common(cancelp)
    cancelp.add_argument('task_id', help='task_id or task_key')

    args = ap.parse_args()
    if args.cmd == 'status':
        print_status(args)
        return
    if args.cmd == 'list':
        print_list(args)
        return
    if args.cmd in {'history', 'runs'}:
        print_history(args)
        return
    if args.cmd == 'get':
        print_get(args)
        return
    if args.cmd == 'cancel':
        print_cancel(args)
        return
    tasks = make_tasks_from_cli(args)
    runner = QueueRunner(args.state_dir, args.max_workers, args.task_timeout_seconds, args.max_queue_size, args.overflow_policy)
    summary = runner.run(tasks)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    bad = sum(summary['counters'].get(s, 0) for s in BAD_STATUSES)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
