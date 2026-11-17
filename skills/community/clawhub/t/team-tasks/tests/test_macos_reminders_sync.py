"""Ledger/native adapter integration using real transactions and isolated state.

The fake client is the only native surface: no test reaches the user's Reminders.
"""
import builtins
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import threading
import copy
import datetime as dt
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import macos_reminders_sync as mod
import task_store as storage
from reminders_state import StateError, read_json, write_json


def task(number=1, **fields):
    result = {'id': 'T-261013-{:03}'.format(number), 'title': '跟进供应商', 'status': 'pending',
              'comments': [], 'priority': 'medium'}
    result.update(fields)
    return result


def native_row(native_id, *, container='L-main', completed=False, body='', **fields):
    result = {'id': native_id, 'containerId': container, 'name': '旧提醒事项', 'body': body,
              'priority': 5, 'flagged': False, 'completed': completed, 'due': {'kind': 'none'},
              'remindMeDate': None, 'completionDate': '2026-10-12T10:00:00+00:00' if completed else None,
              'modificationDate': '2026-10-12T10:00:00+00:00'}
    result.update(fields)
    return result


class FakeRemindersClient:
    """Stateful native API that can mutate and lose a response, like Automation."""
    def __init__(self, rows=None, list_id='L-main'):
        self.list_id = list_id
        self.rows = copy.deepcopy(rows or [])
        self.reads = 0
        self.ensures = 0
        self.applies = []
        self.sequence = 0
        self.tick = 0
        self.fail_after_action = None
        self.before_read = None
        self.before_apply = None

    def snapshot(self):
        return {'listId': self.list_id, 'reminders': copy.deepcopy(self.rows)}

    def read(self):
        self.reads += 1
        if self.before_read:
            action, self.before_read = self.before_read, None
            action()
        return self.snapshot()

    def probe(self):
        return {'listId': self.list_id}

    def ensure_list(self):
        self.ensures += 1
        if self.list_id is None:
            self.list_id = 'L-main'
        return self.snapshot()

    def stamp(self):
        self.tick += 1
        return (dt.datetime(2026, 10, 13, tzinfo=dt.timezone.utc) + dt.timedelta(seconds=self.tick)).isoformat()

    def apply(self, list_id, operations, *, initialization_markers=None):
        self.applies.append(copy.deepcopy(operations))
        if self.before_apply:
            action, self.before_apply = self.before_apply, None
            action()
        if list_id != self.list_id:
            return {'ok': False, 'code': 'macos_native_conflict', 'message': 'list changed'}
        if initialization_markers is not None:
            if any((row.get('body') or '').split('\n')[0] not in initialization_markers
                   for row in mod.target_items(self.snapshot())):
                return {'ok': False, 'code': 'initialization_target_not_empty', 'message': 'unowned content'}
        for operation in operations:
            action = operation['action']
            if action == 'create':
                self.sequence += 1
                item = operation['item']
                row = native_row('R-new-{}'.format(self.sequence), container=self.list_id,
                                 **mod.desired_fields(item))
                row['completionDate'] = self.stamp() if row['completed'] else None
                row['modificationDate'] = self.stamp()
                self.rows.append(row)
            else:
                matches = [row for row in self.rows if row['id'] == operation['id']]
                if not matches:
                    continue
                row = matches[0]
                if operation.get('expectedModified') != row.get('modificationDate'):
                    return {'ok': False, 'code': 'macos_native_conflict', 'message': 'modified'}
                if action == 'delete':
                    self.rows.remove(row)
                elif action == 'update':
                    row.update(mod.desired_fields(operation['item']))
                    if not row['completed']:
                        row['completionDate'] = None
                    row['modificationDate'] = self.stamp()
                else:
                    raise AssertionError('unexpected native operation ' + action)
            if self.fail_after_action == action:
                self.fail_after_action = None
                raise mod.SyncError('macos_sync_timeout', 'native mutation committed, response lost')
        return {'ok': True, 'snapshot': self.snapshot()}

    def reset_calls(self):
        self.reads = self.ensures = 0
        self.applies = []


class PureAdapterTests(unittest.TestCase):
    def test_non_macos_skips_before_ledger_path_state_lock_or_bridge(self):
        for host in ['Linux', 'Windows']:
            with self.subTest(host=host), patch.object(mod.platform, 'system', return_value=host), \
                    patch.object(mod, 'read_snapshot') as store, patch.object(mod, 'Path') as path, \
                    patch.object(mod, 'MirrorState') as state, patch.object(mod, 'adapter_locks') as lock, \
                    patch.object(mod, 'run_bridge') as bridge:
                result = mod.execute('/does/not/exist')
                self.assertEqual(result, {'ok': True, 'code': 'skipped_non_macos', 'action': 'skip', 'platform': host})
                for unused in [store, path, state, lock, bridge]:
                    unused.assert_not_called()

    def test_non_macos_imports_without_posix_storage_support(self):
        original_import = builtins.__import__
        def without_posix(name, *args, **kwargs):
            if name in {'fcntl', 'task_store'}:
                raise AssertionError('POSIX imports must follow the macOS host check')
            return original_import(name, *args, **kwargs)
        spec = importlib.util.spec_from_file_location('sync_without_posix', SCRIPTS / 'macos_reminders_sync.py')
        fresh = importlib.util.module_from_spec(spec)
        with patch.object(builtins, '__import__', side_effect=without_posix):
            spec.loader.exec_module(fresh)
            with patch.object(fresh.platform, 'system', return_value='Windows'):
                self.assertEqual(fresh.execute('/missing')['code'], 'skipped_non_macos')

    def test_deadlines_support_none_all_day_timed_and_validate_before_mutation(self):
        self.assertEqual(mod.due_fields(task(dueDate='2026-10-14')), {'kind': 'allDay', 'date': '2026-10-14'})
        self.assertEqual(mod.due_fields(task(dueDate='2026-10-14', dueTime='09:30')),
                         {'kind': 'timed', 'at': '2026-10-14T09:30:00+08:00'})
        for removed in [None, '', 'none']:
            self.assertEqual(mod.due_fields(task(dueDate=removed, dueTime='09:30')), {'kind': 'none'})
        for fields in [{'dueDate': '2026-02-30'}, {'dueDate': '2026-10-14', 'dueTime': '24:00'},
                       {'dueDate': '14/10/2026'}, {'dueDate': '2026-10-14', 'dueTime': '9:30'}]:
            with self.subTest(fields=fields), self.assertRaises(mod.SyncError):
                mod.due_fields(task(**fields))

    def test_marker_survives_archive_and_path_alias_but_not_other_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            ledgers = {'team-tasks.json': {'tasks': [task()]}}
            first = mod.build_request(ledgers, root)
            moved = {'team-tasks-archive-2026-09.json': {'tasks': [task(title='改标题', status='done')]}}
            second = mod.build_request(moved, root / '..' / root.name)
            self.assertEqual(first['items'][0]['marker'], second['items'][0]['marker'])
            self.assertNotEqual(first['namespace'], mod.build_request(moved, root / 'other')['namespace'])

    def test_bridge_uses_private_json_and_fixed_script_without_code_interpolation(self):
        request = {'listName': mod.LIST_NAME, 'items': [{'name': '"; $(touch /tmp/no) `id`\n中文'}]}
        seen = []
        def run(argv, **options):
            self.assertEqual(argv[:4], ['/usr/bin/osascript', '-l', 'JavaScript', str(mod.BRIDGE)])
            self.assertEqual(len(argv), 5)
            self.assertNotIn(request['items'][0]['name'], argv)
            payload = Path(argv[4])
            self.assertEqual(stat.S_IMODE(payload.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(payload.parent.stat().st_mode), 0o700)
            self.assertEqual(json.loads(payload.read_text()), request)
            self.assertEqual(options, {'capture_output': True, 'text': True, 'timeout': 120, 'check': False})
            seen.append(payload)
            return subprocess.CompletedProcess(argv, 0, '{"ok":true}', '')
        with patch.object(mod.subprocess, 'run', side_effect=run):
            self.assertEqual(mod.run_bridge(request), {'ok': True})
        self.assertFalse(seen[0].exists())

    def test_bridge_error_timeout_and_malformed_success_are_actionable(self):
        for stderr, code in [('Not authorized (-1743)', 'macos_permission_denied'),
                             ('Reminders unavailable', 'macos_bridge_error')]:
            with self.subTest(stderr=stderr), patch.object(mod.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1, '', stderr)):
                with self.assertRaises(mod.SyncError) as caught:
                    mod.run_bridge({})
                self.assertEqual(caught.exception.code, code)
        with patch.object(mod.subprocess, 'run', side_effect=subprocess.TimeoutExpired('osascript', 120)):
            with self.assertRaises(mod.SyncError) as caught:
                mod.run_bridge({})
            self.assertEqual(caught.exception.code, 'macos_sync_timeout')
        for stdout in ['not json', '[]', '{}', '{"ok":1}', '{"ok":"true"}']:
            with self.subTest(stdout=stdout), patch.object(mod.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, stdout, '')):
                with self.assertRaises(mod.SyncError) as caught:
                    mod.run_bridge({})
                self.assertEqual(caught.exception.code, 'macos_bridge_error')


class MirrorIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='team-tasks-native-fake-')
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.home_patch = patch.object(Path, 'home', return_value=self.base / 'home')
        self.home_patch.start()
        self.addCleanup(self.home_patch.stop)
        self.root = self.base / 'ledger'
        self.root.mkdir()
        self.state_root = self.base / 'private-state'
        self.store = storage.TaskStore(self.root)
        self.store.execute({'op': 'init'})
        self.tid = self.create('待处理任务', dueDate='2026-10-14', dueTime='09:30')
        self.native = FakeRemindersClient()
        self.host = patch.object(mod.platform, 'system', return_value='Darwin')
        self.host.start()
        self.addCleanup(self.host.stop)
        self.state = mod.MirrorState(self.root, mod.LIST_NAME, self.state_root)

    def create(self, title, **fields):
        return self.store.execute({'op': 'create', 'actor': 'test', 'fields': dict(title=title, **fields)})['id']

    def execute(self, **options):
        options.setdefault('list_name', mod.LIST_NAME)
        return mod.execute(self.root, state_root=self.state_root, client=self.native, **options)

    def docs(self):
        return self.store.execute({'op': 'read'})['ledgers']

    def task(self, tid=None):
        return next(task for doc in self.docs().values() for task in doc['tasks'] if task['id'] == (tid or self.tid))

    def row(self, tid=None):
        marker = '[team-tasks:v1:{}:{}]'.format(self.state.namespace, tid or self.tid)
        return next(row for row in self.native.rows if (row['body'] or '').split('\n')[0] == marker)

    def status(self, status, tid=None):
        identifier = tid or self.tid
        return self.store.execute({'op': 'status', 'actor': 'test', 'id': identifier,
                                   'status': status, 'expected': {'status': self.task(identifier)['status']}})

    def reopen(self, tid=None):
        identifier = tid or self.tid
        return self.store.execute({'op': 'reopen', 'actor': 'test', 'id': identifier,
                                   'expected': {'status': self.task(identifier)['status']}})

    def initialize(self):
        result = self.execute(initialize=True)
        self.assertTrue(result['ok'], result)
        self.native.reset_calls()
        return result

    def complete_native(self, tid=None, completed_at='2026-10-13T02:00:00+00:00'):
        row = self.row(tid)
        row.update(completed=True, completionDate=completed_at, modificationDate=self.native.stamp())

    def ledger_bytes(self):
        return {path.name: path.read_bytes() for path in self.root.glob('team-tasks*.json')}

    def add_archives(self):
        done, cancelled = self.create('历史完成任务'), self.create('历史取消任务')
        with patch.object(storage, 'now', return_value='2026-09-12T12:00:00+08:00'):
            self.status('done', done)
            self.status('cancelled', cancelled)
        with patch.object(storage, 'now', return_value='2026-10-13T12:00:00+08:00'):
            self.store.execute({'op': 'archive', 'month': '2026-09'})
        return done, cancelled

    def test_dry_run_reads_real_archives_without_native_or_state_writes(self):
        archived = self.add_archives()
        before = self.ledger_bytes()
        with patch.object(mod, 'RemindersClient') as native:
            result = self.execute(dry_run=True)
        self.assertEqual(result['count'], 3)
        self.assertEqual({item['taskId'] for item in result['request']['items']}, {self.tid, *archived})
        self.assertEqual(sum(item['completed'] for item in result['request']['items']), 2)
        self.assertEqual(before, self.ledger_bytes())
        self.assertFalse(self.state_root.exists())
        self.assertEqual(self.native.reads + self.native.ensures, 0)
        native.assert_not_called()

    def test_ordinary_and_scheduled_calls_never_initialize_or_clear_existing_list(self):
        self.native.rows.append(native_row('manual-old'))
        for options in [{}, {'scheduled': True, 'now': dt.datetime(2026, 10, 13, 9, tzinfo=mod.BEIJING)}]:
            result = self.execute(**options)
            self.assertEqual(result['code'], 'initialization_required')
        self.assertEqual(self.native.rows[0]['id'], 'manual-old')
        self.assertEqual(self.native.applies, [])
        self.assertEqual(self.native.reads + self.native.ensures, 0)

    def test_initialize_empty_target_keeps_other_lists_and_includes_archives(self):
        archived = self.add_archives()
        self.native.rows = [native_row('other-list', container='L-other')]
        before = self.ledger_bytes()
        result = self.initialize()
        self.assertEqual(result['code'], 'initialized')
        self.assertEqual(self.native.list_id, 'L-main')
        backup = read_json(Path(result['backup']))
        self.assertEqual(backup['reminders'], [])
        self.assertEqual(backup['kind'], 'script-visible-fields-only')
        self.assertEqual({row['id'] for row in self.native.rows if not row['id'].startswith('R-new-')}, {'other-list'})
        self.assertEqual(len(self.native.rows), 4)
        self.assertFalse(self.row()['completed'])
        self.assertTrue(all(self.row(identifier)['completed'] for identifier in archived))
        self.assertEqual(self.row()['remindMeDate'], '2026-10-14T01:30:00+00:00')
        self.assertEqual(self.state.binding()['phase'], 'complete')
        self.assertEqual(before, self.ledger_bytes())

    def seed_legacy_initialization(self, phase='deleting_old'):
        self.native.rows = [native_row('old-one'), native_row('old-two')]
        backup = {'reminders': copy.deepcopy(self.native.rows)}
        backup_name = 'a' * 32 + '.json'
        write_json(self.root / 'reminders-backups' / backup_name, backup)
        self.state.save_binding({'version': 1, 'listName': mod.LIST_NAME,
            'listId': self.native.list_id, 'namespace': self.state.namespace,
            'dataDir': str(self.root), 'phase': phase, 'oldIds': ['old-one', 'old-two'],
            'backup': backup_name, 'backupHash': hashlib.sha256(mod.json_bytes(backup)).hexdigest()})

    def test_repeated_initialize_never_wipes_post_bootstrap_manual_rows(self):
        self.initialize()
        self.native.rows.append(native_row('later-manual', completed=True))
        before = copy.deepcopy(self.native.rows)
        result = self.execute(initialize=True)
        self.assertEqual(result['code'], 'already_initialized')
        self.assertEqual(self.native.rows, before)
        self.assertEqual(self.native.applies, [])

    def test_missing_list_is_created_once(self):
        self.native.list_id = None
        result = self.execute(initialize=True)
        self.assertTrue(result['ok'])
        self.assertEqual(self.native.ensures, 1)
        self.assertEqual(self.native.list_id, 'L-main')

    def test_snapshot_write_failure_prevents_deletion_and_binding(self):
        before = copy.deepcopy(self.native.rows)
        real_write = mod.write_json
        def refuse_backup(path, value, **options):
            if Path(path).parent.name == 'reminders-backups':
                raise OSError('disk full')
            return real_write(path, value, **options)
        with patch.object(mod, 'write_json', side_effect=refuse_backup):
            with self.assertRaises(OSError):
                self.execute(initialize=True)
        self.assertEqual(self.native.rows, before)
        self.assertEqual(self.native.applies, [])
        self.assertFalse(self.state.binding_path.exists())

    def test_legacy_destructive_initialization_stops_in_every_incomplete_phase(self):
        for phase in ['prepared', 'deleting_old', 'rebuilding', 'verifying']:
            self.seed_legacy_initialization(phase)
            before = self.state.binding_path.read_bytes(), copy.deepcopy(self.native.rows)
            for mode in [{'initialize': True}, {'plan': True}, {}]:
                with self.subTest(phase=phase, mode=mode), self.assertRaises(StateError) as caught:
                    self.execute(**mode)
                self.assertEqual(caught.exception.code, 'state_recovery_required')
            self.assertEqual(before, (self.state.binding_path.read_bytes(), self.native.rows))
            self.assertEqual(self.native.applies, [])

    def test_manual_item_inserted_between_plan_and_apply_is_preserved(self):
        self.native.before_apply = lambda: self.native.rows.append(native_row('inserted-manual'))
        with self.assertRaises(mod.SyncError) as caught:
            self.execute(initialize=True)
        self.assertEqual(caught.exception.code, 'initialization_target_not_empty')
        self.assertEqual([row['id'] for row in self.native.rows], ['inserted-manual'])
        self.assertEqual(self.state.binding()['phase'], 'rebuilding')

    def test_lost_create_response_recovers_markers_without_second_wipe_or_duplicates(self):
        second = self.create('第二任务')
        self.native.fail_after_action = 'create'
        with self.assertRaises(mod.SyncError):
            self.execute(initialize=True)
        self.assertEqual(self.state.binding()['phase'], 'rebuilding')
        preserved = self.native.rows[0]['id']
        self.native.reset_calls()
        result = self.execute(initialize=True)
        self.assertTrue(result['ok'])
        self.assertEqual(len(self.native.rows), 2)
        self.assertIn(preserved, {row['id'] for row in self.native.rows})
        self.assertEqual({self.row()['id'], self.row(second)['id']}, {row['id'] for row in self.native.rows})
        self.assertTrue(all(op['action'] != 'delete' for batch in self.native.applies for op in batch))
        creates = [op for batch in self.native.applies for op in batch if op['action'] == 'create']
        self.assertEqual(len(creates), 1)

    def test_resume_rebuilding_after_old_verification_failure_claims_existing_ids(self):
        all_day = self.create('全天任务', dueDate='2026-10-15')
        no_due = self.create('无截止任务')
        with patch.object(mod, 'different', return_value=['due']):
            with self.assertRaises(mod.SyncError) as caught:
                self.execute(initialize=True)
        self.assertEqual(caught.exception.code, 'macos_verification_failed')
        self.assertEqual(self.state.binding()['phase'], 'rebuilding')
        self.assertEqual(self.state.mapping(self.state.binding())['tasks'], {})
        ids = {row['id'] for row in self.native.rows}
        self.assertEqual(len(ids), 3)
        self.native.reset_calls()
        result = self.execute(initialize=True)
        self.assertEqual(result['code'], 'initialized')
        self.assertEqual(self.native.applies, [])
        self.assertEqual({row['id'] for row in self.native.rows}, ids)
        self.assertEqual(set(self.state.mapping(self.state.binding())['tasks']), {self.tid, all_day, no_due})

    def test_rebuild_preserves_completion_without_saved_baseline(self):
        self.native.fail_after_action = 'create'
        with self.assertRaises(mod.SyncError):
            self.execute(initialize=True)
        self.complete_native()
        rows = copy.deepcopy(self.native.rows)
        self.native.reset_calls()
        preview = self.execute(plan=True)
        self.assertEqual(preview['conflicts'][0]['reason'], 'completion_baseline_missing')
        self.assertEqual(preview['counts']['update'], 0)
        result = self.execute(initialize=True)
        self.assertFalse(result['ok'])
        self.assertEqual(result['conflicts'][0]['reason'], 'completion_baseline_missing')
        self.assertEqual(self.native.rows, rows)
        self.assertEqual(self.native.applies, [])
        self.assertEqual(self.task()['status'], 'pending')
        self.assertEqual(self.state.binding()['phase'], 'rebuilding')
        self.status('done')
        self.assertTrue(self.execute(initialize=True)['ok'])
        self.assertEqual(self.row()['id'], rows[0]['id'])

    def test_rebuild_reuses_saved_completion_baseline_and_reopen_protection(self):
        self.initialize()
        binding = self.state.binding()
        binding['phase'] = 'rebuilding'
        self.state.save_binding(binding)
        self.complete_native()
        self.assertTrue(self.execute(initialize=True)['ok'])
        self.assertEqual(self.task()['status'], 'done')
        self.assertTrue(self.row()['completed'])
        self.reopen()
        binding['phase'] = 'rebuilding'
        self.state.save_binding(binding)
        self.assertTrue(self.execute(initialize=True)['ok'])
        self.assertEqual(self.task()['status'], 'pending')
        self.assertFalse(self.row()['completed'])

    def test_unmarked_item_added_during_rebuild_is_preserved_and_reported(self):
        self.native.fail_after_action = 'create'
        with self.assertRaises(mod.SyncError):
            self.execute(initialize=True)
        self.native.rows.append(native_row('new-manual'))
        self.native.reset_calls()
        with self.assertRaises(mod.SyncError) as caught:
            self.execute(initialize=True)
        self.assertEqual(caught.exception.code, 'macos_native_conflict')
        self.assertIn('new-manual', {row['id'] for row in self.native.rows})
        self.assertEqual(self.native.applies, [])

    def test_duplicate_owned_marker_during_rebuilding_stops_before_further_writes(self):
        self.create('重建中尚未创建的任务')
        self.native.fail_after_action = 'create'
        with self.assertRaises(mod.SyncError):
            self.execute(initialize=True)
        self.assertEqual(self.state.binding()['phase'], 'rebuilding')
        duplicate = copy.deepcopy(self.native.rows[0])
        duplicate.update(id='duplicate-owned-marker', name='重复标记条目有字段漂移')
        self.native.rows.append(duplicate)
        before_rows = copy.deepcopy(self.native.rows)
        before_mapping = self.state.map_path.read_bytes()
        self.native.reset_calls()
        with self.assertRaises(mod.SyncError) as caught:
            self.execute(initialize=True)
        self.assertEqual(caught.exception.code, 'macos_task_conflict')
        self.assertEqual(self.native.applies, [])
        self.assertEqual(self.native.rows, before_rows)
        self.assertEqual(self.state.map_path.read_bytes(), before_mapping)
        self.assertEqual(self.state.binding()['phase'], 'rebuilding')

    def test_missing_map_during_verifying_stops_without_regenerating_mapping(self):
        with patch.object(mod, 'reconcile', side_effect=mod.SyncError('macos_sync_timeout', 'verification interrupted')):
            with self.assertRaises(mod.SyncError):
                self.execute(initialize=True)
        self.assertEqual(self.state.binding()['phase'], 'verifying')
        self.assertTrue(self.state.map_path.exists())
        self.state.map_path.unlink()
        before_rows = copy.deepcopy(self.native.rows)
        before_binding = self.state.binding_path.read_bytes()
        self.native.reset_calls()
        with self.assertRaises(StateError) as caught:
            self.execute(initialize=True)
        self.assertEqual(caught.exception.code, 'state_recovery_required')
        self.assertEqual(self.native.applies, [])
        self.assertEqual(self.native.rows, before_rows)
        self.assertEqual(self.state.binding_path.read_bytes(), before_binding)
        self.assertFalse(self.state.map_path.exists())

    def test_owned_item_moved_out_during_rebuilding_stops_without_creating_duplicate(self):
        self.create('尚未重建的另一任务')
        self.native.fail_after_action = 'create'
        with self.assertRaises(mod.SyncError):
            self.execute(initialize=True)
        self.assertEqual(self.state.binding()['phase'], 'rebuilding')
        self.native.rows[0]['containerId'] = 'L-other'
        before_rows = copy.deepcopy(self.native.rows)
        before_map = self.state.map_path.read_bytes()
        self.native.reset_calls()
        with self.assertRaises(mod.SyncError) as caught:
            self.execute(initialize=True)
        self.assertEqual(caught.exception.code, 'macos_native_conflict')
        self.assertEqual(self.native.applies, [])
        self.assertEqual(self.native.rows, before_rows)
        self.assertEqual(self.state.map_path.read_bytes(), before_map)
        self.assertEqual(self.state.binding()['phase'], 'rebuilding')

    def test_backup_corruption_after_interruption_prevents_more_native_writes(self):
        self.native.fail_after_action = 'create'
        with self.assertRaises(mod.SyncError):
            self.execute(initialize=True)
        backup = self.root / 'reminders-backups' / self.state.binding()['backup']
        value = read_json(backup)
        value['namespace'] = 'tampered'
        write_json(backup, value)
        self.native.reset_calls()
        before = copy.deepcopy(self.native.rows)
        with self.assertRaises(mod.SyncError) as caught:
            self.execute(initialize=True)
        self.assertEqual(caught.exception.code, 'state_recovery_required')
        self.assertEqual(self.native.applies, [])
        self.assertEqual(self.native.rows, before)

    def test_missing_or_corrupt_mapping_never_reinitializes_or_writes_native(self):
        self.initialize()
        saved = self.state.map_path.read_bytes()
        for variant in [None, b'{broken', b'[]']:
            if self.state.map_path.exists():
                self.state.map_path.unlink()
            if variant is not None:
                self.state.map_path.write_bytes(variant)
                self.state.map_path.chmod(0o600)
            for options in [{}, {'initialize': True}]:
                with self.subTest(variant=variant, options=options), self.assertRaises(StateError):
                    self.execute(**options)
            self.assertEqual(self.native.applies, [])
            self.assertEqual(self.native.ensures, 0)
        self.state.map_path.write_bytes(saved)
        self.state.map_path.chmod(0o600)

    def test_changed_data_directory_and_native_list_id_are_binding_conflicts(self):
        self.initialize()
        other = self.base / 'other-ledger'
        other.mkdir()
        storage.TaskStore(other).execute({'op': 'init'})
        with self.assertRaises(StateError) as caught:
            mod.execute(other, state_root=self.state_root, client=self.native, initialize=True, list_name=mod.LIST_NAME)
        self.assertEqual(caught.exception.code, 'binding_conflict')
        self.native.list_id = 'replacement-list'
        with self.assertRaises(mod.SyncError) as caught:
            self.execute()
        self.assertEqual(caught.exception.code, 'binding_conflict')
        self.assertEqual(self.native.applies, [])

    def move_data_directory(self):
        previous = self.root
        self.root = self.base / (self.root.name + '-moved')
        previous.rename(self.root)
        self.store = storage.TaskStore(self.root)
        self.state = mod.MirrorState(self.root, mod.LIST_NAME, self.state_root)
        return str(previous)

    def rebind(self, previous):
        result = self.execute(rebind=True, confirm=self.native.list_id, from_data_dir=previous)
        self.state.binding()
        return result

    def test_relocation_conflict_has_both_paths_and_never_reads_or_writes_native(self):
        self.initialize()
        previous = self.move_data_directory()
        for options in [{}, {'plan': True}, {'initialize': True}, {'dry_run': True}]:
            with self.subTest(options=options), self.assertRaises(StateError) as caught:
                self.execute(**options)
            self.assertEqual(caught.exception.code, 'binding_conflict')
            details = caught.exception.details
            self.assertEqual(details['boundDataDir'], previous)
            self.assertEqual(details['expectedDataDir'], str(self.root))
            self.assertEqual(details['bindingPath'], str(self.state.binding_path))
            self.assertEqual(details['listId'], self.native.list_id)
            self.assertIn(previous, str(caught.exception))
            self.assertIn(str(self.root), str(caught.exception))
        self.assertEqual(self.native.reads, 0)
        self.assertEqual(self.native.applies, [])

    def test_relocation_diagnosis_and_rebind_preview_read_actual_list_without_mutation(self):
        self.initialize()
        self.native.rows.append(native_row('manual'))
        previous = self.move_data_directory()
        before = self.ledger_bytes(), self.state.map_path.read_bytes(), self.state.binding_path.read_bytes()
        diagnosis = self.execute(diagnose=True)
        self.assertEqual(diagnosis['mirror']['error']['code'], 'binding_conflict')
        self.assertEqual(self.native.reads, 0)
        preview = self.execute(rebind=True)
        self.assertEqual(preview['code'], 'rebind_plan')
        self.assertEqual(preview['nativeWrites'], 0)
        self.assertEqual(preview['counts']['unchanged'], 1)
        self.assertEqual(preview['nativeSnapshot']['reminders'], self.native.rows)
        self.assertEqual(before, (self.ledger_bytes(), self.state.map_path.read_bytes(), self.state.binding_path.read_bytes()))
        self.assertFalse((self.state_root / 'rebind-backups').exists())
        self.assertEqual(self.native.applies, [])
        self.assertEqual(self.native.ensures, 0)

    def test_rebind_archives_exact_bytes_preserves_identity_and_is_idempotent(self):
        self.initialize()
        # Deliberately use a different valid JSON representation to test byte preservation.
        binding = self.state.binding()
        raw_binding = json.dumps(binding, ensure_ascii=False).encode() + b'\n\n'
        self.state.binding_path.write_bytes(raw_binding)
        raw_map = self.state.map_path.read_bytes()
        namespace = binding['namespace']
        rows = copy.deepcopy(self.native.rows)
        previous = self.move_data_directory()
        before_ledgers = self.ledger_bytes()
        result = self.rebind(previous)
        self.assertEqual(result['code'], 'rebound')
        archive = Path(result['archive'])
        self.assertEqual((archive / 'binding.json').read_bytes(), raw_binding)
        self.assertEqual((archive / 'reminders-map.json').read_bytes(), raw_map)
        manifest = read_json(archive / 'manifest.json')
        self.assertEqual(manifest['files']['binding.json'], hashlib.sha256(raw_binding).hexdigest())
        self.assertEqual(manifest['files']['reminders-map.json'], hashlib.sha256(raw_map).hexdigest())
        for path in archive.iterdir():
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(archive.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(archive.parent.stat().st_mode), 0o700)
        self.assertEqual(self.ledger_bytes(), before_ledgers)
        self.assertEqual(self.state.map_path.read_bytes(), raw_map)
        self.assertEqual(self.native.rows, rows)
        self.assertEqual(self.native.applies, [])
        self.assertEqual(self.state.binding()['namespaceDir'], previous)
        self.assertEqual(mod.bootstrap_status(self.root, self.state_root)['namespace'], namespace)
        self.assertEqual(self.execute(dry_run=True)['request']['namespace'], namespace)
        self.assertTrue(self.execute(diagnose=True)['ok'])
        self.assertEqual(self.execute(initialize=True)['code'], 'already_initialized')
        for _ in range(2):
            sync = self.execute()
            self.assertTrue(sync['ok'], sync)
            self.assertEqual(sync['counts']['create'], 0)
            self.assertEqual(sync['counts']['update'], 0)
        self.assertEqual(self.native.rows, rows)
        self.assertEqual(self.state.map_path.read_bytes(), raw_map)
        again = self.rebind(str(self.root))
        self.assertEqual(again['code'], 'already_bound')
        self.assertEqual(len(list((self.state_root / 'rebind-backups').iterdir())), 1)
        previous_again = self.move_data_directory()
        self.rebind(previous_again)
        self.assertEqual(self.state.binding()['namespaceDir'], previous)
        self.assertEqual(self.state.namespace, namespace)
        self.assertEqual(self.execute()['counts']['unchanged'], 1)

    def test_rebind_preserves_completion_receipts_detached_state_and_manual_items(self):
        self.initialize()
        other = self.create('将被移除')
        self.execute()
        self.native.rows.remove(self.row(other))
        self.execute()
        self.execute()
        extras = [native_row('manual'), native_row('foreign', body='[team-tasks:v1:foreign:T-other]')]
        self.native.rows.extend(copy.deepcopy(extras))
        previous = self.move_data_directory()
        self.rebind(previous)
        self.native.reset_calls()
        self.complete_native()
        result = self.execute()
        self.assertEqual(result['counts']['writeback'], 1)
        self.assertEqual(result['counts']['create'], 0)
        self.assertEqual(self.task()['status'], 'done')
        comments = copy.deepcopy(self.task()['comments'])
        self.assertEqual(self.execute()['counts']['writeback'], 0)
        self.assertEqual(self.task()['comments'], comments)
        self.assertEqual(read_json(self.state.map_path)['tasks'][other]['state'], 'detached')
        self.assertEqual(self.native.rows[-2:], extras)

    def test_rebind_requires_both_exact_confirmation_fields_before_native_reads(self):
        self.initialize()
        previous = self.move_data_directory()
        before = self.state.binding_path.read_bytes()
        for fields in [{'confirm': 'wrong', 'from_data_dir': previous},
                       {'confirm': self.native.list_id}, {'from_data_dir': previous},
                       {'confirm': self.native.list_id, 'from_data_dir': previous + '/other'}]:
            with self.subTest(fields=fields), self.assertRaises(StateError) as caught:
                self.execute(rebind=True, **fields)
            self.assertEqual(caught.exception.code, 'rebind_confirmation_required')
        self.assertEqual(self.state.binding_path.read_bytes(), before)
        self.assertEqual(self.native.reads, 0)
        self.assertFalse((self.state_root / 'rebind-backups').exists())

    def test_rebind_blocks_missing_mapping_and_replaced_list_without_changing_binding(self):
        self.initialize()
        previous = self.move_data_directory()
        before = self.state.binding_path.read_bytes()
        saved_map = self.state.map_path.read_bytes()
        self.state.map_path.unlink()
        with self.assertRaises(StateError):
            self.rebind(previous)
        self.state.map_path.write_bytes(saved_map)
        self.state.map_path.chmod(0o600)
        self.native.list_id = 'replacement'
        with self.assertRaises(mod.SyncError) as caught:
            self.execute(rebind=True, confirm='L-main', from_data_dir=previous)
        self.assertEqual(caught.exception.code, 'binding_conflict')
        self.assertEqual(self.state.binding_path.read_bytes(), before)
        self.assertEqual(self.native.applies, [])
        self.assertFalse((self.state_root / 'rebind-backups').exists())

    def test_rebind_archive_failure_and_lost_commit_response_are_retryable(self):
        self.initialize()
        previous = self.move_data_directory()
        before = self.state.binding_path.read_bytes()
        with patch.object(mod, 'write_private_bytes', side_effect=OSError('archive failed')):
            with self.assertRaises(OSError):
                self.rebind(previous)
        self.assertEqual(self.state.binding_path.read_bytes(), before)
        save = mod.MirrorState.save_binding
        def commit_then_fail(state, value):
            save(state, value)
            raise OSError('response lost after commit')
        with patch.object(mod.MirrorState, 'save_binding', commit_then_fail):
            with self.assertRaises(OSError):
                self.rebind(previous)
        self.assertEqual(self.state.binding()['dataDir'], str(self.root))
        self.assertEqual(self.rebind(previous)['code'], 'already_bound')
        self.assertEqual(self.execute()['counts']['unchanged'], 1)
        self.assertEqual(self.native.applies, [])

    def test_rebind_interrupted_rebuild_preserves_markers_and_continues_without_wipe(self):
        self.create('第二任务')
        self.native.fail_after_action = 'create'
        with self.assertRaises(mod.SyncError):
            self.execute(initialize=True)
        self.assertEqual(self.state.binding()['phase'], 'rebuilding')
        preserved = {row['id'] for row in self.native.rows}
        previous = self.move_data_directory()
        self.native.reset_calls()
        result = self.rebind(previous)
        self.assertEqual(result['initializationPhase'], 'rebuilding')
        self.assertEqual(self.native.applies, [])
        self.assertTrue((Path(result['archive']) / 'initialization-backup.json').is_file())
        self.assertEqual(self.execute(initialize=True)['code'], 'initialized')
        self.assertEqual(len(self.native.rows), 2)
        self.assertTrue(preserved <= {row['id'] for row in self.native.rows})
        self.assertTrue(all(op['action'] != 'delete' for batch in self.native.applies for op in batch))

    def test_rebind_incomplete_initialization_requires_original_backup(self):
        self.native.fail_after_action = 'create'
        with self.assertRaises(mod.SyncError):
            self.execute(initialize=True)
        binding = self.state.binding()
        previous = self.move_data_directory()
        before = self.state.binding_path.read_bytes()
        (self.root / 'reminders-backups' / binding['backup']).unlink()
        self.native.reset_calls()
        with self.assertRaises(StateError) as caught:
            self.rebind(previous)
        self.assertEqual(caught.exception.code, 'state_recovery_required')
        self.assertEqual(self.state.binding_path.read_bytes(), before)
        self.assertEqual(self.native.reads, 0)
        self.assertEqual(self.native.applies, [])

    def test_rebind_does_not_resume_legacy_destructive_initialization(self):
        self.seed_legacy_initialization()
        previous = self.move_data_directory()
        before = self.state.binding_path.read_bytes()
        with self.assertRaises(StateError) as caught:
            self.rebind(previous)
        self.assertEqual(caught.exception.code, 'state_recovery_required')
        self.assertEqual(self.state.binding_path.read_bytes(), before)
        self.assertEqual(self.native.applies, [])

    def test_real_bridge_requests_use_preserved_namespace_after_rebind(self):
        self.initialize()
        namespace = self.state.namespace
        previous = self.move_data_directory()
        self.rebind(previous)
        with patch.object(mod, 'run_bridge', return_value={'ok': True, 'snapshot': self.native.snapshot()}) as bridge:
            for options in [{'plan': True}, {'diagnose': True, 'native_check': True}, {}]:
                result = mod.execute(self.root, state_root=self.state_root, **options)
                self.assertTrue(result['ok'], result)
        self.assertEqual(len(bridge.call_args_list), 3)
        for call in bridge.call_args_list:
            self.assertIn(call.args[0]['mode'], ('read', 'probe'))
            self.assertEqual(call.args[0]['namespace'], namespace)

    def test_cli_reports_structured_relocation_conflict_and_migration_advice(self):
        self.initialize()
        previous = self.move_data_directory()
        argv = ['sync', '--data-dir', str(self.root), '--state-root', str(self.state_root), '--plan']
        with patch.object(sys, 'argv', argv), patch('sys.stdout', new_callable=io.StringIO) as output:
            self.assertEqual(mod.main(), 1)
        result = json.loads(output.getvalue())
        self.assertEqual(result['boundDataDir'], previous)
        self.assertEqual(result['expectedDataDir'], str(self.root))
        self.assertEqual(result['listId'], self.native.list_id)
        self.assertIn('--rebind', result['recoveryAdvice'])
        self.assertEqual(self.native.reads, 0)
        self.assertEqual(self.native.applies, [])

    def test_normal_sync_preserves_manual_and_other_namespace_items(self):
        self.initialize()
        extras = [native_row('manual-extra'), native_row('different-namespace', body='[team-tasks:v1:other:T-other]')]
        self.native.rows.extend(copy.deepcopy(extras))
        result = self.execute()
        self.assertTrue(result['ok'])
        self.assertEqual(result['counts']['unchanged'], 1)
        self.assertEqual([row for row in self.native.rows if row['id'] in {'manual-extra', 'different-namespace'}], extras)
        self.assertEqual(self.native.applies, [])

    def test_native_drift_is_updated_even_when_cached_ledger_fingerprint_is_unchanged(self):
        self.initialize()
        previous = read_json(self.state.map_path)
        row = self.row()
        row.update(name='手机上改过名称', priority=1, flagged=True, due={'kind': 'none'}, remindMeDate=None)
        row['modificationDate'] = self.native.stamp()
        result = self.execute()
        self.assertTrue(result['ok'])
        self.assertEqual(result['counts']['update'], 1)
        self.assertEqual(self.row()['name'], self.task()['title'])
        self.assertEqual(self.row()['priority'], 5)
        self.assertFalse(self.row()['flagged'])
        self.assertEqual(previous['tasks'][self.tid]['observedFingerprint'], read_json(self.state.map_path)['tasks'][self.tid]['observedFingerprint'])

    def test_plan_shows_native_differences_without_native_or_mapping_writes(self):
        self.initialize()
        self.row()['name'] = 'remote changed'
        before = self.state.map_path.read_bytes()
        ledgers = self.ledger_bytes()
        result = self.execute(plan=True)
        self.assertEqual(result['counts']['update'], 1)
        self.assertIn('name', result['changes'][0]['fields'])
        self.assertEqual(self.native.applies, [])
        self.assertEqual(self.state.map_path.read_bytes(), before)
        self.assertEqual(self.ledger_bytes(), ledgers)

    def test_nonempty_target_is_rejected_without_binding_backup_or_native_writes(self):
        self.native.rows = [native_row('manual'), native_row('completed', completed=True),
                            native_row('child', container='manual'),
                            native_row('foreign', body='[team-tasks:v1:' + 'a' * 64 + ':T-261013-999]'),
                            native_row('other', container='L-other')]
        before = copy.deepcopy(self.native.rows)
        for mode in [{'plan': True}, {'initialize': True}]:
            with self.subTest(mode=mode), self.assertRaises(mod.SyncError) as caught:
                self.execute(**mode)
            self.assertEqual(caught.exception.code, 'initialization_target_not_empty')
            self.assertEqual(self.native.rows, before)
            self.assertFalse(self.state.binding_path.exists())
            self.assertFalse(self.state.map_path.exists())
            self.assertFalse((self.root / 'reminders-backups').exists())
        self.assertEqual(self.native.applies, [])
        self.assertEqual(self.native.ensures, 0)

    def test_plan_of_legacy_destructive_initialization_preserves_evidence(self):
        self.seed_legacy_initialization()
        before = self.state.binding_path.read_bytes(), copy.deepcopy(self.native.rows), self.ledger_bytes()
        with self.assertRaises(StateError) as caught:
            self.execute(plan=True)
        self.assertEqual(caught.exception.code, 'state_recovery_required')
        self.assertEqual(before, (self.state.binding_path.read_bytes(), self.native.rows, self.ledger_bytes()))
        self.assertEqual(self.native.reads, 0)
        self.assertEqual(self.native.applies, [])

    def test_plan_after_lost_create_response_recognizes_created_marker_and_does_not_wipe_it(self):
        self.create('尚未创建的另一任务')
        self.native.fail_after_action = 'create'
        with self.assertRaises(mod.SyncError):
            self.execute(initialize=True)
        self.assertEqual(self.state.binding()['phase'], 'rebuilding')
        self.assertEqual(len(self.native.rows), 1)
        before_rows = copy.deepcopy(self.native.rows)
        before_binding = self.state.binding_path.read_bytes()
        before_mapping = self.state.map_path.read_bytes()
        before_ledgers = self.ledger_bytes()
        self.native.reset_calls()
        for _ in range(2):
            result = self.execute(plan=True)
            self.assertEqual(result['initializationPhase'], 'rebuilding')
            self.assertEqual(result['counts']['removeOld'], 0)
            self.assertEqual(result['counts']['create'], 1)
            self.assertEqual(result['counts']['update'], 0)
            self.assertEqual(result['counts']['unchanged'], 1)
            self.assertEqual(result['counts'].get('writeback', 0), 0)
        self.assertEqual(self.native.applies, [])
        self.assertEqual(self.native.ensures, 0)
        self.assertEqual(self.native.rows, before_rows)
        self.assertEqual(self.state.binding_path.read_bytes(), before_binding)
        self.assertEqual(self.state.map_path.read_bytes(), before_mapping)
        self.assertEqual(self.ledger_bytes(), before_ledgers)

    def test_plan_in_verifying_requires_saved_map_and_leaves_recovery_state_unchanged(self):
        with patch.object(mod, 'reconcile', side_effect=mod.SyncError('macos_sync_timeout', 'verification interrupted')):
            with self.assertRaises(mod.SyncError):
                self.execute(initialize=True)
        self.assertEqual(self.state.binding()['phase'], 'verifying')
        self.state.map_path.unlink()
        before_rows = copy.deepcopy(self.native.rows)
        before_binding = self.state.binding_path.read_bytes()
        before_ledgers = self.ledger_bytes()
        self.native.reset_calls()
        with self.assertRaises(StateError) as caught:
            self.execute(plan=True)
        self.assertEqual(caught.exception.code, 'state_recovery_required')
        self.assertFalse(self.state.map_path.exists())
        self.assertEqual(self.state.binding_path.read_bytes(), before_binding)
        self.assertEqual(self.ledger_bytes(), before_ledgers)
        self.assertEqual(self.native.rows, before_rows)
        self.assertEqual(self.native.applies, [])

    def test_plan_rejects_orphan_mapping_instead_of_proposing_another_wipe(self):
        self.initialize()
        self.state.binding_path.unlink()
        before_rows = copy.deepcopy(self.native.rows)
        before_mapping = self.state.map_path.read_bytes()
        before_ledgers = self.ledger_bytes()
        with self.assertRaises((StateError, mod.SyncError)) as caught:
            self.execute(plan=True)
        self.assertEqual(caught.exception.code, 'state_recovery_required')
        self.assertFalse(self.state.binding_path.exists())
        self.assertEqual(self.state.map_path.read_bytes(), before_mapping)
        self.assertEqual(self.native.rows, before_rows)
        self.assertEqual(self.ledger_bytes(), before_ledgers)
        self.assertEqual(self.native.applies, [])

    def test_native_completion_commits_status_source_comment_and_outbox_once(self):
        self.initialize()
        before = self.docs()[storage.MAIN]['_reminderSyncEvents']
        self.complete_native()
        result = self.execute()
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['counts']['writeback'], 1)
        completed = self.task()
        self.assertEqual(completed['status'], 'done')
        self.assertNotEqual(completed['completedAt'], '2026-10-13T02:00:00+00:00')
        self.assertEqual(len(completed['comments']), 1)
        self.assertIn('2026-10-13T02:00:00+00:00', completed['comments'][0]['content'])
        events = self.docs()[storage.MAIN]['_reminderSyncEvents']
        self.assertEqual(events[:len(before)], before)
        self.assertEqual([event['action'] for event in events[len(before):]], ['status', 'comment'])
        raw = self.ledger_bytes()
        again = self.execute()
        self.assertTrue(again['ok'])
        self.assertEqual(again['counts']['writeback'], 0)
        self.assertEqual(raw, self.ledger_bytes())

    def test_writeback_committed_but_native_response_lost_does_not_duplicate_comment(self):
        self.initialize()
        self.complete_native()
        self.native.fail_after_action = 'update'
        with self.assertRaises(mod.SyncError):
            self.execute()
        self.assertEqual(self.task()['status'], 'done')
        before = self.ledger_bytes()
        self.native.reset_calls()
        result = self.execute()
        self.assertTrue(result['ok'])
        self.assertEqual(before, self.ledger_bytes())
        self.assertEqual(len(self.task()['comments']), 1)
        self.assertEqual(self.native.applies, [])

    def test_completion_transaction_response_lost_retries_without_duplicate_status_or_comment(self):
        self.initialize()
        self.complete_native()
        actual_execute = storage.TaskStore.execute
        def lost_completion_response(store, request):
            result = actual_execute(store, request)
            if request.get('op') == 'complete_external':
                raise mod.SyncError('macos_sync_timeout', 'completion committed, response lost')
            return result
        with patch.object(storage.TaskStore, 'execute', lost_completion_response):
            with self.assertRaises(mod.SyncError):
                self.execute()
        committed = self.ledger_bytes()
        self.assertEqual(self.task()['status'], 'done')
        self.assertEqual(len(self.task()['comments']), 1)
        result = self.execute()
        self.assertTrue(result['ok'])
        self.assertEqual(result['counts']['writeback'], 0)
        self.assertEqual(self.ledger_bytes(), committed)

    def test_missing_completion_time_and_missing_baseline_stop_safely(self):
        self.initialize()
        self.complete_native(completed_at=None)
        result = self.execute()
        self.assertFalse(result['ok'])
        self.assertEqual(result['conflicts'][0]['reason'], 'completion_time_missing')
        self.assertEqual(self.task()['status'], 'pending')
        self.assertEqual(self.native.applies, [])
        mapping = read_json(self.state.map_path)
        mapping['tasks'][self.tid]['pendingFingerprint'] = None
        write_json(self.state.map_path, mapping)
        self.row()['completionDate'] = '2026-10-13T02:00:00+00:00'
        with self.assertRaises(StateError) as caught:
            self.execute()
        self.assertEqual(caught.exception.code, 'state_recovery_required')
        self.assertEqual(self.task()['status'], 'pending')

    def test_reopened_ledger_overrides_old_completed_native_state(self):
        self.initialize()
        self.complete_native()
        self.status('done')
        self.reopen()
        result = self.execute()
        self.assertTrue(result['ok'])
        self.assertEqual(result['counts']['writeback'], 0)
        self.assertEqual(self.task()['status'], 'pending')
        self.assertFalse(self.row()['completed'])
        self.assertEqual(self.task()['comments'], [])

    def test_concurrent_reopen_conflict_never_advances_pending_baseline_to_stale_completion(self):
        self.initialize()
        self.complete_native()
        def concurrently_reopen():
            self.status('done')
            self.reopen()
        self.native.before_read = concurrently_reopen
        first = self.execute()
        self.assertFalse(first['ok'])
        self.assertEqual(first['conflicts'][0]['reason'], 'ledger_conflict')
        self.assertEqual(self.task()['status'], 'pending')
        self.assertTrue(self.row()['completed'])
        second = self.execute()
        self.assertTrue(second['ok'], second)
        self.assertEqual(second['counts']['writeback'], 0)
        self.assertEqual(self.task()['status'], 'pending')
        self.assertFalse(self.row()['completed'])
        self.assertEqual(self.task()['comments'], [])

    def test_cancelled_completion_and_uncheck_do_not_reopen_ledger(self):
        self.status('cancelled')
        self.initialize()
        self.row().update(completed=False, completionDate=None, modificationDate=self.native.stamp())
        result = self.execute()
        self.assertTrue(result['ok'])
        self.assertEqual(self.task()['status'], 'cancelled')
        self.assertTrue(self.row()['completed'])
        self.assertEqual(result['counts']['writeback'], 0)

    def test_terminal_deletion_is_detached_and_never_rebuilt(self):
        self.status('done')
        self.initialize()
        self.native.rows.remove(self.row())
        for _ in range(3):
            result = self.execute()
            self.assertTrue(result['ok'])
            self.assertEqual(result['counts']['create'], 0)
        self.assertEqual(self.native.rows, [])
        entry = read_json(self.state.map_path)['tasks'][self.tid]
        self.assertEqual(entry['state'], 'detached')
        self.assertEqual(entry['reason'], 'removed')

    def test_pending_deletion_needs_two_observations_and_plan_does_not_increment(self):
        self.initialize()
        self.native.rows.remove(self.row())
        before = self.state.map_path.read_bytes()
        for _ in range(3):
            preview = self.execute(plan=True)
            self.assertEqual(preview['counts']['missing'], 1)
        self.assertEqual(self.state.map_path.read_bytes(), before)
        first = self.execute()
        self.assertEqual(first['counts']['missing'], 1)
        self.assertEqual(read_json(self.state.map_path)['tasks'][self.tid]['missing'], 1)
        second = self.execute()
        self.assertEqual(second['counts']['detached'], 1)
        self.assertEqual(read_json(self.state.map_path)['tasks'][self.tid]['state'], 'detached')
        self.assertEqual(self.native.applies, [])
        self.assertEqual(self.native.rows, [])

    def test_failed_native_read_does_not_count_as_missing_observation(self):
        self.initialize()
        self.native.rows.remove(self.row())
        before = self.state.map_path.read_bytes()
        def permission_failure():
            raise mod.SyncError('macos_permission_denied', 'permission lost')
        self.native.before_read = permission_failure
        with self.assertRaises(mod.SyncError) as caught:
            self.execute()
        self.assertEqual(caught.exception.code, 'macos_permission_denied')
        self.assertEqual(self.state.map_path.read_bytes(), before)
        result = self.execute()
        self.assertEqual(result['counts']['missing'], 1)
        self.assertEqual(read_json(self.state.map_path)['tasks'][self.tid]['missing'], 1)

    def test_explicit_reopen_restores_detached_pending_item(self):
        self.initialize()
        self.native.rows.remove(self.row())
        self.execute()
        self.execute()
        self.assertEqual(read_json(self.state.map_path)['tasks'][self.tid]['state'], 'detached')
        self.reopen()
        result = self.execute()
        self.assertTrue(result['ok'])
        self.assertEqual(result['counts']['create'], 1)
        self.assertFalse(self.row()['completed'])

    def test_explicit_reopen_recreates_deleted_terminal_item(self):
        self.status('done')
        self.initialize()
        original_id = self.row()['id']
        self.native.rows.remove(self.row())
        self.execute()
        self.reopen()
        result = self.execute()
        self.assertTrue(result['ok'])
        self.assertEqual(result['counts']['create'], 1)
        self.assertNotEqual(self.row()['id'], original_id)
        self.assertFalse(self.row()['completed'])

    def test_moved_item_is_detached_without_duplicate_and_can_be_moved_back(self):
        self.initialize()
        original_id = self.row()['id']
        self.row()['containerId'] = 'L-other'
        first = self.execute()
        self.assertEqual(first['counts']['detached'], 1)
        self.assertEqual(len(self.native.rows), 1)
        self.assertEqual(self.native.applies, [])
        self.status('done')
        self.reopen()
        second = self.execute()
        self.assertEqual(second['counts']['create'], 0)
        self.assertEqual(self.native.applies, [])
        self.row()['containerId'] = self.native.list_id
        third = self.execute()
        self.assertTrue(third['ok'])
        self.assertEqual(third['counts']['create'], 0)
        self.assertEqual(self.row()['id'], original_id)
        self.assertEqual(read_json(self.state.map_path)['tasks'][self.tid]['state'], 'mirrored')

    def test_unbaselined_moved_completed_item_remains_conflict_after_return(self):
        self.initialize()
        unbaselined = self.create('尚未建立同步基线的任务')
        request = mod.build_request(self.docs(), self.root)
        item = next(entry for entry in request['items'] if entry['taskId'] == unbaselined)
        remote = native_row('unbaselined-moved', container='L-other', **mod.desired_fields(item))
        remote.update(completed=True, completionDate='2026-10-13T02:00:00+00:00')
        self.native.rows.append(remote)
        first = self.execute()
        self.assertTrue(first['ok'])
        self.assertEqual(first['counts']['detached'], 1)
        entry = read_json(self.state.map_path)['tasks'][unbaselined]
        self.assertEqual(entry['reason'], 'moved')
        self.assertIsNone(entry.get('observedFingerprint'))
        self.assertIsNone(entry.get('pendingFingerprint'))
        self.assertEqual(self.native.applies, [])
        self.row(unbaselined)['containerId'] = self.native.list_id
        before_map = self.state.map_path.read_bytes()
        before_ledgers = self.ledger_bytes()
        for _ in range(2):
            result = self.execute()
            self.assertFalse(result['ok'])
            self.assertEqual(result['conflicts'], [{'taskId': unbaselined, 'reason': 'completion_baseline_missing'}])
            self.assertEqual(result['counts']['create'], 0)
            self.assertEqual(result['counts']['writeback'], 0)
        self.assertEqual(self.native.applies, [])
        self.assertEqual(self.ledger_bytes(), before_ledgers)
        self.assertEqual(self.state.map_path.read_bytes(), before_map)
        self.assertEqual(self.task(unbaselined)['status'], 'pending')
        self.assertTrue(self.row(unbaselined)['completed'])
        self.assertEqual(len([row for row in self.native.rows if row['id'] == 'unbaselined-moved']), 1)

    def test_archive_move_preserves_native_id_and_does_not_detach_source(self):
        self.initialize()
        with patch.object(storage, 'now', return_value='2026-09-12T12:00:00+08:00'):
            self.status('done')
        self.execute()
        original_id = self.row()['id']
        with patch.object(storage, 'now', return_value='2026-10-13T12:00:00+08:00'):
            self.store.execute({'op': 'archive', 'month': '2026-09'})
        self.native.reset_calls()
        result = self.execute()
        self.assertTrue(result['ok'])
        self.assertEqual(result['counts']['unchanged'], 1)
        self.assertEqual(result['counts']['create'], 0)
        self.assertEqual(self.row()['id'], original_id)
        self.assertEqual(read_json(self.state.map_path)['tasks'][self.tid]['state'], 'terminal')

    def test_duplicate_marker_and_changed_owned_marker_stop_without_updates(self):
        self.initialize()
        duplicate = copy.deepcopy(self.row())
        duplicate['id'] = 'duplicate'
        self.native.rows.append(duplicate)
        with self.assertRaises(mod.SyncError) as caught:
            self.execute()
        self.assertEqual(caught.exception.code, 'macos_task_conflict')
        self.native.rows.remove(duplicate)
        self.row()['body'] = 'user removed marker'
        result = self.execute()
        self.assertFalse(result['ok'])
        self.assertEqual(result['conflicts'][0]['reason'], 'marker_changed')
        self.assertEqual(self.native.applies, [])

    def test_scheduled_outside_slot_skips_before_paths_ledger_state_and_native(self):
        with patch.object(mod, 'Path') as path, patch.object(mod, 'read_snapshot') as read, \
                patch.object(mod, 'MirrorState') as state, patch.object(mod, 'RemindersClient') as client:
            result = mod.execute('/missing', scheduled=True, now=dt.datetime(2026, 10, 13, 9, 1, tzinfo=mod.BEIJING))
        self.assertEqual(result['code'], 'outside_schedule')
        for unused in [path, read, state, client]:
            unused.assert_not_called()

    def test_successful_scheduled_slot_is_deduplicated_before_store_and_native_reads(self):
        self.initialize()
        stamp = dt.datetime(2026, 10, 13, 9, tzinfo=mod.BEIJING)
        self.assertTrue(self.execute(scheduled=True, now=stamp)['ok'])
        self.assertEqual(read_json(self.state.map_path)['lastSuccessfulSlot'], '2026-10-13T09:00+08:00')
        self.native.reset_calls()
        with patch.object(mod, 'read_snapshot') as source:
            again = self.execute(scheduled=True, now=stamp + dt.timedelta(seconds=58))
        self.assertEqual(again['code'], 'duplicate_slot')
        self.assertEqual(self.native.reads, 0)
        self.assertEqual(self.native.applies, [])
        source.assert_not_called()

    def test_busy_scheduled_execution_skips_without_native_or_ledger_reads(self):
        self.initialize()
        with mod.sync_lock(self.root), patch.object(mod, 'read_snapshot') as source:
            result = self.execute(scheduled=True, now=dt.datetime(2026, 10, 13, 9, tzinfo=mod.BEIJING))
        self.assertEqual(result['code'], 'busy')
        self.assertTrue(result['ok'])
        self.assertEqual(self.native.reads, 0)
        self.assertEqual(self.native.applies, [])
        source.assert_not_called()

    def test_diagnose_is_read_only_and_checks_actual_bound_list(self):
        first = self.execute(diagnose=True, native_check=True)
        self.assertFalse(first['ok'])
        self.assertEqual(first['code'], 'initialization_required')
        self.initialize()
        before = self.ledger_bytes(), self.state.map_path.read_bytes(), self.state.binding_path.read_bytes()
        result = self.execute(diagnose=True, native_check=True)
        self.assertTrue(result['ok'])
        self.assertTrue(result['initialized'])
        self.assertEqual(result['requestMode'], 'diagnose')
        self.assertEqual(before, (self.ledger_bytes(), self.state.map_path.read_bytes(), self.state.binding_path.read_bytes()))
        self.assertEqual(self.native.applies, [])

    def test_cli_diagnostic_private_result_echoes_probe_token(self):
        result_path = self.base / 'probe-result.json'
        argv = ['sync', '--data-dir', str(self.root), '--state-root', str(self.state_root),
                '--diagnose', '--native-check', '--result-file', str(result_path), '--probe-token', 'unique-token']
        with patch.object(sys, 'argv', argv), patch.object(mod, 'execute', return_value={'ok': True, 'code': 'ok', 'initialized': True}), \
                patch('sys.stdout', io.StringIO()):
            self.assertEqual(mod.main(), 0)
        result = read_json(result_path)
        self.assertEqual(result['probeToken'], 'unique-token')
        self.assertEqual(result['requestMode'], 'diagnose')
        self.assertEqual(stat.S_IMODE(result_path.stat().st_mode), 0o600)


    def test_fresh_mirror_requires_name_without_native_access_or_state_writes(self):
        for mode in [{}, {'initialize': True}, {'plan': True}, {'dry_run': True}]:
            with self.subTest(mode=mode), self.assertRaises(StateError) as caught:
                self.execute(list_name=None, **mode)
            self.assertEqual(caught.exception.code, 'list_name_required')
        self.assertEqual(self.native.reads + self.native.ensures, 0)
        self.assertFalse(self.state.binding_dir.exists())
        self.assertFalse(self.state.map_path.exists())
        self.assertEqual(self.task()['status'], 'pending')

    def test_invalid_list_names_stop_before_native_or_state_changes(self):
        for name in ['', '   ', 'line\nbreak', 'nul\x00name', 'tab\tname', 'del\x7fname']:
            with self.subTest(name=name), self.assertRaises(StateError) as caught:
                self.execute(list_name=name, initialize=True)
            self.assertEqual(caught.exception.code, 'invalid_list_name')
        self.assertEqual(self.native.reads + self.native.ensures, 0)
        self.assertFalse(self.state.binding_dir.exists())

    def test_custom_name_is_remembered_and_old_style_calls_reuse_it(self):
        name = '团队待办 · 项目甲 "中文"'
        preview = self.execute(list_name=name, dry_run=True)
        self.assertEqual(preview['request']['listName'], name)
        self.assertTrue(self.execute(list_name=name, initialize=True)['ok'])
        self.native.reset_calls()
        for mode in [{}, {'plan': True}, {'diagnose': True}, {'dry_run': True}]:
            result = self.execute(list_name=None, **mode)
            self.assertTrue(result['ok'], result)
        state = mod.MirrorState(self.root, state_root=self.state_root)
        self.assertEqual(state.list_name, name)
        self.assertEqual(state.binding()['listId'], self.native.list_id)
        self.assertEqual(self.native.applies, [])
        with patch.object(mod, 'run_bridge', return_value={'ok': True, 'snapshot': self.native.snapshot()}) as bridge:
            self.assertTrue(mod.execute(self.root, state_root=self.state_root, plan=True)['ok'])
        self.assertEqual(bridge.call_args.args[0]['listName'], name)

    def test_two_ledgers_with_same_task_id_sync_and_complete_independently(self):
        self.initialize()
        other = self.base / 'second-ledger'
        other.mkdir()
        second_store = storage.TaskStore(other)
        second_store.execute({'op': 'init'})
        with patch.object(storage, 'now', return_value=self.task()['createdAt']):
            other_tid = second_store.execute({'op': 'create', 'actor': 'test', 'fields': {'title': '独立事项'}})['id']
        self.assertEqual(other_tid, self.tid)
        second_native = FakeRemindersClient(list_id='L-second')
        second_state = self.base / 'second-state'
        self.assertTrue(mod.execute(other, state_root=second_state, list_name='项目乙',
                                    client=second_native, initialize=True)['ok'])
        self.assertNotEqual(self.row()['body'].split('\n')[0], second_native.rows[0]['body'].split('\n')[0])
        second_bytes = (other / 'team-tasks.json').read_bytes()
        second_rows = copy.deepcopy(second_native.rows)
        self.complete_native()
        self.assertEqual(self.execute()['counts']['writeback'], 1)
        self.assertEqual(self.task()['status'], 'done')
        self.assertEqual((other / 'team-tasks.json').read_bytes(), second_bytes)
        self.assertEqual(second_native.rows, second_rows)
        self.assertTrue(mod.execute(other, state_root=self.base / 'third-state', client=second_native)['ok'])

    def test_other_state_root_cannot_claim_occupied_empty_ledger_list(self):
        empty = self.base / 'empty-ledger'
        empty.mkdir()
        storage.TaskStore(empty).execute({'op': 'init'})
        native = FakeRemindersClient(list_id='L-empty')
        self.assertTrue(mod.execute(empty, state_root=self.base / 'isolated-state', list_name='空台账',
                                    client=native, initialize=True)['ok'])
        self.assertEqual(native.rows, [])
        with self.assertRaises(StateError) as caught:
            self.execute(list_name='空台账', initialize=True)
        self.assertEqual(caught.exception.code, 'binding_conflict')
        self.assertEqual(caught.exception.details['boundDataDir'], str(empty))
        self.assertEqual(self.native.reads + self.native.ensures, 0)

    def test_same_ledger_cannot_bind_second_list_even_before_map_is_created(self):
        self.initialize()
        binding = self.state.binding()
        binding['phase'] = 'prepared'
        self.state.save_binding(binding)
        self.state.map_path.unlink()
        before = self.state.binding_path.read_bytes()
        with self.assertRaises(StateError) as caught:
            self.execute(list_name='另一个列表', initialize=True)
        self.assertEqual(caught.exception.code, 'binding_conflict')
        self.assertEqual(caught.exception.details['listName'], mod.LIST_NAME)
        self.assertEqual(caught.exception.details['bindingPath'], str(self.state.binding_path))
        self.assertEqual(self.state.binding_path.read_bytes(), before)
        self.assertEqual(self.native.reads + self.native.ensures, 0)

    def test_renamed_empty_list_cannot_be_claimed_by_another_ledger(self):
        empty = self.base / 'empty-owner'
        empty.mkdir()
        storage.TaskStore(empty).execute({'op': 'init'})
        self.assertTrue(mod.execute(empty, list_name='原名称', client=self.native, initialize=True)['ok'])
        owner = mod.MirrorState(empty)
        original = owner.binding_path.read_bytes()
        for options in ({'plan': True}, {'initialize': True}):
            with self.assertRaises(StateError) as caught:
                self.execute(list_name='重命名后', **options)
            self.assertEqual(caught.exception.code, 'binding_conflict')
        self.assertEqual(owner.binding_path.read_bytes(), original)
        self.assertEqual(len(list(owner.binding_dir.glob('*.json'))), 1)
        self.assertFalse((self.root / 'reminders-backups').exists())
        self.assertEqual(self.native.applies, [])

    def test_concurrent_names_cannot_commit_the_same_native_identity(self):
        other = self.base / 'competing-native-id'
        other.mkdir()
        storage.TaskStore(other).execute({'op': 'init'})
        barrier = threading.Barrier(2)
        actual_save = mod.MirrorState.save_binding
        def competing_save(state, value):
            if value['phase'] == 'prepared':
                barrier.wait(timeout=5)
            return actual_save(state, value)
        clients = [FakeRemindersClient(), FakeRemindersClient()]
        def run(index):
            try:
                return mod.execute([self.root, other][index], list_name='名称' + str(index),
                    state_root=self.base / ('state-' + str(index)), client=clients[index], initialize=True)['code']
            except StateError as exc:
                return exc.code
        with patch.object(mod.MirrorState, 'save_binding', competing_save), ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(run, [0, 1]))
        self.assertCountEqual(results, ['initialized', 'binding_conflict'])
        self.assertEqual(clients[results.index('binding_conflict')].applies, [])
        self.assertEqual(len(list(self.state.binding_dir.glob('*.json'))), 1)
        winner = mod.MirrorState([self.root, other][results.index('initialized')])
        self.assertEqual(winner.binding()['phase'], 'complete')

    def run_competing_initializations(self, same_ledger):
        other = self.root if same_ledger else self.base / 'competing-ledger'
        if not same_ledger:
            other.mkdir()
            storage.TaskStore(other).execute({'op': 'init'})
        barrier = threading.Barrier(2)
        actual_locks = mod.adapter_locks
        @contextmanager
        def competing_locks(state, scheduled=False):
            barrier.wait(timeout=5)
            with actual_locks(state, scheduled):
                yield
        clients = [FakeRemindersClient(list_id='L-first'),
                   FakeRemindersClient(list_id='L-second' if same_ledger else 'L-first')]
        def run(index):
            try:
                result = mod.execute([self.root, other][index],
                    state_root=self.base / ('state-' + str(index)),
                    list_name=['项目甲', '项目乙' if same_ledger else '项目甲'][index],
                    client=clients[index], initialize=True)
                return result['code']
            except StateError as exc:
                return exc.code
        with patch.object(mod, 'adapter_locks', competing_locks), ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(run, [0, 1]))
        self.assertCountEqual(results, ['initialized', 'binding_conflict'])
        loser = clients[results.index('binding_conflict')]
        self.assertEqual(loser.reads + loser.ensures, 0)
        self.assertEqual(loser.applies, [])
        self.assertEqual(len(list(self.state.binding_dir.glob('*.json'))), 1)

    def test_concurrent_two_names_for_same_ledger_are_serialized(self):
        self.run_competing_initializations(same_ledger=True)

    def test_concurrent_two_state_roots_cannot_claim_same_list(self):
        self.run_competing_initializations(same_ledger=False)

    def move_binding_to_legacy_state(self):
        self.initialize()
        raw = self.state.binding_path.read_bytes()
        mod.write_private_bytes(self.state.legacy_binding_path, raw, exclusive=True)
        self.state.binding_path.unlink()
        return raw

    def test_legacy_custom_state_is_read_without_migration_then_imported_on_write(self):
        raw = self.move_binding_to_legacy_state()
        original_map = self.state.map_path.read_bytes()
        self.assertTrue(self.execute(list_name=None, plan=True)['ok'])
        self.assertFalse(self.state.binding_path.exists())
        self.assertEqual(self.state.legacy_binding_path.read_bytes(), raw)
        self.assertFalse((self.state.binding_dir.parent / 'binding-migration-backups').exists())
        self.assertTrue(self.execute(list_name=None)['ok'])
        binding = read_json(self.state.binding_path)
        evidence = binding['legacyImports'][str(self.state.legacy_binding_path)]
        self.assertEqual(evidence['sha256'], hashlib.sha256(raw).hexdigest())
        self.assertEqual((Path(evidence['archive']) / 'binding.json').read_bytes(), raw)
        self.assertEqual(self.state.legacy_binding_path.read_bytes(), raw)
        self.assertEqual(self.state.map_path.read_bytes(), original_map)
        self.assertEqual(self.native.applies, [])
        self.assertTrue(mod.execute(self.root, state_root=self.base / 'new-helper-root', client=self.native)['ok'])
        self.assertEqual(len(list((self.state.binding_dir.parent / 'binding-migration-backups').iterdir())), 1)

    def test_migration_failure_and_lost_response_preserve_retryable_state(self):
        raw = self.move_binding_to_legacy_state()
        with patch('reminders_state.write_private_bytes', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                self.execute()
        self.assertFalse(self.state.binding_path.exists())
        self.assertEqual(self.state.legacy_binding_path.read_bytes(), raw)
        save = mod.MirrorState.save_binding
        def lost_response(state, binding):
            save(state, binding)
            raise OSError('lost response after registry commit')
        with patch.object(mod.MirrorState, 'save_binding', lost_response):
            with self.assertRaises(OSError):
                self.execute()
        self.assertTrue(self.execute()['ok'])
        self.assertEqual(self.native.applies, [])
        self.assertEqual(self.state.legacy_binding_path.read_bytes(), raw)

    def test_corrupt_mapping_blocks_legacy_import(self):
        self.move_binding_to_legacy_state()
        self.state.map_path.write_bytes(b'{broken')
        with self.assertRaises(StateError):
            self.execute()
        self.assertFalse(self.state.binding_path.exists())
        self.assertEqual(self.native.applies, [])

    def test_old_installation_writing_imported_binding_is_detected_from_other_root(self):
        self.move_binding_to_legacy_state()
        self.assertTrue(self.execute()['ok'])
        value = read_json(self.state.legacy_binding_path)
        value['phase'] = 'verifying'
        write_json(self.state.legacy_binding_path, value)
        self.native.reset_calls()
        with self.assertRaises(StateError) as caught:
            mod.execute(self.root, state_root=self.base / 'unrelated-root', client=self.native)
        self.assertEqual(caught.exception.code, 'binding_conflict')
        self.assertEqual(self.native.reads + self.native.ensures, 0)

    def test_imported_legacy_binding_can_be_relocated_without_changing_identity(self):
        self.move_binding_to_legacy_state()
        previous = self.move_data_directory()
        result = self.rebind(previous)
        self.assertEqual(result['code'], 'rebound')
        self.assertEqual(self.state.binding()['namespaceDir'], previous)
        self.assertTrue(self.execute(list_name=None)['ok'])
        self.assertEqual(self.native.applies, [])

    def test_multiple_or_corrupt_bindings_do_not_fall_back_to_unconfigured(self):
        self.initialize()
        binding = self.state.binding()
        duplicate = dict(binding, listName='重复绑定', listId='L-another')
        duplicate_path = self.state.binding_dir / (hashlib.sha256('重复绑定'.encode()).hexdigest() + '.json')
        write_json(duplicate_path, duplicate)
        with self.assertRaises(StateError) as caught:
            self.execute(list_name=None)
        self.assertEqual(caught.exception.code, 'binding_conflict')
        duplicate_path.unlink()
        self.state.binding_path.write_bytes(b'{invalid')
        with self.assertRaises(StateError) as caught:
            self.execute(list_name=None)
        self.assertEqual(caught.exception.code, 'state_recovery_required')
        self.assertEqual(self.native.reads + self.native.ensures, 0)


if __name__ == '__main__':
    unittest.main()
