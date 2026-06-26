#!/usr/bin/env python3
"""
龙虾记忆系统 - 记忆清理脚本
清理过期的中期记忆文件
"""

import argparse
import json
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path


def find_expired_files(memory_dir: str, retention_days: int = 30) -> list:
    """查找过期的记忆文件"""
    memory_path = Path(memory_dir)
    if not memory_path.exists():
        return []
    
    cutoff = datetime.now() - timedelta(days=retention_days)
    files = []
    
    for f in memory_path.glob("*.md"):
        # 从文件名提取日期 YYYY-MM-DD.md
        import re
        match = re.match(r"(\d{4}-\d{2}-\d{2})\.md", f.name)
        if match:
            file_date = datetime.strptime(match.group(1), "%Y-%m-%d")
            if file_date < cutoff:
                files.append((f, file_date))
    
    return sorted(files, key=lambda x: x[1])


def archive_file(file_path: Path, archive_dir: Path) -> bool:
    """归档文件到 archive 目录"""
    if not archive_dir.exists():
        archive_dir.mkdir(parents=True)
    
    archive_path = archive_dir / file_path.name
    shutil.move(str(file_path), str(archive_path))
    return True


def delete_file(file_path: Path) -> bool:
    """删除文件"""
    file_path.unlink()
    return True


def has_important_content(file_path: Path) -> bool:
    """检查文件是否包含重要内容"""
    content = file_path.read_text(encoding="utf-8")
    important_markers = ["#重要", "#决策", "#错误", "[已升级"]
    return any(marker in content for marker in important_markers)


def update_heartbeat_state(state_path: Path, stats: dict):
    """更新心跳状态"""
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
    else:
        state = {"lastChecks": {}, "stats": {}}
    
    state["lastChecks"]["expiredCleanup"] = datetime.now().isoformat()
    state["stats"]["cleanedThisMonth"] = state["stats"].get("cleanedThisMonth", 0) + stats.get("cleaned", 0)
    state["stats"]["archivedThisMonth"] = state["stats"].get("archivedThisMonth", 0) + stats.get("archived", 0)
    
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="清理过期的中期记忆")
    parser.add_argument("--workspace", default="~/.openclaw/workspace", help="工作空间路径")
    parser.add_argument("--retention", type=int, default=30, help="保留天数")
    parser.add_argument("--action", choices=["archive", "delete", "auto"], default="auto", help="处理方式")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不执行")
    args = parser.parse_args()
    
    workspace = Path(args.workspace).expanduser()
    memory_dir = workspace / "memory"
    archive_dir = memory_dir / "archive"
    state_path = memory_dir / "heartbeat-state.json"
    
    print(f"🔍 扫描超过 {args.retention} 天的记忆文件...")
    expired_files = find_expired_files(memory_dir, args.retention)
    
    if not expired_files:
        print("✅ 没有过期的记忆文件")
        return
    
    print(f"   找到 {len(expired_files)} 个过期文件:\n")
    
    to_archive = []
    to_delete = []
    
    for f, date in expired_files:
        age = (datetime.now() - date).days
        important = has_important_content(f)
        
        if args.action == "auto":
            action = "archive" if important else "delete"
        else:
            action = args.action
        
        status = "📦 归档" if action == "archive" else "🗑️ 删除"
        important_mark = " ⚠️含重要内容" if important else ""
        
        print(f"   {status} {f.name} ({age}天前){important_mark}")
        
        if action == "archive":
            to_archive.append(f)
        else:
            to_delete.append(f)
    
    if args.dry_run:
        print(f"\n[DRY RUN] 预览完成: {len(to_archive)} 归档, {len(to_delete)} 删除")
        return
    
    print("\n🚀 执行清理...")
    
    stats = {"archived": 0, "cleaned": 0}
    
    for f in to_archive:
        if archive_file(f, archive_dir):
            print(f"   📦 已归档: {f.name}")
            stats["archived"] += 1
    
    for f in to_delete:
        if delete_file(f):
            print(f"   🗑️ 已删除: {f.name}")
            stats["cleaned"] += 1
    
    # 更新心跳状态
    update_heartbeat_state(state_path, stats)
    
    print(f"\n✅ 清理完成: {stats['archived']} 归档, {stats['cleaned']} 删除")


if __name__ == "__main__":
    main()
