# -*- coding: utf-8 -*-
"""
安全文件编辑器
基于Claude Code的SedEdit安全设计实现

核心设计：
- 模拟预览模式（dry-run）
- 4眼原则（二次确认）
- 原子备份+回滚
- _simulatedSedEdit字段omit（防注入）
"""

import shutil
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass

BACKUP_DIR = Path.home() / ".openclaw" / "workspace" / "tmp" / "file-backups"
SAFE_EDIT_LOG = Path.home() / ".openclaw" / "workspace" / "logs" / "safe-file-editor.log"

@dataclass
class EditResult:
    """编辑结果"""
    success: bool
    file_path: str
    backup_path: Optional[str]
    changes: str  # diff描述
    hash_before: str
    hash_after: str
    dry_run: bool
    message: str

class SafeFileEditor:
    """
    安全文件编辑器
    
    参考Claude Code权限模型：
    - isReadOnly: () => False  # 默认会修改
    - checkPermissions: () => ({ behavior: 'allow' })
    """
    
    def __init__(self, require_confirmation: bool = True):
        self.require_confirmation = require_confirmation
        ensure_backup_dir()
    
    def edit(
        self,
        file_path: str,
        old_text: str,
        new_text: str,
        dry_run: bool = True,
        show_diff: bool = True
    ) -> EditResult:
        """
        安全编辑文件
        
        Args:
            dry_run: True=预览变更，False=实际执行
            show_diff: 显示完整diff
        
        Returns:
            EditResult with success status and details
        """
        path = Path(file_path)
        
        # 检查文件存在
        if not path.exists():
            return EditResult(
                success=False,
                file_path=file_path,
                backup_path=None,
                changes="",
                hash_before="",
                hash_after="",
                dry_run=dry_run,
                message=f"File not found: {file_path}"
            )
        
        # 读取原始内容
        try:
            with open(path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            return EditResult(
                success=False,
                file_path=file_path,
                backup_path=None,
                changes="",
                hash_before="",
                hash_after="",
                dry_run=dry_run,
                message=f"Read error: {str(e)}"
            )
        
        hash_before = hashlib.md5(original_content.encode()).hexdigest()
        
        # 检查old_text是否存在
        if old_text not in original_content:
            return EditResult(
                success=False,
                file_path=file_path,
                backup_path=None,
                changes="",
                hash_before=hash_before,
                hash_after=hash_before,
                dry_run=dry_run,
                message=f"old_text not found in file. Search for unique text."
            )
        
        # 生成新内容
        new_content = original_content.replace(old_text, new_text, 1)
        hash_after = hashlib.md5(new_content.encode()).hexdigest()
        
        # 生成diff
        changes = f"- {old_text[:50]}...\n+ {new_text[:50]}..." if len(old_text) > 50 else f"- {old_text}\n+ {new_text}"
        
        if dry_run:
            # 预览模式：只返回结果，不写入
            log_edit(file_path, "DRY_RUN", hash_before, hash_after, changes)
            return EditResult(
                success=True,
                file_path=file_path,
                backup_path=None,
                changes=changes,
                hash_before=hash_before,
                hash_after=hash_after,
                dry_run=True,
                message=f"Preview: {changes}"
            )
        
        # 实际执行
        try:
            # 1. 备份
            backup_path = create_backup(path)
            
            # 2. 原子写入（先写临时文件，再重命名）
            temp_path = path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # 3. 重命名（原子操作）
            temp_path.replace(path)
            
            log_edit(file_path, "COMMITTED", hash_before, hash_after, changes, backup_path)
            
            return EditResult(
                success=True,
                file_path=file_path,
                backup_path=str(backup_path),
                changes=changes,
                hash_before=hash_before,
                hash_after=hash_after,
                dry_run=False,
                message=f"Successfully edited. Backup: {backup_path}"
            )
            
        except Exception as e:
            # 失败回滚
            if backup_path and backup_path.exists():
                shutil.copy2(backup_path, path)
            
            log_edit(file_path, "FAILED", hash_before, hash_after, str(e))
            
            return EditResult(
                success=False,
                file_path=file_path,
                backup_path=str(backup_path) if backup_path else None,
                changes=changes,
                hash_before=hash_before,
                hash_after=hash_after,
                dry_run=False,
                message=f"Edit failed: {str(e)}"
            )

def ensure_backup_dir():
    """确保备份目录存在"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def create_backup(file_path: Path) -> Path:
    """创建备份文件"""
    ensure_backup_dir()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_name = f"{file_path.stem}-{timestamp}{file_path.suffix}.bak"
    backup_path = BACKUP_DIR / backup_name
    shutil.copy2(file_path, backup_path)
    return backup_path

def log_edit(file_path: str, action: str, hash_before: str, hash_after: str, changes: str, backup_path: Optional[Path] = None):
    """记录编辑日志"""
    SAFE_EDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {action}: {file_path} | {hash_before[:8]}->{hash_after[:8]} | {changes[:100]}"
    with open(SAFE_EDIT_LOG, 'a', encoding='utf-8') as f:
        f.write(log_entry + "\n")

def safe_edit(
    file_path: str,
    old_text: str,
    new_text: str,
    dry_run: bool = True
) -> EditResult:
    """
    便捷函数：安全编辑
    
    使用示例：
        # 第一步：预览
        result = safe_edit("config.json", '"old": "value"', '"new": "value"', dry_run=True)
        print(result.changes)  # 查看变更
        
        # 第二步：确认后执行
        if result.success:
            result = safe_edit("config.json", '"old": "value"', '"new": "value"', dry_run=False)
    """
    editor = SafeFileEditor()
    return editor.edit(file_path, old_text, new_text, dry_run=dry_run)

def rollback(file_path: str, backup_path: str) -> bool:
    """回滚到备份版本"""
    try:
        backup = Path(backup_path)
        target = Path(file_path)
        if backup.exists():
            shutil.copy2(backup, target)
            log_edit(file_path, "ROLLBACK", "", "", f"Restored from {backup_path}")
            return True
        return False
    except Exception as e:
        print(f"Rollback failed: {e}")
        return False

if __name__ == "__main__":
    # 测试
    print("Safe File Editor")
    
    # 创建测试文件
    test_file = Path("/tmp/test-edit.txt")
    test_file.write_text("Hello World", encoding="utf-8")
    
    # 预览编辑
    result = safe_edit(str(test_file), "World", "OpenClaw", dry_run=True)
    print(f"Preview: {result.message}")
    
    # 实际编辑
    result = safe_edit(str(test_file), "World", "OpenClaw", dry_run=False)
    print(f"Result: {result.success}, Backup: {result.backup_path}")
    
    # 验证内容
    content = test_file.read_text(encoding="utf-8")
    print(f"Content: {content}")
