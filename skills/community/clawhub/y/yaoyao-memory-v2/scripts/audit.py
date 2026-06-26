#!/usr/bin/env python3
"""审计日志 - 记录记忆系统操作"""
import json
import os
from datetime import datetime
from pathlib import Path

AUDIT_LOG = Path.home() / ".openclaw" / "workspace" / "memory" / "audit.log"

def log(action: str, detail: str, category: str = "memory"):
    """记录审计日志"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "category": category,
        "detail": detail
    }
    
    # 确保目录存在
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    
    # 追加写入
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def get_logs(limit: int = 50, category: str = None):
    """获取最近的审计日志"""
    if not AUDIT_LOG.exists():
        return []
    
    logs = []
    with open(AUDIT_LOG, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                if category is None or entry.get("category") == category:
                    logs.append(entry)
            except:
                continue
    
    return logs[-limit:]

def show_stats():
    """显示审计统计"""
    logs = get_logs(limit=1000)
    
    stats = {
        "total": len(logs),
        "by_action": {},
        "by_category": {}
    }
    
    for log in logs:
        action = log.get("action", "unknown")
        category = log.get("category", "unknown")
        stats["by_action"][action] = stats["by_action"].get(action, 0) + 1
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
    
    return stats

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "stats":
            stats = show_stats()
            print(f"审计统计（共 {stats['total']} 条记录）：")
            print("\n按操作：")
            for action, count in sorted(stats["by_action"].items()):
                print(f"  {action}: {count}")
            print("\n按类别：")
            for category, count in sorted(stats["by_category"].items()):
                print(f"  {category}: {count}")
        elif sys.argv[1] == "recent":
            logs = get_logs(limit=10)
            print("最近操作：")
            for log in reversed(logs):
                print(f"  [{log['timestamp']}] {log['action']} - {log['detail']}")
        elif sys.argv[1] == "clear":
            if AUDIT_LOG.exists():
                AUDIT_LOG.unlink()
                print("审计日志已清除")
            else:
                print("没有审计日志")
    else:
        print("用法：audit.py [stats|recent|clear]")
