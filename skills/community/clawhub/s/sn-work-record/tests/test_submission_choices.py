"""Network is mocked at the boundary; exercise real submission resolution."""
import contextlib
import importlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
with patch('runtime_bootstrap.ensure_runtime'):
    cli = importlib.import_module('submit_time_entry')
import personal_settings as settings


def catalog():
    return {'project': {'status': 'available', 'complete': True, 'options': [
        {'value': '42', 'label': '示例项目', 'bo_to_pm_status': 1},
        {'value': '43', 'label': '示例商机', 'bo_to_pm_status': 0}]},
        'fill_type': {'status': 'available', 'options': [{'value': '1', 'label': '工作'}, {'value': '2', 'label': '事假'}]},
        'project_phase': {'status': 'available', 'options': [{'value': '0', 'label': '商务'}, {'value': '1', 'label': '研发/交付'}]},
        'work_type': {'status': 'available', 'options': [{'value': '5', 'label': '开发'}]}}


class SubmissionTests(unittest.TestCase):
    def invoke(self, extra, *, options=None, settings_path=None, lookup_error=None, write_result=None):
        stream = io.StringIO()
        error = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            argv = ['submit', '2026-10-10', '--job-desc', '中文选项链路验证（仅预览，不提交）',
                    '--settings', str(settings_path or Path(directory) / 'absent.json'), *extra]
            with patch.object(sys, 'argv', argv), patch.object(cli, 'load_credentials', return_value=('alice', 'secret', 'https://oa.example')), patch.object(cli, 'OAAuth') as auth, patch.object(cli, 'discover_options', create=True) as discover, patch.object(cli, 'submit_time_entry') as write, patch.object(cli, 'is_workday', return_value=True), contextlib.redirect_stdout(stream), contextlib.redirect_stderr(error):
                write.return_value = write_result if write_result is not None else {'code':200,'submission_status':'submitted-confirmed','verified':True}
                if isinstance(write_result, BaseException):
                    write.side_effect = write_result
                discover.return_value = options if options is not None else catalog()
                if lookup_error:
                    discover.side_effect = lookup_error
                auth.return_value.call.side_effect = lambda operation, **kw: operation(Mock())
                exit_code = 0
                try:
                    cli.main()
                except SystemExit as exc:
                    exit_code = exc.code
                return exit_code, stream.getvalue(), error.getvalue(), write, auth

    def test_cli_unknown_write_explicitly_prohibits_resend(self):
        from submission_guard import SubmissionUncertain
        args = ['--project','示例项目','--fill-type','工作','--project-phase','研发/交付','--work-type','开发','--man-hour','8']
        code, output, error, _, _ = self.invoke(args, write_result=SubmissionUncertain('结果未知；禁止重发，请只读核实'))
        self.assertEqual(code, 1)
        self.assertEqual(output, '')
        self.assertIn('禁止重发', error)

    def test_cli_duplicate_is_not_reported_as_new_submission(self):
        args = ['--project','示例项目','--fill-type','工作','--project-phase','研发/交付','--work-type','开发','--man-hour','8']
        code, output, error, _, _ = self.invoke(args, write_result={'code':200,'submission_status':'skipped-existing','verified':True})
        self.assertEqual(code, 0, error)
        self.assertIn('未重复提交', output)
        self.assertNotIn('提交成功', output)
        code, output, error, _, _ = self.invoke(args, write_result={'code':200})
        self.assertEqual(code, 1)
        self.assertNotIn('成功', output)

    def test_chinese_preview_has_names_and_never_submits(self):
        code, output, error, write, auth = self.invoke(['--preview', '--json', '--project', '示例项目', '--fill-type', '工作', '--project-phase', '研发/交付', '--work-type', '开发', '--man-hour', '0.5'])
        self.assertEqual(code, 0, error)
        data = json.loads(output)
        self.assertTrue(data['preview_only'])
        self.assertEqual(data['project_name'], '示例项目')
        self.assertEqual(data['project_phase'], '研发/交付')
        self.assertEqual(data['work_type'], '开发')
        self.assertEqual(data['man_hour'], 0.5)
        self.assertNotIn('project_id', data)
        write.assert_not_called()
        auth.assert_called_once()

    def test_legacy_codes_are_verified_and_assertions_cannot_override_live_project(self):
        base = ['--preview', '--json', '--project-id', '42', '--project-name', '示例项目', '--bo-to-pm-status', '1', '--fill-type', '1', '--project-phase', '1', '--work-type', '5', '--man-hour', '1', '--include-codes']
        code, output, error, write, _ = self.invoke(base)
        self.assertEqual(code, 0, error)
        self.assertEqual(json.loads(output)['codes']['bo_to_pm_status'], 1)
        write.assert_not_called()
        for flag, value in [('--project-name', '旧项目名称'), ('--bo-to-pm-status', '0'), ('--project-id', '042')]:
            changed = base.copy()
            changed[changed.index(flag) + 1] = value
            code, _, _, write, _ = self.invoke(changed)
            self.assertEqual(code, 1)
            write.assert_not_called()

    def test_invalid_input_rejected_before_auth(self):
        base = ['--preview', '--save-draft', '--project', '42', '--fill-type', '工作', '--project-phase', '商务', '--work-type', '开发', '--man-hour', '1']
        for change in [['--man-hour', 'nan'], ['--man-hour', '-1'], ['--job-desc', '  '], ['--fill-date', '2026-02-30'], ['--fill-date', '2026-1-1'], ['--fill-date', '2026-10-09']]:
            code, _, _, write, auth = self.invoke(base + change)
            self.assertEqual(code, 1, change)
            auth.assert_not_called()
            write.assert_not_called()

    def test_malformed_live_codes_cannot_be_selected(self):
        for bad in [' 5', '5 ', '+5', '５', '5.0', 'None']:
            options = catalog()
            options['work_type']['options'][0]['value'] = bad
            code, _, _, write, _ = self.invoke(['--preview', '--project', '42', '--fill-type', '工作', '--project-phase', '商务', '--work-type', bad, '--man-hour', '1'], options=options)
            self.assertEqual(code, 1, bad)
            write.assert_not_called()

    def test_saved_defaults_are_revalidated_refreshed_and_never_changed(self):
        values = dict(project_id='42', project_name='旧名称', man_hour=6, fill_type='1', project_phase='1', work_type='5', bo_to_pm_status=0)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'prefs.json'
            settings.save_settings(path, 'alice', 'https://oa.example', values, confirmed=True)
            before = path.read_bytes()
            code, output, error, write, _ = self.invoke(['--preview', '--json', '--include-codes'], settings_path=path)
            self.assertEqual(code, 0, error)
            self.assertEqual(json.loads(output)['project_name'], '示例项目')
            self.assertEqual(json.loads(output)['codes']['bo_to_pm_status'], 1)
            code, _, _, write, _ = self.invoke(['--preview', '--project', '示例商机'], settings_path=path)
            self.assertEqual(code, 1)  # inherited delivery phase is incompatible
            write.assert_not_called()
            code, output, error, _, _ = self.invoke(['--preview', '--json', '--include-codes', '--project', '示例商机', '--project-phase', '商务', '--man-hour', '2'], settings_path=path)
            self.assertEqual(code, 0, error)
            self.assertEqual(json.loads(output)['codes']['bo_to_pm_status'], 0)
            self.assertEqual(json.loads(output)['project_name'], '示例商机')
            self.assertEqual(path.read_bytes(), before)
            for key in ('project_id', 'fill_type', 'project_phase', 'work_type'):
                settings.save_settings(path, 'alice', 'https://oa.example', {**values, key: '999999'}, confirmed=True)
                code, _, _, write, _ = self.invoke(['--preview'], settings_path=path)
                self.assertEqual(code, 1, key)
                write.assert_not_called()
            settings.save_settings(path, 'bob', 'https://oa.example', values, confirmed=True)
            code, _, _, write, auth = self.invoke(['--preview'], settings_path=path)
            self.assertEqual(code, 1)
            auth.assert_not_called()

    def test_submit_receives_exact_preview_codes_with_write_relogin_disabled(self):
        args = ['--project', '示例商机', '--fill-type', '工作', '--project-phase', '商务', '--work-type', '开发', '--man-hour', '2']
        code, output, error, _, _ = self.invoke(args + ['--preview', '--json', '--include-codes'])
        self.assertEqual(code, 0, error)
        preview = json.loads(output)
        code, _, error, write, auth = self.invoke(args)
        self.assertEqual(code, 0, error)
        write.assert_called_once()
        payload = write.call_args.kwargs
        self.assertEqual({key: payload[key] for key in preview['codes']}, preview['codes'])
        self.assertEqual(payload['man_hour'], preview['man_hour'])
        self.assertEqual(payload['job_desc'], preview['job_desc'])
        self.assertEqual(payload['save_or_submit'], 1)
        self.assertEqual(auth.return_value.call.call_args.kwargs, {'allow_relogin': False})

    def test_lookup_failure_unknown_ambiguity_and_incomplete_never_write(self):
        base = ['--project', '42', '--fill-type', '工作', '--project-phase', '商务', '--work-type', '开发', '--man-hour', '1']
        code, _, _, write, _ = self.invoke(base, lookup_error=RuntimeError('private host/token'))
        self.assertEqual(code, 1)
        write.assert_not_called()
        for field in ('project', 'fill_type', 'project_phase', 'work_type'):
            changed = base.copy()
            changed[changed.index('--' + field.replace('_', '-')) + 1] = '不存在'
            code, _, _, write, _ = self.invoke(changed)
            self.assertEqual(code, 1, field)
            write.assert_not_called()
        for bad in ('ambiguous', 'incomplete', 'unavailable'):
            options = catalog()
            if bad == 'ambiguous':
                options['work_type']['options'].append({'value': '6', 'label': '开发'})
            elif bad == 'incomplete':
                options['project']['complete'] = False
            else:
                options['work_type']['status'] = 'unavailable'
            code, _, _, write, _ = self.invoke(base, options=options)
            self.assertEqual(code, 1, bad)
            write.assert_not_called()

    def test_dangling_settings_symlink_cannot_be_silently_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'prefs.json'
            path.symlink_to(Path(directory) / 'missing.json')
            code, _, _, write, auth = self.invoke(['--preview', '--project', '42', '--fill-type', '工作', '--project-phase', '商务', '--work-type', '开发', '--man-hour', '1'], settings_path=path)
            self.assertEqual(code, 1)
            auth.assert_not_called()
            write.assert_not_called()

    def test_write_auth_expiry_never_refreshes_or_retries(self):
        import oa_utils
        auth = object.__new__(oa_utils.OAAuth)
        auth.session = Mock()
        operation = Mock(side_effect=oa_utils.AuthExpiredError('expired'))
        with patch.object(auth, 'refresh') as refresh, patch.object(oa_utils, 'clear_cached_token') as clear:
            with self.assertRaises(RuntimeError):
                auth.call(operation, allow_relogin=False)
            operation.assert_called_once_with(auth.session)
            refresh.assert_not_called()
            clear.assert_called_once()

    def test_legacy_status_assertion_rejects_malformed_tokens_without_repair(self):
        base = ['--preview', '--project', '42', '--fill-type', '工作', '--project-phase', '商务', '--work-type', '开发', '--man-hour', '1']
        for token in ('01', '+1', '１', ' 1', '1 '):
            code, _, _, write, auth = self.invoke(base + ['--bo-to-pm-status', token])
            self.assertEqual(code, 1, token)
            auth.assert_not_called()
            write.assert_not_called()

    def test_leave_not_supported_even_in_preview_or_draft(self):
        for mode in (['--preview'], ['--save-draft']):
            code, output, error, write, _ = self.invoke([*mode, '--project', '42', '--fill-type', '事假', '--project-phase', '商务', '--work-type', '开发', '--man-hour', '1'])
            self.assertEqual(code, 1)
            self.assertIn('普通工作', error)
            write.assert_not_called()
