#!/usr/bin/env python3
"""
Write result from task folder to Zrise.
Uses mail.compose.message to avoid XML-RPC HTML double-escape.

Usage:
    python3 writeback_to_zrise.py --task-dir /path/to/.tasks/42356
    python3 writeback_to_zrise.py --task-dir /path/to/.tasks/42356 --plan
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from zrise_utils import connect_zrise


def extract_markdown(content):
    """Extract markdown text from JSON wrapper if present."""
    content_stripped = content.strip()
    if not content_stripped.startswith('{'):
        return content

    depth, end = 0, -1
    for i, c in enumerate(content_stripped):
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end <= 0:
        return content

    try:
        parsed = json.loads(content_stripped[:end])
        for key in ('output', 'result', 'content', 'text', 'response'):
            val = parsed.get(key)
            if isinstance(val, str) and len(val) > 50:
                return val
            elif isinstance(val, dict):
                for k2 in ('output', 'content', 'text'):
                    v2 = val.get(k2)
                    if isinstance(v2, str) and len(v2) > 50:
                        return v2
    except (json.JSONDecodeError, TypeError):
        pass
    return content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-dir', required=True)
    parser.add_argument('--workflow', default='general')
    parser.add_argument('--plan', action='store_true', help='Post plan for review')
    args = parser.parse_args()
    if hasattr(args, 'task_dir') and args.task_dir:
        args.task_dir = args.task_dir.strip()

    task_dir = Path(args.task_dir)
    task = json.loads((task_dir / 'task.json').read_text(encoding='utf-8'))
    task_id = task['task_id']
    task_name = task.get('name', '')

    db, uid, secret, models, url = connect_zrise()

    if args.plan:
        plan = json.loads((task_dir / 'plan.json').read_text(encoding='utf-8'))
        content = plan.get('plan', '(no plan)')
        tag = f'[AI-PLAN] {args.workflow}'
    else:
        result_file = task_dir / 'result.md'
        content = result_file.read_text(encoding='utf-8') if result_file.exists() else '(no result)'
        tag = f'✅ Kết quả — {args.workflow}'

    content = extract_markdown(content)

    try:
        import markdown as md
        html_body = md.markdown(content, extensions=['fenced_code', 'tables'])
    except ImportError:
        html_body = f'<pre>{content}</pre>'

    body = f'<p><b>{tag}</b></p><p><i>{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}</i></p>{html_body}'

    # Use mail.compose.message to avoid XML-RPC HTML double-escape
    # Step 1: create compose
    compose_id = models.execute_kw(db, uid, secret, 'mail.compose.message', 'create', [{
        'composition_mode': 'comment',
        'model': 'project.task',
        'res_ids': str([task_id]),
        'subtype_id': 2,
        'body': body,
        'partner_ids': [],
        'subject': task_name,
        'force_send': True,
    }])

    # Step 2: send
    models.execute_kw(db, uid, secret, 'mail.compose.message', 'action_send_mail',
                      [[compose_id]], {'context': {}})

    print(json.dumps({
        'ok': True, 'task_id': task_id,
        'workflow': args.workflow,
        'compose_id': compose_id,
        'mode': 'plan' if args.plan else 'result',
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
