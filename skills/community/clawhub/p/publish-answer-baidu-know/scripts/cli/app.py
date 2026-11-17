"""CLI：argparse 与分发。"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from service.task_service import (
    cmd_config_path,
    cmd_health,
    cmd_log_get,
    cmd_logs,
    cmd_run,
    cmd_version,
)
from util.config_bootstrap import bootstrap_skill_config
from util.argparse_zh import ZhArgumentParser
from util.constants import LOG_LOGGER_NAME, SKILL_SLUG
from util.logging_config import get_skill_logger, setup_skill_logging


def _cli_str_or_none(raw: Optional[str]) -> Optional[str]:
    if raw is None:
        return None
    v = str(raw).strip()
    return v or None


def _handle_run(args: argparse.Namespace) -> int:
    """分发 run 子命令。

    支持两种模式：
    1. 业务模式（推荐）：--question-url + --input-id + [--target] + [--idempotency-key]
    2. 兼容位置参数：run [target] [input_id]（仅用于快速测试，不传 --question-url 时
       会进入 mock 模式或返回参数错误）
    """
    question_url = _cli_str_or_none(getattr(args, "question_url", None))
    input_id = _cli_str_or_none(getattr(args, "input_id", None))
    target = _cli_str_or_none(getattr(args, "target", None))
    idempotency_key = _cli_str_or_none(getattr(args, "idempotency_key", None))

    # 兼容位置参数：未显式传 --question-url 时，把位置参数兜底解析
    tail = [str(x).strip() for x in (args.run_tail or []) if str(x).strip()]
    if not question_url and not input_id and len(tail) <= 2:
        # 旧式：run [target] [input_id]
        if len(tail) == 2:
            target = target or tail[0]
            input_id = input_id or tail[1]
        elif len(tail) == 1:
            if tail[0].isdigit():
                input_id = input_id or tail[0]
            else:
                target = target or tail[0]

    return cmd_run(
        target=target,
        input_id=input_id,
        question_url=question_url,
        idempotency_key=idempotency_key,
    )


def _print_full_usage() -> None:
    print(f"{SKILL_SLUG} 可用命令：")
    print("  python main.py run --question-url URL --input-id PATH [--target ACCOUNT] [--idempotency-key KEY]")
    print("  python main.py logs [--limit N] [--status s] [--task-type t] [--target-id tid]")
    print("  python main.py log-get <log_id>")
    print("  python main.py health")
    print("  python main.py config-path")
    print("  python main.py version")


def build_parser() -> ZhArgumentParser:
    p = ZhArgumentParser(
        prog="main.py",
        description="百度知道回答自动发布：把本地回答文稿发布到百度知道指定问题下。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="cmd", required=True, parser_class=ZhArgumentParser)

    sp = sub.add_parser("run", help="发布回答到百度知道指定问题")
    sp.add_argument("--question-url", "-u", default=None, metavar="问题URL", dest="question_url",
                    help="百度知道问题页 URL（必填）")
    sp.add_argument("--input-id", "-i", default=None, metavar="回答文稿路径", dest="input_id",
                    help="本地回答文稿文件路径（必填）")
    sp.add_argument("--target", "-t", default=None, metavar="账号",
                    help="指定账号 ID 或登录标识；省略时由 account-manager 自动挑选")
    sp.add_argument("--idempotency-key", default=None, metavar="幂等键", dest="idempotency_key",
                    help="幂等键，重复运行同一键不会重复发布")
    sp.add_argument("run_tail", nargs="*", metavar="位置参数（兼容旧式）")
    sp.set_defaults(handler=_handle_run)

    sp = sub.add_parser("logs", help="查看任务日志")
    sp.add_argument("--limit", type=int, default=10)
    sp.add_argument("--status", default=None)
    sp.add_argument("--task-type", default=None, dest="task_type")
    sp.add_argument("--target-id", default=None, dest="target_id")
    sp.set_defaults(handler=lambda a: cmd_logs(
        limit=a.limit, status=a.status, task_type=a.task_type, target_id=a.target_id
    ))

    sp = sub.add_parser("log-get", help="按 log_id 查看单条任务日志(JSON)")
    sp.add_argument("log_id")
    sp.set_defaults(handler=lambda a: cmd_log_get(a.log_id))

    sp = sub.add_parser("health", help="健康检查")
    sp.set_defaults(handler=lambda _a: cmd_health())

    sp = sub.add_parser("config-path", help="输出用户 .env 与模板路径")
    sp.set_defaults(handler=lambda _a: cmd_config_path())

    sp = sub.add_parser("version", help="版本信息(JSON)")
    sp.set_defaults(handler=lambda _a: cmd_version())
    return p


def main(argv: Optional[List[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    bootstrap_skill_config()
    setup_skill_logging(SKILL_SLUG, LOG_LOGGER_NAME)
    get_skill_logger().info("cli_start argv=%s", sys.argv)
    if not argv:
        _print_full_usage()
        return 1
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.handler(args))
