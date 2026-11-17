"""Real SIGINT timing with fake services; no network, real config or model calls."""
import io
import json
import os
from pathlib import Path
import secrets
import selectors
import signal
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import qianlima_account as account


def interrupt_child(stage):
    calls = []
    key = 'qlm_' + secrets.token_hex(16)
    token = secrets.token_hex(16)

    def pause():
        os.write(1, b'READY\n')
        signal.pause()

    class Config:
        written = False
        value = 'previous-test-configuration'
        closed = False

        def preflight(self, version, replace):
            if stage == 'before_login':
                pause()

        def save(self, value, version, replace):
            if stage == 'write_unknown':
                self.written = None
                pause()
            self.value, self.written = value, True
            if stage == 'after_write':
                pause()

        def close(self):
            self.closed = True

    class API:
        def request(self, method, path, body=None, token=None):
            calls.append(path)
            if path.startswith('/api/legal'):
                return {'version': 'test-v1'}
            if path == '/api/auth/sms/send':
                pause()
            if path == '/api/auth/login':
                if stage == 'login_in_flight':pause()
                return {'accessToken': secret_token, 'newUser': False,
                        'defaultApiKey': {'keyId': 7, 'status': 'ACTIVE', 'apiKey': key}}
            if path == '/api/points/account':
                if stage == 'after_login':
                    pause()
                return {'availablePoints': 0}
            return None

    secret_token = token
    config = Config()
    data = dict(action='send' if stage == 'send_in_flight' else 'verify',
                phone='19900000001', smsCode='012345', consent=True,
                configVersion='fake-v', replaceConfirmed=True)
    output = io.StringIO()
    with patch.object(account, 'CodexConfig', return_value=config), \
         patch.object(account, 'AccountAPI', return_value=API()), \
         patch.object(sys, 'argv', ['qianlima_account.py', 'register', '--input-stdin']), \
         patch.object(sys, 'stdin', io.StringIO(json.dumps(data))), \
         patch.object(sys, 'stdout', output):
        code = account.main(config_factory=account.CodexConfig)
    serialized = output.getvalue()
    print(json.dumps(dict(exit_code=code, result=json.loads(serialized), calls=calls,
                          old_value_preserved=config.value == 'previous-test-configuration',
                          new_value_present=config.value == key, closed=config.closed,
                          secret_leaked=any(v in serialized for v in (key, token, '012345')))))


@unittest.skipUnless(hasattr(signal, 'SIGINT') and hasattr(signal, 'pause'), 'POSIX signal test')
class CancellationTests(unittest.TestCase):
    def run_stage(self, stage):
        env = {k: v for k, v in os.environ.items() if k in ('PATH', 'LANG', 'TMPDIR')}
        proc = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), '--cancel-child', stage],
                                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, env=env)
        try:
            with selectors.DefaultSelector() as selector:
                selector.register(proc.stdout, selectors.EVENT_READ)
                self.assertTrue(selector.select(10), 'child did not reach requested cancellation point')
            self.assertEqual(proc.stdout.readline(), b'READY\n')
            proc.send_signal(signal.SIGINT)
            out, err = proc.communicate(timeout=15)
            self.assertEqual(proc.returncode, 0, err.decode())
            self.assertEqual(err, b'')
            self.assertNotIn(b'qlm_', out)
            result = json.loads(out)
            self.assertEqual(result['exit_code'], 1)
            self.assertEqual(result['result']['status'], 'cancelled')
            self.assertTrue(result['closed'])
            self.assertFalse(result['secret_leaked'])
            return result
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
            proc.stdout.close()
            proc.stderr.close()

    def test_before_login_keeps_previous_config_and_does_not_authenticate(self):
        result = self.run_stage('before_login')
        self.assertTrue(result['old_value_preserved'])
        self.assertFalse(result['result']['configuration_written'])
        self.assertFalse(any('/auth/' in p for p in result['calls']))
        self.assertIs(result['result']['login_completed'],False)

    def test_login_in_flight_keeps_login_state_unknown(self):
        result = self.run_stage('login_in_flight')
        self.assertIsNone(result['result']['login_completed'])
        self.assertFalse(result['result']['configuration_written'])
        self.assertTrue(result['old_value_preserved'])
        self.assertEqual(result['calls'].count('/api/auth/login'),1)
        self.assertNotIn('/api/auth/logout',result['calls'])

    def test_send_in_flight_does_not_replay_or_login(self):
        result = self.run_stage('send_in_flight')
        self.assertEqual(result['calls'].count('/api/auth/sms/send'), 1)
        self.assertNotIn('/api/auth/login', result['calls'])
        self.assertTrue(result['old_value_preserved'])
        self.assertFalse(result['result']['configuration_written'])

    def test_after_login_before_save_cleans_token_without_overwrite(self):
        result = self.run_stage('after_login')
        self.assertEqual(result['calls'].count('/api/auth/login'), 1)
        self.assertEqual(result['calls'][-1], '/api/auth/logout')
        self.assertIs(result['result']['login_completed'],True)
        self.assertIs(result['result']['logout_confirmed'],True)
        self.assertTrue(result['old_value_preserved'])
        self.assertFalse(result['result']['configuration_written'])

    def test_after_save_keeps_actual_written_state_without_rollback(self):
        result = self.run_stage('after_write')
        self.assertTrue(result['new_value_present'])
        self.assertTrue(result['result']['configuration_written'])
        self.assertEqual(result['calls'][-1], '/api/auth/logout')
        self.assertIs(result['result']['login_completed'],True)
        self.assertIs(result['result']['logout_confirmed'],True)

    def test_uncertain_write_stays_unknown(self):
        result = self.run_stage('write_unknown')
        self.assertIsNone(result['result']['configuration_written'])
        self.assertEqual(result['calls'][-1], '/api/auth/logout')
        self.assertIs(result['result']['login_completed'],True)
        self.assertIs(result['result']['logout_confirmed'],True)


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--cancel-child':
        interrupt_child(sys.argv[2])
    else:
        unittest.main()
