#!/usr/bin/env python3
"""
OpenClaw 秘书式记忆系统 - 迁移脚本
将旧的扁平结构迁移到新的秘书式分区结构

用法:
    python3 migrate.py [--dry-run]           # 干跑测试
    python3 migrate.py                        # 执行迁移

旧结构:
    memory/
    ├── 2026-03-10.md
    ├── 2026-03-12.md
    └── ... (所有 md 文件在根目录)

新结构:
    memory/
    ├── daily/           # 每日日志
    ├── archive/         # 归档
    ├── agenda/          # 待办
    ├── profile/         # 偏好
    ├── projects/        # 进行中项目
    ├── knowledge/       # 知识
    └── ... (脚本和配置在根目录)

迁移逻辑:
    1. 创建新目录结构
    2. 备份旧文件到 .backup/
    3. 移动日期格式的 md 文件到 daily/
    4. 移动项目相关的 md 文件到 projects/
    5. 移动论文相关的 md 文件到 projects/
    6. 创建索引文件
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
import argparse

# ============== 配置 ==============
MEMORY_DIR = Path(os.environ.get("OPENCLAW_MEMORY_DIR", "/root/.openclaw/workspace/memory"))
BACKUP_DIR = MEMORY_DIR / ".backup"

# 新目录
NEW_DIRS = [
    "daily",
    "archive/daily",
    "archive/projects",
    "archive/decisions",
    "agenda/today",
    "agenda/this-week",
    "agenda/follow-ups",
    "profile/preferences",
    "profile/habits",
    "profile/contacts",
    "projects",
    "knowledge/tech",
    "knowledge/domain",
]


# ============== 迁移引擎 ==============

class MigrationManager:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.stats = {
            "created_dirs": [],
            "migrated_files": [],
            "backed_up": [],
            "errors": []
        }

    def log(self, msg: str):
        print(f"[Migration] {msg}")

    def ensure_dirs(self):
        """创建新目录结构"""
        for d in NEW_DIRS:
            path = MEMORY_DIR / d
            if not self.dry_run:
                path.mkdir(parents=True, exist_ok=True)
            self.stats["created_dirs"].append(d)
            self.log(f"创建目录: {d}")

    def backup_old_structure(self):
        """备份旧结构到 .backup/"""
        if self.dry_run:
            self.log(f"[DRY] 备份到: {BACKUP_DIR}")
            return

        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        for item in MEMORY_DIR.iterdir():
            if item.is_file() and not item.name.startswith('.'):
                dest = BACKUP_DIR / item.name
                shutil.copy2(item, dest)
                self.stats["backed_up"].append(item.name)
        self.log(f"备份完成: {len(self.stats['backed_up'])} 个文件")

    def migrate_daily_files(self):
        """迁移日期格式的日志文件到 daily/"""
        daily_target = MEMORY_DIR / "daily"

        for item in MEMORY_DIR.iterdir():
            if not item.is_file():
                continue
            # 匹配 YYYY-MM-DD.md 格式
            if re.match(r'^\d{4}-\d{2}-\d{2}\.md$', item.name):
                dest = daily_target / item.name
                if self.dry_run:
                    self.log(f"[DRY] 移动: {item.name} -> daily/")
                else:
                    shutil.move(str(item), str(dest))
                self.stats["migrated_files"].append(item.name)

    def migrate_projects(self):
        """迁移项目相关文件到 projects/"""
        for item in MEMORY_DIR.iterdir():
            if not item.is_file():
                continue
            if "项目" in item.name or "project" in item.name.lower():
                dest = MEMORY_DIR / "projects" / item.name
                if self.dry_run:
                    self.log(f"[DRY] 移动: {item.name} -> projects/")
                else:
                    shutil.move(str(item), str(dest))
                self.stats["migrated_files"].append(item.name)

    def migrate_thesis(self):
        """迁移论文相关文件到 projects/"""
        keywords = ["论文", "毕业", "thesis", "毕设"]
        for item in MEMORY_DIR.iterdir():
            if not item.is_file():
                continue
            if any(kw in item.name for kw in keywords):
                dest = MEMORY_DIR / "projects" / item.name
                if self.dry_run:
                    self.log(f"[DRY] 移动: {item.name} -> projects/")
                else:
                    shutil.move(str(item), str(dest))
                self.stats["migrated_files"].append(item.name)

    def create_index_files(self):
        """创建索引文件"""
        # projects/README.md
        readme = MEMORY_DIR / "projects" / "README.md"
        if not readme.exists():
            content = """# 项目目录

此目录包含进行中的项目记忆。

## 文件规范

- `<项目名>.md` - 项目主文件
- 包含: 项目信息、状态、路径、备注

## 项目列表

（由 consolidation 脚本自动维护）
"""
            if not self.dry_run:
                readme.write_text(content, encoding="utf-8")
            self.log("创建: projects/README.md")

    def run(self):
        """执行迁移"""
        self.log(f"开始迁移 (dry_run={self.dry_run})")
        self.log(f"Memory 目录: {MEMORY_DIR}")

        # 1. 创建新目录
        self.ensure_dirs()

        # 2. 备份旧文件
        self.backup_old_structure()

        # 3. 迁移文件
        self.migrate_daily_files()
        self.migrate_projects()
        self.migrate_thesis()

        # 4. 创建索引
        self.create_index_files()

        # 5. 打印报告
        self.print_report()

        return self.stats

    def print_report(self):
        """打印迁移报告"""
        print("\n" + "=" * 50)
        print("[Migration] 迁移完成!")
        print(f"  创建目录: {len(self.stats['created_dirs'])}")
        print(f"  迁移文件: {len(self.stats['migrated_files'])}")
        print(f"  备份文件: {len(self.stats['backed_up'])}")
        print(f"  错误: {len(self.stats['errors'])}")

        if self.stats['migrated_files']:
            print("\n迁移的文件:")
            for f in self.stats['migrated_files']:
                print(f"  - {f}")

        if self.stats['errors']:
            print("\n错误:")
            for e in self.stats['errors']:
                print(f"  - {e}")


# ============== 主程序 ==============

def main():
    parser = argparse.ArgumentParser(description="OpenClaw 秘书式记忆系统 - 迁移脚本")
    parser.add_argument("--dry-run", action="store_true", help="仅显示将要执行的操作，不实际修改")
    args = parser.parse_args()

    migrator = MigrationManager(dry_run=args.dry_run)
    migrator.run()


if __name__ == "__main__":
    main()
