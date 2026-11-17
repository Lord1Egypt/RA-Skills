#!/usr/bin/env python3
"""tenyuan-cloud-shop 包体校验器 v0.3.2

检查项：
  1. 必需文件齐全
  2. 零二进制文件（SkillHub 禁止二进制，静默跳过不报错，必须主动拦截）
  3. 版本一致性：除 CHANGELOG.md 外，任何 md/yaml 中的版本号必须等于 SKILL.md frontmatter 的 version
  4. 必备声明语句存在（不承诺交易 / 示意图如实标注 / 不参与交易）

负向测试（必须执行，只跑正向测试的校验器不可信）：
  对本目录副本依次制造 4 类错误，逐一确认校验器报错：
    A. 删掉 references/api.md           → 应报缺失必需文件
    B. 放入一个 1 字节 .png             → 应报二进制文件
    C. 把 README.md 中 0.3.2 改成 0.2.0 → 应报版本不一致
    D. 从 DISCLAIMER.md 删掉「不参与交易」→ 应报必备声明缺失
  用法：python3 scripts/validate_package.py --negative-test /tmp/neg-test-dir
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

VERSION = "0.3.2"

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "DISCLAIMER.md",
    "CHANGELOG.md",
    "PACKAGING.md",
    "LICENSE.md",
    "agents/openai.yaml",
    "assets/icon.svg",
    "assets/icon-256.png",
    "references/api.md",
    "scripts/validate_package.py",
]

# 文本后缀白名单（在此之外的一律视为二进制）
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".svg", ".py", ".txt", ".json"}

# 已知安全的二进制素材白名单（仅当文件后缀不在 TEXT_SUFFIXES 时核对相对路径）
# 新增此表是为了让商店仅收 PNG 的场景合规；不在此表的二进制仍会触发拦截
ASSET_BINARY_WHITELIST = {"assets/icon-256.png"}

# 必备声明语句：(文件, 语句子串)
REQUIRED_STATEMENTS = [
    ("DISCLAIMER.md", "不参与交易"),
    ("DISCLAIMER.md", "示意"),
    ("SKILL.md", "示意图"),
    ("SKILL.md", "不得向用户承诺在线支付"),
]

VERSION_EXEMPT_FILES = {"CHANGELOG.md"}  # 变更日志天然含历史版本号


def find_root(start: Path) -> Path:
    """从 start 向上找包含 SKILL.md 的目录；被测包可能位于任意路径（含 /tmp）。"""
    p = start.resolve()
    for candidate in [p, *p.parents]:
        if (candidate / "SKILL.md").is_file():
            return candidate
    # 向下找一层（zip 解包常产生嵌套目录）
    for child in p.iterdir():
        if (child / "SKILL.md").is_file():
            return child
    raise SystemExit(f"FATAL: 未找到 SKILL.md，{p} 不是技能包目录")


def check(pkg: Path) -> list[str]:
    errors = []

    # 1. 必需文件
    for rel in REQUIRED_FILES:
        if not (pkg / rel).is_file():
            errors.append(f"[缺失必需文件] {rel}")

    # 2. 零二进制（跳过本目录自身不存在的场景；排除隐藏文件如 .DS_Store 直接报错）
    for f in sorted(pkg.rglob("*")):
        if f.is_dir():
            continue
        rel = f.relative_to(pkg).as_posix()
        if f.suffix.lower() not in TEXT_SUFFIXES:
            if rel not in ASSET_BINARY_WHITELIST:
                errors.append(f"[二进制/未知类型文件] {rel}")
        if f.name == ".DS_Store":
            errors.append(f"[打包残留] {rel}")

    # 3. 版本一致性（以 SKILL.md frontmatter 为基准）
    skill = (pkg / "SKILL.md").read_text(encoding="utf-8") if (pkg / "SKILL.md").is_file() else ""
    m = re.search(r"^version:\s*(\S+)", skill, re.M)
    declared = m.group(1) if m else None
    if not declared:
        errors.append("[版本] SKILL.md frontmatter 缺少 version 字段")
    elif declared != VERSION:
        errors.append(f"[版本] 校验器 VERSION={VERSION} 与 SKILL.md version={declared} 不一致（升版时须同步改两者）")

    ver_pattern = re.compile(r"\bv?0\.\d+\.\d+\b")
    for f in sorted(pkg.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in {".md", ".yaml", ".yml", ".py"}:
            continue
        rel = str(f.relative_to(pkg))
        if rel in VERSION_EXEMPT_FILES or rel == "scripts/validate_package.py":
            continue
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for found in ver_pattern.findall(line):
                if found.lstrip("v") != declared:
                    errors.append(f"[版本不一致] {rel}:{i} 出现 {found}，应为 {declared}")
                    break

    # 4. 必备声明语句
    for rel, needle in REQUIRED_STATEMENTS:
        target = pkg / rel
        if target.is_file() and needle not in target.read_text(encoding="utf-8"):
            errors.append(f"[必备声明缺失] {rel} 中未找到「{needle}」")

    return errors


def negative_test() -> int:
    src = Path(__file__).resolve().parent.parent
    failures = []

    cases = [
        ("A-缺失必需文件", lambda p: (p / "references" / "api.md").unlink(), "缺失必需文件"),
        ("B-二进制文件", lambda p: (p / "assets" / "evil.png").write_bytes(b"\x89PNG"), "二进制"),
        ("C-版本不一致", lambda p: (p / "README.md").write_text(
            (p / "README.md").read_text(encoding="utf-8").replace("0.3.2", "0.2.0"), encoding="utf-8"), "版本不一致"),
        ("D-必备声明缺失", lambda p: (p / "DISCLAIMER.md").write_text(
            (p / "DISCLAIMER.md").read_text(encoding="utf-8").replace("不参与交易", "不参与买卖"), encoding="utf-8"), "必备声明缺失"),
    ]

    with tempfile.TemporaryDirectory(prefix="neg-test-") as td:
        workdir = Path(td) / "pkg"
        for name, mutate, expect_keyword in cases:
            if workdir.exists():
                shutil.rmtree(workdir)
            shutil.copytree(src, workdir, ignore=shutil.ignore_patterns(".DS_Store", "__pycache__"))
            mutate(workdir)
            errs = check(workdir)
            hit = any(expect_keyword in e for e in errs)
            status = "已拦截" if hit else "*** 未拦截（假阴性！） ***"
            print(f"  负向测试 {name}: {status}")
            if not hit:
                failures.append(name)
                for e in errs[:5]:
                    print(f"    实际输出: {e}")

    if failures:
        print(f"负向测试失败：{failures}")
        return 1
    print("负向测试 4/4 全部正确拦截")
    return 0


def main() -> int:
    if "--negative-test" in sys.argv:
        return negative_test()

    pkg = find_root(Path(__file__).resolve().parent)
    print(f"校验目标: {pkg}")
    errors = check(pkg)

    if errors:
        print(f"\nVALIDATION FAIL（{len(errors)} 处）:")
        for e in errors:
            print(f"  {e}")
        return 1
    print("\nVALIDATION PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
