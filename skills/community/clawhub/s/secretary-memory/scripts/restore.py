#!/usr/bin/env python3
"""
OpenClaw 秘书式记忆系统 - 恢复/回溯能力
支持按日期、话题、文件类型精细化恢复

用法:
    python3 restore.py --list                  # 列出所有归档操作历史
    python3 restore.py --date 2026-04-23       # 恢复指定日期的所有归档
    python3 restore.py --topic "项目X"          # 恢复指定话题的所有归档
    python3 restore.py --date 2026-04-23 --dry-run  # 预览恢复
    python3 restore.py --file archive/decisions/xxx.md  # 恢复单个文件
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import argparse

# ============== 配置 ==============
MEMORY_DIR = Path(os.environ.get("OPENCLAW_MEMORY_DIR", "/root/.openclaw/workspace/memory"))
DAILY_DIR = MEMORY_DIR / "daily"
ARCHIVE_DIR = MEMORY_DIR / "archive"
RESTORE_LOG_FILE = ARCHIVE_DIR / ".restore_log.json"


# ============== 恢复管理器 ==============

class RestoreManager:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.restore_log = self.load_restore_log()

    def load_restore_log(self) -> List[Dict]:
        """加载恢复日志"""
        if RESTORE_LOG_FILE.exists():
            try:
                return json.loads(RESTORE_LOG_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return []

    def save_restore_log(self):
        """保存恢复日志"""
        if self.dry_run:
            return
        RESTORE_LOG_FILE.write_text(
            json.dumps(self.restore_log, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def log_operation(self, operation: str, source: str, dest: str, file_type: str):
        """记录操作到日志"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,  # "archive" or "restore"
            "source": source,
            "dest": dest,
            "type": file_type
        }
        self.restore_log.append(entry)
        self.save_restore_log()

    def list_operations(self, limit: int = 50) -> List[Dict]:
        """列出最近的归档/恢复操作"""
        return self.restore_log[-limit:]

    def find_archive_entries_by_date(self, date: str) -> List[Dict]:
        """查找指定日期的归档操作"""
        results = []
        for entry in self.restore_log:
            if entry.get("operation") == "archive":
                # 检查源文件或目标文件是否包含该日期
                source_file = Path(entry.get("source", ""))
                if date in source_file.name or date in entry.get("dest", ""):
                    results.append(entry)
        return results

    def find_archive_entries_by_topic(self, topic: str) -> List[Dict]:
        """查找指定话题的归档操作"""
        results = []
        topic_lower = topic.lower()
        for entry in self.restore_log:
            if entry.get("operation") == "archive":
                source_path = entry.get("source", "").lower()
                dest_path = entry.get("dest", "").lower()
                if topic_lower in source_path or topic_lower in dest_path:
                    results.append(entry)
        return results

    def restore_file(self, source: Path, dest: Path) -> bool:
        """恢复单个文件"""
        if not source.exists():
            print(f"[Warning] 源文件不存在: {source}")
            return False

        if dest.exists():
            print(f"[Warning] 目标文件已存在: {dest}")
            return False

        if self.dry_run:
            print(f"[DRY] 恢复: {source.relative_to(MEMORY_DIR)} -> {dest.relative_to(MEMORY_DIR)}")
            return True

        try:
            # 确保目标目录存在
            dest.parent.mkdir(parents=True, exist_ok=True)
            source.rename(dest)
            print(f"[OK] 已恢复: {dest.relative_to(MEMORY_DIR)}")
            return True
        except Exception as e:
            print(f"[Error] 恢复失败: {e}")
            return False

    def restore_by_date(self, date: str) -> int:
        """恢复指定日期的所有归档文件"""
        entries = self.find_archive_entries_by_date(date)
        if not entries:
            print(f"[Info] 未找到日期 {date} 的归档记录")
            return 0

        print(f"找到 {len(entries)} 条归档记录将恢复:\n")
        count = 0

        for entry in entries:
            source = ARCHIVE_DIR / entry["dest"]
            # 恢复时，source 是 archive 路径，dest 是原始位置
            # 但 restore_log 记录的是 archive 操作：source=原始位置，dest=archive位置
            # 所以恢复时需要反向：source=archive位置，dest=原始位置
            actual_source = ARCHIVE_DIR / entry["dest"]
            actual_dest = MEMORY_DIR / entry["source"]

            if self.restore_file(actual_source, actual_dest):
                # 记录恢复操作
                self.log_operation("restore", entry["dest"], entry["source"], entry.get("type", ""))
                count += 1

        return count

    def restore_by_topic(self, topic: str) -> int:
        """恢复指定话题的所有归档文件"""
        entries = self.find_archive_entries_by_topic(topic)
        if not entries:
            print(f"[Info] 未找到话题「{topic}」的归档记录")
            return 0

        print(f"找到 {len(entries)} 条归档记录将恢复:\n")
        count = 0

        for entry in entries:
            actual_source = ARCHIVE_DIR / entry["dest"]
            actual_dest = MEMORY_DIR / entry["source"]

            if self.restore_file(actual_source, actual_dest):
                self.log_operation("restore", entry["dest"], entry["source"], entry.get("type", ""))
                count += 1

        return count

    def restore_single_file(self, archive_path: str) -> bool:
        """恢复单个归档文件"""
        # archive_path 应该是相对于 ARCHIVE_DIR 的路径
        source = ARCHIVE_DIR / archive_path

        # 查找对应的原始位置
        for entry in self.restore_log:
            if entry.get("operation") == "archive" and entry.get("dest") == archive_path:
                dest = MEMORY_DIR / entry["source"]
                if self.restore_file(source, dest):
                    self.log_operation("restore", archive_path, entry["source"], entry.get("type", ""))
                    return True
                return False

        # 如果在日志中没找到，尝试从路径推断
        # archive/daily/2026-04-23.md -> daily/2026-04-23.md
        if archive_path.startswith("archive/"):
            inferred_dest = MEMORY_DIR / archive_path.replace("archive/", "")
            if self.restore_file(source, inferred_dest):
                self.log_operation("restore", archive_path, inferred_dest.relative_to(MEMORY_DIR), "inferred")
                return True

        print(f"[Error] 无法确定归档文件 {archive_path} 的原始位置")
        return False

    def list_archive_files(self) -> List[Dict]:
        """列出所有已归档的文件"""
        archives = []

        # 扫描 archive 目录
        if ARCHIVE_DIR.exists():
            for archive_type in ["daily", "decisions", "projects"]:
                type_dir = ARCHIVE_DIR / archive_type
                if type_dir.exists():
                    for f in type_dir.rglob("*.md"):
                        rel_path = f.relative_to(ARCHIVE_DIR)
                        # 查找对应的归档时间
                        archive_time = None
                        for entry in reversed(self.restore_log):
                            if entry.get("operation") == "archive" and entry.get("dest") == str(rel_path):
                                archive_time = entry.get("timestamp")
                                break

                        archives.append({
                            "file": str(rel_path),
                            "type": archive_type,
                            "archived_at": archive_time or "unknown",
                            "size": f.stat().st_size if f.exists() else 0
                        })

        return archives

    def format_list(self, operations: List[Dict]) -> str:
        """格式化操作列表"""
        if not operations:
            return "[Info] 暂无归档/恢复记录"

        output = ["## 归档/恢复操作历史\n"]
        output.append(f"共 {len(operations)} 条记录:\n")

        for entry in operations[-20:]:  # 只显示最近20条
            timestamp = entry.get("timestamp", "")[:19]
            op = entry.get("operation", "")
            op_icon = "📦 →" if op == "archive" else "↩️ ←"
            file_type = entry.get("type", "")

            output.append(f"{op_icon} [{timestamp}] {file_type}")
            output.append(f"   {entry.get('source', '')} -> {entry.get('dest', '')}")

        return '\n'.join(output)


# ============== 主程序 ==============

def main():
    parser = argparse.ArgumentParser(description="OpenClaw 秘书式记忆系统 - 恢复")
    parser.add_argument("--list", "-l", action="store_true", help="列出归档操作历史")
    parser.add_argument("--date", "-d", type=str, help="恢复指定日期的归档 (YYYY-MM-DD)")
    parser.add_argument("--topic", "-t", type=str, help="恢复指定话题的归档")
    parser.add_argument("--file", "-f", type=str, help="恢复单个归档文件 (相对于 archive/)")
    parser.add_argument("--dry-run", action="store_true", help="预览恢复，不实际执行")
    parser.add_argument("--archives", action="store_true", help="列出所有已归档的文件")
    args = parser.parse_args()

    manager = RestoreManager(dry_run=args.dry_run)

    # 列出归档操作历史
    if args.list:
        operations = manager.list_operations()
        print(manager.format_list(operations))
        return

    # 列出所有已归档文件
    if args.archives:
        archives = manager.list_archive_files()
        if not archives:
            print("[Info] 暂无归档文件")
            return
        print(f"## 已归档文件 ({len(archives)} 个)\n")
        for a in archives[:30]:
            print(f"- [{a['type']}] {a['file']} (归档于 {a['archived_at'][:10]})")
        if len(archives) > 30:
            print(f"\n... 还有 {len(archives) - 30} 个文件")
        return

    # 恢复操作
    count = 0
    if args.date:
        count = manager.restore_by_date(args.date)
    elif args.topic:
        count = manager.restore_by_topic(args.topic)
    elif args.file:
        if manager.restore_single_file(args.file):
            count = 1
    else:
        parser.print_help()
        print("\n[Error] 请指定 --date, --topic, 或 --file 参数")
        return

    if not args.dry_run and count > 0:
        print(f"\n[OK] 恢复了 {count} 个文件")
    elif args.dry_run and count > 0:
        print(f"\n[DRY RUN] 将恢复 {count} 个文件")


if __name__ == "__main__":
    main()
