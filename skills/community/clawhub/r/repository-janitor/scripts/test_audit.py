#!/usr/bin/env python3
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import time
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("janitor", Path(__file__).with_name("audit.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class Regression(unittest.TestCase):
    def config(self, path):
        return {"repositories":[{"id":"fixture","path":str(path),"github":"fixture/test"}],
                "budget_seconds":30,"command_timeout_seconds":2}
    def test_non_git_is_not_ok(self):
        with tempfile.TemporaryDirectory() as d:
            a=m.Audit(self.config(d))
            a.repository(a.config["repositories"][0])
            self.assertTrue(a.errors)
            self.assertFalse(a.summaries)
    def test_timeout_is_unknown(self):
        with patch.object(m.subprocess, "run", side_effect=subprocess.TimeoutExpired("git",1)):
            with self.assertRaises(m.Unknown): m.Runner().run(["git"])
    def test_budget(self):
        with self.assertRaises(m.Unknown): m.Runner(budget=0).run(["git"])
    def test_unknown_does_not_resolve(self):
        old={"x":{"scope":"r","label":"pending","severity":2,"status":"new","first_seen":"0"}}
        result=m.fold(old,{},set(),"1")
        self.assertNotEqual(result["x"]["status"],"resolved")
        self.assertTrue(result["x"]["uncertain"])
    def test_confirmed_resolution(self):
        old={"x":{"scope":"r","label":"pending","severity":2,"status":"new","first_seen":"0"}}
        self.assertEqual(m.fold(old,{},{"r"},"1")["x"]["status"],"resolved")
    def test_escalation(self):
        old={"x":{"scope":"r","label":"pending","severity":1,"status":"new","first_seen":"0"}}
        new={"x":{"scope":"r","label":"pending","severity":3}}
        self.assertEqual(m.fold(old,new,{"r"},"1")["x"]["status"],"worsened")
    def test_failed_check_continues(self):
        a=m.Audit({"repositories":[]})
        a.check("bad",lambda: (_ for _ in ()).throw(m.Unknown("failed")))
        a.check("good",lambda: None)
        self.assertIn("good",a.completed)
        self.assertEqual(len(a.errors),1)
    def test_atomic_private_state(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"state/latest.json"
            m.atomic(p,{"test":True})
            self.assertTrue(json.loads(p.read_text())["test"])
            self.assertEqual(p.stat().st_mode & 0o777,0o600)
    def test_real_worktrees_individually(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"repo"; p.mkdir()
            def git(*args):
                subprocess.run(["git","-C",str(p),*args],check=True,capture_output=True)
            git("init")
            git("-c","user.name=Fixture","-c","user.email=fixture@example.invalid",
                "commit","--allow-empty","-m","fixture")
            wt=Path(d)/"linked"
            git("worktree","add","-b","fixture",str(wt))
            (wt/"untracked.txt").write_text("test")
            a=m.Audit(self.config(p))
            a.repository(a.config["repositories"][0])
            trees=[v for k,v in a.observations.items() if "/wt/" in k and isinstance(v,dict) and "dirty_count" in v]
            self.assertEqual(len(trees),2)
            self.assertEqual(sum(v["dirty_count"] for v in trees),1)
    def test_no_clean_conclusion_on_error(self):
        text=m.render({"checked_at":"now","findings":{},"repositories":[],"errors":[{"scope":"git","error":"timeout"}]})
        self.assertNotIn("No decision needed",text)

class WatchdogTests(unittest.TestCase):
    def setUp(self):
        spec=importlib.util.spec_from_file_location("watchdog",Path(__file__).with_name("watchdog.py"))
        self.w=importlib.util.module_from_spec(spec); spec.loader.exec_module(self.w)
        self.now=1000000000
        self.job={"enabled":True,"state":{"lastRunAtMs":self.now-1000,
            "lastRunStatus":"ok","lastDeliveryStatus":"delivered"}}
    def test_healthy(self): self.assertEqual(self.w.health(self.job,self.now),"healthy")
    def test_disabled(self):
        self.job["enabled"]=False
        self.assertEqual(self.w.health(self.job,self.now),"disabled")
    def test_stale(self):
        self.job["state"]["lastRunAtMs"]=1
        self.assertIn("27 hours",self.w.health(self.job,self.now))
    def test_delivery_failed(self):
        self.job["state"]["lastDeliveryStatus"]="not-delivered"
        self.assertIn("delivery",self.w.health(self.job,self.now))

if __name__=="__main__": unittest.main()

