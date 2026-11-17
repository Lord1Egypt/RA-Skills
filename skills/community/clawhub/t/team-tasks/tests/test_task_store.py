import copy
import multiprocessing as mp
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'task_store.py'
sys.path.insert(0, str(SCRIPT.parent))
import task_store as mod


def worker(root, op, tid=None, number=0):
    store = mod.TaskStore(root)
    request = {'op': op, 'actor': 'worker'}
    if op == 'create':
        request['fields'] = {'title': 'parallel task'}
    elif op == 'comment':
        request.update(id=tid, content=str(number))
    else:
        request = {'op': 'remind', 'id': tid, 'slot': '2026-09-08T14:00+08:00'}
    store.execute(request)


def crash_worker(root, request, point):
    original = mod.atomic_write
    def fail(path, raw):
        if point == 'before_journal' and path.name == '.task-store-transaction.json':
            os._exit(81)
        if point == 'before_ledger' and path.name == mod.MAIN:
            os._exit(81)
        original(path, raw)
        if point == 'after_journal' and path.name == '.task-store-transaction.json':
            os._exit(81)
        if point == 'after_ledger' and path.name == mod.MAIN:
            os._exit(81)
    mod.atomic_write = fail
    mod.TaskStore(root).execute(request)


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = mod.TaskStore(self.root)
        self.store.execute({'op': 'init'})
        self.tid = self.store.execute({'op': 'create', 'actor': 'test', 'fields': {'title': 'first'}})['id']

    def docs(self):
        return self.store.execute({'op': 'read'})['ledgers']

    def task(self):
        return self.docs()[mod.MAIN]['tasks'][0]

    def raw(self):
        return (self.root / mod.MAIN).read_bytes()

    def fixture(self, doc):
        # Fixture setup is deliberately outside the production mutation API.
        (self.root / mod.MAIN).write_bytes(mod.encode(doc))

    def assert_rejected(self, request, code='validation_failed'):
        old = self.raw()
        with self.assertRaises(mod.StoreError) as err:
            self.store.execute(request)
        self.assertEqual(err.exception.code, code)
        self.assertEqual(old, self.raw())

    def test_nine_of_thirty_five_preserves_everything(self):
        doc = self.docs()[mod.MAIN]
        base = doc['tasks'][0]
        doc['extension'] = {'nested': [1, 2]}
        doc['tasks'] = []
        for i in range(35):
            task = copy.deepcopy(base)
            task['id'] = f'T-260101-{i+1:03}'
            task['comments'] = [{'at': mod.now(), 'from': 'a', 'content': 'valuable'}]
            task['custom'] = {'nested': [i]}
            doc['tasks'].append(task)
        self.fixture(doc)
        for task in doc['tasks'][:9]:
            self.store.execute({'op': 'update', 'actor': 'a', 'id': task['id'],
                                'changes': {'priority': 'high'}, 'expected': {'priority': 'medium'}})
        actual = self.docs()[mod.MAIN]
        self.assertEqual(len(actual['tasks']), 35)
        self.assertEqual(actual['tasks'][9:], doc['tasks'][9:])
        self.assertEqual(actual['extension'], doc['extension'])
        for before, after in zip(doc['tasks'][:9], actual['tasks'][:9]):
            expected = copy.deepcopy(before)
            expected['priority'] = 'high'
            expected['history'] = after['history']
            self.assertEqual(expected, after)
            self.assertEqual(after['history'][:-1], before['history'])

    def test_corruption_and_request_rejection(self):
        good = self.docs()[mod.MAIN]
        duplicate = copy.deepcopy(good)
        duplicate['tasks'].append(copy.deepcopy(duplicate['tasks'][0]))
        invalid_history = copy.deepcopy(good)
        invalid_history['tasks'][0]['history'] = None
        for value in [good['tasks'], duplicate, invalid_history, {'tasks': []}]:
            self.fixture(value)
            self.assert_rejected({'op': 'comment', 'actor': 'a', 'id': self.tid, 'content': 'no'})
        (self.root / mod.MAIN).write_bytes(b'{"tasks":')
        self.assert_rejected({'op': 'read'})
        self.fixture(good)
        for field in ['id', 'history', 'comments', 'status', 'reminderCount', 'tasks']:
            self.assert_rejected({'op': 'update', 'actor': 'a', 'id': self.tid,
                                  'changes': {field: []}, 'expected': {field: None}})
        self.assert_rejected({'op': 'replace', 'tasks': []})
        self.assert_rejected({'op': 'read', 'tasks': []})
        self.assert_rejected({'op': 'update', 'actor': 'a', 'id': self.tid,
                              'changes': {'priority': 'high'}, 'expected': {'priority': 'low'}}, 'conflict')
        with self.assertRaises(mod.StoreError):
            mod.decode(b'{"tasks": [], "tasks": []}')

    def test_concurrent_create_comment_reminder(self):
        ctx = mp.get_context('spawn')
        procs = [ctx.Process(target=worker, args=(str(self.root), op, self.tid, n))
                 for n in range(6) for op in ['create', 'comment', 'remind']]
        for process in procs:
            process.start()
        for process in procs:
            process.join(30)
            self.assertEqual(process.exitcode, 0)
        doc = self.docs()[mod.MAIN]
        self.assertEqual(len(doc['tasks']), 7)
        self.assertEqual(len({t['id'] for t in doc['tasks']}), 7)
        task = doc['tasks'][0]
        self.assertEqual(len(task['comments']), 6)
        self.assertEqual(task['reminderCount'], 1)
        # A late retry of an older slot remains idempotent after a newer slot.
        self.store.execute({'op': 'remind', 'id': self.tid, 'slot': '2026-09-08T18:00+08:00'})
        r = self.store.execute({'op': 'remind', 'id': self.tid, 'slot': '2026-09-08T14:00+08:00'})
        self.assertTrue(r['duplicate'])
        self.assertEqual(self.task()['reminderCount'], 2)

    def test_meaningful_comment_updates_progress_and_outbox_atomically(self):
        plain = self.store.execute({'op': 'comment', 'actor': 'Ada', 'id': self.tid,
                                    'content': '自动同步日志'})
        self.assertTrue(plain['ok'])
        before = self.task()['lastProgressAt']
        result = self.store.execute({'op': 'comment', 'actor': 'Ada', 'id': self.tid,
                                     'content': '已完成供应商确认', 'meaningfulProgress': True})
        self.assertTrue(result['ok'])
        saved = self.task()
        self.assertIsNone(before)
        self.assertTrue(saved['comments'][-1]['meaningfulProgress'])
        self.assertEqual(saved['lastProgressAt'], saved['comments'][-1]['at'])
        event = self.docs()[mod.MAIN]['_reminderSyncEvents'][-1]
        self.assertEqual(event['action'], 'comment')
        self.assertEqual(event['changedFields'], ['comments', 'lastProgressAt'])
        self.assert_rejected({'op': 'comment', 'actor': 'Ada', 'id': self.tid,
                              'content': 'bad', 'meaningfulProgress': 'yes'})

    def test_legacy_backup_handling(self):
        bak = self.root / (mod.MAIN + '.bak')
        bak.write_bytes(self.raw())
        self.docs()
        self.assertFalse(bak.exists())
        different = self.docs()[mod.MAIN]
        different['tasks'][0]['title'] = 'previous'
        bak.write_bytes(mod.encode(different))
        self.assert_rejected({'op': 'read'}, 'recovery_required')
        self.assertTrue(bak.exists())
        bak.write_bytes(b'{')
        self.assert_rejected({'op': 'read'}, 'recovery_required')

    def managed_backup(self, raw=None):
        folder = self.store.backups / ('20260908T060000.000000Z-' + 'b' * 32)
        folder.mkdir(exist_ok=True)
        path = folder / mod.MAIN
        path.write_bytes(self.raw() if raw is None else raw)
        return path

    def restore_request(self, path):
        return {'op': 'restore', 'backup': str(path),
                'expectedHash': mod.digest(self.raw())}

    def test_restore_managed_relative_and_absolute(self):
        backup = self.managed_backup()
        for source in [backup, backup.relative_to(self.store.root)]:
            self.assertTrue(self.store.execute(self.restore_request(source))['ok'])

    def test_restore_invalid_sources_never_read(self):
        backup = self.managed_backup()
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside) / mod.MAIN
            external.write_bytes(self.raw())
            sources = [external, self.root / 'chosen.json',
                       str(backup.parent / '..' / backup.parent.name / mod.MAIN),
                       backup.parent / 'team-tasks-archive-2020-01.json',
                       'backups/not-a-snapshot/' + mod.MAIN, None, 12]
            for source in sources:
                with self.subTest(source=source), patch.object(mod.os, 'fdopen') as read:
                    request = self.restore_request(source)
                    request['backup'] = source if source is None or source == 12 else str(source)
                    self.assert_rejected(request)
                    read.assert_not_called()

    def test_restore_symlinks_and_nonregular_never_read(self):
        backup = self.managed_backup()
        for component in [backup, backup.parent, self.store.backups]:
            moved = component.with_name(component.name + '-saved')
            component.rename(moved)
            component.symlink_to(moved, target_is_directory=moved.is_dir())
            try:
                with patch.object(mod.os, 'fdopen') as read:
                    self.assert_rejected(self.restore_request(backup))
                    read.assert_not_called()
            finally:
                component.unlink()
                moved.rename(component)
        backup.unlink()
        for kind in ['directory', 'fifo', 'hardlink']:
            if kind == 'directory':
                backup.mkdir()
            elif kind == 'fifo':
                os.mkfifo(backup)
            else:
                os.link(self.root / mod.MAIN, backup)
            try:
                with patch.object(mod.os, 'fdopen') as read:
                    self.assert_rejected(self.restore_request(backup))
                    read.assert_not_called()
            finally:
                backup.rmdir() if kind == 'directory' else backup.unlink()

    def test_restore_file_replaced_after_open_never_read(self):
        backup = self.managed_backup()
        original = mod.os.open
        def replace_after_open(path, flags, *args, **kwargs):
            fd = original(path, flags, *args, **kwargs)
            if path == mod.MAIN and flags & os.O_NOFOLLOW:
                backup.rename(backup.with_suffix('.saved'))
                backup.write_bytes(self.raw())
            return fd
        with patch.object(mod.os, 'open', side_effect=replace_after_open), patch.object(mod.os, 'fdopen') as read:
            self.assert_rejected(self.restore_request(backup), 'conflict')
            read.assert_not_called()

    def test_restore_directory_replaced_after_open_never_read(self):
        backup = self.managed_backup()
        original = mod.os.open
        def replace_after_open(path, flags, *args, **kwargs):
            fd = original(path, flags, *args, **kwargs)
            if path == backup.parent.name:
                backup.parent.rename(backup.parent.with_name(backup.parent.name + '-saved'))
                backup.parent.mkdir()
                backup.write_bytes(self.raw())
            return fd
        with patch.object(mod.os, 'open', side_effect=replace_after_open), patch.object(mod.os, 'fdopen') as read:
            self.assert_rejected(self.restore_request(backup), 'conflict')
            read.assert_not_called()

    def test_restore_inplace_change_during_read_rejected(self):
        backup = self.managed_backup()
        original = mod.os.fdopen
        def change_at_read(fd, *args, **kwargs):
            backup.write_bytes(self.raw() + b' ')
            return original(fd, *args, **kwargs)
        with patch.object(mod.os, 'fdopen', side_effect=change_at_read):
            self.assert_rejected(self.restore_request(backup), 'conflict')

    def test_restore_replacement_during_read_rejected(self):
        backup = self.managed_backup()
        original = mod.os.fdopen
        def replace_at_read(fd, *args, **kwargs):
            backup.rename(backup.with_suffix('.saved'))
            backup.write_bytes(self.raw())
            return original(fd, *args, **kwargs)
        with patch.object(mod.os, 'fdopen', side_effect=replace_at_read):
            self.assert_rejected(self.restore_request(backup), 'conflict')

    def test_restore_preserves_corrupt_evidence(self):
        good = self.raw()
        backup = self.managed_backup(good)
        (self.root / mod.MAIN).write_bytes(b'broken')
        (self.root / (mod.MAIN + '.bak')).write_bytes(b'legacy broken')
        self.assert_rejected({'op': 'restore', 'backup': str(backup), 'expectedHash': 'stale'}, 'conflict')
        result = self.store.execute({'op': 'restore', 'backup': str(backup),
                                     'expectedHash': mod.digest(b'broken')})
        self.assertEqual((Path(result['backup']) / mod.MAIN).read_bytes(), b'broken')
        self.assertEqual(self.raw(), good)
        self.assertEqual(next(self.root.glob('legacy-evidence-*')).joinpath(mod.MAIN + '.bak').read_bytes(), b'legacy broken')
        self.docs()

    def test_missing_ledger_never_auto_initializes(self):
        (self.root / mod.MAIN).unlink()
        with self.assertRaises(mod.StoreError) as err:
            self.docs()
        self.assertEqual(err.exception.code, 'recovery_required')
        self.assertFalse((self.root / mod.MAIN).exists())

    def test_lock_timeout(self):
        with self.store.locked():
            with self.assertRaises(mod.StoreError) as err:
                mod.TaskStore(self.root, timeout=.05).execute({'op': 'read'})
            self.assertEqual(err.exception.code, 'lock_timeout')
        self.assertTrue((self.root / '.task-store.lock').exists())
        self.docs()

    def test_io_failures_leave_main_readable(self):
        request = {'op': 'comment', 'actor': 'a', 'id': self.tid, 'content': 'safe'}
        old = self.raw()
        with patch.object(mod.tempfile, 'mkstemp', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                self.store.execute(request)
        self.assertEqual(old, self.raw())
        self.assertTrue(any(p.joinpath(mod.MAIN).read_bytes() == old for p in self.store.backups.iterdir() if p.joinpath(mod.MAIN).exists()))
        original = mod.atomic_write
        def fail(path, raw):
            if path.name == mod.MAIN:
                with patch.object(mod.os, 'fsync', side_effect=OSError('disk error')):
                    return original(path, raw)
            return original(path, raw)
        with patch.object(mod, 'atomic_write', side_effect=fail):
            with self.assertRaises(OSError):
                self.store.execute(request)
        self.assertEqual(old, self.raw())
        self.assertTrue(self.store.journal.exists())
        self.assertTrue(list(self.root.glob('.*.tmp')))
        result = self.store.execute({'op': 'read'})
        self.assertTrue(result['recoveredTransaction'])
        self.assertEqual(len(self.task()['comments']), 1)

    def test_real_process_exit_at_commit_boundaries(self):
        ctx = mp.get_context('spawn')
        for point in ['before_journal', 'after_journal', 'before_ledger', 'after_ledger']:
            before = len(self.task()['comments'])
            process = ctx.Process(target=crash_worker, args=(str(self.root),
                                 {'op': 'comment', 'actor': 'a', 'id': self.tid, 'content': point}, point))
            process.start()
            process.join(15)
            self.assertEqual(process.exitcode, 81)
            mod.validate(mod.decode(self.raw()))
            self.assertEqual(len(self.task()['comments']), before + (point != 'before_journal'))
            self.assertFalse(self.store.journal.exists())

    def prepare_archive(self):
        doc = self.docs()[mod.MAIN]
        task = doc['tasks'][0]
        task.update(status='done', completedAt='2020-01-01T10:00:00+08:00')
        self.fixture(doc)
        return copy.deepcopy(task)

    def test_archive_reopen_crash_and_id_scan(self):
        before = self.prepare_archive()
        ctx = mp.get_context('spawn')
        p = ctx.Process(target=crash_worker, args=(str(self.root), {'op': 'archive', 'month': '2020-01'}, 'after_ledger'))
        p.start()
        p.join(15)
        self.assertEqual(p.exitcode, 81)
        docs = self.docs()
        archive = 'team-tasks-archive-2020-01.json'
        self.assertEqual(docs[mod.MAIN]['tasks'], [])
        self.assertEqual(docs[archive]['tasks'], [before])
        created = self.store.execute({'op': 'create', 'actor': 'a', 'fields': {'title': 'new'}})
        self.assertNotEqual(created['id'], self.tid)
        p = ctx.Process(target=crash_worker, args=(str(self.root),
                           {'op': 'reopen', 'actor': 'a', 'id': self.tid, 'expected': {'status': 'done'}}, 'after_ledger'))
        p.start()
        p.join(15)
        self.assertEqual(p.exitcode, 81)
        docs = self.docs()
        self.assertEqual(docs[archive]['tasks'], [])
        reopened = next(t for t in docs[mod.MAIN]['tasks'] if t['id'] == self.tid)
        self.assertEqual(reopened['status'], 'pending')
        self.assertEqual(reopened['history'][:-1], before['history'])
        self.assertEqual(reopened['comments'], before['comments'])

    def test_transaction_divergence_blocks_all_replacements(self):
        self.prepare_archive()
        original = mod.atomic_write
        def fail(path, raw):
            if path.name == mod.MAIN:
                raise OSError('crash')
            return original(path, raw)
        with patch.object(mod, 'atomic_write', side_effect=fail):
            with self.assertRaises(OSError):
                self.store.execute({'op': 'archive', 'month': '2020-01'})
        doc = mod.decode(self.raw())
        doc['external'] = 'uncooperative writer'
        self.fixture(doc)
        self.assert_rejected({'op': 'read'}, 'recovery_required')
        self.assertFalse((self.root / 'team-tasks-archive-2020-01.json').exists())
        self.assertTrue(self.store.journal.exists())

    def test_later_participant_conflict_does_not_write_first(self):
        self.prepare_archive()
        original = mod.atomic_write
        def fail(path, raw):
            if path.name == mod.MAIN:
                raise OSError('crash before any ledger replacement')
            return original(path, raw)
        with patch.object(mod, 'atomic_write', side_effect=fail):
            with self.assertRaises(OSError):
                self.store.execute({'op': 'archive', 'month': '2020-01'})
        archive = self.root / 'team-tasks-archive-2020-01.json'
        archive.write_bytes(mod.encode({'version': '1.0', 'updatedAt': mod.now(), 'tasks': []}))
        old_archive = archive.read_bytes()
        self.assert_rejected({'op': 'read'}, 'recovery_required')
        self.assertEqual(archive.read_bytes(), old_archive)

    def test_disjoint_updates_survive_and_stale_same_field_conflicts(self):
        self.store.execute({'op': 'update', 'actor': 'a', 'id': self.tid,
                            'changes': {'title': 'new'}, 'expected': {'title': 'first'}})
        self.store.execute({'op': 'update', 'actor': 'b', 'id': self.tid,
                            'changes': {'priority': 'high'}, 'expected': {'priority': 'medium'}})
        self.assertEqual(self.task()['title'], 'new')
        self.assertEqual(self.task()['priority'], 'high')
        self.assert_rejected({'op': 'update', 'actor': 'a', 'id': self.tid,
                              'changes': {'title': 'stale'}, 'expected': {'title': 'first'}}, 'conflict')

    def test_reminder_sync_outbox_is_atomic_leased_and_acknowledged(self):
        created = self.docs()[mod.MAIN]['_reminderSyncEvents']
        self.assertEqual(len(created), 1)
        self.assertEqual(created[0]['action'], 'create')
        self.store.execute({'op': 'update', 'actor': 'a', 'id': self.tid,
                            'changes': {'dueDate': '2026-09-20'}, 'expected': {'dueDate': None}})
        claimed = self.store.execute({'op': 'sync_claim', 'actor': 'worker-a',
                                     'limit': 10, 'leaseSeconds': 60})['events']
        self.assertEqual(len(claimed), 2)
        self.assertEqual(self.store.execute({'op': 'sync_claim', 'actor': 'worker-b',
                                             'limit': 10, 'leaseSeconds': 60})['events'], [])
        self.assertEqual(self.store.execute({'op': 'sync_ack', 'actor': 'worker-b',
                                             'eventIds': [claimed[0]['id']]} )['acknowledged'], [])
        acknowledged = self.store.execute({'op': 'sync_ack', 'actor': 'worker-a',
                                           'eventIds': [claimed[0]['id']]})['acknowledged']
        self.assertEqual(acknowledged, [claimed[0]['id']])
        remaining = self.docs()[mod.MAIN]['_reminderSyncEvents']
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0]['changedFields'], ['dueDate'])

    def test_retention_keeps_last_100_and_recent_30_days(self):
        for p in self.store.backups.iterdir():
            for child in p.iterdir():
                child.unlink()
            p.rmdir()
        folders = []
        for i in range(105):
            folder = self.store.backups / (f'20200101T000000.{i:06}Z-' + 'a' * 32)
            folder.mkdir()
            (folder / mod.MAIN).write_bytes(self.raw())
            old = time.time() - 31 * 86400
            os.utime(folder, (old, old))
            folders.append(folder)
        # Even a folder outside the last 100 is retained if younger than 30 days.
        os.utime(folders[0], None)
        self.store.prune()
        self.assertTrue(folders[0].exists())
        self.assertFalse(folders[1].exists())
        self.assertEqual(len(list(self.store.backups.iterdir())), 101)

    def old_snapshot(self):
        folder = self.store.backups / ('20000101T000000.000000Z-' + 'c' * 32)
        folder.mkdir()
        (folder / mod.MAIN).write_bytes(self.raw())
        old = time.time() - 31 * 86400
        os.utime(folder, (old, old))
        for i in range(100):
            (self.store.backups / (f'20200101T000000.{i:06}Z-' + 'd' * 32)).mkdir()
        return folder

    def test_backup_and_prune_reject_external_directory_symlink(self):
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside)
            sentinel = external / mod.MAIN
            sentinel.write_bytes(b'outside')
            original = self.store.backups.with_name('backups-saved')
            self.store.backups.rename(original)
            self.store.backups.symlink_to(external, target_is_directory=True)
            before = self.raw()
            for action in [lambda: self.store.execute({'op': 'comment', 'actor': 'a',
                                                     'id': self.tid, 'content': 'blocked'}),
                           self.store.prune]:
                with self.assertRaises((OSError, mod.StoreError)):
                    action()
                self.assertEqual(self.raw(), before)
                self.assertEqual(list(external.iterdir()), [sentinel])
                self.assertEqual(sentinel.read_bytes(), b'outside')
            self.assertFalse(self.store.journal.exists())

    def test_backup_directory_replaced_after_open_stays_confined(self):
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside)
            original_open = mod.os.open
            def swap(path, flags, *args, **kwargs):
                fd = original_open(path, flags, *args, **kwargs)
                if path == 'backups':
                    self.store.backups.rename(self.store.backups.with_name('backups-saved'))
                    self.store.backups.symlink_to(external, target_is_directory=True)
                return fd
            before = self.raw()
            with patch.object(mod.os, 'open', side_effect=swap):
                with self.assertRaises(mod.StoreError):
                    self.store.backup({mod.MAIN: before})
            self.assertEqual(self.raw(), before)
            self.assertEqual(list(external.iterdir()), [])

    def test_prune_backups_replaced_after_open_stays_confined(self):
        folder = self.old_snapshot()
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside)
            sentinel = external / mod.MAIN
            sentinel.write_bytes(b'outside')
            original_open = mod.os.open
            def swap(path, flags, *args, **kwargs):
                fd = original_open(path, flags, *args, **kwargs)
                if path == 'backups':
                    self.store.backups.rename(self.store.backups.with_name('backups-saved'))
                    self.store.backups.symlink_to(external, target_is_directory=True)
                return fd
            with patch.object(mod.os, 'open', side_effect=swap):
                with self.assertRaises(mod.StoreError):
                    self.store.prune()
            self.assertEqual(sentinel.read_bytes(), b'outside')
            self.assertTrue(self.store.backups.with_name('backups-saved').joinpath(folder.name, mod.MAIN).exists())

    def test_prune_file_replaced_after_open_preserves_external_file(self):
        folder = self.old_snapshot()
        backup = folder / mod.MAIN
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside) / mod.MAIN
            external.write_bytes(b'outside')
            original_open = mod.os.open
            def swap(path, flags, *args, **kwargs):
                fd = original_open(path, flags, *args, **kwargs)
                if path == mod.MAIN:
                    backup.rename(backup.with_suffix('.saved'))
                    backup.symlink_to(external)
                return fd
            with patch.object(mod.os, 'open', side_effect=swap):
                with self.assertRaises(mod.StoreError):
                    self.store.prune()
            self.assertEqual(external.read_bytes(), b'outside')
            self.assertTrue(backup.is_symlink())

    def test_prune_snapshot_symlink_preserves_external_files(self):
        folder = self.old_snapshot()
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside)
            sentinel = external / mod.MAIN
            sentinel.write_bytes(b'outside')
            (folder / mod.MAIN).unlink()
            folder.rmdir()
            folder.symlink_to(external, target_is_directory=True)
            with self.assertRaises((OSError, mod.StoreError)):
                self.store.prune()
            self.assertEqual(sentinel.read_bytes(), b'outside')
            self.assertTrue(folder.is_symlink())

    def test_prune_bad_children_preserve_whole_snapshot(self):
        folder = self.old_snapshot()
        backup = folder / mod.MAIN
        other = folder / 'team-tasks-archive-2020-01.json'
        other.write_bytes(b'preserve')
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside) / mod.MAIN
            external.write_bytes(b'outside')
            for kind in ['symlink', 'hardlink', 'fifo']:
                backup.unlink()
                if kind == 'symlink':
                    backup.symlink_to(external)
                elif kind == 'hardlink':
                    os.link(external, backup)
                else:
                    os.mkfifo(backup)
                old = time.time() - 31 * 86400
                os.utime(folder, (old, old))
                with self.assertRaises((OSError, mod.StoreError)):
                    self.store.prune()
                self.assertEqual(external.read_bytes(), b'outside')
                self.assertEqual(other.read_bytes(), b'preserve')
                self.assertTrue(folder.exists())

    def test_prune_snapshot_replaced_after_open_stays_confined(self):
        folder = self.old_snapshot()
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside)
            sentinel = external / mod.MAIN
            sentinel.write_bytes(b'outside')
            original_open = mod.os.open
            def swap(path, flags, *args, **kwargs):
                fd = original_open(path, flags, *args, **kwargs)
                if path == folder.name:
                    folder.rename(folder.with_name(folder.name + '-saved'))
                    folder.symlink_to(external, target_is_directory=True)
                return fd
            with patch.object(mod.os, 'open', side_effect=swap):
                with self.assertRaises(mod.StoreError):
                    self.store.prune()
            self.assertEqual(sentinel.read_bytes(), b'outside')

    def test_backup_permissions_and_unsafe_existing_directory(self):
        self.assertEqual(self.store.backups.stat().st_mode & 0o777, 0o700)
        self.store.backups.chmod(0o755)
        folder = self.store.backup({mod.MAIN: self.raw()})
        self.assertEqual(self.store.backups.stat().st_mode & 0o777, 0o700)
        self.assertEqual(folder.stat().st_mode & 0o777, 0o700)
        self.assertEqual((folder / mod.MAIN).stat().st_mode & 0o777, 0o600)
        self.store.backups.chmod(0o777)
        try:
            with self.assertRaises(mod.StoreError):
                self.store.backup({mod.MAIN: self.raw()})
        finally:
            self.store.backups.chmod(0o700)
        info = list(os.stat(folder))
        info[4] = os.geteuid() + 1
        with self.assertRaises(mod.StoreError):
            self.store.check_owned(os.stat_result(info), directory=True)

    def test_prune_security_failure_after_commit_reports_success_with_warning(self):
        with patch.object(self.store, 'prune', side_effect=mod.StoreError('conflict', 'changed')):
            result = self.store.execute({'op': 'comment', 'actor': 'a',
                                         'id': self.tid, 'content': 'committed'})
        self.assertTrue(result['ok'])
        self.assertTrue(result['warnings'])
        self.assertEqual(self.task()['comments'][-1]['content'], 'committed')

    def test_cli_structured_errors(self):
        p = subprocess.run([sys.executable, str(SCRIPT), '--data-dir', str(self.root)],
                           input=b'{"op":"replace","tasks":[]}', capture_output=True)
        self.assertEqual(p.returncode, 1)
        result = mod.decode(p.stdout)
        self.assertFalse(result['ok'])
        self.assertEqual(result['code'], 'validation_failed')


if __name__ == '__main__':
    unittest.main()
