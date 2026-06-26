#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared helpers for account services."""

from __future__ import annotations

import json

from bs4 import BeautifulSoup

from database import Database


VALID_PROCESSING_MODES = {"sync_only", "sync_and_detail"}


def normalize_processing_mode(value: str | None) -> str:
    normalized = str(value or "sync_only").strip().lower()
    if normalized not in VALID_PROCESSING_MODES:
        raise ValueError(f"娑撳秵鏁幐浣烘畱 processing_mode: {value}")
    return normalized


def normalize_categories(categories: str | list[str] | tuple[str, ...] | None) -> list[str]:
    if categories is None:
        return []
    if isinstance(categories, str):
        raw = categories.strip()
        if not raw:
            return []
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = raw.replace(";", ",").replace("|", ",").split(",")
    else:
        parsed = list(categories)

    result: list[str] = []
    seen: set[str] = set()
    for item in parsed:
        text = str(item or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    if len(result) > 1:
        result = result[:1]
    return result


def serialize_categories(categories: str | list[str] | tuple[str, ...] | None) -> str:
    return json.dumps(normalize_categories(categories), ensure_ascii=False)


def decorate_account_row(row: dict | None) -> dict | None:
    if not row:
        return None
    data = dict(row)
    data["processing_mode"] = normalize_processing_mode(str(data.get("processing_mode") or "sync_only"))
    data["categories"] = normalize_categories(str(data.get("categories_json") or "[]"))
    data["auto_export_markdown"] = bool(int(data.get("auto_export_markdown") or 0))
    return data


def resolve_account(db: Database, fakeid: str = "", nickname: str = "") -> dict | None:
    if fakeid:
        return decorate_account_row(db.row("SELECT * FROM account WHERE fakeid = ?", (fakeid,)))
    if nickname:
        return decorate_account_row(db.row("SELECT * FROM account WHERE nickname = ?", (nickname,)))
    return None


def pick_exact_match(accounts: list[dict], keyword: str) -> dict | None:
    normalized_keyword = keyword.strip().casefold()
    exact_matches = [
        item
        for item in accounts
        if str(item.get("nickname", "")).strip().casefold() == normalized_keyword
        or str(item.get("alias", "")).strip().casefold() == normalized_keyword
    ]
    if len(exact_matches) == 1:
        return exact_matches[0]
    if len(accounts) == 1:
        return accounts[0]
    return None


def extract_account_name_from_article_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for selector in [".wx_follow_nickname", "#js_name", "mp-common-profile"]:
        node = soup.select_one(selector)
        if not node:
            continue
        if selector == "mp-common-profile":
            candidate = str(node.get("data-nickname") or "").strip()
        else:
            candidate = node.get_text(strip=True)
        if candidate:
            return candidate
    meta = soup.find("meta", attrs={"property": "profile:nickname"})
    return str(meta.get("content") or "").strip() if meta else ""
