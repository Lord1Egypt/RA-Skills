import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import reminder_migration
import task_store


class ReminderMigrationTests(unittest.TestCase):
    def test_report_only_migrates_explicit_active_task_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            store = task_store.TaskStore(directory)
            store.execute({'op': 'init'})
            active = store.execute({'op': 'create', 'actor': 'test', 'fields': {'title': 'active'}})['id']
            done = store.execute({'op': 'create', 'actor': 'test', 'fields': {'title': 'done'}})['id']
            store.execute({'op': 'status', 'actor': 'test', 'id': done, 'status': 'done',
                           'expected': {'status': 'pending'}})
            before = store.execute({'op': 'read'})['ledgers'][task_store.MAIN]
            report = reminder_migration.report(directory, [
                {'id': 'already-dynamic', 'taskId': active, 'dynamic': True},
                {'id': 'static', 'taskId': active, 'dynamic': False},
                {'id': 'completed-one-shot', 'taskId': done, 'oneShot': True},
                {'id': 'no-id'},
                {'id': 'missing', 'taskId': 'T-000000-001'},
            ])
            self.assertEqual([entry['ruleId'] for entry in report['linked']], ['already-dynamic'])
            self.assertEqual([entry['ruleId'] for entry in report['pendingMigration']], ['static'])
            self.assertEqual({entry['ruleId'] for entry in report['orphans']}, {'no-id', 'missing'})
            self.assertEqual({entry['ruleId'] for entry in report['shouldDisable']},
                             {'completed-one-shot', 'no-id', 'missing'})
            after = store.execute({'op': 'read'})['ledgers'][task_store.MAIN]
            self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
