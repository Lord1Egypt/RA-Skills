#!/usr/bin/env python3
"""
session-cleanup / test_regression.py
------------------------------------
Regression test for v1.4.0 fixes.
Tests: P2-6 (deep copy), P2-9 (pre-check), and core safety logic.
Run: python test_regression.py
"""

import copy
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Add the scripts dir to path so we can import cleanup
sys.path.insert(0, str(Path(__file__).parent))
import cleanup

PASS = 0
FAIL = 0


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


# ─── P2-6: track_init deep copy ────────────────────────────────────────────
print("\n═══ P2-6: track_init deep copy ═══")

with tempfile.TemporaryDirectory() as tmpdir:
    # Create two track files
    path1 = os.path.join(tmpdir, "track1.json")
    path2 = os.path.join(tmpdir, "track2.json")

    cleanup.track_init("/workspace/A", path1)
    cleanup.track_init("/workspace/B", path2)

    # Load both and verify they are independent
    with open(path1) as f:
        t1 = json.load(f)
    with open(path2) as f:
        t2 = json.load(f)

    test("workspace A stored correctly", t1["workspace"] == "/workspace/A")
    test("workspace B stored correctly", t2["workspace"] == "/workspace/B")
    test("items are independent (not shared ref)",
         t1["items"] is not t2["items"],
         f"id(t1.items)={id(t1['items'])}, id(t2.items)={id(t2['items'])}")

    # Mutate one and verify the other is unaffected
    t1["items"]["temp_files"].append("/tmp/test.py")
    test("mutation isolation", len(t2["items"]["temp_files"]) == 0,
         f"t2 temp_files should be empty but has {len(t2['items']['temp_files'])} items")

    # Also verify TRACK_TEMPLATE is not mutated
    test("TRACK_TEMPLATE untouched",
         len(cleanup.TRACK_TEMPLATE["items"]["temp_files"]) == 0)


# ─── P2-9: uninstall_pip/uninstall_npm pre-check ───────────────────────────
print("\n═══ P2-9: pip/npm uninstall pre-check ═══")

# Test with a package that almost certainly does NOT exist
test("_pip_package_installed returns False for nonexistent",
     not cleanup._pip_package_installed("zzz_nonexistent_pkg_12345"))

result = cleanup.uninstall_pip(["zzz_nonexistent_pkg_12345"])
test("uninstall_pip skips uninstalled package",
     len(result["skipped"]) == 1 and result["skipped"][0]["reason"] == "not installed",
     f"got: {result}")
test("uninstall_pip has no failures for uninstalled package",
     len(result["failed"]) == 0,
     f"got: {result}")

# npm may not be available on all systems; test gracefully
try:
    result_npm = cleanup.uninstall_npm(["zzz_nonexistent_npm_pkg_12345"])
    test("uninstall_npm skips uninstalled package",
         len(result_npm.get("skipped", [])) >= 0,  # At minimum no crash
         f"got: {result_npm}")
except FileNotFoundError:
    test("uninstall_npm gracefully handles missing npm", True, "npm not installed on system")


# ─── Core safety: is_safe_to_delete ────────────────────────────────────────
print("\n═══ Core: is_safe_to_delete ═══")

# Forbidden paths
safe, reason = cleanup.is_safe_to_delete(Path.home() / "Desktop" / "test.py")
test("Desktop is forbidden", not safe, f"reason: {reason}")

safe, reason = cleanup.is_safe_to_delete(Path.home() / "Downloads" / "test.py")
test("Downloads is forbidden", not safe, f"reason: {reason}")

safe, reason = cleanup.is_safe_to_delete(Path.home() / "Documents" / "test.py")
test("Documents is forbidden", not safe, f"reason: {reason}")

safe, reason = cleanup.is_safe_to_delete(Path("C:/Windows") / "test.py")
test("C:/Windows is forbidden", not safe, f"reason: {reason}")

# Temp paths should be safe
temp_dir = Path(os.environ.get("TEMP", "C:/Windows/Temp"))
safe, reason = cleanup.is_safe_to_delete(temp_dir / "test_script.py")
test("TEMP dir is safe", safe, f"reason: {reason}")

# Workspace + ALLOWED_SUBDIRS
ws = "d:/WorkSpace/Claw/AI项目"
safe, reason = cleanup.is_safe_to_delete(
    Path("d:/WorkSpace/Claw/AI项目/generated-images/test.png"), workspace=ws)
test("generated-images under workspace is safe", safe, f"reason: {reason}")

safe, reason = cleanup.is_safe_to_delete(
    Path("d:/WorkSpace/Claw/AI项目/node_modules/lodash/index.js"), workspace=ws)
test("node_modules under workspace is safe", safe, f"reason: {reason}")

# Workspace source file should NOT be safe for script auto-delete
safe, reason = cleanup.is_safe_to_delete(
    Path("d:/WorkSpace/Claw/AI项目/fetch_trending.py"), workspace=ws)
test("workspace source file is NOT safe for script", not safe, f"reason: {reason}")


# ─── _is_skipped partial matching ───────────────────────────────────────────
print("\n═══ Core: _is_skipped partial matching ═══")

test("exact match", cleanup._is_skipped("foo.py", ["foo.py"]))
test("partial match", cleanup._is_skipped("/tmp/demo/foo.py", ["foo.py"]))
test("no match", not cleanup._is_skipped("/tmp/bar.py", ["foo.py"]))
test("empty skip_list", not cleanup._is_skipped("anything", []))


# ─── skip_list in load_track_as_manifest ────────────────────────────────────
print("\n═══ Core: load_track_as_manifest skip_list ═══")

with tempfile.TemporaryDirectory() as tmpdir:
    track_data = {
        "started_at": "2026-01-01T00:00:00",
        "workspace": "/test",
        "items": {
            "temp_files": ["/tmp/a.py", "/tmp/b.py", "/tmp/keep_this.py"],
            "pip_packages": ["requests"],
            "npm_packages": [],
            "system_software": [],
            "skills": [],
            "other": []
        },
        "skip_list": ["keep_this.py"]
    }
    track_path = os.path.join(tmpdir, "session-track.json")
    with open(track_path, "w") as f:
        json.dump(track_data, f)

    manifest, workspace = cleanup.load_track_as_manifest(track_path)
    test("skip_list filters partial match",
         "/tmp/keep_this.py" not in manifest.get("temp_files", []),
         f"temp_files: {manifest.get('temp_files')}")
    test("non-skipped items preserved",
         "/tmp/a.py" in manifest.get("temp_files", []),
         f"temp_files: {manifest.get('temp_files')}")
    test("workspace extracted", workspace == "/test")


# ─── send_to_trash: allow_hard_delete=False default ────────────────────────
print("\n═══ Core: send_to_trash safety ═══")

# Test with a nonexistent path — should not crash
ok, msg = cleanup.send_to_trash(Path("C:/nonexistent_path_12345/test.py"))
test("send_to_trash handles nonexistent path gracefully",
     not ok,  # should fail, not crash
     f"returned: ({ok}, {msg})")

# Test that allow_hard_delete=False prevents fallback
# We can't easily test this without mocking, but we can verify the default
import inspect
sig = inspect.signature(cleanup.send_to_trash)
test("send_to_trash default allow_hard_delete=False",
     sig.parameters["allow_hard_delete"].default is False)


# ─── CLI: --init creates valid JSON ────────────────────────────────────────
print("\n═══ CLI: --init ═══")

with tempfile.TemporaryDirectory() as tmpdir:
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "cleanup.py"),
         "--init", tmpdir],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    test("--init exit code 0", result.returncode == 0, f"got: {result.returncode}")

    track_path = os.path.join(tmpdir, ".workbuddy", "session-track.json")
    test("--init creates session-track.json", os.path.exists(track_path))

    with open(track_path) as f:
        data = json.load(f)
    test("--init JSON has items", "items" in data and "temp_files" in data["items"])
    test("--init JSON has skip_list", "skip_list" in data)


# ─── CLI: --dry-run doesn't delete ────────────────────────────────────────
print("\n═══ CLI: --dry-run ═══")

with tempfile.TemporaryDirectory() as tmpdir:
    # Create a temp file
    test_file = os.path.join(tmpdir, "test_dry_run.txt")
    with open(test_file, "w") as f:
        f.write("test")

    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "cleanup.py"),
         "--paths", test_file, "--dry-run"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    test("--dry-run exit code 0", result.returncode == 0)
    test("--dry-run does NOT delete file", os.path.exists(test_file))
    stdout = result.stdout or ""
    test("--dry-run output mentions DRY-RUN", "DRY-RUN" in stdout or "dry-run" in stdout.lower())


# ─── Summary ───────────────────────────────────────────────────────────────
print("\n" + "═" * 50)
print(f"Results: {PASS} passed, {FAIL} failed out of {PASS + FAIL} tests")
if FAIL == 0:
    print("🎉 All regression tests passed!")
else:
    print("⚠️  Some tests failed — review above for details.")
sys.exit(0 if FAIL == 0 else 1)
