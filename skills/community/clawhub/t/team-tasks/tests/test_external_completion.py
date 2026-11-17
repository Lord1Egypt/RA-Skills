import copy
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import task_store as mod


def crash_completion(root, request, point):
    original = mod.atomic_write

    def write(path, raw):
        if point == 'before_journal' and path.name == '.task-store-transaction.json':
            os._exit(81)
        if point == 'before_ledger' and path.name == mod.MAIN:
            os._exit(81)
        original(path, raw)
        if point == 'after_journal' and path.name == '.task-store-transaction.json':
            os._exit(81)
        if point == 'after_ledger' and path.name == mod.MAIN:
            os._exit(81)

    mod.atomic_write = write
    mod.TaskStore(root).execute(request)
    if point == 'after_commit':
        os._exit(81)  # The caller never receives the committed response.


def completion_worker(root, request):
    mod.TaskStore(root).execute(request)


class ExternalCompletionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = mod.TaskStore(self.root)
        self.store.execute({'op': 'init'})
        self.tid = self.store.execute({'op': 'create', 'actor': 'Alice',
                                       'fields': {'title': '完成季度核对'}})['id']

    def docs(self):
        return self.store.execute({'op': 'read'})['ledgers']

    def task(self):
        return next(t for d in self.docs().values() for t in d['tasks'] if t['id'] == self.tid)

    def request(self):
        return {'op': 'complete_external', 'actor': 'macOS 提醒事项', 'id': self.tid,
                'expected': {'status': 'pending',
                             'historyFingerprint': mod.status_history_fingerprint(self.task())},
                'source': {'kind': 'macos-reminders', 'namespace': 'a' * 64,
                           'reminderId': 'x-apple-reminder://123',
                           'completionDate': '2020-01-05T14:10:00+08:00',
                           'receiptId': 'b' * 64}}

    def reject(self, request, code='validation_failed'):
        before = (self.root / mod.MAIN).read_bytes()
        with self.assertRaises(mod.StoreError) as raised:
            self.store.execute(request)
        self.assertEqual(raised.exception.code, code)
        self.assertEqual((self.root / mod.MAIN).read_bytes(), before)

    def assert_once(self, request):
        task = self.task()
        receipts = [h for h in task['history'] if isinstance(h['detail'], dict) and
                    h['detail'].get('externalCompletion', {}).get('receiptId') ==
                    request['source']['receiptId']]
        self.assertEqual(task['status'], 'done')
        self.assertEqual(len(receipts), 1)
        self.assertEqual(receipts[0]['action'], 'status')
        self.assertEqual(receipts[0]['detail']['externalCompletion'], request['source'])
        self.assertEqual(len([c for c in task['comments'] if
                              request['source']['completionDate'] in c['content']]), 1)
        events = self.docs()[mod.MAIN]['_reminderSyncEvents']
        self.assertEqual([e['action'] for e in events], ['create', 'status', 'comment'])
        self.assertEqual([e['changedFields'] for e in events[-2:]], [['status'], ['comments']])
        self.assertNotIn('_externalCompletionReceipts', self.docs()[mod.MAIN])

    def test_atomic_completion_provenance_and_idempotent_retry(self):
        request = self.request()
        original = self.task()
        stamp = '2020-01-06T10:00:00+08:00'
        with patch.object(mod, 'now', return_value=stamp):
            result = self.store.execute(request)
        self.assertFalse(result['duplicate'])
        self.assertTrue(result['changed'])
        saved = self.task()
        self.assertEqual(saved['completedAt'], stamp)
        self.assertEqual(saved['comments'][-1]['at'], stamp)
        self.assertIn(request['source']['completionDate'], saved['comments'][-1]['content'])
        self.assertEqual(saved['history'][:-2], original['history'])
        self.assert_once(request)
        before = (self.root / mod.MAIN).read_bytes()
        retry = self.store.execute(request)
        self.assertTrue(retry['duplicate'])
        self.assertFalse(retry['changed'])
        self.assertEqual((self.root / mod.MAIN).read_bytes(), before)

    def test_canonical_status_fingerprint_and_unrelated_changes(self):
        request = self.request()
        initial = self.task()
        canonical = json.dumps(initial['history'], sort_keys=True, ensure_ascii=False,
                               separators=(',', ':')).encode('utf-8')
        self.assertEqual(request['expected']['historyFingerprint'], hashlib.sha256(canonical).hexdigest())
        self.store.execute({'op': 'comment', 'actor': 'Bob', 'id': self.tid, 'content': '已核对数据'})
        self.store.execute({'op': 'update', 'actor': 'Bob', 'id': self.tid,
                            'changes': {'priority': 'high'}, 'expected': {'priority': 'medium'}})
        self.assertEqual(mod.status_history_fingerprint(self.task()),
                         request['expected']['historyFingerprint'])
        self.store.execute(request)
        self.assertEqual(self.task()['priority'], 'high')
        self.assertEqual(self.task()['comments'][0]['content'], '已核对数据')
        self.assertNotEqual(mod.status_history_fingerprint(self.task()),
                            request['expected']['historyFingerprint'])

    def test_status_done_then_reopen_rejects_stale_aba_fingerprint(self):
        request = self.request()
        self.store.execute({'op': 'status', 'actor': 'Alice', 'id': self.tid,
                            'status': 'done', 'expected': {'status': 'pending'}})
        self.store.execute({'op': 'reopen', 'actor': 'Alice', 'id': self.tid,
                            'expected': {'status': 'done'}})
        self.assertEqual(self.task()['status'], 'pending')
        self.reject(request, 'conflict')
        self.assertEqual(self.task()['comments'], [])

    def test_duplicate_survives_reopen_without_completing_again(self):
        request = self.request()
        self.store.execute(request)
        self.store.execute({'op': 'reopen', 'actor': 'Alice', 'id': self.tid,
                            'expected': {'status': 'done'}})
        result = self.store.execute(request)
        self.assertTrue(result['duplicate'])
        self.assertFalse(result['changed'])
        self.assertEqual(self.task()['status'], 'pending')
        self.assertEqual(len(self.task()['comments']), 1)

    def test_archived_duplicate_is_safe_and_novel_completion_is_rejected(self):
        request = self.request()
        with patch.object(mod, 'now', return_value='2020-01-06T10:00:00+08:00'):
            self.store.execute(request)
        self.store.execute({'op': 'archive', 'month': '2020-01'})
        archived = self.root / 'team-tasks-archive-2020-01.json'
        before = archived.read_bytes()
        self.assertTrue(self.store.execute(request)['duplicate'])
        self.assertEqual(archived.read_bytes(), before)
        novel = copy.deepcopy(request)
        novel['source']['receiptId'] = 'c' * 64
        self.reject(novel, 'conflict')
        self.assertEqual(archived.read_bytes(), before)

    def test_same_receipt_with_different_source_conflicts(self):
        request = self.request()
        self.store.execute(request)
        for key, value in [('namespace', 'c' * 64), ('reminderId', 'another-id'),
                           ('completionDate', '2020-01-05T14:11:00+08:00')]:
            changed = copy.deepcopy(request)
            changed['source'][key] = value
            with self.subTest(key=key):
                self.reject(changed, 'conflict')

    def test_non_pending_task_is_not_overridden(self):
        request = self.request()
        self.store.execute({'op': 'status', 'actor': 'Alice', 'id': self.tid,
                            'status': 'cancelled', 'expected': {'status': 'pending'}})
        self.reject(request, 'conflict')
        self.assertEqual(self.task()['status'], 'cancelled')

    def test_external_input_validation_does_not_mutate(self):
        malformed = [None, {}, {'kind': 'macos-reminders'}]
        for source in malformed:
            request = self.request()
            request['source'] = source
            self.reject(request)
        for key, value in [('kind', 'other'), ('namespace', 'x' * 64), ('receiptId', 'short'),
                           ('reminderId', ''), ('reminderId', '\x00'),
                           ('completionDate', '2020-01-05T14:10:00'),
                           ('completionDate', '2020-13-05T14:10:00+08:00'),
                           ('completionDate', None)]:
            request = self.request()
            request['source'][key] = value
            with self.subTest(key=key, value=value):
                self.reject(request)
        for expected in [None, {}, {'status': 'done', 'historyFingerprint': 'a' * 64},
                         {'status': 'pending', 'historyFingerprint': 'z' * 64}]:
            request = self.request()
            request['expected'] = expected
            self.reject(request)
        request = self.request()
        request['source']['extra'] = True
        self.reject(request)

    def test_utc_z_completion_date_is_supported(self):
        request = self.request()
        request['source']['completionDate'] = '2020-01-05T06:10:00Z'
        self.assertTrue(self.store.execute(request)['changed'])

    def test_completion_preserves_existing_outbox_leases(self):
        request = self.request()
        event = self.store.execute({'op': 'sync_claim', 'actor': 'scheduler'})['events'][0]
        self.store.execute(request)
        events = self.docs()[mod.MAIN]['_reminderSyncEvents']
        self.assertEqual(events[0], event)
        self.assertNotIn('lease', events[1])
        self.assertNotIn('lease', events[2])

    def test_concurrent_comments_and_duplicate_completion_are_preserved(self):
        request = self.request()
        ctx = mp.get_context('spawn')
        requests = [request, request] + [
            {'op': 'comment', 'actor': 'Bob', 'id': self.tid, 'content': 'comment-' + str(n)}
            for n in range(3)]
        processes = [ctx.Process(target=completion_worker, args=(str(self.root), r)) for r in requests]
        for process in processes:
            process.start()
        for process in processes:
            process.join(30)
            self.assertEqual(process.exitcode, 0)
        saved = self.task()
        self.assertEqual(len(saved['comments']), 4)
        self.assertEqual({c['content'] for c in saved['comments'] if c['from'] == 'Bob'},
                         {'comment-' + str(n) for n in range(3)})
        self.assertEqual(len([h for h in saved['history'] if h['action'] == 'status']), 1)
        events = self.docs()[mod.MAIN]['_reminderSyncEvents']
        self.assertEqual(len([e for e in events if e['action'] == 'status']), 1)
        self.assertEqual(len([e for e in events if e['action'] == 'comment']), 4)

    def test_faults_and_lost_response_recover_exactly_once(self):
        ctx = mp.get_context('spawn')
        for point in ['before_journal', 'after_journal', 'before_ledger', 'after_ledger', 'after_commit']:
            with self.subTest(point=point), tempfile.TemporaryDirectory() as root:
                store = mod.TaskStore(root)
                store.execute({'op': 'init'})
                tid = store.execute({'op': 'create', 'actor': 'Alice',
                                     'fields': {'title': 'atomic'}})['id']
                request = self.request()
                request['id'] = tid
                task = store.execute({'op': 'read'})['ledgers'][mod.MAIN]['tasks'][0]
                request['expected']['historyFingerprint'] = mod.status_history_fingerprint(task)
                process = ctx.Process(target=crash_completion, args=(root, request, point))
                process.start()
                process.join(30)
                self.assertEqual(process.exitcode, 81)
                result = store.execute(request)
                self.assertEqual(result['duplicate'], point != 'before_journal')
                self.assertTrue(store.execute(request)['duplicate'])
                doc = store.execute({'op': 'read'})['ledgers'][mod.MAIN]
                saved = doc['tasks'][0]
                self.assertEqual(saved['status'], 'done')
                self.assertEqual(len(saved['comments']), 1)
                self.assertEqual([h['action'] for h in saved['history']], ['create', 'status', 'comment'])
                self.assertEqual([e['action'] for e in doc['_reminderSyncEvents']],
                                 ['create', 'status', 'comment'])
                self.assertFalse(Path(root, '.task-store-transaction.json').exists())


if __name__ == '__main__':
    unittest.main()
