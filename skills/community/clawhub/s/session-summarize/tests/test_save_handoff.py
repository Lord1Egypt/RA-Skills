#!/usr/bin/env python3
"""Regression tests for task-bound handoff validation, persistence, and inspection."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "save_handoff.py"
INSPECT = ROOT / "scripts" / "inspect_handoff.py"
HEADER = "<!-- summarize-handoff schema=2 {metadata} -->\n"


def run(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(script), *args], text=True, capture_output=True, check=False)


def report(
    task_id: str = "task-a",
    *,
    project_root: str = "PLACEHOLDER",
    branch: str = "master",
    head: str = "0123456789abcdef",
) -> str:
    metadata = {
        "created_at": "2026-07-20T00:00:00Z",
        "task_id": task_id,
        "project_root": project_root,
        "branch": branch,
        "head": head,
        "goal_digest": "0123456789abcdef",
    }
    return HEADER.format(metadata=json.dumps(metadata, ensure_ascii=False, separators=(",", ":"))) + "# 交接\n\n安全内容。\n"


def test_task_bound_save_and_inspect() -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    for trigger in ("复盘", "handoff", "总结 保存", "总结 恢复", "summarize save"):
        assert trigger in manifest["triggers"], f"manifest 缺少触发词: {trigger}"
    with tempfile.TemporaryDirectory(prefix="summarize-handoff-") as temporary:
        root = Path(temporary)
        source = root / "report.md"
        target = root / ".transfers" / "latest.md"
        source.write_text(report(project_root=str(root)), encoding="utf-8")
        first = run(SCRIPT, "--input", str(source), "--output", str(target))
        assert first.returncode == 0, first.stderr
        pointer = target.read_text(encoding="utf-8")
        assert "summarize-pointer schema=1" in pointer
        saved_report = next((target.parent / "handoffs").glob("*-task-a.md"))
        assert saved_report.read_text(encoding="utf-8") == source.read_text(encoding="utf-8")
        assert "handoffs/20260720T000000Z-task-a.md" in pointer

        source.write_text(report("task-b", project_root=str(root), head="fedcba9876543210"), encoding="utf-8")
        second = run(SCRIPT, "--input", str(source), "--output", str(target))
        assert second.returncode == 0, second.stderr
        assert list((target.parent / "handoffs").glob("*-task-a.md"))
        assert list((target.parent / "handoffs").glob("*-task-b.md"))
        assert target.with_name("latest.md.bak").exists()

        duplicate = root / "duplicate.md"
        duplicate.write_text(report("task-a", project_root=str(root)) + "different\n", encoding="utf-8")
        duplicate_result = run(SCRIPT, "--input", str(duplicate), "--output", str(target))
        assert duplicate_result.returncode == 4, duplicate_result.stderr
        assert "相同 created_at 和 task_id" in duplicate_result.stderr

        inspect = run(INSPECT, str(root))
        assert inspect.returncode == 0, inspect.stderr
        assert json.loads(inspect.stdout)["status"] == "过期参考"

        target.write_text("<!-- summarize-pointer schema=1 {\"report\":\"../outside.md\"} -->\n", encoding="utf-8")
        escaped = run(INSPECT, str(root))
        assert json.loads(escaped.stdout)["status"] == "受阻"

        invalid = run(SCRIPT, "--input", str(source), "--output", str(root / "wrong.md"))
        assert invalid.returncode == 4, invalid.stderr
        target.with_name("latest.md.lock").write_text("pid=other\n", encoding="utf-8")
        locked = run(SCRIPT, "--input", str(source), "--output", str(target))
        assert locked.returncode == 4, locked.stderr
        target.with_name("latest.md.lock").unlink()

        secret = root / "secret.md"
        fake_github_token = "ghp_" + "abcdefghijklmnopqrstuvwxyz123456"
        secret.write_text(report() + f"token: {fake_github_token}\n", encoding="utf-8")
        rejected = run(SCRIPT, "--input", str(secret), "--check-only")
        assert rejected.returncode == 3, rejected.stderr
        assert "疑似密钥" in rejected.stderr

        raw = root / "raw.md"
        raw.write_text(report() + "response_item: raw payload\n", encoding="utf-8")
        raw_result = run(SCRIPT, "--input", str(raw), "--check-only")
        assert raw_result.returncode == 3, raw_result.stderr
        assert "原始对话" in raw_result.stderr

        pii = root / "pii.md"
        pii.write_text(report() + "contact: person@example.com\n", encoding="utf-8")
        pii_result = run(SCRIPT, "--input", str(pii), "--check-only")
        assert pii_result.returncode == 3, pii_result.stderr
        assert "疑似密钥" in pii_result.stderr

        legacy = root / ".transfers" / "latest.md"
        legacy.write_text("<!-- summarize-handoff schema=1 created_at=2026-07-11T00:00:00Z -->\n# 旧报告\n", encoding="utf-8")
        legacy_result = run(INSPECT, str(root))
        assert json.loads(legacy_result.stdout)["status"] == "旧格式，未验证"


def test_inspect_accepts_matching_git_context() -> None:
    with tempfile.TemporaryDirectory(prefix="summarize-git-") as temporary:
        root = Path(temporary).resolve()
        commands = (
            ("init", "-b", "main"),
            ("config", "user.email", "summarize-test@example.invalid"),
            ("config", "user.name", "Summarize Test"),
        )
        for command in commands:
            result = subprocess.run(["git", "-C", str(root), *command], text=True, capture_output=True, check=False)
            assert result.returncode == 0, result.stderr
        (root / "tracked.txt").write_text("tracked\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "tracked.txt"], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-m", "fixture"], capture_output=True, text=True, check=True)
        head = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
        source = root / "report.md"
        target = root / ".transfers" / "latest.md"
        source.write_text(report("matching", project_root=str(root), branch="main", head=head), encoding="utf-8")
        saved = run(SCRIPT, "--input", str(source), "--output", str(target))
        assert saved.returncode == 0, saved.stderr
        inspected = run(INSPECT, str(root))
        assert inspected.returncode == 0, inspected.stderr
        assert json.loads(inspected.stdout)["status"] == "已验证"


def main() -> None:
    test_task_bound_save_and_inspect()
    print("save_handoff tests passed")


if __name__ == "__main__":
    main()
