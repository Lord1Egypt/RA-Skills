#!/usr/bin/env python3
"""
statsoft-cli Automated Tests
验证技能结构完整性、路径引用正确性、配置文件有效性。
支持 34 款统计软件。
"""

import os
import sys
import json
import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
CONFIG_FILE = SKILL_DIR / "config.json"

passed = 0
failed = 0


def check(condition, description):
    global passed, failed
    if condition:
        print(f"  \033[32m✓\033[0m {description}")
        passed += 1
    else:
        print(f"  \033[31m✗ {description}\033[0m")
        failed += 1


def section(title):
    print(f"\n\033[36m=== {title} ===\033[0m")


# --- Structure Tests ---
section("目录结构")

required_dirs = [
    SCRIPTS_DIR,
    SCRIPTS_DIR / "cross-platform",
    SCRIPTS_DIR / "windows-only",
    SKILL_DIR / "references",
    SKILL_DIR / "tests",
]
for d in required_dirs:
    check(d.is_dir(), f"目录存在: {d.relative_to(SKILL_DIR)}")

required_files = [
    SKILL_DIR / "SKILL.md",
    SKILL_DIR / "README.md",
    SKILL_DIR / "README_zh-CN.md",
    SKILL_DIR / "LICENSE",
    SKILL_DIR / "config.json.example",
    SKILL_DIR / "references" / "command-examples.md",
    SKILL_DIR / "references" / "version-specifics.md",
    SKILL_DIR / "references" / "completion-prompts.md",
]
for f in required_files:
    check(f.is_file(), f"文件存在: {f.relative_to(SKILL_DIR)}")

# --- Path References in SKILL.md ---
section("SKILL.md 路径引用")

skill_md = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

routing_entries = [
    "scripts/windows-only/SPSS/setup_spss.ps1",
    "scripts/windows-only/statsoft-r.ps1",
    "scripts/cross-platform/R/setup_r.sh",
    "scripts/cross-platform/Stata/setup_stata.sh",
    "scripts/windows-only/statsoft-sas.ps1",
    "scripts/cross-platform/SAS/setup_sas.sh",
]
for entry in routing_entries:
    check(entry in skill_md, f"路由表路径存在: {entry}")

# Check old paths NOT present (avoid substring matches)
import re
old_patterns = [
    r"(?<!scripts/)windows-only/SPSS/setup_spss\.ps1",
    r"(?<!scripts/)cross-platform/R/setup_r\.sh",
]
for pat in old_patterns:
    check(not re.search(pat, skill_md), f"旧路径已移除: {pat}")

# --- config.json validity ---
section("config.json")

if CONFIG_FILE.is_file():
    try:
        config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        check(True, "config.json 是有效 JSON")
        required_sw = ["SPSS", "R", "Stata", "SAS"]
        for sw in required_sw:
            check(sw in config or sw.lower() in [k.lower() for k in config.keys()],
                  f"  - {sw} 已配置")
    except json.JSONDecodeError as e:
        check(False, f"config.json JSON 解析失败: {e}")
else:
    check((SKILL_DIR / "config.json.example").is_file(), "config.json 不存在（运行时生成，example 模板存在）")

# --- Setup scripts cross-platform: no hardcoded paths ---
section("cross-platform setup 脚本变量传递")

cross_platform_dir = SCRIPTS_DIR / "cross-platform"
for sh_file in cross_platform_dir.rglob("setup_*.sh"):
    content = sh_file.read_text(encoding="utf-8")
    # Check no bare $VAR inside python3 -c "..." strings
    has_inline = 'python3 -c "' in content or "python3 -c '" in content
    check(not has_inline or 'sys.argv' in content,
          f"{sh_file.relative_to(SKILL_DIR)}: sys.argv 变量传递")

# --- Summary ---
section("测试结果")
print(f"  通过: {passed}")
print(f"  失败: {failed}")
print(f"  总计: {passed + failed}")

sys.exit(0 if failed == 0 else 1)
