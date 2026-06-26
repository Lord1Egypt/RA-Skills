#!/usr/bin/env python3
"""
pytest-test-master CLI
pytest 专项技能命令行工具
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pytest_master import (
    ALL_TOPICS, get_topic_keys, output_content, list_all_topics
)


def main():
    parser = argparse.ArgumentParser(
        description="pytest-test-master — pytest 专项技能",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
子命令:
  fixtures     fixtures 最佳实践（scope/yield/params/autouse/request/teardown/session/inject）
  mock         mock/patch 使用模式（patch/mock_obj/assert_calls/freeze/spy/scope_mock/common）
  parametrize  参数化测试（basic/ids/indirect/combine/generate/product）
  coverage     coverage 报告分析（report/html/xml/threshold/exclude/debug）
  data         测试数据生成（faker/factory/fixture_data/seed/strategy）

示例:
  %(prog)s fixtures scope              # 查看 fixture scope 级别说明
  %(prog)s mock patch                  # 查看 @patch 装饰器用法
  %(prog)s parametrize combine          # 查看多 parametrize 组合
  %(prog)s coverage threshold           # 查看覆盖率阈值设置
  %(prog)s data factory                 # 查看 factory_boy 工厂模式
  %(prog)s fixtures                     # 列出 fixtures 所有主题
  %(prog)s --list                       # 列出所有可用主题
  %(prog)s --all fixtures               # 列出 fixtures 下所有主题（含标题）
        """
    )

    # 子命令定位
    parser.add_argument("subcommand", nargs="?", default=None,
                        help="子命令: fixtures | mock | parametrize | coverage | data")
    parser.add_argument("topic", nargs="?", default=None,
                        help="具体主题（查看子命令可用主题）")

    # 列表选项
    parser.add_argument("--list", "-l", action="store_true",
                        help="列出所有可用主题")
    parser.add_argument("--all", "-a", dest="show_all", metavar="SUBCOMMAND",
                        help="显示子命令下所有主题（含标题）")
    parser.add_argument("--topics", dest="topics_for", metavar="SUBCOMMAND",
                        help="显示子命令的所有 topic key")

    args = parser.parse_args()

    # --list: 列出所有主题
    if args.list:
        print(list_all_topics())
        return 0

    # --all: 显示子命令下所有主题
    if args.show_all:
        if args.show_all not in ALL_TOPICS:
            print(f"未知子命令: {args.show_all}，可用: {', '.join(ALL_TOPICS.keys())}", file=sys.stderr)
            return 1
        print(output_content(args.show_all, None))
        return 0

    # --topics: 显示子命令的 topic key
    if args.topics_for:
        if args.topics_for not in ALL_TOPICS:
            print(f"未知子命令: {args.topics_for}，可用: {', '.join(ALL_TOPICS.keys())}", file=sys.stderr)
            return 1
        for key in get_topic_keys(args.topics_for):
            print(key)
        return 0

    # 子命令 + topic: 输出具体内容
    if args.subcommand:
        if args.subcommand not in ALL_TOPICS:
            print(f"未知子命令: {args.subcommand}，可用: {', '.join(ALL_TOPICS.keys())}", file=sys.stderr)
            return 1

        if args.topic:
            result = output_content(args.subcommand, args.topic)
        else:
            # 只给子命令没给 topic，列出该子命令所有主题
            result = output_content(args.subcommand, None)

        print(result)
        return 0

    # 无参数：默认行为
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
