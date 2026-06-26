#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Command handlers for the WeChat Article Assistant CLI."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from typing import Any

from account_service import (
    add_account,
    add_account_by_keyword,
    add_account_by_url,
    delete_account,
    list_account_articles,
    list_accounts,
    list_sync_targets,
    resolve_account_by_url,
    search_account,
    set_account_config,
    set_sync_target,
)
from article_service import article_detail, export_account_report_markdown, export_recent_combined_report_markdown, fetch_account_details, recent_articles
from database import Database
from env_check import env_check
from login_service import login_clear, login_import, login_info, login_poll, login_start, login_wait
from log_utils import get_logger
from mp_client import WechatLoginExpiredError, WechatMPClient, WechatRequestError
from openclaw_messaging import OpenClawMessenger, resolve_message_target
from session_store import get_login_session
from sync_service import sync_account, sync_all, sync_due, sync_logs


LOGGER = get_logger(__name__)


def parse_proxy_urls(values: Any) -> list[str]:
    if values is None:
        return []
    if isinstance(values, str):
        values = [values]
    urls: list[str] = []
    for value in values:
        text = str(value or "").replace("\r", "\n").replace(",", "\n").replace(";", "\n")
        for item in text.split("\n"):
            item = item.strip()
            if item:
                urls.append(item)
    deduped: list[str] = []
    seen: set[str] = set()
    for item in urls:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


def serialize_proxy_urls(values: Any) -> str:
    return "\n".join(parse_proxy_urls(values))


def proxy_row_with_list(row: dict[str, Any]) -> dict[str, Any]:
    data = dict(row or {})
    data["proxy_urls"] = parse_proxy_urls(data.get("proxy_url"))
    data["proxy_count"] = len(data["proxy_urls"])
    return data


def resolve_cli_message_target(args: argparse.Namespace):
    return resolve_message_target(
        channel=args.channel or None,
        target=args.target or None,
        account=args.account or None,
        inbound_meta_json=args.inbound_meta_json or None,
        inbound_meta_file=args.inbound_meta_file or None,
    )


def validate_login_message_args(args: argparse.Namespace) -> dict[str, Any] | None:
    message_target = resolve_cli_message_target(args)
    if message_target:
        return None
    return {
        "success": False,
        "error": "login-start 缺少 channel/target",
        "formatted_text": "login-start 缺少 channel/target",
    }


def attach_message_target(result: dict[str, Any], message_target) -> dict[str, Any]:
    if not message_target:
        return result
    data = result.setdefault("data", {})
    if isinstance(data, dict):
        data.setdefault("message_target", asdict(message_target))
    return result


def handle_command(args: argparse.Namespace) -> dict[str, Any]:
    db = Database()
    try:
        LOGGER.debug("handle_command command=%s", args.command)
        if args.command == "login-start":
            validation_error = validate_login_message_args(args)
            if validation_error:
                return validation_error
            message_target = resolve_cli_message_target(args)
            result = login_start(
                db,
                messenger=OpenClawMessenger(message_target) if message_target else None,
                sid=args.sid,
                wait=args.wait,
                timeout=args.timeout,
                interval=args.interval,
                notify=args.notify,
            )
            return attach_message_target(result, message_target)
        if args.command == "login-poll":
            message_target = resolve_cli_message_target(args)
            result = login_poll(
                db,
                sid=args.sid,
                messenger=OpenClawMessenger(message_target) if message_target else None,
                notify=args.notify,
            )
            return attach_message_target(result, message_target)
        if args.command == "login-wait":
            message_target = resolve_cli_message_target(args)
            result = login_wait(
                db,
                sid=args.sid,
                timeout=args.timeout,
                interval=args.interval,
                messenger=OpenClawMessenger(message_target) if message_target else None,
                notify=args.notify,
            )
            return attach_message_target(result, message_target)
        if args.command == "login-import":
            return login_import(db, file_path=args.file, validate=args.validate)
        if args.command == "login-info":
            return login_info(db, validate=args.validate)
        if args.command == "login-clear":
            return login_clear(db)
        if args.command == "proxy-set":
            now = int(__import__("time").time())
            proxy_urls = parse_proxy_urls(getattr(args, "urls", []) or [])
            proxy_urls.extend(parse_proxy_urls(getattr(args, "url", "")))
            db.execute(
                """
                INSERT INTO proxy_config (name, enabled, proxy_url, apply_article_fetch, apply_sync, created_at, updated_at)
                VALUES ('default', ?, ?, ?, ?, COALESCE((SELECT created_at FROM proxy_config WHERE name = 'default'), ?), ?)
                ON CONFLICT(name) DO UPDATE SET
                  enabled = excluded.enabled,
                  proxy_url = excluded.proxy_url,
                  apply_article_fetch = excluded.apply_article_fetch,
                  apply_sync = excluded.apply_sync,
                  updated_at = excluded.updated_at
                """,
                (
                    1 if args.enabled else 0,
                    serialize_proxy_urls(proxy_urls),
                    1 if args.apply_article_fetch else 0,
                    1 if args.apply_sync else 0,
                    now,
                    now,
                ),
            )
            return {"success": True, "data": proxy_row_with_list(db.row("SELECT * FROM proxy_config WHERE name = 'default'") or {}), "formatted_text": "代理配置已更新"}
        if args.command == "proxy-show":
            return {"success": True, "data": proxy_row_with_list(db.row("SELECT * FROM proxy_config WHERE name = 'default'") or {}), "formatted_text": "当前代理配置"}
        if args.command == "search-account":
            return search_account(db, keyword=args.keyword, limit=args.limit)
        if args.command == "resolve-account-url":
            return resolve_account_by_url(db, url=args.url, limit=args.limit)
        if args.command == "add-account":
            return add_account(db, fakeid=args.fakeid, nickname=args.nickname, alias=args.alias, avatar=args.avatar, service_type=args.service_type, signature=args.signature, enable_sync=args.enable_sync, sync_hour=args.sync_hour, sync_minute=args.sync_minute, initial_sync=args.initial_sync, processing_mode=args.processing_mode, categories=args.categories, auto_export_markdown=args.auto_export_markdown)
        if args.command == "add-account-by-keyword":
            return add_account_by_keyword(db, keyword=args.keyword, limit=args.limit, initial_sync=args.initial_sync, processing_mode=args.processing_mode, categories=args.categories, auto_export_markdown=args.auto_export_markdown)
        if args.command == "add-account-by-url":
            return add_account_by_url(db, url=args.url, limit=args.limit, initial_sync=args.initial_sync, processing_mode=args.processing_mode, categories=args.categories, auto_export_markdown=args.auto_export_markdown)
        if args.command == "list-accounts":
            return list_accounts(db)
        if args.command == "set-account-config":
            return set_account_config(db, fakeid=args.fakeid, nickname=args.nickname, processing_mode=args.processing_mode, categories=args.categories, auto_export_markdown=args.auto_export_markdown)
        if args.command == "delete-account":
            return delete_account(db, fakeid=args.fakeid, nickname=args.nickname)
        if args.command == "list-sync-targets":
            return list_sync_targets(db)
        if args.command == "set-sync-target":
            return set_sync_target(db, fakeid=args.fakeid, nickname=args.nickname, enabled=args.enabled, sync_hour=args.sync_hour, sync_minute=args.sync_minute)
        if args.command == "list-account-articles":
            return list_account_articles(db, fakeid=args.fakeid, nickname=args.nickname, begin=args.begin, count=args.count, keyword=args.keyword, remote=args.remote, save_remote=args.save)
        if args.command == "fetch-account-details":
            return fetch_account_details(db, fakeid=args.fakeid, nickname=args.nickname, limit=args.limit, download_images=args.download_images, include_html=args.include_html, force_refresh=args.force_refresh, save_files=args.save, export_markdown=args.export_markdown, include_report_markdown=args.include_report_markdown, report_title=args.report_title)
        if args.command == "export-account-report":
            return export_account_report_markdown(db, fakeid=args.fakeid, nickname=args.nickname, limit=args.limit, title=args.title, save_file=args.save, include_markdown=args.include_markdown)
        if args.command == "export-recent-report":
            return export_recent_combined_report_markdown(db, hours=args.hours, limit=args.limit, title=args.title, save_file=args.save, include_markdown=args.include_markdown, only_markdown_accounts=args.only_markdown_accounts)
        if args.command == "sync":
            return sync_account(db, fakeid=args.fakeid)
        if args.command == "sync-all":
            return sync_all(
                db,
                interval_seconds=args.interval_seconds,
                channel=args.channel,
                target=args.target,
                account=args.account,
            )
        if args.command == "sync-due":
            return sync_due(db, grace_minutes=args.grace_minutes)
        if args.command == "sync-logs":
            return sync_logs(db, fakeid=args.fakeid, limit=args.limit)
        if args.command == "recent-articles":
            return recent_articles(db, hours=args.hours, limit=args.limit)
        if args.command == "article-detail":
            return article_detail(db, aid=args.aid, link=args.link, download_images=args.download_images, include_html=args.include_html, force_refresh=args.force_refresh, save_files=args.save)
        if args.command == "doctor":
            session = get_login_session(db)
            proxy = proxy_row_with_list(db.row("SELECT * FROM proxy_config WHERE name = 'default'") or {})
            client = WechatMPClient(db)
            env_result = env_check()
            session_summary: dict[str, Any] = {}
            if session:
                cookies = session.get("cookies") or []
                session_summary = {
                    "id": session.get("id"),
                    "token": session.get("token", ""),
                    "nickname": session.get("nickname", ""),
                    "head_img": session.get("head_img", ""),
                    "source": session.get("source", ""),
                    "valid": bool(session.get("valid")),
                    "last_validated_at": session.get("last_validated_at"),
                    "expires_at": session.get("expires_at"),
                    "created_at": session.get("created_at"),
                    "updated_at": session.get("updated_at"),
                    "cookie_count": len(cookies),
                    "has_cookie_header": bool(session.get("cookie_header")),
                }
            login_health: dict[str, Any] = {
                "present": bool(session and session.get("token")),
                "validated": False,
                "message": "未找到登录会话",
                "reason": "未找到登录会话",
                "reason_type": "missing_session",
            }
            if session and session.get("token"):
                try:
                    validated = client.validate_login()
                    login_health = {
                        "present": True,
                        "validated": True,
                        "message": "登录态校验通过",
                        "reason": "登录态校验通过",
                        "reason_type": "ok",
                        "nickname": validated.get("nickname", ""),
                        "head_img": validated.get("head_img", ""),
                        "token": validated.get("token", ""),
                    }
                except WechatLoginExpiredError as exc:
                    login_health = {"present": True, "validated": False, "message": str(exc), "reason": str(exc), "reason_type": "login_expired"}
                except WechatRequestError as exc:
                    login_health = {"present": True, "validated": False, "message": str(exc), "reason": str(exc), "reason_type": "request_error"}
            return {
                "success": True,
                "data": {
                    "logged_in": bool(login_health.get("validated")),
                    "login_session": session_summary,
                    "login_health": login_health,
                    "proxy_config": proxy or {},
                    "proxy_health": {
                        "sync": client.check_proxy_health("sync"),
                        "article": client.check_proxy_health("article"),
                    },
                    "env_check": env_result.get("data", {}),
                },
                "formatted_text": "系统状态检查完成",
            }
        if args.command == "env-check":
            return env_check()
        return {"success": False, "error": f"未知命令: {args.command}", "formatted_text": f"未知命令: {args.command}"}
    finally:
        db.close()
