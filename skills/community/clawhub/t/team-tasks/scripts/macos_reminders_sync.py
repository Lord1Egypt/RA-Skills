#!/usr/bin/env python3
"""Mirror every ledger task to one macOS Reminders list, without consuming outbox events."""

import argparse
import copy
import uuid
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager, ExitStack
from reminders_state import MirrorState, StateError, namespace_for, private_directory, read_json, write_json, write_private_bytes, json_bytes, validate_list_name

LIST_NAME = '团队待办（team-tasks）'  # Legacy name; fresh mirrors require --list-name.
BRIDGE = Path(__file__).with_name('macos_reminders.js')
BEIJING = dt.timezone(dt.timedelta(hours=8))
STATUSES = {'pending': '待处理', 'done': '已完成', 'cancelled': '已取消'}
PRIORITIES = {'critical': 1, 'high': 1, 'medium': 5, 'low': 9}


class SyncError(Exception):
    def __init__(self, code, message, details=None):
        self.code, self.details = code, details or {}
        super().__init__(message)


def due_fields(task):
    date = task.get('dueDate')
    if date in (None, '', 'none'):
        return {'kind': 'none'}
    if not isinstance(date, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
        raise SyncError('invalid_due_date', 'Invalid dueDate for ' + task['id'])
    try:
        parsed = dt.date.fromisoformat(date)
        clock = task.get('dueTime')
        if clock in (None, '', 'none'):
            return {'kind': 'allDay', 'date': parsed.isoformat()}
        if not isinstance(clock, str) or not re.fullmatch(r'\d{2}:\d{2}', clock):
            raise ValueError('Expected HH:MM')
        stamp = dt.datetime.combine(parsed, dt.time.fromisoformat(clock), BEIJING)
    except ValueError as exc:
        raise SyncError('invalid_due_date', 'Invalid deadline for ' + task['id']) from exc
    return {'kind': 'timed', 'at': stamp.isoformat(timespec='seconds')}


def build_request(ledgers, directory, namespace=None, *, list_name=LIST_NAME):
    validate_list_name(list_name)
    namespace = namespace or namespace_for(directory)
    items = []
    for name in sorted(ledgers):
        for task in ledgers[name]['tasks']:
            marker = '[team-tasks:v1:{}:{}]'.format(namespace, task['id'])
            title = task.get('title')
            if not isinstance(title, str) or not title.strip():
                raise SyncError('invalid_task', 'Missing title for ' + task['id'])
            priority = task.get('priority', 'medium')
            if priority not in PRIORITIES:
                raise SyncError('invalid_task', 'Invalid priority for ' + task['id'])
            tags = task.get('tags', [])
            if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
                raise SyncError('invalid_task', 'Invalid tags for ' + task['id'])
            body = [marker, '任务 ID：' + task['id'], '状态：' + STATUSES[task['status']],
                    '负责人：' + (task.get('assignee') or '未指定'),
                    '重要性：' + priority, '阻塞：' + ('是' if task.get('isBlocking') else '否')]
            if tags:
                body.append('标签：' + '、'.join(tags))
            if task.get('description'):
                body.extend(['', '描述：', task['description']])
            if task.get('snoozedUntil'):
                body.append('台账暂停提醒至：' + task['snoozedUntil'])
            if task['comments']:
                comment = task['comments'][-1]
                body.extend(['', '最新进展：{} {}\n{}'.format(
                    comment['at'], comment['from'], comment['content'])])
            items.append({'taskId': task['id'], 'marker': marker, 'name': title,
                          'body': '\n'.join(body), 'priority': PRIORITIES[priority],
                          'flagged': bool(task.get('isBlocking')),
                          'completed': task['status'] != 'pending', 'due': due_fields(task)})
    return {'listName': list_name, 'namespace': namespace,
            'items': sorted(items, key=lambda item: item['taskId'])}


@contextmanager
def sync_lock(directory, timeout=30):
    import fcntl
    # Permanent separate lock: do not hold the ledger lock during Automation consent.
    flags = os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW
    fd = os.open(directory / '.macos-reminders.lock', flags, 0o600)
    with os.fdopen(fd, 'a+b') as lock:
        deadline = time.monotonic() + timeout
        while True:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise SyncError('macos_sync_lock_timeout', 'macOS sync is already running; keep its lock file')
                time.sleep(min(.05, max(0, deadline - time.monotonic())))
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def _run_bridge(request):
    # Data is read from a private JSON file by a fixed script, never evaluated as code.
    with tempfile.TemporaryDirectory(prefix='team-tasks-reminders-') as directory:
        payload = Path(directory) / 'request.json'
        with payload.open('x', encoding='utf-8') as stream:
            os.chmod(payload, 0o600)
            json.dump(request, stream, ensure_ascii=False, allow_nan=False)
        try:
            result = subprocess.run(['/usr/bin/osascript', '-l', 'JavaScript', str(BRIDGE), str(payload)],
                                    capture_output=True, text=True, timeout=15 if request.get('mode') == 'probe' else 120, check=False)
        except subprocess.TimeoutExpired as exc:
            raise SyncError('macos_probe_timeout' if request.get('mode') == 'probe' else 'macos_sync_timeout',
                            'Native probe timed out; no retry was started' if request.get('mode') == 'probe'
                            else 'Reminders did not finish; rerun sync to reconcile partial writes') from exc
    if result.returncode != 0:
        code = 'macos_permission_denied' if '-1743' in result.stderr else 'macos_bridge_error'
        raise SyncError(code, result.stderr.strip() or 'osascript failed')
    try:
        response = json.loads(result.stdout)
    except ValueError as exc:
        raise SyncError('macos_bridge_error', 'Reminders returned invalid JSON; rerun sync to reconcile') from exc
    if not isinstance(response, dict) or type(response.get('ok')) is not bool:
        raise SyncError('macos_bridge_error', 'Reminders returned an invalid result')
    return response



BRIDGE_TIMINGS = {}


def run_bridge(request):
    started = time.monotonic()
    BRIDGE_TIMINGS['bridgeCalls'] = BRIDGE_TIMINGS.get('bridgeCalls', 0) + 1
    BRIDGE_TIMINGS['lastBridgeMode'] = request.get('mode', 'unknown')
    try:
        result = _run_bridge(request)
        for key, value in result.get('timings', {}).items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                BRIDGE_TIMINGS[key] = BRIDGE_TIMINGS.get(key, 0) + value
        return result
    finally:
        BRIDGE_TIMINGS['bridgeMs'] = BRIDGE_TIMINGS.get('bridgeMs', 0) + round((time.monotonic() - started) * 1000, 2)



class RemindersClient:
    def __init__(self, namespace, *, list_name=LIST_NAME):
        self.namespace = namespace
        self.list_name = validate_list_name(list_name)

    def call(self, mode, **fields):
        result = run_bridge({'mode': mode, 'listName': self.list_name, 'namespace': self.namespace, **fields})
        if not result['ok']:
            raise SyncError(result.get('code', 'macos_bridge_error'), result.get('message', '原生同步失败'), result)
        return result

    def probe(self):
        return self.call('probe')['snapshot']

    def read(self):
        return self.call('read')['snapshot']

    def ensure_list(self):
        return self.call('ensure_list')['snapshot']

    def apply(self, list_id, operations, *, initialization_markers=None):
        fields = {} if initialization_markers is None else {'initializationMarkers': initialization_markers}
        return self.call('apply', listId=list_id, operations=operations, **fields)


@contextmanager
def adapter_locks(state, scheduled=False):
    import fcntl
    private_directory(state.binding_dir)
    fd = os.open(state.binding_lock, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'a+b') as lock, ExitStack() as stack:
        deadline = time.monotonic() + (0 if scheduled else 30)
        while True:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise SyncError('macos_sync_lock_timeout', '目标列表正在同步')
                time.sleep(.05)
        try:
            stack.enter_context(sync_lock(state.root, timeout=0 if scheduled else 30))
            state.check_ledger_binding()
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def target_ids(snapshot):
    """Resolve ancestry once per snapshot, including nested reminders."""
    index = {entry['id']: entry for entry in snapshot['reminders']}
    membership = {snapshot.get('listId'): True} if snapshot.get('listId') else {}
    for native_id in index:
        trail, seen, current = [], set(), native_id
        while current in index and current not in membership and current not in seen:
            seen.add(current)
            trail.append(current)
            current = index[current].get('containerId')
        included = membership.get(current, False)
        for ancestor in trail:
            membership[ancestor] = included
    return {native_id for native_id in index if membership.get(native_id)}


def belongs(item, snapshot, scope=None):
    return item['id'] in (target_ids(snapshot) if scope is None else scope)


def target_items(snapshot):
    scope = target_ids(snapshot)
    return [item for item in snapshot['reminders'] if item['id'] in scope]


def marker_index(snapshot, namespace):
    index = {}
    prefix = '[team-tasks:v1:' + namespace + ':'
    for entry in snapshot['reminders']:
        marker = (entry.get('body') or '').split('\n')[0]
        if marker in index and marker.startswith(prefix):
            raise SyncError('macos_task_conflict', '存在重复的任务标记')
        index[marker] = entry
    return index


def stamp_value(value):
    if value is None:
        return None
    parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Timestamp requires timezone')
    return parsed.astimezone(dt.timezone.utc).isoformat()


def desired_fields(item):
    due = copy.deepcopy(item['due'])
    alarm = None
    if due['kind'] == 'timed':
        due['at'] = stamp_value(due['at'])
        alarm = due['at']
    return {key: item[key] for key in ('name', 'body', 'priority', 'flagged', 'completed')} | {'due': due, 'remindMeDate': alarm}


def different(item, remote):
    actual = {key: remote.get(key) for key in ('name', 'body', 'priority', 'flagged', 'completed', 'due', 'remindMeDate')}
    actual['due'] = copy.deepcopy(actual['due'])
    if actual['due'] and actual['due'].get('kind') == 'timed':
        actual['due']['at'] = stamp_value(actual['due']['at'])
    actual['remindMeDate'] = stamp_value(actual['remindMeDate'])
    return [key for key, value in desired_fields(item).items() if value != actual[key]]


def completion_request(task, remote, namespace, fingerprint):
    completion = stamp_value(remote.get('completionDate'))
    if completion is None:
        raise ValueError('Missing completion time')
    token_data = [namespace, task['id'], remote['id'], completion, fingerprint]
    receipt = hashlib.sha256(json.dumps(token_data, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
    return {'op': 'complete_external', 'actor': 'macos-reminders-adapter', 'id': task['id'],
            'expected': {'status': 'pending', 'historyFingerprint': fingerprint},
            'source': {'kind': 'macos-reminders', 'namespace': namespace, 'reminderId': remote['id'],
                       'completionDate': completion, 'receiptId': receipt}}


def build_plan(ledgers, request, snapshot, mapping):
    from task_store import status_history_fingerprint
    planned = copy.deepcopy(mapping)
    tasks = {task['id']: task for doc in ledgers.values() for task in doc['tasks']}
    by_id = {entry['id']: entry for entry in snapshot['reminders']}
    by_marker = marker_index(snapshot, request['namespace'])
    scope = target_ids(snapshot)
    result = {'operations': [], 'completions': [], 'conflicts': [], 'changes': [], 'mapping': planned}
    counts = dict(create=0, update=0, unchanged=0, writeback=0, missing=0, detached=0, conflicts=0)
    for item in request['items']:
        tid, task = item['taskId'], tasks[item['taskId']]
        fingerprint = status_history_fingerprint(task)
        previous = mapping['tasks'].get(tid)
        remote = by_marker.get(item['marker'])
        if previous and previous['reminderId'] in by_id:
            mapped = by_id[previous['reminderId']]
            if (mapped.get('body') or '').split('\n')[0] != item['marker']:
                result['conflicts'].append({'taskId': tid, 'reason': 'marker_changed'})
                continue
            if remote and remote['id'] != mapped['id']:
                raise SyncError('macos_task_conflict', '映射 ID 与标记 ID 不一致：' + tid)
            remote = mapped
        local_changed = bool(previous and previous.get('observedFingerprint') and previous['observedFingerprint'] != fingerprint)
        if remote and not belongs(remote, snapshot, scope):
            entry = copy.deepcopy(previous or {'reminderId': remote['id'], 'missing': 0})
            entry.update(state='detached', reason='moved')
            planned['tasks'][tid] = entry
            counts['detached'] += 1
            result['changes'].append({'taskId': tid, 'action': 'detached', 'reason': 'moved'})
            continue
        if remote is None:
            if previous and previous.get('reason') == 'moved':
                counts['detached'] += 1
                result['changes'].append({'taskId': tid, 'action': 'detached', 'reason': 'moved'})
                continue
            if previous and not (task['status'] == 'pending' and local_changed):
                entry = planned['tasks'][tid]
                entry['missing'] = previous.get('missing', 0) + 1
                if task['status'] != 'pending' or previous['state'] == 'detached' or entry['missing'] >= 2:
                    entry.update(state='detached', reason='removed')
                    counts['detached'] += 1
                else:
                    counts['missing'] += 1
                result['changes'].append({'taskId': tid, 'action': entry['state'], 'missing': entry['missing']})
                continue
            result['operations'].append({'action': 'create', 'taskId': tid, 'item': item})
            result['changes'].append({'taskId': tid, 'action': 'create'})
            counts['create'] += 1
            continue
        entry = copy.deepcopy(previous or {'reminderId': remote['id'], 'missing': 0, 'pendingFingerprint': None})
        entry.update(reminderId=remote['id'], missing=0)
        if task['status'] == 'pending' and remote['completed']:
            if previous and previous.get('pendingFingerprint') == fingerprint:
                try:
                    inbound = completion_request(task, remote, request['namespace'], fingerprint)
                except (ValueError, TypeError):
                    result['conflicts'].append({'taskId': tid, 'reason': 'completion_time_missing'})
                    continue
                result['completions'].append(inbound)
                result['changes'].append({'taskId': tid, 'action': 'writeback'})
                counts['writeback'] += 1
                continue
            if not local_changed:
                result['conflicts'].append({'taskId': tid, 'reason': 'completion_baseline_missing'})
                continue
        fields = different(item, remote)
        if fields:
            result['operations'].append({'action': 'update', 'taskId': tid, 'id': remote['id'],
                                         'expectedModified': remote.get('modificationDate'), 'item': item})
            result['changes'].append({'taskId': tid, 'action': 'update', 'fields': fields})
            counts['update'] += 1
        else:
            counts['unchanged'] += 1
        entry.update(state='mirrored' if task['status'] == 'pending' else 'terminal', reason=None,
                     observedFingerprint=fingerprint, pendingFingerprint=fingerprint if task['status'] == 'pending' else None)
        planned['tasks'][tid] = entry
    for tid in set(planned['tasks']) - set(tasks):
        planned['tasks'][tid].update(state='detached', reason='source_missing')
    counts['conflicts'] = len(result['conflicts'])
    result['counts'] = counts
    return result


def bootstrap_status(directory, state_root=None, *, list_name=None):
    state = MirrorState(directory, list_name, state_root)
    binding = state.binding()
    initialized = bool(binding and binding['phase'] == 'complete')
    if initialized:
        state.mapping(binding)
    return {'initialized': initialized, 'namespace': state.namespace, 'listName': state.list_name,
            'listId': binding['listId'] if binding else None}


def check_binding(binding, snapshot):
    if snapshot.get('listId') != binding['listId']:
        raise SyncError('binding_conflict', '目标列表消失或被替换，保留绑定记录核查',
                        {'listId': binding['listId'], 'actualListId': snapshot.get('listId')})


def reconcile(state, binding, client, slot=None):
    from task_store import StoreError, TaskStore, status_history_fingerprint
    mapping = state.mapping(binding)
    if slot and mapping.get('lastSuccessfulSlot') == slot:
        return {'ok': True, 'code': 'duplicate_slot', 'action': 'skip', 'slot': slot}
    source = read_snapshot(state.root)
    request = build_request(source['ledgers'], state.root, state.namespace, list_name=state.list_name)
    snapshot = client.read()
    check_binding(binding, snapshot)
    plan = build_plan(source['ledgers'], request, snapshot, mapping)
    completed = []
    for inbound in plan['completions']:
        try:
            TaskStore(state.root).execute(inbound)
            completed.append(inbound['id'])
        except StoreError as exc:
            if exc.code != 'conflict':
                raise SyncError(exc.code, str(exc)) from exc
            plan['conflicts'].append({'taskId': inbound['id'], 'reason': 'ledger_conflict'})
    if plan['completions']:
        source = read_snapshot(state.root)
        request = build_request(source['ledgers'], state.root, state.namespace, list_name=state.list_name)
        fresh = build_plan(source['ledgers'], request, snapshot, mapping)
        rejected = {entry['taskId'] for entry in plan['conflicts'] if entry['reason'] == 'ledger_conflict'}
        skipped = [op for op in fresh['operations'] if op['taskId'] in rejected]
        fresh['operations'] = [op for op in fresh['operations'] if op['taskId'] not in rejected]
        for op in skipped:
            fresh['counts'][op['action']] -= 1
        fresh['changes'] = [entry for entry in fresh['changes'] if entry['taskId'] not in rejected]
        for tid in rejected:
            if tid in mapping['tasks']:
                fresh['mapping']['tasks'][tid] = copy.deepcopy(mapping['tasks'][tid])
            else:
                fresh['mapping']['tasks'].pop(tid, None)
        fresh['conflicts'].extend(entry for entry in plan['conflicts'] if entry['reason'] == 'ledger_conflict')
        plan = fresh
    result_snapshot = snapshot
    if plan['operations']:
        response = client.apply(binding['listId'], plan['operations'])
        if not response.get('ok'):
            raise SyncError(response.get('code', 'macos_sync_error'), response.get('message', '原生写入失败'), response)
        result_snapshot = response['snapshot']
    tasks = {task['id']: task for doc in source['ledgers'].values() for task in doc['tasks']}
    items = {item['taskId']: item for item in request['items']}
    scope = target_ids(result_snapshot)
    final_markers = {marker: row for marker, row in marker_index(result_snapshot, state.namespace).items()
                     if row['id'] in scope}
    for op in plan['operations']:
        tid, item = op['taskId'], items[op['taskId']]
        remote = final_markers.get(item['marker'])
        if remote is None or different(item, remote):
            raise SyncError('macos_verification_failed', '原生字段校验失败：' + tid)
        fp = status_history_fingerprint(tasks[tid])
        plan['mapping']['tasks'][tid] = {'reminderId': remote['id'], 'state': 'mirrored' if tasks[tid]['status'] == 'pending' else 'terminal',
                                         'missing': 0, 'pendingFingerprint': fp if tasks[tid]['status'] == 'pending' else None,
                                         'observedFingerprint': fp, 'nativeModifiedAt': remote.get('modificationDate')}
    if slot and not plan['conflicts']:
        plan['mapping']['lastSuccessfulSlot'] = slot
    state.save_map(plan['mapping'])
    counts = plan['counts']
    counts['writeback'] = len(completed)
    counts['conflicts'] = len(plan['conflicts'])
    return {'ok': not plan['conflicts'], 'code': 'ok' if not plan['conflicts'] else 'sync_conflicts',
            'action': 'sync', 'listName': state.list_name, 'listId': binding['listId'], 'counts': counts,
            'changes': plan['changes'], 'conflicts': plan['conflicts'], 'recoveredTransaction': source['recoveredTransaction']}


def initialize_mirror(state, client):
    from task_store import StoreError, TaskStore
    binding = state.binding()
    check_initialization_recovery(binding)
    source = read_snapshot(state.root)
    request = build_request(source['ledgers'], state.root, state.namespace, list_name=state.list_name)
    if binding and binding['phase'] == 'complete':
        state.mapping(binding)
        return {'ok': True, 'code': 'already_initialized', 'action': 'skip', 'listId': binding['listId']}
    if binding is None:
        if state.map_path.exists() or state.map_path.is_symlink():
            raise SyncError('state_recovery_required', '存在无绑定的映射，不能自动清空列表')
        snapshot = client.read()
        state.check_native_target(snapshot.get('listId'))
        require_empty_target(snapshot)
        if snapshot.get('listId') is None:
            snapshot = client.ensure_list()
        require_empty_target(snapshot)
        state.check_native_target(snapshot['listId'])
        originals = target_items(snapshot)
        operation_id = uuid.uuid4().hex
        backup_path = state.root / 'reminders-backups' / (operation_id + '.json')
        backup = {'format': 1, 'kind': 'script-visible-fields-only', 'listName': state.list_name,
                  'listId': snapshot['listId'], 'namespace': state.namespace,
                  'createdAt': dt.datetime.now(BEIJING).isoformat(), 'reminders': originals}
        write_json(backup_path, backup, exclusive=True)
        binding = {'version': 1, 'listName': state.list_name, 'listId': snapshot['listId'],
                   'namespace': state.namespace, 'dataDir': str(state.root), 'phase': 'prepared',
                   'operationId': operation_id, 'backup': backup_path.name,
                   'backupHash': hashlib.sha256(json_bytes(backup)).hexdigest(),
                   'oldIds': [entry['id'] for entry in originals]}
        state.save_binding(binding)
    snapshot = client.read()
    check_binding(binding, snapshot)
    if not re.fullmatch(r'[a-f0-9]{32}\.json', binding.get('backup', '')):
        raise SyncError('state_recovery_required', '初始化备份路径无效')
    backup = read_json(state.root / 'reminders-backups' / binding['backup'])
    if backup is None or hashlib.sha256(json_bytes(backup)).hexdigest() != binding.get('backupHash'):
        raise SyncError('state_recovery_required', '初始化快照丢失或校验失败，不能继续删除')
    if binding['phase'] in ('prepared', 'deleting_old'):
        require_empty_target(snapshot)
        binding['phase'] = 'rebuilding'
        state.save_binding(binding)
    mapping = state.mapping(binding, required=binding['phase'] == 'verifying')
    if mapping is None:
        mapping = state.empty_map(binding['listId'])
        state.save_map(mapping)
    if binding['phase'] == 'rebuilding':
        snapshot = client.read()
        check_binding(binding, snapshot)
        source = read_snapshot(state.root)
        request = build_request(source['ledgers'], state.root, state.namespace, list_name=state.list_name)
        marker_set = {item['marker'] for item in request['items']}
        extras = [row['id'] for row in target_items(snapshot) if (row.get('body') or '').split('\n')[0] not in marker_set]
        if extras:
            raise SyncError('macos_native_conflict', '初始化期间新增了未关联事项；保留这些新事项并停止', {'unexpectedIds': extras})
        # An earlier create may have committed before its response/map was saved.
        # Reuse normal completion baselines before touching recovered markers.
        recovery = build_plan(source['ledgers'], request, snapshot, mapping)
        for inbound in recovery['completions']:
            try:
                TaskStore(state.root).execute(inbound)
            except StoreError as exc:
                if exc.code != 'conflict':
                    raise SyncError(exc.code, str(exc)) from exc
                recovery['conflicts'].append({'taskId': inbound['id'], 'reason': 'ledger_conflict'})
        if recovery['conflicts']:
            recovery['counts']['conflicts'] = len(recovery['conflicts'])
            return {'ok': False, 'code': 'sync_conflicts', 'action': 'initialize',
                    'listName': state.list_name, 'listId': binding['listId'],
                    'counts': recovery['counts'], 'conflicts': recovery['conflicts']}
        if recovery['completions']:
            source = read_snapshot(state.root)
            request = build_request(source['ledgers'], state.root, state.namespace, list_name=state.list_name)
        from task_store import status_history_fingerprint
        by_marker = marker_index(snapshot, state.namespace)
        scope = target_ids(snapshot)
        operations = []
        for item in request['items']:
            remote = by_marker.get(item['marker'])
            if remote and remote['id'] not in scope:
                raise SyncError('macos_native_conflict', '重建的关联事项已移动，移回目标列表后继续')
            if remote is None:
                operations.append({'action': 'create', 'taskId': item['taskId'], 'item': item})
            elif different(item, remote):
                operations.append({'action': 'update', 'taskId': item['taskId'], 'id': remote['id'],
                                   'expectedModified': remote.get('modificationDate'), 'item': item})
        if operations:
            response = client.apply(binding['listId'], operations, initialization_markers=sorted(marker_set))
            if not response.get('ok'):
                raise SyncError(response.get('code', 'macos_sync_error'), response.get('message', '重建未完成'), response)
            snapshot = response['snapshot']
        by_marker = marker_index(snapshot, state.namespace)
        scope = target_ids(snapshot)
        tasks = {task['id']: task for doc in source['ledgers'].values() for task in doc['tasks']}
        for item in request['items']:
            remote = by_marker.get(item['marker'])
            if not remote or remote['id'] not in scope or different(item, remote):
                raise SyncError('macos_verification_failed', '重建字段不一致：' + item['taskId'])
            fp = status_history_fingerprint(tasks[item['taskId']])
            mapping['tasks'][item['taskId']] = {'reminderId': remote['id'], 'state': 'mirrored' if not item['completed'] else 'terminal',
                'missing': 0, 'pendingFingerprint': fp if not item['completed'] else None, 'observedFingerprint': fp}
        state.save_map(mapping)
        binding['phase'] = 'verifying'
        state.save_binding(binding)
    result = reconcile(state, binding, client)
    if not result['ok']:
        return result
    binding['phase'] = 'complete'
    state.save_binding(binding)
    result.update(code='initialized', backup=str(state.root / 'reminders-backups' / binding['backup']))
    return result


def require_empty_target(snapshot):
    if target_items(snapshot):
        raise SyncError('initialization_target_not_empty',
                        '首次初始化只接受新建或空列表；目标包含事项，请指定其他 --list-name',
                        {'listId': snapshot.get('listId'), 'existingCount': len(target_items(snapshot))})


def check_initialization_recovery(binding):
    if binding and binding['phase'] != 'complete' and binding['oldIds']:
        raise StateError('state_recovery_required',
                         '旧版破坏性初始化尚未完成；保留快照和日志，核查恢复方案，不能继续自动删除或重建')


def rebind_mirror(state, client=None, confirm=None, from_data_dir=None):
    """Transfer location, preserving identity and all native and ledger state.

    Only the binding is committed, last and atomically. A crash during archive
    creation leaves the old binding active; retry never needs to delete state.
    """
    binding = state.read_binding()
    if binding is None:
        raise StateError('initialization_required', '没有可迁移的绑定；先核对 --plan')
    check_initialization_recovery(binding)
    details = state.binding_details(binding)
    committing = confirm is not None or from_data_dir is not None
    same_transfer = (binding['dataDir'] == str(state.root) and from_data_dir is not None and
                     from_data_dir == binding.get('reboundFromDataDir'))
    if committing and (confirm != binding['listId'] or
                       (from_data_dir != binding['dataDir'] and not same_transfer)):
        raise StateError('rebind_confirmation_required',
                         '--rebind 执行需 --confirm 原列表 ID 和 --from-data-dir 原绑定目录，两项必须精确匹配', details)
    source = read_snapshot(state.root)
    mapping = state.mapping(binding, required=binding['phase'] in ('complete', 'verifying'))
    backup_path = state.root / 'reminders-backups' / binding['backup']
    backup = None
    if binding['phase'] != 'complete':
        backup = read_json(backup_path, with_bytes=True)
        if backup is None or hashlib.sha256(json_bytes(backup[0])).hexdigest() != binding['backupHash']:
            raise StateError('state_recovery_required', '未完成初始化的原快照丢失或校验失败；随台账搬迁 reminders-backups 后重试', details)
    native = client or RemindersClient(binding['namespace'], list_name=state.list_name)
    snapshot = native.read()
    check_binding(binding, snapshot)
    request = build_request(source['ledgers'], state.root, binding['namespace'], list_name=state.list_name)
    marker_index(snapshot, binding['namespace'])
    result = {'ok': True, 'code': 'rebind_plan', 'action': 'preview', **details,
              'preservedNamespace': binding['namespace'], 'nativeWrites': 0,
              'nativeSnapshot': {'listId': snapshot['listId'], 'reminders': target_items(snapshot)},
              'message': '迁移仅更新绑定目录，保留命名空间、映射、初始化阶段及原生条目；确认原列表 ID 和原目录后执行。'}
    if binding['phase'] == 'complete':
        preview = build_plan(source['ledgers'], request, snapshot, mapping)
        result.update(counts=preview['counts'], changes=preview['changes'], conflicts=preview['conflicts'])
    if not committing:
        return result
    if binding['dataDir'] == str(state.root):
        return {**result, 'code': 'already_bound', 'action': 'skip'}
    # Validate confirmation, map and native identity before any legacy migration.
    state.migrate_legacy_binding()
    binding = state.read_binding()
    # These reads and the final commit run under the permanent per-list lock.
    binding_snapshot = read_json(state.binding_path, with_bytes=True)
    if binding_snapshot is None or binding_snapshot[0] != binding:
        raise StateError('state_conflict', '迁移期间绑定改变；重新预览')
    map_snapshot = read_json(state.map_path, with_bytes=True)
    if (map_snapshot[0] if map_snapshot else None) != mapping:
        raise StateError('state_conflict', '迁移期间映射改变；重新预览')
    archive_root = private_directory(state.state_root / 'rebind-backups')
    archive = archive_root / uuid.uuid4().hex
    private_directory(archive)
    snapshots = {'binding.json': binding_snapshot}
    if map_snapshot is not None:
        snapshots['reminders-map.json'] = map_snapshot
    if backup is not None:
        snapshots['initialization-backup.json'] = backup
    hashes = {}
    for name, (_, raw) in snapshots.items():
        write_private_bytes(archive / name, raw, exclusive=True)
        archived = read_json(archive / name, with_bytes=True)[1]
        if archived != raw:
            raise StateError('state_recovery_required', '迁移归档回读不一致；保留原绑定')
        hashes[name] = hashlib.sha256(raw).hexdigest()
    stamp = dt.datetime.now(BEIJING).isoformat()
    write_json(archive / 'manifest.json', {'version': 1, 'createdAt': stamp,
               **details, 'files': hashes}, exclusive=True)
    # Persist the newly created archive's parent entries before committing its pointer.
    for parent in (archive_root, state.state_root):
        fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    relocated = {**binding, 'dataDir': str(state.root),
                 'namespaceDir': binding.get('namespaceDir', binding['dataDir']),
                 'reboundFromDataDir': binding['dataDir'],
                 'reboundAt': stamp, 'rebindArchive': str(archive)}
    state.save_binding(relocated)
    return {**result, 'code': 'rebound', 'action': 'rebind', 'archive': str(archive),
            'message': '绑定目录已迁移；完整保留原命名空间和映射，未写入提醒事项。运行 --plan 后继续同步或原初始化。'}


def execute(directory, dry_run=False, *, plan=False, initialize=False, scheduled=False,
            diagnose=False, native_check=False, rebind=False, confirm=None, from_data_dir=None,
            state_root=None, client=None, now=None, list_name=None):
    host = platform.system()
    if host != 'Darwin':
        return {'ok': not scheduled and not diagnose, 'code': 'host_unavailable' if scheduled or diagnose else 'skipped_non_macos', 'action': 'skip', 'platform': host}
    if diagnose and not native_check:
        from macos_sync_status import sync_status
        return {**sync_status(directory, state_root, bootstrap=lambda d, r: bootstrap_status(d, r, list_name=list_name)),
                'requestMode': 'diagnose'}
    slot = None
    if scheduled:
        from macos_sync_schedule import schedule_slot
        slot = schedule_slot(now or dt.datetime.now(BEIJING))
        if slot is None:
            return {'ok': True, 'code': 'outside_schedule', 'action': 'skip'}
    root = Path(directory).resolve()
    state = MirrorState(root, list_name, state_root)
    if rebind:
        if confirm is None and from_data_dir is None:
            return rebind_mirror(state, client)
        with adapter_locks(state):
            return rebind_mirror(state, client, confirm, from_data_dir)
    binding = state.binding()
    check_initialization_recovery(binding)
    if dry_run:
        source = read_snapshot(root)
        request = build_request(source['ledgers'], root, state.namespace, list_name=state.list_name)
        return {'ok': True, 'code': 'dry_run', 'action': 'preview', 'count': len(request['items']),
                'recoveredTransaction': source['recoveredTransaction'], 'request': request}
    native = client or RemindersClient(state.namespace, list_name=state.list_name)
    if plan:
        source = read_snapshot(root)
        request = build_request(source['ledgers'], root, state.namespace, list_name=state.list_name)
        snapshot = native.read()
        if binding is None or binding['phase'] != 'complete':
            counts = {'removeOld': 0, 'create': len(request['items'])}
            changes, conflicts = [], []
            if binding is None:
                if state.map_path.exists() or state.map_path.is_symlink():
                    raise StateError('state_recovery_required', '存在无绑定的映射，不能自动清空列表')
                state.check_native_target(snapshot.get('listId'))
                require_empty_target(snapshot)
            else:
                check_binding(binding, snapshot)
                phase = binding['phase']
                if phase in ('prepared', 'deleting_old'):
                    require_empty_target(snapshot)
                elif phase == 'rebuilding':
                    mapping = state.mapping(binding, required=False) or state.empty_map(binding['listId'])
                    recovery = build_plan(source['ledgers'], request, snapshot, mapping)
                    conflicts.extend(recovery['conflicts'])
                    protected = {entry['taskId'] for entry in recovery['conflicts']}
                    completed = {entry['id'] for entry in recovery['completions']}
                    by_marker = marker_index(snapshot, state.namespace)
                    scope = target_ids(snapshot)
                    counts = dict(removeOld=0, create=0, update=0, unchanged=0)
                    expected = {item['marker'] for item in request['items']}
                    for row in target_items(snapshot):
                        if (row.get('body') or '').split('\n')[0] not in expected:
                            conflicts.append({'reminderId': row['id'], 'reason': 'unexpected_during_initialization'})
                    for item in request['items']:
                        if item['taskId'] in protected:
                            continue
                        if item['taskId'] in completed:
                            counts['writeback'] = counts.get('writeback', 0) + 1
                            changes.append({'taskId': item['taskId'], 'action': 'writeback'})
                            continue
                        remote = by_marker.get(item['marker'])
                        if remote and remote['id'] not in scope:
                            conflicts.append({'taskId': item['taskId'], 'reason': 'moved'})
                            continue
                        fields = different(item, remote) if remote else []
                        action = 'create' if remote is None else ('update' if fields else 'unchanged')
                        counts[action] += 1
                        if action != 'unchanged':
                            changes.append({'taskId': item['taskId'], 'action': action, 'fields': fields})
                else:
                    result = build_plan(source['ledgers'], request, snapshot, state.mapping(binding))
                    counts, changes, conflicts = {'removeOld': 0, **result['counts']}, result['changes'], result['conflicts']
            return {'ok': True, 'code': 'initialization_required', 'action': 'preview', 'listName': state.list_name,
                    'counts': counts, 'changes': changes, 'conflicts': conflicts,
                    'initializationPhase': binding['phase'] if binding else None,
                    'message': '需显式初始化或继续本次初始化；首次只接受新建或空列表。预览未修改提醒事项或映射。'}
        check_binding(binding, snapshot)
        result = build_plan(source['ledgers'], request, snapshot, state.mapping(binding))
        return {'ok': True, 'code': 'plan', 'action': 'preview', 'listName': state.list_name,
                'counts': result['counts'], 'changes': result['changes'], 'conflicts': result['conflicts']}
    if diagnose:
        status = bootstrap_status(root, state_root, list_name=state.list_name)
        if not status['initialized']:
            return {'ok': False, 'code': 'initialization_required', 'requestMode': 'diagnose', **status}
        from task_store import TaskStore, StoreError
        try:
            TaskStore(root, timeout=1).execute({'op': 'inspect'})
        except StoreError as exc:
            raise SyncError(exc.code, str(exc)) from exc
        check_binding(binding, native.probe())
        return {'ok': True, 'code': 'ok', 'requestMode': 'diagnose',
                'callsNative': True, 'nativeProbeVerified': True, **status}
    if not initialize and (binding is None or binding['phase'] != 'complete'):
        return {'ok': False, 'code': 'initialization_required', 'message': '先显式运行 --initialize-mirror；普通和定时同步不会清空列表'}
    try:
        with adapter_locks(state, scheduled):
            state.migrate_legacy_binding()
            binding = state.binding()
            if initialize:
                return initialize_mirror(state, native)
            if binding is None or binding['phase'] != 'complete':
                raise SyncError('initialization_required', '初始化未完成')
            return reconcile(state, binding, native, slot)
    except SyncError as exc:
        if scheduled and exc.code == 'macos_sync_lock_timeout':
            return {'ok': True, 'code': 'busy', 'action': 'skip', 'slot': slot}
        raise


def read_snapshot(directory):
    from task_store import StoreError, TaskStore
    try:
        return TaskStore(directory).execute({'op': 'read'})
    except StoreError as exc:
        raise SyncError(exc.code, str(exc)) from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', required=True)
    parser.add_argument('--state-root', help='Trusted private helper/legacy state directory; list ownership is shared per user')
    parser.add_argument('--list-name', help='Explicit native list name for a new mirror; existing bindings are reused')
    modes = parser.add_mutually_exclusive_group()
    for flag in ('dry-run', 'plan', 'initialize-mirror', 'scheduled', 'diagnose', 'rebind', 'sync-status'):
        modes.add_argument('--' + flag, action='store_true')
    parser.add_argument('--confirm', help='Exact bound native list ID; only with --rebind')
    parser.add_argument('--from-data-dir', help='Exact old bound directory; only with --rebind')
    parser.add_argument('--native-check', action='store_true', help='Explicit single 15s native list probe; only with --diagnose')
    parser.add_argument('--task-id', help='Local task lookup; only with --sync-status or local --diagnose')
    parser.add_argument('--result-file')
    parser.add_argument('--probe-token')
    args = parser.parse_args()
    if (args.confirm is not None or args.from_data_dir is not None) and not args.rebind:
        parser.error('--confirm 和 --from-data-dir 只能用于 --rebind')
    local_status = args.sync_status or (args.diagnose and not args.native_check)
    if args.native_check and not args.diagnose:
        parser.error('--native-check requires --diagnose')
    if args.task_id and not local_status:
        parser.error('--task-id requires local --sync-status or --diagnose')
    if local_status and (args.result_file or args.probe_token):
        parser.error('Local status is read-only; --result-file/--probe-token require --diagnose --native-check')
    started_at = dt.datetime.now(dt.timezone.utc).isoformat()
    started = time.monotonic()
    BRIDGE_TIMINGS.clear()
    try:
        if local_status:
            from macos_sync_status import sync_status, ScheduleError
            try:
                result = sync_status(args.data_dir, args.state_root, bootstrap=lambda d, r: bootstrap_status(d, r, list_name=args.list_name),
                                     task_id=args.task_id, list_name=args.list_name)
            except ScheduleError as exc:
                raise SyncError(exc.code, str(exc)) from exc
        else:
            result = execute(args.data_dir, args.dry_run, plan=args.plan, initialize=args.initialize_mirror,
                             scheduled=args.scheduled, diagnose=args.diagnose, native_check=args.native_check, rebind=args.rebind,
                             confirm=args.confirm, from_data_dir=args.from_data_dir, state_root=args.state_root, list_name=args.list_name)
    except (StateError, SyncError) as exc:
        result = {'ok': False, 'code': exc.code, 'message': str(exc), **getattr(exc, 'details', {})}
        result['ok'] = False
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = {'ok': False, 'code': 'macos_sync_error', 'message': str(exc)}
    if not local_status and result.get('code') not in ('outside_schedule', 'duplicate_slot'):
        result['startedAt'] = started_at
        result['finishedAt'] = dt.datetime.now(dt.timezone.utc).isoformat()
        result['timings'] = {**BRIDGE_TIMINGS, 'totalMs': round((time.monotonic() - started) * 1000, 2)}
    if args.diagnose:
        result['requestMode'] = 'diagnose'
    if args.probe_token:
        result['probeToken'] = args.probe_token
    if not result['ok']:
        result['recoveryAdvice'] = '保留已提交台账、映射和初始化日志；只重试同步或恢复状态，不重放创建/评论，不删除初始化记录。'
        if result['code'] == 'macos_permission_denied':
            result['recoveryAdvice'] += ' 在系统设置→隐私与安全性→自动化中授权实际运行宿主访问提醒事项。'
        elif result['code'] == 'binding_conflict' and result.get('boundDataDir'):
            result['recoveryAdvice'] = '独立台账请指定未占用的 --list-name；同一台账完整搬迁才使用 --rebind。保留映射和绑定，不删除状态或清空列表来解除冲突。'
    if args.result_file:
        try:
            # Preserve the last useful result rather than overwriting it every idle minute.
            if result.get('code') not in ('outside_schedule', 'duplicate_slot'):
                write_json(Path(args.result_file), result)
        except (OSError, StateError) as exc:
            result = {'ok': False, 'code': 'result_write_failed', 'message': str(exc)}
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
