"""CLI routing tests; authentication and every remote operation are mocked."""
import contextlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import update_time_entry as cli
import oa_utils as oa

class CliTests(unittest.TestCase):
    def invoke(self, flags, result=None, error=None):
        auth = MagicMock()
        auth.call.side_effect = lambda operation, **kwargs: operation(auth.session)
        output = io.StringIO()
        errors = io.StringIO()
        with patch.object(sys, 'argv', ['update_time_entry.py','123',*flags]), \
             patch.object(cli, 'load_credentials', return_value=('test-account','unused','https://oa.example')) as credentials, \
             patch.object(cli, 'OAAuth', return_value=auth), \
             patch.object(cli, 'amend_time_entry', create=True, return_value=result, side_effect=error) as amendment, \
             patch.object(cli, 'update_time_entry', return_value={'code':200, 'verified':True}) as direct, \
             patch.object(cli, 'get_time_entry_details', return_value=({'state':'20'},{})) as detail, \
             contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            code = 0
            try: cli.main()
            except SystemExit as exc: code = exc.code
        return code, output.getvalue(), errors.getvalue(), auth, amendment, direct, detail, credentials

    def test_preview_routes_to_guard_without_consent_or_direct_put(self):
        result = {'amendment_status':'preview','verified':False,'detail':{'jobDesc':'new'}}
        code, output, _, auth, amendment, direct, detail, _ = self.invoke(['--preview','--job-desc','new','--json'], result)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output), result)
        amendment.assert_called_once_with(auth.session, 'https://oa.example', '123', 'new', preview=True, withdraw_resubmit=False)
        direct.assert_not_called()
        detail.assert_not_called()
        self.assertFalse(auth.call.call_args.kwargs['allow_relogin'])

    def test_permission_routes_to_guard_and_outputs_verified_status(self):
        result = {'amendment_status':'amended-confirmed','verified':True,'detail':{'jobDesc':'new'}}
        code, output, _, auth, amendment, direct, detail, _ = self.invoke(['--withdraw-resubmit','--job-desc','new','--json'], result)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output), result)
        amendment.assert_called_once_with(auth.session, 'https://oa.example', '123', 'new', preview=False, withdraw_resubmit=True)
        direct.assert_not_called()
        detail.assert_not_called()

    def test_amendment_and_delete_are_mutually_exclusive_before_auth(self):
        for flags in (['--preview','--delete'], ['--withdraw-resubmit','--delete'], ['--withdraw-resubmit'], ['--preview']):
            code, _, _, _, amendment, direct, _, credentials = self.invoke(flags)
            self.assertEqual(code, 2)
            credentials.assert_not_called()
            direct.assert_not_called()
            amendment.assert_not_called()

    def test_delete_requires_confirmation_before_auth(self):
        code, _, _, _, _, direct, _, credentials = self.invoke(['--delete'])
        self.assertEqual(code, 2)
        credentials.assert_not_called()
        direct.assert_not_called()

    def test_plain_job_description_remains_available_but_deletion_is_disabled(self):
        code, _, _, auth, amendment, direct, _, _ = self.invoke(['--job-desc', 'new'])
        self.assertEqual(code, 0)
        direct.assert_called_once_with(auth.session, 'https://oa.example', '123', job_desc='new', is_deleted=None)
        amendment.assert_not_called()
        self.assertFalse(auth.call.call_args_list[0].kwargs['allow_relogin'])
        for flag in ('--delete', '--restore-deleted'):
            code, _, errors, auth, amendment, direct, detail, credentials = self.invoke([flag, '--confirm-entry-id', '123'])
            self.assertEqual(code, 2)
            self.assertIn('无可靠恢复契约', errors)
            credentials.assert_not_called()
            auth.call.assert_not_called()
            direct.assert_not_called()
            amendment.assert_not_called()
            detail.assert_not_called()

    def test_mutation_error_does_not_fallback_or_expose_transport_details(self):
        from submission_guard import SubmissionUncertain
        error = SubmissionUncertain('撤回可能已发生；未重新提交，禁止重发')
        code, output, errors, auth, amendment, direct, detail, _ = self.invoke(['--withdraw-resubmit','--job-desc','new'], error=error)
        self.assertEqual(code, 1)
        self.assertIn('未重新提交', errors)
        self.assertNotIn('成功', output)
        direct.assert_not_called()
        detail.assert_not_called()
        self.assertEqual(auth.call.call_count, 1)

    def test_untrusted_transport_exception_is_not_printed(self):
        code, output, errors, _, _, direct, detail, _ = self.invoke(
            ['--withdraw-resubmit','--job-desc','new'],
            error=ConnectionError('https://private.invalid token=secret'))
        self.assertEqual(code, 1)
        self.assertNotIn('private.invalid', errors)
        self.assertNotIn('secret', errors)
        self.assertIn('只读核实', errors)
        self.assertIn('撤回/重新提交状态未知', errors)
        direct.assert_not_called()
        detail.assert_not_called()

    def test_withdrawn_status_has_human_label(self):
        self.assertEqual(oa.state_to_text('-1'), '已撤回')

if __name__ == '__main__': unittest.main()
