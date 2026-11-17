#!/usr/bin/env python3
"""document + smoke 级自检（simaguang-perspective）。

覆盖：
- SKILL.md / manifest.json 完整性，以及两者版本号是否同步（document）
- 版本单源：SKILL.md frontmatter version == manifest.version
- 关键脚本/引用文件存在性（smoke）
- 隐私扫描：包内不得出现作者本机绝对路径与明文密钥
- 发布卫生：无 __pycache__/.pyc/_archived_onetime；manifest 与磁盘文件不漂移
- SKILL.md 提到的 references/ 文件必须真实存在（文档承诺=实现）
- 3 类模板冒烟渲染（--type 跑到临时目录，断言非空）
- PYTHONIOENCODING=ascii 下 smoke_utf8_json.py 中文 JSON 输出（UTF-8 自举防线）
- 关键 CLI --help 返回码

退出码：0 全绿；1 有 FAIL。SKIP 不算失败（环境不具备，例如没有 pdftotext）。
"""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PYTHON = sys.executable
FAILURES: list[str] = []
SKIPS: list[str] = []
CHECK_FILES: list[str] = [
        "SKILL.md",
        "SKILL.lite.md",
        "manifest.json",
        "README.md",
        "README.en.md",
        "references/optional-本地扩展.md",
        "scripts/project_paths.py",
        "scripts/pyboot.py",
        "scripts/lint_cross_platform.py",
        "scripts/smoke_utf8_json.py",
        "scripts/run_test_prompts.py",
        "scripts/generate_work_product.py",
        "scripts/prepare_input.py",
        "scripts/build_handoff.py",
        "scripts/generate_work_product.cmd",
        "scripts/prepare_input.cmd",
        "test-prompts.json"
]
CLI_HELP: list[str] = [
        "run_test_prompts.py",
        "generate_work_product.py",
        "build_handoff.py",
        "test_routing_coverage.py",
        "project_paths.py",
]
SMOKE_TEMPLATES: list[str] = ["project-plan", "report", "novel-chapter"]

# 隐私扫描：这些写法出现在包里就说明没脱敏。
# 规则定义行（含 re.compile( / ABS_USER_PATH）本身会包含关键字，扫描时跳过。
PRIVACY_PATTERNS = [
    ("绝对用户路径", re.compile(r"(?<![\w.-])/(?:Users|home)/[A-Za-z0-9._-]+")),
    ("Windows 用户路径", re.compile(r"[A-Za-z]:\\Users\\[A-Za-z0-9._-]+")),
    ("明文密钥", re.compile(
        r"""(?i)\b(?:api[_-]?key|secret|access[_-]?token|password|passwd)\b\s*[:=]\s*['"][A-Za-z0-9_\-]{16,}['"]""")),
]
RULE_LINE_MARKERS = ("re.compile(", "PRIVACY_PATTERNS", "ABS_USER_PATH", "RULE_LINE_MARKERS")
SCAN_SUFFIXES = {".py", ".sh", ".cmd", ".md", ".json", ".yml", ".yaml", ".toml"}
SCAN_SKIP_DIRS = {"__pycache__", ".git", "handoff", "examples"}
# 这些文件是"规则/文档里必须举反例"的地方，扫描时跳过内容但仍检查其它文件。
SCAN_SKIP_FILES = {"scripts/lint_cross_platform.py", "scripts/self_test.py"}


def check(cond: bool, msg: str) -> None:
    if cond:
        print(f"PASS  {msg}")
    else:
        FAILURES.append(msg)
        print(f"FAIL  {msg}")


def skip(msg: str) -> None:
    SKIPS.append(msg)
    print(f"SKIP  {msg}")


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    import os as _os
    env = dict(_os.environ)
    env["PYTHONIOENCODING"] = "ascii"
    env["PYTHONUTF8"] = "1"
    r = subprocess.run(cmd, cwd=str(cwd), env=env, capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def frontmatter_version() -> str:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    block = text.split("---", 2)[1] if text.startswith("---") else ""
    m = re.search(r"^version:\s*(\S+)\s*$", block, re.M)
    return m.group(1).strip("\"'") if m else ""


def privacy_hits() -> list[str]:
    hits: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if SCAN_SKIP_DIRS & set(path.relative_to(ROOT).parts):
            continue
        if rel in SCAN_SKIP_FILES:
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines, 1):
            if any(marker in line for marker in RULE_LINE_MARKERS):
                continue
            for label, pattern in PRIVACY_PATTERNS:
                if pattern.search(line):
                    hits.append(f"{rel}:{number} [{label}] {line.strip()[:80]}")
    return hits


def hygiene_hits() -> list[str]:
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if "__pycache__" in path.parts:
            hits.append(f"缓存目录残留：{path.relative_to(ROOT).as_posix()}")
        elif path.suffix in (".pyc", ".pyo"):
            hits.append(f"字节码残留：{path.relative_to(ROOT).as_posix()}")
        elif "_archived_onetime" in path.parts:
            hits.append(f"一次性脚本归档残留：{path.relative_to(ROOT).as_posix()}")
    return hits


def dangling_refs() -> list[str]:
    """SKILL.md 提到的 references/*.md 必须真实存在。"""
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    named = {m.strip("`") for m in re.findall(r"references/[^\s`）)，、]+\.md", text)}
    return sorted(rel for rel in named if not (ROOT / rel).is_file())


def main() -> int:
    skill_md = ROOT / "SKILL.md"
    manifest = ROOT / "manifest.json"
    check(skill_md.is_file(), "SKILL.md 存在")
    check(manifest.is_file(), "manifest.json 存在")
    check("name:" in skill_md.read_text(encoding="utf-8")[:400], "SKILL.md frontmatter name")

    if manifest.is_file():
        m = json.loads(manifest.read_text(encoding="utf-8"))
        check(m.get("entry") == "SKILL.md", "manifest entry=SKILL.md")
        check(("scripts" in m) and ("references" in m), "manifest 含 scripts/references")
        fv = frontmatter_version()
        check(fv and fv == m.get("version"), f"版本单源一致 SKILL.md={fv} manifest={m.get('version')}")
        check(bool(str(m.get("description", "")).strip(" >")) and len(str(m.get("description", ""))) > 30,
              "manifest.description 非空且完整（不是 > 之类的残片）")
        missing = [rel for rel in list(m.get("scripts", [])) + list(m.get("references", []))
                   if not (ROOT / rel).is_file()]
        check(not missing, f"manifest 列出的文件全部存在（缺 {len(missing)} 个）")
        if missing:
            for rel in missing[:10]:
                print(f"      manifest 缺失：{rel}")

    for rel in CHECK_FILES:
        check((ROOT / rel).is_file(), f"文件存在 {rel}")

    hits = privacy_hits()
    check(not hits, f"隐私扫描 0 命中（命中 {len(hits)} 处）")
    for line in hits[:10]:
        print(f"      {line}")

    dirty = hygiene_hits()
    check(not dirty, f"发布卫生：无缓存/字节码/一次性归档（{len(dirty)} 处）")
    for line in dirty[:10]:
        print(f"      {line}")

    dangling = dangling_refs()
    check(not dangling, f"SKILL.md 引用的 references 文件均存在（缺 {len(dangling)} 个）")
    for rel in dangling[:10]:
        print(f"      断链：{rel}")

    rc, out = run([PYTHON, str(HERE / "smoke_utf8_json.py")], HERE)
    ok = rc == 0 and '"status": "ok"' in out
    check(ok, "smoke_utf8_json (PYTHONIOENCODING=ascii) JSON ok")
    if not ok:
        print(out)

    for cli in CLI_HELP:
        rc, out = run([PYTHON, str(HERE / cli), "--help"], HERE)
        check(rc == 0, f"CLI --help rc=0  {cli}")
        if rc != 0:
            print(out)

    with tempfile.TemporaryDirectory() as tmp:
        for key in SMOKE_TEMPLATES:
            out_path = Path(tmp) / f"{key}.md"
            rc, out = run([PYTHON, str(HERE / "generate_work_product.py"),
                           "--type", key, "--output", str(out_path)], HERE)
            body = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
            check(rc == 0 and len(body) > 100,
                  f"模板冒烟渲染 {key}（rc={rc} 字节={len(body)}）")
            if rc != 0:
                print(out)

    rc, out = run([PYTHON, str(HERE / "build_handoff.py"), "--out",
                   str(Path(tempfile.gettempdir()) / "simaguang-handoff-smoke.md")], HERE)
    check(rc == 0, "build_handoff --out 可写（无外部项目时降级）")
    if rc != 0:
        print(out)

    if FAILURES:
        print(f"SELF_TEST_FAILED count={len(FAILURES)} skips={len(SKIPS)}")
        return 1
    tail = f"，{len(SKIPS)} 项跳过：{'；'.join(SKIPS)}" if SKIPS else ""
    print(f"SELF_TEST_OK{tail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
