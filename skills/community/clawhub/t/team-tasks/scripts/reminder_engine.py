#!/usr/bin/env python3
"""Build and reserve risk-based team-task reminders.

This is deliberately a policy and storage adapter, not a scheduler or a
notification client.  A trusted integration invokes it at the configured
time, optionally overrides the bundled holiday calendar, sends the returned messages, and
uses the returned ``scheduledFor`` value for its randomized delivery time.
"""

import argparse
import datetime as dt
import json
import random
import sys
from pathlib import Path

from task_store import MAIN, StoreError, TaskStore
from calendar_data import CalendarError, CN_TZ, load_builtin_calendar, require_years


SLOTS = ('09:00', '10:00', '14:00', '18:00')
LEVELS = ('low', 'medium', 'high', 'critical')
LEVEL_NUMBER = {level: number for number, level in enumerate(LEVELS)}
URGENCY_NUMBER = {'overdue': 4, 'today': 3, 'soon': 2, 'normal': 1, 'none': 0}
PRIORITY_NUMBER = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}


def calendar_time(now, calendar):
    """Use the bundled calendar's civil timezone; preserve legacy overrides."""
    if isinstance(calendar, dict) and calendar.get('timezone') == 'Asia/Shanghai':
        return now.astimezone(CN_TZ)
    return now


def parse_now(value=None):
    if value is None:
        return dt.datetime.now().astimezone()
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError('--now must include a UTC offset')
    return parsed


def due_at(task, tzinfo):
    """Return the effective deadline; a date-only deadline ends that day."""
    due_date = task.get('dueDate')
    if due_date in (None, '', 'none'):
        return None
    day = dt.date.fromisoformat(due_date)
    due_time = task.get('dueTime')
    clock = dt.time.fromisoformat(due_time) if due_time not in (None, '', 'none') else dt.time.max
    return dt.datetime.combine(day, clock, tzinfo=tzinfo)


def urgency_for(task, now):
    deadline = due_at(task, now.tzinfo)
    if deadline is None:
        return 'none', None
    if now > deadline:
        return 'overdue', deadline
    if deadline.date() == now.date() or deadline - now <= dt.timedelta(hours=24):
        return 'today', deadline
    if deadline - now <= dt.timedelta(hours=72):
        return 'soon', deadline
    return 'normal', deadline


def raise_level(level):
    return LEVELS[min(LEVEL_NUMBER[level] + 1, len(LEVELS) - 1)]


def attention_for(task, urgency, stale_workdays=0):
    """Combine business priority, time risk, and blocking without mutating a task."""
    priority = task.get('priority', 'medium')
    if priority not in PRIORITY_NUMBER:
        priority = 'medium'
    attention = priority
    if urgency == 'overdue':
        attention = max((attention, 'high'), key=LEVEL_NUMBER.get)
    elif urgency == 'today':
        attention = max((attention, 'high'), key=LEVEL_NUMBER.get)
        if priority in ('high', 'critical'):
            attention = 'critical'
    elif urgency == 'soon':
        attention = max((attention, 'medium'), key=LEVEL_NUMBER.get)
    if task.get('isBlocking'):
        attention = raise_level(attention)
    reasons = []
    if stale_workdays > 3:
        before = attention
        attention = raise_level(attention)
        if attention != before:
            reasons.append('stale_over_3_workdays')
    if stale_workdays > 5 and LEVEL_NUMBER[attention] < LEVEL_NUMBER['high']:
        attention = 'high'
        reasons.append('stale_over_5_workdays')
    if task.get('isBlocking') and stale_workdays > 3 and LEVEL_NUMBER[attention] < LEVEL_NUMBER['high']:
        attention = 'high'
        reasons.append('blocking_stale_over_3_workdays')
    if stale_workdays > 10 and LEVEL_NUMBER[attention] < LEVEL_NUMBER['critical']:
        attention = 'critical'
        reasons.append('stale_over_10_workdays')
    return attention, reasons


def classified(task, now, calendar=None):
    now = calendar_time(now, calendar)
    require_years(calendar, {now.year})
    urgency, deadline = urgency_for(task, now)
    priority = task.get('priority', 'medium')
    if priority not in PRIORITY_NUMBER:
        priority = 'medium'
    stale_workdays = stale_workdays_for(task, now, calendar)
    attention, reasons = attention_for(task, urgency, stale_workdays)
    return {**task, 'priority': priority, 'urgency': urgency, 'deadline': deadline,
            'staleWorkdays': stale_workdays, 'attentionReasons': reasons,
            'attentionLevel': attention}


def action_sort_key(task):
    deadline = task['deadline'] or dt.datetime.max.replace(tzinfo=dt.timezone.utc)
    # Earlier deadline wins within identical risk, followed by stable task ID.
    return (-LEVEL_NUMBER[task['attentionLevel']], -URGENCY_NUMBER[task['urgency']],
            -PRIORITY_NUMBER[task['priority']], not task.get('isBlocking', False), deadline, task['id'])


def is_summary_candidate(task):
    return (task['urgency'] in ('overdue', 'today', 'soon') or
            (task.get('isBlocking') and task['priority'] in ('critical', 'high')) or
            (task['deadline'] is None and not task.get('isBlocking') and task['staleWorkdays'] > 3))


def selected_for_slot(tasks, slot):
    if slot == '09:00':
        return sorted((task for task in tasks if is_summary_candidate(task)), key=action_sort_key)[:5]
    # An unscheduled task does not become a daytime interruption merely because
    # it has a high business priority; a blocking item is the explicit exception.
    high_frequency = [task for task in tasks
                      if task['urgency'] != 'none' or task.get('isBlocking')]
    selected = [task for task in high_frequency if task['attentionLevel'] == 'critical']
    if slot in ('10:00', '18:00'):
        selected.extend(task for task in high_frequency
                        if task['attentionLevel'] != 'critical' and task['priority'] == 'high')
        selected.extend(task for task in tasks
                        if task['deadline'] is None and not task.get('isBlocking') and
                        task['staleWorkdays'] > 10 and task not in selected)
    return sorted(selected, key=action_sort_key)


def due_label(task):
    if task['deadline'] is None:
        return '未排期'
    return task['deadline'].isoformat(timespec='minutes')


def snoozed(task, now):
    value = task.get('snoozedUntil')
    if value in (None, '', 'none'):
        return False
    try:
        until = dt.datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return False
    if until.tzinfo is None:
        return False
    return until > now


def parse_timestamp(value, tzinfo):
    if not isinstance(value, str):
        return None
    try:
        parsed = dt.datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(tzinfo)


def progress_at(task, now):
    """Return the explicitly recorded progress, then a marked comment, then creation."""
    explicit = parse_timestamp(task.get('lastProgressAt'), now.tzinfo)
    if explicit is not None:
        return explicit
    for comment in reversed(task.get('comments', [])):
        if comment.get('meaningfulProgress'):
            progress = parse_timestamp(comment.get('at'), now.tzinfo)
            if progress is not None:
                return progress
    return parse_timestamp(task.get('createdAt'), now.tzinfo)


def snooze_intervals(task, now):
    """Recover known snooze intervals from append-only task history."""
    intervals = []
    active = None
    for entry in task.get('history', []):
        stamp = parse_timestamp(entry.get('at'), now.tzinfo)
        if stamp is None:
            continue
        detail = entry.get('detail')
        if not isinstance(detail, dict):
            continue
        values = detail.get('changes') if entry.get('action') == 'update' else detail.get('fields')
        if not isinstance(values, dict) or 'snoozedUntil' not in values:
            continue
        if active is not None:
            intervals.append((active[0], min(active[1], stamp)))
            active = None
        until = parse_timestamp(values.get('snoozedUntil'), now.tzinfo)
        if until is not None and until > stamp:
            active = (stamp, until)
    if active is not None:
        intervals.append(active)
    return intervals


def date_is_snoozed(day, intervals):
    day_start = dt.datetime.combine(day, dt.time.min, tzinfo=intervals[0][0].tzinfo) if intervals else None
    day_end = day_start + dt.timedelta(days=1) if day_start else None
    return any(start < day_end and end > day_start for start, end in intervals)


def stale_workdays_for(task, now, calendar=None):
    now = calendar_time(now, calendar)
    progress = progress_at(task, now)
    if progress is None or progress.date() >= now.date():
        return 0
    intervals = snooze_intervals(task, now)
    days = 0
    day = progress.date() + dt.timedelta(days=1)
    last = now.date() - dt.timedelta(days=1)
    if day <= last:
        require_years(calendar, range(day.year, last.year + 1))
    while day < now.date():
        if is_working_day(day, calendar) and not date_is_snoozed(day, intervals):
            days += 1
        day += dt.timedelta(days=1)
    return days


# Separate entries into paragraphs for channels that collapse soft line breaks.
ENTRY_SEPARATOR = '\n\n'
TITLE = '**{text}**'


def bold(text):
    return TITLE.format(text=text)


def render_summary(tasks, pending_total):
    lines = [bold('团队任务晨间摘要')]
    for task in tasks:
        lines.append('{id} {title} ｜ 负责人：{assignee} ｜ 截止：{due} ｜ 紧急度：{urgency}{stale}'.format(
            id=bold('[{}]'.format(task['id'])), title=task['title'], assignee=task.get('assignee') or '未分配',
            due=due_label(task), urgency=task['urgency'], stale=stale_label(task)))
    lines.append('另有 {} 项待处理任务。'.format(pending_total - len(tasks)))
    return ENTRY_SEPARATOR.join(lines)


def render_focus(tasks, slot):
    lines = [bold('团队任务重点提醒 {}'.format(slot))]
    for task in tasks:
        lines.append('{id} {title} ｜ 负责人：{assignee} ｜ 截止：{due} ｜ 重要性：{priority} ｜ 紧急度：{urgency} ｜ 关注度：{attention}{stale}'.format(
            id=bold('[{}]'.format(task['id'])), title=task['title'], assignee=task.get('assignee') or '未分配',
            due=due_label(task), priority=task['priority'], urgency=task['urgency'],
            attention=task['attentionLevel'], stale=stale_label(task)))
    return ENTRY_SEPARATOR.join(lines)


def slot_key(now, slot):
    offset = now.strftime('%z')
    offset = offset[:3] + ':' + offset[3:] if offset else ''
    return '{}T{}{}'.format(now.date().isoformat(), slot, offset)


def stale_label(task):
    if not task.get('attentionReasons'):
        return ''
    return ' ｜ 无有效进展：{} 个工作日 ｜ 上调原因：{}'.format(
        task['staleWorkdays'], '；'.join(task['attentionReasons']))


def normalize_calendar(calendar):
    if calendar is None:
        return {'holidays': set(), 'makeupWorkdays': set()}
    if isinstance(calendar, set):  # Legacy in-process callers.
        return {'holidays': calendar, 'makeupWorkdays': set()}
    return calendar


def is_working_day(day, calendar=None):
    current = normalize_calendar(calendar)
    require_years(current, {day.year})
    if day in current['holidays']:
        return False
    if day in current['makeupWorkdays']:
        return True
    return day.weekday() < 5


def load_holidays(path):
    if path is None:
        return load_builtin_calendar()
    values = json.loads(Path(path).read_text(encoding='utf-8'))
    if isinstance(values, list):
        values = {'holidays': values, 'makeupWorkdays': []}
    if not isinstance(values, dict) or set(values) - {'holidays', 'makeupWorkdays'}:
        raise CalendarError('calendar_invalid', 'holiday file must be a JSON date array or calendar object')
    try:
        holidays = values.get('holidays', [])
        makeup = values.get('makeupWorkdays', [])
        if not isinstance(holidays, list) or not isinstance(makeup, list):
            raise ValueError
        if not all(isinstance(value, str) for value in holidays + makeup):
            raise ValueError
        if any(dt.date.fromisoformat(value).isoformat() != value for value in holidays + makeup):
            raise ValueError
        holidays, makeup = {dt.date.fromisoformat(value) for value in holidays}, {dt.date.fromisoformat(value) for value in makeup}
    except (TypeError, ValueError):
        raise CalendarError('calendar_invalid', 'calendar dates must be YYYY-MM-DD strings') from None
    conflicts = sorted(day.isoformat() for day in holidays & makeup)
    if conflicts:
        raise CalendarError('calendar_conflict', 'calendar holidays conflict with makeup workdays', conflicts)
    return {'holidays': holidays, 'makeupWorkdays': makeup}


def build_plan(doc, now, slot, holidays):
    now = calendar_time(now, holidays)
    require_years(holidays, {now.year})
    if not is_working_day(now.date(), holidays):
        return {'silent': True, 'reason': 'non_working_day', 'pendingTotal': 0, 'tasks': []}
    pending = [classified(task, now, holidays) for task in doc['tasks']
               if task.get('status') == 'pending' and not snoozed(task, now)]
    receipt_key = slot_key(now, slot)
    receipts = doc.get('_reminderReceipts', {})
    candidates = [task for task in selected_for_slot(pending, slot)
                  if receipt_key not in receipts.get(task['id'], []) and task.get('lastRemindedSlot') != receipt_key]
    if not candidates:
        return {'silent': True, 'reason': 'no_eligible_tasks', 'pendingTotal': len(pending), 'tasks': []}
    text = render_summary(candidates, len(pending)) if slot == '09:00' else render_focus(candidates, slot)
    return {'silent': False, 'reason': None, 'pendingTotal': len(pending), 'tasks': candidates, 'text': text,
            'receiptSlot': receipt_key}


def execute(data_dir, now, slot, holidays, reserve=False, delay_minutes=None):
    now = calendar_time(now, holidays)
    require_years(holidays, {now.year})
    store = TaskStore(data_dir)
    doc = store.execute({'op': 'read'})['ledgers'][MAIN]
    plan = build_plan(doc, now, slot, holidays)
    delay = random.SystemRandom().randint(0, 15) if delay_minutes is None else delay_minutes
    result = {key: value for key, value in plan.items() if key != 'tasks'}
    result.update(slot=slot, scheduledFor=(now + dt.timedelta(minutes=delay)).isoformat(timespec='minutes'),
                  delayMinutes=delay, selected=[task['id'] for task in plan['tasks']], reserved=[])
    if reserve:
        for task in plan['tasks']:
            try:
                receipt = store.execute({'op': 'remind', 'id': task['id'], 'slot': plan['receiptSlot']})
            except StoreError as exc:
                if exc.code not in ('conflict', 'not_found'):
                    raise
                continue
            if not receipt.get('duplicate'):
                result['reserved'].append(task['id'])
        if not result['reserved'] and plan['tasks']:
            result.update(silent=True, reason='already_reserved', text=None)
        elif len(result['reserved']) != len(plan['tasks']):
            sent = set(result['reserved'])
            kept = [task for task in plan['tasks'] if task['id'] in sent]
            result['selected'] = result['reserved']
            result['text'] = render_summary(kept, plan['pendingTotal']) if slot == '09:00' else render_focus(kept, slot)
    return result


def find_task(doc, task_id):
    for task in doc.get('tasks', []):
        if task.get('id') == task_id:
            return task
    return None


def render_task_reminder(task):
    latest_comment = task.get('comments', [])[-1].get('content') if task.get('comments') else '暂无'
    return ENTRY_SEPARATOR.join([
        bold('任务提醒'),
        bold('[{id}] {title}'.format(id=task['id'], title=task['title'])),
        '负责人：{}'.format(task.get('assignee') or '未分配'),
        '截止：{}'.format(due_label(task)),
        '重要性：{}'.format(task['priority']),
        '紧急度：{}'.format(task['urgency']),
        '关注度：{}{}'.format(task['attentionLevel'], stale_label(task)),
        '最新进展：{}'.format(latest_comment),
    ])


def resolve_task_reminder(data_dir, task_id, slot, now, reserve=False, delivery_reference=None, calendar=None):
    """Resolve one dynamic reminder from the current task snapshot.

    ``slot`` is an opaque, adapter-supplied idempotency key and must include a
    date and timezone.  It is deliberately not a scheduler expression.
    """
    if not isinstance(task_id, str) or not task_id:
        raise ValueError('task ID is required')
    now = calendar_time(now, calendar)
    planned = parse_timestamp(slot, now.tzinfo) if isinstance(slot, str) else None
    if planned is None:
        raise ValueError('slot must include date and timezone')
    require_years(calendar, {now.year, planned.year})
    store = TaskStore(data_dir)
    doc = store.execute({'op': 'read'})['ledgers'][MAIN]
    task = find_task(doc, task_id)
    base = {'taskId': task_id, 'slot': slot, 'deliveryReference': delivery_reference}
    if task is None:
        return {**base, 'action': 'silent', 'reason': 'task_not_found'}
    if task.get('status') != 'pending':
        return {**base, 'action': 'silent', 'reason': 'inactive_task', 'status': task.get('status')}
    if snoozed(task, now):
        return {**base, 'action': 'silent', 'reason': 'snoozed', 'status': 'pending'}
    if not is_working_day(planned.date(), calendar):
        return {**base, 'action': 'silent', 'reason': 'non_working_day', 'status': 'pending'}
    current = classified(task, now, calendar)
    if reserve:
        try:
            receipt = store.execute({'op': 'remind', 'id': task_id, 'slot': slot})
        except StoreError as exc:
            if exc.code in ('conflict', 'not_found'):
                return {**base, 'action': 'silent', 'reason': 'state_changed'}
            raise
        if receipt.get('duplicate'):
            return {**base, 'action': 'silent', 'reason': 'already_reserved'}
    return {**base, 'action': 'deliver', 'status': 'pending', 'text': render_task_reminder(current),
            'task': {key: current.get(key) for key in ('id', 'title', 'assignee', 'dueDate', 'dueTime',
                                                       'priority', 'urgency', 'attentionLevel', 'staleWorkdays',
                                                       'attentionReasons')}}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', required=True, help='local team-tasks data directory')
    parser.add_argument('--slot', required=True, help='planned reminder time slot or specialized reminder key')
    parser.add_argument('--task-id', help='resolve one task-backed specialized reminder')
    parser.add_argument('--delivery-reference', help='opaque adapter delivery reference, echoed in output')
    parser.add_argument('--holiday-file', help='override the bundled CN annual calendar with a legacy JSON date array or holidays/makeupWorkdays object')
    parser.add_argument('--now', help='ISO-8601 timestamp with UTC offset; for deterministic runs')
    parser.add_argument('--reserve', action='store_true', help='record task ID + date + slot through task_store before sending')
    parser.add_argument('--delay-minutes', type=int, choices=range(16), metavar='0..15',
                        help='override the 0–15 minute random delivery delay')
    args = parser.parse_args(argv)
    try:
        current = parse_now(args.now)
        calendar = load_holidays(args.holiday_file)
        current = calendar_time(current, calendar)
        require_years(calendar, {current.year})
        if args.task_id:
            output = resolve_task_reminder(Path(args.data_dir), args.task_id, args.slot, current,
                                            reserve=args.reserve,
                                            delivery_reference=args.delivery_reference, calendar=calendar)
        else:
            if args.slot not in SLOTS:
                raise ValueError('--slot must be one of {} for team reminders'.format(', '.join(SLOTS)))
            if args.delivery_reference is not None:
                raise ValueError('--delivery-reference requires --task-id')
            output = execute(Path(args.data_dir), current, args.slot, calendar,
                             reserve=args.reserve, delay_minutes=args.delay_minutes)
    except (StoreError, OSError, ValueError, json.JSONDecodeError) as exc:
        output = {'ok': False, 'code': getattr(exc, 'code', 'validation_failed'), 'message': str(exc)}
        if getattr(exc, 'conflicts', None):
            output['conflicts'] = exc.conflicts
        if getattr(exc, 'missing_years', None):
            output['missingYears'] = exc.missing_years
        print(json.dumps(output, ensure_ascii=False))
        return 1
    print(json.dumps({'ok': True, **output}, ensure_ascii=False, default=str))
    return 0


if __name__ == '__main__':
    sys.exit(main())
