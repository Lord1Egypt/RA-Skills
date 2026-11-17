#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selftest.py — 用「已知坏输入」证明验证器本身有效。

纪律来源（AGENTS.md / dsh-plugin-release）：
  只对好输入报「通过」的脚本等于没有。必须先拿已知有问题的输入跑一遍，
  确认它真能报错；再拿干净输入跑，确认不误报。

用法：python3 scripts/selftest.py
退出码：0 = 全部通过；1 = 有用例失败
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE / "release_audit.py"

# 密钥形状的测试数据一律拼接生成：本文件若直接写成字面量，
# 仓库自己的 check-secrets.sh 会把夹具当成真密钥拦下来。
FAKE_SK = "sk-" + "proj-" + "a" * 24
FAKE_PEM = ("-----BEGIN " + "RSA PRIVATE KEY" + "-----\nMIIB\n"
            + "-----END " + "RSA PRIVATE KEY" + "-----\n")

# 每个用例: (名字, {相对路径: 内容}, 期望 {类别: 最高严重级别})
#   严重级别: BLOCK=2 WARN=1 INFO=0；断言「该类别最严重发现恰好等于此值」
#   （类别无发现 = 0；这同时防止漏报——本应报 WARN 的类别若静默无发现即失败）
CASES = [
    {
        "name": "干净项目（MIT + 全宽松依赖）不误报",
        "files": {
            "package.json": json.dumps({
                "name": "my-clean-pkg", "version": "1.0.0", "license": "MIT",
                "author": "y16689540962-cloud", "dependencies": {"lodash": "^4.17.21"},
            }),
            "LICENSE": "MIT License\n\nCopyright (c) 2026 y16689540962-cloud\n",
            "index.js": "console.log('hello');\n",
            "node_modules/lodash/package.json": json.dumps(
                {"name": "lodash", "version": "4.17.21", "license": "MIT"}),
        },
        "expect": {"A": 0, "B": 0, "D": 0, "E": 0},
        "expect_absent": ["BLOCK"],
    },
    {
        "name": "A: 依赖 GPL → BLOCK",
        "files": {
            "package.json": json.dumps({
                "name": "gpl-user", "version": "1.0.0", "license": "MIT",
                "dependencies": {"some-gpl-pkg": "^1.0.0"},
            }),
            "LICENSE": "MIT License\n",
        },
        "registry": {"some-gpl-pkg": "GPL-3.0-only"},
        "expect": {"A": 2},
    },
    {
        "name": "A: 依赖 CC-BY-NC 素材包 → BLOCK",
        "files": {
            "package.json": json.dumps({
                "name": "nc-user", "version": "1.0.0", "license": "MIT",
                "dependencies": {"nc-icons": "^1.0.0"},
            }),
            "LICENSE": "MIT License\n",
        },
        "registry": {"nc-icons": "CC-BY-NC-4.0"},
        "expect": {"A": 2},
    },
    {
        "name": "A: 依赖 MPL-2.0 弱传染 → WARN（不 BLOCK）",
        "files": {
            "package.json": json.dumps({
                "name": "mpl-user", "version": "1.0.0", "license": "MIT",
                "dependencies": {"mpl-thing": "^1.0.0"},
            }),
            "LICENSE": "MIT License\n",
        },
        "registry": {"mpl-thing": "MPL-2.0"},
        "expect": {"A": 1},
    },
    {
        "name": "A: 完全未声明许可证 → BLOCK",
        "files": {
            "package.json": json.dumps({"name": "no-lic", "version": "0.1.0"}),
            "index.js": "console.log(1);\n",
        },
        "expect": {"A": 2},
    },
    {
        "name": "A: 无 LICENSE 文件仅字段声明 → WARN",
        "files": {
            "package.json": json.dumps({"name": "field-only", "version": "1.0.0", "license": "MIT"}),
            "index.js": "",
        },
        "expect": {"A": 1},
    },
    {
        "name": "A: package.json 与 LICENSE 不一致 → WARN",
        "files": {
            "package.json": json.dumps({"name": "mismatch", "version": "1.0.0", "license": "MIT"}),
            "LICENSE": "Apache License\nVersion 2.0\n",
        },
        "expect": {"A": 1},
    },
    {
        "name": "B: 源码文件带 GPL SPDX 头 → BLOCK",
        "files": {
            "package.json": json.dumps({"name": "spdx-gpl", "version": "1.0.0", "license": "MIT"}),
            "LICENSE": "MIT License\n",
            "lib/stolen.js": "// SPDX-License-Identifier: GPL-2.0-only\nconsole.log(1);\n",
        },
        "expect": {"B": 2},
    },
    {
        "name": "B: 他人版权行 → WARN",
        "files": {
            "package.json": json.dumps({"name": "copied", "version": "1.0.0", "license": "MIT", "author": "y16689540962-cloud"}),
            "LICENSE": "MIT License\n",
            "util.js": "// Copyright (c) 2019 Someone Else\ncoolFunction();\n",
        },
        "expect": {"B": 1},
    },
    {
        "name": "B: 自己的版权行 + THIRD-PARTY-NOTICES 不误报",
        "files": {
            "package.json": json.dumps({"name": "own", "version": "1.0.0", "license": "MIT", "author": "y16689540962-cloud"}),
            "LICENSE": "MIT License\n\nCopyright (c) 2026 y16689540962-cloud\n",
            "main.js": "// Copyright (c) 2026 y16689540962-cloud\n",
            "THIRD-PARTY-NOTICES.md": "react\nCopyright (c) Meta Platforms, Inc.\n",
        },
        "expect": {"B": 0},
    },
    {
        "name": "C: 无许可说明的字体 → WARN",
        "files": {
            "package.json": json.dumps({"name": "fonty", "version": "1.0.0", "license": "MIT"}),
            "LICENSE": "MIT License\n",
            "assets/FancyFont.ttf": "\x00\x01\x00\x00fake",
        },
        "expect": {"C": 1},
    },
    {
        "name": "C: 署名文件声明 CC-BY-NC 素材 → WARN",
        "files": {
            "package.json": json.dumps({"name": "docnc", "version": "1.0.0", "license": "MIT"}),
            "LICENSE": "MIT License\n",
            "CREDITS.txt": "banner.png — CC-BY-NC-4.0 图库\n",
        },
        "expect": {"C": 1},
    },
    {
        "name": "C: 说明文档里解释 NC 规则 → 只 INFO，不算告警",
        "files": {
            "package.json": json.dumps({"name": "explain", "version": "1.0.0", "license": "MIT"}),
            "LICENSE": "MIT License\n",
            "README.md": "注意：CC-BY-NC-4.0 素材不可用于可再分发的项目。\n",
        },
        "expect": {"C": 0},
    },
    {
        "name": "B: 文档里引用 GPL 许可证示例 → 不误报为真许可证头",
        "files": {
            "package.json": json.dumps({"name": "docquote", "version": "1.0.0", "license": "MIT"}),
            "LICENSE": "MIT License\n",
            "README.md": "例如旧版会写 `// SPDX-License-Identifier: GPL-2.0-only`。\n",
        },
        "expect": {"B": 0},
    },
    {
        "name": "B: 字符串字面量里的 SPDX 头（测试夹具形态）→ 不误报",
        "files": {
            "package.json": json.dumps({"name": "fixtureish", "version": "1.0.0", "license": "MIT"}),
            "LICENSE": "MIT License\n",
            "check.mjs": 'const sample = "// SPDX-License-Identifier: GPL-2.0-only\\nconsole.log(1);";\n',
        },
        "expect": {"B": 0},
    },
    {
        "name": "D: 名称命中知名商标 → WARN",
        "files": {
            "package.json": json.dumps({"name": "super-chatgpt-tool", "version": "1.0.0", "license": "MIT"}),
            "LICENSE": "MIT License\n",
        },
        "expect": {"D": 1},
    },
    {
        "name": "D: 描述性命名（for X）只 WARN、绝不 BLOCK",
        "files": {
            "package.json": json.dumps({"name": "claude-helper", "version": "1.0.0", "license": "MIT"}),
            "LICENSE": "MIT License\n",
        },
        "expect": {"D": 1},
        "expect_absent": ["BLOCK"],
    },
    {
        "name": "E: 疑似密钥 → BLOCK",
        "files": {
            "package.json": json.dumps({"name": "leaky", "version": "1.0.0", "license": "MIT"}),
            "LICENSE": "MIT License\n",
            "config.js": "const KEY = '" + FAKE_SK + "';\n",
        },
        "expect": {"E": 2},
    },
    {
        "name": "A: 有 LICENSE 文件但 package.json 无 license 字段 → WARN（真实项目场景）",
        "files": {
            "package.json": json.dumps({"name": "field-missing", "version": "0.1.0"}),
            "LICENSE-APACHE-2.0.txt": "Apache License\nVersion 2.0, January 2004\n",
        },
        "expect": {"A": 1},
    },
    {
        "name": "A: 多个许可文件（MIT + Apache 文本并存）→ INFO 提示确认关系",
        "files": {
            "package.json": json.dumps({"name": "dual", "version": "1.0.0", "license": "MIT"}),
            "LICENSE": "MIT License\n",
            "LICENSE-APACHE-2.0.txt": "Apache License\nVersion 2.0, January 2004\n",
        },
        "expect": {"A": 0},
    },
    {
        "name": "E: .pem 私钥文件（内置回退路径）→ BLOCK",
        "files": {
            "package.json": json.dumps({"name": "pemmy", "version": "1.0.0", "license": "MIT"}),
            "LICENSE": "MIT License\n",
            "server.pem": FAKE_PEM,
        },
        "expect": {"E": 2},
    },
]


def run_case(case):
    tmp = Path(tempfile.mkdtemp(prefix="ria-selftest-"))
    try:
        for rel, content in case["files"].items():
            p = tmp / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
        if "registry" in case:
            # 本地 registry 模拟：不联网，通过 monkey-patch 不行 → 用 node_modules 注入
            for name, lic in case["registry"].items():
                d = tmp / "node_modules" / name
                d.mkdir(parents=True, exist_ok=True)
                (d / "package.json").write_text(
                    json.dumps({"name": name, "version": "1.0.0", "license": lic}),
                    encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(AUDIT), str(tmp), "--format", "json"],
            capture_output=True, text=True, timeout=120)
        if proc.returncode not in (0, 1, 2):
            return False, f"异常退出码 {proc.returncode}: {proc.stderr[-300:]}"
        data = json.loads(proc.stdout)
        sev = {"INFO": 0, "WARN": 1, "BLOCK": 2}
        got = {}
        for f in data["findings"]:
            got[f["category"]] = max(got.get(f["category"], 0), sev[f["severity"]])
        for cat, need in case["expect"].items():
            actual = got.get(cat, 0)
            if actual != need:
                return False, (f"类别 {cat} 期望最高严重级 {need}，实际 {actual}；"
                               f"findings={[(f['category'], f['severity'], f['title']) for f in data['findings']]}")
        for bad in case.get("expect_absent", []):
            if any(f["severity"] == bad for f in data["findings"]):
                return False, f"不应出现 {bad}，实际 findings={[(f['category'], f['severity'], f['title']) for f in data['findings']]}"
        return True, "ok"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_never_executes_target_scripts():
    """安全属性：审核被审项目时，绝不执行其中的脚本。

    构造一个恶意 check-secrets.sh（被执就会写 marker 文件），
    审核后断言 marker 不存在，且报告里给出「已跳过执行」的 INFO。
    """
    tmp = Path(tempfile.mkdtemp(prefix="ria-noexec-"))
    marker = tmp / "PWNED"
    try:
        (tmp / "package.json").write_text(json.dumps({"name": "evil", "license": "MIT"}))
        (tmp / "LICENSE").write_text("MIT License\n")
        (tmp / "check-secrets.sh").write_text(
            f"#!/bin/bash\ntouch '{marker}'\nexit 1\n")
        proc = subprocess.run(
            [sys.executable, str(AUDIT), str(tmp), "--format", "json"],
            capture_output=True, text=True, timeout=120)
        data = json.loads(proc.stdout)
        if marker.exists():
            return False, "审核过程执行了被审项目的 check-secrets.sh（任意代码执行）"
        infos = [f for f in data["findings"]
                 if f["category"] == "E" and f["severity"] == "INFO"
                 and "跳过执行" in f["title"]]
        if not infos:
            return False, "未提示「已跳过执行」"
        return True, "ok"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_symlink_escape_is_not_followed():
    """安全属性：不跟随符号链接读取项目外的文件。"""
    outer = Path(tempfile.mkdtemp(prefix="ria-outside-"))
    tmp = Path(tempfile.mkdtemp(prefix="ria-symlink-"))
    secret_file = outer / "id_rsa"
    try:
        secret_file.write_text("-----BEGIN " + "RSA PRIVATE KEY" + "-----\n")
        (tmp / "package.json").write_text(json.dumps({"name": "sl", "license": "MIT"}))
        (tmp / "LICENSE").write_text("MIT License\n")
        (tmp / "leak.pem").symlink_to(secret_file)
        proc = subprocess.run(
            [sys.executable, str(AUDIT), str(tmp), "--format", "json"],
            capture_output=True, text=True, timeout=120)
        data = json.loads(proc.stdout)
        if any(f["category"] == "E" and f["severity"] == "BLOCK" for f in data["findings"]):
            return False, "跟随了符号链接，读到了项目外的私钥"
        if "id_rsa" in proc.stdout:
            return False, "报告中出现了项目外文件名"
        return True, "ok"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.rmtree(outer, ignore_errors=True)


def test_secret_value_is_redacted():
    """安全属性：报告不回显密钥值（报告可能被转发或上传）。"""
    tmp = Path(tempfile.mkdtemp(prefix="ria-redact-"))
    try:
        (tmp / "package.json").write_text(json.dumps({"name": "r", "license": "MIT"}))
        (tmp / "LICENSE").write_text("MIT License\n")
        (tmp / "config.js").write_text(f"const K = '{FAKE_SK}';\n")
        proc = subprocess.run(
            [sys.executable, str(AUDIT), str(tmp), "--format", "json"],
            capture_output=True, text=True, timeout=120)
        if FAKE_SK in proc.stdout:
            return False, "报告中回显了完整密钥"
        if FAKE_SK[:16] in proc.stdout:
            return False, "报告中回显了密钥前缀"
        data = json.loads(proc.stdout)
        if not any(f["category"] == "E" and f["severity"] == "BLOCK" for f in data["findings"]):
            return False, "未检出密钥"
        return True, "ok"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    passed = failed = 0
    for name, fn in (
        ("安全：绝不执行被审项目脚本", test_never_executes_target_scripts),
        ("安全：不跟随符号链接读取项目外文件", test_symlink_escape_is_not_followed),
        ("安全：报告不回显密钥值", test_secret_value_is_redacted),
    ):
        ok, msg = fn()
        print(("✅" if ok else "❌") + " " + name + ("" if ok else f"\n   → {msg}"))
        passed, failed = passed + (1 if ok else 0), failed + (0 if ok else 1)
    for case in CASES:
        ok, msg = run_case(case)
        mark = "✅" if ok else "❌"
        print(f"{mark} {case['name']}" + ("" if ok else f"\n   → {msg}"))
        passed, failed = passed + (1 if ok else 0), failed + (0 if ok else 1)
    print(f"\n{passed} 通过 / {failed} 失败")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
