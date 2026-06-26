#!/usr/bin/env python3
"""
撤销操作脚本
撤销之前的文件整理操作
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

# ANSI 颜色代码
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

    @staticmethod
    def disable():
        Colors.HEADER = ''
        Colors.OKBLUE = ''
        Colors.OKCYAN = ''
        Colors.OKGREEN = ''
        Colors.WARNING = ''
        Colors.FAIL = ''
        Colors.ENDC = ''
        Colors.BOLD = ''

if not sys.stdout.isatty() or os.name == 'nt':
    Colors.disable()


class UndoManager:
    """撤销操作管理器"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path).resolve()
        self.history_dir = self.base_path / ".history"
        self.backup_dir = self.base_path / "Backup"

    def list_operations(self):
        """列出可撤销的操作"""
        if not self.history_dir.exists():
            print(f"{Colors.WARNING}未找到历史记录{Colors.ENDC}")
            return []

        operations = []
        for history_file in sorted(self.history_dir.glob("organize_*.json"), reverse=True):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    operations.append({
                        'id': history_file.stem.replace('organize_', ''),
                        'file': history_file,
                        'data': data
                    })
            except Exception as e:
                print(f"{Colors.FAIL}读取历史文件失败 {history_file}: {e}{Colors.ENDC}")

        return operations

    def display_operations(self, operations):
        """显示可撤销的操作列表"""
        if not operations:
            print(f"{Colors.WARNING}没有可撤销的操作{Colors.ENDC}")
            return

        print(f"\n{Colors.BOLD}{Colors.HEADER}{'━' * 60}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}  可撤销的操作{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'━' * 60}{Colors.ENDC}\n")

        for idx, op in enumerate(operations, 1):
            data = op['data']
            timestamp = data.get('timestamp', 'N/A')
            mode = data.get('mode', 'unknown')
            stats = data.get('stats', {})

            # 格式化时间
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                time_str = timestamp

            print(f"{Colors.OKCYAN}[{idx}] 操作ID: {op['id']}{Colors.ENDC}")
            print(f"     时间: {time_str}")
            print(f"     模式: {mode.upper()}")
            print(f"     已整理: {stats.get('organized_files', 0)} 个文件")
            print(f"     已重命名: {stats.get('renamed_files', 0)} 个文件")
            print()

    def undo_operation(self, operation_id: str, preview: bool = True) -> bool:
        """撤销指定操作"""
        history_file = self.history_dir / f"organize_{operation_id}.json"

        if not history_file.exists():
            print(f"{Colors.FAIL}未找到操作记录: {operation_id}{Colors.ENDC}")
            return False

        # 检查备份目录
        if not self.backup_dir.exists():
            print(f"{Colors.FAIL}未找到备份目录，无法撤销{Colors.ENDC}")
            return False

        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            print(f"\n{Colors.BOLD}{Colors.HEADER}{'━' * 60}{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.HEADER}  撤销操作: {operation_id}{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.HEADER}{'━' * 60}{Colors.ENDC}\n")

            print(f"{Colors.OKCYAN}操作信息:{Colors.ENDC}")
            print(f"  时间: {data.get('timestamp', 'N/A')}")
            print(f"  模式: {data.get('mode', 'unknown').upper()}")
            print(f"  已整理: {data.get('stats', {}).get('organized_files', 0)} 个文件")
            print()

            # 统计备份文件
            backup_files = list(self.backup_dir.glob("*"))
            backup_files = [f for f in backup_files if f.is_file()]

            if not backup_files:
                print(f"{Colors.WARNING}备份目录为空，无需恢复{Colors.ENDC}")
                return True

            print(f"{Colors.OKCYAN}找到 {len(backup_files)} 个备份文件{Colors.ENDC}")
            print(f"{Colors.OKCYAN}备份目录: {self.backup_dir}{Colors.ENDC}")
            print()

            if preview:
                print(f"{Colors.WARNING}预览模式 - 以下是将要恢复的文件:{Colors.ENDC}")
                for backup_file in backup_files[:10]:  # 只显示前10个
                    print(f"  • {backup_file.name}")
                if len(backup_files) > 10:
                    print(f"  ... 还有 {len(backup_files) - 10} 个文件")
                print()
                print(f"{Colors.WARNING}要实际恢复文件，请使用 --confirm 参数{Colors.ENDC}")
                return True

            # 确认操作
            if not preview:
                confirm = input(f"{Colors.WARNING}确认要恢复备份文件？这将覆盖当前文件 (yes/no): {Colors.ENDC}")
                if confirm.lower() not in ['yes', 'y']:
                    print(f"{Colors.WARNING}操作已取消{Colors.ENDC}")
                    return False

            # 执行恢复
            print(f"{Colors.OKCYAN}正在恢复文件...{Colors.ENDC}")

            restored = 0
            errors = 0

            for backup_file in backup_files:
                try:
                    target_path = self.base_path / backup_file.name

                    # 处理文件名冲突
                    if target_path.exists():
                        counter = 1
                        stem = backup_file.stem
                        while target_path.exists():
                            target_path = self.base_path / f"{stem}_restored{counter}{backup_file.suffix}"
                            counter += 1

                    shutil.copy2(backup_file, target_path)
                    restored += 1
                    print(f"  {Colors.OKGREEN}✓{Colors.ENDC} {backup_file.name}")

                except Exception as e:
                    errors += 1
                    print(f"  {Colors.FAIL}✗{Colors.ENDC} {backup_file.name}: {e}")

            print()
            print(f"{Colors.OKGREEN}恢复完成{Colors.ENDC}")
            print(f"  成功: {restored} 个文件")
            print(f"  失败: {errors} 个文件")

            # 询问是否删除备份
            if errors == 0:
                delete_backup = input(f"\n{Colors.WARNING}恢复成功，是否删除备份？(yes/no): {Colors.ENDC}")
                if delete_backup.lower() in ['yes', 'y']:
                    shutil.rmtree(self.backup_dir)
                    print(f"{Colors.OKGREEN}备份已删除{Colors.ENDC}")

            return True

        except Exception as e:
            print(f"{Colors.FAIL}撤销操作失败: {e}{Colors.ENDC}")
            return False

    def undo_last_operation(self, preview: bool = True) -> bool:
        """撤销最后一次操作"""
        operations = self.list_operations()

        if not operations:
            print(f"{Colors.WARNING}没有可撤销的操作{Colors.ENDC}")
            return False

        last_operation = operations[0]
        return self.undo_operation(last_operation['id'], preview)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="撤销操作 - 撤销之前的文件整理操作",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  查看可撤销操作: python3 undo.py --list
  撤销最后一次:   python3 undo.py --last
  撤销指定操作:   python3 undo.py --id 20240312_153000
  预览撤销:       python3 undo.py --last --preview
  确认撤销:       python3 undo.py --last --confirm
        """
    )

    parser.add_argument("--path", default=".", help="基础路径（默认：当前目录）")
    parser.add_argument("--list", "-l", action="store_true", help="列出可撤销的操作")
    parser.add_argument("--last", action="store_true", help="撤销最后一次操作")
    parser.add_argument("--id", metavar="ID", help="撤销指定ID的操作")
    parser.add_argument("--preview", "-p", action="store_true",
                       help="预览模式（默认启用，使用 --confirm 实际执行）")
    parser.add_argument("--confirm", "-c", action="store_true",
                       help="确认执行撤销操作")

    args = parser.parse_args()

    manager = UndoManager(args.path)

    # 列出可撤销操作
    if args.list:
        operations = manager.list_operations()
        manager.display_operations(operations)
        return

    # 撤销最后一次操作
    if args.last:
        preview = not args.confirm
        manager.undo_last_operation(preview=preview)
        return

    # 撤销指定操作
    if args.id:
        preview = not args.confirm
        manager.undo_operation(args.id, preview=preview)
        return

    # 默认显示列表
    operations = manager.list_operations()
    manager.display_operations(operations)


if __name__ == "__main__":
    main()
