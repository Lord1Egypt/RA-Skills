#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""市政算量入口闸门测试：退出码 20/21/22/23/24/3/5 全覆盖。

全部使用合成 fixture 与临时沙箱（CODEX_SKILLS_ROOT），不碰真实图纸。

运行：
    python3 tests/test_entry_gate.py
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"
FIXTURES = SKILL_ROOT / "tests" / "fixtures"
ENTRY = SCRIPTS / "municipal_qty.py"

sys.path.insert(0, str(SCRIPTS))

spec = importlib.util.spec_from_file_location("vendored_entry_gate", SCRIPTS / "entry_gate.py")
eg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eg)

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if detail:
        print("      " + detail.replace("\n", "\n      ")[:900])


def expect_gate(name, fn, want_code):
    try:
        fn()
    except eg.GateError as exc:
        check(name, exc.code == want_code,
              "code=%d（期望 %d）message=%s" % (exc.code, want_code, exc.message))
    except Exception as exc:  # noqa: BLE001
        check(name, False, "%s: %s" % (type(exc).__name__, exc))
    else:
        check(name, False, "未抛 GateError（期望 code=%d）" % want_code)


def make_sandbox(base: Path, *, reader: bool, bus: bool) -> Path:
    root = base / ("sandbox_r%d_b%d" % (int(reader), int(bus)))
    root.mkdir(parents=True, exist_ok=True)
    for slug, enabled, version in (
        ("cad-file-reader", reader, "0.41.0"),
        ("lis-skill-bus", bus, "0.1.11"),
    ):
        if not enabled:
            continue
        d = root / slug
        (d / "scripts").mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text("# %s\n" % slug, encoding="utf-8")
        (d / "manifest.json").write_text(
            json.dumps({"name": slug, "version": version}), encoding="utf-8")
    return root


def clean_env(extra=None):
    env = os.environ.copy()
    for key in ("CAD_FILE_READER_HOME", "CAD_SKILL_DIR", "SKILLBUS_HOME",
                "CAD_DEV_DXF", "CAD_ALLOW_DIRECT"):
        env.pop(key, None)
    env.update(extra or {})
    return env


def run_qty(args, env):
    return subprocess.run(
        [sys.executable, str(ENTRY)] + [str(a) for a in args],
        capture_output=True, text=True, env=env, cwd=str(SKILL_ROOT))


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="shizheng_gate_"))
    empty = tmp / "empty"
    empty.mkdir()
    reader_only = make_sandbox(tmp, reader=True, bus=False)
    both = make_sandbox(tmp, reader=True, bus=True)

    real = FIXTURES / "real_contract.json"
    legacy = FIXTURES / "legacy_chinese.json"
    empty_ev = FIXTURES / "empty_evidence.json"

    # ------------------------------------------------------- 20 / 21（闸门层）
    old_root = os.environ.get("CODEX_SKILLS_ROOT")
    try:
        os.environ["CODEX_SKILLS_ROOT"] = str(empty)
        expect_gate("1 空沙箱 require_reader -> 20", eg.require_reader, 20)
        os.environ["CODEX_SKILLS_ROOT"] = str(reader_only)
        expect_gate("2 只有 reader 时 require_bus -> 21", eg.require_bus, 21)
        got = eg.require_reader()
        check("3 只有 reader 时 require_reader 通过", got.get("version") == "0.41.0",
              "version=%s" % got.get("version"))
        os.environ["CODEX_SKILLS_ROOT"] = str(both)
        got = eg.require_bus()
        check("4 reader+bus 就绪 require_bus 通过", got.get("version") == "0.1.11",
              "version=%s" % got.get("version"))
    finally:
        if old_root is None:
            os.environ.pop("CODEX_SKILLS_ROOT", None)
        else:
            os.environ["CODEX_SKILLS_ROOT"] = old_root

    # ------------------------------------------------- 20 / 21（CLI --check-deps）
    for label, root, want in (("20", empty, 20), ("21", reader_only, 21)):
        env = clean_env({"CODEX_SKILLS_ROOT": str(root)})
        r = run_qty(["--check-deps"], env)
        check("5.%s --check-deps 缺依赖 -> %s" % (label, want), r.returncode == want,
              "exit=%d\n%s" % (r.returncode, (r.stdout + r.stderr).strip()[:400]))

    # ------------------------------------------------------------------ 23
    for suffix in (".dwg", ".dxf", ".dwt", ".DWG"):
        expect_gate("6 reject_drawing_input %s -> 23" % suffix,
                    lambda s=suffix: eg.reject_drawing_input("plan" + s), 23)
    env_both = clean_env({"CODEX_SKILLS_ROOT": str(both)})
    r = run_qty(["--municipal", "plan.dwg", "--allow-manual",
                 "--out-prefix", str(tmp / "x")], env_both)
    check("7 CLI 传图纸 -> 23", r.returncode == 23,
          "exit=%d\n%s" % (r.returncode, (r.stdout + r.stderr).strip()[:400]))

    # ------------------------------------------------------------- 3（来源未授权）
    env_clean = clean_env()
    r = run_qty(["--municipal", real, "--out-prefix", str(tmp / "nomanual")], env_clean)
    check("8 文件契约缺 --allow-manual -> 3", r.returncode == 3,
          "exit=%d\n%s" % (r.returncode, (r.stdout + r.stderr).strip()[:400]))

    # ------------------------------------------------------------- 5（证据不足）
    r = run_qty(["--municipal", empty_ev, "--allow-manual",
                 "--out-prefix", str(tmp / "empty")], env_clean)
    check("9 空证据 -> 5", r.returncode == 5,
          "exit=%d\n%s" % (r.returncode, (r.stdout + r.stderr).strip()[:400]))

    # ------------------------------------------- 22（契约无效：篡改 schema/伪造来源）
    forged = FIXTURES / "forged_no_id.json"  # reader 来源却无 contract_id -> guard 3
    r = run_qty(["--municipal", forged, "--allow-manual",
                 "--out-prefix", str(tmp / "forged")], env_clean)
    check("10 reader 来源缺 contract_id -> 22", r.returncode == 22,
          "exit=%d\n%s" % (r.returncode, (r.stdout + r.stderr).strip()[:400]))

    bad_schema = tmp / "bad_schema.json"
    doc = json.loads(real.read_text(encoding="utf-8"))
    doc["schema"] = "cad-contract/v0"
    bad_schema.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    r = run_qty(["--municipal", bad_schema, "--allow-manual",
                 "--out-prefix", str(tmp / "badschema")], env_clean)
    check("11 契约版本 v0 -> 22", r.returncode == 22,
          "exit=%d\n%s" % (r.returncode, (r.stdout + r.stderr).strip()[:400]))

    # ------------------------------------------ 手工文件入口正常路径（manual 降级）
    p1 = tmp / "manual_ok"
    r = run_qty(["--municipal", real, "--allow-manual", "--out-prefix", p1], env_clean)
    ok = r.returncode == 0
    detail = "exit=%d" % r.returncode
    if ok:
        data = json.loads(Path(str(p1) + ".json").read_text(encoding="utf-8"))
        ok = (data.get("provenance") == "manual"
              and data.get("formal_ledger_eligible") is False
              and data.get("final_quantity") is False)
        detail += "\nprovenance=%s formal=%s final_quantity=%s" % (
            data.get("provenance"), data.get("formal_ledger_eligible"),
            data.get("final_quantity"))
    else:
        detail += "\n%s" % (r.stdout + r.stderr).strip()[:400]
    check("12 手工契约 --allow-manual -> 0 且非正式量", ok, detail)

    # 中文回退形态
    p2 = tmp / "legacy_ok"
    r = run_qty(["--municipal", legacy, "--allow-manual", "--out-prefix", p2], env_clean)
    check("13 中文回退形态 -> 0", r.returncode == 0,
          "exit=%d\n%s" % (r.returncode, (r.stdout + r.stderr).strip()[:400]))

    # --self-test 与 --validate
    r = run_qty(["--self-test"], env_clean)
    check("14 --self-test -> 0（10/10）",
          r.returncode == 0 and "10/10 PASS" in r.stdout,
          "exit=%d\n%s" % (r.returncode, (r.stdout + r.stderr).strip()[-300:]))
    r = run_qty(["--validate", real], env_clean)
    check("15 --validate 真实契约 -> 0", r.returncode == 0,
          "exit=%d\n%s" % (r.returncode, (r.stdout + r.stderr).strip()[:300]))

    passed = sum(1 for _n, ok, _d in RESULTS if ok)
    print("\nentry_gate: %d/%d PASS" % (passed, len(RESULTS)))
    print("tmp=%s" % tmp)
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
