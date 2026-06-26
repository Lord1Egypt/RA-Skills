#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manual smoke test runner for the WeChat Article Assistant skill.

Examples:
  python scripts/dev/smoke_test.py --cookie-file path/to/cookie.json
  python scripts/dev/smoke_test.py --steps login-import,search,add,remote-list
  python scripts/dev/smoke_test.py --proxy-url wechat.zzgzai.online --steps proxy,doctor,article-detail
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
CLI_PATH = SCRIPTS_DIR / "wechat_article_assistant.py"
DEFAULT_STEPS = [
    "doctor",
    "login-import",
    "search",
    "add",
    "remote-list",
    "sync",
    "article-detail",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run smoke tests for wechat-article-assistant")
    parser.add_argument("--home", default="", help="测试数据目录；为空时自动创建 .tmp 目录")
    parser.add_argument("--cookie-file", default="", help="登录 cookie JSON 文件")
    parser.add_argument("--keyword", default="水e交费", help="测试公众号关键字")
    parser.add_argument("--fakeid", default="", help="指定 fakeid，跳过自动解析")
    parser.add_argument("--article-aid", default="", help="指定文章 aid，跳过自动选择")
    parser.add_argument("--article-link", default="", help="指定文章链接，也可用于测试 URL 反查公众号")
    parser.add_argument("--proxy-url", default="", help="测试代理地址")
    parser.add_argument("--proxy-enable", default="true", help="是否启用代理")
    parser.add_argument("--steps", default=",".join(DEFAULT_STEPS), help="执行步骤，逗号分隔")
    parser.add_argument("--continue-on-error", action="store_true", help="某一步失败后继续后续步骤")
    parser.add_argument("--debug", action="store_true", help="为子命令开启 debug 日志")
    parser.add_argument("--log-level", default="", help="传给子命令的日志级别")
    return parser.parse_args()


def build_home(args: argparse.Namespace) -> Path:
    if args.home:
        return Path(args.home).expanduser().resolve()
    workspace_root = SCRIPTS_DIR.parents[4]
    suffix = time.strftime("%Y%m%d-%H%M%S")
    return (workspace_root / ".tmp" / f"wechat-article-assistant-smoke-{suffix}").resolve()


def run_cli(home: Path, extra_args: list[str], args: argparse.Namespace) -> tuple[int, dict[str, Any] | None, str, str]:
    command = [sys.executable, str(CLI_PATH)]
    if args.debug:
        command.append("--debug")
    elif args.log_level:
        command.extend(["--log-level", args.log_level])
    command.extend(extra_args)
    command.append("--json")

    env = os.environ.copy()
    env["WECHAT_ARTICLE_ASSISTANT_HOME"] = str(home)
    completed = subprocess.run(command, capture_output=True, env=env)
    payload: dict[str, Any] | None = None
    stdout = decode_output(completed.stdout)
    stderr = decode_output(completed.stderr)
    if stdout:
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            payload = None
    return completed.returncode, payload, stdout, stderr


def decode_output(raw: bytes) -> str:
    for encoding in ("utf-8", "gbk"):
        try:
            return raw.decode(encoding).strip()
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace").strip()


def print_step(name: str, code: int, payload: dict[str, Any] | None, stdout: str, stderr: str) -> None:
    print(f"\n=== {name} ===")
    print(f"exit_code: {code}")
    if payload is not None:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif stdout:
        print(stdout)
    if stderr:
        print("--- stderr ---")
        print(stderr)


def should_stop(code: int, payload: dict[str, Any] | None, args: argparse.Namespace) -> bool:
    failed = code != 0 or (payload is not None and not payload.get("success", False))
    return failed and not args.continue_on_error


def main() -> int:
    args = parse_args()
    steps = [item.strip() for item in args.steps.split(",") if item.strip()]
    home = build_home(args)
    state: dict[str, Any] = {"home": str(home), "fakeid": args.fakeid, "article_aid": args.article_aid}

    print(f"home: {home}")
    print(f"steps: {', '.join(steps)}")

    for step in steps:
        if step == "doctor":
            code, payload, stdout, stderr = run_cli(home, ["doctor"], args)
        elif step == "login-import":
            if not args.cookie_file:
                print("\n=== login-import ===\nskipped: missing --cookie-file")
                continue
            code, payload, stdout, stderr = run_cli(
                home,
                ["login-import", "--file", args.cookie_file, "--validate", "true"],
                args,
            )
        elif step == "proxy":
            if not args.proxy_url:
                print("\n=== proxy ===\nskipped: missing --proxy-url")
                continue
            code, payload, stdout, stderr = run_cli(
                home,
                [
                    "proxy-set",
                    "--url",
                    args.proxy_url,
                    "--enabled",
                    args.proxy_enable,
                    "--apply-article-fetch",
                    "true",
                    "--apply-sync",
                    "true",
                ],
                args,
            )
        elif step == "search":
            code, payload, stdout, stderr = run_cli(home, ["search-account", args.keyword, "--limit", "5"], args)
        elif step == "resolve-account-url":
            if not args.article_link:
                print("\n=== resolve-account-url ===\nskipped: missing --article-link")
                continue
            code, payload, stdout, stderr = run_cli(
                home,
                ["resolve-account-url", "--url", args.article_link, "--limit", "10"],
                args,
            )
        elif step == "add":
            code, payload, stdout, stderr = run_cli(
                home,
                ["add-account-by-keyword", args.keyword, "--initial-sync", "false"],
                args,
            )
        elif step == "add-account-url":
            if not args.article_link:
                print("\n=== add-account-url ===\nskipped: missing --article-link")
                continue
            code, payload, stdout, stderr = run_cli(
                home,
                ["add-account-by-url", "--url", args.article_link, "--initial-sync", "false"],
                args,
            )
        elif step == "remote-list":
            fakeid = state.get("fakeid")
            if not fakeid:
                print("\n=== remote-list ===\nskipped: missing fakeid")
                continue
            code, payload, stdout, stderr = run_cli(
                home,
                ["list-account-articles", "--fakeid", fakeid, "--remote", "true", "--count", "3"],
                args,
            )
        elif step == "sync":
            fakeid = state.get("fakeid")
            if not fakeid:
                print("\n=== sync ===\nskipped: missing fakeid")
                continue
            code, payload, stdout, stderr = run_cli(home, ["sync", "--fakeid", fakeid], args)
        elif step == "article-detail":
            target_aid = state.get("article_aid")
            if target_aid:
                code, payload, stdout, stderr = run_cli(
                    home,
                    ["article-detail", "--aid", target_aid, "--download-images", "true", "--include-html", "false"],
                    args,
                )
            elif args.article_link:
                code, payload, stdout, stderr = run_cli(
                    home,
                    ["article-detail", "--link", args.article_link, "--download-images", "true", "--include-html", "false"],
                    args,
                )
            else:
                print("\n=== article-detail ===\nskipped: missing article aid or link")
                continue
        else:
            print(f"\n=== {step} ===\nskipped: unknown step")
            continue

        print_step(step, code, payload, stdout, stderr)

        if payload and payload.get("success"):
            data = payload.get("data") or {}
            if step == "add":
                state["fakeid"] = data.get("fakeid") or state.get("fakeid")
            if step == "add-account-url":
                state["fakeid"] = data.get("fakeid") or state.get("fakeid")
            if step == "remote-list":
                articles = data.get("articles") or []
                if articles and not state.get("article_aid"):
                    state["article_aid"] = articles[0].get("aid", "")

        if should_stop(code, payload, args):
            return 1

    print("\n=== summary ===")
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
