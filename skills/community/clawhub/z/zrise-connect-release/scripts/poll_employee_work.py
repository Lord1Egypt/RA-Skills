#!/usr/bin/env python3
"""
Poll tasks from Zrise for a given employee.
Categorizes tasks: new, changed, SLA breach, approaching deadline.

Usage:
    python3 poll_employee_work.py --employee-id 10 --limit 20 --json
    python3 poll_employee_work.py --employee-id 10 --sla-hours 24 --deadline-hours 48 --json

Logic:
    - NEW: task not seen before in poll state
    - CHANGED: task hash changed since last poll (stage, name, description, assignee)
    - SLA_BREACH: write_date older than --sla-hours (default 24h) and not Done
    - DEADLINE_SOON: date_deadline within --deadline-hours (default 48h) and not Done
    - STALE: no activity/change for --stale-hours (default 72h) and not Done

State tracking:
    - state/zrise/poll-state/<employee_id>.json stores seen tasks + hashes
    - Each poll updates state; only novel tasks are returned as 'notify'
"""
import argparse
import hashlib
import json
import sys
import time
import xmlrpc.client
from datetime import datetime, timezone, timedelta
from pathlib import Path

from zrise_utils import get_openclaw_config_path, get_state_path

DONE_KEYWORDS = ['done', 'cancelled', 'cancel', 'hoàn thành', 'hủy']
MAX_RETRIES = 2
RETRY_DELAY = 3  # seconds


def zrise_call(fn, *args, **kwargs):
    """Wrapper with retry for intermittent Zrise API errors."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            return fn(*args, **kwargs)
        except xmlrpc.client.Fault as e:
            if attempt < MAX_RETRIES and ('IndexError' in str(e) or 'TypeError' in str(e)):
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
            raise


def now_utc():
    return datetime.now(timezone.utc)


def parse_datetime(dt_str):
    """Parse Zrise datetime string to UTC datetime."""
    if not dt_str:
        return None
    # Handle ISO format with timezone like '2026-03-17T16:19:38.260137+00:00'
    try:
        dt = datetime.fromisoformat(dt_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        pass
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f',
                '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f'):
        try:
            return datetime.strptime(dt_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def task_hash(task):
    """Hash of fields that indicate a meaningful change."""
    payload = {
        'name': (task.get('name') or ''),
        'stage': (task.get('stage_id') or ['', ''])[1],
        'user_ids': sorted(task.get('user_ids', [])),
        'priority': task.get('priority', ''),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def is_done(stage_name):
    return any(kw in (stage_name or '').lower() for kw in DONE_KEYWORDS)


def load_poll_state(employee_id):
    """Load previous poll state for dedup/change detection."""
    state_dir = get_state_path('zrise/poll-state')
    state_dir.mkdir(parents=True, exist_ok=True)
    state_file = state_dir / f'{employee_id}.json'
    if state_file.exists():
        return json.loads(state_file.read_text(encoding='utf-8'))
    return {'seen_tasks': {}, 'last_poll': None}


def save_poll_state(employee_id, state):
    """Save poll state."""
    state_dir = get_state_path('zrise/poll-state')
    state_dir.mkdir(parents=True, exist_ok=True)
    state_file = state_dir / f'{employee_id}.json'
    state['last_poll'] = now_utc().isoformat()
    state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')


def poll_tasks(employee_id, limit=20, sla_hours=24, deadline_hours=48, stale_hours=72):
    """Poll and categorize tasks for employee."""
    with open(str(get_openclaw_config_path()), 'r') as f:
        cfg = json.load(f)

    env = cfg['skills']['entries']['zrise-connect']['env']
    url = env['ZRISE_URL'].rstrip('/')
    db = env['ZRISE_DB']
    user = env['ZRISE_USERNAME']
    api_key = env.get('ZRISE_API_KEY')

    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', allow_none=True)
    uid = common.authenticate(db, user, api_key, {})
    if not uid:
        return {'error': 'Authentication failed'}

    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', allow_none=True)

    # Map employee → user
    emp = zrise_call(models.execute_kw, db, uid, api_key, 'hr.employee', 'read',
                            [[employee_id]], {'fields': ['id', 'name', 'user_id']})
    if not emp:
        return {'error': f'Employee {employee_id} not found'}
    user_ref = emp[0].get('user_id')
    if not user_ref:
        return {'error': f'Employee {employee_id} has no linked user account'}
    user_id = user_ref[0] if isinstance(user_ref, list) else user_ref

    # Fetch tasks with relevant fields
    # Note: Zrise's project.task._search has intermittent bugs with 'in' operator.
    # Retry with different domain syntaxes if the first attempt fails.
    task_ids = None
    domain_variants = [
        [('user_ids', 'in', [user_id])],
        [('user_ids', '=', [user_id])],
    ]
    for domain in domain_variants:
        try:
            task_ids = zrise_call(models.execute_kw, 
                db, uid, api_key,
                'project.task', 'search',
                [domain],
                {'limit': limit, 'order': 'priority desc, write_date desc'},
            )
            break
        except xmlrpc.client.Fault:
            continue

    if not task_ids:
        return {
            'employee_id': employee_id, 'user_id': user_id,
            'poll_time': now_utc().isoformat(), 'total_pending': 0,
            'notify_count': 0, 'summary': {'new': 0, 'changed': 0, 'sla_breach': 0,
            'deadline_soon': 0, 'stale': 0},
            'notify_tasks': [], 'all_pending': [],
        }

    tasks = zrise_call(models.execute_kw, 
        db, uid, api_key,
        'project.task', 'read',
        [task_ids],
        {'fields': ['id', 'name', 'description', 'stage_id', 'project_id',
                     'date_deadline', 'create_date', 'write_date',
                     'date_last_stage_update', 'user_ids', 'priority']},
    )

    # Load previous state
    prev_state = load_poll_state(employee_id)
    seen = prev_state.get('seen_tasks', {})
    now = now_utc()

    new_tasks = []
    changed_tasks = []
    sla_breach_tasks = []
    deadline_soon_tasks = []
    stale_tasks = []
    all_pending = []

    for t in tasks:
        stage_name = (t.get('stage_id') or [None, ''])[1]

        # Skip done/cancelled
        if is_done(stage_name):
            continue

        tid = str(t['id'])
        h = task_hash(t)
        write_dt = parse_datetime(t.get('write_date'))
        create_dt = parse_datetime(t.get('create_date'))
        stage_dt = parse_datetime(t.get('date_last_stage_update'))
        deadline_dt = parse_datetime(t.get('date_deadline'))

        task_info = {
            'task_id': t['id'],
            'name': t.get('name'),
            'stage': stage_name,
            'project': (t.get('project_id') or [None, 'Unknown'])[1],
            'deadline': t.get('date_deadline'),
            'link': f"{url}/web#id={t['id']}&model=project.task&view_type=form",
            'write_date': t.get('write_date'),
            'create_date': t.get('create_date'),
            'priority': t.get('priority', '0'),
        }

        all_pending.append(task_info)

        # Categorize
        prev = seen.get(tid)
        categories = []

        if prev is None:
            # Never seen before
            categories.append('new')
            new_tasks.append({**task_info, 'category': 'new'})
        elif prev.get('hash') != h:
            # Hash changed → something meaningful updated
            categories.append('changed')
            changed_tasks.append({
                **task_info,
                'category': 'changed',
                'changes': {
                    'prev_stage': prev.get('stage'),
                    'prev_hash': prev.get('hash'),
                }
            })
        else:
            # Same as before → check SLA / deadline
            # Use the most recent of write_date and date_last_stage_update
            last_activity = max(write_dt, stage_dt) if write_dt and stage_dt else (write_dt or stage_dt)
            if not last_activity:
                last_activity = create_dt

            if last_activity:
                hours_since_activity = (now - last_activity).total_seconds() / 3600

                # SLA breach: no update for sla_hours
                # Only notify once per SLA period (default: re-notify every 24h)
                sla_renotify_hours = max(sla_hours, 24)
                last_sla_notify = prev.get('last_sla_notify')
                last_sla_dt = parse_datetime(last_sla_notify) if last_sla_notify else None
                should_notify_sla = False

                if hours_since_activity >= sla_hours:
                    if last_sla_dt is None:
                        should_notify_sla = True  # First SLA alert
                    elif (now - last_sla_dt).total_seconds() / 3600 >= sla_renotify_hours:
                        should_notify_sla = True  # Re-notify after cooldown

                if should_notify_sla:
                    categories.append('sla_breach')
                    sla_breach_tasks.append({
                        **task_info,
                        'category': 'sla_breach',
                        'hours_since_update': round(hours_since_activity, 1),
                    })

                # Stale: no update for stale_hours (informational, not in notify)
                if hours_since_activity >= stale_hours:
                    categories.append('stale')
                    stale_tasks.append({
                        **task_info,
                        'hours_since_update': round(hours_since_activity, 1),
                    })

            # Deadline approaching
            if deadline_dt:
                hours_until_deadline = (deadline_dt - now).total_seconds() / 3600
                if 0 <= hours_until_deadline <= deadline_hours:
                    # Only notify once per deadline alert
                    last_deadline_notify = prev.get('last_deadline_notify')
                    if last_deadline_notify != t.get('date_deadline'):
                        categories.append('deadline_soon')
                        deadline_soon_tasks.append({
                            **task_info,
                            'category': 'deadline_soon',
                            'hours_until_deadline': round(hours_until_deadline, 1),
                        })

        # Update seen state
        seen_update = {
            'hash': h,
            'stage': stage_name,
            'name': t.get('name'),
            'last_seen': now.isoformat(),
        }
        # Track notification timestamps to avoid re-notify on next poll
        if 'sla_breach' in categories:
            seen_update['last_sla_notify'] = now.isoformat()
        # For NEW tasks that already breach SLA: mark as seen so next poll won't re-alert
        elif prev is None and not categories:
            pass
        elif prev is None:
            # New task: if it would breach SLA, pre-mark it so next poll doesn't double-notify
            last_activity = max(write_dt, stage_dt) if write_dt and stage_dt else (write_dt or stage_dt)
            if last_activity:
                hours_since = (now - last_activity).total_seconds() / 3600
                if hours_since >= sla_hours:
                    seen_update['last_sla_notify'] = now.isoformat()
        if 'deadline_soon' in categories:
            seen_update['last_deadline_notify'] = t.get('date_deadline')
        # Preserve existing notification timestamps from previous state
        if prev:
            for k in ('last_sla_notify', 'last_deadline_notify'):
                if k not in seen_update and k in prev:
                    seen_update[k] = prev[k]
        seen[tid] = seen_update

    # Determine which tasks should trigger notification
    notify_tasks = new_tasks + changed_tasks + sla_breach_tasks + deadline_soon_tasks

    # Save updated state
    save_poll_state(employee_id, {'seen_tasks': seen, 'last_poll': now.isoformat()})

    return {
        'employee_id': employee_id,
        'user_id': user_id,
        'poll_time': now.isoformat(),
        'total_pending': len(all_pending),
        'notify_count': len(notify_tasks),
        'summary': {
            'new': len(new_tasks),
            'changed': len(changed_tasks),
            'sla_breach': len(sla_breach_tasks),
            'deadline_soon': len(deadline_soon_tasks),
            'stale': len(stale_tasks),
        },
        'notify_tasks': notify_tasks,
        'all_pending': all_pending,
    }


def main():
    parser = argparse.ArgumentParser(description='Poll tasks from Zrise for employee')
    parser.add_argument('--employee-id', type=int, required=True)
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--sla-hours', type=int, default=24,
                        help='Notify if no update for N hours (default: 24)')
    parser.add_argument('--deadline-hours', type=int, default=48,
                        help='Notify if deadline within N hours (default: 48)')
    parser.add_argument('--stale-hours', type=int, default=72,
                        help='Mark stale if no update for N hours (default: 72)')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    parser.add_argument('--notify-only', action='store_true',
                        help='Only output tasks that need notification')
    args = parser.parse_args()

    result = poll_tasks(
        args.employee_id,
        limit=args.limit,
        sla_hours=args.sla_hours,
        deadline_hours=args.deadline_hours,
        stale_hours=args.stale_hours,
    )

    if args.json:
        if args.notify_only:
            output = {
                'notify_count': result.get('notify_count', 0),
                'summary': result.get('summary', {}),
                'notify_tasks': result.get('notify_tasks', []),
            }
            print(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result.get('error'):
            print(f"❌ {result['error']}")
            sys.exit(1)

        summary = result.get('summary', {})
        print(f"📋 Pending: {result['total_pending']} | Notify: {result['notify_count']}")
        if summary.get('new'):
            print(f"  🆕 New: {summary['new']}")
        if summary.get('changed'):
            print(f"  🔄 Changed: {summary['changed']}")
        if summary.get('sla_breach'):
            print(f"  ⚠️  SLA breach (> {args.sla_hours}h no update): {summary['sla_breach']}")
        if summary.get('deadline_soon'):
            print(f"  🔴 Deadline soon (< {args.deadline_hours}h): {summary['deadline_soon']}")

        for t in result.get('notify_tasks', []):
            tags = []
            if 'hours_since_update' in t:
                tags.append(f"{t['hours_since_update']}h no update")
            if 'hours_until_deadline' in t:
                tags.append(f"{t['hours_until_deadline']}h to deadline")
            tag_str = f" [{', '.join(tags)}]" if tags else ""
            print(f"  - [{t['task_id']}] {t['name']} ({t['stage']}){tag_str}")


if __name__ == '__main__':
    main()
