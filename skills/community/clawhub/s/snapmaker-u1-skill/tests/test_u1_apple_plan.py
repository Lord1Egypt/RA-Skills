"""Local availability and CLI contracts; never request model generation/downloads."""

import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts" / "u1_apple_plan.swift"


class ApplePlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if platform.system() != "Darwin" or shutil.which("xcrun") is None:
            raise unittest.SkipTest("The native Foundation Models helper requires macOS and Swift.")
        supplied = os.environ.get("U1_APPLE_PLAN_BINARY")
        existing = Path(supplied) if supplied else ROOT / ".runtime" / "apple" / "u1_apple_plan"
        if existing.is_file() and os.access(existing, os.X_OK) and existing.stat().st_mtime >= SOURCE.stat().st_mtime:
            cls.binary = existing.resolve()
            return
        cls.temporary = tempfile.TemporaryDirectory(prefix="u1-apple-plan-tests-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.binary = Path(cls.temporary.name) / "u1_apple_plan"
        command = ["xcrun", "swiftc", "-parse-as-library", "-module-cache-path",
                   str(Path(cls.temporary.name) / "module-cache"), str(SOURCE), "-o", str(cls.binary)]
        built = subprocess.run(command, capture_output=True, text=True, timeout=120)
        if built.returncode:
            unsupported = ("sandbox_apply", "no such module 'FoundationModels'", "SDK is not supported by the compiler",
                           "unable to find utility", "unable to load standard library")
            if any(message in built.stderr for message in unsupported):
                raise unittest.SkipTest("Foundation Models compilation is unavailable in this context; provide a prebuilt U1_APPLE_PLAN_BINARY. " + built.stderr[:300])
            raise AssertionError("Swift helper failed to compile:\n" + built.stderr)

    def invoke(self, *arguments):
        completed = subprocess.run([str(self.binary), *arguments], capture_output=True, text=True, timeout=30)
        self.assertTrue(completed.stdout.strip(), completed.stderr)
        try:
            report = json.loads(completed.stdout)
        except json.JSONDecodeError:
            self.fail("Helper did not return one JSON object: " + completed.stdout + completed.stderr)
        self.assertIsInstance(report, dict)
        self.assertEqual(report["engine"], "SystemLanguageModel")
        self.assertEqual(report["model"], "SystemLanguageModel.default")
        self.assertTrue(report["localOnly"])
        self.assertFalse(report["privateCloudComputeUsed"])
        self.assertTrue(report["recommendationsOnly"])
        self.assertFalse(report["sliceExecuted"])
        self.assertFalse(report["printing"])
        self.assertFalse(report["slicerSettingsVerified"])
        self.assertFalse(report["hardwareCompatibilityVerified"])
        return completed, report

    def test_actual_doctor_reports_availability_without_generation(self):
        completed, report = self.invoke("--doctor")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn(report["status"], ("available", "unavailable"))
        self.assertEqual(report["available"], report["status"] == "available")
        self.assertNotIn("recommendation", report)
        if not report["available"]:
            self.assertTrue(report["unavailableReason"])
            self.assertTrue(report["message"])

    def test_help_is_json_and_describes_recommendations_only(self):
        completed, report = self.invoke("--help")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(report["status"], "help")
        self.assertIn("--doctor", report["usage"])
        self.assertIn("--brief", report["usage"])
        self.assertNotIn("recommendation", report)

    def test_missing_unknown_and_conflicting_arguments_fail_before_generation(self):
        cases = [(), ("--unknown",), ("--brief",), ("--doctor", "--brief", "a decorative part"),
                 ("--doctor", "--doctor"), ("--brief", "one", "two")]
        for arguments in cases:
            with self.subTest(arguments=arguments):
                completed, report = self.invoke(*arguments)
                self.assertEqual(completed.returncode, 2)
                self.assertEqual(report["status"], "error")
                self.assertEqual(report["errorCode"], "invalid_input")
                self.assertNotIn("recommendation", report)
                self.assertNotIn("available", report)

    def test_blank_oversized_and_control_character_briefs_are_rejected(self):
        for brief in ("", " \n\t ", "x" * 2001, "🟦" * 2000, "part\x07name"):
            with self.subTest(length=len(brief), sample=brief[:20]):
                completed, report = self.invoke("--brief", brief)
                self.assertEqual(completed.returncode, 2)
                self.assertEqual(report["errorCode"], "invalid_input")
                self.assertNotIn("recommendation", report)
                self.assertNotIn("available", report)


if __name__ == "__main__":
    unittest.main()
