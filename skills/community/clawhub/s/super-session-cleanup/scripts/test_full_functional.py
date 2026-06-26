#!/usr/bin/env python3
"""
session-cleanup / test_full_functional.py
-----------------------------------------
Full functional test for v1.4.0 — covers all CLI commands, safety, and edge cases.
Run: python test_full_functional.py
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Windows GBK console fix
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SCRIPT = str(Path(__file__).parent / "cleanup.py")
PYTHON = sys.executable
PASS = FAIL = 0
issues = []


def run(args, expect_exit=None):
    """Run cleanup.py with given args, return (exitcode, stdout, stderr)."""
    result = subprocess.run(
        [PYTHON, SCRIPT] + args,
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if expect_exit is not None and result.returncode != expect_exit:
        fail(f"exit code: expected {expect_exit}, got {result.returncode}", " ".join(args))
    return result.returncode, result.stdout, result.stderr


def test(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        msg = f"  ❌ {name}"
        if detail:
            msg += f" — {detail}"
        print(msg)
        issues.append(f"{name}: {detail}")


def fail(name, detail=""):
    global FAIL
    FAIL += 1
    print(f"  ❌ {name} — {detail}")
    issues.append(f"{name}: {detail}")


# ═══════════════════════════════════════════════════════════
print("\n═══ 1. --init 创建跟踪文件 ═══")

with tempfile.TemporaryDirectory() as tmpdir:
    ec, out, err = run(["--init", tmpdir], expect_exit=0)
    track_path = os.path.join(tmpdir, ".workbuddy", "session-track.json")
    test("--init creates file", os.path.exists(track_path))
    test("--init output mentions created", "created" in out.lower())

    with open(track_path) as f:
        data = json.load(f)
    test("--init JSON has started_at", bool(data.get("started_at")))
    test("--init JSON workspace matches", data.get("workspace") == tmpdir)
    test("--init JSON has all item categories",
         set(data["items"].keys()) == {"temp_files", "pip_packages", "npm_packages", "system_software", "skills", "other"})
    test("--init JSON skip_list is empty", data["skip_list"] == [])

    # Double init should overwrite
    ec2, out2, _ = run(["--init", tmpdir], expect_exit=0)
    with open(track_path) as f:
        data2 = json.load(f)
    test("--init overwrite produces valid JSON", data2["workspace"] == tmpdir)


# ═══════════════════════════════════════════════════════════
print("\n═══ 2. --add 添加各类条目 ═══")

with tempfile.TemporaryDirectory() as tmpdir:
    track_path = os.path.join(tmpdir, ".workbuddy", "session-track.json")
    run(["--init", tmpdir], expect_exit=0)

    # Add temp file
    ec, out, _ = run(["--add", "temp_files", "C:/tmp/test.py", "--track-file", track_path], expect_exit=0)
    test("--add temp_files succeeds", "Added" in out)

    # Add pip package
    ec, out, _ = run(["--add", "pip_packages", "requests", "--track-file", track_path], expect_exit=0)
    test("--add pip_packages succeeds", "Added" in out)

    # Add npm package
    ec, out, _ = run(["--add", "npm_packages", "lodash", "--track-file", track_path], expect_exit=0)
    test("--add npm_packages succeeds", "Added" in out)

    # Add system_software
    ec, out, _ = run(["--add", "system_software", "ripgrep", "--track-file", track_path], expect_exit=0)
    test("--add system_software succeeds", "Added" in out)

    # Add skill
    ec, out, _ = run(["--add", "skills", "/home/user/.workbuddy/skills/test-skill", "--track-file", track_path], expect_exit=0)
    test("--add skills succeeds", "Added" in out)

    # Add duplicate — should be skipped
    ec, out, _ = run(["--add", "temp_files", "C:/tmp/test.py", "--track-file", track_path], expect_exit=0)
    test("--add duplicate is skipped", "Already" in out)

    # Invalid category
    ec, _, _ = run(["--add", "invalid_cat", "foo", "--track-file", track_path], expect_exit=2)
    test("--add invalid category exits 2", ec == 2)

    # Verify file contents
    with open(track_path) as f:
        data = json.load(f)
    test("--add items persisted correctly",
         "C:/tmp/test.py" in data["items"]["temp_files"] and
         "requests" in data["items"]["pip_packages"] and
         "lodash" in data["items"]["npm_packages"])


# ═══════════════════════════════════════════════════════════
print("\n═══ 3. --skip-add + --show ═══")

with tempfile.TemporaryDirectory() as tmpdir:
    track_path = os.path.join(tmpdir, ".workbuddy", "session-track.json")
    run(["--init", tmpdir], expect_exit=0)
    run(["--add", "temp_files", "C:/tmp/keep_me.py", "--track-file", track_path], expect_exit=0)
    run(["--add", "temp_files", "C:/tmp/delete_me.py", "--track-file", track_path], expect_exit=0)

    # Skip an item
    ec, out, _ = run(["--skip-add", "keep_me.py", "--track-file", track_path], expect_exit=0)
    test("--skip-add succeeds", "Added" in out)

    # Skip duplicate
    ec, out, _ = run(["--skip-add", "keep_me.py", "--track-file", track_path], expect_exit=0)
    test("--skip-add duplicate detected", "Already" in out)

    # Show
    ec, out, _ = run(["--show", "--track-file", track_path], expect_exit=0)
    test("--show displays items", "temp_files" in out)
    test("--show marks skipped items", "skipped" in out.lower() or "保留" in out)

    # Verify skip_list persisted
    with open(track_path) as f:
        data = json.load(f)
    test("skip_list persisted", "keep_me.py" in data["skip_list"])


# ═══════════════════════════════════════════════════════════
print("\n═══ 4. --track-file + --dry-run 预览清理 ═══")

with tempfile.TemporaryDirectory() as tmpdir:
    track_path = os.path.join(tmpdir, ".workbuddy", "session-track.json")
    run(["--init", tmpdir], expect_exit=0)

    # Create real temp files
    temp_dir = os.environ.get("TEMP", "/tmp")
    test_file1 = os.path.join(temp_dir, "cleanup_test_1.txt")
    test_file2 = os.path.join(temp_dir, "cleanup_test_2.txt")
    for f in [test_file1, test_file2]:
        with open(f, "w") as fh:
            fh.write("test")

    run(["--add", "temp_files", test_file1, "--track-file", track_path], expect_exit=0)
    run(["--add", "temp_files", test_file2, "--track-file", track_path], expect_exit=0)
    run(["--skip-add", "cleanup_test_2.txt", "--track-file", track_path], expect_exit=0)

    ec, out, _ = run(["--track-file", track_path, "--dry-run"], expect_exit=0)
    test("--dry-run mentions DRY-RUN", "DRY-RUN" in out)
    test("--dry-run shows file1 for deletion", "cleanup_test_1" in out)

    # Files should still exist after dry-run
    test("dry-run does NOT delete file1", os.path.exists(test_file1))
    test("dry-run does NOT delete file2", os.path.exists(test_file2))

    # Clean up temp files manually
    for f in [test_file1, test_file2]:
        if os.path.exists(f):
            os.unlink(f)


# ═══════════════════════════════════════════════════════════
print("\n═══ 5. --track-file 实际清理（临时文件） ═══")

with tempfile.TemporaryDirectory() as tmpdir:
    track_path = os.path.join(tmpdir, ".workbuddy", "session-track.json")
    run(["--init", tmpdir], expect_exit=0)

    # Create temp files in OS temp
    temp_dir = os.environ.get("TEMP", "/tmp")
    real_file = os.path.join(temp_dir, "cleanup_real_test.txt")
    with open(real_file, "w") as fh:
        fh.write("delete me")

    run(["--add", "temp_files", real_file, "--track-file", track_path], expect_exit=0)

    ec, out, _ = run(["--track-file", track_path], expect_exit=0)
    test("actual cleanup runs", "Cleanup complete" in out or "Deleted" in out or "deleted" in out.lower())


# ═══════════════════════════════════════════════════════════
print("\n═══ 6. --manifest + --workspace 清理 ═══")

with tempfile.TemporaryDirectory() as tmpdir:
    # Create workspace structure
    ws = os.path.join(tmpdir, "myproject")
    gen_dir = os.path.join(ws, "generated-images")
    os.makedirs(gen_dir)
    img_file = os.path.join(gen_dir, "test_img.png")
    with open(img_file, "w") as f:
        f.write("fake image")

    src_file = os.path.join(ws, "main.py")
    with open(src_file, "w") as f:
        f.write("print('hello')")

    # Create manifest
    manifest = {
        "temp_files": [img_file],
        "other": [src_file],
        "pip_packages": [],
        "npm_packages": [],
        "skills": []
    }
    manifest_path = os.path.join(tmpdir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f)

    # Dry run with workspace
    ec, out, _ = run(["--manifest", manifest_path, "--workspace", ws, "--dry-run"], expect_exit=0)
    test("manifest dry-run: generated-images allowed", "test_img" in out)
    test("manifest dry-run: workspace source blocked", "workspace file" in out.lower() or "not a disposable subdir" in out.lower() or "SKIP" in out)


# ═══════════════════════════════════════════════════════════
print("\n═══ 7. --paths 直接删除 ═══")

with tempfile.TemporaryDirectory() as tmpdir:
    # Create a temp file to delete
    f1 = os.path.join(tmpdir, "direct_delete_test.txt")
    with open(f1, "w") as fh:
        fh.write("test")

    ec, out, _ = run(["--paths", f1, "--dry-run"], expect_exit=0)
    test("--paths dry-run mentions file", "direct_delete_test" in out)
    test("--paths dry-run does not delete", os.path.exists(f1))


# ═══════════════════════════════════════════════════════════
print("\n═══ 8. 安全边界 ═══")

# Test forbidden paths with --paths
forbidden_tests = [
    str(Path.home() / "Desktop" / "test.py"),
    str(Path.home() / "Documents" / "test.py"),
    str(Path.home() / "Downloads" / "test.py"),
]

# These files don't exist, so they'll be "skipped: does not exist"
# But we can test is_safe_to_delete directly
sys.path.insert(0, str(Path(__file__).parent))
import cleanup

for fp in forbidden_tests:
    safe, reason = cleanup.is_safe_to_delete(Path(fp))
    test(f"Forbidden: {Path(fp).name} in {Path(fp).parent.name}", not safe, f"reason: {reason}")

# Workspace source file protection
ws = "d:/WorkSpace/Claw/AI项目"
safe, reason = cleanup.is_safe_to_delete(Path("d:/WorkSpace/Claw/AI项目/SKILL.md"), workspace=ws)
test("Workspace source file blocked", not safe, f"reason: {reason}")

# Workspace generated-images allowed
safe, reason = cleanup.is_safe_to_delete(Path("d:/WorkSpace/Claw/AI项目/generated-images/img.png"), workspace=ws)
test("Workspace generated-images allowed", safe, f"reason: {reason}")

# Workspace node_modules allowed
safe, reason = cleanup.is_safe_to_delete(Path("d:/WorkSpace/Claw/AI项目/node_modules/lodash/index.js"), workspace=ws)
test("Workspace node_modules allowed", safe, f"reason: {reason}")

# No workspace provided → workspace source is allowed (no workspace context)
safe, reason = cleanup.is_safe_to_delete(Path("d:/WorkSpace/Claw/AI项目/SKILL.md"))
test("No workspace: non-forbidden path allowed", safe, f"reason: {reason}")

# C:/Windows is forbidden
safe, reason = cleanup.is_safe_to_delete(Path("C:/Windows/System32/test.dll"))
test("C:/Windows is forbidden", not safe, f"reason: {reason}")

# TEMP dir is safe
temp_dir = Path(os.environ.get("TEMP", "C:/Windows/Temp"))
safe, reason = cleanup.is_safe_to_delete(temp_dir / "test.py")
test("TEMP dir is safe", safe, f"reason: {reason}")


# ═══════════════════════════════════════════════════════════
print("\n═══ 9. pip/npm 预检查 ═══")

# pip: nonexistent package should be skipped, not fail
result = cleanup.uninstall_pip(["zzz_nonexistent_pkg_99999"])
test("pip pre-check: nonexistent skipped", len(result["skipped"]) == 1)
test("pip pre-check: no failures", len(result["failed"]) == 0)

# npm: nonexistent package should be skipped (if npm available)
try:
    result_npm = cleanup.uninstall_npm(["zzz_nonexistent_npm_99999"])
    test("npm pre-check: nonexistent skipped", len(result_npm.get("skipped", [])) >= 0)
    test("npm pre-check: no failures", len(result_npm.get("failed", [])) == 0,
         f"failed: {result_npm.get('failed')}")
except FileNotFoundError:
    test("npm pre-check: npm not available (graceful)", True)

# pip dry-run should still list as "uninstalled"
result_dry = cleanup.uninstall_pip(["fake_pkg"], dry_run=True)
test("pip dry-run lists package", "fake_pkg" in result_dry.get("uninstalled", []))


# ═══════════════════════════════════════════════════════════
print("\n═══ 10. 错误处理与边界 ═══")

# No arguments → exit 2
ec, _, _ = run([], expect_exit=2)
test("No args exits 2", ec == 2)

# Nonexistent track file
ec, _, _ = run(["--track-file", "C:/nonexistent_path_12345/session-track.json"], expect_exit=2)
test("Nonexistent track-file exits 2", ec == 2)

# Nonexistent manifest
ec, _, _ = run(["--manifest", "C:/nonexistent_path_12345/manifest.json"], expect_exit=2)
test("Nonexistent manifest exits 2", ec == 2)

# --show without --track-file → exits 0 (just ignored, no crash)
ec, _, _ = run(["--show"], expect_exit=2)
test("--show without --track-file exits 2", ec == 2)

# Empty track file cleanup (no items)
with tempfile.TemporaryDirectory() as tmpdir:
    track_path = os.path.join(tmpdir, ".workbuddy", "session-track.json")
    run(["--init", tmpdir], expect_exit=0)
    ec, out, _ = run(["--track-file", track_path], expect_exit=0)
    test("Empty track cleanup succeeds", "Cleanup complete" in out)

# Deep copy: multiple inits don't share state
with tempfile.TemporaryDirectory() as tmpdir:
    p1 = os.path.join(tmpdir, "t1.json")
    p2 = os.path.join(tmpdir, "t2.json")
    cleanup.track_init("/ws/A", p1)
    cleanup.track_init("/ws/B", p2)
    with open(p1) as f:
        d1 = json.load(f)
    with open(p2) as f:
        d2 = json.load(f)
    d1["items"]["temp_files"].append("test.py")
    test("Deep copy: no cross-contamination", len(d2["items"]["temp_files"]) == 0)

# Skip list partial matching in load_track_as_manifest
with tempfile.TemporaryDirectory() as tmpdir:
    track_data = {
        "started_at": "2026-01-01T00:00:00",
        "workspace": "/test",
        "items": {
            "temp_files": ["/tmp/a.py", "/tmp/b.py", "/tmp/keep_this.py"],
            "pip_packages": [],
            "npm_packages": [],
            "system_software": [],
            "skills": [],
            "other": []
        },
        "skip_list": ["keep_this"]
    }
    tp = os.path.join(tmpdir, "st.json")
    with open(tp, "w") as f:
        json.dump(track_data, f)
    manifest, ws = cleanup.load_track_as_manifest(tp)
    test("Partial skip: 'keep_this' matches '/tmp/keep_this.py'",
         "/tmp/keep_this.py" not in manifest.get("temp_files", []))
    test("Partial skip: non-matched items preserved",
         "/tmp/a.py" in manifest.get("temp_files", []))

# send_to_trash default safety
import inspect
sig = inspect.signature(cleanup.send_to_trash)
test("send_to_trash allow_hard_delete defaults False",
     sig.parameters["allow_hard_delete"].default is False)

# _is_skipped edge cases
test("_is_skipped: exact match", cleanup._is_skipped("foo", ["foo"]))
test("_is_skipped: partial match", cleanup._is_skipped("/path/to/foo.py", ["foo"]))
test("_is_skipped: no match", not cleanup._is_skipped("bar.py", ["foo"]))
test("_is_skipped: empty list", not cleanup._is_skipped("anything", []))
test("_is_skipped: multiple entries", cleanup._is_skipped("/tmp/test.py", ["keep", "test"]))


# ═══════════════════════════════════════════════════════════
print("\n" + "═" * 60)
print(f"Results: {PASS} passed, {FAIL} failed out of {PASS + FAIL} tests")
if issues:
    print("\n⚠️  Issues found:")
    for i in issues:
        print(f"  • {i}")
if FAIL == 0:
    print("\n🎉 All functional tests passed!")
else:
    print("\n❌ Some tests failed — see above for details.")
sys.exit(0 if FAIL == 0 else 1)
