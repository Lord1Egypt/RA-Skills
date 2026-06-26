#!/usr/bin/env python3
"""
OpenClaw tool: zrise-task-info
Agent calls this to fetch task details from Zrise.
Usage: openclaw.invoke --tool zrise-task-info --args-json '{"task_id": 42374}'
"""
import json
import sys
import os
import html as html_lib
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from zrise_utils import connect_zrise

def strip_html(text):
    """Remove HTML tags and decode entities."""
    text = html_lib.unescape(text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main():
    if len(sys.argv) > 1 and not sys.argv[1].startswith('{'):
        task_id = int(sys.argv[1])
    else:
        args = json.loads(sys.argv[1]) if len(sys.argv) > 1 else json.loads(sys.stdin.read())
        task_id = args.get('task_id')
    if not task_id:
        print(json.dumps({"error": "Missing task_id"}))
        return

    db, uid, secret, models, url = connect_zrise()

    # Fetch task
    tasks = models.execute_kw(db, uid, secret, 'project.task', 'search_read',
        [[['id', '=', task_id]]],
        {'fields': ['id', 'name', 'description', 'stage_id', 'project_id',
                     'date_deadline', 'priority', 'user_ids', 'tag_ids']})

    if not tasks:
        print(json.dumps({"error": f"Task {task_id} not found"}))
        return

    t = tasks[0]

    # Fetch comments
    msgs = models.execute_kw(db, uid, secret, 'mail.message', 'search_read',
        [[['res_id', '=', task_id], ['model', '=', 'project.task']]],
        {'fields': ['body', 'author_id', 'date', 'message_type'],
         'limit': 10, 'order': 'id desc'})

    comments = []
    plan = None
    for m in msgs:
        # Skip system messages
        if m.get('message_type') in ('notification', 'user_notification'):
            continue
        body = strip_html(m.get('body', ''))
        if not body or len(body) < 5:
            continue

        # Check for [AI-PLAN] prefix
        if '[AI-PLAN]' in body:
            plan = body.replace('[AI-PLAN]', '').strip()
            continue

        # Skip auto-assignment messages
        if 'You have been assigned' in body or 'AI dang xu ly task' in body:
            continue

        comments.append({
            'author': str(m['author_id'][1]) if isinstance(m['author_id'], list) else str(m['author_id']),
            'date': str(m['date']),
            'body': body[:300]
        })

    result = {
        'task_id': t['id'],
        'name': t['name'],
        'description': strip_html(t.get('description') or ''),
        'stage': t['stage_id'][1] if isinstance(t['stage_id'], list) else str(t['stage_id']),
        'project': t['project_id'][1] if isinstance(t['project_id'], list) else str(t['project_id']),
        'deadline': str(t.get('date_deadline') or ''),
        'priority': t.get('priority', '0'),
        'plan': plan,
        'comments': comments[:5],
        'url': f'https://zrise.app/web#id={t["id"]}&model=project.task&view_type=form'
    }

    print(json.dumps(result, ensure_ascii=True, indent=2))

if __name__ == '__main__':
    main()
