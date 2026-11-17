"""Read-only local sync status. Never reads Reminders or recovers ledger writes."""
import datetime as dt
from pathlib import Path
import re
from macos_sync_schedule import NativeSchedule, PLAN_TIMES, BEIJING, ScheduleError


def next_slot(now=None):
    stamp = (now or dt.datetime.now(BEIJING)).astimezone(BEIJING)
    for offset in (0, 1):
        day = stamp.date() + dt.timedelta(days=offset)
        for clock in PLAN_TIMES:
            candidate = dt.datetime.combine(day, dt.time.fromisoformat(clock), BEIJING)
            if candidate > stamp:
                return candidate.isoformat(timespec='minutes')


def package_identity():
    script = Path(__file__).resolve()
    match = re.search(r'^  version: "([^"]+)"$',
                      (script.parent.parent / 'SKILL.md').read_text(), re.MULTILINE)
    return {'packageVersion': match.group(1) if match else None,
            'scriptPath': str(script.parent / 'macos_reminders_sync.py')}


def local_task_status(directory, task_id, state_root=None, list_name=None):
    from task_store import TaskStore, StoreError, status_history_fingerprint
    from reminders_state import MirrorState, StateError
    if not re.fullmatch(r'T-\d{6}-\d{3,}', task_id):
        return {'ok': False, 'code': 'invalid_task_id', 'taskId': task_id}
    try:
        docs = TaskStore(directory, timeout=1).execute({'op': 'inspect'})['ledgers']
        found = [(name, task) for name, doc in docs.items() for task in doc['tasks']
                 if task['id'] == task_id]
        if not found:
            return {'ok': False, 'code': 'task_not_found', 'taskId': task_id}
        ledger, task = found[0]
        statuses = [h for h in task['history'] if h.get('action') in ('status', 'reopen')]
        receipts = []
        for entry in statuses:
            detail = entry.get('detail')
            if isinstance(detail, dict) and detail.get('status') == 'done' and detail.get('externalCompletion'):
                try:
                    source = TaskStore.external_source(detail['externalCompletion'])
                except StoreError:
                    continue
                receipts.append({'recordedAt': entry['at'], 'source': source})
        last = statuses[-1] if statuses else None
        latest_receipt = (receipts[-1] if receipts and last and
                          receipts[-1]['recordedAt'] == last['at'] and
                          isinstance(last.get('detail'), dict) and
                          last['detail'].get('externalCompletion') == receipts[-1]['source'] else None)
        origin = ('macos-reminders-record' if task['status'] == 'done' and latest_receipt else
                  'ledger' if task['status'] == 'done' and last and
                  isinstance(last.get('detail'), dict) and last['detail'].get('status') == 'done' else 'unknown')
        result = {'ok': True, 'code': 'local_task_status', 'taskId': task_id,
                  'ledgerStatus': task['status'], 'ledgerFile': ledger,
                  'completedAt': task.get('completedAt'), 'lastStatusHistory': last,
                  'currentCompletionOrigin': origin, 'nativeCompletionHistory': receipts,
                  'mapping': None, 'mappingStatusHistoryMatches': None,
                  'currentNativeVerified': False}
        try:
            state = MirrorState(directory, list_name, state_root)
            binding = state.binding()
            if binding and binding['phase'] == 'complete':
                row = state.mapping(binding)['tasks'].get(task_id)
                result['mapping'] = row
                if row:
                    result['mappingStatusHistoryMatches'] = row.get('observedFingerprint') == status_history_fingerprint(task)
        except StateError as exc:
            result['mappingError'] = {'code': exc.code, 'message': str(exc)}
        return result
    except (StoreError, OSError, ValueError) as exc:
        return {'ok': False, 'code': getattr(exc, 'code', 'inspect_unavailable'),
                'taskId': task_id, 'message': str(exc)}


def sync_status(directory, state_root=None, *, bootstrap, now=None, task_id=None, list_name=None):
    schedule = NativeSchedule(directory, state_root)
    background = schedule.status()
    try:
        mirror = bootstrap(directory, state_root)
    except Exception as exc:
        # Only expected local-state errors may be represented as an unavailable mirror.
        from reminders_state import StateError
        if not isinstance(exc, StateError):
            raise
        mirror = {'initialized': False, 'error': {'code': exc.code, 'message': str(exc)}}
    enabled = bool(background['enabled'] and mirror['initialized'])
    last = background.get('lastSync')
    last_failed = isinstance(last, dict) and last.get('ok') is False
    message = ('后台同步已启用，下一时点将处理最新台账；当前状态未进行原生核验。'
               if enabled else '后台同步未就绪；台账保存不受影响，提醒事项不会自动更新。')
    if last_failed:
        message += ' 上次同步失败：' + str(last.get('code', 'unknown')) + '；尚未确认提醒事项已更新。'
    result = {'ok': True, 'code': 'sync_status', 'mirror': mirror,
            **package_identity(),
            'backgroundEnabled': bool(background['enabled']),
            'nextSyncAt': next_slot(now) if enabled else None,
            'lastSync': last, 'lastSyncAt': last.get('finishedAt') if isinstance(last, dict) else None,
            'currentSyncVerified': False, 'callsNative': False,
            'lastSyncFailed': last_failed,
            'message': message}
    if task_id is not None:
        result['task'] = local_task_status(directory, task_id, state_root, list_name)
        if not result['task']['ok']:
            result.update(ok=False, code=result['task']['code'])
            result['message'] += ' 本地任务状态暂不可用；没有启动原生查询。'
        elif result['task']['currentCompletionOrigin'] == 'macos-reminders-record':
            result['message'] += ' 台账已完成，最近状态历史记录了原生完成回写；当前提醒事项状态未核验。'
        else:
            result['message'] += ' 台账状态为 ' + result['task']['ledgerStatus'] + '；不能据此认定本次原生勾选已收到。'
    return result
