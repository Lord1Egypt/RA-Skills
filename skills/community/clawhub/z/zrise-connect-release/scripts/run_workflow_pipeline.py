#!/usr/bin/env python3
import json
import logging
import pathlib
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from functools import wraps

logger = logging.getLogger('run_workflow')

# Transient errors worth retrying: timeouts, connection issues, socket errors
_TRANSIENT_ERRORS = (
    TimeoutError,
    ConnectionRefusedError,
    ConnectionResetError,
    ConnectionAbortedError,
    socket.timeout,
    socket.error,
    BrokenPipeError,
    OSError,
)


def retry_with_backoff(max_retries=3, base_delay=1.0):
    """Decorator: retry on transient errors with exponential backoff.

    On each retry the delay doubles (1s, 2s, 4s, …).
    Logs every attempt with a timestamp.
    If all retries are exhausted, writes the error into context.json
    (the calling step's context) and re-raises so the workflow loop can
    continue to the next step.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, _retry_context_path=None, **kwargs):
            last_err = None
            for attempt in range(1, max_retries + 2):  # 1 initial + max_retries
                try:
                    return func(*args, **kwargs)
                except _TRANSIENT_ERRORS as exc:
                    last_err = exc
                    if attempt > max_retries:
                        break
                    delay = base_delay * (2 ** (attempt - 1))
                    ts = datetime.now(timezone.utc).isoformat()
                    logger.warning(
                        '[%s] %s transient error (attempt %d/%d), retrying in %.0fs: %s',
                        ts, func.__name__, attempt, max_retries + 1, delay, exc,
                    )
                    time.sleep(delay)
            # All retries exhausted – write error to context if path provided
            ts = datetime.now(timezone.utc).isoformat()
            logger.error('[%s] %s failed after %d attempts: %s', ts, func.__name__, max_retries + 1, last_err)
            if _retry_context_path:
                ctx_path = pathlib.Path(_retry_context_path)
                ctx = {}
                if ctx_path.exists():
                    with open(ctx_path, 'r', encoding='utf-8') as f:
                        ctx = json.load(f)
                ctx.setdefault('retry_errors', []).append({
                    'function': func.__name__,
                    'error': str(last_err),
                    'attempts': max_retries + 1,
                    'timestamp': ts,
                })
                with open(ctx_path, 'w', encoding='utf-8') as f:
                    json.dump(ctx, f, ensure_ascii=False, indent=2)
            raise last_err
        return wrapper
    return decorator

from zrise_utils import get_root
ROOT = get_root()
WORKFLOW_CFG = ROOT / 'config' / 'zrise' / 'workflow-routing.json'
AGENT_CFG = ROOT / 'config' / 'zrise' / 'agent-profiles.json'
STATE_DIR = ROOT / 'state' / 'zrise' / 'work-items'


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def emit_progress(work_item_id, event):
    print(json.dumps({'kind': 'progress', 'work_item_id': work_item_id, **event}, ensure_ascii=False), flush=True)


def build_prompt(item, workflow_name, step, previous_outputs, agents=None):
    agents = agents or {}
    profile = agents.get(step['agent'], {'role': step['agent'], 'instruction': step['purpose']})
    title = item.get('task_name') or item.get('activity_summary') or '(no title)'
    link = item.get('link') or '-'
    prior = '\n\n'.join([f"[{o['agent']} - {o['purpose']}]\n{o['output']}" for o in previous_outputs]) or '(none)'
    
    # Inject zrise_data nếu có (từ fetch_task_data.py hoặc work item context)
    zrise_data = item.get('zrise_data') or {}
    task_id = zrise_data.get('task_id') or item.get('task_id')
    task_description = zrise_data.get('description') or '(không có mô tả chi tiết)'
    task_stage = zrise_data.get('stage') or item.get('stage') or '-'
    task_project = zrise_data.get('project') or item.get('project_name') or '-'
    task_deadline = zrise_data.get('deadline') or item.get('deadline') or '-'
    
    # Build instruction để agents biết cách fetch data nếu cần
    if task_id:
        zrise_instruction = f"""
**Dữ liệu Zrise đã có sẵn:**
- Task ID: {task_id}
- Mô tả: {task_description}
- Stage: {task_stage}
- Project: {task_project}
- Deadline: {task_deadline}

**Nếu cần thêm chi tiết:** Dùng `zrise-connect` skill hoặc chạy:
```bash
python3 scripts/zrise/fetch_task_data.py {task_id}
```
"""
    else:
        zrise_instruction = """
**⚠️ Không có dữ liệu Zrise trong work item.**

Để lấy data, dùng:
```bash
python3 scripts/zrise/fetch_task_data.py <task_id>
```
Hoặc cung cấp `zrise_data` trong work item với fields:
- task_id, name, description, stage, project, deadline
"""
    
    return f"""
Bạn đang chạy trong workflow `{workflow_name}` cho một work item Zrise.

## THÔNG TIN WORK ITEM

- work_item_id: {item.get('work_item_id')}
- title: {title}
- project: {task_project}
- stage: {task_stage}
- deadline: {task_deadline}
- link: {link}
- event_type: {item.get('event_type')}

{zrise_instruction}

## VAI TRÒ & NHIỆM VỤ

- Vai trò hiện tại: {profile['role']}
- Mục đích bước này: {step['purpose']}
- Instruction: {profile['instruction']}

## OUTPUT CÁC BƯỚC TRƯỚC

{prior}

## YÊU CẦU OUTPUT

- Viết bằng tiếng Việt
- Ngắn, chắc, hành động được
- Không lan man
- Nếu thiếu dữ liệu thì nói rõ thiếu gì
- Nếu có risk thì nêu rõ
- **Ưu tiên:** Dùng dữ liệu từ `zrise_data` nếu có sẵn
""".strip()


@retry_with_backoff(max_retries=3, base_delay=1.0)
def run_claude(prompt, model_config=None):
    """Run Claude with specified model config.

    Wrapped with retry_with_backoff so transient network/process errors
    (timeout, connection refused, etc.) are retried up to 3 times with
    exponential delays of 1s → 2s → 4s before giving up.
    """
    # For now, use Claude CLI (workflow agents are not OpenClaw agents)
    # Model config is stored for future integration with OpenClaw agent system

    cmd = ['claude', '--permission-mode', 'bypassPermissions', '--print', prompt]
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=180)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or 'claude failed')
    return proc.stdout.strip()


def main():
    if len(sys.argv) < 3:
        raise SystemExit('Usage: run_workflow_pipeline.py <work_item_id> <workflow_name>')
    print('[pipeline-v2] run_workflow_pipeline started', flush=True)  # v2 marker
    work_item_id = sys.argv[1]
    workflow_name = sys.argv[2]
    item_path = STATE_DIR / f'{work_item_id}.json'
    if not item_path.exists():
        raise SystemExit('work item not found')
    item = load_json(item_path)

    # Load workflow config with fallback
    if WORKFLOW_CFG.exists():
        cfg_data = load_json(WORKFLOW_CFG)
        workflow = cfg_data.get('workflows', {}).get(workflow_name)
        if not workflow:
            # Fallback: single-step generic workflow
            workflow = {'steps': [{'agent': 'generic', 'purpose': f'Process {workflow_name}'}]}
    else:
        # Fallback: single-step generic workflow
        workflow = {
            'steps': [{'agent': 'generic', 'purpose': f'Process {workflow_name}'}]
        }

    # Load agent profiles with fallback
    agents = {}
    if AGENT_CFG.exists():
        agents = load_json(AGENT_CFG).get('agents', {})

    outputs = []
    progress = []
    emit_progress(work_item_id, {'status': 'workflow_started', 'workflow_name': workflow_name, 'step_count': len(workflow['steps'])})
    for idx, step in enumerate(workflow['steps'], start=1):
        started = {'at': datetime.now(timezone.utc).isoformat(), 'status': 'step_started', 'step': idx, 'agent': step['agent'], 'purpose': step['purpose']}
        progress.append(started)
        emit_progress(work_item_id, started)
        prompt = build_prompt(item, workflow_name, step, outputs, agents)
        try:
            out = run_claude(prompt, _retry_context_path=str(item_path))  # Use Claude CLI for workflow agents
        except Exception as exc:
            # Final failure after retries – record error and continue to next step
            ts = datetime.now(timezone.utc).isoformat()
            logger.error('[%s] Step %d (%s) failed permanently: %s', ts, idx, step['agent'], exc)
            outputs.append({'step': idx, 'agent': step['agent'], 'purpose': step['purpose'], 'output': f'[ERROR] {exc}', 'error': True})
            finished = {'at': ts, 'status': 'step_failed', 'step': idx, 'agent': step['agent'], 'purpose': step['purpose'], 'error': str(exc)}
            progress.append(finished)
            emit_progress(work_item_id, finished)
            continue
        outputs.append({'step': idx, 'agent': step['agent'], 'purpose': step['purpose'], 'output': out})
        finished = {'at': datetime.now(timezone.utc).isoformat(), 'status': 'step_finished', 'step': idx, 'agent': step['agent'], 'purpose': step['purpose']}
        progress.append(finished)
        emit_progress(work_item_id, finished)

    final_summary = outputs[-1]['output'] if outputs else '(no output)'
    item['workflow_execution'] = {'workflow_name': workflow_name, 'steps': outputs, 'progress': progress, 'finished_at': datetime.now(timezone.utc).isoformat()}
    item['result_summary'] = final_summary
    save_json(item_path, item)
    print(json.dumps({'kind': 'result', 'ok': True, 'work_item_id': work_item_id, 'workflow_name': workflow_name, 'steps': outputs, 'result_summary': final_summary}, ensure_ascii=False))


if __name__ == '__main__':
    main()
