import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from doctor import native_feishu_checks

class NativePreflightTest(unittest.TestCase):
    def test_profile_is_explicit_in_both_checks(self):
        result=native_feishu_checks({'feishu':{'profile':'selected','root_folder_token':'folder'}})
        self.assertEqual(result['auth_status_argv'],['/usr/bin/env','-u','HERMES_HOME','lark-cli','auth','status','--json','--verify','--profile','selected'])
        self.assertEqual(result['native_cli_prefix'],['/usr/bin/env','-u','HERMES_HOME','lark-cli'])
        self.assertEqual(result['folder_read_argv'][-4:],['--as','user','--profile','selected'])

    def test_no_default_profile_fallback(self):
        for profile in [None,'',' ']:
            with self.assertRaises(ValueError):native_feishu_checks({'feishu':{'profile':profile}})
        self.assertIsNone(native_feishu_checks({}))
