#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Learning Manager CLI - 学习记录管理命令行工具

提供便捷的命令行接口来管理学习记录。
"""

import argparse
import sys
from pathlib import Path

# 导入学习管理器
from learning_manager import LearningManager, LearningEntry


def cmd_init(args):
    """初始化学习记录目录"""
    workspace = Path(args.workspace).resolve()
    manager = LearningManager(workspace)
    manager.ensure_dirs()
    print(f"✅ 学习记录目录已初始化：{manager.learnings_dir}")
    print(f"   - {manager.learnings_file}")
    print(f"   - {manager.errors_file}")
    print(f"   - {manager.features_file}")


def cmd_add_learning(args):
    """添加学习记录"""
    workspace = Path(args.workspace).resolve()
    manager = LearningManager(workspace)
    manager.ensure_dirs()
    
    entry_id = manager.add_learning(
        category=args.category,
        summary=args.summary,
        details=args.details or '',
        priority=args.priority,
        area=args.area,
        source=args.source,
        related_files=args.files or [],
        pattern_key=args.pattern_key
    )
    
    print(f"✅ 学习记录已添加：{entry_id}")
    print(f"   分类：{args.category}")
    print(f"   优先级：{args.priority}")
    print(f"   文件：{manager.learnings_file}")


def cmd_add_error(args):
    """添加错误记录"""
    workspace = Path(args.workspace).resolve()
    manager = LearningManager(workspace)
    manager.ensure_dirs()
    
    entry_id = manager.add_error(
        command=args.command,
        error_msg=args.error,
        context=args.context or '',
        priority=args.priority,
        area=args.area,
        reproducible=args.reproducible
    )
    
    print(f"✅ 错误记录已添加：{entry_id}")
    print(f"   命令：{args.command}")
    print(f"   优先级：{args.priority}")
    print(f"   文件：{manager.errors_file}")


def cmd_add_feature(args):
    """添加功能请求"""
    workspace = Path(args.workspace).resolve()
    manager = LearningManager(workspace)
    manager.ensure_dirs()
    
    entry_id = manager.add_feature_request(
        capability=args.capability,
        user_context=args.context or '',
        complexity=args.complexity,
        priority=args.priority
    )
    
    print(f"✅ 功能请求已添加：{entry_id}")
    print(f"   功能：{args.capability}")
    print(f"   复杂度：{args.complexity}")
    print(f"   文件：{manager.features_file}")


def cmd_list_pending(args):
    """列出待处理的高优先级条目"""
    workspace = Path(args.workspace).resolve()
    manager = LearningManager(workspace)
    
    if not manager.learnings_file.exists():
        print("⚠️ 学习记录文件不存在，请先运行 init")
        return
    
    pending = manager.get_pending_high_priority()
    
    if not pending:
        print("✅ 没有待处理的高优先级条目")
        return
    
    print(f"\n📋 待处理的高优先级条目 ({len(pending)} 条):\n")
    for item in pending:
        print(f"  [{item['id']}] {item['category']}")
        print(f"   优先级：{item['priority']}")
        print(f"   预览：{item['content'][:100]}...\n")


def cmd_check_recurring(args):
    """检查重复模式"""
    workspace = Path(args.workspace).resolve()
    manager = LearningManager(workspace)
    
    if not manager.learnings_file.exists():
        print("⚠️ 学习记录文件不存在，请先运行 init")
        return
    
    recurring = manager.check_recurring_patterns()
    
    if not recurring:
        print("✅ 没有发现重复模式 (Recurrence-Count >= 3)")
        return
    
    print(f"\n🔄 发现重复模式 ({len(recurring)} 个):\n")
    for item in recurring:
        print(f"  [{item['id']}] Pattern-Key: {item['pattern_key']}")
        print(f"   重复次数：{item['recurrence_count']}")
        print(f"   建议：提升到项目文件\n")


def main():
    parser = argparse.ArgumentParser(
        description='Learning Manager CLI - 学习记录管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--workspace',
        type=str,
        default='./workspace',
        help='工作目录路径 (默认：./workspace)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # init 命令
    init_parser = subparsers.add_parser('init', help='初始化学习记录目录')
    init_parser.set_defaults(func=cmd_init)
    
    # add-learning 命令
    learn_parser = subparsers.add_parser('add-learning', help='添加学习记录')
    learn_parser.add_argument('--category', required=True, help='分类 (correction/knowledge_gap/best_practice/gotcha/workflow)')
    learn_parser.add_argument('--summary', required=True, help='摘要')
    learn_parser.add_argument('--details', help='详细信息')
    learn_parser.add_argument('--priority', choices=['low', 'medium', 'high', 'critical'], default='medium')
    learn_parser.add_argument('--area', choices=['frontend', 'backend', 'infra', 'tests', 'docs', 'config'], default='config')
    learn_parser.add_argument('--source', choices=['conversation', 'error', 'user_feedback', 'knowledge_gap'], default='conversation')
    learn_parser.add_argument('--files', nargs='*', help='相关文件')
    learn_parser.add_argument('--pattern-key', help='模式键 (用于重复检测)')
    learn_parser.set_defaults(func=cmd_add_learning)
    
    # add-error 命令
    error_parser = subparsers.add_parser('add-error', help='添加错误记录')
    error_parser.add_argument('--command', required=True, help='失败的命令')
    error_parser.add_argument('--error', required=True, help='错误信息')
    error_parser.add_argument('--context', help='上下文')
    error_parser.add_argument('--priority', choices=['low', 'medium', 'high', 'critical'], default='high')
    error_parser.add_argument('--area', choices=['frontend', 'backend', 'infra', 'tests', 'docs', 'config'], default='config')
    error_parser.add_argument('--reproducible', choices=['yes', 'no', 'unknown'], default='unknown')
    error_parser.set_defaults(func=cmd_add_error)
    
    # add-feature 命令
    feat_parser = subparsers.add_parser('add-feature', help='添加功能请求')
    feat_parser.add_argument('--capability', required=True, help='功能描述')
    feat_parser.add_argument('--context', help='用户上下文')
    feat_parser.add_argument('--complexity', choices=['simple', 'medium', 'complex'], default='medium')
    feat_parser.add_argument('--priority', choices=['low', 'medium', 'high'], default='medium')
    feat_parser.set_defaults(func=cmd_add_feature)
    
    # list-pending 命令
    pending_parser = subparsers.add_parser('list-pending', help='列出待处理的高优先级条目')
    pending_parser.set_defaults(func=cmd_list_pending)
    
    # check-recurring 命令
    recurring_parser = subparsers.add_parser('check-recurring', help='检查重复模式')
    recurring_parser.set_defaults(func=cmd_check_recurring)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
