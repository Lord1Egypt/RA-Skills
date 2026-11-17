"""Offline contract tests; never authenticate or contact OA."""
import contextlib
import importlib
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))


class QueryRangesTests(unittest.TestCase):
    def module(self):
        self.assertTrue((SCRIPTS / 'query_time_ranges.py').exists(), 'CLI not implemented')
        return importlib.import_module('query_time_ranges')

    def test_invalid_ranges_before_api_import_or_auth(self):
        mod = self.module()
        for bounds in [('2026-02-30', '2026-03-01'), ('2026-1-01', '2026-01-02'),
                       ('2026-10-03', '2026-10-01')]:
            with self.subTest(bounds=bounds), patch.object(mod, '_api') as api:
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as exc:
                    mod.main(['--range', *bounds, '--json'])
                self.assertEqual(exc.exception.code, 2)
                api.assert_not_called()

    def run_cli(self, responses, args=None):
        from types import SimpleNamespace
        from unittest.mock import Mock
        mod = self.module()
        session = object()
        auth = SimpleNamespace(call=lambda operation: operation(session))
        def query(s, url, day):
            self.assertIs(s, session)
            value = responses[day]
            if isinstance(value, Exception):
                raise value
            return value
        api = SimpleNamespace(load_credentials=Mock(return_value=('user-secret', 'pass-secret', 'https://oa.invalid')),
                              resolve_base_url=lambda base, override: override or base,
                              OAAuth=Mock(return_value=auth), query_time_entries=Mock(side_effect=query),
                              state_to_text=lambda state: {'10': '草稿', '30': '已审批'}.get(state, state))
        out, err = io.StringIO(), io.StringIO()
        with patch.object(mod, '_api', return_value=api), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = mod.main(args or ['--range', '2026-10-08', '2026-10-08', '--json'])
        self.assertTrue(out.getvalue(), 'No snapshot produced')
        return rc, json.loads(out.getvalue()), api, out.getvalue() + err.getvalue()

    @staticmethod
    def record(identity='internal-id', hours='0.1', **fields):
        return dict(id=identity, manHour=hours, jobDesc='  exact\n描述  ', state='30',
                    projectName='Project', **fields)

    def test_observed_oa_midnight_datetime_is_validated(self):
        for value, expected in [('2026-10-08 00:00:00', 0),
                                ('2026-10-09 00:00:00', 1),
                                ('2026-10-08 24:00:00', 1),
                                ('2026-10-08 00:00:00garbage', 1)]:
            with self.subTest(fillDate=value):
                rows = [self.record(fillDate=value)]
                rc, result, _, _ = self.run_cli({'2026-10-08': (rows, {'code': '200', 'data': rows})})
                self.assertEqual(rc, expected)
                self.assertEqual(result['stats']['records'], 1 if expected == 0 else 0)

    def test_success_overlaps_decimal_multiple_records(self):
        rows = [self.record(), self.record('second-id', '0.2')]
        rc, result, api, text = self.run_cli({
            '2026-10-08': (rows, {'code': 200, 'data': rows}),
            '2026-10-09': ([], {'code': 200, 'data': []})},
            ['--range', '2026-10-08', '2026-10-09', '--range', '2026-10-08', '2026-10-08', '--json'])
        self.assertEqual(rc, 0)
        self.assertTrue(result['complete'])
        self.assertEqual(api.OAAuth.call_count, 1)
        self.assertEqual(api.query_time_entries.call_count, 2)
        self.assertEqual(result['stats'], {'records': 2, 'dates': 1, 'hours': '0.3', 'states': {'已审批': 2}})
        self.assertEqual([g['stats']['hours'] for g in result['ranges']], ['0.3', '0.3'])
        self.assertEqual(result['days'][0]['records'][0]['description'], rows[0]['jobDesc'])
        self.assertEqual(result['days'][1]['status'], 'empty')
        self.assertNotIn('internal-id', text)
        self.assertNotIn('second-id', text)

    def test_failed_or_malformed_days_are_not_empty(self):
        good = [self.record()]
        bad_cases = [RuntimeError('pass-secret token-secret raw-body'), ([], {'code': 500, 'data': []}),
                     ([], {'code': 200}), ([], {'code': 200, 'data': None}),
                     ([], {'code': 200, 'data': {}}), ([42], {'code': 200, 'data': [42]}),
                     (good, {'code': 200, 'data': []})]
        for response in bad_cases:
            with self.subTest(response=response):
                rc, result, _, text = self.run_cli({'2026-10-08': (good, {'code': 200, 'data': good}),
                                                   '2026-10-09': response},
                    ['--range', '2026-10-08', '2026-10-09', '--json'])
                self.assertNotEqual(rc, 0)
                self.assertFalse(result['complete'])
                self.assertTrue(result['partial'])
                self.assertEqual(result['days'][1]['status'], 'failed')
                self.assertIn(result['days'][1]['error_type'], ['query_failed', 'malformed_response'])
                self.assertEqual(result['stats']['records'], 1)
                self.assertFalse(result['ranges'][0]['complete'])
                for secret in ('pass-secret', 'token-secret', 'raw-body'):
                    self.assertNotIn(secret, text)

    def test_duplicate_ids_count_once_and_conflicts_fail_closed(self):
        row = self.record()
        rc, result, _, _ = self.run_cli({'2026-10-08': ([row, row.copy()], {'code': 200, 'data': [row, row.copy()]})})
        self.assertEqual(rc, 0)
        self.assertEqual(result['stats']['records'], 1)
        conflict = dict(row, manHour='7')
        for rows in ([row, conflict], [row, dict(row, projectId='different')]):
            rc, result, _, _ = self.run_cli({'2026-10-08': (rows, {'code': 200, 'data': rows})})
            self.assertEqual(rc, 1)
            self.assertEqual(result['days'][0]['error_type'], 'conflicting_id')
            self.assertEqual(result['stats']['records'], 0)
        rc, result, _, _ = self.run_cli({day: ([row], {'code': 200, 'data': [row]})
                                        for day in ['2026-10-08', '2026-10-09']},
                                       ['--range', '2026-10-08', '2026-10-09', '--json'])
        self.assertEqual(rc, 1)
        self.assertEqual(result['stats']['records'], 0)
        self.assertTrue(all(d['error_type'] == 'conflicting_id' for d in result['days']))

    def test_invalid_records_fail_day_not_silently_drop(self):
        invalid = [dict(self.record(), id=value) for value in [None, '', ' ', True, [], {}]]
        invalid += [dict(self.record(), manHour=value) for value in [None, True, 'NaN', 'Infinity', '-1', 'bad']]
        invalid += [dict(self.record(), **fields) for fields in [
            {'fillDate': '2026-10-09'}, {'fillDate': 'bad'}, {'jobDesc': None}, {'state': None},
            {'projectName': {'token': 'secret'}}, {'createdTime': []}]]
        missing = self.record(); del missing['id']; invalid.append(missing)
        for row in invalid:
            with self.subTest(row=row):
                rc, result, _, _ = self.run_cli({'2026-10-08': ([row], {'code': 200, 'data': [row]})})
                self.assertEqual(rc, 1)
                self.assertEqual(result['days'][0]['status'], 'failed')
                self.assertEqual(result['stats']['records'], 0)

    def test_draft_date_suffix_and_exact_decimal_sum(self):
        rows = [dict(self.record('a', '1234567890123456789012345678.1', fillDate='2026-10-08(周四)'), state='10'),
                self.record('b', '0.2', fillDate='2026-10-08')]
        rc, result, _, _ = self.run_cli({'2026-10-08': (rows, {'code': 200, 'data': rows})})
        self.assertEqual(rc, 0)
        self.assertEqual(result['stats']['hours'], '1234567890123456789012345678.3')
        self.assertEqual(result['stats']['states'], {'草稿': 1, '已审批': 1})

    def test_auth_and_backend_logs_never_leak(self):
        mod = self.module()
        from types import SimpleNamespace
        def noisy(*args):
            print('user-secret pass-secret token-secret')
            print('raw-body', file=sys.stderr)
            raise RuntimeError('pass-secret')
        api = SimpleNamespace(load_credentials=lambda path: ('user-secret', 'pass-secret', 'url'),
                              resolve_base_url=lambda base, override: base, OAAuth=noisy)
        out, err = io.StringIO(), io.StringIO()
        with patch.object(mod, '_api', return_value=api), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = mod.main(['--range', '2026-10-08', '2026-10-09', '--json'])
        self.assertEqual(rc, 1)
        result = json.loads(out.getvalue())
        self.assertFalse(result['complete'])
        self.assertTrue(all(d['error_type'] == 'authentication_failed' for d in result['days']))
        for secret in ('user-secret', 'pass-secret', 'token-secret', 'raw-body'):
            self.assertNotIn(secret, out.getvalue() + err.getvalue())

    def test_private_atomic_evidence_contains_real_results_no_credentials(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'evidence.json'
            rows = [dict(self.record(), token='token-secret', password='pass-secret')]
            rc, result, _, text = self.run_cli({'2026-10-08': (rows, {'code': 200, 'data': rows, 'token': 'token-secret'})},
                ['--range', '2026-10-08', '2026-10-08', '--json', '--raw-output', str(target)])
            self.assertEqual(rc, 0)
            self.assertTrue(target.exists(), 'Evidence was not saved')
            self.assertEqual(os.stat(target).st_mode & 0o777, 0o600)
            evidence = json.loads(target.read_text())
            self.assertEqual(evidence['snapshot'], result)
            self.assertEqual(evidence['queries'][0]['response']['data'][0]['id'], 'internal-id')
            self.assertEqual(evidence['queries'][0]['response']['data'][0]['jobDesc'], rows[0]['jobDesc'])
            for secret in ('user-secret', 'pass-secret', 'token-secret'):
                self.assertNotIn(secret, target.read_text() + text)
            self.assertEqual(sorted(p.name for p in Path(directory).iterdir()), ['evidence.json'])
            before = target.read_bytes()
            rc, result, api, _ = self.run_cli({}, ['--range', '2026-10-08', '2026-10-08', '--json', '--raw-output', str(target)])
            self.assertEqual(rc, 1)
            api.OAAuth.assert_not_called()
            self.assertEqual(target.read_bytes(), before)
            self.assertEqual(result['error_type'], 'evidence_failed')

    def test_evidence_publish_race_never_overwrites(self):
        import tempfile
        mod = self.module()
        self.assertTrue(hasattr(mod, 'write_evidence'), 'Atomic publisher missing')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'exists.json'
            path.write_text('preserve me')
            with self.assertRaises(FileExistsError):
                mod.write_evidence(path, {'snapshot': 'new'})
            self.assertEqual(path.read_text(), 'preserve me')
            self.assertEqual(len(list(Path(directory).iterdir())), 1)

    def test_real_readonly_api_seam_and_no_bootstrap_on_import(self):
        import oa_utils
        from types import SimpleNamespace
        mod = self.module()
        calls = []
        rows = [self.record()]
        class Session:
            def post(inner, url, *, json, timeout):
                self.assertEqual(url, 'https://oa.invalid/sn/timeEntry/findEveryDayList')
                self.assertEqual(set(json), {'fillDate'})
                calls.append(json['fillDate'])
                return SimpleNamespace(raise_for_status=lambda: None,
                                       json=lambda: {'code': 200, 'data': rows})
        session = Session()
        auth = SimpleNamespace(call=lambda operation: operation(session))
        out = io.StringIO()
        with patch.object(oa_utils, 'load_credentials', return_value=('u', 'p', 'https://oa.invalid')) as creds, \
             patch.object(oa_utils, 'OAAuth', return_value=auth) as factory, \
             patch.object(mod, '_api', return_value=oa_utils), contextlib.redirect_stdout(out):
            rc = mod.main(['--range', '2026-10-08', '2026-10-08', '--credentials', 'custom.md',
                           '--base-url', 'https://oa.invalid/', '--json'])
        self.assertEqual(rc, 0)
        self.assertEqual(calls, ['2026-10-08'])
        creds.assert_called_once_with('custom.md')
        factory.assert_called_once_with('https://oa.invalid', 'u', 'p')
        import runtime_bootstrap
        with patch.object(runtime_bootstrap, 'ensure_runtime') as boot:
            importlib.reload(mod)
            boot.assert_not_called()

    def test_empty_all_failed_and_output_modes(self):
        rc, result, _, _ = self.run_cli({'2026-10-08': ([], {'code': 200, 'data': []})},
                                       ['--range', '2026-10-08', '2026-10-08'])
        self.assertEqual(rc, 0)
        self.assertTrue(result['complete'])
        self.assertEqual(result['stats'], {'records': 0, 'dates': 0, 'hours': '0', 'states': {}})
        rc, result, _, _ = self.run_cli({'2026-10-08': TimeoutError('private')})
        self.assertEqual(rc, 1)
        self.assertFalse(result['complete'])
        self.assertEqual(result['days'][0]['status'], 'failed')

    def test_partial_evidence_does_not_include_failure_body(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'partial.json'
            rc, result, _, _ = self.run_cli({'2026-10-08': ([], {'code': 200, 'data': []}),
                                            '2026-10-09': RuntimeError('secret-error-body')},
                ['--range', '2026-10-08', '2026-10-09', '--raw-output', str(path), '--json'])
            self.assertEqual(rc, 1)
            evidence = json.loads(path.read_text())
            self.assertEqual(evidence['snapshot'], result)
            self.assertEqual(len(evidence['queries']), 1)
            self.assertNotIn('secret-error-body', path.read_text())

    def test_conflict_invalidates_prior_day_even_when_later_record_malformed(self):
        row = self.record()
        bad = dict(row, manHour='not-hours')
        rc, result, _, _ = self.run_cli({
            '2026-10-08': ([row], {'code': 200, 'data': [row]}),
            '2026-10-09': ([bad], {'code': 200, 'data': [bad]})},
            ['--range', '2026-10-08', '2026-10-09', '--json'])
        self.assertEqual(rc, 1)
        self.assertEqual(result['stats']['records'], 0)
        self.assertTrue(all(d['error_type'] == 'conflicting_id' for d in result['days']))


if __name__ == '__main__':
    unittest.main()
