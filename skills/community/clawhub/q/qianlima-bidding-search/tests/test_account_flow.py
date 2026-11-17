"""Account tests use invented identities and injected services; never send SMS."""
import json
import os
from pathlib import Path
import sys
import secrets
import shutil
import subprocess
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch
import io
import hashlib
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import qianlima_account as account


class FakeAPI:
    def __init__(self):
        self.calls = []
        self.fail = {}

    def request(self, method, path, body=None, token=None):
        self.calls.append((method, path, body, token))
        if path in self.fail:
            raise self.fail[path]
        if path.startswith('/api/legal'):
            return {'version': 'test-v1', 'content': 'Test agreement'}
        return None


def inputs(**changes):
    data = dict(action='send', phone='19900000001', consent=True)
    data.update(changes)
    return data


class LoginAPI(FakeAPI):
    def __init__(self, new=True, balance=500):
        super().__init__()
        self.secret = 'qlm_' + 'test_only_' + 'a' * 24
        self.token = 'test_only_access_token'
        self.new = new
        self.balance = balance
        self.key_status = 'ACTIVE'

    def request(self, method, path, body=None, token=None):
        result = super().request(method, path, body, token)
        if path == '/api/auth/login':
            return dict(accessToken=self.token, newUser=self.new,
                        defaultApiKey=dict(keyId=7, status=self.key_status,
                                           apiKey=self.secret if self.new else None))
        if path.endswith('/reveal'):
            return dict(keyId=7, status=self.key_status, apiKey=self.secret)
        if path == '/api/points/account':
            return dict(availablePoints=self.balance, welcomeStatus='NEW_GRANT', welcomePoints=500)
        return result


class FakeConfig:
    def __init__(self):
        self.value = 'old-test-value'
        self.writes = 0
        self.fail = None

    def preflight(self, version, replace):
        if self.fail:
            raise account.AccountError(self.fail, 'configuration')

    def save(self, key, version, replace):
        self.value = key
        self.writes += 1


class LoginTests(unittest.TestCase):
    def run_flow(self, api=None, config=None):
        api = api or LoginAPI()
        config = config or FakeConfig()
        return account.register(inputs(action='verify', smsCode='012345', configVersion='fake-v',
                                       replaceConfirmed=True), api, config)

    def test_new_and_existing_reveal_and_zero_balance(self):
        for new, balance in [(True, 500), (False, 17), (False, 0)]:
            with self.subTest(new=new, balance=balance):
                api, config = LoginAPI(new, balance), FakeConfig()
                result = self.run_flow(api, config)
                self.assertEqual(result['status'], 'configuration_saved')
                self.assertEqual(result['available_points'], balance)
                self.assertEqual(result['new_user'], new)
                self.assertEqual(result['welcome_granted'], new)
                self.assertEqual(config.value, api.secret)
                paths = [c[1] for c in api.calls]
                self.assertEqual('/api/api-keys/7/reveal' in paths, not new)
                self.assertLess(paths.index('/api/points/account'), paths.index('/api/auth/logout'))
                self.assertEqual(paths[-1], '/api/auth/logout')
                for secret in [api.secret, api.token, '012345']:
                    self.assertNotIn(secret, json.dumps(result))

    def test_balance_failure_or_missing_never_invents_balance(self):
        for balance in [None, False, '500']:
            result = self.run_flow(LoginAPI(balance=balance))
            self.assertEqual(result['status'], 'configuration_saved')
            self.assertFalse(result['balance_available'])
            self.assertNotIn('available_points', result)
        api = LoginAPI()
        api.fail['/api/points/account'] = account.AccountError('result_unknown')
        self.assertEqual(self.run_flow(api)['status'], 'configuration_saved')

    def test_key_failure_logs_out_without_overwrite(self):
        api, config = LoginAPI(False), FakeConfig()
        api.fail['/api/api-keys/7/reveal'] = account.AccountError('request_failed')
        result = self.run_flow(api, config)
        self.assertEqual(result['stage'], 'key')
        self.assertEqual(config.writes, 0)
        self.assertEqual(api.calls[-1][1], '/api/auth/logout')

    def test_unavailable_key_never_enabled_or_created(self):
        for status in ['DISABLED', 'DELETED', None]:
            api, config = LoginAPI(), FakeConfig()
            api.key_status = status
            result = self.run_flow(api, config)
            self.assertEqual(result['status'], 'key_unavailable')
            self.assertEqual(config.writes, 0)
            self.assertFalse(any('/api/api-keys' in c[1] for c in api.calls))

    def test_login_timeout_not_replayed(self):
        api = LoginAPI()
        api.fail['/api/auth/login'] = account.AccountError('result_unknown')
        result = self.run_flow(api)
        self.assertEqual(result['stage'], 'login')
        self.assertEqual(sum(c[1] == '/api/auth/login' for c in api.calls), 1)

    def test_config_preflight_fails_before_consuming_sms(self):
        api, config = LoginAPI(), FakeConfig()
        config.fail = 'configuration_changed'
        result = self.run_flow(api, config)
        self.assertEqual(result['status'], 'configuration_changed')
        self.assertFalse(any(c[0] == 'POST' for c in api.calls))

    def test_logout_failure_does_not_undo_saved_key(self):
        api = LoginAPI()
        api.fail['/api/auth/logout'] = account.AccountError('result_unknown')
        result = self.run_flow(api)
        self.assertEqual(result['status'], 'configuration_saved')
        self.assertFalse(result['logout_confirmed'])

    def test_save_failure_and_unknown_write_keep_actual_state(self):
        for written in (False, None, True):
            config = FakeConfig()
            config.written = written
            with patch.object(config, 'save', side_effect=account.AccountError('configuration_write_failed')):
                result = self.run_flow(config=config)
            self.assertEqual(result['configuration_written'], written)
            self.assertEqual(result['stage'], 'configuration')
            self.assertTrue(result['logout_confirmed'])

    def test_missing_gift_evidence_and_masked_key(self):
        api = LoginAPI()
        original = api.request
        def missing_gift(method, path, body=None, token=None):
            value = original(method, path, body, token)
            if path == '/api/points/account':
                value.pop('welcomeStatus')
            return value
        api.request = missing_gift
        self.assertFalse(self.run_flow(api)['welcome_granted'])
        api = LoginAPI()
        api.secret = 'qlm_abc****defghijklmnop'
        self.assertEqual(self.run_flow(api)['status'], 'key_unavailable')

    def test_full_key_without_token_can_configure_but_no_balance_or_logout(self):
        api = LoginAPI()
        api.token = None
        result = self.run_flow(api)
        self.assertEqual(result['status'], 'configuration_saved')
        self.assertTrue(result['key_obtained'])
        self.assertFalse(result['balance_available'])
        self.assertFalse(result['logout_confirmed'])
        self.assertFalse(any(c[1] in ('/api/points/account', '/api/auth/logout') for c in api.calls))
        api = LoginAPI(False)
        api.token = None
        self.assertEqual(self.run_flow(api)['status'], 'key_unavailable')

    def test_cli_uses_stdin_and_safe_results(self):
        api, config = LoginAPI(), FakeConfig()
        config.close = lambda: None
        with patch.object(account, 'CodexConfig', return_value=config), patch.object(account, 'AccountAPI', return_value=api), \
             patch.object(sys, 'argv', ['qianlima_account.py', 'register', '--input-stdin']), \
             patch.object(sys, 'stdin', io.StringIO(json.dumps(inputs(action='verify', smsCode='012345')))), \
             patch.object(sys, 'stdout', io.StringIO()) as output:
            self.assertEqual(account.main(config_factory=account.CodexConfig), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result['status'], 'configuration_saved')
        for secret in [api.secret, api.token, '012345']:
            self.assertNotIn(secret, output.getvalue())

    def test_missing_or_invalid_default_key_id_stops_before_reveal(self):
        for key_id in (None, 0, -1, True, '7', 7.5, [], {}):
            with self.subTest(key_id=key_id):
                api, config = LoginAPI(False), FakeConfig()
                original = api.request
                def respond(method, path, body=None, token=None):
                    value = original(method, path, body, token)
                    if path == '/api/auth/login':
                        if key_id is None:
                            value['defaultApiKey'].pop('keyId')
                        else:
                            value['defaultApiKey']['keyId'] = key_id
                    return value
                with patch.object(api, 'request', side_effect=respond):
                    result = self.run_flow(api, config)
                self.assertEqual(result['status'], 'key_unavailable')
                self.assertEqual(result['stage'], 'key')
                self.assertEqual(config.writes, 0)
                self.assertEqual([c[1] for c in api.calls], [
                    '/api/legal?type=TERMS', '/api/legal?type=PRIVACY', '/api/auth/login', '/api/auth/logout'])

    def test_reveal_invalid_results_and_timeout_never_save_or_retry(self):
        valid = LoginAPI().secret
        cases = [None, {}, [], {'keyId': 8, 'status': 'ACTIVE', 'apiKey': valid},
                 {'keyId': 7, 'status': 'ACTIVE'},
                 {'keyId': 7, 'status': 'ACTIVE', 'apiKey': ''},
                 {'keyId': 7, 'status': 'DISABLED', 'apiKey': valid},
                 account.AccountError('result_unknown')]
        for index, response in enumerate(cases):
            with self.subTest(case=index):
                api, config = LoginAPI(False), FakeConfig()
                original = api.request
                def respond(method, path, body=None, token=None):
                    value = original(method, path, body, token)
                    if path.endswith('/reveal'):
                        if isinstance(response, Exception):
                            raise response
                        return response
                    return value
                with patch.object(api, 'request', side_effect=respond):
                    result = self.run_flow(api, config)
                expected = 'result_unknown' if isinstance(response, Exception) else 'key_unavailable'
                self.assertEqual(result['status'], expected)
                self.assertEqual(result['stage'], 'key')
                self.assertEqual(config.writes, 0)
                self.assertEqual(config.value, 'old-test-value')
                self.assertTrue(result['logout_confirmed'])
                self.assertEqual([c[1] for c in api.calls], [
                    '/api/legal?type=TERMS', '/api/legal?type=PRIVACY', '/api/auth/login', '/api/api-keys/7/reveal', '/api/auth/logout'])

    def test_missing_points_data_and_business_failure_keep_saved_key(self):
        for response in (None, {}, account.AccountError('request_failed')):
            with self.subTest(kind=type(response).__name__):
                api, config = LoginAPI(), FakeConfig()
                original = api.request
                def respond(method, path, body=None, token=None):
                    value = original(method, path, body, token)
                    if path == '/api/points/account':
                        if isinstance(response, Exception):
                            raise response
                        return response
                    return value
                with patch.object(api, 'request', side_effect=respond):
                    result = self.run_flow(api, config)
                self.assertEqual(result['status'], 'configuration_saved')
                self.assertFalse(result['balance_available'])
                self.assertFalse(result['welcome_granted'])
                self.assertNotIn('available_points', result)
                self.assertEqual(config.value, api.secret)
                self.assertEqual(config.writes, 1)
                self.assertEqual([c[1] for c in api.calls][-2:],
                                 ['/api/points/account', '/api/auth/logout'])

    def test_gift_requires_all_evidence_and_preserves_actual_balance(self):
        cases = [({}, True), ({'welcomePoints': None}, False),
                 ({'welcomePoints': 0}, False), ({'welcomePoints': 499}, False),
                 ({'welcomePoints': '500'}, False), ({'welcomeStatus': None}, False),
                 ({'welcomeStatus': 'ALREADY_GRANTED'}, False)]
        for new in (True, False):
            for changes, granted in cases:
                with self.subTest(new=new, changes=changes):
                    api = LoginAPI(new, balance=17)
                    original = api.request
                    def respond(method, path, body=None, token=None):
                        value = original(method, path, body, token)
                        if path == '/api/points/account':
                            for k, v in changes.items():
                                if v is None:
                                    value.pop(k)
                                else:
                                    value[k] = v
                        return value
                    with patch.object(api, 'request', side_effect=respond):
                        result = self.run_flow(api)
                    self.assertEqual(result['welcome_granted'], new and granted)
                    self.assertEqual(result['available_points'], 17)
                    self.assertEqual(result['status'], 'configuration_saved')

    def test_unknown_auth_fields_do_not_escape_cli_outputs(self):
        marker = 'unknown-auth-' + secrets.token_hex(16)
        api, config = LoginAPI(False), FakeConfig()
        original = api.request
        def respond(method, path, body=None, token=None):
            value = original(method, path, body, token)
            if isinstance(value, dict):
                value['unknown'] = {'nested': [marker, api.secret, api.token]}
            return value
        config.close = lambda: None
        output, errors = io.StringIO(), io.StringIO()
        with patch.object(api, 'request', side_effect=respond), \
             patch.object(account, 'CodexConfig', return_value=config), \
             patch.object(account, 'AccountAPI', return_value=api), \
             patch.object(sys, 'argv', ['account', 'register', '--input-stdin']), \
             patch.object(sys, 'stdin', io.StringIO(json.dumps(inputs(action='verify', smsCode='012345')))), \
             patch.object(sys, 'stdout', output), patch.object(sys, 'stderr', errors):
            self.assertEqual(account.main(config_factory=account.CodexConfig), 0)
        self.assertEqual(json.loads(output.getvalue())['status'], 'configuration_saved')
        self.assertEqual(errors.getvalue(), '')
        for secret in (marker, api.secret, api.token, '012345'):
            self.assertNotIn(secret, output.getvalue())
        self.assertNotIn('api_responses', json.loads(output.getvalue()))


class TransportTests(unittest.TestCase):
    def test_business_codes_do_not_leak_response_or_retry(self):
        for code, expected in [(0, None), (40101, 'sms_invalid'), (20003, 'account_disabled'),
                               (20002, 'rate_limited'), (50000, 'request_failed'), (200, 'request_failed')]:
            payload = dict(code=code, data=None, message='test-secret-must-not-leak')
            fake = unittest.mock.MagicMock()
            fake.open.return_value.__enter__.return_value.read.return_value = json.dumps(payload).encode()
            with patch.object(account.request, 'build_opener', return_value=fake):
                if expected:
                    with self.assertRaises(account.AccountError) as ctx:
                        account.AccountAPI().request('POST', '/api/auth/sms/send', {'phone': '19900000001'})
                    self.assertEqual(ctx.exception.status, expected)
                    self.assertNotIn('test-secret', str(ctx.exception))
                else:
                    self.assertIsNone(account.AccountAPI().request('POST', '/api/auth/sms/send'))
            self.assertEqual(fake.open.call_count, 1)

    def test_redirect_has_no_forward_request(self):
        self.assertIsNone(account.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://invalid.example'))

    def test_unknown_timeout_and_malformed_response(self):
        for content, expected in [(b'not json', 'invalid_response'), (b'[]', 'invalid_response'),
                                  (b'{"code":true}', 'invalid_response')]:
            fake = unittest.mock.MagicMock()
            fake.open.return_value.__enter__.return_value.read.return_value = content
            with patch.object(account.request, 'build_opener', return_value=fake), self.assertRaises(account.AccountError) as ctx:
                account.AccountAPI().request('POST', '/api/auth/login')
            self.assertEqual(ctx.exception.status, expected)
        fake.open.side_effect = TimeoutError('test-secret')
        with patch.object(account.request, 'build_opener', return_value=fake), self.assertRaises(account.AccountError) as ctx:
            account.AccountAPI().request('POST', '/api/auth/login')
        self.assertEqual(ctx.exception.status, 'result_unknown')

    def test_guide_adapts_without_query_and_without_sms(self):
        result = account.prepare(FakeAPI(), pending_query=False, has_key=True)
        self.assertNotIn('继续查询', result['guidance'])
        self.assertNotIn('还没有配置', result['guidance'])
        self.assertTrue(result['guidance'].startswith('**千里马AI 数据平台**'))
        self.assertEqual(set(result), {'status', 'guidance'})

    def test_connection_errors_and_wrapped_timeouts_are_classified_once(self):
        from urllib.error import URLError, HTTPError
        cases = [(URLError(ConnectionRefusedError('synthetic-secret')), 'request_failed'),
                 (URLError(TimeoutError('synthetic-secret')), 'result_unknown'),
                 (TimeoutError('synthetic-secret'), 'result_unknown'),
                 (HTTPError('https://invalid.test', 429, 'synthetic-secret', {}, None), 'rate_limited'),
                 (HTTPError('https://invalid.test', 503, 'synthetic-secret', {}, None), 'request_failed')]
        for failure, expected in cases:
            for path in ('/api/auth/sms/send', '/api/auth/login'):
                with self.subTest(kind=type(failure).__name__, path=path):
                    opener = unittest.mock.MagicMock()
                    opener.open.side_effect = failure
                    with patch.object(account.request, 'build_opener', return_value=opener):
                        with self.assertRaises(account.AccountError) as caught:
                            account.AccountAPI().request('POST', path, {'phone': '19900000001'})
                    self.assertEqual(caught.exception.status, expected)
                    self.assertNotIn('synthetic-secret', str(caught.exception))
                    opener.open.assert_called_once()

    def test_login_business_rejection_stops_entire_registration_chain(self):
        for code, status in ((40101, 'sms_invalid'), (20003, 'account_disabled'),
                             (40100, 'login_rejected'), (50000, 'request_failed')):
            with self.subTest(code=code):
                calls = []
                def respond(opener, req, **kwargs):
                    calls.append(req.full_url)
                    result = ({'code': 0, 'data': {'version': 'test-v1'}}
                              if '/api/legal?' in req.full_url else
                              {'code': code, 'message': 'secret-rejection',
                               'data': {'unknown': 'secret-rejection'}})
                    return io.BytesIO(json.dumps(result).encode())
                config = FakeConfig()
                with patch.object(account.request.OpenerDirector, 'open', respond):
                    result = account.register(inputs(action='verify', smsCode='012345'),
                                              account.AccountAPI(), config)
                self.assertEqual(result['status'], status)
                self.assertEqual(result['stage'], 'login')
                self.assertFalse(result['configuration_written'])
                self.assertEqual(config.writes, 0)
                self.assertEqual(config.value, 'old-test-value')
                self.assertEqual(calls, [account.ACCOUNT_BASE_URL + p for p in (
                    '/api/legal?type=TERMS', '/api/legal?type=PRIVACY', '/api/auth/login',)])
                self.assertNotIn('secret-rejection', json.dumps(result))

    def test_account_bearer_headers_use_current_login_token_only(self):
        for new in (True, False):
            with self.subTest(new=new):
                api, config = LoginAPI(new), FakeConfig()
                seen = []
                def respond(opener, req, **kwargs):
                    path = req.full_url.removeprefix(account.ACCOUNT_BASE_URL)
                    needs_token = path in ('/api/api-keys/7/reveal', '/api/points/account', '/api/auth/logout')
                    self.assertEqual(req.get_header('Authorization'),
                                     'Bearer ' + api.token if needs_token else None)
                    self.assertIsNone(req.get_header('Qianlimaapikey'))
                    self.assertEqual(req.get_header('Content-type'), 'application/json')
                    seen.append(path)
                    body = json.loads(req.data) if req.data else None
                    value = api.request(req.get_method(), path, body,
                                        api.token if needs_token else None)
                    return io.BytesIO(json.dumps({'code': 0, 'data': value}).encode())
                with patch.object(account.request.OpenerDirector, 'open', respond):
                    result = account.register(inputs(action='verify', smsCode='012345'),
                                              account.AccountAPI(), config)
                self.assertEqual(result['status'], 'configuration_saved')
                self.assertEqual(seen, ['/api/legal?type=TERMS', '/api/legal?type=PRIVACY', '/api/auth/login'] + ([] if new else ['/api/api-keys/7/reveal']) +
                                      ['/api/points/account', '/api/auth/logout'])


@unittest.skipUnless(os.environ.get('QLM_CODEX_TEST_BINARY'), 'opt-in isolated native Codex test')
class NativeCodexTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='qlm-native-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.home = self.root / 'codex-home'
        self.home.mkdir(mode=0o700)
        self.config_file = self.home / 'config.toml'
        self.config_file.write_text('model_reasoning_effort = "low"\n')
        self.config_file.chmod(0o600)
        self.binary = os.environ['QLM_CODEX_TEST_BINARY']
        self.config = account.CodexConfig(self.home, self.binary, self.root)
        self.addCleanup(self.config.close)
        self.key = 'qlm_' + secrets.token_hex(16)

    def save(self):
        self.config.save(self.key, self.config.metadata()['configVersion'], False)

    def test_native_save_load_lifecycle_and_other_settings(self):
        self.save()
        self.assertEqual(self.config.snapshot()[1], self.key)
        self.assertIn('model_reasoning_effort = "low"', self.config_file.read_text())
        self.assertEqual(self.config_file.stat().st_mode & 0o777, 0o600)
        # A separate native execution backend reads durable config on startup.
        backend = account.CodexRPC(self.home, self.binary)
        try:
            result = backend.call('command/exec', dict(command=[sys.executable, '-c',
                'import os,hashlib; print(hashlib.sha256(os.environ.get("QIANLIMA_API_KEY", "").encode()).hexdigest() == '
                + repr(hashlib.sha256(self.key.encode()).hexdigest()) + ')'],
                cwd=str(self.root), sandboxPolicy={'type': 'dangerFullAccess'}))
            self.assertEqual(result['stdout'].strip(), 'True')
            self.assertNotIn(self.key, json.dumps(result))
        finally:
            backend.close()

    def test_conflict_and_confirmed_replacement(self):
        version = self.config.metadata()['configVersion']
        self.save()
        with self.assertRaises(account.AccountError):
            self.config.save('qlm_' + secrets.token_hex(16), version, True)
        version = self.config.metadata()['configVersion']
        with self.assertRaises(account.AccountError):
            self.config.save('qlm_' + secrets.token_hex(16), version, False)
        other = 'qlm_' + secrets.token_hex(16)
        self.config.save(other, version, True)
        self.assertTrue(self.config.snapshot()[1] == other)

    def test_initially_absent_config_and_symlink_refusal(self):
        self.config.close()
        self.config_file.unlink()
        config = account.CodexConfig(self.home, self.binary, self.root)
        try:
            config.save(self.key, config.metadata()['configVersion'], False)
            self.assertTrue(config.snapshot()[1] == self.key)
        finally:
            config.close()
        self.config_file.unlink()
        target = self.root / 'unrelated.toml'
        target.write_text('')
        self.config_file.symlink_to(target)
        with self.assertRaises(account.AccountError):
            account.CodexConfig(self.home, self.binary, self.root)
        self.assertEqual(target.read_text(), '')

    def test_no_stdout_or_file_secret_export(self):
        self.save()
        for fd in [1, 2]:
            with self.assertRaises(account.AccountError):
                self.config.export_private(fd)
        with (self.root / 'not-a-pipe').open('wb') as f:
            with self.assertRaises(account.AccountError):
                self.config.export_private(f.fileno())
        reader, writer = os.pipe()
        try:
            self.config.export_private(writer)
            os.close(writer)
            writer = None
            self.assertTrue(os.read(reader, 1024).decode() == self.key)
        finally:
            os.close(reader)
            if writer is not None:
                os.close(writer)

    def test_immediate_shell_reload_after_existing_engine_and_update(self):
        root = Path(__file__).resolve().parents[1]
        # Keep an engine that was started before account configuration to test refresh.
        backend = account.CodexRPC(self.home, self.binary)
        try:
            self.save()
            for n in range(2):
                copy = self.root / ('install-' + str(n))
                shutil.copytree(root / 'scripts', copy / 'scripts', ignore=shutil.ignore_patterns('__pycache__'))
                # Refresh only the current command environment, never run a query wrapper.
                script = ('set +x\nexport CODEX_HOME="$1"\n'
                    'qlm_key="$("$2" -c \'import sys; sys.path.insert(0,sys.argv[1]+"/scripts"); import qianlima_account as a; a.CodexConfig().export_private(3)\' "$3" 3>&1 1>/dev/null)" || exit 1\n'
                    'export QIANLIMA_API_KEY="$qlm_key"\nunset qlm_key\n'
                    '"$2" -c \'import os; print(bool(os.environ.get("QIANLIMA_API_KEY")))\'')
                result = backend.call('command/exec', dict(command=['/bin/sh', '-c', script,
                    'qlm-test', str(self.home), sys.executable, str(copy)], cwd=str(self.root),
                    sandboxPolicy={'type': 'dangerFullAccess'}))
                self.assertEqual(result['exitCode'], 0, result)
                self.assertEqual(result['stdout'].strip(), 'True')
                self.assertNotIn(self.key, json.dumps(result))
                self.assertFalse(any(self.key.encode() in p.read_bytes() for p in copy.rglob('*') if p.is_file()))
            for p in self.home.rglob('*'):
                if p.is_file() and p != self.config_file:
                    self.assertNotIn(self.key.encode(), p.read_bytes(), str(p))
        finally:
            backend.close()

    def test_native_written_but_readback_mismatch_reports_actual_state(self):
        api = LoginAPI()
        version = self.config.metadata()['configVersion']
        snapshot = self.config.snapshot
        def mismatched_readback():
            current, key = snapshot()
            return current, 'synthetic-other-key' if self.config.written is True else key
        with patch.object(self.config, 'snapshot', side_effect=mismatched_readback):
            result = account.register(inputs(action='verify', smsCode='012345', configVersion=version),
                                      api, self.config)
        self.assertEqual(result['status'], 'configuration_written_not_loaded')
        self.assertTrue(result['configuration_written'])
        self.assertNotIn('current_environment_loaded', result)
        self.assertEqual(self.config.snapshot()[1], api.secret)
        self.assertEqual(self.config_file.stat().st_mode & 0o777, 0o600)
        self.assertNotIn(api.secret, json.dumps(result))
        self.assertTrue(result['logout_confirmed'])

    def test_registered_key_reaches_original_http_queries_and_cache_stays_clean(self):
        root = Path(__file__).resolve().parents[1]
        api = LoginAPI(False, 0)
        api.secret = self.key
        result = account.register(inputs(action='verify', smsCode='012345',
            configVersion=self.config.metadata()['configVersion']), api, self.config)
        self.assertEqual(result['status'], 'configuration_saved')
        received = []
        key = self.key
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass
            def answer(self, post=False):
                valid = self.headers.get('qianlimaApiKey') == key
                received.append((self.path, valid))
                if post:
                    query = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                    filename = 'search_page_' + str(query['currentPage']) + '.json'
                else:
                    filename = 'detail_101.json'
                body = (root / 'tests' / 'fixtures' / filename).read_bytes()
                self.send_response(200 if valid else 401)
                self.end_headers()
                self.wfile.write(body)
            def do_POST(self):
                self.answer(True)
            def do_GET(self):
                self.answer()
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        state = self.root / 'query-state'
        env = {k: v for k, v in os.environ.items() if not k.startswith(('QIANLIMA_', 'CODEX_'))}
        env.update(CODEX_HOME=str(self.home), QIANLIMA_SKILL_STATE_DIR=str(state))
        command = ('set +x\nqlm_key="$("$1" -c \'import sys; sys.path.insert(0,sys.argv[1]+"/scripts"); import qianlima_account as a; a.CodexConfig().export_private(3)\' "$2" 3>&1 1>/dev/null)" || exit 1\n'
                   'export QIANLIMA_API_KEY="$qlm_key"\nunset qlm_key\n'
                   'qlm_python="$1"; qlm_root="$2"; shift 2\n'
                   '"$qlm_python" "$qlm_root/scripts/qianlima_skill.py" "$@"')
        def query(*args):
            proc = subprocess.run(['/bin/sh', '-c', command, 'qlm-test', sys.executable, str(root),
                '--base-url', f'http://127.0.0.1:{server.server_port}', *args],
                env=env, capture_output=True, text=True, timeout=30)
            self.assertNotIn(key, proc.stdout + proc.stderr)
            self.assertEqual(proc.returncode, 0, proc.stdout)
            return json.loads(proc.stdout)
        try:
            first = query('search', '--query-json', json.dumps({'keywordGroups': [{'keywords': ['测试'], 'matchScopes': [2]}], 'numPerPage': 2}))
            follow = first['follow_up']
            second = query('next', '--session-id', follow['session_id'], '--result-set-id', follow['result_set_id'])
            self.assertEqual(second['request_query']['currentPage'], 2)
            self.assertTrue(query('detail', '--id', '101')['ok'])
            self.assertEqual(len(received), 3)
            self.assertTrue(all(ok for _, ok in received))
            self.assertEqual(sum(c[1] == '/api/auth/login' for c in api.calls), 1)
            for file in state.rglob('*'):
                if file.is_file():
                    self.assertNotIn(key.encode(), file.read_bytes())
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


class SendTests(unittest.TestCase):
    def setUp(self):
        self.api = FakeAPI()

    def test_preparation_is_readonly_and_has_single_guide(self):
        result = account.prepare(self.api)
        self.assertEqual(set(result), {'status', 'guidance'})
        self.assertIn('[前往官网](https://ai.qianlima.com/?source=', result['guidance'])
        self.assertEqual(self.api.calls, [])

    def test_send_accepts_null_data_and_returns_full_phone(self):
        result = account.register(inputs(), self.api)
        self.assertEqual(result['status'], 'sms_sent')
        self.assertEqual(result['phone'], '19900000001')
        self.assertNotIn('phone_masked', result)
        self.assertEqual(result['expires_in_seconds'], 600)
        self.assertEqual(self.api.calls[-1][2], {'phone': '19900000001'})

    def test_no_implicit_send_or_consent(self):
        for changes in [dict(action=''), dict(consent=False), dict(phone='bad'),
                        dict(action='verify', smsCode='')]:
            with self.subTest(changes=changes):
                self.api.calls.clear()
                result = account.register(inputs(**changes), self.api)
                self.assertNotEqual(result['status'], 'sms_sent')
                self.assertFalse(any(c[0] == 'POST' for c in self.api.calls))

    def test_login_uses_script_versions_instead_of_legacy_inputs(self):
        api = LoginAPI()
        result = account.register(inputs(action='verify', smsCode='012345',
                                          agreementVersion='old-terms', privacyVersion='old-privacy'), api)
        self.assertEqual(result['status'], 'credential_available')
        login = next(c for c in api.calls if c[1] == '/api/auth/login')
        self.assertEqual(login[2]['agreementVersion'], 'test-v1')
        self.assertEqual(login[2]['privacyVersion'], 'test-v1')
        self.assertEqual(sum(c[1].startswith('/api/legal') for c in api.calls), 2)

    def test_script_maps_distinct_backend_versions_to_login_fields(self):
        api = LoginAPI()
        original = api.request
        def request(method, path, body=None, token=None):
            result = original(method, path, body, token)
            if path == '/api/legal?type=TERMS':
                return {'version': 'terms-current'}
            if path == '/api/legal?type=PRIVACY':
                return {'version': 'privacy-current'}
            return result
        with patch.object(api, 'request', side_effect=request):
            result = account.register(inputs(action='verify', smsCode='001234'), api)
        self.assertEqual(result['status'], 'credential_available')
        login = next(c for c in api.calls if c[1] == '/api/auth/login')
        self.assertEqual(login[2], dict(phone='19900000001', smsCode='001234',
            agreementVersion='terms-current', privacyVersion='privacy-current',
            sourceCode=account.PACKAGE_SOURCE_CODE))

    def test_legal_failure_stops_before_login_without_writing_configuration(self):
        for kind in ('TERMS', 'PRIVACY'):
            api, config = LoginAPI(), FakeConfig()
            api.fail[f'/api/legal?type={kind}'] = account.AccountError('request_failed')
            result = account.register(inputs(action='verify', smsCode='012345'), api, config)
            self.assertEqual(result['status'], 'request_failed')
            self.assertEqual(result['stage'], 'legal')
            self.assertFalse(any(c[0] == 'POST' for c in api.calls))
            self.assertEqual(config.writes, 0)
            self.assertEqual(config.value, 'old-test-value')

    def test_existing_config_is_confirmed_before_send(self):
        config = FakeConfig()
        config.fail = 'replacement_confirmation_required'
        result = account.register(inputs(), self.api, config)
        self.assertEqual(result['status'], 'replacement_confirmation_required')
        self.assertFalse(any(c[0] == 'POST' for c in self.api.calls))

    def test_failure_limit_timeout_are_distinct_without_retry(self):
        for status in ['request_failed', 'rate_limited', 'result_unknown']:
            self.api.calls.clear()
            self.api.fail['/api/auth/sms/send'] = account.AccountError(status)
            result = account.register(inputs(), self.api)
            self.assertEqual(result['status'], status)
            self.assertEqual(result['stage'], 'sms')
            self.assertEqual(sum(c[0] == 'POST' for c in self.api.calls), 1)


class InputContractTests(unittest.TestCase):
    def test_optional_consent_and_code_alias_reach_backend_unchanged(self):
        for consent in ({}, {'consent': True}):
            for code in ({'smsCode': '012345'}, {'code': '012345'},
                         {'smsCode': '012345', 'code': '012345'}):
                with self.subTest(consent=consent, code=code):
                    api = LoginAPI()
                    data = dict(action='verify', phone='19900000001', **code, **consent)
                    original = dict(data)
                    result = account.register(data, api)
                    self.assertEqual(result['status'], 'credential_available')
                    login = next(c[2] for c in api.calls if c[1] == '/api/auth/login')
                    self.assertEqual(login['smsCode'], '012345')
                    self.assertNotIn('code', login)
                    self.assertNotIn('consent', login)
                    self.assertEqual(data, original)
                    self.assertFalse(any(c[1] == '/api/auth/sms/send' for c in api.calls))
        api = FakeAPI()
        result = account.register(dict(action='send', phone='19900000001'), api)
        self.assertEqual(result['status'], 'sms_sent')
        self.assertEqual(api.calls, [('POST', '/api/auth/sms/send', {'phone': '19900000001'}, None)])

    def test_input_errors_stop_before_api_and_configuration(self):
        cases = [({'smsCode': '012345', 'code': '654321'}, 'code_conflict'),
                 ({'code': 12345}, 'code_invalid'),
                 ({'code': '１２３４５６'}, 'code_invalid'),
                 ({'code': ''}, 'code_required'),
                 ({'code': '012345', 'consent': False}, 'consent_required'),
                 ({'code': '012345', 'consent': 'true'}, 'invalid_consent')]
        for fields, status in cases:
            with self.subTest(fields=fields):
                api, config = LoginAPI(), FakeConfig()
                with patch.object(config, 'preflight') as preflight:
                    result = account.register(dict(action='verify', phone='19900000001', **fields), api, config)
                    preflight.assert_not_called()
                self.assertEqual(result['status'], status)
                self.assertEqual(result['stage'], 'input')
                self.assertIs(result['request_sent'], False)
                self.assertTrue(result['agent_instruction'])
                self.assertEqual(api.calls, [])
                self.assertEqual(config.writes, 0)

    class Config(FakeConfig):
        def snapshot(self):
            return 'fake-v', None

        # Capture the real method before the CLI constructor is patched.
        preflight = account.CodexConfig.preflight

        def close(self):
            self.closed = True

    def invoke(self, data):
        api, config = LoginAPI(), self.Config()
        output, errors = io.StringIO(), io.StringIO()
        with patch.object(account, 'AccountAPI', return_value=api), \
             patch.object(account, 'CodexConfig', return_value=config), \
             patch.object(sys, 'argv', ['account', 'register', '--input-stdin']), \
             patch.object(sys, 'stdin', io.StringIO(json.dumps(data))), \
             patch.object(sys, 'stdout', output), patch.object(sys, 'stderr', errors):
            code = account.main(config_factory=account.CodexConfig)
        self.assertEqual(code, 1)
        self.assertEqual(errors.getvalue(), '')
        self.assertTrue(config.closed)
        self.assertEqual(config.writes, 0)
        self.assertEqual(config.value, 'old-test-value')
        self.assertFalse(any(c[0] == 'POST' for c in api.calls))
        self.assertNotIn('19900000001', output.getvalue())
        self.assertNotIn('012345', output.getvalue())
        return json.loads(output.getvalue()), api.calls

    def test_cli_required_fields_missing_for_send_and_verify(self):
        expected = {'action': 'invalid_input',
                    'phone': 'phone_invalid', 'smsCode': 'code_required',
                    'configVersion': 'configuration_changed'}
        for action in ('send', 'verify'):
            for field, status in expected.items():
                if action == 'send' and field == 'smsCode':
                    continue
                with self.subTest(action=action, missing=field):
                    data = inputs(action=action, smsCode='012345', configVersion='fake-v')
                    data.pop(field)
                    result, calls = self.invoke(data)
                    self.assertEqual(result['status'], status)
                    self.assertEqual(calls, [])

    def test_cli_wrong_phone_code_and_consent_types(self):
        for field, values, expected in (
            ('phone', [None, 19900000001, True, [], {}, '', '１２３４５６７８９０１'], 'phone_invalid'),
            ('smsCode', [None, ''], 'code_required'),
            ('smsCode', [1234, True, [], {}, '   ', '1234', '1234567', '１２３４５６', '١٢٣٤٥٦'], 'code_invalid'),
            ('consent', [None, 0, 1, 'true', [], {}], 'invalid_consent')):
            for value in values:
                with self.subTest(field=field, value=value):
                    data = inputs(action='verify', smsCode='012345', configVersion='fake-v')
                    data[field] = value
                    result, calls = self.invoke(data)
                    self.assertEqual(result['status'], expected)
                    self.assertEqual(calls, [])
        for data in (None, [], 'not-an-object', 1):
            result, calls = self.invoke(data)
            self.assertEqual(result['status'], 'invalid_input')
            self.assertEqual(calls, [])

    def test_legacy_version_inputs_do_not_override_backend_versions(self):
        for field in ('agreementVersion', 'privacyVersion'):
            for value in (None, 1, True, [], {}, '', '   ', 'stale-version'):
                with self.subTest(field=field, value=value):
                    api = LoginAPI()
                    data = inputs(action='verify', smsCode='012345')
                    data[field] = value
                    result = account.register(data, api)
                    self.assertEqual(result['status'], 'credential_available')
                    login = next(c for c in api.calls if c[1] == '/api/auth/login')
                    self.assertEqual(login[2][field], 'test-v1')

    def test_invalid_backend_version_stops_before_sms_consumption(self):
        for kind in ('TERMS', 'PRIVACY'):
            for response in (None, {}, {'version': None}, {'version': 1},
                             {'version': ''}, {'version': ' '}, {'version': 'invalid/version'}):
                with self.subTest(kind=kind, response=response):
                    api = LoginAPI()
                    original = api.request
                    def request(method, path, body=None, token=None):
                        value = original(method, path, body, token)
                        return response if path == '/api/legal?type=' + kind else value
                    with patch.object(api, 'request', side_effect=request):
                        result = account.register(inputs(action='verify', smsCode='012345'), api)
                    self.assertEqual(result['status'], 'agreement_unavailable')
                    self.assertEqual(result['stage'], 'legal')
                    self.assertFalse(any(c[0] == 'POST' for c in api.calls))
                    self.assertNotIn('api_key', result)


class PackagingAccountTests(unittest.TestCase):
    def test_package_excludes_credentials_git_and_does_not_overwrite(self):
        import package_skill
        import zipfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'skill'
            root.mkdir()
            (root / 'SKILL.md').write_text('test')
            (root / 'scripts').mkdir()
            (root / 'scripts' / 'qianlima_account.py').write_text('test')
            for name in ['.env', '.env.prod', 'config.toml', 'config.json', 'credentials.json']:
                (root / name).write_text('test-only-secret')
            (root / '.git').mkdir()
            (root / '.git' / 'config').write_text('test git')
            output = Path(tmp) / 'candidate.zip'
            package_skill.package(root, output)
            before = output.read_bytes()
            with self.assertRaises(FileExistsError):
                package_skill.package(root, output)
            self.assertEqual(before, output.read_bytes())
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(set(archive.namelist()), {'skill/SKILL.md', 'skill/scripts/qianlima_account.py'})



if __name__ == '__main__':
    unittest.main()
