"""Default model-visible Key flow. Synthetic credentials; no real host or SMS.

The platform fixture below checks the handoff contract, not Agent reliability
or an actual platform's persistence/loading support.
"""
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_account_flow import FakeAPI, LoginAPI, account, inputs


class KeyOutputTests(unittest.TestCase):
    def run_cli(self, api, data=None, command=None):
        data = inputs(action='verify', smsCode='012345') if data is None else data
        with patch.object(account, 'AccountAPI', return_value=api), \
             patch.object(account, 'CodexConfig', side_effect=AssertionError('native config')), \
             patch.object(account, 'PrivateHandoff', side_effect=AssertionError('private handoff')), \
             patch('socket.create_connection', side_effect=AssertionError('network')), \
             patch.object(sys, 'argv', ['account', *(command or ['register', '--input-stdin'])]), \
             patch.object(sys, 'stdin', io.StringIO(json.dumps(data))), \
             patch.object(sys, 'stdout', io.StringIO()) as out, \
             patch.object(sys, 'stderr', io.StringIO()) as err:
            code = account.main()
        self.assertEqual(err.getvalue(), '')
        text = out.getvalue()
        result = json.loads(text)
        for value in ('test_only_access_token', data.get('smsCode')):
            if value:
                self.assertNotIn(value, text)
        if result['status'] == 'sms_sent' or result.get('login_completed') is True:
            self.assertEqual(result['phone'], data['phone'])
            self.assertNotIn('phone_masked', result)
        if result['status'] != 'credential_available':
            self.assertNotIn('api_key', result)
            self.assertNotIn(getattr(api, 'secret', 'not-a-real-key'), text)
        return code, result, text

    def test_default_new_and_existing_user_return_key_without_configuration(self):
        for new in (True, False):
            with self.subTest(new=new):
                api = LoginAPI(new=new)
                code, result, text = self.run_cli(api)
                self.assertEqual(code, 0)
                self.assertEqual(result['status'], 'credential_available')
                self.assertEqual(result['api_key'], api.secret)
                self.assertEqual(text.count(api.secret), 1)
                self.assertTrue(result['login_completed'])
                self.assertTrue(result['key_obtained'])
                self.assertFalse(result['configuration_written'])
                self.assertFalse(result['current_environment_loaded'])
                self.assertTrue(result['logout_confirmed'])
                self.assertEqual(sum(c[1] == '/api/auth/login' for c in api.calls), 1)
                self.assertEqual(any(c[1].endswith('/reveal') for c in api.calls), not new)

    def test_prepare_and_send_do_not_expose_credentials(self):
        for command, data, status in [(['prepare'], {}, 'prepared'),
                                     (None, inputs(), 'sms_sent')]:
            with self.subTest(status=status):
                code, result, _ = self.run_cli(FakeAPI(), data, command)
                self.assertEqual(code, 0)
                self.assertEqual(result['status'], status)

    def test_full_phone_matches_send_and_login_without_mask_collision(self):
        # These invented numbers share the same old masked representation.
        for phone in ('19900000001', '19999990001'):
            with self.subTest(phone=phone):
                api = LoginAPI()
                _, sent, _ = self.run_cli(api, inputs(phone=phone))
                _, verified, _ = self.run_cli(api, inputs(
                    action='verify', phone=phone, smsCode='012345'))
                self.assertEqual(sent['phone'], phone)
                self.assertEqual(verified['phone'], phone)
                requests = [c for c in api.calls if c[1] in (
                    '/api/auth/sms/send', '/api/auth/login')]
                self.assertEqual(len(requests), 2)
                self.assertTrue(all(c[2]['phone'] == phone for c in requests))

    def test_send_needs_no_protocol_versions_or_legal_requests(self):
        for extra in ({}, {'agreementVersion': 'old', 'privacyVersion': 'old'}):
            with self.subTest(extra=extra):
                api = FakeAPI()
                api.fail['/api/legal?type=TERMS'] = AssertionError('must not fetch legal')
                api.fail['/api/legal?type=PRIVACY'] = AssertionError('must not fetch legal')
                data = dict(action='send', phone='19900000001', consent=True, **extra)
                code, result, _ = self.run_cli(api, data)
                self.assertEqual(code, 0)
                self.assertEqual(result['status'], 'sms_sent')
                self.assertEqual(api.calls, [('POST', '/api/auth/sms/send',
                                             {'phone': data['phone']}, None)])

    def test_verify_fetches_required_versions_without_agent_input(self):
        for new in (True, False):
            with self.subTest(new=new):
                api = LoginAPI(new=new)
                data = inputs(action='verify', smsCode='001234')
                code, result, _ = self.run_cli(api, data)
                self.assertEqual(code, 0)
                self.assertEqual(result['api_key'], api.secret)
                login = next(c for c in api.calls if c[1] == '/api/auth/login')
                self.assertEqual(login[2], dict(phone=data['phone'], smsCode='001234',
                    agreementVersion='test-v1', privacyVersion='test-v1',
                    sourceCode=account.PACKAGE_SOURCE_CODE))
                self.assertEqual([c[1] for c in api.calls[:3]], [
                    '/api/legal?type=TERMS', '/api/legal?type=PRIVACY', '/api/auth/login'])
                self.assertEqual(sum(c[1] == '/api/auth/login' for c in api.calls), 1)
                self.assertNotIn('agreementVersion', result)
                self.assertNotIn('privacyVersion', result)

    def test_invalid_input_does_not_consume_sms(self):
        for changes, status in [({'phone': None}, 'phone_invalid'),
                                ({'consent': False}, 'consent_required'),
                                ({'smsCode': ''}, 'code_required')]:
            with self.subTest(status=status):
                api = LoginAPI()
                data = inputs(action='verify', smsCode='012345')
                data.update(changes)
                code, result, _ = self.run_cli(api, data)
                self.assertEqual(code, 1)
                self.assertEqual(result['status'], status)
                self.assertFalse(any(c[0] == 'POST' for c in api.calls))

    def test_login_failure_and_unknown_are_not_retried(self):
        for status in ('sms_invalid', 'result_unknown', 'request_failed'):
            with self.subTest(status=status):
                api = LoginAPI()
                api.fail['/api/auth/login'] = account.AccountError(status)
                code, result, _ = self.run_cli(api)
                self.assertEqual(code, 1)
                self.assertEqual(result['status'], status)
                self.assertEqual(result['stage'], 'login')
                self.assertEqual(sum(c[1] == '/api/auth/login' for c in api.calls), 1)

    def test_reveal_failure_keeps_login_separate_and_logs_out(self):
        api = LoginAPI(new=False)
        api.fail['/api/api-keys/7/reveal'] = account.AccountError('result_unknown')
        code, result, _ = self.run_cli(api)
        self.assertEqual(code, 1)
        self.assertEqual(result['stage'], 'key')
        self.assertTrue(result['login_completed'])
        self.assertFalse(result['configuration_written'])
        self.assertTrue(result['logout_confirmed'])

    def test_disabled_or_masked_key_is_never_returned(self):
        for invalid in ('disabled', 'masked'):
            with self.subTest(invalid=invalid):
                api = LoginAPI()
                if invalid == 'disabled':
                    api.key_status = 'DISABLED'
                else:
                    api.secret = 'qlm_abc****defghijklmnop'
                code, result, _ = self.run_cli(api)
                self.assertEqual(code, 1)
                self.assertEqual(result['status'], 'key_unavailable')

    def test_balance_and_logout_errors_do_not_discard_obtained_key(self):
        api = LoginAPI()
        api.fail['/api/points/account'] = account.AccountError('request_failed')
        api.fail['/api/auth/logout'] = account.AccountError('result_unknown')
        code, result, _ = self.run_cli(api)
        self.assertEqual(code, 0)
        self.assertEqual(result['api_key'], api.secret)
        self.assertFalse(result['balance_available'])
        self.assertFalse(result['logout_confirmed'])

    def test_cancellation_never_prints_key_or_claims_save(self):
        for path in ('/api/auth/login', '/api/points/account', '/api/auth/logout'):
            with self.subTest(path=path):
                api = LoginAPI()
                api.fail[path] = KeyboardInterrupt()
                code, result, _ = self.run_cli(api)
                self.assertEqual(code, 1)
                self.assertEqual(result['status'], 'cancelled')
                self.assertFalse(result['configuration_written'])

    def test_unexpected_local_error_is_sanitized(self):
        api = LoginAPI()
        api.fail['/api/points/account'] = RuntimeError(api.secret + api.token)
        code, result, _ = self.run_cli(api)
        self.assertEqual(code, 1)
        self.assertEqual(result['status'], 'operation_failed')
        self.assertEqual(api.calls[-1][1], '/api/auth/logout')

    def test_extra_auth_fields_are_not_forwarded(self):
        api = LoginAPI()
        original = api.request
        def decorated(*args, **kwargs):
            value = original(*args, **kwargs)
            if isinstance(value, dict):
                value['debug_raw'] = 'private-auth-payload'
            return value
        api.request = decorated
        _, result, text = self.run_cli(api)
        self.assertEqual(result['api_key'], api.secret)
        self.assertNotIn('private-auth-payload', text)
        self.assertNotIn('debug_raw', result)

    def test_cli_subprocess_finishes_without_credential_pipe(self):
        child_code = '''import sys, socket
sys.path.insert(0, sys.argv[1])
from test_account_flow import account, LoginAPI
def no_network(*args, **kwargs):
    raise AssertionError('network disabled')
socket.create_connection = no_network
account.AccountAPI = LoginAPI
sys.argv = ['account', 'register', '--input-stdin']
raise SystemExit(account.main())
'''
        child = subprocess.run([sys.executable, '-c', child_code, str(Path(__file__).parent)],
                               input=json.dumps(inputs(action='verify', smsCode='012345')),
                               capture_output=True, text=True, timeout=10)
        self.assertEqual(child.returncode, 0, child.stderr)
        self.assertEqual(child.stderr, '')
        result = json.loads(child.stdout)
        self.assertEqual(result['status'], 'credential_available')
        self.assertTrue(account.valid_key(result['api_key']))

    def test_both_key_origins_share_fixture_save_read_and_fresh_process_load(self):
        api = LoginAPI()
        _, result, _ = self.run_cli(api)
        # A deterministic platform fixture, NOT a new production credential store.
        # The first save fails; reusing the result must not require another login.
        with tempfile.TemporaryDirectory() as directory:
            settings = Path(directory) / 'existing-platform-settings.json'
            settings.write_text(json.dumps({'unrelated': 1, 'env': {'OTHER': 'retained'}}))
            def save(key):
                values = json.loads(settings.read_text())
                values['env']['QIANLIMA_API_KEY'] = key
                settings.write_text(json.dumps(values))
                self.assertEqual(json.loads(settings.read_text())['env']['QIANLIMA_API_KEY'], key)
            original = settings.read_text()
            with patch.object(Path, 'write_text', side_effect=PermissionError):
                with self.assertRaises(PermissionError):
                    save(result['api_key'])
            self.assertEqual(settings.read_text(), original)
            for key in (result['api_key'], api.secret):  # login result / user-supplied
                save(key)
                fresh_env = dict(os.environ)
                fresh_env.pop('QIANLIMA_API_KEY', None)
                loader = '''import json, os, subprocess, sys
values = json.load(open(sys.argv[1]))
assert values['unrelated'] == 1 and values['env']['OTHER'] == 'retained'
env = dict(os.environ, **values['env'])
subprocess.run([sys.executable, '-c',
    'import os; assert os.environ["QIANLIMA_API_KEY"].startswith("qlm_"); print("loaded")'],
    env=env, check=True)
'''
                child = subprocess.run([sys.executable, '-c', loader, str(settings)],
                                       env=fresh_env, capture_output=True, text=True, timeout=10)
                self.assertEqual(child.returncode, 0, child.stderr)
                self.assertEqual(child.stdout.strip(), 'loaded')
                self.assertNotIn(key, child.stdout + child.stderr)
        self.assertEqual(sum(c[1] == '/api/auth/login' for c in api.calls), 1)


if __name__ == '__main__':
    unittest.main()
