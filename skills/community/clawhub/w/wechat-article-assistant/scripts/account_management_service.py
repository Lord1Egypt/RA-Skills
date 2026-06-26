#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Account creation and discovery services."""

from __future__ import annotations

from article_metadata_service import upsert_articles
from database import Database
from log_utils import get_logger
from mp_client import WechatMPClient
from sync_service import sync_account
from utils import failure, normalize_mp_article_url, now_ts, success

from account_helpers import (
    extract_account_name_from_article_html,
    normalize_categories,
    normalize_processing_mode,
    pick_exact_match,
    serialize_categories,
)


LOGGER = get_logger(__name__)


def search_account(db: Database, keyword: str, limit: int = 10) -> dict:
    LOGGER.debug("search_account keyword=%s limit=%s", keyword, limit)
    client = WechatMPClient(db)
    accounts = client.search_accounts(keyword, count=limit)
    return success(
        {"keyword": keyword, "total": len(accounts), "accounts": accounts},
        f"閹兼粎鍌ㄩ崚?{len(accounts)} 娑擃亜鍙曟导妤€褰块崐娆撯偓?",
    )


def add_account(
    db: Database,
    fakeid: str,
    nickname: str,
    alias: str = "",
    avatar: str = "",
    service_type: int = 0,
    signature: str = "",
    enable_sync: bool = True,
    sync_hour: int = 8,
    sync_minute: int = 0,
    initial_sync: bool = False,
    processing_mode: str = "sync_only",
    categories: str | list[str] | tuple[str, ...] | None = None,
    auto_export_markdown: bool | None = None,
) -> dict:
    if not fakeid or not nickname:
        return failure("濞ｈ濮為崗顑跨船閸欓攱妞傝箛鍛淬€忛幓鎰返 fakeid 閸?nickname")
    LOGGER.info("add_account fakeid=%s nickname=%s initial_sync=%s", fakeid, nickname, initial_sync)
    now = now_ts()
    existing = db.row("SELECT processing_mode, categories_json, auto_export_markdown FROM account WHERE fakeid = ?", (fakeid,)) or {}
    normalized_mode = normalize_processing_mode(processing_mode or str(existing.get("processing_mode") or "sync_only"))
    normalized_categories = normalize_categories(categories if categories is not None else str(existing.get("categories_json") or "[]"))
    export_markdown = bool(auto_export_markdown) if auto_export_markdown is not None else bool(int(existing.get("auto_export_markdown") or 0))
    with db.transaction():
        db.connection.execute(
            """
            INSERT INTO account
            (fakeid, nickname, alias, avatar, service_type, signature, processing_mode, categories_json, auto_export_markdown, enabled, total_count, articles_synced, last_sync_at, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT total_count FROM account WHERE fakeid = ?), 0), COALESCE((SELECT articles_synced FROM account WHERE fakeid = ?), 0), (SELECT last_sync_at FROM account WHERE fakeid = ?), COALESCE((SELECT created_at FROM account WHERE fakeid = ?), ?), ?)
            ON CONFLICT(fakeid) DO UPDATE SET
              nickname = excluded.nickname,
              alias = excluded.alias,
              avatar = excluded.avatar,
              service_type = excluded.service_type,
              signature = excluded.signature,
              processing_mode = excluded.processing_mode,
              categories_json = excluded.categories_json,
              auto_export_markdown = excluded.auto_export_markdown,
              enabled = excluded.enabled,
              updated_at = excluded.updated_at
            """,
            (
                fakeid,
                nickname,
                alias or "",
                avatar or "",
                int(service_type or 0),
                signature or "",
                normalized_mode,
                serialize_categories(normalized_categories),
                1 if export_markdown else 0,
                1 if enable_sync else 0,
                fakeid,
                fakeid,
                fakeid,
                fakeid,
                now,
                now,
            ),
        )
        db.connection.execute(
            """
            INSERT INTO sync_config
            (fakeid, enabled, sync_hour, sync_minute, last_sync_at, last_sync_status, last_sync_message, created_at, updated_at)
            VALUES (?, ?, ?, ?, COALESCE((SELECT last_sync_at FROM sync_config WHERE fakeid = ?), NULL), COALESCE((SELECT last_sync_status FROM sync_config WHERE fakeid = ?), ''), COALESCE((SELECT last_sync_message FROM sync_config WHERE fakeid = ?), ''), COALESCE((SELECT created_at FROM sync_config WHERE fakeid = ?), ?), ?)
            ON CONFLICT(fakeid) DO UPDATE SET
              enabled = excluded.enabled,
              sync_hour = excluded.sync_hour,
              sync_minute = excluded.sync_minute,
              updated_at = excluded.updated_at
            """,
            (fakeid, 1 if enable_sync else 0, sync_hour, sync_minute, fakeid, fakeid, fakeid, fakeid, now, now),
        )
    sync_result = sync_account(db, fakeid) if initial_sync else None
    return success(
        {
            "fakeid": fakeid,
            "nickname": nickname,
            "alias": alias,
            "avatar": avatar,
            "processing_mode": normalized_mode,
            "categories": normalized_categories,
            "auto_export_markdown": export_markdown,
            "enabled": enable_sync,
            "sync_hour": sync_hour,
            "sync_minute": sync_minute,
            "initial_sync": sync_result,
        },
        f"瀹稿弶鍧婇崝鐘插彆娴兼褰? {nickname}",
    )


def add_account_by_keyword(
    db: Database,
    keyword: str,
    limit: int = 10,
    initial_sync: bool = False,
    processing_mode: str = "sync_only",
    categories: str | list[str] | tuple[str, ...] | None = None,
    auto_export_markdown: bool | None = None,
) -> dict:
    LOGGER.info("add_account_by_keyword keyword=%s limit=%s initial_sync=%s", keyword, limit, initial_sync)
    result = search_account(db, keyword, limit=limit)
    if not result.get("success"):
        return result
    accounts = result["data"]["accounts"]
    if not accounts:
        return failure(f"閺堫亝澹橀崚鏉垮彠闁款喖鐡ч垾?{keyword}閳ユ繂顕惔鏃傛畱閸忣兛绱崣?")
    account = pick_exact_match(accounts, keyword)
    if not account:
        return failure("鐎涙ê婀径姘嚋閸婃瑩鈧鍙曟导妤€褰块敍宀冾嚞閸忓牊澧界悰?search-account 閸愬秵妲戠涵?fakeid 濞ｈ濮?", {"keyword": keyword, "accounts": accounts})
    return add_account(
        db,
        fakeid=str(account.get("fakeid") or ""),
        nickname=str(account.get("nickname") or ""),
        alias=str(account.get("alias") or ""),
        avatar=str(account.get("round_head_img") or ""),
        service_type=int(account.get("service_type") or 0),
        signature=str(account.get("signature") or ""),
        initial_sync=initial_sync,
        processing_mode=processing_mode,
        categories=categories,
        auto_export_markdown=auto_export_markdown,
    )


def resolve_account_by_url(db: Database, url: str, limit: int = 20) -> dict:
    normalized_url = normalize_mp_article_url(url)
    LOGGER.info("resolve_account_by_url url=%s limit=%s", normalized_url, limit)
    client = WechatMPClient(db)
    html = client.fetch_public_article(normalized_url)
    account_name = extract_account_name_from_article_html(html)
    if not account_name:
        return failure("鏈兘浠庢枃绔犻摼鎺ヤ腑瑙ｆ瀽鍑哄叕浼楀彿鍚嶇О", {"url": normalized_url})
    candidates = client.search_accounts(account_name, count=limit)
    exact_matches = [item for item in candidates if str(item.get("nickname", "")).strip() == account_name or str(item.get("alias", "")).strip() == account_name]
    matched_accounts = exact_matches or candidates
    return success(
        {"url": normalized_url, "resolved_name": account_name, "total": len(matched_accounts), "accounts": matched_accounts},
        f"宸蹭粠鏂囩珷閾炬帴瑙ｆ瀽鍏紬鍙峰悕绉? {account_name}",
    )


def add_account_by_url(
    db: Database,
    url: str,
    limit: int = 20,
    initial_sync: bool = False,
    processing_mode: str = "sync_only",
    categories: str | list[str] | tuple[str, ...] | None = None,
    auto_export_markdown: bool | None = None,
) -> dict:
    LOGGER.info("add_account_by_url url=%s limit=%s initial_sync=%s", url, limit, initial_sync)
    resolved = resolve_account_by_url(db, url=url, limit=limit)
    if not resolved.get("success"):
        return resolved
    account_name = resolved["data"]["resolved_name"]
    accounts = resolved["data"]["accounts"]
    account = pick_exact_match(accounts, account_name)
    if not account:
        return failure("鏍规嵁鏂囩珷閾炬帴瑙ｆ瀽鍑轰簡鍏紬鍙峰悕绉帮紝浣嗗€欓€夊叕浼楀彿涓嶅敮涓€锛岃鍏堟墽琛?resolve-account-url 纭", resolved["data"])
    return add_account(
        db,
        fakeid=str(account.get("fakeid") or ""),
        nickname=str(account.get("nickname") or ""),
        alias=str(account.get("alias") or ""),
        avatar=str(account.get("round_head_img") or ""),
        service_type=int(account.get("service_type") or 0),
        signature=str(account.get("signature") or ""),
        initial_sync=initial_sync,
        processing_mode=processing_mode,
        categories=categories,
        auto_export_markdown=auto_export_markdown,
    )
