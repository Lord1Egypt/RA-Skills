import datetime as dt
import io
import fcntl
import time
import subprocess
import os
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import macos_sync_status as status
import macos_reminders_sync as sync
from task_store import TaskStore
from reminders_state import StateError


class SyncStatusTests(unittest.TestCase):
    def test_next_slot_after_current_minute_and_overnight(self):
        for current, expected in [('2026-10-13T09:00:00+08:00', '2026-10-13T09:10+08:00'),
                                  ('2026-10-13T21:59:59+08:00', '2026-10-13T22:00+08:00'),
                                  ('2026-10-13T22:00:00+08:00', '2026-10-14T07:00+08:00')]:
            self.assertEqual(status.next_slot(dt.datetime.fromisoformat(current)), expected)

    def test_status_does_not_read_or_recover_ledger_or_call_native(self):
        with tempfile.TemporaryDirectory() as root:
            directory = Path(root)
            # A pending transaction must remain untouched by a status query.
            (directory / '.task-store-transaction.json').write_text('pending transaction')
            before = {p.name: p.read_bytes() for p in directory.iterdir()}
            with patch.object(status.NativeSchedule, 'status', return_value={
                    'enabled': False, 'lastSync': None}), \
                    patch.object(sync, 'run_bridge', side_effect=AssertionError('native read forbidden')), \
                    patch.object(sync, 'read_snapshot', side_effect=AssertionError('ledger recovery forbidden')):
                result = status.sync_status(root, str(directory / 'missing-state'),
                                           bootstrap=sync.bootstrap_status)
            self.assertFalse(result['mirror']['initialized'])
            self.assertFalse(result['currentSyncVerified'])
            self.assertIsNone(result['nextSyncAt'])
            self.assertEqual(before, {p.name: p.read_bytes() for p in directory.iterdir()})

    def test_history_never_proves_current_sync_and_legacy_time_is_unknown(self):
        for last in [{'ok': True}, {'ok': False, 'code': 'macos_sync_timeout',
                                     'finishedAt': '2026-10-13T11:00:00+00:00'}]:
            with patch.object(status, 'NativeSchedule') as factory:
                factory.return_value.status.return_value = {'enabled': True, 'lastSync': last}
                result = status.sync_status('/unused', bootstrap=lambda *a: {'initialized': True})
            self.assertFalse(result['currentSyncVerified'])
            self.assertEqual(result['lastSyncAt'], last.get('finishedAt'))
            self.assertEqual(result['lastSyncFailed'], last['ok'] is False)
            if last['ok'] is False:
                self.assertIn('上次同步失败', result['message'])
            self.assertIsNotNone(result['nextSyncAt'])

    def test_broken_binding_never_promises_automatic_sync(self):
        with patch.object(status, 'NativeSchedule') as factory:
            factory.return_value.status.return_value = {'enabled': True}
            def broken(*args):
                raise StateError('state_recovery_required', 'broken mapping')
            result = status.sync_status('/unused', bootstrap=broken)
        self.assertIsNone(result['nextSyncAt'])
        self.assertIn('不会自动更新', result['message'])

    def test_cli_status_never_executes_sync_and_forbids_result_writes(self):
        args = ['sync', '--data-dir', '/unused', '--sync-status']
        with patch.object(sys, 'argv', args), patch.object(status, 'sync_status', return_value={
                'ok': True, 'code': 'sync_status'}), patch.object(sync, 'execute') as execute, \
                patch.object(sys, 'stdout', new_callable=io.StringIO) as output:
            self.assertEqual(sync.main(), 0)
            execute.assert_not_called()
            self.assertNotIn('finishedAt', json.loads(output.getvalue()))
        with patch.object(sys, 'argv', args + ['--result-file', '/unused']), \
                patch.object(sys, 'stderr', new_callable=io.StringIO), patch.object(sync, 'write_json') as write:
            with self.assertRaises(SystemExit):
                sync.main()
            write.assert_not_called()

    def test_saving_multiple_changes_never_calls_native_and_keeps_latest_state(self):
        with tempfile.TemporaryDirectory() as root, \
                patch.object(sync, 'run_bridge', side_effect=AssertionError('save must not sync')):
            store = TaskStore(root)
            store.execute({'op': 'init'})
            task_id = store.execute({'op': 'create', 'actor': 'test', 'fields': {'title': 'first'}})['id']
            store.execute({'op': 'update', 'actor': 'test', 'id': task_id,
                           'changes': {'title': 'latest'}, 'expected': {'title': 'first'}})
            current = sync.read_snapshot(Path(root))
            request = sync.build_request(current['ledgers'], root)
            self.assertEqual(request['items'][0]['name'], 'latest')

    def test_bridge_timing_survives_failure_and_collects_native_stages(self):
        sync.BRIDGE_TIMINGS.clear()
        with patch.object(sync, '_run_bridge', return_value={'ok': True, 'timings': {
                'nativeReadMs': 100, 'nativeReadCount': 1, 'nativeWriteMs': 5}}):
            sync.run_bridge({'mode': 'read'})
        with patch.object(sync, '_run_bridge', side_effect=sync.SyncError('macos_sync_timeout', 'timeout')):
            with self.assertRaises(sync.SyncError):
                sync.run_bridge({'mode': 'apply'})
        self.assertEqual(sync.BRIDGE_TIMINGS['bridgeCalls'], 2)
        self.assertEqual(sync.BRIDGE_TIMINGS['lastBridgeMode'], 'apply')
        self.assertEqual(sync.BRIDGE_TIMINGS['nativeReadMs'], 100)
        self.assertGreaterEqual(sync.BRIDGE_TIMINGS['bridgeMs'], 0)


class ReadOnlyTaskQueryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = TaskStore(self.root)
        self.store.execute({'op': 'init'})
        self.tid = self.store.execute({'op': 'create', 'actor': 'test', 'fields': {'title': 'test'}})['id']

    def query(self, task_id=None):
        return status.local_task_status(self.root, task_id or self.tid)

    def tree(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def test_inspect_uses_shared_lock_without_creating_or_recovering_files(self):
        before = self.tree()
        with (self.root / '.task-store.lock').open('rb') as reader:
            fcntl.flock(reader, fcntl.LOCK_SH)
            self.assertTrue(self.store.execute({'op': 'inspect'})['ok'])
        self.assertEqual(before, self.tree())
        (self.root / '.task-store-transaction.json').write_text('unfinished')
        before = self.tree()
        result = self.query()
        self.assertEqual(result['code'], 'recovery_required')
        self.assertEqual(before, self.tree())

    def test_busy_lock_returns_within_budget_without_native_fallback(self):
        before = self.tree()
        with (self.root / '.task-store.lock').open('rb') as writer:
            fcntl.flock(writer, fcntl.LOCK_EX)
            started = time.monotonic()
            with patch.object(sync, 'run_bridge', side_effect=AssertionError('no fallback')):
                result = self.query()
            self.assertLess(time.monotonic() - started, 2)
        self.assertEqual(result['code'], 'lock_timeout')
        self.assertEqual(before, self.tree())

    def test_missing_lock_and_corrupt_data_are_not_repaired_by_query(self):
        lock = self.root / '.task-store.lock'
        lock.unlink()
        before = self.tree()
        self.assertEqual(self.query()['code'], 'inspect_unavailable')
        self.assertEqual(before, self.tree())
        lock.write_bytes(b'')
        (self.root / 'team-tasks.json').write_text('{broken')
        before = self.tree()
        self.assertFalse(self.query()['ok'])
        self.assertEqual(before, self.tree())

    def test_missing_task_and_pending_task_never_claim_native_completion(self):
        self.assertEqual(self.query('T-261013-999')['code'], 'task_not_found')
        result = self.query()
        self.assertEqual(result['ledgerStatus'], 'pending')
        self.assertEqual(result['currentCompletionOrigin'], 'unknown')
        self.assertFalse(result['currentNativeVerified'])

    def test_ledger_completion_and_archived_task_have_no_native_receipt(self):
        with patch('task_store.now', return_value='2020-01-06T10:00:00+08:00'):
            self.store.execute({'op': 'status', 'actor': 'test', 'id': self.tid,
                                'status': 'done', 'expected': {'status': 'pending'}})
        self.store.execute({'op': 'archive', 'month': '2020-01'})
        result = self.query()
        self.assertEqual(result['currentCompletionOrigin'], 'ledger')
        self.assertEqual(result['ledgerFile'], 'team-tasks-archive-2020-01.json')
        self.assertEqual(result['nativeCompletionHistory'], [])

    def test_external_receipt_is_historical_after_reopen_and_manual_completion(self):
        from task_store import status_history_fingerprint
        task = self.store.execute({'op': 'inspect'})['ledgers']['team-tasks.json']['tasks'][0]
        self.store.execute({'op': 'complete_external', 'actor': 'native', 'id': self.tid,
                            'expected': {'status': 'pending', 'historyFingerprint': status_history_fingerprint(task)},
                            'source': {'kind': 'macos-reminders', 'namespace': 'a' * 64,
                                       'reminderId': 'R-test', 'completionDate': '2026-10-13T10:00:00+00:00',
                                       'receiptId': 'b' * 64}})
        result = self.query()
        self.assertEqual(result['currentCompletionOrigin'], 'macos-reminders-record')
        self.assertEqual(len(result['nativeCompletionHistory']), 1)
        self.store.execute({'op': 'reopen', 'actor': 'test', 'id': self.tid, 'expected': {'status': 'done'}})
        self.assertEqual(self.query()['currentCompletionOrigin'], 'unknown')
        self.store.execute({'op': 'status', 'actor': 'test', 'id': self.tid,
                            'status': 'done', 'expected': {'status': 'pending'}})
        self.assertEqual(self.query()['currentCompletionOrigin'], 'ledger')
        self.assertEqual(len(self.query()['nativeCompletionHistory']), 1)

    def test_stale_terminal_mapping_is_not_evidence_of_completion(self):
        with patch('reminders_state.MirrorState') as mirror:
            mirror.return_value.binding.return_value = {'phase': 'complete'}
            mirror.return_value.mapping.return_value = {'tasks': {self.tid: {
                'state': 'terminal', 'observedFingerprint': 'old'}}}
            result = self.query()
        self.assertFalse(result['mappingStatusHistoryMatches'])
        self.assertEqual(result['ledgerStatus'], 'pending')
        self.assertEqual(result['currentCompletionOrigin'], 'unknown')

    def test_default_diagnostic_cli_is_local_and_returns_package_identity(self):
        with patch.object(status.NativeSchedule, 'status', return_value={'enabled': False}), \
                patch.object(sys, 'argv', ['sync', '--data-dir', str(self.root), '--diagnose', '--task-id', self.tid]), \
                patch.object(sync, 'run_bridge', side_effect=AssertionError('native forbidden')), \
                patch.object(sync, 'execute', side_effect=AssertionError('sync forbidden')), \
                patch.object(sys, 'stdout', new_callable=io.StringIO) as out:
            self.assertEqual(sync.main(), 0)
        result = json.loads(out.getvalue())
        self.assertEqual(result['packageVersion'], '1.6.6')
        self.assertEqual(result['requestMode'], 'diagnose')
        self.assertFalse(result['callsNative'])
        self.assertEqual(result['task']['taskId'], self.tid)

    def test_timeout_reaps_the_bridge_child_process(self):
        original_run = subprocess.run
        def sleeper(argv, **kwargs):
            kwargs['timeout'] = .1
            return original_run([sys.executable, '-c',
                'import os,time; print(os.getpid(),flush=True); time.sleep(60)'], **kwargs)
        with patch.object(sync.subprocess, 'run', side_effect=sleeper):
            with self.assertRaises(sync.SyncError) as raised:
                sync.run_bridge({'mode': 'probe'})
        child_pid = int(raised.exception.__cause__.stdout.strip())
        with self.assertRaises(ProcessLookupError):
            os.kill(child_pid, 0)

    def test_native_probe_is_single_fifteen_second_call_and_normal_sync_keeps_timeout(self):
        sync.BRIDGE_TIMINGS.clear()
        def blocked(argv, **kwargs):
            self.assertEqual(kwargs['timeout'], 15)
            raise subprocess.TimeoutExpired(argv, 15)
        with patch.object(sync.subprocess, 'run', side_effect=blocked) as runner:
            with self.assertRaises(sync.SyncError) as raised:
                sync.run_bridge({'mode': 'probe'})
            self.assertEqual(raised.exception.code, 'macos_probe_timeout')
            self.assertEqual(runner.call_count, 1)
        with patch.object(sync.subprocess, 'run', return_value=type('Response', (), {
                'returncode': 0, 'stdout': '{"ok":true}', 'stderr': ''})()) as runner:
            sync.run_bridge({'mode': 'read'})
            self.assertEqual(runner.call_args.kwargs['timeout'], 120)


if __name__ == '__main__':
    unittest.main()
