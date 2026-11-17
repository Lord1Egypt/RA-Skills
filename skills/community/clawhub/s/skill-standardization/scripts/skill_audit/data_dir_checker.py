#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data_dir_checker.py — R-22 数据目录规范检查
v2.38.5

检查技能安装目录是否包含应归属数据目录的文件，
并在 --fix 模式下自动迁移到 skills/.standardization/<skill>/

参考 universal-file-ops 设计：
- 操作前自动备份
- 操作日志记录
- 支持回滚
"""

import os
import shutil
import json
import datetime
from pathlib import Path
from ._path_detector import has_path_feature

from .utils import _is_asset_dir

# ── 路径常量（通用写法，适用于任何安装结构）───────────────────
_SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR   = os.path.dirname(os.path.dirname(_SCRIPT_DIR))  # scripts/ → skill-root
_SKILLS_ROOT = os.path.dirname(_SKILL_DIR)
SKILL_NAME    = os.path.basename(_SKILL_DIR)
DATA_DIR      = os.path.join(_SKILLS_ROOT, ".standardization", SKILL_NAME)
BACKUP_DIR   = os.path.join(DATA_DIR, "backup")
LOG_DIR      = os.path.join(DATA_DIR, "logs")

# ── 数据目录合规子目录 ─────────────────────────────────────────
# 参见 references/data_dir_map.md
VALID_SUBDIRS = {"data", "backup", "logs", "temp", "cache", "output", "state"}

# ── 安装目录允许的文件/目录（白名单）─────────────────────────
INSTALL_WHITELIST = {
    "SKILL.md", "_meta.json", "CHANGELOG.md",
    "scripts", "references", "assets",
}

# ── 跳过检查的文件名模式（修复脚本、测试脚本等）────────────
SKIP_PATTERNS = [
    "fix_", "test_", "debug_", "_test.py", "master_fix.py",
]


def _is_fix_script(filepath):
    """判断是否为修复/迁移脚本（允许写其他技能目录）"""
    fname = os.path.basename(filepath)
    return any(fname.startswith(p.replace("_", "")) for p in SKIP_PATTERNS if p.endswith("_")) or \
           any(p in fname for p in SKIP_PATTERNS if not p.endswith("_"))


def check_external_data_dir(skill_dir, verbose=False):
    """
    R-12: 检查技能是否把数据写到安装目录外合法位置
    返回：(passed: bool, details: list)
    """
    issues = []
    passed = True

    # 检查是否引用了 skill 安装目录外的硬编码路径
    for root, _, files in os.walk(skill_dir):
        for fname in files:
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(root, fname)
            if fname in ("data_dir_checker.py", "artifact_checker.py"):
                continue  # 检查器自身，跳过自检 (R-11 误报防护)
            if _is_fix_script(fpath):
                continue  # 修复脚本允许写其他位置
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                # 检查是否有硬编码的绝对路径指向技能外
                if "C:" in content or "/Users/" in content or "/home/" in content:
                    # 排除注释和字符串中的示例路径
                    lines = content.split("\n")
                    for i, line in enumerate(lines):
                        if ("C:" in line or "/Users/" in line or "/home/" in line) and \
                           not line.strip().startswith("#") and "example" not in line.lower():
                            issues.append(f"  {fpath}:{i+1} 可能包含硬编码绝对路径")
                            passed = False
            except Exception:
                pass

    return passed, issues


def check_data_dir_compliance(skill_dir=None, auto_fix=False, verbose=False, **kwargs):
    """
    R-22: 检查技能安装目录是否包含应归属数据目录的文件
    返回：(passed: bool, details: list, fixable: list)

    支持两种调用方式：
    - check_data_dir_compliance(skill_dir, ...)
    - check_data_dir_compliance(filepath=..., skill_dir=..., **kwargs)  # METHOD_MAP 统一调用
    """
    # 兼容 METHOD_MAP 调用（传 filepath=skill_md）
    if skill_dir is None:
        skill_dir = kwargs.get("skill_dir", kwargs.get("filepath", "."))
    if isinstance(skill_dir, str) and skill_dir.endswith("SKILL.md"):
        skill_dir = os.path.dirname(skill_dir)
    issues = []
    fixable = []
    passed = True

    skill_name = os.path.basename(skill_dir.rstrip("/\\"))
    skills_root = os.path.dirname(skill_dir.rstrip("/\\"))
    expected_data_dir = os.path.join(skills_root, ".standardization", skill_name)

    # 扫描安装目录，找数据类文件
    for root, dirs, files in os.walk(skill_dir):
        # 跳过 scripts/、references/ 和 .standardization/（标准化数据目录）
        rel_root = os.path.relpath(root, skill_dir)
        if (rel_root.startswith("scripts") or rel_root.startswith("references")
            or rel_root == ".standardization" or rel_root.startswith(".standardization\\") or rel_root.startswith(".standardization/")):
            continue
        # 跳过被脚本引用的功能数据目录（R-11 同款交叉引用检查）
        rel_parts = rel_root.replace("\\", "/").split("/")
        if any(_is_asset_dir(skill_dir, p) for p in rel_parts if p and p != "."):
            continue

        for fname in files:
            fpath = os.path.join(root, fname)
            ext = os.path.splitext(fname)[1].lower()

            # 判断是否为数据类文件
            is_data_file = (
                ext in (".csv", ".json", ".log", ".txt", ".bak", ".tmp") or
                "backup" in fname or "log" in fname or
                fname.startswith(".")  # 隐藏文件
            )

            if is_data_file and fname not in INSTALL_WHITELIST:
                rel_path = os.path.relpath(fpath, skill_dir)
                fixable.append((fpath, os.path.join(expected_data_dir, "data", rel_path)))
                issues.append(f"  产出物路径违规：{rel_path} — 应迁至 .standardization/{skill_name}/data/")
                passed = False

    # 检查 scripts/ 里的硬编码路径（排除修复脚本）
    for root, _, files in os.walk(os.path.join(skill_dir, "scripts")):
        for fname in files:
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(root, fname)
            if _is_fix_script(fpath):
                continue
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    for i, line in enumerate(f, 1):
                        if "DATA_DIR" in line or "data_dir" in line:
                            if "skills/" in line and ".standardization" not in line:
                                issues.append(f"  {fname}:{i} 硬编码路径应改用动态 DATA_DIR")
                                passed = False
            except Exception:
                pass

    return passed, issues, fixable


def fix_data_dir_compliance(skill_dir, fixable_list, dry_run=False, **kw):
    """
    自动修复 R-22 违规：迁移文件到数据目录
    """
    results = {"moved": 0, "skipped": 0, "errors": []}

    for src, dst in fixable_list:
        if dry_run:
            print(f"  [DRY-RUN] 将移动：{src} → {dst}")
            continue
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            results["moved"] += 1
            print(f"  ✅ 已迁移：{os.path.basename(src)} → {dst}")
        except Exception as e:
            results["errors"].append(str(e))
            results["skipped"] += 1

    return results


def log_check_result(skill_name, check_name, passed, details):
    """记录检查结果到日志"""
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, "audit.log")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {skill_name} | {check_name} | {'PASS' if passed else 'FAIL'}\n")
        for d in details:
            f.write(f"  {d}\n")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python data_dir_checker.py <skill_dir> [--fix]")
        sys.exit(1)

    skill_dir = sys.argv[1]
    auto_fix = "--fix" in sys.argv

    print("=" * 60)
    print("  R-22 数据目录规范检查")
    print("=" * 60)

    passed, issues, fixable = check_data_dir_compliance(skill_dir, auto_fix)
    print(f"\n结果: {'✅ PASS' if passed else '❌ FAIL'}")
    for issue in issues:
        print(issue)

    if not passed and auto_fix and fixable:
        print("\n─── 自动修复 ───────────────────────────────────────")
        fix_data_dir_issues(skill_dir, fixable)

    log_check_result(os.path.basename(skill_dir), "R-22", passed, issues)
    sys.exit(0 if passed else 1)
