#!/usr/bin/env python3
"""
yue宝 恢复脚本
从备份包恢复 OpenClaw 配置、技能、记忆
"""

import os
import sys
import tarfile
import shutil
import json
from datetime import datetime
from pathlib import Path

HOME = Path.home()

def restore_backup(backup_file):
    backup_path = Path(backup_file)
    if not backup_path.exists():
        print(f"❌  备份文件不存在: {backup_file}")
        sys.exit(1)

    print(f"🔄  开始恢复 yue宝...")
    print(f"📦  备份文件: {backup_path}")
    print()

    # 先备份当前状态（如果存在）
    openclaw_dir = HOME / ".openclaw"
    if openclaw_dir.exists():
        pre_restore_backup = HOME / f"backups/pre-restore-{datetime.now().strftime('%Y%m%d_%H%M')}.tar.gz"
        pre_restore_backup.parent.mkdir(parents=True, exist_ok=True)
        print(f"⚠️  先备份当前状态到: {pre_restore_backup}")
        with tarfile.open(pre_restore_backup, "w:gz") as tar:
            tar.add(openclaw_dir, arcname=".openclaw",
                    filter=lambda ti: None if ".venv-stock" in ti.name or "__pycache__" in ti.name else ti)
        print(f"✅  当前状态已备份")
        print()

    # 解压备份
    print("解压备份文件...")
    with tarfile.open(backup_path, "r:gz") as tar:
        members = tar.getmembers()
        for member in members:
            target = HOME / member.name
            target.parent.mkdir(parents=True, exist_ok=True)
            print(f"  恢复: {member.name}")
        tar.extractall(HOME)

    print()
    print("✅  文件恢复完成！")
    print()
    print("📋  后续步骤:")
    print("   1. 重建 Python 环境（如果是新机器）:")
    print("      cd ~/.openclaw/workspace")
    print("      python3 -m venv .venv-stock")
    print("      source .venv-stock/bin/activate")
    print("      pip install yfinance pandas numpy pandas-ta ta ddgs tavily-python requests beautifulsoup4")
    print()
    print("   2. 重新登录 ClawHub（如果需要）:")
    print("      clawhub auth login --token <YOUR_TOKEN> --no-browser")
    print()
    print("   3. 启动 OpenClaw:")
    print("      openclaw start")
    print()
    print("   4. 验证状态:")
    print("      openclaw status")
    print("      openclaw doctor")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 restore.py <备份文件路径>")
        print("示例: python3 restore.py ~/backups/openclaw-backup-2026-03-19.tar.gz")
        sys.exit(1)
    restore_backup(sys.argv[1])
