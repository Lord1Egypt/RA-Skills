#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cad-file-reader 跨平台不可回归 lint。

扫描业务脚本（.py/.sh/.cmd/.ps1）里会破坏 Windows/Linux 的 darwin-only
路径、命令与系统调用：

  ERROR  — 未见到平台分支保护（platform.system / sys.platform / os.name /
            darwin / win32 / nt / Linux / Windows 等），大概率在其它 OS 直接崩溃；
  WARN   — 已带平台分支保护，或在注释/说明里被提及，仍需人工复核；
  每条命中都会给一条建议 fix 命令。

默认跳过 vendor/ 与 tests/；vendor 原生库用 --vendor-check 单列探测，
允许仓库里存在 darwin .so，但三平台 CI 不因缺少其它平台二进制而失败。
用法：
  python3 scripts/lint_cross_platform.py scripts/            # 只扫业务脚本
  python3 scripts/lint_cross_platform.py scripts/ --vendor-check
  python3 scripts/lint_cross_platform.py scripts/ --platform ubuntu  # CI 等价模拟
"""
from __future__ import annotations

import argparse
import platform
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_VENDOR = SKILL_DIR / "vendor"

# --------------------------------------------------------------------------- #
# 规则表：每条 = (名称, 正则, 建议 fix)。cmd/fix 是模板，{file} 会被替换。
# --------------------------------------------------------------------------- #
RULES = [
    ("OPT_HOMEBREW",
     re.compile(r"(?<![\w./])/opt/homebrew(?:/|(?=[\s,'\"`]))"),
     "用 platform_paths.find_tool() 发现工具，勿裸写 macOS 前缀。fix: python3 scripts/platform_paths.py"),
    ("APPLICATIONS_MAC",
     re.compile(r"(?<![\w./])/Applications/"),
     "把 /Applications/... 收进 darwin 分支；非 macOS 用 where/winget/apt 路径。fix: python3 scripts/platform_paths.py"),
    ("VENV_BIN",
     re.compile(r"\.venv/bin/"),
     "venv 可执行名跨平台不同：Windows 是 Scripts/python.exe。fix: python3 scripts/pyboot.py / platform_paths"),
    ("OSASCRIPT",
     re.compile(r"\bosascript\b"),
     "osascript 仅 macOS 可用。fix: 用平台分支，非 darwin 用 win/posix 对应命令"),
    ("BREW_CMD",
     re.compile(r"(^|[\s;&|])\bbrew\s"),
     "brew 仅 macOS（homebrew）存在。fix: darwin 分支用 brew，其它平台用 apt/dnf/pip/winget/choco"),
    ("XCODE_SELECT",
     re.compile(r"\bxcode-select\b"),
     "xcode-select 仅 macOS。fix: darwin 分支才调用"),
    ("SETRLIMIT",
     re.compile(r"\b(?:resource\.)?setrlimit\b|RLIMIT_(?:AS|DATA|CPU|RSS|STACK)"),
     "setrlimit/RLIMIT_* 不是全平台可用（Windows 无；macOS 部分受限）。fix: 用 mem_guard.py 看门狗"),
    ("GETRUSAGE",
     re.compile(r"\bresource\.getrusage\b|RUSAGE_SELF"),
     "resource.getrusage 仅 POSIX。fix: 包一层平台分支，Windows 用 psutil.Process().memory_info().rss"),
    ("SIGALRM",
     re.compile(r"\bsignal\.SIGALRM\b|SIGALRM"),
     "SIGALRM 仅 POSIX；Windows 需 Timer 协作式超时。fix: 用 scripts/safe_timeout.py 的 deadline()"),
    ("SIGKILL",
     re.compile(r"\bsignal\.SIGKILL\b|SIGKILL"),
     "SIGKILL 仅 POSIX。fix: 平台分支外避免直接 kill；Windows 用 terminate()"),
    ("NATIVE_DYLIB",
     re.compile(r"\b[\w.-]+\.dylib\b"),
     "dylib 是 macOS 原生库格式。fix: 仓库内 sudo 二进制请走 platform 分支；Windows/Linux 由 pip wheel 提供"),
    ("DARWIN_SO",
     re.compile(r"\.cpython-\d+[^-]*-darwin\.so\b"),
     "darwin 专有扩展名出现在业务脚本里通常是误引用。fix: vendor 由各平台 setup/pip 重建，不应在脚本里硬依赖"),
]
# 命中即视为“文件带平台分支”的提示词（大小写不敏感）。
GUARD_TOKENS = (
    "platform.system", "sys.platform", "os.name", "platform.platform",
    "darwin", "linux", "win32", "windows", "mingw", "nt ", "nt", "posix",
)


def _is_comment(suffix: str, line: str) -> bool:
    s = line.lstrip()
    if not s:
        return False
    if suffix == ".sh":
        return s.startswith("#")
    if suffix in (".cmd", ".ps1"):
        return s.startswith(("#", "rem ", "::", "<#"))
    if suffix == ".py":
        return s.startswith("#") or s.startswith('"""') or s.startswith("'''")
    return s.startswith("#")


def _has_guard(text: str) -> bool:
    low = text.lower()
    return any(tok in low for tok in GUARD_TOKENS)


def _scan_file(path: Path) -> list[dict]:
    findings: list[dict] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return findings
    suffix = path.suffix.lower()
    guard = _has_guard(text)
    # 仅对命令类规则，在 .py 里只追 subprocess.run([...]) 这样的真实调用。
    for number, raw in enumerate(text.splitlines(), 1):
        if _is_comment(suffix, raw):
            continue
        line = raw
        if suffix == ".py":
            # brew/osascript 只在作为可执行程序名（subprocess）出现时才告警，
            # 避免把“建议文案”里的 brew 误报。
            filtered = line
            if RULES[4][1].search(line) and "subprocess" not in line and "run(" not in line:
                filtered = RULES[4][1].sub("", filtered)
            if RULES[3][1].search(line) and "subprocess" not in line and "run(" not in line:
                filtered = RULES[3][1].sub("", filtered)
        else:
            filtered = line
        for name, pat, fix in RULES:
            if pat.search(filtered):
                level = "WARN" if guard else "ERROR"
                findings.append({
                    "file": str(path),
                    "line": number,
                    "rule": name,
                    "level": level,
                    "text": line.strip()[:120],
                    "fix": fix,
                })
    return findings


# 扫描器自身不是“业务脚本”，不参与被扫描（避免规则表字符串自报）。
_SELF_NAME = "lint_cross_platform.py"


def _walk_files(paths, skip_dirs) -> list[Path]:
    out: list[Path] = []
    suffixes = {".py", ".sh", ".cmd", ".ps1"}
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            skips = tuple(item.strip() for item in skip_dirs.split(",") if item.strip())
            for f in sorted(p.rglob("*")):
                if f.suffix.lower() not in suffixes:
                    continue
                if any(part in skips for part in f.parts):
                    continue
                if f.name == _SELF_NAME:
                    continue
                out.append(f)
        elif p.suffix.lower() in suffixes and p.exists() and p.name != _SELF_NAME:
            out.append(p)
    return out


def _vendor_probe(vendor: Path, platform_name: str) -> int:
    """vendor 原生库探测：允许 darwin 二进制存在；其它平台缺失不是失败。

    返回 0 = 校验通过（可能有 WARN 输出），1 = 出错（仅供 --strict 使用）。
    """
    if not vendor.is_dir():
        print(f"vendor 目录不存在：{vendor}\n  → 说明仓库未内置二进制，CI 里由 setup 补齐，不视为失败。")
        return 0
    darwin = list(vendor.rglob("*.dylib")) + [p for p in vendor.rglob("*.so") if "darwin" in p.name]
    native = list(vendor.rglob("*.so")) + list(vendor.rglob("*.pyd")) + list(vendor.rglob("*.dylib"))
    cur_tag = "win32" if platform_name.lower() in ("windows", "win32", "win") else (
        "darwin" if platform_name.lower() in ("darwin", "macos", "mac") else "linux")
    cur = [p for p in native if cur_tag in p.name or p.suffix == ".pyd" and cur_tag == "win32"]
    portable_abi = [p for p in vendor.rglob("*.abi3.so")]
    if darwin:
        print(f"vendor 含 darwin 原生二进制 {len(darwin)} 个（允许存在；Windows/Linux 由 setup/pip 补对应 wheel，不因缺少 darwin 二进制报错）。")
    if cur:
        print(f"[vendor] 当前平台 {cur_tag} 原生扩展 {len(cur)} 个；|WARN| 若个别核心包仍走纯 Python 回退属可接受降级。")
    else:
        print(f"[vendor] 当前平台 {cur_tag} 未发现原生扩展（可接受：纯 Python 回退或由 setup 补齐；只提示不失败）。")
    if portable_abi:
        print(f"[vendor] 可见 ABI3 便携扩展 {len(portable_abi)} 个（跨平台使用不受 darwin .so 影响）。")
    return 0


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="+", help="要扫描的文件或目录（默认建议 scripts/）")
    ap.add_argument("--skip-dirs", default="vendor,__pycache__,tests,.git",
                    help="跳过的目录名，逗号分隔")
    ap.add_argument("--vendor-check", action="store_true",
                    help="额外探测 vendor 原生库（允许 darwin .so，其它平台缺失不失败）")
    ap.add_argument("--vendor", default=str(DEFAULT_VENDOR), help="vendor 目录")
    ap.add_argument("--platform", default=platform.system(),
                    help="当前平台名（darwin/windows/linux/win/macos/ubuntu...，用于 CI 等价模拟）")
    ap.add_argument("--strict", action="store_true",
                    help="把 WARN 也当作失败（默认只对 ERROR 返回非 0）")
    args = ap.parse_args()

    files = _walk_files(args.paths, args.skip_dirs)
    findings: list[dict] = []
    for f in files:
        findings.extend(_scan_file(f))

    errors = [x for x in findings if x["level"] == "ERROR"]
    warns = [x for x in findings if x["level"] == "WARN"]
    for x in errors + warns:
        print(f"{x['file']}:{x['line']} [{x['rule']}|{x['level']}] {x['text']}")
        print(f"  → {x['fix']}")

    rc = 0
    if args.vendor_check:
        rc |= _vendor_probe(Path(args.vendor), args.platform)
    if errors:
        rc = 1
    if args.strict and warns:
        rc = 1

    print(f"扫描 {len(files)} 个文件，命中 ERROR {len(errors)} 处 / WARN {len(warns)} 处（共 {len(findings)} 处）")
    return rc


if __name__ == "__main__":
    sys.exit(main())
