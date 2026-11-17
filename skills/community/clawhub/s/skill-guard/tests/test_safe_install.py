import fcntl
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("safe_install", ROOT / "scripts/safe_install.py")
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


MOCK_CLI = r'''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
tool = Path(sys.argv[0]).name
with open(os.environ['CALL_LOG'], 'a') as log:
    log.write(json.dumps([tool] + args) + '\n')
mode = os.environ.get('SCENARIO', 'clean')
if tool == 'clawhub':
    if mode == 'download_error':
        print('UNTRUSTED OUTPUT MARKER')
        sys.exit(1)
    root = Path(args[args.index('--workdir') + 1]) / 'skills' / args[args.index('install') + 1]
    root.mkdir(parents=True)
    (root / 'SKILL.md').write_text('---\nname: example-skill\ndescription: Test skill\n---\nRead-only test.\n')
    (root / 'script.sh').write_text('#!/bin/sh\nexit 0\n')
    if mode == 'file_symlink':
        (root / 'link').symlink_to(os.environ['SENTINEL'])
    if mode == 'directory_symlink':
        (root / 'link').symlink_to(Path(os.environ['SENTINEL']).parent)
    if mode == 'hardlink':
        os.link(os.environ['SENTINEL'], root / 'link')
    if mode == 'fifo':
        os.mkfifo(root / 'pipe')
    if mode == 'binary':
        (root / 'asset.bin').write_bytes(b'\xff\x00')
    if mode == 'nul':
        (root / 'asset.bin').write_bytes(b'text\x00text')
    if mode == 'missing_skill':
        (root / 'SKILL.md').unlink()
    if mode == 'unreadable_dir':
        hidden = root / 'unreadable'
        hidden.mkdir()
        (hidden / 'payload.sh').write_text('not scanned')
        hidden.chmod(0)
    if mode == 'oversize':
        with (root / 'large.txt').open('wb') as f:
            f.truncate(21 * 1024 * 1024)
    if mode == 'root_symlink':
        other = root.with_name('other')
        root.rename(other)
        root.symlink_to(other)
    if mode == 'parent_symlink':
        parent = root.parent
        other = parent.with_name('other-skills')
        parent.rename(other)
        parent.symlink_to(other)
    sys.exit(0)
root = Path(args[-1])
files = [{'name': p.relative_to(root).as_posix(), 'type': 'script'}
         for p in root.rglob('*') if p.is_file()]
result = {'path': str(root.parent), 'server_risks': [], 'skill_risks': [
    {'name': 'example-skill', 'files': files, 'risk_indexes': {}}]}
skill = result['skill_risks'][0]
if mode == 'scanner_error':
    print('UNTRUSTED OUTPUT MARKER', file=sys.stderr)
    sys.exit(1)
if mode == 'empty': sys.exit(0)
if mode == 'malformed':
    print('UNTRUSTED OUTPUT MARKER')
    sys.exit(0)
if mode == 'missing_results':
    print('{}')
    sys.exit(0)
if mode == 'findings':
    skill['risk_indexes'] = {'insecure_credential_handling': {'score': 200, 'evidence': 'UNTRUSTED OUTPUT MARKER'}}
if mode == 'path_error': result['error'] = {'is_failure': False}
if mode == 'skill_error': skill['error'] = {'is_failure': False}
if mode == 'no_skills': result['skill_risks'] = []
if mode == 'wrong_path': result['path'] = '/unrelated/path'
if mode == 'server_result': result['server_risks'] = [{'name': 'unexpected'}]
if mode == 'missing_file': skill['files'] = files[:-1]
if mode == 'extra_file': skill['files'].append({'name': 'unrelated', 'type': 'asset'})
if mode == 'duplicate_file': skill['files'].append(files[0])
if mode == 'missing_risks': del skill['risk_indexes']
if mode == 'null_risks': skill['risk_indexes'] = None
if mode == 'mutated': (root / 'script.sh').write_text('changed after scanning')
if mode == 'mode_changed': (root / 'script.sh').chmod(0o777)
if mode == 'added_file': (root / 'extra.txt').write_text('not scanned')
print(json.dumps({'scan_path_responses': [result]}))
'''


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skill-guard-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.workspace = self.base / "workspace with spaces"
        self.bin = self.base / "bin"
        self.bin.mkdir()
        for tool in ("clawhub", "uvx"):
            path = self.bin / tool
            path.write_text(MOCK_CLI)
            path.chmod(0o700)
        self.sentinel = self.base / "outside-sentinel"
        self.sentinel.write_text("preserve me")
        self.log = self.base / "calls.jsonl"
        self.env = dict(os.environ, PATH=str(self.bin) + os.pathsep + os.environ['PATH'],
                        CLAWHUB_WORKDIR=str(self.workspace), CALL_LOG=str(self.log),
                        SENTINEL=str(self.sentinel), SNYK_TOKEN="mock-authentication-only")

    def run_cli(self, *args, scenario="clean"):
        result = subprocess.run([str(ROOT / "scripts/safe-install.sh"), *args],
                                env=dict(self.env, SCENARIO=scenario),
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(self.sentinel.read_text(), "preserve me")
        self.assertNotIn("UNTRUSTED OUTPUT MARKER", result.stdout + result.stderr)
        return result

    def existing(self):
        target = self.workspace / "skills/example-skill"
        target.mkdir(parents=True)
        (target / "old.txt").write_text("old installation")
        return target

    def test_clean_install_and_exact_tool_arguments(self):
        result = self.run_cli("example-skill", "--version", "1.2.3")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.workspace / "skills/example-skill/SKILL.md").is_file())
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertEqual(len(calls), 2)
        self.assertIn("--no-input", calls[0])
        self.assertEqual(calls[0][-2:], ["--version", "1.2.3"])
        self.assertIn("snyk-agent-scan==0.6.3", calls[1])
        self.assertIn("--show-analysis-results", calls[1])
        self.assertNotIn("--dangerously-run-mcp-servers", calls[1])
        runs = list((self.workspace / ".skill-guard").glob("run-*"))
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0].stat().st_mode & 0o777, 0o700)

    def test_invalid_inputs_never_invoke_tools(self):
        cases = [("../../outside-sentinel",), ("/tmp/skill",), ("..",), ("",),
                 ("bad;name",), ("two words",), ("Uppercase",), ("a--b",),
                 ("a", "b"), ("a", "--skip-scan"), ("a", "--version"),
                 ("a", "--version", "1.0 --force"), ("a", "--version", "../../x"),
                 ("a", "--for"), ("@owner/a",)]
        for args in cases:
            with self.subTest(args=args):
                self.assertEqual(self.run_cli(*args).returncode, 1)
                self.assertFalse(self.log.exists())
                self.assertFalse(self.workspace.exists())

    def test_errors_and_incomplete_scans_preserve_existing_installation(self):
        target = self.existing()
        cases = ["download_error", "scanner_error", "empty", "malformed", "missing_results",
                 "path_error", "skill_error", "no_skills", "wrong_path", "server_result",
                 "missing_file", "extra_file", "duplicate_file", "missing_risks", "null_risks",
                 "mutated", "mode_changed", "added_file", "file_symlink", "directory_symlink",
                 "root_symlink", "parent_symlink", "hardlink", "fifo", "binary", "nul",
                 "missing_skill", "oversize", "unreadable_dir"]
        for scenario in cases:
            with self.subTest(scenario=scenario):
                result = self.run_cli("example-skill", "--force", scenario=scenario)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertEqual((target / "old.txt").read_text(), "old installation")
                self.assertFalse((target / "SKILL.md").exists())

    def test_findings_quarantine_candidate_and_preserve_existing(self):
        target = self.existing()
        result = self.run_cli("example-skill", "--force", scenario="findings")
        self.assertEqual(result.returncode, 2)
        self.assertEqual((target / "old.txt").read_text(), "old installation")
        self.assertEqual(len(list((self.workspace / ".skill-guard").glob("run-*/skills/example-skill/SKILL.md"))), 1)

    def test_force_preserves_previous_installation(self):
        target = self.existing()
        result = self.run_cli("example-skill", "--force")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((target / "SKILL.md").is_file())
        backups = list((self.workspace / ".skill-guard").glob("run-*/previous-skill/old.txt"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "old installation")

    def test_existing_without_force_stops_before_download(self):
        self.existing()
        self.assertEqual(self.run_cli("example-skill").returncode, 1)
        self.assertFalse(self.log.exists())

    def test_live_skills_symlink_is_rejected(self):
        self.workspace.mkdir()
        (self.workspace / "skills").symlink_to(self.base)
        self.assertEqual(self.run_cli("example-skill", "--force").returncode, 1)
        self.assertFalse(self.log.exists())

    def test_existing_target_symlink_is_rejected(self):
        (self.workspace / "skills").mkdir(parents=True)
        (self.workspace / "skills/example-skill").symlink_to(self.base)
        self.assertEqual(self.run_cli("example-skill", "--force").returncode, 1)
        self.assertFalse(self.log.exists())

    def test_staging_symlink_is_rejected(self):
        self.workspace.mkdir()
        (self.workspace / ".skill-guard").symlink_to(self.base)
        self.assertEqual(self.run_cli("example-skill").returncode, 1)
        self.assertFalse(self.log.exists())

    def test_world_writable_workspace_is_rejected(self):
        self.workspace.mkdir(mode=0o777)
        self.workspace.chmod(0o777)
        self.assertEqual(self.run_cli("example-skill").returncode, 1)
        self.assertFalse(self.log.exists())

    def test_lock_prevents_concurrent_installations(self):
        state = self.workspace / ".skill-guard"
        state.mkdir(parents=True, mode=0o700)
        with (state / "install.lock").open("w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.assertEqual(self.run_cli("example-skill").returncode, 1)
            self.assertFalse(self.log.exists())

    def test_missing_authentication_stops_before_download(self):
        self.env.pop("SNYK_TOKEN")
        self.assertEqual(self.run_cli("example-skill").returncode, 1)
        self.assertFalse(self.log.exists())

    def test_failed_replacement_restores_old_installation(self):
        target = self.existing()
        run = self.base / "run"
        staged = run / "candidate"
        staged.mkdir(parents=True)
        (staged / "SKILL.md").write_text("candidate")
        original_rename = Path.rename
        for failure in (OSError("simulated move failure"), KeyboardInterrupt()):
            def fail_candidate(path, destination):
                if path == staged:
                    raise failure
                return original_rename(path, destination)
            with mock.patch.object(Path, "rename", fail_candidate):
                with self.assertRaises(type(failure)):
                    guard.promote(staged, target, run, True)
            self.assertEqual((target / "old.txt").read_text(), "old installation")
            self.assertTrue((staged / "SKILL.md").is_file())
            self.assertFalse((run / "previous-skill").exists())

    def test_timeout_blocks_installation(self):
        with mock.patch.object(guard.subprocess, "run", side_effect=subprocess.TimeoutExpired("scanner", 300)):
            with self.assertRaises(guard.Blocked):
                guard.run_tool(["scanner"], self.base)

    def test_scan_path_accepts_only_skill_or_its_private_parent(self):
        staged = self.base / 'private-run/skills/example-skill'
        files = {'SKILL.md': ('unused', 0o600)}
        for path in (staged, staged.parent, staged.parent.parent, self.base / 'other/skills'):
            report = {'scan_path_responses': [{
                'path': str(path), 'server_risks': [], 'skill_risks': [{
                    'name': 'example-skill', 'files': [{'name': 'SKILL.md', 'type': 'instruction'}],
                    'risk_indexes': {},
                }],
            }]}
            with self.subTest(path=path):
                if path in (staged, staged.parent):
                    guard.require_clean_report(json.dumps(report), staged, files)
                else:
                    with self.assertRaises(guard.Blocked):
                        guard.require_clean_report(json.dumps(report), staged, files)

    def test_interrupt_immediately_after_backup_move_restores_old_installation(self):
        target = self.existing()
        run = self.base / "run"
        staged = run / "candidate"
        staged.mkdir(parents=True)
        (staged / "SKILL.md").write_text("candidate")
        original_rename = Path.rename

        def interrupt_after_move(path, destination):
            result = original_rename(path, destination)
            if path == target:
                raise KeyboardInterrupt
            return result

        with mock.patch.object(Path, "rename", interrupt_after_move):
            with self.assertRaises(KeyboardInterrupt):
                guard.promote(staged, target, run, True)
        self.assertEqual((target / "old.txt").read_text(), "old installation")
        self.assertTrue((staged / "SKILL.md").is_file())
        self.assertFalse((run / "previous-skill").exists())


if __name__ == "__main__":
    unittest.main()
