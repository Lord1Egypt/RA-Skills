#!/usr/bin/env python3
"""
SQL 文件拆分工具 - 多数据库方言支持
支持 MySQL, PostgreSQL, Oracle, SQL Server, 达梦(DM) 等数据库

v2.2 新功能:
- 添加 GUI 界面 (gui.py)
- 添加断点续传功能 (checkpoint.py)
- 添加批量并行处理 (batch_processor.py)
- 添加结果预览和对比 (result_previewer.py)
- 添加配置文件管理 (config_manager.py)

v2.1 新功能:
- 集成详细错误处理和修复建议
- 添加进度条显示（支持 tqdm）
- 支持 dry-run 预览模式
- 返回结构化的 SplitResult 对象

v2.0 重写要点:
"""

import sys
import argparse
from pathlib import Path

# 导入核心模块
from split_sql_v21 import split_sql_file, SQLDialect
from error_handler import SplitResult

# 导入新功能模块
from gui import SQLSplitterGUI
from checkpoint import CheckpointManager
from batch_processor import BatchProcessor
from result_previewer import ResultPreviewer
from config_manager import ConfigManager, SplitConfig

import tkinter as tk


def run_gui():
    """运行 GUI 模式"""
    root = tk.Tk()
    app = SQLSplitterGUI(root)
    root.mainloop()


def run_batch(args):
    """运行批量处理模式"""
    processor = BatchProcessor(
        max_workers=args.max_workers,
        use_checkpoint=not args.no_checkpoint
    )

    # 设置进度回调
    def progress_callback(completed, total, message):
        print(f"[{completed}/{total}] {message}")

    processor.set_progress_callback(progress_callback)

    # 处理目录
    if args.directory:
        result = processor.process_directory(
            input_dir=args.input,
            output_base_dir=args.output,
            pattern=args.pattern,
            dialect=SQLDialect[args.dialect.upper()] if args.dialect != "auto" else None,
            options={
                'verbose': args.verbose,
                'dry_run': args.dry_run,
                'show_progress': not args.no_progress,
                'no_merge': args.no_merge
            }
        )
    else:
        # 处理单个文件
        files = [{'input_file': args.input, 'output_dir': args.output}]
        result = processor.process_files(
            files=files,
            output_base_dir=args.output,
            dialect=SQLDialect[args.dialect.upper()] if args.dialect != "auto" else None,
            options={
                'verbose': args.verbose,
                'dry_run': args.dry_run,
                'show_progress': not args.no_progress,
                'no_merge': args.no_merge
            }
        )

    print(result.get_summary())


def run_preview(args):
    """运行预览模式"""
    previewer = ResultPreviewer()

    try:
        preview = previewer.preview_split_result(
            original_file=args.input,
            output_dir=args.output
        )

        if args.table:
            print(previewer.generate_summary_table(preview))
        else:
            print(previewer.format_preview(preview))

        if args.compare:
            print("\n与原始文件对比:")
            print(previewer.compare_with_original(args.input, args.output))

    except Exception as e:
        print(f"预览失败: {e}")
        sys.exit(1)


def run_checkpoint(args):
    """运行检查点管理"""
    manager = CheckpointManager()

    if args.list:
        print("检查点列表:")
        for cp in manager.list_checkpoints():
            print(f"  {cp['input_file']}: {cp['progress']} ({cp['status']})")

    elif args.resume:
        resume_info = manager.get_resume_progress(args.input)
        if resume_info:
            print(f"恢复进度: {resume_info['progress']:.1%}")
            print(f"可以恢复: {resume_info['can_resume']}")
            print(f"状态: {resume_info['status']}")
        else:
            print("未找到检查点")

    elif args.clear:
        deleted = manager.clear_old_checkpoints(days=args.days)
        print(f"已删除 {deleted} 个旧检查点")

    elif args.delete:
        if manager.delete_checkpoint(args.input):
            print(f"已删除检查点: {args.input}")
        else:
            print(f"删除检查点失败: {args.input}")


def run_config(args):
    """运行配置管理"""
    manager = ConfigManager()

    if args.list:
        print("配置列表:")
        for cfg in manager.list_configs():
            print(f"  {cfg['name']}: {cfg['dialect']}")

    elif args.save:
        config = SplitConfig(
            dialect=args.dialect,
            output_dir=args.output,
            verbose=args.verbose,
            dry_run=args.dry_run,
            no_merge=args.no_merge,
            show_progress=not args.no_progress,
            max_workers=args.max_workers,
            use_checkpoint=not args.no_checkpoint
        )
        if manager.save_config(config, args.name):
            print(f"配置已保存: {args.name}")
        else:
            print("保存配置失败")
            sys.exit(1)

    elif args.load:
        config = manager.load_config(args.name)
        if config:
            print(f"配置: {args.name}")
            print(f"  方言: {config.dialect}")
            print(f"  输出目录: {config.output_dir}")
            print(f"  最大并发: {config.max_workers}")
            print(f"  使用检查点: {config.use_checkpoint}")
        else:
            print(f"配置不存在: {args.name}")
            sys.exit(1)

    elif args.delete:
        if manager.delete_config(args.name):
            print(f"已删除配置: {args.name}")
        else:
            print(f"删除配置失败: {args.name}")

    elif args.export:
        if manager.export_config(args.name, args.export_path, args.format):
            print(f"配置已导出: {args.export_path}")
        else:
            print("导出配置失败")
            sys.exit(1)

    elif args.import_config:
        if manager.import_config(args.import_path, args.name):
            print(f"配置已导入: {args.name}")
        else:
            print("导入配置失败")
            sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="SQL 文件拆分工具 v2.2 - 支持多数据库方言",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本拆分
  python3 split_sql_v22.py input.sql output_dir

  # 指定方言
  python3 split_sql_v22.py input.sql output_dir --dialect oracle

  # GUI 模式
  python3 split_sql_v22.py --gui

  # 批量处理
  python3 split_sql_v22.py --batch input_dir output_dir

  # 预览结果
  python3 split_sql_v22.py --preview input.sql output_dir

  # 检查点管理
  python3 split_sql_v22.py --checkpoint --list

  # 配置管理
  python3 split_sql_v22.py --config --list
        """
    )

    # 模式选择
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--gui', action='store_true', help='GUI 模式')
    mode_group.add_argument('--batch', action='store_true', help='批量处理模式')
    mode_group.add_argument('--preview', action='store_true', help='预览模式')
    mode_group.add_argument('--checkpoint', action='store_true', help='检查点管理')
    mode_group.add_argument('--config', action='store_true', help='配置管理')

    # 基本参数
    parser.add_argument('input', nargs='?', help='输入文件或目录')
    parser.add_argument('output', nargs='?', help='输出目录')

    # 拆分参数
    parser.add_argument('--dialect', default='auto',
                       choices=['auto', 'mysql', 'postgresql', 'oracle', 'sqlserver', 'dm', 'generic'],
                       help='SQL 方言 (默认: auto)')
    parser.add_argument('-q', '--quiet', action='store_true', help='静默模式')
    parser.add_argument('--dry-run', action='store_true', help='预览模式，不实际创建文件')
    parser.add_argument('--no-merge', action='store_true', help='不生成合并脚本')
    parser.add_argument('--no-progress', action='store_true', help='不显示进度条')

    # 批量处理参数
    parser.add_argument('--directory', action='store_true', help='处理整个目录')
    parser.add_argument('--pattern', default='*.sql', help='文件匹配模式 (默认: *.sql)')
    parser.add_argument('--max-workers', type=int, default=4, help='最大并发数 (默认: 4)')
    parser.add_argument('--no-checkpoint', action='store_true', help='不使用断点续传')

    # 预览参数
    parser.add_argument('--table', action='store_true', help='以表格形式显示')
    parser.add_argument('--compare', action='store_true', help='与原始文件对比')

    # 检查点参数
    parser.add_argument('--list', action='store_true', help='列出所有检查点')
    parser.add_argument('--resume', action='store_true', help='显示恢复进度')
    parser.add_argument('--clear', action='store_true', help='清理旧检查点')
    parser.add_argument('--delete', action='store_true', help='删除检查点')
    parser.add_argument('--days', type=int, default=7, help='保留天数 (默认: 7)')

    # 配置参数
    parser.add_argument('--name', default='default', help='配置名称 (默认: default)')
    parser.add_argument('--save', action='store_true', help='保存配置')
    parser.add_argument('--load', action='store_true', help='加载配置')
    parser.add_argument('--export-path', help='导出路径')
    parser.add_argument('--format', default='json', choices=['json', 'yaml'], help='导出格式')
    parser.add_argument('--import-path', help='导入路径')
    parser.add_argument('--import-config', action='store_true', help='导入配置')

    args = parser.parse_args()

    # 社区版付费功能提示
    PRO_MSG = "⚠️ 此功能需要专业版 (¥299/月)，访问 https://sqlsplitter.com"

    # 根据模式执行
    if args.gui:
        print(PRO_MSG); sys.exit(1)
    elif args.batch:
        print(PRO_MSG); sys.exit(1)
    elif args.preview:
        print(PRO_MSG); sys.exit(1)
    elif args.checkpoint:
        print(PRO_MSG); sys.exit(1)
    elif args.config:
        print(PRO_MSG); sys.exit(1)
    else:
        # 默认模式：基本拆分
        if not args.input or not args.output:
            parser.error("需要 input 和 output 参数，或使用 --gui/--batch/--preview/--checkpoint/--config 模式")

        result = split_sql_file(
            args.input,
            args.output,
            dialect=SQLDialect[args.dialect.upper()] if args.dialect != "auto" else None,
            verbose=not args.quiet,
            dry_run=args.dry_run,
            show_progress=not args.no_progress,
            no_merge=args.no_merge
        )

        if result.success:
            print(f"拆分完成! 共 {result.total} 个文件")
            if result.stats:
                print("统计:")
                for obj_type, count in sorted(result.stats.items()):
                    print(f"  {obj_type}: {count}")
            sys.exit(0)
        else:
            print("拆分失败:")
            for error in result.errors:
                print(f"  - {error}")
            sys.exit(1)


if __name__ == "__main__":
    main()