#!/usr/bin/env python3
"""
Execute AI task by calling OpenClaw llm-task plugin via openclaw.invoke CLI.
Self-fetches minimal info from task.json + optional tool call for plan/comments.
Prompt is kept short (<300 chars) to avoid timeouts.

Usage:
    python3 execute_ai_task.py --task-dir /path/to/.tasks/42356 --agent demo-ba
    python3 execute_ai_task.py --task-dir /path/to/.tasks/42356 --feedback "thêm phần UI"
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path


def get_gateway_config():
    config_path = Path.home() / '.openclaw' / 'openclaw.json'
    cfg = json.loads(config_path.read_text(encoding='utf-8'))
    gw = cfg.get('gateway', {})
    port = gw.get('port', 18789)
    token = gw.get('auth', {}).get('token', '')
    return f'http://127.0.0.1:{port}', token


def strip_html(text):
    """Remove HTML tags, decode entities, return plain text."""
    if not text:
        return ''
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()


def call_openclaw_invoke(prompt, session_key, timeout=180, retries=2):
    """Call openclaw.invoke CLI with retry on rate limit."""
    gateway_url, gateway_token = get_gateway_config()
    args_json = json.dumps({'prompt': prompt}, ensure_ascii=True)

    env = {
        'OPENCLAW_URL': gateway_url,
        'OPENCLAW_TOKEN': gateway_token,
        'PATH': '/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin',
        'SHELL': '/bin/bash',
        'HOME': os.environ.get('HOME', '/Users/khoabui'),
    }

    cmd = [
        '/opt/homebrew/bin/openclaw.invoke',
        '--tool', 'llm-task',
        '--action', 'json',
        '--session-key', session_key,
        '--args-json', args_json,
    ]

    for attempt in range(retries + 1):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True,
                                    timeout=timeout, shell=False, env=env)
        except subprocess.TimeoutExpired:
            return None, 'CLI timeout'
        except Exception as e:
            return None, f'Invoke failed: {e}'

        if result.returncode != 0:
            stderr = result.stderr.strip()
            if attempt < retries and ('500' in stderr or 'tool execution failed' in stderr):
                time.sleep(5 * (attempt + 1))
                continue
            return None, f'CLI error (code {result.returncode}): {stderr[-500:]}'

        output = result.stdout.strip()
        if not output:
            return None, 'Empty response'

        try:
            parsed = json.loads(output)
            if isinstance(parsed, list):
                texts = []
                for item in parsed:
                    if isinstance(item, dict):
                        for part in item.get('content', []):
                            if isinstance(part, dict) and part.get('type') == 'text':
                                texts.append(part['text'])
                        details = item.get('details', {})
                        if isinstance(details, dict) and details.get('json'):
                            texts.append(str(details['json']))
                if texts:
                    return '\n'.join(texts), None
            return str(parsed), None
        except json.JSONDecodeError:
            return output, None

    return None, 'Max retries exceeded'


def fetch_plan_and_comments(task_id):
    """Call zrise_task_info.py to get plan and recent comments (for plan extraction)."""
    script = Path(__file__).parent / 'zrise_task_info.py'
    proc = subprocess.run(
        [sys.executable, str(script), str(task_id)],
        capture_output=True, text=True, timeout=30,
    )
    if proc.returncode != 0:
        return None, []
    try:
        data = json.loads(proc.stdout.strip())
        plan = data.get('plan', '')
        comments = data.get('comments', [])
        return plan, comments
    except json.JSONDecodeError:
        return None, []


def build_prompt(task_id, name, desc, plan, feedback='', prev_result='', result_old=''):
    """Build ultra-short prompt (<200 chars) to avoid timeouts.
    If feedback is provided and result_old exists, include it for revise."""
    name_clean = strip_html(name)[:20]
    desc_clean = strip_html(desc)[:60]
    
    plan_short = ''
    if plan and '[AI-PLAN]' in plan:
        plan_short = strip_html(plan.split('[AI-PLAN]')[1])[:40]
    
    # Clean all inputs: strip HTML, remove quotes/braces to avoid parse errors
    def clean_for_prompt(text, length):
        t = strip_html(text)[:length]
        t = t.replace("'", "").replace('"', '').replace('{', '(').replace('}', ')')
        t = t.replace('\n', ' ').replace('\r', '')
        return t
    
    feedback_clean = clean_for_prompt(feedback, 20)
    result_old_clean = clean_for_prompt(result_old, 30)
    prev_clean = clean_for_prompt(prev_result, 30)
    
    parts = [f"T{task_id}:{name_clean}", f"D:{desc_clean}"]
    if plan_short:
        parts.append(f"P:{plan_short}")
    if feedback:
        # If we have feedback and old result, include revise context
        if result_old:
            parts.append(f"FB: {feedback_clean} | Prev: {result_old_clean}")
        else:
            parts.append(f"FB: {feedback_clean}")
    elif prev_result:
        # Only include prev_result if no feedback (normal flow)
        parts.append(f"Prev: {prev_clean}")
    
    parts.extend([
        "Viet bang tieng Viet su dung HTML tags (h1 h2 p ul li strong).",
        "Chi tiet, hanh dong, 800-2000 tu.",
        "KHONG dung markdown hoac code blocks.",
    ])
    
    return ' '.join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-dir', required=True)
    parser.add_argument('--workflow', default='general')
    parser.add_argument('--agent', default=None)
    parser.add_argument('--feedback', default='')
    args = parser.parse_args()
    args.task_dir = args.task_dir.strip()

    task_dir = Path(args.task_dir)
    task = json.loads((task_dir / 'task.json').read_text(encoding='utf-8'))
    task_id = task['task_id']

    # Load plan for workflow/agent selection (from analyze step)
    plan_file = task_dir / 'plan.json'
    if plan_file.exists():
        plan_data = json.loads(plan_file.read_text(encoding='utf-8'))
        if args.workflow == 'general':
            args.workflow = plan_data.get('workflow', 'general')
        if not args.agent:
            args.agent = plan_data.get('suggested_agent')

    # Fetch task description (raw, may contain HTML)
    desc_raw = task.get('description', '')
    
    # Fetch plan and recent comments via tool (only for plan extraction and feedback context)
    plan_text, comments = fetch_plan_and_comments(task_id)
    
    # Use comments to extract feedback if any (look for review comments)
    feedback_from_comments = ''
    if comments:
        recent = [c for c in comments if 'Feedback' in c.get('body', '') or 'review' in c.get('body', '').lower()]
        if recent:
            feedback_from_comments = recent[0].get('body', '')[:500]

    # Use explicit feedback arg if provided, else from comments
    final_feedback = args.feedback or feedback_from_comments

    # Load previous result for revise
    result_file = task_dir / 'result.md'
    prev_result = result_file.read_text(encoding='utf-8') if result_file.exists() else ''

    # Read old result for revise context if feedback is provided
    result_old = ''
    if final_feedback:
        result_old_file = task_dir / 'result_old.md'
        if result_old_file.exists():
            result_old = result_old_file.read_text(encoding='utf-8')

    session_key = f'zrise-task-{task_id}'
    prompt = build_prompt(
        task_id, 
        task.get('name', ''), 
        desc_raw, 
        plan_text or '',
        final_feedback,
        prev_result,
        result_old
    )
    
    result_text, error = call_openclaw_invoke(prompt, session_key)

    if error:
        result_text = f'CLI error: {error}'

    result_file.write_text(result_text, encoding='utf-8')

    output = {
        'task_id': task_id,
        'workflow': args.workflow,
        'agent': args.agent or 'openclaw',
        'session_key': session_key,
        'task_name': task.get('name'),
        'project': task.get('project'),
        'result': result_text,
        'result_file': str(result_file),
        'source': f'agent:{args.agent}\n',
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
