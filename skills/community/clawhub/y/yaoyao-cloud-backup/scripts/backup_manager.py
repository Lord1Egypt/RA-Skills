#!/usr/bin/env python3
"""
backup_manager.py - 备份管理器

功能：
- 手动/自动备份记忆目录
- 增量备份（只备份变更的文件）
- 备份列表和恢复
- 压缩备份
"""

import argparse
import gzip
import hashlib
import json
import os
import shutil
import tarfile
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
BACKUP_DIR = MEMORY_DIR / "backups"
BACKUP_INDEX = BACKUP_DIR / ".backup_index.json"


@dataclass
class BackupInfo:
    """备份信息"""
    id: str
    timestamp: str
    size: int  # bytes
    file_count: int
    hash: str  # 备份文件的 MD5
    description: str = ""
    full: bool = True  # True=全量, False=增量


class BackupManager:
    """备份管理器"""
    
    def __init__(self):
        self.backups: List[BackupInfo] = []
        self.load_index()
    
    def load_index(self):
        """加载备份索引"""
        if BACKUP_INDEX.exists():
            try:
                with open(BACKUP_INDEX) as f:
                    data = json.load(f)
                    self.backups = [BackupInfo(**b) for b in data.get("backups", [])]
            except:
                self.backups = []
    
    def save_index(self):
        """保存备份索引"""
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        with open(BACKUP_INDEX, "w") as f:
            json.dump({
                "backups": [asdict(b) for b in self.backups],
            }, f, indent=2)
    
    def calculate_hash(self, filepath: Path) -> str:
        """计算文件 MD5"""
        md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                md5.update(chunk)
        return md5.hexdigest()
    
    def create_backup(self, description: str = "", full: bool = False) -> BackupInfo:
        """创建备份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_id = f"backup_{timestamp}"
        
        # 查找上一个全量备份
        last_full = None
        for b in reversed(self.backups):
            if b.full:
                last_full = b
                break
        
        # 收集要备份的文件
        files_to_backup = []
        if full or not last_full:
            # 全量备份
            for f in MEMORY_DIR.glob("*.md"):
                if f.name.startswith("."):
                    continue
                files_to_backup.append(f)
        else:
            # 增量备份：只备份变更的文件
            last_backup_file = BACKUP_DIR / f"{last_full.id}.tar.gz"
            if last_backup_file.exists():
                last_mtime = last_backup_file.stat().st_mtime
                for f in MEMORY_DIR.glob("*.md"):
                    if f.name.startswith("."):
                        continue
                    if f.stat().st_mtime > last_mtime:
                        files_to_backup.append(f)
        
        if not files_to_backup:
            print("没有需要备份的文件")
            return None
        
        # 创建备份文件
        backup_file = BACKUP_DIR / f"{backup_id}.tar.gz"
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        
        total_size = 0
        with tarfile.open(backup_file, "w:gz") as tar:
            for f in files_to_backup:
                tar.add(f, arcname=f.name)
                total_size += f.stat().st_size
        
        # 计算备份文件 hash
        backup_hash = self.calculate_hash(backup_file)
        
        # 创建备份信息
        info = BackupInfo(
            id=backup_id,
            timestamp=datetime.now().isoformat(),
            size=backup_file.stat().st_size,
            file_count=len(files_to_backup),
            hash=backup_hash,
            description=description,
            full=full or not last_full,
        )
        
        self.backups.append(info)
        self.save_index()
        
        return info
    
    def list_backups(self) -> List[BackupInfo]:
        """列出所有备份"""
        return sorted(self.backups, key=lambda b: b.timestamp, reverse=True)
    
    def restore_backup(self, backup_id: str, target_dir: Path = None) -> bool:
        """恢复备份"""
        target = target_dir or MEMORY_DIR
        
        backup_file = BACKUP_DIR / f"{backup_id}.tar.gz"
        if not backup_file.exists():
            print(f"备份文件不存在: {backup_file}")
            return False
        
        # 验证 hash
        current_hash = self.calculate_hash(backup_file)
        info = next((b for b in self.backups if b.id == backup_id), None)
        if info and info.hash != current_hash:
            print("⚠️ 警告: 备份文件 hash 不匹配，可能已损坏")
        
        # 解压到临时目录
        with tempfile.TemporaryDirectory() as tmpdir:
            with tarfile.open(backup_file, "r:gz") as tar:
                tar.extractall(tmpdir)
            
            # 移动文件到目标目录
            for f in Path(tmpdir).glob("*.md"):
                dest = target / f.name
                shutil.copy2(f, dest)
        
        print(f"✅ 已恢复到: {target}")
        return True
    
    def delete_backup(self, backup_id: str) -> bool:
        """删除备份"""
        backup_file = BACKUP_DIR / f"{backup_id}.tar.gz"
        if backup_file.exists():
            backup_file.unlink()
        
        self.backups = [b for b in self.backups if b.id != backup_id]
        self.save_index()
        return True
    
    def prune_old_backups(self, keep: int = 10) -> int:
        """清理旧备份（保留最近 N 个）"""
        backups = self.list_backups()
        if len(backups) <= keep:
            return 0
        
        to_delete = backups[keep:]
        for b in to_delete:
            self.delete_backup(b.id)
        
        return len(to_delete)


def main():
    parser = argparse.ArgumentParser(description="备份管理")
    parser.add_argument("--create", "-c", action="store_true", help="创建备份")
    parser.add_argument("--list", "-l", action="store_true", help="列出备份")
    parser.add_argument("--restore", "-r", help="恢复备份")
    parser.add_argument("--delete", "-d", help="删除备份")
    parser.add_argument("--prune", "-p", type=int, default=0, help="清理旧备份（保留数量）")
    parser.add_argument("--full", "-f", action="store_true", help="全量备份")
    parser.add_argument("--desc", help="备份描述")
    
    args = parser.parse_args()
    
    manager = BackupManager()
    
    if args.create:
        info = manager.create_backup(args.desc or "", full=args.full)
        if info:
            full_mark = "全量" if info.full else "增量"
            print(f"✅ 备份创建成功: {info.id}")
            print(f"   类型: {full_mark}")
            print(f"   文件: {info.file_count}个")
            print(f"   大小: {info.size / 1024:.1f}KB")
    
    elif args.list:
        backups = manager.list_backups()
        if not backups:
            print("暂无备份")
        else:
            print(f"📦 备份列表 ({len(backups)}个)")
            for b in backups:
                full_mark = "📦" if b.full else "📁"
                ts = b.timestamp[:19]
                print(f"  {full_mark} {b.id}")
                print(f"     {ts} | {b.file_count}文件 | {b.size/1024:.1f}KB | {b.description or '无描述'}")
    
    elif args.restore:
        if manager.restore_backup(args.restore):
            print(f"✅ 已恢复: {args.restore}")
        else:
            print(f"❌ 恢复失败: {args.restore}")
    
    elif args.delete:
        manager.delete_backup(args.delete)
        print(f"✅ 已删除: {args.delete}")
    
    elif args.prune > 0:
        deleted = manager.prune_old_backups(args.prune)
        print(f"✅ 已清理 {deleted} 个旧备份")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
