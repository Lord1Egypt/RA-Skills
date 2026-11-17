#!/usr/bin/env python3
"""
skill_builder package — Skill 标准化构建器 v2.30.1

支持三种模式：
  create   — 从模板初始化新的标准 skill
  update   — 对已有 skill 进行增量规范化更新
  refactor — 对非标 skill 进行整体改造（信息零遗漏）

基于 SKILL.md 标准化规范草案 v0.1 + 目录结构规范 + 渐进式 MD 体系。
"""

import argparse
import json
import os
import re
import shutil

import sys
from datetime import datetime
from pathlib import Path

# ── [GBK 兼容] 强制 stdout 使用 UTF-8，防止 Windows 终端 emoji print 崩溃 ──
if sys.stdout.encoding and sys.stdout.encoding.upper() not in ('UTF-8', 'UTF8'):
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1, errors='replace')
if sys.stderr.encoding and sys.stderr.encoding.upper() not in ('UTF-8', 'UTF8'):
    sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1, errors='replace')

# ── 导入子模块 ─────────────────────────────────────────────
from .creator import SkillCreator
from .updater import SkillUpdater
from .refactor import Refactor
from .migrator import SkillMigrator
from .version_manager import VersionManager
from .utils import *

# ── 常量 ─────────────────────────────────────────────
__version__ = "2.30.0"

# R-12: 外部数据目录变量检测模式（通用化，非框架绑定）
_DATA_VAR_RE = re.compile(
    r'^([A-Za-z_]*?(?:DATA|STORAGE|DB|CACHE|CONFIG)[A-Za-z_]*(?:_DIR|_PATH))\s*=\s*(.+)$'
)

SPEC_DIR = Path(__file__).parent / "spec"

# 主 SKILL.md 必须包含的章节（用于 update/refactor 检查）
REQUIRED_SECTIONS = [
    ("触发场景", ["触发条件", "触发场景", "适用场景", "触发"]),
    ("核心能力", ["核心功能", "核心能力", "概述", "核心概念", "Overview", "技能概述"]),
    ("快速开始", ["快速开始", "快速上手", "Quick Start"]),
]

# 可选拆分到 references/ 的章节关键词（用于 refactor 拆分判断）
SPLITTABLE_KEYWORDS = {
    "详细教程": ["详细教程", "使用指南", "完整指南", "逐步指南"],
    "示例集合": ["示例", "examples", "用例", "案例"],
    "参考文档": ["参考文档", "API 参考", "命令参考", "参数说明"],
    "常见问题": ["常见问题", "FAQ", "faq", "疑难解答"],
    "版本日志": ["更新日志", "changelog", "版本历史", "变更记录"],
    "架构设计": ["架构", "architecture", "设计", "模块说明"],
}


def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(description="Skill 标准化构建器 v2.30.0")
    subparsers = parser.add_subparsers(dest="command", help="执行模式")

    # create 子命令
    create_parser = subparsers.add_parser("create", help="创建新 Skill")
    create_parser.add_argument("name", help="技能名称（目录名）")
    create_parser.add_argument("--desc", default="", help="一句话描述")
    create_parser.add_argument("--dir", default=".", help="输出目录（默认当前目录）")
    create_parser.add_argument("--tags", default="", help="逗号分隔标签")

    # update 子命令
    update_parser = subparsers.add_parser("update", help="更新已有 Skill")
    update_parser.add_argument("skill_dir", help="技能目录路径")
    update_parser.add_argument("--fix", action="store_true", help="自动修复可修复项")
    update_parser.add_argument("--backup", action="store_true", help="备份后再修改")
    update_parser.add_argument("--workspace", default=".", help="工作区根目录")
    update_parser.add_argument("--inject-auth", action="store_true",
                             help="扫描风险操作并注入授权要求章节到 SKILL.md")
    update_parser.add_argument("--version-bump", nargs="?", const="patch", default="patch",
                             choices=["patch", "minor", "major"],
                             help="自动升级版本号（默认：patch，传 --version-bump minor/major 指定）")

    # refactor 子命令
    refactor_parser = subparsers.add_parser("refactor", help="改造非标 Skill")
    refactor_parser.add_argument("skill_dir", help="技能目录路径")
    refactor_parser.add_argument("--backup", action="store_true", help="备份后再修改（默认开启）")
    refactor_parser.add_argument("--no-backup", action="store_true", help="跳过备份（不推荐）")
    refactor_parser.add_argument("--dry-run", action="store_true", help="仅输出计划，不执行")
    refactor_parser.add_argument("--workspace", default=".", help="工作区根目录")
    refactor_parser.add_argument("--inject-auth", action="store_true",
                             help="扫描风险操作并注入授权要求章节到 SKILL.md")
    refactor_parser.add_argument("--fix-code", action="store_true",
                             help="自动修复 scripts/ 中硬编码的数据目录路径（阶段3.5）")

    # migrate-data 子命令（v2.30.0 新增）
    migrate_parser = subparsers.add_parser("migrate-data", aliases=["migrate"],
                                      help="迁移技能数据目录到新规范路径")
    migrate_parser.add_argument("skill_dir", help="技能目录路径")
    migrate_parser.add_argument("--dry-run", action="store_true", help="仅输出计划，不执行")
    migrate_parser.add_argument("--force", action="store_true", help="强制覆盖已存在的目标目录")

    # inspect 子命令（v2.44.0 新增）
    inspect_parser = subparsers.add_parser("inspect", help="扫描 skill 结构生成蓝皮书")
    inspect_parser.add_argument("skill_dir", help="技能目录路径")
    inspect_parser.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    if args.command == "create":
        creator = SkillCreator()
        creator.create(args)
    elif args.command == "update":
        updater = SkillUpdater()
        updater.update(args)
    elif args.command == "refactor":
        refactor = Refactor()
        refactor.refactor(args)
    elif args.command in ("migrate-data", "migrate"):
        migrator = SkillMigrator()
        migrator.migrate(args)
    elif args.command == "inspect":
        from ..skill_inspector import inspect_skill
        result = inspect_skill(args.skill_dir, "json" if args.json else "text")
        print(result)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
