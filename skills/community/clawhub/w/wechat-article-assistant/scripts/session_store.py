#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Persistence for login sessions and login QR-code sessions."""

from __future__ import annotations

import json
from typing import Any

from database import Database
from utils import cookie_entities_to_header, min_cookie_expiry, now_ts


def get_login_session(db: Database) -> dict[str, Any] | None:
    row = db.row("SELECT * FROM login_session WHERE id = 1")
    if not row:
        return None
    row["cookies"] = json.loads(row.get("cookie_json") or "[]")
    row["valid"] = bool(row.get("valid"))
    return row


def save_login_session(
    db: Database,
    token: str,
    cookies: list[dict[str, Any]],
    nickname: str = "",
    head_img: str = "",
    source: str = "",
    valid: bool = True,
) -> dict[str, Any]:
    now = now_ts()
    expires_at = min_cookie_expiry(cookies)
    cookie_json = json.dumps(cookies, ensure_ascii=False)
    cookie_header = cookie_entities_to_header(cookies)
    existing = get_login_session(db)
    if existing:
        db.execute(
            """
            UPDATE login_session
            SET token = ?, cookie_json = ?, cookie_header = ?, nickname = ?, head_img = ?,
                source = ?, valid = ?, last_validated_at = ?, expires_at = ?, updated_at = ?
            WHERE id = 1
            """,
            (
                token,
                cookie_json,
                cookie_header,
                nickname or "",
                head_img or "",
                source or "",
                1 if valid else 0,
                now if valid else None,
                expires_at,
                now,
            ),
        )
    else:
        db.execute(
            """
            INSERT INTO login_session
            (id, token, cookie_json, cookie_header, nickname, head_img, source, valid, last_validated_at, expires_at, created_at, updated_at)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                token,
                cookie_json,
                cookie_header,
                nickname or "",
                head_img or "",
                source or "",
                1 if valid else 0,
                now if valid else None,
                expires_at,
                now,
                now,
            ),
        )
    return get_login_session(db) or {}


def update_login_validation(db: Database, valid: bool, nickname: str = "", head_img: str = "") -> dict[str, Any] | None:
    session = get_login_session(db)
    if not session:
        return None
    now = now_ts()
    db.execute(
        """
        UPDATE login_session
        SET valid = ?, last_validated_at = ?, nickname = CASE WHEN ? <> '' THEN ? ELSE nickname END,
            head_img = CASE WHEN ? <> '' THEN ? ELSE head_img END, updated_at = ?
        WHERE id = 1
        """,
        (
            1 if valid else 0,
            now,
            nickname or "",
            nickname or "",
            head_img or "",
            head_img or "",
            now,
        ),
    )
    return get_login_session(db)


def clear_login_session(db: Database) -> None:
    db.execute("DELETE FROM login_session WHERE id = 1")


def save_qrcode_session(
    db: Database,
    sid: str,
    cookies: list[dict[str, Any]],
    qr_path: str,
    status: int = 0,
    status_text: str = "等待扫码",
    expires_at: int | None = None,
    notify_channel: str = "",
    notify_target: str = "",
    notify_account: str = "",
) -> dict[str, Any]:
    now = now_ts()
    db.execute(
        """
        INSERT OR REPLACE INTO login_qrcode_session
        (sid, status, status_text, cookie_json, qr_path, notify_channel, notify_target, notify_account, created_at, expires_at, updated_at, completed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT created_at FROM login_qrcode_session WHERE sid = ?), ?), ?, ?, (SELECT completed_at FROM login_qrcode_session WHERE sid = ?))
        """,
        (
            sid,
            status,
            status_text,
            json.dumps(cookies, ensure_ascii=False),
            qr_path,
            notify_channel or "",
            notify_target or "",
            notify_account or "",
            sid,
            now,
            expires_at,
            now,
            sid,
        ),
    )
    return get_qrcode_session(db, sid) or {}


def get_qrcode_session(db: Database, sid: str) -> dict[str, Any] | None:
    row = db.row("SELECT * FROM login_qrcode_session WHERE sid = ?", (sid,))
    if not row:
        return None
    row["cookies"] = json.loads(row.get("cookie_json") or "[]")
    return row


def update_qrcode_status(
    db: Database,
    sid: str,
    status: int,
    status_text: str,
    cookies: list[dict[str, Any]] | None = None,
    completed: bool = False,
) -> dict[str, Any] | None:
    now = now_ts()
    if cookies is None:
        db.execute(
            """
            UPDATE login_qrcode_session
            SET status = ?, status_text = ?, updated_at = ?, completed_at = CASE WHEN ? = 1 THEN ? ELSE completed_at END
            WHERE sid = ?
            """,
            (status, status_text, now, 1 if completed else 0, now, sid),
        )
    else:
        db.execute(
            """
            UPDATE login_qrcode_session
            SET status = ?, status_text = ?, cookie_json = ?, updated_at = ?,
                completed_at = CASE WHEN ? = 1 THEN ? ELSE completed_at END
            WHERE sid = ?
            """,
            (
                status,
                status_text,
                json.dumps(cookies, ensure_ascii=False),
                now,
                1 if completed else 0,
                now,
                sid,
            ),
        )
    return get_qrcode_session(db, sid)
