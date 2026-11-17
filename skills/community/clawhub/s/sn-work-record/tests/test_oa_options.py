import sys
from pathlib import Path
import unittest
from unittest.mock import Mock
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import oa_options as o

class SelectionTests(unittest.TestCase):
    def test_chinese_selection_derives_status_and_restricts_phase(self):
        self.assertTrue(hasattr(o, 'resolve_selection'), 'Chinese selection resolver missing')
        catalog = {'project': {'status':'available','complete':True,'options':[{'value':'42','label':'示例项目','bo_to_pm_status':0}]},
                   'fill_type': {'status':'available','options':[{'value':'1','label':'工作'}]},
                   'work_type': {'status':'available','options':[{'value':'5','label':'开发'}]},
                   'project_phase': {'status':'available','options':[{'value':'0','label':'商务'},{'value':'1','label':'研发/交付'}]}}
        choices = dict(project='示例项目', fill_type='工作', work_type='开发', project_phase='商务', man_hour=6)
        result = o.resolve_selection(catalog, choices)
        self.assertEqual(result, dict(project_id='42', project_name='示例项目', fill_type='1', work_type='5', project_phase='0', man_hour=6, bo_to_pm_status=0))
        for changes in [{'project_phase':'研发/交付'}, {'work_type':'不存在'}, {'man_hour':None}, {'bo_to_pm_status':1}]:
            with self.assertRaises(ValueError):
                o.resolve_selection(catalog, {**choices, **changes})
        catalog['project']['options'].append({'value':'43','label':'示例项目','bo_to_pm_status':1})
        with self.assertRaises(ValueError):
            o.resolve_selection(catalog, choices)

class ConfigurationTests(unittest.TestCase):
    def test_first_use_chinese_cli_preview_never_saves(self):
        import configure_personal_settings as cli
        import contextlib, io
        from unittest.mock import patch
        argv = ['configure', '--project', '示例项目', '--man-hour','6','--fill-type','工作','--project-phase','研发/交付','--work-type','开发']
        catalog = {'project': {'status':'available','complete':True,'options':[{'value':'42','label':'示例项目','bo_to_pm_status':1}]},
                   'fill_type': {'status':'available','options':[{'value':'1','label':'工作'}]},
                   'work_type': {'status':'available','options':[{'value':'5','label':'开发'}]},
                   'project_phase': {'status':'available','options':[{'value':'1','label':'研发/交付'}]}}
        with patch.object(sys, 'argv', argv), patch.object(cli,'load_credentials',return_value=('alice','secret','https://oa.example')), patch('oa_utils.OAAuth') as auth, patch.object(cli,'save_settings') as save, contextlib.redirect_stdout(io.StringIO()):
            auth.return_value.call.return_value = catalog
            cli.main()
            save.assert_not_called()
            auth.assert_called_once()

class OptionsTests(unittest.TestCase):
    def test_verified_dictionary_and_project_metadata(self):
        session = Mock()
        session.post.return_value.json.side_effect = [
            {'code': 200, 'data': {'content': [{'id': '42', 'projectBoName': '商机名称', 'projectPmName': '项目名称', 'boToPmStatus': 1}], 'totalElements': 1}},
            {'code': 200, 'data': [{'dictType': name, 'dictValue': '1', 'dictLabel': label} for name, label in [('sn_fill_type','工作'), ('sn_job_type','开发'), ('sn_fee_request_project_type','研发/交付')]]}]
        result = o.discover_options(session, 'https://oa.example')
        self.assertEqual(result['project']['options'][0], {'value':'42','label':'项目名称','bo_to_pm_status':1})
        self.assertEqual(result['work_type']['options'], [{'value':'1','label':'开发'}])
        self.assertEqual(result['bo_to_pm_status']['status'], 'derived')
        self.assertEqual(session.post.call_args.args[0], 'https://oa.example/sn/system/dict/data/typeList')
        self.assertEqual(session.post.call_args.kwargs['json'], ['sn_fill_type','sn_fee_request_project_type','sn_job_type'])
