from __future__ import annotations

import argparse
import json
import sys

from toupiaoya.auth import auth_status, cmd_login, resolve_token


def register(subparsers: argparse._SubParsersAction) -> None:
    subparsers.add_parser(
        "login",
        help="交互式登录：将 X-Openclaw-Token 写入 ~/.toupiaoya/config.json（推荐）",
    )
    auth_parser = subparsers.add_parser("auth", help="认证相关命令")
    auth_subparsers = auth_parser.add_subparsers(dest="auth_command")
    status_parser = auth_subparsers.add_parser("status", help="验证登录状态")
    status_parser.add_argument(
        "--access-token",
        type=str,
        required=False,
        default=None,
        help="X-Openclaw-Token；默认从 ~/.toupiaoya/config.json 读取",
    )


def run_login() -> None:
    cmd_login()


def run_auth(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    auth_command = getattr(args, "auth_command", None)
    if auth_command != "status":
        parser.print_help()
        raise SystemExit(1)
    token_cli = getattr(args, "access_token", None)
    token = resolve_token(token_cli)
    if not token:
        print(
            "缺少 X-Openclaw-Token：请先执行 `login` 或传 --access-token。",
            file=sys.stderr,
        )
        raise SystemExit(1)
    result = auth_status(token)
    print(json.dumps(result, ensure_ascii=False, indent=2))
