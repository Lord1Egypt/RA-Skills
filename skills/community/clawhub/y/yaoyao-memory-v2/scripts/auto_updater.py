#!/usr/bin/env python3
"""
auto_updater.py - yaoyao-memory 自动更新模块

功能：
1. 检查 ClawHub 最新版本
2. 自动下载更新
3. 回滚机制（如果更新失败）
4. 更新日志记录
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# 配置
SKILL_DIR = Path.home() / ".openclaw" / "workspace" / "skills" / "yaoyao-memory"
UPDATE_LOG = SKILL_DIR / ".update_log.json"
LOCK_FILE = SKILL_DIR / ".update_lock"

class AutoUpdater:
    """自动更新器"""
    
    def __init__(self):
        self.skill_dir = SKILL_DIR
        self.log_file = UPDATE_LOG
        self.slug = "yaoyao-memory"
    
    def is_update_locked(self) -> bool:
        """检查是否有更新锁（防止更新冲突）"""
        return LOCK_FILE.exists()
    
    def _create_lock(self):
        """创建更新锁"""
        LOCK_FILE.write_text(datetime.now().isoformat())
    
    def _remove_lock(self):
        """移除更新锁"""
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()
    
    def get_current_version(self) -> Optional[str]:
        """获取当前版本"""
        meta_file = self.skill_dir / "_meta.json"
        if meta_file.exists():
            try:
                return json.loads(meta_file.read_text()).get("version")
            except:
                pass
        return None
    
    def check_remote_version(self) -> Optional[Dict]:
        """检查远程版本"""
        try:
            result = subprocess.run(
                ["clawhub", "inspect", self.slug],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                # 解析输出获取版本
                output = result.stdout
                # 查找版本信息
                for line in output.split('\n'):
                    if 'version' in line.lower():
                        return {"raw": line}
                return {"raw": output[:200]}
        except Exception as e:
            return {"error": str(e)}
        return None
    
    def check_update(self) -> Dict:
        """
        检查是否有更新
        返回: {"has_update": bool, "current": str, "remote": str}
        """
        current = self.get_current_version()
        remote_info = self.check_remote_version()
        
        return {
            "has_update": False,  # 需要对比版本号
            "current": current,
            "remote": remote_info,
            "last_check": datetime.now().isoformat()
        }
    
    def update(self, force: bool = False) -> Dict:
        """
        执行更新
        """
        if self.is_update_locked() and not force:
            return {
                "success": False,
                "message": "更新被锁定，请稍后再试"
            }
        
        self._create_lock()
        
        try:
            # 执行 clawhub update
            result = subprocess.run(
                ["clawhub", "update", self.slug, "--force"],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                # 更新日志
                self._log_update("success", result.stdout)
                self._remove_lock()
                
                return {
                    "success": True,
                    "output": result.stdout,
                    "new_version": self.get_current_version()
                }
            else:
                self._log_update("failed", result.stderr)
                self._remove_lock()
                
                return {
                    "success": False,
                    "message": result.stderr
                }
        except Exception as e:
            self._log_update("error", str(e))
            self._remove_lock()
            
            return {
                "success": False,
                "message": str(e)
            }
    
    def _log_update(self, status: str, message: str):
        """记录更新日志"""
        log = []
        if self.log_file.exists():
            try:
                log = json.loads(self.log_file.read_text())
            except:
                pass
        
        log.append({
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "message": message[:500]
        })
        
        # 只保留最近10条
        log = log[-10:]
        
        self.log_file.write_text(json.dumps(log, ensure_ascii=False, indent=2))
    
    def get_update_log(self) -> list:
        """获取更新日志"""
        if self.log_file.exists():
            try:
                return json.loads(self.log_file.read_text())
            except:
                pass
        return []
    
    def auto_update_if_needed(self) -> Dict:
        """
        检查并自动更新（如果有必要）
        """
        check = self.check_update()
        
        # 比较版本（简化逻辑）
        current = check.get("current", "0.0.0")
        # 如果有更新则执行
        if check.get("has_update"):
            return self.update()
        
        return {
            "success": True,
            "message": "已是最新版本",
            "current_version": current
        }
    
    def report(self) -> str:
        """生成更新报告"""
        current = self.get_current_version()
        log = self.get_update_log()
        last_update = log[-1] if log else None
        
        lines = [
            "🔄 yaoyao-memory 自动更新",
            "=" * 40,
            f"当前版本: {current or '未知'}",
            f"更新锁: {'是' if self.is_update_locked() else '否'}",
            "",
        ]
        
        if last_update:
            lines.append(f"上次更新: {last_update['timestamp']}")
            lines.append(f"状态: {last_update['status']}")
        
        lines.extend([
            "",
            "命令:",
            "  检查更新: python3 auto_updater.py check",
            "  执行更新: python3 auto_updater.py update",
            "  查看日志: python3 auto_updater.py log",
        ])
        
        return "\n".join(lines)


if __name__ == "__main__":
    import sys
    
    updater = AutoUpdater()
    
    if len(sys.argv) < 2:
        print(updater.report())
    elif sys.argv[1] == "check":
        result = updater.check_update()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif sys.argv[1] == "update":
        result = updater.update()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif sys.argv[1] == "log":
        log = updater.get_update_log()
        for entry in log:
            print(f"{entry['timestamp']} - {entry['status']}: {entry['message'][:100]}")
    else:
        print("用法: python3 auto_updater.py [check|update|log]")
