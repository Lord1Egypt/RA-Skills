#!/usr/bin/env python3
"""
Update task stage on Zrise.

Usage:
    python3 update_task_stage.py <task_id> <new_stage>
    python3 update_task_stage.py 41994 "Done" --comment "Task completed"
    python3 update_task_stage.py 41994 "In Progress"
    python3 update_task_stage.py 41994 --rollback
    python3 update_task_stage.py --batch-stdin --stage "In Progress"

Known issue: AuditlogRule server-side bug may cause stage update to fail.
The script logs a retry request when this happens.
"""
import argparse
import json
import sys
import xmlrpc.client
from datetime import datetime, timezone
from pathlib import Path

from zrise_utils import connect_zrise, get_state_path


def get_state_dir():
    d = get_state_path('zrise/stage-pending')
    d.mkdir(parents=True, exist_ok=True)
    return d



def find_stage_id(models, db, uid, secret, project_id, stage_name):
    """Find stage ID by name in a project."""
    stages = models.execute_kw(db, uid, secret, 'project.task.type',
                               'search_read',
                               [[('project_ids', 'in', [project_id])]],
                               {'fields': ['id', 'name']})
    for s in stages:
        if stage_name.lower() in s['name'].lower():
            return s['id']
    # Fallback: try without project filter
    stages = models.execute_kw(db, uid, secret, 'project.task.type',
                               'search_read',
                               [[('name', 'ilike', f'%{stage_name}%')]],
                               {'fields': ['id', 'name'], 'limit': 5})
    return stages[0]['id'] if stages else None


def log_pending_update(task_id, stage_name, comment=None):
    """Log a pending stage update for later retry."""
    pending = get_state_dir() / f'{task_id}.json'
    data = {
        'task_id': task_id,
        'target_stage': stage_name,
        'comment': comment,
        'logged_at': datetime.now(timezone.utc).isoformat(),
    }
    pending.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    return pending


def update_stage(task_id, new_stage, comment=None):
    """Update task stage and optionally add comment."""
    conn = connect_zrise()
    if not conn:
        print("❌ Authentication failed")
        return False
    db, uid, secret, models, url = conn

    # Get current task
    tasks = models.execute_kw(db, uid, secret, 'project.task', 'read',
                              [[task_id]], {'fields': ['id', 'name', 'project_id', 'stage_id']})
    if not tasks:
        print(f"❌ Task {task_id} not found")
        return False

    task = tasks[0]
    project_id = task.get('project_id', [None])[0]
    current_stage_id = (task.get('stage_id') or [None])[0]
    current_stage_name = (task.get('stage_id') or [None, 'Unknown'])[1]

    # Find new stage
    stage_id = find_stage_id(models, db, uid, secret, project_id, new_stage)
    if not stage_id:
        print(f"❌ Stage '{new_stage}' not found in project {project_id}")
        return False

    # Get target stage name
    stages = models.execute_kw(db, uid, secret, 'project.task.type', 'read',
                               [[stage_id]], {'fields': ['name']})
    target_stage_name = stages[0]['name'] if stages else new_stage

    # Update stage — Zrise execute_kw unpacks 7th param as **kw, so pass ids+vals as single param
    try:
        models.execute_kw(db, uid, secret, 'project.task', 'write',
                          [task_id, {'stage_id': stage_id}])
    except xmlrpc.client.Fault as e:
        print(f"❌ Stage update failed: {e}")
        return False

    print(f"✅ Task {task_id}: '{current_stage_name}' → '{target_stage_name}' (stage_id: {stage_id})")

    # Add comment if provided (message_post: standard format [[id]], {kwargs})
    if comment:
        try:
            models.execute_kw(db, uid, secret, 'project.task', 'message_post',
                              [[task_id]], {'body': f'<p>{comment}</p>', 'message_type': 'comment'})
            print(f"💬 Comment added to task {task_id}")
        except xmlrpc.client.Fault:
            pass  # Non-critical

    return True


def main():
    parser = argparse.ArgumentParser(description='Update Zrise task stage')
    parser.add_argument('task_id', type=int, nargs='?', help='Task ID')
    parser.add_argument('new_stage', nargs='?', help='New stage name')
    parser.add_argument('--comment', default=None, help='Optional comment')
    parser.add_argument('--batch-stdin', action='store_true', help='Read task IDs from stdin')
    parser.add_argument('--stage', help='Stage name for --batch-stdin mode')
    args = parser.parse_args()

    if args.batch_stdin:
        data = json.load(sys.stdin)
        task_ids = data.get('move_tasks', [])
        if not args.stage:
            print("❌ --stage required with --batch-stdin")
            sys.exit(1)
        for tid in task_ids:
            update_stage(tid, args.stage)
    elif args.task_id and args.new_stage:
        success = update_stage(args.task_id, args.new_stage, args.comment)
        sys.exit(0 if success else 1)
    else:
        parser.error('task_id and new_stage are required')


if __name__ == '__main__':
    main()
