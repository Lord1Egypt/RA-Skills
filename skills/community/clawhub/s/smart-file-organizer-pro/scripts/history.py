#!/usr/bin/env python3
"""
操作历史管理脚本
查看和管理整理操作历史记录
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

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


class HistoryManager:
    """操作历史管理器"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path).resolve()
        self.history_dir = self.base_path / ".history"

    def list_operations(self) -> List[Dict]:
        """列出所有历史操作"""
        if not self.history_dir.exists():
            print(f"{Colors.WARNING}未找到历史记录{Colors.ENDC}")
            return []

        operations = []
        for history_file in sorted(self.history_dir.glob("organize_*.json"), reverse=True):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    operations.append({
                        'file': history_file,
                        'data': data
                    })
            except Exception as e:
                print(f"{Colors.FAIL}读取历史文件失败 {history_file}: {e}{Colors.ENDC}")

        return operations

    def display_operations(self, operations: List[Dict]):
        """显示操作列表"""
        if not operations:
            return

        print(f"\n{Colors.BOLD}{Colors.HEADER}{'━' * 60}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}  操作历史记录{Colors.ENDC}")
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

            # 获取操作ID
            op_id = op['file'].stem.replace('organize_', '')

            print(f"{Colors.OKCYAN}[{idx}] 操作ID: {op_id}{Colors.ENDC}")
            print(f"     时间: {time_str}")
            print(f"     模式: {mode.upper()}")
            print(f"     统计: 整理 {stats.get('organized_files', 0)} | "
                  f"重命名 {stats.get('renamed_files', 0)} | "
                  f"发现重复 {stats.get('duplicates_found', 0)}")
            print(f"     错误: {stats.get('errors', 0)}")
            print()

    def show_operation_detail(self, operation_id: str):
        """显示操作详情"""
        history_file = self.history_dir / f"organize_{operation_id}.json"

        if not history_file.exists():
            print(f"{Colors.FAIL}未找到操作记录: {operation_id}{Colors.ENDC}")
            return

        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            print(f"\n{Colors.BOLD}{Colors.HEADER}{'━' * 60}{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.HEADER}  操作详情: {operation_id}{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.HEADER}{'━' * 60}{Colors.ENDC}\n")

            # 基本信息
            print(f"{Colors.OKCYAN}基本信息:{Colors.ENDC}")
            print(f"  时间: {data.get('timestamp', 'N/A')}")
            print(f"  模式: {data.get('mode', 'unknown').upper()}")
            print()

            # 配置信息
            config = data.get('config', {})
            print(f"{Colors.OKCYAN}配置:{Colors.ENDC}")
            print(f"  重命名: {'是' if config.get('rename') else '否'}")
            print(f"  去重: {'是' if config.get('deduplicate') else '否'}")
            print()

            # 统计信息
            stats = data.get('stats', {})
            print(f"{Colors.OKCYAN}统计:{Colors.ENDC}")
            for key, value in stats.items():
                if key not in ['start_time', 'end_time', 'log']:
                    print(f"  {key}: {value}")
            print()

            # 操作日志
            log = data.get('log', [])
            if log:
                print(f"{Colors.OKCYAN}操作日志 (最近20条):{Colors.ENDC}")
                for entry in log[-20:]:
                    print(f"  {entry}")

        except Exception as e:
            print(f"{Colors.FAIL}读取操作详情失败: {e}{Colors.ENDC}")

    def get_operation_by_index(self, index: int, operations: List[Dict]) -> Dict:
        """根据索引获取操作"""
        if 1 <= index <= len(operations):
            return operations[index - 1]
        return None


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="操作历史管理 - 查看和管理整理操作历史",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  查看历史:     python3 history.py --list
  查看详情:     python3 history.py --show 20240312_153000
  按索引查看:   python3 history.py --index 1
        """
    )

    parser.add_argument("--path", default=".", help="基础路径（默认：当前目录）")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有历史操作")
    parser.add_argument("--show", "-s", metavar="ID", help="显示指定操作的详情")
    parser.add_argument("--index", "-i", type=int, metavar="N", help="按索引显示操作详情")
    parser.add_argument("--export", "-e", metavar="FILE", help="导出历史到文件")

    args = parser.parse_args()

    manager = HistoryManager(args.path)

    # 列出所有操作
    if args.list:
        operations = manager.list_operations()
        manager.display_operations(operations)
        return

    # 显示指定操作详情
    if args.show:
        manager.show_operation_detail(args.show)
        return

    # 按索引显示
    if args.index:
        operations = manager.list_operations()
        op = manager.get_operation_by_index(args.index, operations)
        if op:
            op_id = op['file'].stem.replace('organize_', '')
            manager.show_operation_detail(op_id)
        else:
            print(f"{Colors.FAIL}无效的索引: {args.index}{Colors.ENDC}")
        return

    # 导出历史
    if args.export:
        operations = manager.list_operations()
        export_data = [op['data'] for op in operations]

        try:
            with open(args.export, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            print(f"{Colors.OKGREEN}历史已导出到: {args.export}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}导出失败: {e}{Colors.ENDC}")
        return

    # 默认显示列表
    operations = manager.list_operations()
    manager.display_operations(operations)


if __name__ == "__main__":
    main()
