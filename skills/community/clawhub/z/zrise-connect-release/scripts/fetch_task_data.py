#!/usr/bin/env python3
"""
Fetch task data from Zrise and save to shared task folder.

Usage:
    python3 fetch_task_data.py <task_id> --save
    # Saves to: .tasks/<task_id>/task.json
    # Prints path to stdout for next step
"""
import sys
import json
import re
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from zrise_utils import connect_zrise

TASKS_DIR = Path(__file__).resolve().parent.parent.parent / '.tasks'


def fetch_task(task_id):
    db, uid, secret, models, url = connect_zrise()
    tasks = models.execute_kw(db, uid, secret, 'project.task', 'read',
                              [[task_id]], {'fields': ['id', 'name', 'description',
                                                      'stage_id', 'project_id',
                                                      'date_deadline', 'priority']})
    if not tasks:
        return None
    t = tasks[0]
    raw_desc = t.get('description') or ''
    if not isinstance(raw_desc, str):
        raw_desc = str(raw_desc)
    desc = re.sub('<[^<]+?>', '', raw_desc)

    try:
        messages = models.execute_kw(db, uid, secret, 'mail.message', 'search_read',
                                    [[('model', '=', 'project.task'), ('res_id', '=', task_id)]],
                                    {'fields': ['id', 'body', 'date', 'author_id'],
                                     'limit': 10, 'order': 'date desc'})
        comments = []
        for m in messages:
            body = re.sub('<[^<]+?>', '', str(m.get('body', '')))
            if body.strip():
                author = (m.get('author_id') or ['', 'Unknown'])[1] if isinstance(m.get('author_id'), list) else str(m.get('author_id', ''))
                comments.append({'author': author, 'date': m.get('date'), 'body': body[:500]})
    except Exception:
        comments = []

    return {
        'task_id': t['id'],
        'name': t.get('name'),
        'description': desc[:3000] if desc else '',
        'stage': (t.get('stage_id') or [None, 'Unknown'])[1],
        'project': (t.get('project_id') or [None, 'Unknown'])[1],
        'project_id': (t.get('project_id') or [None])[0],
        'deadline': t.get('date_deadline'),
        'priority': t.get('priority', '0'),
        'link': f"{url}/web#id={t['id']}&model=project.task&view_type=form",
        'comments': comments,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('task_id', type=int)
    parser.add_argument('--save', action='store_true', help='Save to .tasks/ folder')
    args = parser.parse_args()

    task = fetch_task(args.task_id)
    if not task:
        print(json.dumps({'error': f'Task {args.task_id} not found'}))
        sys.exit(1)

    if args.save:
        task_dir = TASKS_DIR / str(args.task_id)
        task_dir.mkdir(parents=True, exist_ok=True)
        task_file = task_dir / 'task.json'
        task_file.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding='utf-8')
        print(task_dir)
    else:
        print(json.dumps(task, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
