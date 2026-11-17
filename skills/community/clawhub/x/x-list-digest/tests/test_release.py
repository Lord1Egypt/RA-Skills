import contextlib,io,json,runpy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))

class ReleaseTest(unittest.TestCase):
    def test_unconfigured_doctor_reports_structure_without_crashing(self):
        output=io.StringIO()
        with contextlib.redirect_stdout(output):
            runpy.run_path(str(Path(__file__).resolve().parents[1]/'scripts/doctor.py'),run_name='__main__')
        value=json.loads(output.getvalue())
        self.assertEqual(value['lists'],{})
        self.assertIsNone(value['native_feishu_checks'])
        self.assertEqual(value['browser'],'requires_host_login_and_list_access_check')
