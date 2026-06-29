import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = SKILL_ROOT / "scripts" / "register_scheduled_task.ps1"


class RegisterScheduledTaskTests(unittest.TestCase):
    def test_script_contains_scheduling_and_overwrite_guards(self):
        self.assertTrue(SCRIPT_PATH.exists(), f"Missing script: {SCRIPT_PATH}")
        source = SCRIPT_PATH.read_text(encoding="utf-8")
        for token in (
            "[CmdletBinding(SupportsShouldProcess = $true",
            "[Parameter(Mandatory = $true)]",
            "[string]$Vault",
            "[string]$ProjectName = 'arxiv-daily'",
            "[string]$TaskName",
            "[string]$At",
            "[switch]$Force",
            "Get-ScheduledTask",
            "New-ScheduledTaskAction",
            "New-ScheduledTaskTrigger",
            "Register-ScheduledTask",
            "-WindowStyle Hidden",
            "$PSCmdlet.ShouldProcess",
            "already exists",
            "NextRunTime",
        ):
            with self.subTest(token=token):
                self.assertIn(token, source)

    def test_whatif_validates_without_creating_task(self):
        self.assertTrue(SCRIPT_PATH.exists(), f"Missing script: {SCRIPT_PATH}")
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory) / "Vault"
            wrapper = (
                vault
                / "arxiv-daily"
                / "scripts"
                / "arxiv_daily.ps1"
            )
            wrapper.parent.mkdir(parents=True)
            wrapper.write_text("exit 0\n", encoding="utf-8")
            task_name = "CodexSkillValidation-DoNotCreate"

            result = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(SCRIPT_PATH),
                    "-Vault",
                    str(vault),
                    "-TaskName",
                    task_name,
                    "-At",
                    "10:30",
                    "-WhatIf",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            verification = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-Command",
                    (
                        f"if (Get-ScheduledTask -TaskName '{task_name}' "
                        "-ErrorAction SilentlyContinue) { exit 1 } else { exit 0 }"
                    ),
                ]
            )
            self.assertEqual(verification.returncode, 0)


if __name__ == "__main__":
    unittest.main()
