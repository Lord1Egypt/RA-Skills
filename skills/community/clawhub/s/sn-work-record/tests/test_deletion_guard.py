import copy
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
from submission_guard import bind_submission_session

class Session:
    headers = {'Authorization': 'Bearer fictional', 'Admin-OA-Token': 'fictional'}

class DeletionTests(unittest.TestCase):
    def test_explicit_confirmation_required_before_any_read_or_write(self):
        import deletion_guard as dg
        session = bind_submission_session(Session(), 'https://example.invalid', 'fixture')
        with self.assertRaises(ValueError):
            dg.protected_change(session, 'https://example.invalid', '123', action='delete', confirmation=None, read=lambda: self.fail('read'), write=lambda value: self.fail('write'))

    def test_delete_backups_complete_detail_and_restores_same_id(self):
        import deletion_guard as dg
        session = bind_submission_session(Session(), 'https://example.invalid', 'fixture')
        record = dict(id='123', fillDate='2026-10-08', projectId='1', projectName='fixture', projectPhase='1', workType='1', manHour=2, jobDesc='fictional', boToPmStatus=0, fillType='1', state='20', isDeleted=0, extra='preserved')
        original = copy.deepcopy(record)
        calls = []
        def write(value):
            calls.append(value)
            record['isDeleted'] = value
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'SN_WORK_RECORD_GUARD_DIR': tmp}):
            result = dg.protected_change(session, 'https://example.invalid', '123', action='delete', confirmation='123', read=lambda: copy.deepcopy(record), write=write)
            self.assertTrue(result['verified'])
            backups = list(Path(tmp).glob('deletion-*.json'))
            self.assertEqual(len(backups), 1)
            import json
            self.assertEqual(json.loads(backups[0].read_text())['backup'], original)
            self.assertEqual(backups[0].stat().st_mode & 0o777, 0o600)
            result = dg.protected_change(session, 'https://example.invalid', '123', action='restore', confirmation='123', read=lambda: copy.deepcopy(record), write=write)
            self.assertTrue(result['verified'])
            self.assertEqual(record, original)
            self.assertEqual(calls, [1, 0])

    def test_imported_delete_requires_explicit_confirmation(self):
        import oa_utils
        from unittest.mock import Mock
        session = Mock()
        with self.assertRaises(ValueError):
            oa_utils.update_time_entry(session, 'https://example.invalid', '123', is_deleted=1)
        session.put.assert_not_called()

    def test_unknown_outcome_never_retries_and_preserves_submission_guard(self):
        import deletion_guard as dg
        from submission_guard import SubmissionUncertain
        from unittest.mock import Mock
        for error in (TimeoutError(), ConnectionError(), RuntimeError('401'), KeyboardInterrupt()):
            with self.subTest(error=type(error).__name__), tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'SN_WORK_RECORD_GUARD_DIR': tmp}):
                session = bind_submission_session(Session(), 'https://example.invalid', 'fixture')
                record = dict(id='123', fillDate='2026-10-08', projectId='1', projectName='fixture', projectPhase='1', workType='1', manHour=2, jobDesc='fictional', boToPmStatus=0, fillType='1', state='20', isDeleted=0)
                guard = Path(tmp) / 'existing-submission.json'
                guard.write_bytes(b'untouched historical intent')
                guard.chmod(0o600)
                writer = Mock(side_effect=error)
                expected = KeyboardInterrupt if isinstance(error, KeyboardInterrupt) else SubmissionUncertain
                with self.assertRaises(expected):
                    dg.protected_change(session, 'https://example.invalid', '123', action='delete', confirmation='123', read=lambda: copy.deepcopy(record), write=writer)
                with self.assertRaises(SubmissionUncertain):
                    dg.protected_change(session, 'https://example.invalid', '123', action='delete', confirmation='123', read=lambda: copy.deepcopy(record), write=writer)
                self.assertEqual(writer.call_count, 1)
                self.assertEqual(guard.read_bytes(), b'untouched historical intent')

    def test_restore_without_backup_fails_closed(self):
        import deletion_guard as dg
        from unittest.mock import Mock
        session = bind_submission_session(Session(), 'https://example.invalid', 'fixture')
        record = dict(id='123', fillDate='2026-10-08', projectId='1', projectName='fixture', projectPhase='1', workType='1', manHour=2, jobDesc='fictional', boToPmStatus=0, fillType='1', state='20', isDeleted=1)
        writer = Mock()
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'SN_WORK_RECORD_GUARD_DIR': tmp}), self.assertRaises(ValueError):
            dg.protected_change(session, 'https://example.invalid', '123', action='restore', confirmation='123', read=lambda: record, write=writer)
        writer.assert_not_called()

    def test_date_changes_between_initial_read_and_lock_fail_closed(self):
        import deletion_guard as dg
        from unittest.mock import Mock
        session = bind_submission_session(Session(), 'https://example.invalid', 'fixture')
        record = dict(id='123', fillDate='2026-10-08', projectId='1', projectName='fixture', projectPhase='1', workType='1', manHour=2, jobDesc='fictional', boToPmStatus=0, fillType='1', state='20', isDeleted=0)
        reader = Mock(side_effect=[record, {**record, 'fillDate':'2026-10-09'}, {**record, 'isDeleted':1}])
        writer = Mock()
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'SN_WORK_RECORD_GUARD_DIR': tmp}), self.assertRaises(ValueError):
            dg.protected_change(session, 'https://example.invalid', '123', action='delete', confirmation='123', read=reader, write=writer)
        writer.assert_not_called()

    def test_concurrent_submission_day_lock_blocks_delete(self):
        import deletion_guard as dg
        from submission_guard import day_lock, digest
        from unittest.mock import Mock
        session = bind_submission_session(Session(), 'https://example.invalid', 'fixture')
        context = session._sn_submission_context
        record = dict(id='123', fillDate='2026-10-08', projectId='1', projectName='fixture', projectPhase='1', workType='1', manHour=2, jobDesc='fictional', boToPmStatus=0, fillType='1', state='20', isDeleted=0)
        writer = Mock()
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'SN_WORK_RECORD_GUARD_DIR': tmp}):
            scope = digest([context[0], context[1], record['fillDate']])
            with day_lock(Path(tmp) / (scope + '.lock')), self.assertRaises(ValueError):
                dg.protected_change(session, 'https://example.invalid', '123', action='delete', confirmation='123', read=lambda: record, write=writer)
        writer.assert_not_called()

    def test_field_conflict_after_deleted_record_prevents_restore(self):
        import deletion_guard as dg
        from submission_guard import SubmissionUncertain
        from unittest.mock import Mock
        session = bind_submission_session(Session(), 'https://example.invalid', 'fixture')
        record = dict(id='123', fillDate='2026-10-08', projectId='1', projectName='fixture', projectPhase='1', workType='1', manHour=2, jobDesc='fictional', boToPmStatus=0, fillType='1', state='20', isDeleted=0)
        writer = Mock(side_effect=lambda value: record.update(isDeleted=value))
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'SN_WORK_RECORD_GUARD_DIR': tmp}):
            dg.protected_change(session, 'https://example.invalid', '123', action='delete', confirmation='123', read=lambda: copy.deepcopy(record), write=writer)
            record['jobDesc'] = 'changed remotely'
            with self.assertRaises(SubmissionUncertain):
                dg.protected_change(session, 'https://example.invalid', '123', action='restore', confirmation='123', read=lambda: copy.deepcopy(record), write=writer)
        self.assertEqual(writer.call_count, 1)

if __name__ == '__main__': unittest.main()
