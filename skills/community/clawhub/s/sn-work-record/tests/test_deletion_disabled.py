"""Production deletion is disabled; these tests never contact OA."""
import contextlib
import importlib
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))


class DeletionDisabledTests(unittest.TestCase):
    def test_api_rejects_delete_and_restore_before_any_network(self):
        import oa_utils
        for flag in (0, 1):
            with self.subTest(flag=flag):
                session = Mock()
                with self.assertRaisesRegex(ValueError, '无可靠恢复契约'):
                    oa_utils.update_time_entry(session, 'https://example.invalid', '123',
                                               is_deleted=flag, confirm_entry_id='123')
                self.assertEqual(session.mock_calls, [])

    def test_cli_rejects_before_credentials_or_auth(self):
        with patch('runtime_bootstrap.ensure_runtime'):
            cli = importlib.import_module('update_time_entry')
        for flag in ('--delete', '--restore-deleted'):
            with self.subTest(flag=flag), patch.object(sys, 'argv', ['update', '123', flag, '--confirm-entry-id', '123']), patch.object(cli, 'load_credentials') as credentials, patch.object(cli, 'OAAuth') as auth, contextlib.redirect_stderr(io.StringIO()) as stderr:
                with self.assertRaises(SystemExit) as caught:
                    cli.main()
                self.assertEqual(caught.exception.code, 2)
                self.assertIn('无可靠恢复契约', stderr.getvalue())
                credentials.assert_not_called()
                auth.assert_not_called()
