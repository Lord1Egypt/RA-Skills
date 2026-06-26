from __future__ import annotations

import argparse
from typing import Callable

from toupiaoya.commands import auth_cmd, material_cmd, project_cmd, search_cmd, upload_cmd
from toupiaoya.constants import DEFAULT_BASE_URL


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="toupiaoya CLI: search / login / auth / project (create|list) / upload / material"
    )

    subparsers = parser.add_subparsers(dest="command")

    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=(
            "API 根地址（环境变量 TOUPIAOYA_API_BASE 或 EQXIU_AIGC_API_BASE；"
            f"未设置则内置默认 {DEFAULT_BASE_URL!r}）"
        ),
    )

    search_cmd.register(subparsers)
    project_cmd.register(subparsers)
    auth_cmd.register(subparsers)
    upload_cmd.register(subparsers)
    material_cmd.register(subparsers)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    command = args.command or "search"
    dispatch: dict[str, Callable[[argparse.Namespace, argparse.ArgumentParser], None]] = {
        "search": search_cmd.run,
        "upload": upload_cmd.run,
    }

    if command == "login":
        auth_cmd.run_login()
    elif command == "auth":
        auth_cmd.run_auth(args, parser)
    elif command == "material":
        material_cmd.run_material(args, parser)
    elif command == "project":
        project_cmd.run_project(args, parser)
    elif command in dispatch:
        dispatch[command](args, parser)
    else:
        parser.print_help()
