#!/usr/bin/env python3
import argparse, json, os, pathlib, random, re, subprocess, sys, time

SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
GEN_SCRIPT = SKILL_DIR / 'scripts/generate-image.js'
DEFAULT_OUTPUT_DIR = os.path.expanduser('~/.openclaw/generated-images')

RETRYABLE_CATEGORIES = {'timeout', 'upstream_failure', 'rate_limit', 'rate_limited', 'wrapper_error'}
RETRYABLE_STAGES = {'timeout', 'request', 'wrapper_parse', 'batch_timeout'}


def safe_err(s):
    s = str(s)
    s = re.sub(r'sk-[A-Za-z0-9_\-]{8,}', 'sk-***', s)
    s = re.sub(r'Bearer\s+[A-Za-z0-9_\.\-]+', 'Bearer ***', s, flags=re.I)
    s = re.sub(r'(app_secret|appSecret|apiKey|api_key|token|secret)["\']?\s*[:=]\s*["\'][^"\']+', r'\1:"[redacted]', s, flags=re.I)
    return s[-4000:]


def is_retryable(data):
    if data.get('ok'):
        return False
    diag = data.get('diagnosis') or {}
    return bool(
        diag.get('retryable')
        or diag.get('category') in RETRYABLE_CATEGORIES
        or (
            data.get('stage') in RETRYABLE_STAGES
            and data.get('http_status') in (None, 408, 429, 500, 502, 503, 504)
        )
        or data.get('http_status') in (408, 429, 500, 502, 503, 504)
    )


def delay_for(attempt_index, base_delay, max_delay, jitter):
    delay = min(max_delay, base_delay * (2 ** (attempt_index - 1)))
    return delay + (random.uniform(0, jitter) if jitter > 0 else 0)


def slugify(name):
    name = name or 'happy-img2-direct'
    name = re.sub(r'[^A-Za-z0-9._-]+', '-', name).strip('-._')
    return name[:80] or 'happy-img2-direct'


def iso_now():
    return time.strftime('%Y-%m-%dT%H:%M:%S%z')


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def write_state(path, *, status, attempt, max_attempts, started_at, run_started, output='', last_error=''):
    elapsed_seconds = round(max(0.0, time.time() - run_started), 3)
    payload = {
        'status': status,
        'attempt': attempt,
        'max_attempts': max_attempts,
        'started_at': started_at,
        'updated_at': iso_now(),
        'elapsed_seconds': elapsed_seconds,
        'output': output,
        'last_error': safe_err(last_error) if last_error else '',
    }
    write_json(path, payload)


def main():
    ap = argparse.ArgumentParser(description='Generate one image via an OpenAI-compatible images API provider configured in OpenClaw.')
    ap.add_argument('--prompt', required=True)
    ap.add_argument('--task-name', default='happy-img2-direct')
    ap.add_argument('--provider', default=os.environ.get('OPENCLAW_IMAGE_PROVIDER', 'happy'))
    ap.add_argument('--model', default=os.environ.get('OPENCLAW_IMAGE_MODEL', 'gpt-image-2'))
    ap.add_argument('--size', default='1024x1024')
    ap.add_argument('--timeout-ms', type=int, default=600000)
    ap.add_argument('--output-dir', default=DEFAULT_OUTPUT_DIR)
    ap.add_argument('--raw', action='store_true', help='marker only: keep prompt as-is')
    ap.add_argument('--input-image', '--image', '--reference-image', dest='input_images', action='append', default=[], help='reference/input image path for image-to-image/edit mode; repeatable; routes to /images/edits')
    ap.add_argument('--images', default='', help='JSON array or comma-separated reference image paths for edit mode; combined max 5 total with --input-image/--image/--reference-image')
    ap.add_argument('--max-attempts', type=int, default=3)
    ap.add_argument('--retry-base-delay', type=float, default=8.0)
    ap.add_argument('--retry-max-delay', type=float, default=45.0)
    ap.add_argument('--retry-jitter', type=float, default=5.0)
    # Compatibility flags. Sending is intentionally not implemented in the public skill.
    ap.add_argument('--no-send', action='store_true')
    ap.add_argument('--to-open-id', default='')
    args = ap.parse_args()

    all_input_images = list(args.input_images or [])
    if args.images:
        try:
            parsed_images = json.loads(args.images)
            if isinstance(parsed_images, list):
                all_input_images.extend(str(x) for x in parsed_images)
            else:
                all_input_images.append(str(parsed_images))
        except Exception:
            all_input_images.extend(x.strip() for x in str(args.images).split(',') if x.strip())
    if len(all_input_images) > 5:
        print(json.dumps({'ok': False, 'stage': 'invalid_input', 'error': 'too many input images: max 5 total across --input-image/--image/--reference-image and --images', 'input_images_count': len(all_input_images)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    max_attempts = max(1, min(5, args.max_attempts))
    output_dir = pathlib.Path(os.path.expanduser(args.output_dir))
    output_dir.mkdir(parents=True, exist_ok=True)
    run_dir = output_dir / '_runs' / f"{slugify(args.task_name)}-{time.strftime('%Y%m%d-%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)
    run_started = time.time()
    state_path = run_dir / 'state.json'
    run_started_at = iso_now()
    write_state(
        state_path,
        status='running',
        attempt=1,
        max_attempts=max_attempts,
        started_at=run_started_at,
        run_started=run_started,
    )

    attempts = []
    final_data = None
    for attempt in range(1, max_attempts + 1):
        attempt_name = args.task_name if attempt == 1 else f"{args.task_name}-retry{attempt}"
        output = output_dir / f"{slugify(attempt_name)}-{time.strftime('%Y%m%d-%H%M%S')}.png"
        cmd = [
            'node', str(GEN_SCRIPT),
            '--prompt', args.prompt,
            '--output', str(output),
            '--provider', args.provider,
            '--model', args.model,
            '--size', args.size,
            '--timeout-ms', str(args.timeout_ms),
        ]
        for img in all_input_images:
            cmd += ['--input-image', img]
        attempt_dir = run_dir / f'attempt-{attempt:02d}'
        attempt_dir.mkdir(parents=True, exist_ok=True)
        write_json(
            attempt_dir / 'request.json',
            {
                'prompt': args.prompt,
                'task_name': attempt_name,
                'provider': args.provider,
                'model': args.model,
                'size': args.size,
                'timeout_ms': args.timeout_ms,
                'output': str(output),
                'input_images': all_input_images,
                'mode': 'edit' if all_input_images else 'generation',
            },
        )
        write_state(
            state_path,
            status='running',
            attempt=attempt,
            max_attempts=max_attempts,
            started_at=run_started_at,
            run_started=run_started,
            output=str(output),
        )
        started = time.time()
        stdout = ''
        stderr = ''
        try:
            proc = subprocess.run(
                cmd,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=args.timeout_ms / 1000 + 30,
            )
            stdout = proc.stdout or ''
            stderr = proc.stderr or ''
            try:
                data = json.loads(stdout.strip())
            except Exception:
                data = {
                    'ok': False,
                    'stage': 'wrapper_parse',
                    'returncode': proc.returncode,
                    'stdout': stdout[-4000:],
                    'stderr': stderr[-4000:],
                    'diagnosis': {
                        'category': 'wrapper_error',
                        'human_reason': 'Generator did not return parseable JSON.',
                        'retryable': True,
                    },
                }
        except subprocess.TimeoutExpired as e:
            stdout = e.stdout if isinstance(e.stdout, str) else ''
            stderr = e.stderr if isinstance(e.stderr, str) else ''
            data = {
                'ok': False,
                'stage': 'wrapper_timeout',
                'error': f'outer wrapper timeout after {args.timeout_ms / 1000 + 30}s',
                'diagnosis': {
                    'category': 'timeout',
                    'human_reason': 'Outer wrapper timed out.',
                    'retryable': True,
                },
            }
        elapsed = round(time.time() - started, 3)
        (attempt_dir / 'stdout.txt').write_text(stdout or '', encoding='utf-8')
        (attempt_dir / 'stderr.txt').write_text(stderr or '', encoding='utf-8')
        data.update({'attempt': attempt, 'max_attempts': max_attempts, 'elapsed_seconds': elapsed, 'attempt_dir': str(attempt_dir)})
        write_json(attempt_dir / 'result.json', data)
        attempts.append(data)

        if data.get('ok'):
            write_state(
                state_path,
                status='success',
                attempt=attempt,
                max_attempts=max_attempts,
                started_at=run_started_at,
                run_started=run_started,
                output=str(output),
            )
            final_data = data
            break

        retryable = attempt < max_attempts and is_retryable(data)
        failure_status = 'timeout' if (data.get('diagnosis') or {}).get('category') == 'timeout' or data.get('stage') == 'wrapper_timeout' else 'failed'
        write_state(
            state_path,
            status='retrying' if retryable else failure_status,
            attempt=attempt,
            max_attempts=max_attempts,
            started_at=run_started_at,
            run_started=run_started,
            output=str(output),
            last_error=data.get('error') or data,
        )
        if retryable:
            time.sleep(delay_for(attempt, args.retry_base_delay, args.retry_max_delay, args.retry_jitter))
        elif attempt < max_attempts:
            break

    if final_data:
        result = {**final_data, 'attempts_count': len(attempts), 'run_dir': str(run_dir)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    result = {
        'ok': False,
        'stage': 'failed_after_retries',
        'error': safe_err(attempts[-1] if attempts else 'unknown'),
        'attempts_count': len(attempts),
        'run_dir': str(run_dir),
        'attempts': attempts,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(1)


if __name__ == '__main__':
    main()
