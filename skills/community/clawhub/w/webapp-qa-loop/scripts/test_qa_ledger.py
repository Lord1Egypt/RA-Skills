#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCRIPT = Path(__file__).with_name("qa_ledger.py")
BASE = datetime(2026, 8, 25, 1, 0, 0, tzinfo=timezone.utc)


class LedgerV2CliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.run_dir = self.root / "运行 qa"
        self.tick = 0

    def tearDown(self) -> None:
        self.temp.cleanup()

    def cli(self, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        at = (BASE + timedelta(seconds=self.tick)).isoformat().replace("+00:00", "Z")
        self.tick += 1
        command = [sys.executable, str(SCRIPT), "--run-dir", str(self.run_dir), "--at", at, *args]
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(command, text=True, capture_output=True, encoding="utf-8", env=environment)
        self.assertEqual(
            expected,
            result.returncode,
            msg=f"command: {command}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        return result

    def cli_at(self, at: str, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(SCRIPT), "--run-dir", str(self.run_dir), "--at", at, *args]
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(command, text=True, capture_output=True, encoding="utf-8", env=environment)
        self.assertEqual(
            expected,
            result.returncode,
            msg=f"command: {command}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        return result

    def init(self, mode: str = "audit", repair: bool | None = None, depth: str = "smoke") -> None:
        args = [
            "init", "--name", "中文质量运行", "--mode", mode, "--depth", depth,
            "--scope", "登录与工作台", "--project", "示例项目",
        ]
        if repair is not None:
            args.extend(["--repair-authorized", str(repair).lower()])
        self.cli(*args)

    def target(
        self,
        name: str = "local",
        environment: str = "local",
        url: str = "http://127.0.0.1:3000",
        authorization: str | None = None,
        production: bool = False,
    ) -> str:
        args = [
            "declare-target", "--name", name, "--environment", environment,
            "--url", url, "--immutable-id", f"provider/account/project/{environment}/region",
        ]
        if authorization:
            args.extend(["--authorization-source", authorization])
        if production:
            args.append("--production")
        else:
            args.append("--isolated")
        return self.cli(*args).stdout.strip()

    def scenario(
        self,
        target: str,
        risk: str = "A",
        level: str = "R1",
        issue: str | None = None,
        name: str = "有效输入",
    ) -> str:
        args = [
            "declare-scenario", "--flow", "核心流程", "--name", name,
            "--risk-class", risk, "--target", target, "--route", "/",
            "--regression-level", level, "--required",
        ]
        if issue:
            args.extend(["--issue", issue])
        return self.cli(*args).stdout.strip()

    def plan(
        self,
        target: str,
        phase: str,
        kind: str,
        level: str = "R1",
        issue: str | None = None,
        name: str | None = None,
    ) -> str:
        args = [
            "declare-check", "--name", name or f"{phase}-{kind}", "--kind", kind,
            "--phase", phase, "--environment", self.target_environment(target),
            "--target", target, "--required", "--regression-level", level,
        ]
        if issue:
            args.extend(["--issue", issue])
        return self.cli(*args).stdout.strip()

    def target_environment(self, target_id: str) -> str:
        return next(item["environment"] for item in self.load()["targets"] if item["id"] == target_id)

    def issue(self, severity: str = "P1") -> str:
        return self.cli(
            "add", "--title", "按钮状态错误", "--area", "表单", "--kind", "functional",
            "--severity", severity, "--step", "打开页面", "--expected", "按钮可用",
            "--actual", "按钮禁用", "--before-evidence", "evidence/before.png",
            "--evidence", "evidence/repro.txt", "--next-action", "分析表单状态",
        ).stdout.strip()

    def advance_prefix(self) -> None:
        for state in ("DISCOVER", "BASELINE", "EXPLORE", "TRIAGE"):
            self.cli("advance", state)

    def load(self) -> dict:
        return json.loads((self.run_dir / "qa-ledger.json").read_text(encoding="utf-8"))

    def configure_release(
        self, target: str, artifact: str = "sha256:abc", rollback_authorized: bool = False,
        rollback_trigger: str | None = None,
    ) -> None:
        args = [
            "configure-release", "--target", target, "--intended-artifact", artifact,
            "--rollback-readiness", "ready", "--rollback-plan", "redeploy known-good image",
            "--rollback-execution-authorized", str(rollback_authorized).lower(),
            "--rollback-recovery-artifact", "sha256:known-good",
        ]
        if rollback_authorized:
            args.extend(["--rollback-authorization-source", "current task: rollback on named trigger"])
        if rollback_trigger:
            args.extend(["--rollback-trigger", rollback_trigger])
        self.cli(*args)

    def declare_attempt_at_local_verify(self) -> str:
        return self.cli("declare-attempt").stdout.strip()

    def gate_browser_pass(
        self, target: str, scenario: str, attempt: str, phase: str = "baseline",
    ) -> None:
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", phase,
            "--result", "pass", "--target", target, "--artifact", "sha256:abc",
            "--attempt", attempt, "--evidence", f"evidence/{scenario}-{phase}-gate.png",
        )

    def test_01_init_unicode_and_writes_only_run_dir(self) -> None:
        self.init()
        self.cli("validate")
        data = self.load()
        self.assertEqual(2, data["schema_version"])
        self.assertEqual("中文质量运行", data["run"]["name"])
        self.assertEqual({"qa-ledger.json"}, {path.name for path in self.run_dir.iterdir()})

    def test_02_state_jump_is_rejected_without_mutation(self) -> None:
        self.init()
        before = (self.run_dir / "qa-ledger.json").read_bytes()
        self.cli("advance", "REPORT", expected=3)
        self.assertEqual(before, (self.run_dir / "qa-ledger.json").read_bytes())

    def test_03_audit_success_accounts_for_declared_pass(self) -> None:
        self.init()
        target = self.target()
        scenario = self.scenario(target)
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/pass.png",
        )
        self.cli("advance", "REPORT")
        self.cli("validate", "--strict")

    def test_04_audit_can_succeed_with_open_evidenced_defect(self) -> None:
        self.init()
        target = self.target()
        issue = self.issue()
        scenario = self.scenario(target, issue=issue)
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "fail", "--target", target, "--issue", issue,
            "--details", "button remains disabled", "--evidence", "evidence/fail.png",
        )
        self.cli("advance", "REPORT")
        self.cli("validate", "--strict")
        self.assertEqual("open", self.load()["issues"][0]["status"])

    def test_05_audit_failure_without_result_evidence_cannot_succeed(self) -> None:
        self.init()
        target = self.target()
        issue = self.issue()
        scenario = self.scenario(target, issue=issue)
        self.advance_prefix()
        result = self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "fail", "--target", target, "--issue", issue,
            "--details", "confirmed",
            expected=3,
        )
        self.assertIn("reproduction evidence", result.stderr)

    def test_06_undeclared_scenario_and_cross_target_are_rejected(self) -> None:
        self.init()
        first = self.target()
        second = self.target("other", "other", "http://127.0.0.1:4000")
        scenario = self.scenario(first)
        self.cli(
            "add-coverage", "--scenario", "SCN-999", "--phase", "baseline",
            "--result", "pass", "--target", first, expected=4,
        )
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "pass", "--target", second, expected=3,
        )

    def test_07_repair_requires_structured_evidence_and_r0_r1(self) -> None:
        self.init(mode="repair", repair=True, depth="targeted")
        target = self.target()
        issue = self.issue()
        r0 = self.scenario(target, level="R0", issue=issue, name="精确复现")
        r1 = self.scenario(target, level="R1", issue=issue, name="相邻状态")
        self.advance_prefix()
        self.cli("update", issue, "--status", "investigating")
        self.cli("advance", "REPAIR")
        self.cli("add-evidence", issue, "--kind", "repair", "--ref", "evidence/diff.txt")
        self.cli(
            "update", issue, "--status", "fixed", "--root-cause", "派生状态遗漏字段",
            "--resolution", "扩展有效性选择器", "--approach", "extend",
            "--reused", "现有表单选择器",
        )
        self.cli("advance", "LOCAL_VERIFY")
        self.cli("add-evidence", issue, "--kind", "after", "--ref", "evidence/after.png")
        for scenario in (r0, r1):
            self.cli(
                "add-coverage", "--scenario", scenario, "--phase", "post-fix",
                "--result", "pass", "--target", target, "--issue", issue,
                "--evidence", f"evidence/{scenario}.png",
            )
        self.cli(
            "update", issue, "--status", "verified", "--verification", "R0/R1通过",
        )
        self.cli("advance", "REPORT")
        self.cli("validate", "--strict")

    def test_08_verified_issue_rejects_missing_after_and_r1(self) -> None:
        self.init(mode="repair", repair=True)
        target = self.target()
        issue = self.issue()
        r0 = self.scenario(target, level="R0", issue=issue)
        self.advance_prefix()
        self.cli("update", issue, "--status", "investigating")
        self.cli("advance", "REPAIR")
        self.cli("add-evidence", issue, "--kind", "repair", "--ref", "evidence/diff.txt")
        self.cli(
            "update", issue, "--status", "fixed", "--root-cause", "x",
            "--resolution", "y", "--approach", "extend",
        )
        self.cli("advance", "LOCAL_VERIFY")
        self.cli(
            "add-coverage", "--scenario", r0, "--phase", "post-fix",
            "--result", "pass", "--target", target, "--issue", issue,
        )
        result = self.cli(
            "update", issue, "--status", "verified", expected=3,
        )
        self.assertIn("after evidence", result.stderr)
        self.assertIn("R1", result.stderr)

    def release_until_deploy(
        self, rollback_authorized: bool = False, rollback_trigger: str | None = None,
    ) -> tuple[str, str, str, str, str]:
        self.init(mode="release", repair=False, depth="release-regression")
        deployment_scope = "current task: deploy staging"
        target = self.target(
            "staging", "staging", "https://staging.example.test",
            authorization=deployment_scope,
        )
        scenario = self.scenario(target, risk="A", level="R4", name="发布冒烟")
        pre = self.plan(target, "pre-deploy", "build", level="R3")
        health = self.plan(target, "post-deploy", "health", level="R4")
        self.configure_release(
            target, rollback_authorized=rollback_authorized, rollback_trigger=rollback_trigger,
        )
        self.advance_prefix()
        self.cli("advance", "LOCAL_VERIFY")
        attempt = self.declare_attempt_at_local_verify()
        self.gate_browser_pass(target, scenario, attempt)
        self.cli(
            "add-check", "--plan", pre, "--result", "pass", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt, "--details", "build passed",
            "--evidence", "reports/build.txt",
        )
        self.cli("advance", "RELEASE_GATE")
        self.cli("release-gate", "--attempt", attempt)
        self.cli("advance", "DEPLOY")
        return target, scenario, pre, health, attempt

    def full_release_until_remote(self) -> tuple[str, str, str, str, str]:
        target, scenario, pre, health, attempt = self.release_until_deploy()
        self.cli(
            "record-deployment", "--attempt", attempt, "--result", "pass",
            "--observed-artifact", "sha256:abc", "--evidence", "provider/deploy/123",
        )
        self.cli("advance", "REMOTE_VERIFY")
        return target, scenario, pre, health, attempt

    def finish_release(self, target: str, scenario: str, health: str, attempt: str) -> None:
        self.cli(
            "add-check", "--plan", health, "--result", "pass", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt, "--details", "healthy",
            "--evidence", "provider/health/123",
        )
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "post-deploy",
            "--result", "pass", "--target", target, "--artifact", "sha256:abc",
            "--attempt", attempt, "--evidence", "evidence/staging-smoke.png",
        )
        self.cli("advance", "REPORT")
        self.cli("validate", "--strict")

    def test_09_release_without_repair_completes_bound_gate(self) -> None:
        target, scenario, _, health, attempt = self.full_release_until_remote()
        self.assertFalse(self.load()["run"]["repair_authorized"])
        self.finish_release(target, scenario, health, attempt)

    def test_10_release_rejects_cross_target_and_mixed_artifact(self) -> None:
        self.init(mode="release", repair=False, depth="release-regression")
        target = self.target("staging", "staging", "https://staging.example.test", "current task")
        other = self.target("other", "staging", "https://other.example.test", "current task")
        pre = self.plan(target, "pre-deploy", "build")
        self.configure_release(target)
        self.advance_prefix()
        self.cli("advance", "LOCAL_VERIFY")
        attempt = self.declare_attempt_at_local_verify()
        self.cli(
            "add-check", "--plan", pre, "--result", "pass", "--target", other,
            "--artifact", "sha256:abc", "--attempt", attempt,
            "--evidence", "reports/wrong-target.txt", expected=3,
        )
        self.cli(
            "add-check", "--plan", pre, "--result", "pass", "--target", target,
            "--artifact", "sha256:wrong", "--attempt", attempt,
            "--evidence", "reports/wrong-artifact.txt", expected=3,
        )

    def test_11_release_gate_requires_predeploy_plan_and_pass(self) -> None:
        self.init(mode="release", repair=False)
        target = self.target("staging", "staging", "https://staging.example.test", "current task")
        self.configure_release(target)
        self.advance_prefix()
        self.cli("advance", "LOCAL_VERIFY")
        attempt = self.declare_attempt_at_local_verify()
        self.cli("advance", "RELEASE_GATE")
        result = self.cli("release-gate", "--attempt", attempt, expected=3)
        self.assertIn("pre-deploy", result.stderr)

    def test_12_newer_predeploy_failure_invalidates_old_gate(self) -> None:
        self.init(mode="release", repair=False)
        target = self.target("staging", "staging", "https://staging.example.test", "current task")
        scenario = self.scenario(target, risk="A", level="R4", name="发布冒烟")
        pre = self.plan(target, "pre-deploy", "build")
        self.plan(target, "post-deploy", "health", level="R4")
        self.configure_release(target)
        self.advance_prefix()
        self.cli("advance", "LOCAL_VERIFY")
        attempt = self.declare_attempt_at_local_verify()
        self.gate_browser_pass(target, scenario, attempt)
        self.cli(
            "add-check", "--plan", pre, "--result", "pass", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt,
            "--evidence", "reports/build-pass.txt",
        )
        self.cli("advance", "RELEASE_GATE")
        self.cli("release-gate", "--attempt", attempt)
        self.cli(
            "add-check", "--plan", pre, "--result", "fail", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt, "--details", "new failure",
            "--evidence", "reports/build-fail.txt",
        )
        self.assertEqual("pending", self.load()["release"]["gate"]["status"])
        self.cli("advance", "DEPLOY", expected=3)

    def test_13_deploy_and_observed_artifact_require_gate_and_match(self) -> None:
        self.init(mode="release", repair=False)
        target = self.target("staging", "staging", "https://staging.example.test", "current task")
        scenario = self.scenario(target, risk="A", level="R4", name="发布冒烟")
        pre = self.plan(target, "pre-deploy", "build")
        self.plan(target, "post-deploy", "health", level="R4")
        self.configure_release(target)
        self.advance_prefix()
        self.cli("advance", "LOCAL_VERIFY")
        attempt = self.declare_attempt_at_local_verify()
        self.gate_browser_pass(target, scenario, attempt)
        self.cli("advance", "RELEASE_GATE")
        self.cli("advance", "DEPLOY", expected=3)
        self.cli(
            "add-check", "--plan", pre, "--result", "pass", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt,
            "--evidence", "reports/build-pass.txt",
        )
        self.cli("release-gate", "--attempt", attempt)
        self.cli("advance", "DEPLOY")
        self.cli(
            "record-deployment", "--attempt", attempt, "--result", "pass",
            "--observed-artifact", "sha256:wrong", expected=3,
        )

    def test_14_latest_postdeploy_failure_cannot_be_hidden(self) -> None:
        target, scenario, _, health, attempt = self.full_release_until_remote()
        for result in ("pass", "fail"):
            self.cli(
                "add-check", "--plan", health, "--result", result, "--target", target,
                "--artifact", "sha256:abc", "--attempt", attempt,
                "--details", f"latest={result}", "--evidence", f"provider/health/{result}",
            )
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "post-deploy",
            "--result", "pass", "--target", target, "--artifact", "sha256:abc",
            "--attempt", attempt, "--evidence", "evidence/smoke.png",
        )
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn("latest result is fail", result.stderr)

    def test_15_production_target_requires_current_task_identity(self) -> None:
        self.init(mode="release", repair=False)
        result = self.cli(
            "declare-target", "--name", "prod", "--environment", "production",
            "--url", "https://example.com", "--production", expected=3,
        )
        self.assertIn("current task", result.stderr)

    def test_16_summary_resume_is_read_only_and_complete(self) -> None:
        self.init()
        target = self.target()
        self.cli(
            "update", "RUN", "--current-target", target, "--current-url",
            "http://127.0.0.1:3000/login", "--next-action", "继续登录失败态",
            "--note", "浏览器停在登录页", "--cleanup-status", "residual",
            "--cleanup-details", "qa-user-123 remains",
        )
        ledger = self.run_dir / "qa-ledger.json"
        before_hash = hashlib.sha256(ledger.read_bytes()).hexdigest()
        before_mtime = ledger.stat().st_mtime_ns
        result = self.cli("summary", "--format", "markdown")
        self.assertIn("继续登录失败态", result.stdout)
        self.assertIn("qa-user-123", result.stdout)
        self.cli("validate", "--format", "json")
        self.assertEqual(before_hash, hashlib.sha256(ledger.read_bytes()).hexdigest())
        self.assertEqual(before_mtime, ledger.stat().st_mtime_ns)

    def test_17_schema_v1_is_rejected_without_traceback(self) -> None:
        self.run_dir.mkdir()
        (self.run_dir / "qa-ledger.json").write_text('{"schema_version": 1}\n', encoding="utf-8")
        result = self.cli("validate", expected=3)
        self.assertIn("schema v1 is unsupported", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_18_nonempty_dir_time_reversal_and_stale_lock(self) -> None:
        self.run_dir.mkdir()
        sentinel = self.run_dir / "keep.txt"
        sentinel.write_text("keep", encoding="utf-8")
        self.cli(
            "init", "--name", "bad", "--mode", "audit", "--depth", "smoke",
            "--scope", "x", expected=4,
        )
        self.assertEqual("keep", sentinel.read_text(encoding="utf-8"))
        sentinel.unlink()
        self.run_dir.rmdir()
        self.init()
        before = (self.run_dir / "qa-ledger.json").read_bytes()
        self.tick = -1
        self.cli("update", "RUN", "--note", "past", expected=3)
        self.assertEqual(before, (self.run_dir / "qa-ledger.json").read_bytes())
        self.tick = 2
        lock = self.run_dir / ".qa-ledger.lock"
        lock.write_text("stale", encoding="utf-8")
        old = time.time() - 600
        os.utime(lock, (old, old))
        self.cli("update", "RUN", "--note", "recovered")
        self.assertFalse(lock.exists())

    def test_19_malformed_v2_validate_has_no_traceback(self) -> None:
        self.run_dir.mkdir()
        (self.run_dir / "qa-ledger.json").write_text(
            '{"schema_version":2,"run":{},"counters":{},"targets":[null]}\n',
            encoding="utf-8",
        )
        result = self.cli("validate", expected=3)
        self.assertIn("INVALID", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_20_success_needs_declared_browser_scenario(self) -> None:
        self.init()
        self.advance_prefix()
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn("declared browser scenario", result.stderr)
        self.cli("advance", "REPORT", "--settlement", "blocked", "--reason", "No runnable browser target")
        strict = self.cli("validate", "--strict", expected=3)
        self.assertIn("blocked", strict.stdout)

    def test_21_postfix_and_after_cannot_predate_fix(self) -> None:
        self.init(mode="repair", repair=True)
        target = self.target()
        issue = self.issue()
        scenario = self.scenario(target, level="R0", issue=issue)
        self.advance_prefix()
        self.cli("update", issue, "--status", "investigating")
        self.cli("advance", "LOCAL_VERIFY")
        result = self.cli(
            "add-evidence", issue, "--kind", "after", "--ref", "evidence/too-early.png",
            expected=3,
        )
        self.assertIn("fixed first", result.stderr)
        result = self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "post-fix",
            "--result", "pass", "--target", target, "--issue", issue,
            "--evidence", "evidence/too-early-r0.png", expected=3,
        )
        self.assertIn("not yet fixed", result.stderr)

    def test_22_any_gate_check_change_requires_new_gate(self) -> None:
        self.init(mode="release", repair=False)
        target = self.target("staging", "staging", "https://staging.example.test", "current task")
        scenario = self.scenario(target, risk="A", level="R4", name="发布冒烟")
        baseline = self.plan(target, "baseline", "test", level="R2")
        self.plan(target, "pre-deploy", "build", level="R3")
        self.plan(target, "post-deploy", "health", level="R4")
        self.configure_release(target)
        self.advance_prefix()
        self.cli("advance", "LOCAL_VERIFY")
        attempt = self.declare_attempt_at_local_verify()
        self.gate_browser_pass(target, scenario, attempt)
        for plan, evidence in ((baseline, "reports/baseline.txt"), ("PLN-002", "reports/build.txt")):
            self.cli(
                "add-check", "--plan", plan, "--result", "pass", "--target", target,
                "--artifact", "sha256:abc", "--attempt", attempt, "--evidence", evidence,
            )
        self.cli("advance", "RELEASE_GATE")
        self.cli("release-gate", "--attempt", attempt)
        self.cli(
            "add-check", "--plan", baseline, "--result", "fail", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt,
            "--details", "new baseline failure", "--evidence", "reports/baseline-fail.txt",
        )
        self.assertEqual("pending", self.load()["release"]["gate"]["status"])
        self.cli("advance", "DEPLOY", expected=3)

    def test_23_absolute_path_and_huge_id_fail_cleanly(self) -> None:
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        relative = subprocess.run(
            [sys.executable, str(SCRIPT), "--run-dir", "~\\qa-relative", "validate"],
            text=True, capture_output=True, encoding="utf-8", env=environment,
        )
        self.assertEqual(3, relative.returncode)
        self.assertIn("must be absolute", relative.stderr)
        self.assertNotIn("Traceback", relative.stderr)
        self.init()
        self.target()
        data = self.load()
        data["targets"][0]["id"] = "TGT-" + "9" * 5000
        (self.run_dir / "qa-ledger.json").write_text(json.dumps(data), encoding="utf-8")
        result = self.cli("validate", expected=3)
        self.assertIn("INVALID", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_24_cleanup_state_is_part_of_success_gate(self) -> None:
        self.init()
        target = self.target()
        scenario = self.scenario(target)
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/pass.png",
        )
        self.cli("update", "RUN", "--cleanup-status", "pending")
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn("cleanup is still pending", result.stderr)
        self.cli("update", "RUN", "--cleanup-status", "residual")
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn("named leftovers", result.stderr)
        self.cli(
            "update", "RUN", "--cleanup-status", "residual",
            "--cleanup-details", "qa-user remains by explicit test constraint",
        )
        self.cli("advance", "REPORT")

    def test_25_passing_check_requires_evidence(self) -> None:
        self.init()
        target = self.target()
        plan = self.plan(target, "baseline", "test")
        self.cli("advance", "DISCOVER")
        self.cli("advance", "BASELINE")
        result = self.cli(
            "add-check", "--plan", plan, "--result", "pass", "--target", target,
            expected=3,
        )
        self.assertIn("requires evidence", result.stderr)

    def test_26_release_repaired_p2_needs_remote_r0_and_r1(self) -> None:
        self.init(mode="release", repair=True, depth="release-regression")
        target = self.target("staging", "staging", "https://staging.example.test", "current task")
        issue = self.issue(severity="P2")
        r0 = self.cli(
            "declare-scenario", "--flow", "缺陷回归", "--name", "精确复现",
            "--risk-class", "C", "--target", target, "--regression-level", "R0",
            "--optional", "--issue", issue,
        ).stdout.strip()
        r1 = self.cli(
            "declare-scenario", "--flow", "缺陷回归", "--name", "相邻行为",
            "--risk-class", "C", "--target", target, "--regression-level", "R1",
            "--optional", "--issue", issue,
        ).stdout.strip()
        smoke = self.scenario(target, risk="A", level="R4", name="发布冒烟")
        pre = self.plan(target, "pre-deploy", "build", level="R3")
        health = self.plan(target, "post-deploy", "health", level="R4")
        self.configure_release(target)
        self.advance_prefix()
        self.cli("update", issue, "--status", "investigating")
        self.cli("advance", "REPAIR")
        self.cli("add-evidence", issue, "--kind", "repair", "--ref", "evidence/diff.txt")
        self.cli(
            "update", issue, "--status", "fixed", "--root-cause", "遗漏状态",
            "--resolution", "复用并扩展选择器", "--approach", "extend",
        )
        self.cli("advance", "LOCAL_VERIFY")
        attempt = self.declare_attempt_at_local_verify()
        self.cli("add-evidence", issue, "--kind", "after", "--ref", "evidence/after.png")
        for scenario in (r0, r1):
            self.cli(
                "add-coverage", "--scenario", scenario, "--phase", "post-fix",
                "--result", "pass", "--target", target, "--artifact", "sha256:abc",
                "--attempt", attempt, "--issue", issue, "--evidence", f"evidence/{scenario}-local.png",
            )
        self.cli("update", issue, "--status", "verified")
        self.gate_browser_pass(target, smoke, attempt, phase="post-fix")
        self.cli(
            "add-check", "--plan", pre, "--result", "pass", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt, "--evidence", "reports/build.txt",
        )
        self.cli("advance", "RELEASE_GATE")
        self.cli("release-gate", "--attempt", attempt)
        self.cli("advance", "DEPLOY")
        self.cli(
            "record-deployment", "--attempt", attempt, "--result", "pass",
            "--observed-artifact", "sha256:abc", "--evidence", "provider/deploy/123",
        )
        self.cli("advance", "REMOTE_VERIFY")
        self.cli(
            "add-check", "--plan", health, "--result", "pass", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt, "--evidence", "provider/health/123",
        )
        for scenario in (smoke, r0):
            self.cli(
                "add-coverage", "--scenario", scenario, "--phase", "post-deploy",
                "--result", "pass", "--target", target, "--artifact", "sha256:abc",
                "--attempt", attempt, "--evidence", f"evidence/{scenario}-remote.png",
            )
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn("post-deploy R1", result.stderr)

    def test_27_linked_failure_cannot_be_hidden_by_other_pass(self) -> None:
        self.init(mode="repair", repair=True)
        target = self.target()
        issue = self.issue()
        r0a = self.scenario(target, level="R0", issue=issue, name="精确路径A")
        r0b = self.scenario(target, level="R0", issue=issue, name="精确路径B")
        r1 = self.scenario(target, level="R1", issue=issue, name="相邻路径")
        self.advance_prefix()
        self.cli("update", issue, "--status", "investigating")
        self.cli("advance", "REPAIR")
        self.cli("add-evidence", issue, "--kind", "repair", "--ref", "evidence/diff.txt")
        self.cli(
            "update", issue, "--status", "fixed", "--root-cause", "遗漏分支",
            "--resolution", "扩展已有分支", "--approach", "extend",
        )
        self.cli("advance", "LOCAL_VERIFY")
        self.cli("add-evidence", issue, "--kind", "after", "--ref", "evidence/after.png")
        for scenario, outcome in ((r0a, "pass"), (r0b, "fail"), (r1, "pass"), (r0a, "pass")):
            self.cli(
                "add-coverage", "--scenario", scenario, "--phase", "post-fix",
                "--result", outcome, "--target", target, "--issue", issue,
                "--details", f"{scenario}={outcome}",
                "--evidence", f"evidence/{scenario}-{outcome}-{self.tick}.png",
            )
        result = self.cli("update", issue, "--status", "verified", expected=3)
        self.assertIn("post-fix R0", result.stderr)
        self.cli(
            "add-coverage", "--scenario", r0b, "--phase", "post-fix",
            "--result", "pass", "--target", target, "--issue", issue,
            "--evidence", "evidence/r0b-retest.png",
        )
        self.cli("update", issue, "--status", "verified")

    def test_28_verified_issue_must_reopen_before_new_repair(self) -> None:
        self.init(mode="repair", repair=True)
        target = self.target()
        issue = self.issue()
        r0 = self.scenario(target, level="R0", issue=issue, name="精确路径")
        r1 = self.scenario(target, level="R1", issue=issue, name="相邻路径")
        self.advance_prefix()
        self.cli("update", issue, "--status", "investigating")
        self.cli("advance", "REPAIR")
        self.cli("add-evidence", issue, "--kind", "repair", "--ref", "evidence/diff-1.txt")
        self.cli(
            "update", issue, "--status", "fixed", "--root-cause", "原因一",
            "--resolution", "修复一", "--approach", "extend",
        )
        self.cli("advance", "LOCAL_VERIFY")
        self.cli("add-evidence", issue, "--kind", "after", "--ref", "evidence/after-1.png")
        for scenario in (r0, r1):
            self.cli(
                "add-coverage", "--scenario", scenario, "--phase", "post-fix",
                "--result", "pass", "--target", target, "--evidence", f"evidence/{scenario}-1.png",
            )
        self.cli("update", issue, "--status", "verified")
        self.cli("advance", "REPAIR")
        result = self.cli(
            "add-evidence", issue, "--kind", "repair", "--ref", "evidence/diff-2.txt",
            expected=3,
        )
        self.assertIn("investigating issue", result.stderr)
        result = self.cli(
            "update", issue, "--resolution", "偷偷修改已验证修复", "--approach", "new",
            expected=3,
        )
        self.assertIn("investigating issue", result.stderr)
        self.cli("update", issue, "--status", "investigating")
        self.assertEqual("", self.load()["issues"][0]["fixed_at"])
        result = self.cli(
            "update", issue, "--status", "fixed", "--root-cause", "原因二",
            "--resolution", "修复二", "--approach", "extend", expected=3,
        )
        self.assertIn("current repair cycle", result.stderr)

    def test_29_optional_declaration_must_be_accounted_for(self) -> None:
        self.init()
        target = self.target()
        required = self.scenario(target, name="必测路径")
        optional = self.cli(
            "declare-scenario", "--flow", "探索", "--name", "可选路径",
            "--risk-class", "C", "--target", target, "--regression-level", "R2", "--optional",
        ).stdout.strip()
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", required, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/required.png",
        )
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn(optional, result.stderr)
        self.cli(
            "add-coverage", "--scenario", optional, "--phase", "baseline",
            "--result", "skipped", "--target", target,
            "--details", "第三方沙箱当前不可用",
        )
        self.cli("advance", "REPORT")

    def test_30_required_class_c_failure_blocks_repair_success(self) -> None:
        self.init(mode="repair", repair=True)
        target = self.target()
        issue = self.issue(severity="P2")
        scenario = self.scenario(target, risk="C", level="R2", issue=issue, name="必测边界")
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "fail", "--target", target, "--issue", issue,
            "--details", "边界行为失败",
            "--evidence", "evidence/class-c-fail.png",
        )
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn("gating scenario", result.stderr)

    def test_31_deeply_nested_json_fails_without_traceback(self) -> None:
        self.run_dir.mkdir()
        payload = '{"schema_version":2,"x":' + "[" * 5000 + "0" + "]" * 5000 + "}"
        (self.run_dir / "qa-ledger.json").write_text(payload, encoding="utf-8")
        result = self.cli("validate", expected=5)
        self.assertIn("cannot read ledger", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_32_strict_validation_rejects_tampered_release_binding(self) -> None:
        target, scenario, _, health, attempt = self.full_release_until_remote()
        self.finish_release(target, scenario, health, attempt)
        base = self.load()
        mutations = {
            "attempt target": lambda value: value["deployment_attempts"][0].__setitem__("target_id", "TGT-999"),
            "attempt artifact": lambda value: value["deployment_attempts"][0].__setitem__("intended_artifact", "sha256:evil"),
            "rollback readiness": lambda value: value["release"]["rollback"].update({"readiness": "not-ready", "plan": ""}),
            "gate timestamp": lambda value: value["release"]["gate"].__setitem__("passed_at", ""),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                value = json.loads(json.dumps(base))
                mutate(value)
                (self.run_dir / "qa-ledger.json").write_text(json.dumps(value), encoding="utf-8")
                result = self.cli("validate", "--strict", expected=3)
                self.assertIn("INVALID", result.stdout)
                self.assertNotIn("Traceback", result.stderr)

    def test_33_repaired_p2_must_be_verified(self) -> None:
        self.init(mode="repair", repair=True)
        target = self.target()
        issue = self.issue(severity="P2")
        scenario = self.scenario(target, risk="A", level="R2", name="核心回归")
        self.advance_prefix()
        self.cli("update", issue, "--status", "investigating")
        self.cli("advance", "REPAIR")
        self.cli("add-evidence", issue, "--kind", "repair", "--ref", "evidence/p2-diff.txt")
        self.cli(
            "update", issue, "--status", "fixed", "--root-cause", "P2原因",
            "--resolution", "P2修复", "--approach", "extend",
        )
        self.cli("advance", "LOCAL_VERIFY")
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "post-fix",
            "--result", "pass", "--target", target, "--evidence", "evidence/core-pass.png",
        )
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn("repair work but is not verified", result.stderr)

    def test_34_every_linked_regression_declaration_needs_fresh_result(self) -> None:
        self.init(mode="repair", repair=True)
        target = self.target()
        issue = self.issue()
        r0_old = self.scenario(target, level="R0", issue=issue, name="旧R0")
        r0_new = self.scenario(target, level="R0", issue=issue, name="新R0")
        r1 = self.scenario(target, level="R1", issue=issue, name="R1")
        self.advance_prefix()
        self.cli("update", issue, "--status", "investigating")
        self.cli(
            "add-coverage", "--scenario", r0_old, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/r0-old.png",
        )
        self.cli("advance", "REPAIR")
        self.cli("add-evidence", issue, "--kind", "repair", "--ref", "evidence/fresh-diff.txt")
        self.cli(
            "update", issue, "--status", "fixed", "--root-cause", "fresh",
            "--resolution", "fresh fix", "--approach", "extend",
        )
        self.cli("advance", "LOCAL_VERIFY")
        self.cli("add-evidence", issue, "--kind", "after", "--ref", "evidence/fresh-after.png")
        for scenario in (r0_new, r1):
            self.cli(
                "add-coverage", "--scenario", scenario, "--phase", "post-fix",
                "--result", "pass", "--target", target,
                "--evidence", f"evidence/{scenario}-fresh.png",
            )
        result = self.cli("update", issue, "--status", "verified", expected=3)
        self.assertIn("post-fix R0", result.stderr)

    def test_35_release_retry_returns_through_local_verify(self) -> None:
        self.init(mode="release", repair=False, depth="release-regression")
        target = self.target("staging", "staging", "https://staging.example.test", "current task")
        scenario = self.scenario(target, risk="A", level="R4", name="发布冒烟")
        postfix = self.plan(target, "post-fix", "test", level="R2")
        pre = self.plan(target, "pre-deploy", "build", level="R3")
        health = self.plan(target, "post-deploy", "health", level="R4")
        self.configure_release(target)
        self.advance_prefix()
        self.cli("advance", "LOCAL_VERIFY")
        first = self.declare_attempt_at_local_verify()
        self.gate_browser_pass(target, scenario, first)
        for plan in (postfix, pre):
            self.cli(
                "add-check", "--plan", plan, "--result", "pass", "--target", target,
                "--artifact", "sha256:abc", "--attempt", first,
                "--evidence", f"reports/{plan}-first.txt",
            )
        self.cli("advance", "RELEASE_GATE")
        self.cli("release-gate", "--attempt", first)
        self.cli("advance", "DEPLOY")
        self.cli(
            "record-deployment", "--attempt", first, "--result", "unknown",
            "--details", "provider request timed out; target state is not reconciled",
            "--evidence", "provider/unknown/1",
        )
        result = self.cli("advance", "LOCAL_VERIFY", expected=3)
        self.assertIn("failed-unchanged", result.stderr)
        self.cli(
            "record-deployment", "--attempt", first, "--result", "failed-unchanged",
            "--observed-artifact", "sha256:known-good",
            "--details", "provider confirms rollout never started; target unchanged",
            "--evidence", "provider/reconciled/1",
        )
        self.cli("advance", "LOCAL_VERIFY")
        second = self.declare_attempt_at_local_verify()
        self.gate_browser_pass(target, scenario, second)
        for plan in (postfix, pre):
            self.cli(
                "add-check", "--plan", plan, "--result", "pass", "--target", target,
                "--artifact", "sha256:abc", "--attempt", second,
                "--evidence", f"reports/{plan}-second.txt",
            )
        self.cli("advance", "RELEASE_GATE")
        self.cli("release-gate", "--attempt", second)
        self.cli("advance", "DEPLOY")
        self.cli(
            "record-deployment", "--attempt", second, "--result", "pass",
            "--observed-artifact", "sha256:abc", "--evidence", "provider/deploy/2",
        )
        self.cli("advance", "REMOTE_VERIFY")
        self.cli(
            "add-check", "--plan", health, "--result", "pass", "--target", target,
            "--artifact", "sha256:abc", "--attempt", second, "--evidence", "provider/health/2",
        )
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "post-deploy",
            "--result", "pass", "--target", target, "--artifact", "sha256:abc",
            "--attempt", second, "--evidence", "evidence/retry-smoke.png",
        )
        self.cli("advance", "REPORT")
        self.cli("validate", "--strict")
        summary = self.cli("summary", "--format", "markdown").stdout
        self.assertIn(f"{first} [failed-unchanged", summary)
        self.assertIn("provider request timed out", summary)
        self.assertIn("provider confirms rollout never started", summary)
        self.assertIn(f"{second} [succeeded", summary)
        json_summary = json.loads(self.cli("summary", "--format", "json").stdout)
        self.assertEqual(2, len(json_summary["deployment_attempts"]))

    def test_36_remote_rollback_is_recorded_durably(self) -> None:
        self.init(mode="release", repair=False, depth="release-regression")
        target = self.target("staging", "staging", "https://staging.example.test", "current task")
        scenario = self.scenario(target, risk="A", level="R4", name="发布冒烟")
        pre = self.plan(target, "pre-deploy", "build", level="R3")
        health = self.plan(target, "post-deploy", "health", level="R4")
        self.cli(
            "configure-release", "--target", target, "--intended-artifact", "sha256:abc",
            "--rollback-readiness", "ready", "--rollback-plan", "redeploy known-good image",
            "--rollback-execution-authorized", "true",
            "--rollback-authorization-source", "current task: rollback on failed health",
            "--rollback-recovery-artifact", "sha256:known-good",
        )
        self.advance_prefix()
        self.cli("advance", "LOCAL_VERIFY")
        attempt = self.declare_attempt_at_local_verify()
        self.gate_browser_pass(target, scenario, attempt)
        self.cli(
            "add-check", "--plan", pre, "--result", "pass", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt, "--evidence", "reports/build.txt",
        )
        self.cli("advance", "RELEASE_GATE")
        self.cli("release-gate", "--attempt", attempt)
        self.cli("advance", "DEPLOY")
        self.cli(
            "record-deployment", "--attempt", attempt, "--result", "pass",
            "--observed-artifact", "sha256:abc", "--evidence", "provider/deploy/rollback-case",
        )
        self.cli("advance", "REMOTE_VERIFY")
        self.cli(
            "add-check", "--plan", health, "--result", "fail", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt, "--details", "readiness failed",
            "--evidence", "provider/health/fail",
        )
        self.cli(
            "record-rollback", "--attempt", attempt, "--result", "rolled-back",
            "--observed-artifact", "sha256:known-good", "--health-result", "pass",
            "--details", "known-good restored", "--evidence", "provider/rollback/1",
        )
        self.cli(
            "advance", "REPORT", "--settlement", "failed",
            "--reason", "new artifact failed readiness and was rolled back",
        )
        summary = self.cli("summary", "--format", "markdown").stdout
        self.assertIn("rolled-back", summary)
        self.assertIn("sha256:known-good", summary)
        self.cli("validate")

    def test_37_evidenced_scenario_exclusion_is_accounted(self) -> None:
        self.init(mode="repair", repair=True)
        target = self.target()
        applicable = self.scenario(target, risk="A", name="适用路径")
        excluded = self.scenario(target, risk="A", name="仅管理员路径")
        self.advance_prefix()
        self.cli(
            "set-disposition", excluded, "--status", "out",
            "--reason", "当前角色无管理员能力", "--evidence", "evidence/role-matrix.md",
        )
        self.cli(
            "add-coverage", "--scenario", applicable, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/applicable.png",
        )
        self.cli("advance", "REPORT")
        summary = self.cli("summary", "--format", "markdown").stdout
        self.assertIn(f"{excluded} A", summary)
        self.assertIn("disposition=out", summary)
        self.assertIn("当前角色无管理员能力", summary)
        self.assertIn("evidence/role-matrix.md", summary)

    def test_38_evidenced_baseline_debt_does_not_mask_required_gate(self) -> None:
        self.init(mode="repair", repair=True)
        target = self.target()
        scenario = self.scenario(target, risk="A", name="核心路径")
        broad = self.plan(target, "baseline", "test", level="R3")
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/core.png",
        )
        self.cli(
            "add-check", "--plan", broad, "--result", "fail", "--target", target,
            "--details", "known unrelated legacy suite failure", "--evidence", "reports/legacy-fail.txt",
        )
        self.cli(
            "set-disposition", broad, "--status", "baseline-debt",
            "--reason", "failure predates and does not consume changed module",
            "--evidence", "evidence/baseline-comparison.md",
        )
        self.cli("advance", "REPORT")
        summary = self.cli("summary", "--format", "markdown").stdout
        self.assertIn("disposition=baseline-debt", summary)
        self.assertIn("failure predates", summary)
        self.assertIn("evidence/baseline-comparison.md", summary)

    def test_39_issue_cannot_be_silently_downgraded_or_excluded(self) -> None:
        self.init()
        issue = self.issue(severity="P0")
        self.advance_prefix()
        result = self.cli("update", issue, "--severity", "P3", expected=3)
        self.assertIn("reason and classification evidence", result.stderr)
        result = self.cli(
            "update", issue, "--scope-status", "out", "--note", "not applicable",
            expected=3,
        )
        self.assertIn("classification evidence", result.stderr)
        self.cli(
            "update", issue, "--severity", "P3", "--note", "initial impact was overstated",
            "--classification-evidence", "evidence/impact-analysis.md",
        )
        history = self.load()["issues"][0]["classification_history"]
        self.assertEqual(("P0", "P3"), (history[-1]["old_severity"], history[-1]["new_severity"]))

    def test_40_failed_critical_browser_flow_blocks_release_gate(self) -> None:
        self.init(mode="release", repair=False)
        target = self.target("staging", "staging", "https://staging.example.test", "current task")
        issue = self.issue(severity="P1")
        scenario = self.scenario(target, risk="A", level="R4", issue=issue, name="关键下单")
        pre = self.plan(target, "pre-deploy", "build", level="R3")
        self.plan(target, "post-deploy", "health", level="R4")
        self.configure_release(target)
        self.advance_prefix()
        self.cli("advance", "LOCAL_VERIFY")
        attempt = self.declare_attempt_at_local_verify()
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "fail", "--target", target, "--artifact", "sha256:abc",
            "--attempt", attempt, "--details", "checkout remains blocked",
            "--evidence", "evidence/checkout-fail.png",
        )
        self.cli(
            "add-check", "--plan", pre, "--result", "pass", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt, "--evidence", "reports/build.txt",
        )
        self.cli("advance", "RELEASE_GATE")
        result = self.cli("release-gate", "--attempt", attempt, expected=3)
        self.assertIn("gating scenario", result.stderr)
        self.assertIn("blocks deployment", result.stderr)

    def test_41_initial_issue_exclusion_requires_evidence(self) -> None:
        self.init()
        result = self.cli(
            "add", "--title", "不适用问题", "--area", "权限", "--kind", "functional",
            "--severity", "P1", "--scope-status", "out", "--step", "访问管理员页",
            "--expected", "显示页面", "--actual", "角色无权限",
            "--before-evidence", "evidence/admin-page.png", expected=3,
        )
        self.assertIn("classification evidence", result.stderr)
        issue = self.cli(
            "add", "--title", "不适用问题", "--area", "权限", "--kind", "functional",
            "--severity", "P1", "--scope-status", "out", "--step", "访问管理员页",
            "--expected", "显示页面", "--actual", "角色无权限",
            "--before-evidence", "evidence/admin-page.png", "--note", "当前角色不是管理员",
            "--classification-evidence", "evidence/role-matrix.md",
        ).stdout.strip()
        self.assertEqual("out", next(item for item in self.load()["issues"] if item["id"] == issue)["scope_status"])

    def test_42_rollback_requires_recorded_execution_authority(self) -> None:
        target, _, _, _, attempt = self.full_release_until_remote()
        result = self.cli(
            "record-rollback", "--attempt", attempt, "--result", "rolled-back",
            "--observed-artifact", "sha256:known-good", "--health-result", "pass",
            "--details", f"recovered {target}", "--evidence", "provider/rollback/unauthorized",
            expected=3,
        )
        self.assertIn("not authorized", result.stderr)

    def test_43_new_browser_result_invalidates_gate_snapshot(self) -> None:
        self.init(mode="release", repair=False)
        target = self.target("staging", "staging", "https://staging.example.test", "current task")
        scenario = self.scenario(target, risk="A", level="R4", name="发布冒烟")
        pre = self.plan(target, "pre-deploy", "build", level="R3")
        self.plan(target, "post-deploy", "health", level="R4")
        self.configure_release(target)
        self.advance_prefix()
        self.cli("advance", "LOCAL_VERIFY")
        attempt = self.declare_attempt_at_local_verify()
        self.gate_browser_pass(target, scenario, attempt)
        self.cli(
            "add-check", "--plan", pre, "--result", "pass", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt, "--evidence", "reports/build.txt",
        )
        self.cli("advance", "RELEASE_GATE")
        self.cli("release-gate", "--attempt", attempt)
        self.gate_browser_pass(target, scenario, attempt)
        self.assertEqual("pending", self.load()["release"]["gate"]["status"])
        self.cli("advance", "DEPLOY", expected=3)

    def test_44_repair_success_rejects_open_in_scope_p2(self) -> None:
        self.init(mode="repair", repair=True)
        target = self.target()
        issue = self.issue(severity="P2")
        scenario = self.cli(
            "declare-scenario", "--flow", "辅助流程", "--name", "低风险异常",
            "--risk-class", "C", "--target", target, "--regression-level", "R2",
            "--optional", "--issue", issue,
        ).stdout.strip()
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "fail", "--target", target, "--issue", issue,
            "--details", "confirmed low-risk defect", "--evidence", "evidence/p2-open.png",
        )
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn("in scope and must be verified", result.stderr)

    def test_45_release_configuration_cannot_hide_unknown_attempt(self) -> None:
        target, _, _, _, attempt = self.release_until_deploy()
        self.cli(
            "record-deployment", "--attempt", attempt, "--result", "unknown",
            "--details", "provider timed out; actual target remains unknown",
            "--evidence", "provider/unknown/reconfigure-case",
        )
        result = self.cli(
            "configure-release", "--target", target, "--intended-artifact", "sha256:abc",
            "--rollback-readiness", "ready", "--rollback-plan", "redeploy known-good image",
            "--rollback-execution-authorized", "false",
            "--rollback-recovery-artifact", "sha256:known-good", expected=3,
        )
        self.assertIn("immutable once deployment work begins", result.stderr)
        data = self.load()
        self.assertEqual(attempt, data["release"]["active_attempt_id"])
        self.assertEqual("unknown", data["release"]["outcome"])
        self.cli("validate")

    def test_46_deliver_requires_plan_authority_and_reconciled_result(self) -> None:
        self.init()
        target = self.target()
        scenario = self.scenario(target)
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/audit-pass.png",
        )
        self.cli("advance", "REPORT")
        result = self.cli("advance", "DELIVER", expected=3)
        self.assertIn("authorized delivery plan", result.stderr)
        delivery = self.cli(
            "plan-delivery", "--action", "report-send", "--target", "qa-owner@example.test",
            "--authorization-source", "current task: send QA report",
            "--idempotency-key", "report-run-001", "--details", "send final QA report",
        ).stdout.strip()
        result = self.cli("validate", "--strict", expected=3)
        self.assertIn("INVALID", result.stdout)
        self.cli("advance", "DELIVER")
        result = self.cli("validate", "--strict", expected=3)
        self.assertIn("INVALID", result.stdout)
        result = self.cli(
            "record-delivery", "--delivery", delivery, "--result", "succeeded",
            "--details", "mail provider accepted message", "--evidence", "provider/mail/001",
            expected=3,
        )
        self.assertIn("external-id", result.stderr)
        self.cli(
            "record-delivery", "--delivery", delivery, "--result", "succeeded",
            "--external-id", "message-001", "--details", "mail provider accepted message",
            "--evidence", "provider/mail/001",
        )
        self.cli("validate", "--strict")
        summary = self.cli("summary", "--format", "markdown").stdout
        self.assertIn("report-send [succeeded]", summary)
        self.assertIn("message-001", summary)
        self.assertIn("current task: send QA report", summary)
        self.assertIn("send final QA report", summary)
        self.assertIn("provider/mail/001", summary)

    def test_47_only_one_reconciled_deployment_retry_is_allowed(self) -> None:
        target, scenario, pre, _, first = self.release_until_deploy()
        self.cli(
            "record-deployment", "--attempt", first, "--result", "failed-unchanged",
            "--observed-artifact", "sha256:known-good",
            "--details", "provider confirms no rollout", "--evidence", "provider/reconcile/first",
        )
        self.cli("advance", "LOCAL_VERIFY")
        second = self.declare_attempt_at_local_verify()
        self.gate_browser_pass(target, scenario, second)
        self.cli(
            "add-check", "--plan", pre, "--result", "pass", "--target", target,
            "--artifact", "sha256:abc", "--attempt", second, "--evidence", "reports/build-second.txt",
        )
        self.cli("advance", "RELEASE_GATE")
        self.cli("release-gate", "--attempt", second)
        self.cli("advance", "DEPLOY")
        self.cli(
            "record-deployment", "--attempt", second, "--result", "failed-unchanged",
            "--observed-artifact", "sha256:known-good",
            "--details", "provider again confirms no rollout", "--evidence", "provider/reconcile/second",
        )
        result = self.cli("advance", "LOCAL_VERIFY", expected=3)
        self.assertIn("retry limit reached", result.stderr)
        self.assertEqual(2, len(self.load()["deployment_attempts"]))

    def test_48_release_configuration_is_idempotent_before_attempt_only(self) -> None:
        self.init(mode="release", repair=False)
        target = self.target("staging", "staging", "https://staging.example.test", "current task")
        self.configure_release(target)
        before = self.load()["release"]
        self.configure_release(target)
        self.assertEqual(before, self.load()["release"])
        result = self.cli(
            "configure-release", "--target", target, "--intended-artifact", "sha256:different",
            "--rollback-readiness", "ready", "--rollback-plan", "redeploy known-good image",
            "--rollback-execution-authorized", "false",
            "--rollback-recovery-artifact", "sha256:known-good", expected=3,
        )
        self.assertIn("immutable", result.stderr)

    def test_49_rollback_is_terminal_for_an_attempt(self) -> None:
        _, _, _, _, attempt = self.release_until_deploy(rollback_authorized=True)
        self.cli(
            "record-deployment", "--attempt", attempt, "--result", "pass",
            "--observed-artifact", "sha256:abc", "--evidence", "provider/deploy/terminal",
        )
        self.cli(
            "record-rollback", "--attempt", attempt, "--result", "rolled-back",
            "--observed-artifact", "sha256:known-good", "--health-result", "pass",
            "--details", "known-good restored", "--evidence", "provider/rollback/terminal",
        )
        result = self.cli(
            "record-deployment", "--attempt", attempt, "--result", "pass",
            "--observed-artifact", "sha256:abc", "--evidence", "provider/deploy/illegal-replay",
            expected=3,
        )
        self.assertIn("illegal deployment outcome transition", result.stderr)
        result = self.cli("advance", "REMOTE_VERIFY", expected=3)
        self.assertIn("intended artifact successfully observed", result.stderr)
        self.assertEqual("rolled-back", self.load()["release"]["outcome"])

    def test_50_record_deployment_cannot_bypass_rollback_command(self) -> None:
        _, _, _, _, attempt = self.release_until_deploy(rollback_authorized=True)
        result = self.cli(
            "record-deployment", "--attempt", attempt, "--result", "rolled-back",
            "--details", "attempted bypass", "--evidence", "provider/rollback/bypass",
            expected=2,
        )
        self.assertIn("invalid choice", result.stderr)

    def test_51_failed_unchanged_attempt_cannot_be_reused_as_success(self) -> None:
        _, _, _, _, attempt = self.release_until_deploy()
        self.cli(
            "record-deployment", "--attempt", attempt, "--result", "failed-unchanged",
            "--observed-artifact", "sha256:known-good",
            "--details", "provider confirms no rollout", "--evidence", "provider/no-rollout",
        )
        result = self.cli(
            "record-deployment", "--attempt", attempt, "--result", "pass",
            "--observed-artifact", "sha256:abc", "--evidence", "provider/illegal-success",
            expected=3,
        )
        self.assertIn("illegal deployment outcome transition", result.stderr)

    def test_52_rollback_authority_requires_a_source(self) -> None:
        self.init(mode="release", repair=False)
        target = self.target("staging", "staging", "https://staging.example.test", "current task")
        result = self.cli(
            "configure-release", "--target", target, "--intended-artifact", "sha256:abc",
            "--rollback-readiness", "ready", "--rollback-plan", "redeploy known-good image",
            "--rollback-execution-authorized", "true",
            "--rollback-recovery-artifact", "sha256:known-good", expected=3,
        )
        self.assertIn("rollback-authorization-source", result.stderr)

    def test_53_conditional_rollback_requires_matching_trigger_evidence(self) -> None:
        _, _, _, _, attempt = self.release_until_deploy(
            rollback_authorized=True, rollback_trigger="health-degraded",
        )
        self.cli(
            "record-deployment", "--attempt", attempt, "--result", "pass",
            "--observed-artifact", "sha256:abc", "--evidence", "provider/deploy/conditional",
        )
        result = self.cli(
            "record-rollback", "--attempt", attempt, "--result", "rolled-back",
            "--observed-artifact", "sha256:known-good", "--health-result", "pass",
            "--details", "attempt without trigger", "--evidence", "provider/rollback/no-trigger",
            expected=3,
        )
        self.assertIn("exact configured --trigger", result.stderr)
        result = self.cli(
            "record-rollback", "--attempt", attempt, "--result", "rolled-back",
            "--observed-artifact", "sha256:known-good", "--health-result", "pass",
            "--trigger", "wrong-trigger", "--trigger-evidence", "provider/health/wrong",
            "--details", "attempt with wrong trigger", "--evidence", "provider/rollback/wrong-trigger",
            expected=3,
        )
        self.assertIn("exact configured --trigger", result.stderr)
        self.cli(
            "record-rollback", "--attempt", attempt, "--result", "rolled-back",
            "--observed-artifact", "sha256:known-good", "--health-result", "pass",
            "--trigger", "health-degraded", "--trigger-evidence", "provider/health/failed",
            "--details", "configured health trigger observed", "--evidence", "provider/rollback/conditional",
        )
        self.assertEqual("rolled-back", self.load()["release"]["outcome"])

    def test_54_ready_rollback_requires_immutable_recovery_artifact(self) -> None:
        self.init(mode="release", repair=False)
        target = self.target("staging", "staging", "https://staging.example.test", "current task")
        result = self.cli(
            "configure-release", "--target", target, "--intended-artifact", "sha256:abc",
            "--rollback-readiness", "ready", "--rollback-plan", "redeploy known-good image",
            "--rollback-execution-authorized", "false", expected=3,
        )
        self.assertIn("rollback-recovery-artifact", result.stderr)

    def test_55_issue_summary_preserves_scope_and_severity_reasons(self) -> None:
        self.init()
        issue = self.cli(
            "add", "--title", "管理员页不适用", "--area", "权限", "--kind", "functional",
            "--severity", "P1", "--scope-status", "out", "--step", "打开管理员页",
            "--expected", "管理员可见", "--actual", "当前角色无权限",
            "--before-evidence", "evidence/admin.png", "--note", "not in requested admin role",
            "--classification-evidence", "evidence/role-matrix",
        ).stdout.strip()
        self.advance_prefix()
        self.cli(
            "update", issue, "--severity", "P2", "--note", "impact has workaround",
            "--classification-evidence", "evidence/impact",
        )
        summary = self.cli("summary", "--format", "markdown").stdout
        self.assertIn("out: not in requested admin role; evidence: evidence/role-matrix", summary)
        self.assertIn("severity P1->P2", summary)
        self.assertIn("reason=impact has workaround; evidence=evidence/impact", summary)

    def test_56_all_browser_scenarios_cannot_be_excluded_for_success(self) -> None:
        self.init()
        target = self.target()
        scenario = self.scenario(target, risk="A", name="唯一浏览器路径")
        self.advance_prefix()
        self.cli(
            "set-disposition", scenario, "--status", "out",
            "--reason", "role does not expose this route", "--evidence", "evidence/role-scope",
        )
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn("at least one applicable browser scenario", result.stderr)

    def test_57_required_audit_skip_cannot_hide_behind_optional_pass(self) -> None:
        self.init()
        target = self.target()
        critical = self.scenario(target, risk="A", name="关键路径")
        lower = self.cli(
            "declare-scenario", "--flow", "探索", "--name", "低风险路径",
            "--risk-class", "C", "--target", target, "--regression-level", "R2", "--optional",
        ).stdout.strip()
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", critical, "--phase", "baseline",
            "--result", "skipped", "--target", target, "--details", "not executed",
        )
        self.cli(
            "add-coverage", "--scenario", lower, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/lower-pass.png",
        )
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn(f"required/high-risk scenario {critical} is skipped", result.stderr)

    def test_58_repair_failure_requires_a_confirmed_issue(self) -> None:
        self.init(mode="repair", repair=True)
        target = self.target()
        critical = self.scenario(target, risk="A", name="核心通过路径")
        failing = self.cli(
            "declare-scenario", "--flow", "探索", "--name", "可选失败路径",
            "--risk-class", "C", "--target", target, "--regression-level", "R2", "--optional",
        ).stdout.strip()
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", critical, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/core-pass.png",
        )
        result = self.cli(
            "add-coverage", "--scenario", failing, "--phase", "baseline",
            "--result", "fail", "--target", target, "--details", "confirmed visible failure",
            "--evidence", "evidence/untracked-failure.png",
            expected=3,
        )
        self.assertIn("requires a confirmed issue", result.stderr)

    def test_59_repaired_issue_cannot_be_excluded_to_bypass_verification(self) -> None:
        self.init(mode="repair", repair=True)
        self.target()
        issue = self.issue(severity="P2")
        self.advance_prefix()
        self.cli("update", issue, "--status", "investigating")
        self.cli("advance", "REPAIR")
        self.cli("add-evidence", issue, "--kind", "repair", "--ref", "evidence/repaired-diff.txt")
        self.cli(
            "update", issue, "--status", "fixed", "--root-cause", "confirmed root cause",
            "--resolution", "source was changed", "--approach", "extend",
        )
        self.cli("advance", "LOCAL_VERIFY")
        self.cli("advance", "TRIAGE")
        result = self.cli(
            "update", issue, "--scope-status", "out", "--note", "attempted exclusion",
            "--classification-evidence", "evidence/late-scope-change", expected=3,
        )
        self.assertIn("cannot move out of scope after repair work", result.stderr)
        data = self.load()
        data["issues"][0]["scope_status"] = "out"
        (self.run_dir / "qa-ledger.json").write_text(json.dumps(data), encoding="utf-8")
        result = self.cli("validate", "--strict", expected=3)
        self.assertIn("INVALID", result.stdout)

    def test_60_historical_browser_failure_cannot_be_hidden_by_a_later_pass(self) -> None:
        self.init()
        target = self.target()
        issue = self.issue(severity="P2")
        scenario = self.scenario(target, issue=issue)
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "fail", "--target", target, "--issue", issue,
            "--details", "confirmed historical failure", "--evidence", "evidence/fail.png",
        )
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/pass.png",
        )
        self.cli("advance", "REPORT")
        self.cli("validate", "--strict")
        data = self.load()
        data["coverage"][0]["issues"] = []
        (self.run_dir / "qa-ledger.json").write_text(json.dumps(data), encoding="utf-8")
        result = self.cli("validate", "--strict", expected=3)
        self.assertIn("lacks a confirmed issue", result.stdout)

    def test_61_optional_health_failure_blocks_release_success(self) -> None:
        self.init(mode="release", repair=False, depth="release-regression")
        target = self.target("staging", "staging", "https://staging.example.test", "current task")
        scenario = self.scenario(target, risk="A", level="R4", name="发布冒烟")
        pre = self.plan(target, "pre-deploy", "build", level="R3")
        required_health = self.plan(target, "post-deploy", "health", level="R4", name="readiness")
        optional_health = self.cli(
            "declare-check", "--name", "secondary health signal", "--kind", "health",
            "--phase", "post-deploy", "--environment", "staging", "--target", target,
            "--optional", "--regression-level", "R4",
        ).stdout.strip()
        self.configure_release(target)
        self.advance_prefix()
        self.cli("advance", "LOCAL_VERIFY")
        attempt = self.declare_attempt_at_local_verify()
        self.gate_browser_pass(target, scenario, attempt)
        self.cli(
            "add-check", "--plan", pre, "--result", "pass", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt, "--evidence", "reports/build.txt",
        )
        self.cli("advance", "RELEASE_GATE")
        self.cli("release-gate", "--attempt", attempt)
        self.cli("advance", "DEPLOY")
        self.cli(
            "record-deployment", "--attempt", attempt, "--result", "pass",
            "--observed-artifact", "sha256:abc", "--evidence", "provider/deploy/health-test",
        )
        self.cli("advance", "REMOTE_VERIFY")
        self.cli(
            "add-check", "--plan", required_health, "--result", "pass", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt, "--evidence", "provider/health/ready",
        )
        self.cli(
            "add-check", "--plan", optional_health, "--result", "fail", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt, "--details", "degraded",
            "--evidence", "provider/health/degraded",
        )
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "post-deploy",
            "--result", "pass", "--target", target, "--artifact", "sha256:abc",
            "--attempt", attempt, "--evidence", "evidence/remote-smoke.png",
        )
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn(f"post-deploy health plan {optional_health}", result.stderr)

    def test_62_release_gate_requires_a_required_health_plan(self) -> None:
        self.init(mode="release", repair=False, depth="release-regression")
        target = self.target("staging", "staging", "https://staging.example.test", "current task")
        scenario = self.scenario(target, risk="A", level="R4", name="发布冒烟")
        pre = self.plan(target, "pre-deploy", "build", level="R3")
        self.cli(
            "declare-check", "--name", "optional readiness", "--kind", "health",
            "--phase", "post-deploy", "--environment", "staging", "--target", target,
            "--optional", "--regression-level", "R4",
        )
        self.configure_release(target)
        self.advance_prefix()
        self.cli("advance", "LOCAL_VERIFY")
        attempt = self.declare_attempt_at_local_verify()
        self.gate_browser_pass(target, scenario, attempt)
        self.cli(
            "add-check", "--plan", pre, "--result", "pass", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt, "--evidence", "reports/build.txt",
        )
        self.cli("advance", "RELEASE_GATE")
        result = self.cli("release-gate", "--attempt", attempt, expected=3)
        self.assertIn("requires a required post-deploy health plan", result.stderr)

    def test_63_issue_classification_must_match_replayed_evidenced_history(self) -> None:
        self.init(mode="repair", repair=True)
        target = self.target()
        issue = self.issue(severity="P1")
        scenario = self.scenario(target, issue=issue)
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/core-pass.png",
        )
        base = self.load()
        mutations = {
            "scope": ("scope_status", "out", "scope does not match replayed classification history"),
            "severity": ("severity", "P3", "severity does not match replayed classification history"),
        }
        for label, (field, value, expected_message) in mutations.items():
            with self.subTest(label=label):
                tampered = json.loads(json.dumps(base))
                tampered["issues"][0][field] = value
                (self.run_dir / "qa-ledger.json").write_text(json.dumps(tampered), encoding="utf-8")
                result = self.cli("validate", expected=3)
                self.assertIn(expected_message, result.stdout)
                result = self.cli("advance", "REPORT", expected=5)
                self.assertIn("existing ledger is invalid", result.stderr)
        (self.run_dir / "qa-ledger.json").write_text(json.dumps(base), encoding="utf-8")

    def test_64_verified_issue_recurrence_requires_a_new_repair_cycle(self) -> None:
        self.init(mode="repair", repair=True)
        target = self.target()
        issue = self.issue()
        r0 = self.scenario(target, level="R0", issue=issue, name="精确复现")
        r1 = self.scenario(target, level="R1", issue=issue, name="相邻状态")
        self.advance_prefix()
        self.cli("update", issue, "--status", "investigating")
        self.cli("advance", "REPAIR")
        self.cli("add-evidence", issue, "--kind", "repair", "--ref", "evidence/diff.txt")
        self.cli(
            "update", issue, "--status", "fixed", "--root-cause", "派生状态遗漏",
            "--resolution", "扩展选择器", "--approach", "extend",
        )
        self.cli("advance", "LOCAL_VERIFY")
        self.cli("add-evidence", issue, "--kind", "after", "--ref", "evidence/after.png")
        for scenario in (r0, r1):
            self.cli(
                "add-coverage", "--scenario", scenario, "--phase", "post-fix",
                "--result", "pass", "--target", target, "--issue", issue,
                "--evidence", f"evidence/{scenario}.png",
            )
        self.cli("update", issue, "--status", "verified")
        same_second = self.load()["issues"][0]["verified_at"]
        self.cli_at(
            same_second,
            "add-coverage", "--scenario", r0, "--phase", "post-fix",
            "--result", "fail", "--target", target, "--issue", issue,
            "--details", "verified behavior recurred", "--evidence", "evidence/recurred.png",
        )
        self.cli_at(
            same_second,
            "add-coverage", "--scenario", r0, "--phase", "post-fix",
            "--result", "pass", "--target", target, "--issue", issue,
            "--evidence", "evidence/later-pass.png",
        )
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn("failed after its current verification", result.stderr)
        summary = self.cli("summary", "--format", "markdown").stdout
        self.assertIn("REGRESSED", summary)

        self.cli("update", issue, "--status", "investigating")
        self.cli("advance", "REPAIR")
        self.cli("add-evidence", issue, "--kind", "repair", "--ref", "evidence/diff-cycle-2.txt")
        self.cli(
            "update", issue, "--status", "fixed", "--root-cause", "遗漏复发边界",
            "--resolution", "补充复发边界处理", "--approach", "extend",
        )
        self.cli("advance", "LOCAL_VERIFY")
        self.cli("add-evidence", issue, "--kind", "after", "--ref", "evidence/after-cycle-2.png")
        for scenario in (r0, r1):
            self.cli(
                "add-coverage", "--scenario", scenario, "--phase", "post-fix",
                "--result", "pass", "--target", target, "--issue", issue,
                "--evidence", f"evidence/{scenario}-cycle-2.png",
            )
        self.cli("update", issue, "--status", "verified")
        self.cli("advance", "REPORT")
        self.cli("validate", "--strict")

    def test_65_health_failure_cannot_be_hidden_by_a_later_pass(self) -> None:
        target, scenario, _, health, attempt = self.full_release_until_remote()
        self.cli(
            "add-check", "--plan", health, "--result", "fail", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt, "--details", "readiness degraded",
            "--evidence", "provider/health/fail",
        )
        self.cli(
            "add-check", "--plan", health, "--result", "pass", "--target", target,
            "--artifact", "sha256:abc", "--attempt", attempt, "--details", "later green",
            "--evidence", "provider/health/pass",
        )
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "post-deploy",
            "--result", "pass", "--target", target, "--artifact", "sha256:abc",
            "--attempt", attempt, "--evidence", "evidence/remote-smoke.png",
        )
        summary = self.cli("summary", "--format", "markdown").stdout
        self.assertIn("Post-deploy health history", summary)
        self.assertIn("result=fail", summary)
        self.assertIn("result=pass", summary)
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn("recorded degradation", result.stderr)

    def test_66_out_of_scope_and_active_repair_cannot_be_combined(self) -> None:
        self.init(mode="repair", repair=True)
        issue = self.issue()
        self.advance_prefix()
        result = self.cli(
            "update", issue, "--status", "investigating", "--scope-status", "out",
            "--note", "attempted combined transition",
            "--classification-evidence", "evidence/scope-analysis.md", expected=3,
        )
        self.assertIn("investigating status requires an in-scope issue", result.stderr)
        current = self.load()["issues"][0]
        self.assertEqual(("open", "in"), (current["status"], current["scope_status"]))

        data = self.load()
        data["issues"][0]["status"] = "investigating"
        data["issues"][0]["scope_status"] = "out"
        data["issues"][0]["classification_history"].append({
            "old_severity": "P1", "new_severity": "P1", "old_scope": "in",
            "new_scope": "out", "reason": "tampered", "evidence": "evidence/tampered",
            "at": (BASE + timedelta(seconds=self.tick + 10)).isoformat().replace("+00:00", "Z"),
        })
        (self.run_dir / "qa-ledger.json").write_text(json.dumps(data), encoding="utf-8")
        result = self.cli("validate", expected=3)
        self.assertIn("out-of-scope issue cannot be investigating", result.stdout)

    def test_67_scenario_disposition_requires_a_continuous_history(self) -> None:
        self.init(mode="repair", repair=True)
        target = self.target()
        passing = self.scenario(target, name="核心通过")
        blocked = self.scenario(target, name="被阻塞必测项")
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", passing, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/pass.png",
        )
        self.cli(
            "add-coverage", "--scenario", blocked, "--phase", "baseline",
            "--result", "blocked", "--target", target, "--details", "dependency unavailable",
        )
        data = self.load()
        item = next(value for value in data["scenarios"] if value["id"] == blocked)
        item.update({
            "disposition": "out", "disposition_reason": "tampered exclusion",
            "disposition_evidence": "evidence/tampered", "disposition_at": item["created_at"],
        })
        (self.run_dir / "qa-ledger.json").write_text(json.dumps(data), encoding="utf-8")
        result = self.cli("validate", expected=3)
        self.assertIn("disposition does not match replayed history", result.stdout)
        result = self.cli("advance", "REPORT", expected=5)
        self.assertIn("existing ledger is invalid", result.stderr)

    def test_68_delivery_terminal_history_cannot_be_reopened(self) -> None:
        self.init()
        target = self.target()
        scenario = self.scenario(target)
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/pass.png",
        )
        self.cli("advance", "REPORT")
        delivery = self.cli(
            "plan-delivery", "--action", "report-send", "--target", "owner@example.test",
            "--authorization-source", "current task: send report", "--idempotency-key", "report-1",
            "--details", "send one report",
        ).stdout.strip()
        self.cli("advance", "DELIVER")
        self.cli(
            "record-delivery", "--delivery", delivery, "--result", "succeeded",
            "--external-id", "message-1", "--details", "sent once",
            "--evidence", "provider/message-1",
        )
        data = self.load()
        item = data["deliveries"][0]
        later = (BASE + timedelta(seconds=self.tick + 10)).isoformat().replace("+00:00", "Z")
        item["history"].append({
            "result": "unknown", "external_id": "message-unknown", "details": "tampered reopen",
            "evidence": ["provider/unknown"], "at": later,
        })
        item.update({
            "status": "unknown", "external_id": "message-unknown",
            "outcome_details": "tampered reopen", "evidence": ["provider/unknown"],
            "updated_at": later,
        })
        (self.run_dir / "qa-ledger.json").write_text(json.dumps(data), encoding="utf-8")
        result = self.cli("validate", expected=3)
        self.assertIn("illegal delivery history transition succeeded -> unknown", result.stdout)
        result = self.cli(
            "record-delivery", "--delivery", delivery, "--result", "succeeded",
            "--external-id", "message-2", "--details", "attempted duplicate",
            "--evidence", "provider/message-2", expected=5,
        )
        self.assertIn("existing ledger is invalid", result.stderr)

    def test_69_check_disposition_requires_a_continuous_history(self) -> None:
        self.init(mode="repair", repair=True)
        target = self.target()
        scenario = self.scenario(target)
        plan = self.plan(target, "baseline", "test", level="R2")
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/pass.png",
        )
        self.cli(
            "add-check", "--plan", plan, "--result", "fail", "--target", target,
            "--details", "legacy failure", "--evidence", "reports/fail.txt",
        )
        data = self.load()
        item = next(value for value in data["check_plans"] if value["id"] == plan)
        item.update({
            "disposition": "baseline-debt", "disposition_reason": "tampered debt",
            "disposition_evidence": "evidence/tampered-debt", "disposition_at": item["created_at"],
        })
        (self.run_dir / "qa-ledger.json").write_text(json.dumps(data), encoding="utf-8")
        result = self.cli("validate", expected=3)
        self.assertIn("disposition does not match replayed history", result.stdout)

    def test_70_release_check_plan_requires_an_exact_target(self) -> None:
        self.init(mode="release", repair=False, depth="release-regression")
        result = self.cli(
            "declare-check", "--name", "unbound readiness", "--kind", "health",
            "--phase", "post-deploy", "--environment", "staging", "--required",
            "--regression-level", "R4", expected=3,
        )
        self.assertIn("release check plans require --target", result.stderr)

    def test_71_failed_unchanged_retry_requires_observed_artifact(self) -> None:
        _, _, _, _, attempt = self.release_until_deploy()
        result = self.cli(
            "record-deployment", "--attempt", attempt, "--result", "failed-unchanged",
            "--details", "provider reports no rollout", "--evidence", "provider/no-rollout",
            expected=3,
        )
        self.assertIn("requires --observed-artifact", result.stderr)
        self.cli(
            "record-deployment", "--attempt", attempt, "--result", "failed-unchanged",
            "--observed-artifact", "sha256:known-good",
            "--details", "provider confirms known-good remains active",
            "--evidence", "provider/known-good-active",
        )
        self.cli("advance", "LOCAL_VERIFY")

    def test_72_attempt_current_fields_must_match_replayed_history(self) -> None:
        target, scenario, _, health, attempt = self.full_release_until_remote()
        self.finish_release(target, scenario, health, attempt)
        data = self.load()
        data["deployment_attempts"][0]["outcome_history"][0]["observed_artifact"] = "sha256:evil"
        (self.run_dir / "qa-ledger.json").write_text(json.dumps(data), encoding="utf-8")
        result = self.cli("validate", "--strict", expected=3)
        self.assertIn("succeeded history has a mismatched artifact", result.stdout)
        self.assertIn("current fields do not match replayed outcome history", result.stdout)

    def test_73_required_audit_check_cannot_be_blocked_or_skipped(self) -> None:
        self.init()
        target = self.target()
        scenario = self.scenario(target)
        plan = self.plan(target, "baseline", "test", level="R2")
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/pass.png",
        )
        self.cli(
            "add-check", "--plan", plan, "--result", "blocked", "--target", target,
            "--details", "required dependency unavailable",
        )
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn(f"required audit check {plan} is blocked", result.stderr)

    def test_74_audit_check_failure_requires_a_confirmed_issue(self) -> None:
        self.init()
        target = self.target()
        scenario = self.scenario(target)
        plan = self.plan(target, "baseline", "test", level="R2")
        self.advance_prefix()
        self.cli(
            "add-coverage", "--scenario", scenario, "--phase", "baseline",
            "--result", "pass", "--target", target, "--evidence", "evidence/pass.png",
        )
        self.cli(
            "add-check", "--plan", plan, "--result", "fail", "--target", target,
            "--details", "assertion failed", "--evidence", "reports/fail.txt",
        )
        result = self.cli("advance", "REPORT", expected=3)
        self.assertIn("must reference a confirmed issue", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
