"""Offline amendment contract tests: all HTTP uses deterministic doubles."""
import copy
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import submission_guard as sg

HOST = 'https://oa.example'
ROW = dict(id='123', fillDate='2026-10-10 00:00:00', projectId='42',
           projectName='Example', projectPhase='1', workType='5', boToPmStatus=1,
           manHour=8, fillType='1', fillUserId='456', jobDesc='old',
           state='20', isDeleted=0, procInsId='process-123')
FINAL = {**ROW, 'jobDesc':'new', 'procInsId':'process-456'}

class Response:
    status_code = 200
    def __init__(self, data): self.data = data
    def raise_for_status(self): pass
    def json(self): return copy.deepcopy(self.data)

class Session:
    def __init__(self, reads=None, stop=None, save=None):
        self.headers = {'Authorization':'Bearer test-token', 'Admin-OA-Token':'test-token'}
        sg.bind_submission_session(self, HOST, 'test-account')
        self.reads = list(reads if reads is not None else [ROW, {**ROW,'state':'-1'}, FINAL])
        self.stop = stop if stop is not None else {'code':200,'isOk':True}
        self.save = save if save is not None else {'code':200,'isOk':True}
        self.calls = []
        self.detail = ROW
    def response(self, value):
        if callable(value): value = value()
        if isinstance(value, BaseException): raise value
        return Response(value)
    def get(self, url, **kwargs):
        self.calls.append(('details', copy.deepcopy(kwargs)))
        return self.response({'code':200,'data':self.detail})
    def post(self, url, **kwargs):
        endpoint = url.rsplit('/',1)[-1]
        self.calls.append((endpoint, copy.deepcopy(kwargs)))
        if endpoint == 'findEveryDayList':
            value = self.reads.pop(0)
            if callable(value): value = value()
            if isinstance(value, BaseException): raise value
            return self.response(value if isinstance(value, dict) and 'code' in value else {'code':200,'data':[value]})
        return self.response(self.stop if endpoint == 'stopProcess' else self.save)
    @property
    def writes(self): return [c for c in self.calls if c[0] in ('stopProcess','saveOrUpdate')]

def amend(session, **kwargs):
    import amendment_guard
    return amendment_guard.amend_time_entry(session, HOST, '123', 'new', **kwargs)

class AmendmentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.env = patch.dict(os.environ, {'SN_WORK_RECORD_GUARD_DIR':self.temp.name})
        self.env.start()
        self.addCleanup(self.env.stop)
    def test_live_success_code_string_is_accepted_without_coercion(self):
        import amendment_guard
        for code in (200, '200'):
            session = Session()
            response = {'code':code, 'isOk':True, 'data':copy.deepcopy(ROW)}
            with patch.object(session, 'get', return_value=Response(response)):
                self.assertEqual(amendment_guard._http(session, HOST, '/sn/timeEntry/details/123'), response)

    def test_malformed_success_codes_are_rejected(self):
        import amendment_guard
        for code in (True, 200.0, '0200', '200 ', ' 200', None):
            session = Session()
            with patch.object(session, 'get', return_value=Response({'code':code, 'isOk':True})):
                with self.assertRaises(ValueError):
                    amendment_guard._http(session, HOST, '/sn/timeEntry/details/123')

    def test_same_record_withdraw_resubmit_preserves_business_fields(self):
        session = Session()
        result = amend(session, withdraw_resubmit=True)
        self.assertEqual(result['amendment_status'], 'amended-confirmed')
        self.assertTrue(result['verified'])
        self.assertEqual(result['detail'], FINAL)
        self.assertEqual([c[0] for c in session.calls], ['details','findEveryDayList','stopProcess','findEveryDayList','saveOrUpdate','findEveryDayList'])
        self.assertEqual(session.writes[0][1]['json'], {'procInsId':'process-123'})
        payload = session.writes[1][1]['json']
        self.assertEqual(payload['saveOrSubmit'], 1)
        expected = {k:ROW[k] for k in ('id','projectId','projectName','projectPhase','workType','boToPmStatus','manHour','fillType','fillUserId','isDeleted')}
        expected.update(jobDesc='new', state='-1', fillDate='2026-10-10(周六)')
        self.assertEqual(payload['timeEntryList'], [expected])
        self.assertTrue(all(c[1]['allow_redirects'] is False for c in session.calls))

    def test_preview_and_consent_gate(self):
        session = Session()
        with self.assertRaises(ValueError): amend(session)
        self.assertEqual(session.calls, [])
        session = Session()
        result = amend(session, preview=True)
        self.assertEqual(result['amendment_status'], 'preview')
        self.assertEqual(session.writes, [])
        self.assertEqual(list(Path(self.temp.name).iterdir()), [])

    def test_matching_submitted_description_skips_without_stop(self):
        session = Session([FINAL])
        session.detail = FINAL
        result = amend(session, withdraw_resubmit=True)
        self.assertEqual(result['amendment_status'], 'skipped-existing')
        self.assertEqual(session.writes, [])

    def test_unproven_initial_row_refuses_before_write(self):
        cases = [{**ROW,'state':s} for s in ('-1','10','30','40',None,True)]
        cases += [{**ROW,'isDeleted':v} for v in (1,True,None)]
        cases += [{**ROW,'fillType':'2'}, {**ROW,'id':'124'}, {**ROW,'fillUserId':' 456'},
                  {**ROW,'manHour':'NaN'}, {**ROW,'fillDate':'2026-10-11'},
                  {**ROW,'fillDate':'2026-10-10junk'}, {**ROW,'projectId':'042'}]
        cases += [{k:v for k,v in ROW.items() if k != field} for field in ROW]
        cases += [{'code':200,'data':[]}, {'code':200,'data':[ROW,ROW]},
                  {'code':200,'data':[ROW],'complete':False}, {'code':200,'data':[ROW],'total':2},
                  {'code':200,'data':None}, {'code':500,'data':[ROW]}]
        for row in cases:
            with self.subTest(row=row):
                session = Session([row])
                with self.assertRaises((ValueError, RuntimeError)): amend(session, withdraw_resubmit=True)
                self.assertEqual(session.writes, [])

    def test_invalid_identifier_never_normalized_or_queried(self):
        from amendment_guard import amend_time_entry
        for token in (' 123','123 ','0123','123/x','',None,123,True):
            session = Session()
            with self.assertRaises(ValueError):
                amend_time_entry(session, HOST, token, 'new', withdraw_resubmit=True)
            self.assertEqual(session.calls, [])

    def test_stop_failure_or_timeout_never_resubmits_and_persists(self):
        for failure in (TimeoutError('secret host'), {'code':500}, {'code':200,'isOk':False}, KeyboardInterrupt()):
            with self.subTest(failure=type(failure).__name__):
                for path in Path(self.temp.name).glob('*.amend.json'): path.unlink()
                session = Session(stop=failure)
                with self.assertRaises((RuntimeError, KeyboardInterrupt)) as error:
                    amend(session, withdraw_resubmit=True)
                if not isinstance(failure, KeyboardInterrupt):
                    self.assertIn('撤回可能已发生', str(error.exception))
                    self.assertIn('未重新提交', str(error.exception))
                    self.assertNotIn('secret host', str(error.exception))
                self.assertEqual([c[0] for c in session.writes], ['stopProcess'])
                later = Session()
                with self.assertRaises(RuntimeError): amend(later, withdraw_resubmit=True)
                self.assertEqual(later.writes, [])
                self.assertEqual(len(list(Path(self.temp.name).glob('*.amend.json'))), 1)

    def test_save_timeout_only_reads_exact_final_record(self):
        session = Session(save=TimeoutError('secret token'))
        result = amend(session, withdraw_resubmit=True)
        self.assertEqual(result['amendment_status'], 'observed-after-uncertain')
        self.assertEqual([c[0] for c in session.writes], ['stopProcess','saveOrUpdate'])
        self.assertTrue(result['verified'])

    def test_final_must_have_exact_identity_immutable_values_and_status(self):
        for field, value in [('id','124'), ('jobDesc','other'), ('projectId','43'),
                             ('fillUserId','457'), ('manHour',7), ('fillDate','2026-10-11'),
                             ('state','30'), ('isDeleted',1), ('fillType','2')]:
            with self.subTest(field=field):
                for path in Path(self.temp.name).glob('*.amend.json'): path.unlink()
                session = Session([ROW, {**ROW,'state':'-1'}, {**FINAL,field:value}])
                with self.assertRaisesRegex(RuntimeError, '重新提交结果未知'):
                    amend(session, withdraw_resubmit=True)
                self.assertEqual(len(session.writes), 2)
                later = Session()
                with self.assertRaises(RuntimeError): amend(later, withdraw_resubmit=True)
                self.assertEqual(later.writes, [])

    def test_journal_is_private_hashed_and_durable_before_each_post(self):
        def inspect(phase):
            journal = next(Path(self.temp.name).glob('*.amend.json'))
            text = journal.read_text()
            value = json.loads(text)
            self.assertEqual(value['status'], phase)
            self.assertEqual(journal.stat().st_mode & 0o777, 0o600)
            for secret in ('test-account','test-token','Example','process-123', 'https://'):
                self.assertNotIn(secret, text)
            return {'code':200,'isOk':True}
        session = Session(stop=lambda:inspect('stop-pending'), save=lambda:inspect('save-pending'))
        amend(session, withdraw_resubmit=True)
        journal = next(Path(self.temp.name).glob('*.amend.json'))
        self.assertEqual(json.loads(journal.read_text())['status'], 'observed')
        self.assertEqual(len(list(Path(self.temp.name).glob('*.lock'))), 1)

    def test_identity_changes_at_each_boundary_block_progress(self):
        for phase in ('details','prequery','stop','withdrawn','save','final'):
            with self.subTest(phase=phase):
                for path in Path(self.temp.name).glob('*.amend.json'): path.unlink()
                session = Session()
                def change(value):
                    sg.bind_submission_session(session, HOST, 'another-account')
                    return value
                if phase == 'details':
                    session.get = lambda *a, **k: session.response(change({'code':200,'data':ROW}))
                elif phase == 'prequery': session.reads[0] = lambda:change(ROW)
                elif phase == 'stop': session.stop = lambda:change({'code':200,'isOk':True})
                elif phase == 'withdrawn': session.reads[1] = lambda:change({**ROW,'state':'-1'})
                elif phase == 'save': session.save = lambda:change({'code':200,'isOk':True})
                else: session.reads[2] = lambda:change(FINAL)
                with self.assertRaises((ValueError,RuntimeError)): amend(session, withdraw_resubmit=True)
                self.assertEqual(len(session.writes), 0 if phase in ('details','prequery') else 1 if phase in ('stop','withdrawn') else 2)

    def test_retry_adapter_on_stop_endpoint_rejected_before_any_http(self):
        import requests
        session = requests.Session()
        session.headers.update({'Authorization':'Bearer test-token','Admin-OA-Token':'test-token'})
        sg.bind_submission_session(session, HOST, 'test-account')
        session.mount(HOST + '/sn/workflow/', requests.adapters.HTTPAdapter(max_retries=1))
        with patch.object(session, 'request') as request:
            with self.assertRaises(ValueError): amend(session, withdraw_resubmit=True)
            request.assert_not_called()

    def test_withdrawn_business_boolean_change_refuses_save(self):
        session = Session([ROW, {**ROW,'state':'-1','isDeleted':False}])
        with self.assertRaisesRegex(RuntimeError, '未重新提交'):
            amend(session, withdraw_resubmit=True)
        self.assertEqual([c[0] for c in session.writes], ['stopProcess'])

    def test_withdrawn_detail_after_interruption_reports_uncertainty(self):
        session = Session(stop=KeyboardInterrupt())
        with self.assertRaises(KeyboardInterrupt): amend(session, withdraw_resubmit=True)
        later = Session()
        later.detail = {**ROW,'state':'-1'}
        with self.assertRaisesRegex(RuntimeError, '撤回可能已发生'):
            amend(later, withdraw_resubmit=True)
        self.assertEqual(later.writes, [])

    def test_pending_history_and_incomplete_current_detail_still_reports_uncertainty(self):
        session = Session(stop=KeyboardInterrupt())
        with self.assertRaises(KeyboardInterrupt): amend(session, withdraw_resubmit=True)
        later = Session()
        later.detail = {k:v for k,v in ROW.items() if k != 'procInsId'}
        with self.assertRaisesRegex(RuntimeError, '撤回可能已发生'):
            amend(later, withdraw_resubmit=True)
        self.assertEqual(later.writes, [])

    def test_day_lock_is_shared_with_ordinary_submit_and_spans_every_phase(self):
        checked = []
        def contend(phase, value):
            contender = Session()
            with self.assertRaises(ValueError): amend(contender, withdraw_resubmit=True)
            self.assertEqual(contender.writes, [])
            payload = {'timeEntryList':[{**ROW,'fillDate':'2026-10-10'}], 'saveOrSubmit':1}
            with self.assertRaises(ValueError):
                sg.guarded_submit(Session(), HOST, payload,
                                  lambda *a:self.fail('ordinary query ran under amendment lock'),
                                  lambda:self.fail('ordinary write ran under amendment lock'))
            checked.append(phase)
            return value
        session = Session([lambda:contend('initial',ROW),
                           lambda:contend('withdrawn',{**ROW,'state':'-1'}),
                           lambda:contend('final',FINAL)],
                          stop=lambda:contend('stop',{'code':200,'isOk':True}),
                          save=lambda:contend('save',{'code':200,'isOk':True}))
        amend(session, withdraw_resubmit=True)
        self.assertEqual(checked, ['initial','stop','withdrawn','save','final'])
        context = session._sn_submission_context
        scope = sg.digest([context[0],context[1],'2026-10-10'])
        self.assertTrue((Path(self.temp.name)/(scope+'.lock')).exists())

    def test_pending_different_wording_cannot_replace_intent(self):
        session = Session(stop=KeyboardInterrupt())
        with self.assertRaises(KeyboardInterrupt): amend(session, withdraw_resubmit=True)
        path = next(Path(self.temp.name).glob('*.amend.json'))
        original = path.read_bytes()
        from amendment_guard import amend_time_entry
        later = Session()
        with self.assertRaises(RuntimeError):
            amend_time_entry(later, HOST, '123', 'another description', withdraw_resubmit=True)
        self.assertEqual(later.writes, [])
        self.assertEqual(path.read_bytes(), original)

    def test_observed_amendment_allows_new_explicit_amendment_only(self):
        amend(Session(), withdraw_resubmit=True)
        from amendment_guard import amend_time_entry
        final2 = {**FINAL,'jobDesc':'next','procInsId':'process-789'}
        later = Session([FINAL,{**FINAL,'state':'-1'},final2])
        later.detail = FINAL
        result = amend_time_entry(later, HOST, '123', 'next', withdraw_resubmit=True)
        self.assertEqual(result['amendment_status'], 'amended-confirmed')
        self.assertEqual(len(later.writes), 2)

    def test_save_uncertainty_reconciles_on_later_call_without_post(self):
        session = Session([ROW,{**ROW,'state':'-1'},RuntimeError('read failed')], save=TimeoutError())
        with self.assertRaises(RuntimeError): amend(session, withdraw_resubmit=True)
        later = Session([FINAL])
        later.detail = FINAL
        result = amend(later, withdraw_resubmit=True)
        self.assertEqual(result['amendment_status'], 'skipped-existing')
        self.assertEqual(later.writes, [])
        path = next(Path(self.temp.name).glob('*.amend.json'))
        self.assertEqual(json.loads(path.read_text())['status'], 'observed')

    def test_corrupt_or_insecure_journal_never_writes(self):
        session = Session(stop=KeyboardInterrupt())
        with self.assertRaises(KeyboardInterrupt): amend(session, withdraw_resubmit=True)
        path = next(Path(self.temp.name).glob('*.amend.json'))
        for content in ('{}','not json'):
            path.write_text(content)
            later = Session()
            with self.assertRaises(RuntimeError): amend(later, withdraw_resubmit=True)
            self.assertEqual(later.writes, [])
        path.chmod(0o644)
        with self.assertRaises(ValueError): amend(Session(), withdraw_resubmit=True)
        path.unlink()
        target = Path(self.temp.name)/'target'
        target.write_text('{}')
        target.chmod(0o600)
        path.symlink_to(target)
        with self.assertRaises(OSError): amend(Session(), withdraw_resubmit=True)
        self.assertEqual(target.read_text(), '{}')

    def test_ordinary_pending_journal_is_not_bypassed_or_changed(self):
        session = Session()
        context = session._sn_submission_context
        scope = sg.digest([context[0],context[1],'2026-10-10'])
        path = Path(self.temp.name)/(scope+'.json')
        sg.save_journal(path, dict(version=1, scope=scope, request=sg.digest('ordinary'),status='pending'))
        original = path.read_bytes()
        with self.assertRaises(RuntimeError): amend(session, withdraw_resubmit=True)
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(session.writes, [])
        self.assertEqual(list(Path(self.temp.name).glob('*.amend.json')), [])

    def test_stop_redirect_and_401_never_lead_to_save(self):
        import amendment_guard as guard
        for status in (302,401):
            for path in Path(self.temp.name).glob('*.amend.json'): path.unlink()
            session = Session()
            original = session.post
            def post(url, **kwargs):
                if url.endswith('stopProcess'):
                    session.calls.append(('stopProcess',copy.deepcopy(kwargs)))
                    reply = Response({'code':200,'isOk':True})
                    reply.status_code = status
                    return reply
                return original(url, **kwargs)
            session.post = post
            with self.assertRaisesRegex(RuntimeError, '未重新提交'): amend(session, withdraw_resubmit=True)
            self.assertEqual([c[0] for c in session.writes], ['stopProcess'])
            self.assertFalse(session.writes[0][1]['allow_redirects'])

    def test_journal_boolean_version_is_malformed_not_version_one(self):
        amend(Session(), withdraw_resubmit=True)
        path = next(Path(self.temp.name).glob('*.amend.json'))
        value = json.loads(path.read_text())
        value['version'] = True
        path.write_text(json.dumps(value))
        later = Session([FINAL])
        later.detail = FINAL
        with self.assertRaises(RuntimeError): amend(later, withdraw_resubmit=True)
        self.assertEqual(later.writes, [])

if __name__ == '__main__': unittest.main()
