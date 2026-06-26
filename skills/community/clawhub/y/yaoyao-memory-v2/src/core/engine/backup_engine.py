#!/usr/bin/env python3
"""Backup Engine - 备份引擎"""

import tarfile
import json
from pathlib import Path
from typing import Dict
from datetime import datetime


class BackupEngine:
    """备份引擎"""
    
    def __init__(self):
        self.backup_dir = Path.home() / ".openclaw" / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def run(self, target: str = "local") -> Dict:
        """执行备份"""
        if target == "local":
            return self._backup_local()
        elif target == "nas":
            return self._backup_nas()
        else:
            return {"status": "error", "message": f"Unknown target: {target}"}
    
    def _backup_local(self) -> Dict:
        """本地备份"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            backup_file = self.backup_dir / f"yaoyao-memory-{timestamp}.tar.gz"
            
            # 打包 memory 目录
            memory_dir = Path.home() / ".openclaw" / "workspace" / "memory"
            
            with tarfile.open(backup_file, "w:gz") as tar:
                tar.add(memory_dir, arcname="memory")
            
            return {
                "status": "ok",
                "file": str(backup_file),
                "size": backup_file.stat().st_size,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _backup_nas(self) -> Dict:
        """NAS备份"""
        # 委托给 sync_engine
        return {
            "status": "ok",
            "message": "NAS backup handled by sync_engine",
        }
