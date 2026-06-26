#!/usr/bin/env python3
"""
Zettelkasten Undo Manager - 撤销管理器
记录操作历史，支持撤销最近的操作
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# 配置 - 支持环境变量覆盖
CARDS_DIR = Path(os.environ.get("ZETTELKASTEN_CARDS_DIR", "~/Desktop/cardsdata")).expanduser()
SYSTEM_DIR = CARDS_DIR / ".system"
HISTORY_FILE = SYSTEM_DIR / "operation_history.json"
TRASH_DIR = SYSTEM_DIR / "trash"

def ensure_system_dir():
    """确保系统目录存在"""
    SYSTEM_DIR.mkdir(parents=True, exist_ok=True)
    TRASH_DIR.mkdir(parents=True, exist_ok=True)

def load_history() -> List[Dict[str, Any]]:
    """加载操作历史"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history: List[Dict[str, Any]]):
    """保存操作历史"""
    ensure_system_dir()
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def log_operation(op_type: str, details: Dict[str, Any]) -> str:
    """
    记录操作
    
    Args:
        op_type: 操作类型 (create/delete/update/batch_delete)
        details: 操作详情
    
    Returns:
        操作ID
    """
    history = load_history()
    
    op_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    operation = {
        "id": op_id,
        "type": op_type,
        "timestamp": datetime.now().isoformat(),
        "details": details
    }
    
    history.append(operation)
    
    # 只保留最近100条记录
    if len(history) > 100:
        history = history[-100:]
    
    save_history(history)
    return op_id

def undo_last_operation() -> Optional[Dict[str, Any]]:
    """
    撤销最后一次操作
    
    Returns:
        撤销结果
    """
    history = load_history()
    
    if not history:
        return None
    
    # 找到最后一条可撤销的操作
    for i in range(len(history) - 1, -1, -1):
        op = history[i]
        if not op.get("undone", False):
            result = undo_operation(op)
            if result:
                # 标记为已撤销
                history[i]["undone"] = True
                history[i]["undone_at"] = datetime.now().isoformat()
                save_history(history)
                return result
    
    return None

def undo_operation(op: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    执行具体的撤销操作
    
    Args:
        op: 操作记录
    
    Returns:
        撤销结果
    """
    op_type = op.get("type")
    details = op.get("details", {})
    
    if op_type == "create":
        # 撤销创建：删除文件
        file_path = Path(details.get("path", ""))
        if file_path.exists():
            # 移到回收站
            trash_path = TRASH_DIR / file_path.name
            shutil.move(str(file_path), str(trash_path))
            return {
                "success": True,
                "action": "delete",
                "file": str(file_path),
                "message": f"已删除创建的卡片: {details.get('title', '')}"
            }
    
    elif op_type == "delete":
        # 撤销删除：恢复文件
        original_path = Path(details.get("original_path", ""))
        trash_path = Path(details.get("trash_path", ""))
        
        if trash_path.exists():
            original_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(trash_path), str(original_path))
            return {
                "success": True,
                "action": "restore",
                "file": str(original_path),
                "message": f"已恢复删除的卡片: {details.get('title', '')}"
            }
    
    elif op_type == "batch_delete":
        # 撤销批量删除：恢复所有文件
        restored = []
        failed = []
        
        for item in details.get("items", []):
            original_path = Path(item.get("original_path", ""))
            trash_path = Path(item.get("trash_path", ""))
            
            if trash_path.exists():
                try:
                    original_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(trash_path), str(original_path))
                    restored.append(str(original_path))
                except Exception as e:
                    failed.append({"file": str(trash_path), "error": str(e)})
        
        return {
            "success": True,
            "action": "batch_restore",
            "restored_count": len(restored),
            "failed": failed,
            "message": f"已恢复 {len(restored)} 个卡片"
        }
    
    elif op_type == "update":
        # 撤销更新：恢复原始内容
        file_path = Path(details.get("path", ""))
        backup_content = details.get("backup_content", "")
        
        if file_path.exists() and backup_content:
            # 保存当前内容到备份
            current_content = file_path.read_text(encoding='utf-8')
            
            # 恢复原始内容
            file_path.write_text(backup_content, encoding='utf-8')
            
            return {
                "success": True,
                "action": "restore_content",
                "file": str(file_path),
                "message": f"已恢复更新前的内容: {details.get('title', '')}"
            }
    
    return None

def list_recent_operations(limit: int = 10) -> List[Dict[str, Any]]:
    """列出最近的操作"""
    history = load_history()
    return history[-limit:][::-1]  # 倒序，最新的在前

def clear_history():
    """清空历史记录"""
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()
    return {"success": True, "message": "操作历史已清空"}

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Zettelkasten 撤销管理器")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # undo 命令
    undo_parser = subparsers.add_parser("undo", help="撤销最后一次操作")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出最近的操作")
    list_parser.add_argument("--limit", "-n", type=int, default=10, help="数量限制")
    
    # clear 命令
    clear_parser = subparsers.add_parser("clear", help="清空操作历史")
    
    # log 命令（内部使用）
    log_parser = subparsers.add_parser("log", help="记录操作（内部使用）")
    log_parser.add_argument("type", help="操作类型")
    log_parser.add_argument("--details", "-d", help="操作详情(JSON)")
    
    args = parser.parse_args()
    
    if args.command == "undo":
        result = undo_last_operation()
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"success": False, "message": "没有可撤销的操作"}, ensure_ascii=False))
    
    elif args.command == "list":
        operations = list_recent_operations(args.limit)
        print(json.dumps(operations, ensure_ascii=False, indent=2))
    
    elif args.command == "clear":
        result = clear_history()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "log":
        details = json.loads(args.details) if args.details else {}
        op_id = log_operation(args.type, details)
        print(json.dumps({"success": True, "op_id": op_id}, ensure_ascii=False))
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
