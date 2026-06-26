#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Article metadata storage and queries."""

from __future__ import annotations

import json
from typing import Any

from database import Database
from log_utils import get_logger
from utils import now_ts, success


LOGGER = get_logger(__name__)


def normalize_remote_article(fakeid: str, article: dict[str, Any]) -> dict[str, Any]:
    payload = dict(article)
    payload["fakeid"] = fakeid
    payload["aid"] = str(article.get("aid") or f"{article.get('appmsgid', 0)}_{article.get('itemidx', 1)}")
    payload["title"] = str(article.get("title") or "")
    payload["link"] = str(article.get("link") or "")
    payload["digest"] = str(article.get("digest") or "")
    payload["cover"] = str(article.get("cover") or "")
    payload["author_name"] = str(article.get("author_name") or "")
    payload["create_time"] = int(article.get("create_time") or 0)
    payload["update_time"] = int(article.get("update_time") or payload["create_time"] or 0)
    payload["is_deleted"] = 1 if article.get("is_deleted") else 0
    return payload


def upsert_articles(db: Database, fakeid: str, articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    LOGGER.debug("upsert_articles fakeid=%s count=%s", fakeid, len(articles))
    now = now_ts()
    saved: list[dict[str, Any]] = []
    for article in articles:
        normalized = normalize_remote_article(fakeid, article)
        article_id = f"{fakeid}:{normalized['aid']}"
        db.execute(
            """
            INSERT INTO article
            (id, fakeid, aid, title, link, digest, cover, author_name, create_time, update_time, is_deleted, detail_fetched, payload_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT detail_fetched FROM article WHERE id = ?), 0), ?, COALESCE((SELECT created_at FROM article WHERE id = ?), ?), ?)
            ON CONFLICT(id) DO UPDATE SET
              title = excluded.title,
              link = excluded.link,
              digest = excluded.digest,
              cover = excluded.cover,
              author_name = excluded.author_name,
              create_time = excluded.create_time,
              update_time = excluded.update_time,
              is_deleted = excluded.is_deleted,
              payload_json = excluded.payload_json,
              updated_at = excluded.updated_at
            """,
            (
                article_id,
                fakeid,
                normalized["aid"],
                normalized["title"],
                normalized["link"],
                normalized["digest"],
                normalized["cover"],
                normalized["author_name"],
                normalized["create_time"] or None,
                normalized["update_time"] or None,
                normalized["is_deleted"],
                article_id,
                json.dumps(normalized, ensure_ascii=False),
                article_id,
                now,
                now,
            ),
        )
        saved.append(normalized)
    return saved


def query_local_articles(
    db: Database,
    fakeid: str,
    begin: int = 0,
    count: int = 10,
    keyword: str = "",
) -> list[dict[str, Any]]:
    sql = """
        SELECT fakeid, aid, title, link, digest, cover, author_name, create_time, update_time, is_deleted
        FROM article
        WHERE fakeid = ?
    """
    params: list[Any] = [fakeid]
    if keyword:
        sql += " AND (title LIKE ? OR digest LIKE ?)"
        like = f"%{keyword}%"
        params.extend([like, like])
    sql += " ORDER BY create_time DESC, updated_at DESC LIMIT ? OFFSET ?"
    params.extend([count, begin])
    return db.rows(sql, params)


def recent_articles(db: Database, hours: int = 24, limit: int = 50) -> dict[str, Any]:
    cutoff = now_ts() - hours * 3600
    rows = db.rows(
        """
        SELECT fakeid, aid, title, link, digest, cover, author_name, create_time, update_time
        FROM article
        WHERE create_time >= ?
        ORDER BY create_time DESC
        LIMIT ?
        """,
        (cutoff, limit),
    )
    return success({"hours": hours, "total": len(rows), "articles": rows}, f"閺堚偓鏉?{hours} 鐏忓繑妞傞弬鍥╃彿閺? {len(rows)}")


def get_article_row(db: Database, aid: str = "", link: str = "") -> dict[str, Any] | None:
    if aid:
        return db.row("SELECT * FROM article WHERE aid = ? ORDER BY update_time DESC LIMIT 1", (aid,))
    if link:
        return db.row("SELECT * FROM article WHERE link = ? ORDER BY update_time DESC LIMIT 1", (link,))
    return None
