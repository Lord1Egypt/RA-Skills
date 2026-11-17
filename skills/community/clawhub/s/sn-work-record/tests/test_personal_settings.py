import sys
from pathlib import Path
import unittest
from unittest.mock import Mock
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import oa_utils

class SafetyTests(unittest.TestCase):
    def test_each_required_field_is_checked_and_explicit_payload_preserved(self):
        values = dict(project_id='42', project_name='Example', man_hour=6,
                      project_phase='2', work_type='7', bo_to_pm_status=0, fill_type='1')
        for key in values:
            session = Mock()
            with self.assertRaises(ValueError, msg=key):
                oa_utils.submit_time_entry(session, 'https://oa.example', '2026-10-09', job_desc='work', **{**values, key: None})
            session.post.assert_not_called()
        session = Mock()
        session.headers = {'Authorization':'Bearer fake-token', 'Admin-OA-Token':'fake-token'}
        from submission_guard import bind_submission_session
        bind_submission_session(session, 'https://oa.example', 'fake-account')
        row = dict(fillDate='2026-10-09', projectName='Example', projectId='42',
                   projectPhase='2', workType='7', manHour=6, jobDesc='work',
                   boToPmStatus=0, fillType='1', state=20, isDeleted=0)
        session.post.return_value.json.side_effect = [
            {'code':200,'data':[]}, {'code':200}, {'code':200,'data':[row]}]
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory, patch.dict('os.environ', {'SN_WORK_RECORD_GUARD_DIR':directory}):
            oa_utils.submit_time_entry(session, 'https://oa.example', '2026-10-09', job_desc='work', **values)
        payload = session.post.call_args_list[1].kwargs['json']['timeEntryList'][0]
        self.assertEqual(payload['manHour'], 6)
        self.assertEqual(payload['workType'], '7')
        self.assertEqual(payload['boToPmStatus'], 0)

    def test_missing_required_fields_never_posts_even_draft(self):
        for mode in (0, 1):
            session = Mock()
            session.post.return_value.json.return_value = {'code': 200}
            with self.assertRaises(ValueError):
                oa_utils.submit_time_entry(session, 'https://oa.example', '2026-10-09', None, None, 'work', save_or_submit=mode)
            session.post.assert_not_called()

class StorageTests(unittest.TestCase):
    def test_confirmed_settings_are_private_bound_and_overridable(self):
        import tempfile, json, os
        import personal_settings as p
        self.assertTrue(hasattr(p, 'save_settings'), 'confirmed storage missing')
        values = dict(project_id='42', project_name='Example', man_hour=6,
                      project_phase='2', work_type='7', fill_type='3', bo_to_pm_status=0)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'prefs.json'
            with self.assertRaises(ValueError):
                p.save_settings(path, 'alice', 'https://oa.example', values, confirmed=False)
            self.assertFalse(path.exists())
            p.save_settings(path, 'alice', 'https://oa.example', values, confirmed=True)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertNotIn('alice', path.read_text())
            self.assertEqual(p.resolve_settings(path, 'alice', 'https://oa.example', {'man_hour': 3})['man_hour'], 3)
            self.assertEqual(p.resolve_settings(path, 'alice', 'https://oa.example', {})['man_hour'], 6)
            for account, host in [('bob', 'https://oa.example'), ('alice', 'https://other.example')]:
                with self.assertRaises(ValueError):
                    p.resolve_settings(path, account, host, {})
            for raw in ('{bad', '[]', '{}'):
                path.write_text(raw)
                with self.assertRaises(ValueError):
                    p.resolve_settings(path, 'alice', 'https://oa.example', {})

class CliTests(unittest.TestCase):
    def test_cli_missing_fields_fails_before_auth_for_drafts(self):
        import importlib
        from unittest.mock import patch
        with patch('runtime_bootstrap.ensure_runtime'):
            cli = importlib.import_module('submit_time_entry')
        with patch.object(sys, 'argv', ['submit', '2026-10-09', '--job-desc', 'work', '--save-draft']), patch.object(cli, 'load_credentials', side_effect=lambda *a, **kw: ('alice', 'secret', 'https://oa.example', '42', 'Example') if kw.get('require_project') else ('alice', 'secret', 'https://oa.example')), patch.object(cli, 'OAAuth') as auth:
            with self.assertRaises(SystemExit):
                cli.main()
            auth.assert_not_called()

class OptionTests(unittest.TestCase):
    def test_discovery_rejects_malformed_project_metadata(self):
        import oa_options
        for records in ([{'id': '42'}], [{'id': None, 'projectBoName': 'bad'}], [{'id': '42', 'projectBoName': 'A', 'boToPmStatus':0}, {'id': '42', 'projectBoName': 'B', 'boToPmStatus':0}]):
            session = Mock()
            session.post.return_value.json.return_value = {'code': 200, 'data': {'content': records}}
            with self.assertRaises(ValueError):
                oa_options.discover_options(session, 'https://oa.example')

class ConfigurationCliTests(unittest.TestCase):
    def test_configuration_confirmation_controls_only_local_save(self):
        import tempfile, contextlib, io
        from unittest.mock import patch
        import configure_personal_settings as cli
        catalog = {'project': {'status':'available','complete':True,'options':[{'value':'42','label':'Example','bo_to_pm_status':1}]},
                   'fill_type': {'status':'available','options':[{'value':'1','label':'工作'}]},
                   'work_type': {'status':'available','options':[{'value':'5','label':'开发'}]},
                   'project_phase': {'status':'available','options':[{'value':'1','label':'研发/交付'}]}}
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / 'prefs.json')
            argv = ['configure', '--settings', path, '--project', 'Example', '--man-hour', '6', '--fill-type', '工作', '--project-phase', '研发/交付', '--work-type', '开发']
            with patch.object(cli, 'load_credentials', return_value=('alice', 'secret', 'https://oa.example')), patch.object(oa_utils,'OAAuth') as auth, contextlib.redirect_stdout(io.StringIO()):
                auth.return_value.call.return_value = catalog
                with patch.object(sys, 'argv', argv):
                    cli.main()
                self.assertFalse(Path(path).exists())
                with patch.object(sys, 'argv', argv + ['--confirm-save']):
                    cli.main()
                import personal_settings
                values = personal_settings.resolve_settings(path, 'alice', 'https://oa.example', {})
                self.assertEqual(values['work_type'], '5')
                self.assertEqual(values['bo_to_pm_status'], 1)

class ValidationTests(unittest.TestCase):
    def test_partial_project_override_and_malformed_values_rejected(self):
        import personal_settings as p, tempfile
        values = dict(project_id='42', project_name='Example', man_hour=6, project_phase='2', work_type='7', fill_type='3', bo_to_pm_status=0)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'prefs.json'
            p.save_settings(path, 'alice', 'https://oa.example', values, confirmed=True)
            with self.assertRaises(ValueError):
                p.resolve_settings(path, 'alice', 'https://oa.example', {'project_id': '43'})
        for key, invalid in [('project_id', True), ('project_phase', {}), ('fill_type', []), ('bo_to_pm_status', 'x'), ('man_hour', float('nan'))]:
            with self.assertRaises(ValueError, msg=key):
                p.validate_fields({**values, key: invalid})

class OptionCliTests(unittest.TestCase):
    def test_option_cli_outputs_unavailable_fields(self):
        import oa_options as cli, contextlib, io, json
        from unittest.mock import patch
        self.assertTrue(hasattr(cli, 'main'), 'option CLI missing')
        stream = io.StringIO()
        self.assertTrue(hasattr(cli, 'ensure_runtime'), 'option CLI runtime bootstrap missing')
        with patch.object(cli, 'ensure_runtime'), patch.object(sys, 'argv', ['options']), patch.object(cli, 'load_credentials', return_value=('alice', 'secret', 'https://oa.example')), patch.object(cli, 'OAAuth') as auth, contextlib.redirect_stdout(stream):
            auth.return_value.call.side_effect = lambda operation: operation(Mock())
            with patch.object(cli, 'discover_options', return_value={'work_type': {'status': 'unavailable'}}):
                cli.main()
        self.assertEqual(json.loads(stream.getvalue())['work_type']['status'], 'unavailable')

if __name__ == '__main__':
    unittest.main()
