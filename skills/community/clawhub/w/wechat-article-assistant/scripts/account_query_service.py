#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Account query, config and sync target services."""

from __future__ import annotations

from article_metadata_service import query_local_articles, upsert_articles
from database import Database
from log_utils import get_logger
from mp_client import WechatMPClient
from utils import failure, now_ts, success

from account_helpers import decorate_account_row, normalize_categories, normalize_processing_mode, resolve_account, serialize_categories


LOGGER = get_logger(__name__)


def list_accounts(db: Database) -> dict:
    rows = db.rows(
        """
        SELECT
          a.fakeid, a.nickname, a.alias, a.avatar, a.service_type, a.signature,
          a.processing_mode, a.categories_json, a.auto_export_markdown,
          a.enabled, a.total_count, a.articles_synced, a.last_sync_at,
          s.sync_hour, s.sync_minute, s.last_sync_status, s.last_sync_message
        FROM account a
        LEFT JOIN sync_config s ON s.fakeid = a.fakeid
        ORDER BY a.updated_at DESC
        """
    )
    decorated = [decorate_account_row(row) for row in rows]
    return success({"total": len(decorated), "accounts": decorated}, f"褰撳墠鍏?{len(decorated)} 涓叕浼楀彿")


def set_account_config(
    db: Database,
    fakeid: str = "",
    nickname: str = "",
    processing_mode: str = "",
    categories: str | list[str] | tuple[str, ...] | None = None,
    auto_export_markdown: bool | None = None,
) -> dict:
    account = resolve_account(db, fakeid=fakeid, nickname=nickname)
    if not account:
        return failure("鏈壘鍒版寚瀹氬叕浼楀彿")
    next_mode = normalize_processing_mode(processing_mode or str(account.get("processing_mode") or "sync_only"))
    next_categories = normalize_categories(categories if categories is not None else account.get("categories") or [])
    next_auto_export = bool(auto_export_markdown) if auto_export_markdown is not None else bool(account.get("auto_export_markdown"))
    db.execute(
        """
        UPDATE account
        SET processing_mode = ?, categories_json = ?, auto_export_markdown = ?, updated_at = ?
        WHERE fakeid = ?
        """,
        (next_mode, serialize_categories(next_categories), 1 if next_auto_export else 0, now_ts(), account["fakeid"]),
    )
    updated = resolve_account(db, fakeid=account["fakeid"]) or {}
    return success(updated, f"宸叉洿鏂板叕浼楀彿閰嶇疆: {account.get('nickname') or account['fakeid']}")


def delete_account(db: Database, fakeid: str = "", nickname: str = "") -> dict:
    account = resolve_account(db, fakeid=fakeid, nickname=nickname)
    if not account:
        return failure("鏈壘鍒版寚瀹氬叕浼楀彿")
    LOGGER.info("delete_account fakeid=%s nickname=%s", account["fakeid"], account.get("nickname", ""))
    target_fakeid = account["fakeid"]
    with db.transaction():
        db.connection.execute("DELETE FROM account WHERE fakeid = ?", (target_fakeid,))
        db.connection.execute("DELETE FROM sync_config WHERE fakeid = ?", (target_fakeid,))
        db.connection.execute("DELETE FROM article_detail WHERE fakeid = ?", (target_fakeid,))
        db.connection.execute("DELETE FROM article WHERE fakeid = ?", (target_fakeid,))
    return success({"fakeid": target_fakeid, "nickname": account.get("nickname", "")}, f"宸插垹闄ゅ叕浼楀彿: {account.get('nickname') or target_fakeid}")


def set_sync_target(
    db: Database,
    fakeid: str = "",
    nickname: str = "",
    enabled: bool | None = None,
    sync_hour: int | None = None,
    sync_minute: int | None = None,
) -> dict:
    account = resolve_account(db, fakeid=fakeid, nickname=nickname)
    if not account:
        return failure("鏈壘鍒版寚瀹氬叕浼楀彿")
    LOGGER.info("set_sync_target fakeid=%s enabled=%s sync_hour=%s sync_minute=%s", account["fakeid"], enabled, sync_hour, sync_minute)
    current = db.row("SELECT * FROM sync_config WHERE fakeid = ?", (account["fakeid"],)) or {}
    now = now_ts()
    db.execute(
        """
        INSERT INTO sync_config
        (fakeid, enabled, sync_hour, sync_minute, last_sync_at, last_sync_status, last_sync_message, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(fakeid) DO UPDATE SET
          enabled = excluded.enabled,
          sync_hour = excluded.sync_hour,
          sync_minute = excluded.sync_minute,
          updated_at = excluded.updated_at
        """,
        (
            account["fakeid"],
            1 if (enabled if enabled is not None else bool(current.get("enabled", 1))) else 0,
            sync_hour if sync_hour is not None else int(current.get("sync_hour", 8)),
            sync_minute if sync_minute is not None else int(current.get("sync_minute", 0)),
            current.get("last_sync_at"),
            current.get("last_sync_status", ""),
            current.get("last_sync_message", ""),
            current.get("created_at", now),
            now,
        ),
    )
    return success(db.row("SELECT * FROM sync_config WHERE fakeid = ?", (account["fakeid"],)) or {}, f"宸叉洿鏂板悓姝ラ厤缃? {account.get('nickname') or account['fakeid']}")


def list_sync_targets(db: Database) -> dict:
    rows = db.rows(
        """
        SELECT
          s.fakeid, a.nickname, a.processing_mode, a.categories_json, a.auto_export_markdown,
          s.enabled, s.sync_hour, s.sync_minute, s.last_sync_at, s.last_sync_status, s.last_sync_message
        FROM sync_config s
        LEFT JOIN account a ON a.fakeid = s.fakeid
        ORDER BY a.updated_at DESC, s.fakeid
        """
    )
    decorated = [decorate_account_row(row) for row in rows]
    return success({"total": len(decorated), "targets": decorated}, f"褰撳墠鍏?{len(decorated)} 涓悓姝ョ洰鏍?")


def list_account_articles(
    db: Database,
    fakeid: str = "",
    nickname: str = "",
    begin: int = 0,
    count: int = 10,
    keyword: str = "",
    remote: bool = True,
    save_remote: bool = True,
) -> dict:
    account = resolve_account(db, fakeid=fakeid, nickname=nickname)
    if not account:
        return failure("鏈壘鍒版寚瀹氬叕浼楀彿")
    target_fakeid = account["fakeid"]
    LOGGER.debug("list_account_articles fakeid=%s begin=%s count=%s keyword=%s remote=%s save_remote=%s", target_fakeid, begin, count, keyword, remote, save_remote)
    if remote:
        client = WechatMPClient(db)
        payload = client.fetch_article_page(fakeid=target_fakeid, begin=begin, count=count, keyword=keyword)
        articles = payload["articles"]
        if save_remote:
            upsert_articles(db, target_fakeid, articles)
        returned_articles = articles[:count] if count and count > 0 else articles
        return success(
            {
                "fakeid": target_fakeid,
                "nickname": account.get("nickname", ""),
                "remote": True,
                "total_count": payload.get("total_count", 0),
                "fetched_count": len(articles),
                "returned_count": len(returned_articles),
                "articles": [dict(item, fakeid=target_fakeid) for item in returned_articles],
            },
            f"杩滅鍛戒腑 {len(articles)} 绡囨枃绔狅紝杩斿洖 {len(returned_articles)} 绡?",
        )
    articles = query_local_articles(db, fakeid=target_fakeid, begin=begin, count=count, keyword=keyword)
    return success(
        {"fakeid": target_fakeid, "nickname": account.get("nickname", ""), "remote": False, "articles": articles, "total": len(articles)},
        f"鏈湴杩斿洖 {len(articles)} 绡囨枃绔?",
    )
