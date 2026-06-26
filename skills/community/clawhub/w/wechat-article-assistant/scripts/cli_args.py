#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Argument parser helpers for the WeChat Article Assistant CLI."""

from __future__ import annotations

import argparse

from utils import parse_bool


def add_json_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true")


def add_message_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--channel", default="")
    parser.add_argument("--target", default="")
    parser.add_argument("--account", default="")
    parser.add_argument("--inbound-meta-json", default="")
    parser.add_argument("--inbound-meta-file", default="")


def add_account_selector(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--fakeid", default="")
    parser.add_argument("--nickname", default="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="WeChat Article Assistant CLI")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--log-level", default="")
    parser.add_argument("--log-console", type=parse_bool, default=None)
    parser.add_argument("--log-file", type=parse_bool, default=None)
    subparsers = parser.add_subparsers(dest="command", required=True)

    p = subparsers.add_parser("login-start")
    add_message_args(p)
    p.add_argument("--sid", default="")
    p.add_argument("--wait", type=parse_bool, default=False)
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--interval", type=int, default=3)
    p.add_argument("--notify", type=parse_bool, default=True)
    add_json_flag(p)

    p = subparsers.add_parser("login-poll")
    add_message_args(p)
    p.add_argument("--sid", required=True)
    p.add_argument("--notify", type=parse_bool, default=False)
    add_json_flag(p)

    p = subparsers.add_parser("login-wait")
    add_message_args(p)
    p.add_argument("--sid", required=True)
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--interval", type=int, default=3)
    p.add_argument("--notify", type=parse_bool, default=True)
    add_json_flag(p)

    p = subparsers.add_parser("login-import")
    p.add_argument("--file", required=True)
    p.add_argument("--validate", type=parse_bool, default=True)
    add_json_flag(p)

    p = subparsers.add_parser("login-info")
    p.add_argument("--validate", type=parse_bool, default=False)
    add_json_flag(p)

    p = subparsers.add_parser("login-clear")
    add_json_flag(p)

    p = subparsers.add_parser("proxy-set")
    p.add_argument("--url", default="")
    p.add_argument("--enabled", type=parse_bool, default=True)
    p.add_argument("--apply-article-fetch", type=parse_bool, default=True)
    p.add_argument("--apply-sync", type=parse_bool, default=True)
    p.add_argument("--urls", action="append", default=[])
    add_json_flag(p)

    p = subparsers.add_parser("proxy-show")
    add_json_flag(p)

    p = subparsers.add_parser("search-account")
    p.add_argument("keyword")
    p.add_argument("--limit", type=int, default=10)
    add_json_flag(p)

    p = subparsers.add_parser("resolve-account-url")
    p.add_argument("--url", required=True)
    p.add_argument("--limit", type=int, default=20)
    add_json_flag(p)

    p = subparsers.add_parser("add-account")
    p.add_argument("--fakeid", required=True)
    p.add_argument("--nickname", required=True)
    p.add_argument("--alias", default="")
    p.add_argument("--avatar", default="")
    p.add_argument("--service-type", type=int, default=0)
    p.add_argument("--signature", default="")
    p.add_argument("--enable-sync", type=parse_bool, default=True)
    p.add_argument("--sync-hour", type=int, default=8)
    p.add_argument("--sync-minute", type=int, default=0)
    p.add_argument("--processing-mode", default="sync_only")
    p.add_argument("--categories", default="")
    p.add_argument("--auto-export-markdown", type=parse_bool, default=False)
    p.add_argument("--initial-sync", type=parse_bool, default=False)
    add_json_flag(p)

    p = subparsers.add_parser("add-account-by-keyword")
    p.add_argument("keyword")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--processing-mode", default="sync_only")
    p.add_argument("--categories", default="")
    p.add_argument("--auto-export-markdown", type=parse_bool, default=False)
    p.add_argument("--initial-sync", type=parse_bool, default=False)
    add_json_flag(p)

    p = subparsers.add_parser("add-account-by-url")
    p.add_argument("--url", required=True)
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--processing-mode", default="sync_only")
    p.add_argument("--categories", default="")
    p.add_argument("--auto-export-markdown", type=parse_bool, default=False)
    p.add_argument("--initial-sync", type=parse_bool, default=False)
    add_json_flag(p)

    p = subparsers.add_parser("list-accounts")
    add_json_flag(p)

    p = subparsers.add_parser("set-account-config")
    add_account_selector(p)
    p.add_argument("--processing-mode", default="")
    p.add_argument("--categories", default=None)
    p.add_argument("--auto-export-markdown", type=parse_bool, default=None)
    add_json_flag(p)

    p = subparsers.add_parser("delete-account")
    add_account_selector(p)
    add_json_flag(p)

    p = subparsers.add_parser("list-sync-targets")
    add_json_flag(p)

    p = subparsers.add_parser("set-sync-target")
    add_account_selector(p)
    p.add_argument("--enabled", type=parse_bool, default=True)
    p.add_argument("--sync-hour", type=int, default=None)
    p.add_argument("--sync-minute", type=int, default=None)
    add_json_flag(p)

    p = subparsers.add_parser("list-account-articles")
    add_account_selector(p)
    p.add_argument("--begin", type=int, default=0)
    p.add_argument("--count", type=int, default=10)
    p.add_argument("--keyword", default="")
    p.add_argument("--remote", type=parse_bool, default=True)
    p.add_argument("--save", type=parse_bool, default=True)
    add_json_flag(p)

    p = subparsers.add_parser("fetch-account-details")
    add_account_selector(p)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--download-images", type=parse_bool, default=True)
    p.add_argument("--include-html", type=parse_bool, default=False)
    p.add_argument("--force-refresh", type=parse_bool, default=False)
    p.add_argument("--save", type=parse_bool, default=True)
    p.add_argument("--export-markdown", type=parse_bool, default=True)
    p.add_argument("--include-report-markdown", type=parse_bool, default=True)
    p.add_argument("--report-title", default="")
    add_json_flag(p)

    p = subparsers.add_parser("export-account-report")
    add_account_selector(p)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--title", default="")
    p.add_argument("--save", type=parse_bool, default=True)
    p.add_argument("--include-markdown", type=parse_bool, default=True)
    add_json_flag(p)

    p = subparsers.add_parser("export-recent-report")
    p.add_argument("--hours", type=int, default=24)
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--title", default="")
    p.add_argument("--save", type=parse_bool, default=True)
    p.add_argument("--include-markdown", type=parse_bool, default=True)
    p.add_argument("--only-markdown-accounts", type=parse_bool, default=True)
    add_json_flag(p)

    p = subparsers.add_parser("sync")
    p.add_argument("--fakeid", required=True)
    add_json_flag(p)

    p = subparsers.add_parser("sync-all")
    p.add_argument("--interval-seconds", type=int, default=0)
    p.add_argument("--channel", default="")
    p.add_argument("--target", default="")
    p.add_argument("--account", default="")
    add_json_flag(p)

    p = subparsers.add_parser("sync-due")
    p.add_argument("--grace-minutes", type=int, default=3)
    add_json_flag(p)

    p = subparsers.add_parser("sync-logs")
    p.add_argument("--fakeid", default="")
    p.add_argument("--limit", type=int, default=50)
    add_json_flag(p)

    p = subparsers.add_parser("recent-articles")
    p.add_argument("--hours", type=int, default=24)
    p.add_argument("--limit", type=int, default=50)
    add_json_flag(p)

    p = subparsers.add_parser("article-detail")
    p.add_argument("--aid", default="")
    p.add_argument("--link", default="")
    p.add_argument("--download-images", type=parse_bool, default=True)
    p.add_argument("--include-html", type=parse_bool, default=False)
    p.add_argument("--force-refresh", type=parse_bool, default=False)
    p.add_argument("--save", type=parse_bool, default=True)
    add_json_flag(p)

    p = subparsers.add_parser("doctor")
    add_json_flag(p)

    p = subparsers.add_parser("env-check")
    add_json_flag(p)

    return parser
