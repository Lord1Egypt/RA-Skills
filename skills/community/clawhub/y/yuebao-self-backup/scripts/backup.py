#!/usr/bin/env python3
"""
yue宝 自备份脚本
备份 OpenClaw 配置、技能、记忆到本地压缩包
"""

import os
import sys
import tarfile
import json
import shutil
from datetime import datetime
from pathlib import Path

HOME = Path.home()
OPENCLAW_DIR = HOME / ".openclaw"
WORKSPACE_DIR = OPENCLAW_DIR / "workspace"
BACKUP_DIR = HOME / "backups"

# 要备份的路径（相对于HOME）
BACKUP_PATHS = [
    # 核心配置
    ".openclaw/openclaw.json",
    ".openclaw/.env",
    ".openclaw/cron/jobs.json",
    # 凭证（加密存储，备份后需妥善保管）
    ".openclaw/credentials",
    ".openclaw/identity",
    # 工作区核心文件
    ".openclaw/workspace/MEMORY.md",
    ".openclaw/workspace/SOUL.md",
    ".openclaw/workspace/IDENTITY.md",
    ".openclaw/workspace/USER.md",
    ".openclaw/workspace/AGENTS.md",
    ".openclaw/workspace/TOOLS.md",
    ".openclaw/workspace/HEARTBEAT.md",
    ".openclaw/workspace/BOOTSTRAP.md",
    # 技能
    ".openclaw/workspace/skills",
    # 记忆
    ".openclaw/workspace/memory",
    # 投资文档
    ".openclaw/workspace/investment_plan_FINAL_v6.md",
    ".openclaw/workspace/investment_plan_FINAL_v5.md",
]

# 排除的路径（太大或可重建）
EXCLUDE_PATTERNS = [
    ".venv-stock",
    "__pycache__",
    "*.pyc",
    ".git",
    "node_modules",
]

def should_exclude(path_str):
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith("*."):
            ext = pattern[1:]
            if path_str.endswith(ext):
                return True
        elif pattern in path_str:
            return True
    return False

def create_backup():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d_%H%M")
    backup_name = f"openclaw-backup-{date_str}.tar.gz"
    backup_path = BACKUP_DIR / backup_name

    print(f"🗄️  开始备份 yue宝...")
    print(f"📦  备份文件: {backup_path}")
    print()

    included = []
    skipped = []

    with tarfile.open(backup_path, "w:gz") as tar:
        for rel_path in BACKUP_PATHS:
            full_path = HOME / rel_path
            if not full_path.exists():
                skipped.append(f"  ⚠️  不存在: {rel_path}")
                continue
            if should_exclude(str(full_path)):
                skipped.append(f"  ⏭️  已排除: {rel_path}")
                continue

            tar.add(full_path, arcname=rel_path,
                    filter=lambda ti: None if should_exclude(ti.name) else ti)
            included.append(f"  ✅  {rel_path}")

    # 写入备份清单
    manifest = {
        "backup_date": datetime.now().isoformat(),
        "backup_file": backup_name,
        "openclaw_version": "2026.3.13",
        "included_paths": [p.strip("  ✅  ") for p in included],
        "restore_instructions": "python3 restore.py <backup_file>",
        "python_env_rebuild": "pip install yfinance pandas numpy pandas-ta ta ddgs tavily-python requests beautifulsoup4",
    }
    manifest_path = BACKUP_DIR / f"manifest-{date_str}.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # 更新 latest 软链接
    latest_link = BACKUP_DIR / "openclaw-backup-latest.tar.gz"
    if latest_link.exists() or latest_link.is_symlink():
        latest_link.unlink()
    latest_link.symlink_to(backup_path)

    # 输出结果
    print("已备份:")
    for line in included:
        print(line)
    if skipped:
        print("\n跳过:")
        for line in skipped:
            print(line)

    size_mb = backup_path.stat().st_size / 1024 / 1024
    print(f"\n✅  备份完成！")
    print(f"   文件: {backup_path}")
    print(f"   大小: {size_mb:.1f} MB")
    print(f"   清单: {manifest_path}")

    # 保留最近6个备份，超出自动删除最早的
    backups = sorted(BACKUP_DIR.glob("openclaw-backup-*.tar.gz"),
                     key=lambda p: p.stat().st_mtime, reverse=True)
    backups = [b for b in backups if not b.name == "openclaw-backup-latest.tar.gz"]
    if len(backups) > 6:
        for old in backups[6:]:
            print(f"   🗑️   删除旧备份: {old.name}")
            old.unlink()

    return backup_path

def list_backups():
    if not BACKUP_DIR.exists():
        print("暂无备份")
        return
    backups = sorted(BACKUP_DIR.glob("openclaw-backup-*.tar.gz"),
                     key=lambda p: p.stat().st_mtime, reverse=True)
    backups = [b for b in backups if not b.name == "openclaw-backup-latest.tar.gz"]
    if not backups:
        print("暂无备份")
        return
    print(f"📦  找到 {len(backups)} 个备份:")
    for b in backups:
        size_mb = b.stat().st_size / 1024 / 1024
        mtime = datetime.fromtimestamp(b.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        print(f"  {mtime}  {b.name}  ({size_mb:.1f} MB)")

if __name__ == "__main__":
    if "--list" in sys.argv or "-l" in sys.argv:
        list_backups()
    else:
        create_backup()
