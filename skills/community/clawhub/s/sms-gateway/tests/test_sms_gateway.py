#!/usr/bin/env python3
"""Integration tests for SMS Gateway skill.

Requires SMS_GATE_URL, SMS_GATE_USER, and SMS_GATE_PASS in .env or environment.
Tests call the actual scripts in scripts/ as subprocesses.
"""
import json
import os
import re
import subprocess
import unittest


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

def load_env():
    """Load .env file from project root."""
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ.setdefault(key.strip(), val.strip())


load_env()

BASE_URL = os.environ.get('SMS_GATE_URL', '').rstrip('/')
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'scripts')


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_script(script_name, args=None):
    """Run a script from scripts/ and return (stdout, stderr, returncode)."""
    cmd = ['python3', os.path.join(SCRIPTS_DIR, script_name)] + (args or [])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestHealth(unittest.TestCase):
    """Test the health check script."""

    @classmethod
    def setUpClass(cls):
        if not BASE_URL:
            raise unittest.SkipTest('SMS_GATE_URL must be set')

    def test_health_passes(self):
        stdout, stderr, rc = run_script('health.py')
        self.assertEqual(rc, 0, f'health.py failed: {stderr}')
        self.assertIn('Gateway:', stdout)

    def test_health_shows_battery(self):
        stdout, _, rc = run_script('health.py')
        self.assertEqual(rc, 0)
        self.assertIn('Battery:', stdout)

    def test_health_shows_connection(self):
        stdout, _, rc = run_script('health.py')
        self.assertEqual(rc, 0)
        self.assertIn('Connected:', stdout)


class TestAuth(unittest.TestCase):
    """Test JWT authentication."""

    @classmethod
    def setUpClass(cls):
        if not BASE_URL:
            raise unittest.SkipTest('SMS_GATE_URL must be set')
        # Clear cached token to force fresh auth
        token_path = os.path.join(os.path.dirname(__file__), '..', '.token.json')
        if os.path.exists(token_path):
            os.unlink(token_path)

    def test_jwt_token_obtained(self):
        """First API call should obtain a JWT token and cache it."""
        stdout, stderr, rc = run_script('list_messages.py', ['1'])
        self.assertEqual(rc, 0, f'list_messages.py failed: {stderr}')
        token_path = os.path.join(os.path.dirname(__file__), '..', '.token.json')
        self.assertTrue(os.path.exists(token_path), '.token.json should be created')
        with open(token_path) as f:
            token_data = json.load(f)
        self.assertIn('access_token', token_data)
        self.assertIn('expires_epoch', token_data)

    def test_cached_token_reused(self):
        """Second call should reuse the cached token (no error)."""
        stdout, stderr, rc = run_script('list_messages.py', ['1'])
        self.assertEqual(rc, 0, f'list_messages.py failed with cached token: {stderr}')


class TestListMessages(unittest.TestCase):
    """Test listing messages."""

    @classmethod
    def setUpClass(cls):
        if not BASE_URL:
            raise unittest.SkipTest('SMS_GATE_URL must be set')

    def test_list_default(self):
        stdout, stderr, rc = run_script('list_messages.py')
        self.assertEqual(rc, 0, f'list_messages.py failed: {stderr}')

    def test_list_with_limit(self):
        stdout, stderr, rc = run_script('list_messages.py', ['2'])
        self.assertEqual(rc, 0, f'list_messages.py failed: {stderr}')


class TestSendAndCheck(unittest.TestCase):
    """Test sending an SMS and checking its status.

    Sends a real SMS to the configured device's own number.
    Only runs if TEST_PHONE_NUMBER is set in environment.
    """

    @classmethod
    def setUpClass(cls):
        if not BASE_URL:
            raise unittest.SkipTest('SMS_GATE_URL must be set')
        cls.phone = os.environ.get('TEST_PHONE_NUMBER', '')
        if not cls.phone:
            raise unittest.SkipTest('TEST_PHONE_NUMBER must be set to run send tests')

    def test_send_and_check_status(self):
        stdout, stderr, rc = run_script('send_sms.py', [
            self.phone, 'Integration test from sms-gateway skill'
        ])
        self.assertEqual(rc, 0, f'send_sms.py failed: {stderr}')
        self.assertIn('SMS sent', stdout)

        # Extract message ID
        match = re.search(r'ID:\s+(\S+)', stdout)
        self.assertIsNotNone(match, f'Could not parse message ID from: {stdout}')
        msg_id = match.group(1)

        # Check status
        stdout, stderr, rc = run_script('check_status.py', [msg_id])
        self.assertEqual(rc, 0, f'check_status.py failed: {stderr}')
        self.assertIn('Message Status', stdout)
        self.assertIn(msg_id[:12], stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
