#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thin CLI entrypoint for the WeChat Article Assistant skill."""

from __future__ import annotations

from cli_args import build_parser
from cli_handlers import handle_command
from log_utils import configure_logging, get_logger
from utils import json_dumps


LOGGER = get_logger(__name__)


def print_result(result: dict, as_json: bool) -> int:
    if as_json:
        print(json_dumps(result))
    else:
        print(result.get("formatted_text") or json_dumps(result))
    return 0 if result.get("success") else 1


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(
        level="DEBUG" if args.debug else (args.log_level or None),
        console=True if args.debug else args.log_console,
        file_logging=True if args.debug else args.log_file,
        force=True,
    )
    try:
        result = handle_command(args)
    except Exception as exc:
        LOGGER.exception("command failed")
        result = {"success": False, "error": str(exc), "formatted_text": str(exc)}
    return print_result(result, as_json=bool(getattr(args, "json", False)))
