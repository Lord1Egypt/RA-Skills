#!/usr/bin/env python3
import argparse, concurrent.futures, json, os, pathlib, re, subprocess, sys, time, uuid

SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
WORKSPACE = pathlib.Path(os.environ.get('OPENCLAW_WORKSPACE', os.getcwd())).resolve()
RUNNER = SKILL_DIR / 'scripts/run.py'
DEFAULT_MAX_WORKERS = 4
MAX_WORKERS_LIMIT = 4
DEFAULT_QUEUE_LIMIT = 200
QUEUE_LIMIT_CAP = 200
TIMEOUT_ERROR_PATTERN = re.compile(r'(timeout|aborterror)', re.I)


def load_input(arg):
    if arg.startswith('@'):
        return json.loads(pathlib.Path(arg[1:]).read_text(encoding='utf-8'))
    return json.loads(arg)


def safe_name(s):
    keep = []
    for ch in str(s):
        if ch.isalnum() or ch in '-_':
            keep.append(ch)
        else:
            keep.append('-')
    return ''.join(keep).strip('-')[:80] or 'task'


def safe_err(s):
    s = str(s)
    s = re.sub(r'sk-[A-Za-z0-9_\-]{8,}', 'sk-***', s)
    s = re.sub(r'Bearer\s+[A-Za-z0-9_\.\-]+', 'Bearer ***', s, flags=re.I)
    s = re.sub(r'(app_secret|appSecret|apiKey|api_key|token|secret)["\']?\s*[:=]\s*["\'][^"\']+', r'\1:"[redacted]', s, flags=re.I)
    return s[-4000:]


def bounded_int(value, default, lower, upper):
    try:
        n = int(value if value is not None else default)
    except (TypeError, ValueError):
        n = default
    return max(lower, min(upper, n))


def iso_now():
    return time.strftime('%Y-%m-%dT%H:%M:%S%z')


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def write_state(path, *, status, started_at, task_started, output='', last_error=''):
    write_json(
        path,
        {
            'status': status,
            'started_at': started_at,
            'updated_at': iso_now(),
            'elapsed_seconds': round(max(0.0, time.time() - task_started), 3),
            'output': output,
            'last_error': safe_err(last_error) if last_error else '',
        },
    )


def rejected_result(task, idx):
    return {
        'ok': False,
        'stage': 'queue_rejected',
        'error': 'task dropped because bounded queue limit exceeded',
        'index': idx,
        'task_name': safe_name(task.get('task_name') or f'task-{idx+1}'),
    }


def _diagnosis_category(data):
    diag = data.get('diagnosis') or {}
    category = diag.get('category')
    return str(category).lower() if category else ''


def _error_mentions_timeout(data):
    return bool(TIMEOUT_ERROR_PATTERN.search(str(data.get('error') or '')))


def _attempt_indicates_timeout(attempt):
    if not isinstance(attempt, dict):
        return False
    if attempt.get('stage') in {'wrapper_timeout', 'timeout', 'batch_timeout'}:
        return True
    if _diagnosis_category(attempt) == 'timeout':
        return True
    return _error_mentions_timeout(attempt) and _diagnosis_category(attempt) == 'timeout'


def infer_root_cause_category(data):
    if not isinstance(data, dict) or data.get('ok'):
        return ''
    if data.get('stage') in {'batch_timeout', 'wrapper_timeout', 'timeout'}:
        return 'timeout'
    if _diagnosis_category(data) == 'timeout':
        return 'timeout'
    attempts = data.get('attempts')
    if isinstance(attempts, list) and attempts:
        timeout_attempt = any(_attempt_indicates_timeout(attempt) for attempt in attempts)
        last_attempt_timeout = _attempt_indicates_timeout(attempts[-1])
        if data.get('stage') == 'failed_after_retries' and (last_attempt_timeout or timeout_attempt):
            return 'timeout'
    if _error_mentions_timeout(data) and _diagnosis_category(data) == 'timeout':
        return 'timeout'
    return ''


def run_one(task, defaults, batch_dir):
    idx = task['_index']
    name = safe_name(task.get('task_name') or f'task-{idx+1}')
    task_dir = batch_dir / f'{idx+1:02d}-{name}'
    task_dir.mkdir(parents=True, exist_ok=True)
    state_path = task_dir / 'state.json'
    task_started = time.time()
    started_at = iso_now()

    prompt = task.get('prompt')
    if not prompt:
        result = {'ok': False, 'stage': 'invalid_task', 'error': 'missing prompt', 'index': idx, 'task_name': name}
        write_json(task_dir / 'result.json', result)
        write_state(state_path, status='failed', started_at=started_at, task_started=task_started, last_error=result['error'])
        return result

    timeout_ms = int(task.get('timeout_ms') or defaults['timeout_ms'])
    send = bool(task.get('send_to_feishu', defaults.get('send_to_feishu', False)))

    cmd = [
        'python3', str(RUNNER),
        '--prompt', prompt,
        '--task-name', name,
        '--size', task.get('size') or defaults.get('size') or '1024x1024',
        '--timeout-ms', str(timeout_ms),
    ]
    cmd += ['--no-send']
    input_images = []
    if task.get('input_image'):
        input_images.append(str(task.get('input_image')))
    if task.get('image'):
        input_images.append(str(task.get('image')))
    if task.get('reference_image'):
        input_images.append(str(task.get('reference_image')))
    if isinstance(task.get('images'), list):
        input_images.extend(str(x) for x in task.get('images'))
    elif task.get('images'):
        input_images.extend(x.strip() for x in str(task.get('images')).split(',') if x.strip())
    if len(input_images) > 5:
        result = {'ok': False, 'stage': 'invalid_task', 'error': 'too many input images: max 5 total across input_image/image/reference_image/images', 'input_images_count': len(input_images), 'index': idx, 'task_name': name}
        write_json(task_dir / 'result.json', result)
        write_state(state_path, status='failed', started_at=started_at, task_started=task_started, last_error=result['error'])
        return result
    for img in input_images:
        cmd += ['--input-image', img]
    if task.get('raw') or defaults.get('raw'):
        cmd += ['--raw']

    meta = {
        'index': idx,
        'task_name': name,
        'prompt': prompt,
        'cmd': cmd,
        'timeout_ms': timeout_ms,
        'send_to_feishu': send,
        'input_images': input_images,
        'mode': 'edit' if input_images else 'generation',
        'task_dir': str(task_dir),
        'started_at': started_at,
    }
    write_json(task_dir / 'batch_task.json', meta)
    write_state(state_path, status='running', started_at=started_at, task_started=task_started)

    try:
        proc = subprocess.run(
            cmd,
            cwd=str(WORKSPACE),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_ms / 1000 + 45,
        )
        (task_dir / 'stdout.txt').write_text(proc.stdout or '', encoding='utf-8')
        (task_dir / 'stderr.txt').write_text(proc.stderr or '', encoding='utf-8')
        try:
            data = json.loads((proc.stdout or '').strip())
        except Exception:
            data = {
                'ok': False,
                'stage': 'batch_parse',
                'returncode': proc.returncode,
                'stdout_tail': (proc.stdout or '')[-3000:],
                'stderr_tail': (proc.stderr or '')[-3000:],
            }
        data.update({'index': idx, 'task_name': name, 'batch_task_dir': str(task_dir), 'finished_at': iso_now()})
    except subprocess.TimeoutExpired as e:
        data = {
            'ok': False,
            'stage': 'batch_timeout',
            'index': idx,
            'task_name': name,
            'error': f'task exceeded wrapper timeout after {timeout_ms / 1000 + 45}s',
            'diagnosis': {'category': 'timeout', 'human_reason': '批量任务外层等待超时。', 'retryable': True},
            'batch_task_dir': str(task_dir),
            'finished_at': iso_now(),
        }
        (task_dir / 'stdout.txt').write_text((e.stdout or '') if isinstance(e.stdout, str) else '', encoding='utf-8')
        (task_dir / 'stderr.txt').write_text((e.stderr or '') if isinstance(e.stderr, str) else '', encoding='utf-8')

    root_cause_category = infer_root_cause_category(data)
    if root_cause_category:
        data['root_cause_category'] = root_cause_category
    write_json(task_dir / 'result.json', data)
    final_status = 'success' if data.get('ok') else ('timeout' if root_cause_category == 'timeout' else 'failed')
    write_state(
        state_path,
        status=final_status,
        started_at=started_at,
        task_started=task_started,
        output=data.get('output') or '',
        last_error='' if data.get('ok') else data.get('error') or data,
    )
    return data


def main():
    ap = argparse.ArgumentParser(description='Batch runner for happy-img2-direct (default/max 4 workers, bounded queue default/max 200)')
    ap.add_argument('input', help='JSON string or @path')
    args = ap.parse_args()
    cfg = load_input(args.input)
    tasks = cfg.get('tasks') or []
    if not isinstance(tasks, list) or not tasks:
        print(json.dumps({'ok': False, 'stage': 'invalid_input', 'error': 'tasks must be non-empty list'}, ensure_ascii=False, indent=2))
        sys.exit(1)

    max_workers = bounded_int(cfg.get('max_workers'), DEFAULT_MAX_WORKERS, 1, MAX_WORKERS_LIMIT)
    queue_limit = bounded_int(cfg.get('queue_limit'), DEFAULT_QUEUE_LIMIT, 1, QUEUE_LIMIT_CAP)
    defaults = {
        'timeout_ms': int(cfg.get('timeout_ms') or 600000),
        'to_open_id': cfg.get('to_open_id') or '',
        'send_to_feishu': bool(cfg.get('send_to_feishu', False)),
        'size': cfg.get('size') or '1024x1024',
        'raw': bool(cfg.get('raw', False)),
    }
    batch_name = safe_name(cfg.get('batch_name') or 'happy-img2-batch')
    batch_dir = WORKSPACE / 'content-factory/live-course-design/img2/batches' / f"{batch_name}-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    batch_dir.mkdir(parents=True, exist_ok=True)
    write_json(batch_dir / 'batch_request.json', cfg)

    for i, t in enumerate(tasks):
        t['_index'] = i

    scheduled_tasks = tasks[:queue_limit]
    rejected_results = [rejected_result(t, i) for i, t in enumerate(tasks[queue_limit:], start=queue_limit)]

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = [ex.submit(run_one, t, defaults, batch_dir) for t in scheduled_tasks]
        for fut in concurrent.futures.as_completed(futs):
            results.append(fut.result())
    results.extend(rejected_results)
    results.sort(key=lambda x: x.get('index', 999999))
    processed = len(results) - len(rejected_results)
    timeout_count = sum(1 for r in results if not r.get('ok') and infer_root_cause_category(r) == 'timeout')
    summary = {
        'ok': all(r.get('ok') for r in results),
        'stage': 'done',
        'batch_dir': str(batch_dir),
        'max_workers': max_workers,
        'queue_limit': queue_limit,
        'total': len(tasks),
        'scheduled': len(scheduled_tasks),
        'processed': processed,
        'rejected': len(rejected_results),
        'success': sum(1 for r in results if r.get('ok')),
        'failed': sum(1 for r in results if not r.get('ok')),
        'timeout': timeout_count,
        'provider': 'happy',
        'model': 'gpt-image-2',
        'no_local_fallback': True,
        'results': results,
    }
    write_json(batch_dir / 'batch_result.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    sys.exit(0 if summary['ok'] else 1)


if __name__ == '__main__':
    main()
