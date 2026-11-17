"""Injected HTTP fakes only; never contact OA or write real records."""
import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import oa_utils as oa

HOST = 'https://oa.example'
VALUES = dict(project_id='42', project_name='Example', man_hour=8,
              project_phase='1', work_type='5', bo_to_pm_status=1, fill_type='1')
ROW = dict(fillDate='2026-10-10', projectId='42', projectName='Example',
           manHour='8.00', projectPhase=1, workType=5, boToPmStatus=1,
           fillType=1, jobDesc='work', state=20, isDeleted=0, id='fake-record')

class Response:
    def __init__(self, data): self.data = data
    def raise_for_status(self): pass
    def json(self): return copy.deepcopy(self.data)

class Session:
    def __init__(self, reads, write=None):
        self.reads = list(reads)
        self.write = write or {'code':200}
        self.calls = []
        self.headers = {'Authorization':'Bearer fake-token', 'Admin-OA-Token':'fake-token'}
        from submission_guard import bind_submission_session
        bind_submission_session(self, HOST, 'fake-account')
    def post(self, url, **kwargs):
        self.calls.append((url.rsplit('/',1)[-1], copy.deepcopy(kwargs)))
        value = self.reads.pop(0) if url.endswith('findEveryDayList') else self.write
        if callable(value): value = value()
        if isinstance(value, BaseException): raise value
        return Response(value)
    @property
    def writes(self): return [c for c in self.calls if c[0]=='saveOrUpdate']

def listing(rows): return {'code':200, 'data':copy.deepcopy(rows)}
def submit(session, **changes):
    return oa.submit_time_entry(session, HOST, '2026-10-10', job_desc='work', **{**VALUES, **changes})

class GuardTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        # Later guard persistence uses an isolated private root; never personal state.
        self.home_patch = patch.dict('os.environ', {'SN_WORK_RECORD_GUARD_DIR':self.directory.name})
        self.home_patch.start()
        self.addCleanup(self.home_patch.stop)

    def clear_fake_journals(self):
        # Independent simulated cases, not a real recovery mechanism.
        for path in Path(self.directory.name).glob('*.json'):
            path.unlink()

    def test_request_digest_does_not_round_large_integer_hours(self):
        from submission_guard import request_digest
        self.assertNotEqual(request_digest({**ROW,'manHour':1234567890123456789012345678901}),
                            request_digest({**ROW,'manHour':1234567890123456789012345678902}))
        self.assertEqual(request_digest({**ROW,'manHour':8}), request_digest({**ROW,'manHour':8.0}))

    def test_explicit_failed_or_incomplete_envelope_never_allows_write(self):
        for metadata in ({'isOk':False}, {'complete':False}, {'last':False}, {'has_more':True}, {'total':False}):
            session = Session([{'code':200,'data':[], **metadata}])
            with self.assertRaises(ValueError):
                submit(session)
            self.assertEqual(session.writes, [])
            self.assertEqual(list(Path(self.directory.name).glob('*.json')), [])

    def test_postwrite_account_change_cannot_confirm_other_accounts_record(self):
        session = Session([listing([]), listing([ROW])])
        def change_identity():
            from submission_guard import bind_submission_session
            bind_submission_session(session, HOST, 'another-account')
            return {'code':200}
        session.write = change_identity
        with self.assertRaises(RuntimeError):
            submit(session)
        self.assertEqual(len(session.writes), 1)
        self.clear_fake_journals()
        later = Session([listing([])])
        def change_on_readback():
            from submission_guard import bind_submission_session
            bind_submission_session(later, HOST, 'another-account')
            return listing([ROW])
        later.reads.append(change_on_readback)
        with self.assertRaises(RuntimeError):
            submit(later)
        self.assertEqual(len(later.writes), 1)

    def test_context_changed_during_prequery_blocks_before_pending_or_post(self):
        session = Session([])
        def change_identity():
            session.headers['Authorization'] = 'Bearer another-token'
            session.headers['Admin-OA-Token'] = 'another-token'
            return listing([])
        session.reads = [change_identity]
        with self.assertRaises(ValueError):
            submit(session)
        self.assertEqual(session.writes, [])
        self.assertEqual(list(Path(self.directory.name).glob('*.json')), [])
        for changes in ({'project_name':123}, {'bo_to_pm_status':2}):
            candidate = Session([listing([])])
            with self.assertRaises(ValueError):
                submit(candidate, **changes)
            self.assertEqual(candidate.calls, [])

    def test_private_storage_crash_and_cross_process_lock_regressions(self):
        import json
        import os
        import multiprocessing
        from submission_guard import SubmissionUncertain
        # OS-level locks, not only a Python in-process mutex.
        checked = []
        def prequery():
            context = multiprocessing.get_context('fork')
            parent, child = context.Pipe()
            def contender():
                candidate = Session([listing([])])
                try:
                    submit(candidate)
                except ValueError:
                    child.send({'blocked':True, 'calls':len(candidate.calls)})
                else:
                    child.send({'blocked':False, 'calls':len(candidate.calls)})
                child.close()
            process = context.Process(target=contender)
            process.start()
            child.close()
            self.assertTrue(parent.poll(5))
            outcome = parent.recv()
            process.join(5)
            self.assertEqual(process.exitcode, 0)
            self.assertEqual(outcome, {'blocked':True,'calls':0})
            checked.append(True)
            parent.close()
            return listing([])
        session = Session([prequery, listing([ROW])])
        submit(session)
        self.assertEqual(checked, [True])
        self.clear_fake_journals()
        # A process interruption bypasses Exception handling, leaving intent durable.
        session = Session([listing([])], write=KeyboardInterrupt())
        with self.assertRaises(KeyboardInterrupt):
            submit(session)
        later = Session([listing([])])
        with self.assertRaises(SubmissionUncertain):
            submit(later)
        self.assertEqual(later.writes, [])
        journal = next(Path(self.directory.name).glob('*.json'))
        self.assertEqual(json.loads(journal.read_text())['status'], 'pending')
        for raw in ('{}', 'not json'):
            journal.write_text(raw)
            candidate = Session([listing([])])
            with self.assertRaises(SubmissionUncertain):
                submit(candidate)
            self.assertEqual(candidate.calls, [])
        journal.chmod(0o644)
        with self.assertRaises(ValueError):
            submit(Session([listing([])]))
        journal.unlink()
        Path(self.directory.name).chmod(0o755)
        candidate = Session([listing([])])
        with self.assertRaises(ValueError):
            submit(candidate)
        self.assertEqual(candidate.calls, [])
        Path(self.directory.name).chmod(0o700)

    def test_prewrite_failure_does_not_leave_pending_marker(self):
        for reply in (RuntimeError('failed read'), {'code':200}, listing([{**ROW,'jobDesc':'conflict'}])):
            session = Session([reply])
            with self.assertRaises((RuntimeError, ValueError)):
                submit(session)
            self.assertEqual(list(Path(self.directory.name).glob('*.json')), [])
            self.assertEqual(session.writes, [])
        for field in ROW:
            if field in ('id',):
                continue
            candidate = Session([listing([{k:v for k,v in ROW.items() if k != field}])])
            with self.assertRaises(ValueError):
                submit(candidate)
            self.assertEqual(candidate.writes, [])

    def test_write_transport_cannot_redirect_or_automatically_retry(self):
        session = Session([listing([]), listing([ROW])])
        submit(session)
        self.assertIs(session.writes[0][1].get('allow_redirects'), False)
        import requests
        from submission_guard import bind_submission_session
        actual = requests.Session()
        actual.headers.update({'Authorization':'Bearer fake-token','Admin-OA-Token':'fake-token'})
        actual.mount('https://', requests.adapters.HTTPAdapter(max_retries=1))
        bind_submission_session(actual, HOST, 'fake-account')
        with patch.object(actual, 'request') as request:
            with self.assertRaises(ValueError):
                submit(actual)
            request.assert_not_called()

    def test_observed_postwrite_conflict_cannot_later_turn_into_success(self):
        session = Session([listing([]), listing([{**ROW,'jobDesc':'other'}]), listing([ROW])])
        with self.assertRaises(RuntimeError):
            submit(session)
        self.assertEqual(len(session.writes), 1)
        self.assertEqual(len(session.calls), 3)

    def test_refreshed_auth_session_preserves_account_binding(self):
        first = Session([listing([ROW])])
        second = Session([listing([ROW])])
        second._sn_submission_context = None
        with patch.object(oa, 'build_session', return_value=first):
            auth = oa.OAAuth(HOST, 'fake-account', 'unused', token='fake-token')
        with patch.object(auth, '_acquire', return_value=(second,'fake-token')), patch.object(oa, 'clear_cached_token'):
            auth.refresh()
        self.assertEqual(submit(auth.session)['submission_status'], 'skipped-existing')

    def test_server_midnight_date_is_compared_as_same_date_only(self):
        session = Session([listing([{**ROW, 'fillDate':'2026-10-10 00:00:00'}])])
        self.assertEqual(submit(session)['submission_status'], 'skipped-existing')
        for value in ('2026-10-10 12:00:00', '2026-10-10junk', '2026-10-11 00:00:00', '2026-1-1 00:00:00'):
            session = Session([listing([{**ROW, 'fillDate':value}])])
            with self.assertRaises(ValueError):
                submit(session)
            self.assertEqual(session.writes, [])
        self.assertEqual(submit(Session([listing([{**ROW,'state':30}])]))['submission_status'], 'skipped-existing')
        session = Session([listing([])] + [listing([{**ROW,'state':30}])]*3)
        with self.assertRaises(RuntimeError):
            submit(session)
        self.assertEqual(len(session.writes), 1)

    def test_local_day_lock_spans_prequery_post_and_readback(self):
        checked = []
        def contender_at(phase, response):
            contender = Session([listing([])])
            with self.assertRaises(ValueError):
                submit(contender, project_id='43')
            self.assertEqual(contender.calls, [])
            checked.append(phase)
            return response
        session = Session([
            lambda: contender_at('prequery', listing([])),
            lambda: contender_at('readback', listing([ROW]))],
            write=lambda: contender_at('write', {'code':200}))
        self.assertEqual(submit(session)['submission_status'], 'submitted-confirmed')
        self.assertEqual(checked, ['prequery','write','readback'])
        self.assertEqual(len(session.writes), 1)

    def test_uncertain_marker_survives_calls_and_is_private_before_post(self):
        import json
        import os
        from submission_guard import SubmissionUncertain
        inspected = []
        def inspect_before_post():
            journals = list(Path(self.directory.name).glob('*.json'))
            self.assertEqual(len(journals), 1)
            data = json.loads(journals[0].read_text())
            self.assertEqual(data['status'], 'pending')
            self.assertEqual(set(data), {'version','scope','request','status'})
            self.assertEqual(journals[0].stat().st_mode & 0o777, 0o600)
            self.assertEqual(Path(self.directory.name).stat().st_mode & 0o777, 0o700)
            self.assertNotIn('fake-account', journals[0].read_text())
            self.assertNotIn('fake-token', journals[0].read_text())
            self.assertNotIn('Example', journals[0].read_text())
            inspected.append(True)
            raise RuntimeError('timeout')
        session = Session([listing([])]*4, write=inspect_before_post)
        with self.assertRaises(SubmissionUncertain):
            submit(session)
        self.assertEqual(inspected, [True])
        for changes in ({}, {'project_id':'43'}, {'man_hour':7}):
            later = Session([listing([])])
            with self.assertRaises(SubmissionUncertain):
                submit(later, **changes)
            self.assertEqual(later.writes, [])
        observed = Session([listing([ROW])])
        self.assertEqual(submit(observed)['submission_status'], 'skipped-existing')
        self.assertEqual(observed.writes, [])
        # Even a formerly observed attempt must not resend if records vanish.
        later = Session([listing([])])
        with self.assertRaises(SubmissionUncertain):
            submit(later)
        self.assertEqual(later.writes, [])

    def test_write_is_success_only_after_exact_submitted_readback(self):
        session = Session([listing([]), listing([]), listing([ROW])])
        result = submit(session)
        self.assertEqual(result.get('submission_status'), 'submitted-confirmed')
        self.assertTrue(result.get('verified'))
        self.assertEqual(len(session.writes), 1)
        self.assertEqual([c[0] for c in session.calls], ['findEveryDayList','saveOrUpdate','findEveryDayList','findEveryDayList'])
        for record in ({**ROW,'state':10}, {**ROW,'jobDesc':'other'}, {**ROW,'isDeleted':1},
                       {k:v for k,v in ROW.items() if k != 'workType'}):
            self.clear_fake_journals()
            session = Session([listing([])] + [listing([record])]*3)
            with self.assertRaises(RuntimeError):
                submit(session)
            self.assertEqual(len(session.writes), 1)

    def test_ambiguous_write_queries_without_ever_resending(self):
        for error in (RuntimeError('network ambiguous'), {'code':500}, ValueError('invalid response')):
            self.clear_fake_journals()
            session = Session([listing([]), listing([ROW])], write=error)
            result = submit(session)
            self.assertEqual(result.get('submission_status'), 'observed-after-uncertain')
            self.assertTrue(result.get('verified'))
            self.assertEqual(len(session.writes), 1)
        self.clear_fake_journals()
        session = Session([listing([])] + [listing([])]*3, write=RuntimeError('timeout'))
        with self.assertRaises(RuntimeError):
            submit(session)
        self.assertEqual(len(session.writes), 1)
        self.assertEqual(len(session.calls), 5)

    def test_invalid_scope_or_draft_fails_before_any_network(self):
        for changes in ({'save_or_submit':0}, {'save_or_submit':True}, {'fill_type':'2'},
                        {'project_id':'042'}, {'work_type':'5.0'}, {'project_phase':True}):
            session = Session([listing([])])
            with self.assertRaises(ValueError):
                submit(session, **changes)
            self.assertEqual(session.calls, [])
        for bad_date in ('2026-02-30', '2026-1-1', '2026-10-10(周六)'):
            session = Session([listing([])])
            with self.assertRaises(ValueError):
                oa.submit_time_entry(session, HOST, bad_date, job_desc='work', **VALUES)
            self.assertEqual(session.calls, [])
        for context in (None, ('https://other.example', 'x'), (HOST, 'bad')):
            session = Session([listing([])])
            session._sn_submission_context = context
            with self.assertRaises(ValueError):
                submit(session)
            self.assertEqual(session.calls, [])

        with patch.object(oa, 'build_session', return_value=Session([listing([ROW])])):
            auth = oa.OAAuth(HOST, 'fake-account', 'unused', token='fake-token')
            self.assertEqual(submit(auth.session)['submission_status'], 'skipped-existing')
            auth.session.headers['Authorization'] = 'Bearer changed-token'
            with self.assertRaises(ValueError):
                submit(auth.session)

    def test_same_day_conflicts_or_unproven_queries_never_write(self):
        cases = [listing([{**ROW, 'jobDesc':'different'}]), listing([{**ROW, 'state':10}]),
                 listing([{**ROW, 'state':40}]), listing([{**ROW, 'isDeleted':1}]),
                 listing([{**ROW, 'projectId':'43'}]), listing([ROW, ROW]),
                 listing([{k:v for k,v in ROW.items() if k != 'workType'}]),
                 {'code':200}, {'code':200,'data':None}, {'code':200,'data':{}},
                 {'code':200,'data':[],'hasMore':True}, {'code':200,'data':[],'total':1},
                 {'code':500,'data':[]}, RuntimeError('query failed')]
        for response in cases:
            with self.subTest(response=response):
                session = Session([response])
                with self.assertRaises((ValueError, RuntimeError)):
                    submit(session)
                self.assertEqual(session.writes, [])

    def test_identical_submitted_record_is_skipped_at_common_api(self):
        session = Session([listing([ROW])])
        result = submit(session)
        self.assertEqual(result['submission_status'], 'skipped-existing')
        self.assertEqual(session.writes, [])
        self.assertEqual(session.calls[0][0], 'findEveryDayList')
