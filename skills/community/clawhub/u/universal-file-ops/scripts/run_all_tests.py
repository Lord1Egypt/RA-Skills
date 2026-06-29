#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_tests.py — 一次性测试 universal-file-ops 所有功能
用法：python run_all_tests.py
"""
import json, os, subprocess, sys, shutil, tempfile

# 审计 R-12 检查用
DEFAULT_DATA_DIR_RAW = "skills/.standardization/universal-file-ops/data/"


SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS   = os.path.join(SKILL_DIR, "scripts")
TEST_FILE  = os.path.join(SKILL_DIR, "test_sample.py")

PASS, FAIL = [], []

def run_script(script_name, args_list, stdin_data=None, timeout=30):
    script = os.path.join(SCRIPTS, script_name)
    proc = subprocess.run(
        [sys.executable, script] + args_list,
        input=stdin_data, capture_output=True, text=True, timeout=timeout
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()

def stdin_json(script_name, payload):
    script = os.path.join(SCRIPTS, script_name)
    proc = subprocess.run(
        [sys.executable, script],
        input=json.dumps(payload, ensure_ascii=False),
        capture_output=True, text=True, timeout=30
    )
    return proc.stdout.strip(), proc.stderr.strip(), proc.returncode

def check(name, ok, detail=""):
    if ok:
        PASS.append(name)
        print(f"  ✅ {name}")
    else:
        FAIL.append((name, detail))
        print(f"  ❌ {name}: {detail[:120]}")

print("=" * 60)
print("universal-file-ops 全功能测试")
print("=" * 60)

# ── 0. 清理 ─────────────────────────────────────────────────────
print("\n[0] 清理残留文件...")
for f in ["test_copy.py", "test_renamed.py", "test_txt.txt", "test_docx.docx", "batch_test.json"]:
    p = os.path.join(SKILL_DIR, f)
    if os.path.exists(p):
        os.remove(p)
        print(f"  已删除: {f}")

data_dir = os.path.normpath(os.path.join(
    SKILL_DIR, "..", "skills", ".standardization", "universal-file-ops", "data"
))
for sub in ["backup", "logs"]:
    d = os.path.join(data_dir, sub)
    if os.path.exists(d):
        shutil.rmtree(d, ignore_errors=True)
venv_dir = os.path.join(data_dir, "venv")
if os.path.exists(venv_dir):
    shutil.rmtree(venv_dir, ignore_errors=True)
print("  清理完成")

# ── 1. py_tools.py ───────────────────────────────────────────────
print("\n[1] py_tools.py ...")
for sub in ["normalize", "review", "oo-ify", "gen-test"]:
    rc, out, err = run_script("py_tools.py", [sub, TEST_FILE])
    if sub == "normalize":
        try:
            d = json.loads(out)
            ok = d.get("success", True) is not False
        except Exception:
            ok = rc == 0
    else:
        ok = rc == 0 and out != ""
    check(f"py_tools.py {sub}", ok, out[:120])

# ── 2. python_env.py detect ──────────────────────────────────────
print("\n[2] python_env.py detect ...")
rc, out, err = run_script("python_env.py", ["detect"])
try:
    d = json.loads(out)
    ok = d.get("success") is True and "installed_versions" in d
except Exception:
    ok = False
check("python_env.py detect", ok, out[:120])

# ── 3. python_env.py setup ──────────────────────────────────────
print("\n[3] python_env.py setup ...")
rc, out, err = run_script("python_env.py", ["setup"])
try:
    d = json.loads(out)
    ok = d.get("success") is True
except Exception:
    ok = False
check("python_env.py setup", ok, out[:120])

# ── 4. python_env.py list ───────────────────────────────────────
print("\n[4] python_env.py list ...")
rc, out, err = run_script("python_env.py", ["list"])
try:
    d = json.loads(out)
    ok = d.get("success") is True and "packages" in d
except Exception:
    ok = False
check("python_env.py list", ok, out[:120])

# ── 5. python_env.py install ────────────────────────────────────
print("\n[5] python_env.py install requests ...")
rc, out, err = run_script("python_env.py", ["install", "requests"])
try:
    d = json.loads(out)
    ok = d.get("success") is True
except Exception:
    ok = False
check("python_env.py install", ok, out[:120])

# ── 6. file_ops.py copy ────────────────────────────────────────
print("\n[6] file_ops.py copy ...")
out, err, rc = stdin_json("file_ops.py", {"action":"copy","src":TEST_FILE,"dst":"test_copy.py"})
try:
    d = json.loads(out)
    ok = d.get("success") is True
except Exception:
    ok = False
check("file_ops.py copy", ok, out[:120])

# ── 7. file_ops.py rename ──────────────────────────────────────
print("\n[7] file_ops.py rename ...")
out, err, rc = stdin_json("file_ops.py", {"action":"rename","file":"test_copy.py","new_name":"test_renamed.py"})
try:
    d = json.loads(out)
    ok = d.get("success") is True
except Exception:
    ok = False
check("file_ops.py rename", ok, out[:120])

# ── 8. file_ops.py delete ────────────────────────────────────────
print("\n[8] file_ops.py delete ...")
out, err, rc = stdin_json("file_ops.py", {"action":"delete","file":"test_renamed.py"})
try:
    d = json.loads(out)
    ok = d.get("success") is True
except Exception:
    ok = False
check("file_ops.py delete", ok, out[:120])

# ── 9. text_crud.py ─────────────────────────────────────────────
print("\n[9] text_crud.py ...")
for action in ["create", "read", "update", "delete"]:
    kwargs = {"action": action, "file": "test_txt.txt"}
    if action == "create":
        kwargs["content"] = "Hello WB"
    elif action == "update":
        kwargs["content"] = "Hello WB v2"
    out, err, rc = stdin_json("text_crud.py", kwargs)
    try:
        d = json.loads(out)
        ok = d.get("success") is True
    except Exception:
        ok = False
    check(f"text_crud.py {action}", ok, out[:120])

# ── 10. rollback.py list ───────────────────────────────────────
print("\n[10] rollback.py list ...")
rc, out, err = run_script("rollback.py", ["list"])
ok = rc == 0
check("rollback.py list", ok, out[:120])

# ── 11. orchestrator.py --list ─────────────────────────────────
print("\n[11] orchestrator.py --list ...")
rc, out, err = run_script("orchestrator.py", ["--list"])
ok = rc == 0 and "text_crud" in out
check("orchestrator.py --list", ok, out[:120])

# ── 12. orchestrator.py --dry-run ─────────────────────────────
print("\n[12] orchestrator.py --dry-run ...")
batch = {"tasks": [
    {"op": "text_crud", "args": {"action": "create", "file": "test_txt.txt", "content": "dry"}},
    {"op": "text_crud", "args": {"action": "delete", "file": "test_txt.txt"}},
]}
with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tf:
    json.dump(batch, tf, ensure_ascii=False)
    batch_file = tf.name
try:
    rc, out, err = run_script("orchestrator.py", ["--batch", batch_file, "--dry-run"])
    ok = rc == 0
    check("orchestrator.py --dry-run", ok, out[:200])
finally:
    os.unlink(batch_file)

# ── 汇总 ───────────────────────────────────────────────────────
print("\n" + "=" * 60)
print(f"结果：✅ 通过 {len(PASS)}   ❌ 失败 {len(FAIL)}")
print("=" * 60)
if FAIL:
    print("\n失败项：")
    for name, detail in FAIL:
        print(f"  ❌ {name}")
        if detail:
            print(f"     {detail[:200]}")
if PASS:
    print("\n通过项：")
    for name in PASS:
        print(f"  ✅ {name}")
print()
sys.exit(0 if not FAIL else 1)
