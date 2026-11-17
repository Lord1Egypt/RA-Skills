import importlib.util
import unittest
import socket,sys
from types import SimpleNamespace
from unittest.mock import patch
from pathlib import Path
spec=importlib.util.spec_from_file_location('preflight',Path(__file__).resolve().parents[1]/'scripts/browser_preflight.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


class PreflightTests(unittest.TestCase):
    def test_owner_must_cover_probe_ipv4_address(self):
        for family,address,expected in [(socket.AF_INET6,'::1',False),(socket.AF_INET,'192.168.1.2',False),(socket.AF_INET,'127.0.0.1',True),(socket.AF_INET,'0.0.0.0',True)]:
            connection=SimpleNamespace(status='LISTEN',family=family,laddr=SimpleNamespace(ip=address,port=9234))
            process=SimpleNamespace(pid=42,info={'cmdline':['chrome','--user-data-dir='+str(module.PROFILE),'--remote-debugging-port=9234']},net_connections=lambda kind:[connection])
            fake=SimpleNamespace(CONN_LISTEN='LISTEN',process_iter=lambda attrs:[process],NoSuchProcess=ProcessLookupError)
            with patch.dict(sys.modules,{'psutil':fake}):self.assertEqual(module.dedicated_owner(),expected)
    def test_existing_verified_browser_not_restarted(self):
        self.assertFalse(module.ensure(lambda:True,lambda:True,lambda:self.fail('unexpected launch'),lambda:True)['launched'])
    def test_missing_browser_launched_once_and_verified(self):
        checks=iter([False,True]);runs=iter([False,True]);calls=[]
        self.assertTrue(module.ensure(lambda:next(checks),lambda:next(runs),lambda:calls.append(1),lambda:True)['ready'])
        self.assertEqual(calls,[1])
    def test_wrong_port_owner_rejected(self):
        with self.assertRaisesRegex(RuntimeError,'unverified'):module.ensure(lambda:True,lambda:False,lambda:self.fail())
    def test_unrelated_listener_rejected_even_with_dedicated_process(self):
        with self.assertRaisesRegex(RuntimeError,'unverified'):module.ensure(lambda:True,lambda:True,lambda:self.fail(),lambda:False)
    def test_locked_running_profile_not_restarted(self):
        with self.assertRaisesRegex(RuntimeError,'CDP unavailable'):module.ensure(lambda:False,lambda:True,lambda:self.fail())
    def test_launch_result_alone_not_success(self):
        with self.assertRaisesRegex(RuntimeError,'readiness'):module.ensure(lambda:False,lambda:False,lambda:True)


if __name__=='__main__':unittest.main()
