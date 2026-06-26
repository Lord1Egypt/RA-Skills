#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Account-level and combined article detail reports plus batch detail fetch."""

from __future__ import annotations

import json
import re
import time
from typing import Any

from article_detail_service import article_detail
from config import get_paths
from database import Database
from utils import ensure_dir, failure, format_timestamp, now_ts, safe_filename, success


def report_file_basename(prefix: str, timestamp: str, identifier: str = "") -> str:
    normalized_prefix = safe_filename(prefix, fallback="report")
    normalized_identifier = safe_filename(identifier, fallback="")
    if normalized_identifier:
        return f"{timestamp}_{normalized_prefix}_{normalized_identifier}"
    return f"{timestamp}_{normalized_prefix}"


def resolve_account_row(db: Database, fakeid: str = "", nickname: str = "") -> dict[str, Any] | None:
    if fakeid:
        return db.row("SELECT * FROM account WHERE fakeid = ?", (fakeid,))
    if nickname:
        return db.row("SELECT * FROM account WHERE nickname = ?", (nickname,))
    return None


def parse_categories_json(value: str) -> list[str]:
    raw = str(value or "").strip()
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = raw.replace(";", ",").replace("|", ",").split(",")
    result: list[str] = []
    seen: set[str] = set()
    for item in data:
        text = str(item or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def article_rows_for_account(db: Database, fakeid: str, article_ids: list[str] | None = None, limit: int = 0) -> list[dict[str, Any]]:
    sql = "SELECT * FROM article WHERE fakeid = ?"
    params: list[Any] = [fakeid]
    if article_ids:
        placeholders = ",".join("?" for _ in article_ids)
        sql += f" AND id IN ({placeholders})"
        params.extend(article_ids)
    sql += " ORDER BY create_time DESC, updated_at DESC"
    if limit and limit > 0:
        sql += " LIMIT ?"
        params.append(limit)
    return db.rows(sql, params)


def detail_rows_for_account(db: Database, fakeid: str, article_ids: list[str] | None = None, limit: int = 0) -> list[dict[str, Any]]:
    sql = """
        SELECT
          a.id AS article_id,
          a.fakeid,
          a.aid,
          a.title,
          a.link,
          a.digest,
          a.author_name,
          a.create_time,
          a.update_time,
          d.account_name,
          d.markdown_content,
          d.text_content,
          d.saved_json_path,
          d.saved_md_path,
          d.saved_html_path,
          d.fetched_at
        FROM article a
        INNER JOIN article_detail d ON d.article_id = a.id
        WHERE a.fakeid = ?
    """
    params: list[Any] = [fakeid]
    if article_ids:
        placeholders = ",".join("?" for _ in article_ids)
        sql += f" AND a.id IN ({placeholders})"
        params.extend(article_ids)
    sql += " ORDER BY a.create_time DESC, a.updated_at DESC"
    if limit and limit > 0:
        sql += " LIMIT ?"
        params.append(limit)
    return db.rows(sql, params)


def detail_rows_for_recent_articles(
    db: Database,
    hours: int = 24,
    limit: int = 200,
    only_markdown_accounts: bool = True,
) -> list[dict[str, Any]]:
    cutoff = now_ts() - max(1, int(hours or 24)) * 3600
    sql = """
        SELECT
          a.id AS article_id,
          a.fakeid,
          a.aid,
          a.title,
          a.link,
          a.digest,
          a.author_name,
          a.create_time,
          a.update_time,
          d.account_name,
          d.markdown_content,
          d.text_content,
          d.saved_json_path,
          d.saved_md_path,
          d.saved_html_path,
          d.fetched_at,
          ac.nickname AS account_nickname,
          ac.processing_mode,
          ac.categories_json,
          ac.auto_export_markdown
        FROM article a
        INNER JOIN article_detail d ON d.article_id = a.id
        INNER JOIN account ac ON ac.fakeid = a.fakeid
        WHERE a.create_time >= ?
    """
    params: list[Any] = [cutoff]
    if only_markdown_accounts:
        sql += " AND ac.auto_export_markdown = 1"
    sql += " ORDER BY a.create_time DESC, a.updated_at DESC"
    if limit and limit > 0:
        sql += " LIMIT ?"
        params.append(limit)
    return db.rows(sql, params)


def summary_text(detail_row: dict[str, Any]) -> str:
    digest = str(detail_row.get("digest") or "").strip()
    if digest:
        return digest
    text_content = str(detail_row.get("text_content") or "").strip()
    if not text_content:
        return ""
    one_line = re.sub(r"\s+", " ", text_content).strip()
    return one_line[:160]


def row_categories(detail_row: dict[str, Any]) -> list[str]:
    return parse_categories_json(str(detail_row.get("categories_json") or "[]"))


def primary_category(detail_row: dict[str, Any]) -> str:
    categories = row_categories(detail_row)
    return categories[0] if categories else "未分类"


def sort_combined_rows(detail_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        detail_rows,
        key=lambda row: (
            primary_category(row),
            str(row.get("account_nickname") or row.get("account_name") or row.get("fakeid") or ""),
            -int(row.get("create_time") or 0),
            str(row.get("title") or ""),
        ),
    )


def render_account_report_markdown(account: dict[str, Any], detail_rows: list[dict[str, Any]], report_title: str) -> str:
    nickname = str(account.get("nickname") or account.get("fakeid") or "")
    categories = parse_categories_json(str(account.get("categories_json") or "[]"))
    category_text = " / ".join(categories) if categories else "未分类"
    lines = [
        f"# {report_title}",
        "",
        f"- 来源公众号：{nickname}",
        f"- 公众号 fakeid：{account.get('fakeid') or ''}",
        f"- 同步策略：{account.get('processing_mode') or 'sync_only'}",
        f"- 主题分类：{category_text}",
        f"- 汇总时间：{format_timestamp(now_ts())}",
        f"- 文章数量：{len(detail_rows)}",
        "",
    ]
    for index, row in enumerate(detail_rows, start=1):
        item_title = str(row.get("title") or row.get("article_id") or f"文章 {index}")
        account_name = str(row.get("account_name") or nickname or "")
        author_name = str(row.get("author_name") or "").strip()
        publish_time = format_timestamp(int(row.get("create_time") or 0))
        summary = summary_text(row)
        markdown_content = str(row.get("markdown_content") or "").strip() or str(row.get("text_content") or "").strip()
        lines.extend([
            f"## {index}. {item_title}",
            "",
            f"- 标题：{item_title}",
            f"- 来源公众号：{account_name}",
            f"- 作者：{author_name or '未知'}",
            f"- 发布时间：{publish_time or '未知'}",
            f"- 主题分类：{category_text}",
            f"- 摘要：{summary or '无'}",
            f"- 链接：{row.get('link') or ''}",
            "",
            "### 内容",
            "",
            markdown_content or "无正文内容",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def render_combined_report_markdown(detail_rows: list[dict[str, Any]], report_title: str, hours: int) -> str:
    sorted_rows = sort_combined_rows(detail_rows)
    account_count = len({str(row.get("fakeid") or "") for row in sorted_rows if str(row.get("fakeid") or "").strip()})
    lines = [
        f"# {report_title}",
        "",
        f"- 汇总范围：最近 {hours} 小时",
        f"- 汇总时间：{format_timestamp(now_ts())}",
        f"- 公众号数量：{account_count}",
        f"- 文章数量：{len(sorted_rows)}",
        f"- 排序方式：先按主题分类分组，再按公众号和发布时间排序",
        "",
    ]

    current_category = None
    current_account = None
    global_index = 0
    for row in sorted_rows:
        global_index += 1
        category_name = primary_category(row)
        account_name = str(row.get("account_nickname") or row.get("account_name") or row.get("fakeid") or "")
        if category_name != current_category:
            current_category = category_name
            current_account = None
            lines.extend([
                f"## 主题：{category_name}",
                "",
            ])
        if account_name != current_account:
            current_account = account_name
            lines.extend([
                f"### 公众号：{account_name}",
                "",
            ])

        item_title = str(row.get("title") or row.get("article_id") or f"文章 {global_index}")
        author_name = str(row.get("author_name") or "").strip()
        publish_time = format_timestamp(int(row.get("create_time") or 0))
        summary = summary_text(row)
        categories = row_categories(row)
        category_text = " / ".join(categories) if categories else "未分类"
        markdown_content = str(row.get("markdown_content") or "").strip() or str(row.get("text_content") or "").strip()
        lines.extend([
            f"#### {global_index}. {item_title}",
            "",
            f"- 标题：{item_title}",
            f"- 来源公众号：{account_name}",
            f"- fakeid：{row.get('fakeid') or ''}",
            f"- 同步策略：{row.get('processing_mode') or 'sync_only'}",
            f"- 主题分类：{category_text}",
            f"- 作者：{author_name or '未知'}",
            f"- 发布时间：{publish_time or '未知'}",
            f"- 摘要：{summary or '无'}",
            f"- 链接：{row.get('link') or ''}",
            "",
            "##### 内容",
            "",
            markdown_content or "无正文内容",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def export_account_report_markdown(
    db: Database,
    fakeid: str = "",
    nickname: str = "",
    article_ids: list[str] | None = None,
    limit: int = 0,
    title: str = "",
    save_file: bool = True,
    include_markdown: bool = True,
) -> dict[str, Any]:
    account = resolve_account_row(db, fakeid=fakeid, nickname=nickname)
    if not account:
        return failure("未找到公众号")
    fakeid_value = str(account.get("fakeid") or "")
    detail_rows = detail_rows_for_account(db, fakeid_value, article_ids=article_ids, limit=limit)
    if not detail_rows:
        return failure("该公众号暂无已抓取详情的文章")
    nickname_value = str(account.get("nickname") or fakeid_value)
    report_title = title.strip() if title.strip() else f"{nickname_value} 详情汇总"
    markdown = render_account_report_markdown(account, detail_rows, report_title)
    report_path = ""
    if save_file:
        report_dir = ensure_dir(get_paths().reports_dir / safe_filename(fakeid_value or nickname_value, fallback="account"))
        timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(now_ts()))
        file_path = report_dir / f"{report_file_basename('account-report', timestamp, fakeid_value or nickname_value)}.md"
        file_path.write_text(markdown, encoding="utf-8")
        report_path = str(file_path)
    data = {
        "fakeid": fakeid_value,
        "nickname": nickname_value,
        "report_title": report_title,
        "report_path": report_path,
        "article_count": len(detail_rows),
        "categories": parse_categories_json(str(account.get("categories_json") or "[]")),
        "articles": [
            {
                "article_id": row.get("article_id") or "",
                "title": row.get("title") or "",
                "source_account": row.get("account_name") or nickname_value,
                "link": row.get("link") or "",
                "summary": summary_text(row),
                "saved_md_path": row.get("saved_md_path") or "",
            }
            for row in detail_rows
        ],
    }
    if include_markdown:
        data["markdown"] = markdown
    return success(data, f"已导出公众号详情汇总: {report_title}")


def export_recent_combined_report_markdown(
    db: Database,
    hours: int = 24,
    limit: int = 200,
    title: str = "",
    save_file: bool = True,
    include_markdown: bool = True,
    only_markdown_accounts: bool = True,
) -> dict[str, Any]:
    detail_rows = detail_rows_for_recent_articles(
        db,
        hours=hours,
        limit=limit,
        only_markdown_accounts=only_markdown_accounts,
    )
    if not detail_rows:
        return failure("最近时间范围内没有可汇总的已抓取详情文章")

    report_title = title.strip() if title.strip() else f"最近{hours}小时公众号文章详情总汇总"
    markdown = render_combined_report_markdown(detail_rows, report_title, hours)
    report_path = ""
    if save_file:
        report_dir = ensure_dir(get_paths().reports_dir / "_combined")
        timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(now_ts()))
        file_path = report_dir / f"{report_file_basename('combined-report', timestamp)}.md"
        file_path.write_text(markdown, encoding="utf-8")
        report_path = str(file_path)

    accounts: dict[str, dict[str, Any]] = {}
    articles: list[dict[str, Any]] = []
    for row in sort_combined_rows(detail_rows):
        fakeid_value = str(row.get("fakeid") or "")
        if fakeid_value and fakeid_value not in accounts:
            accounts[fakeid_value] = {
                "fakeid": fakeid_value,
                "nickname": row.get("account_nickname") or row.get("account_name") or fakeid_value,
                "categories": row_categories(row),
                "processing_mode": row.get("processing_mode") or "sync_only",
            }
        articles.append(
            {
                "article_id": row.get("article_id") or "",
                "fakeid": fakeid_value,
                "title": row.get("title") or "",
                "source_account": row.get("account_nickname") or row.get("account_name") or fakeid_value,
                "categories": row_categories(row),
                "primary_category": primary_category(row),
                "link": row.get("link") or "",
                "summary": summary_text(row),
                "saved_md_path": row.get("saved_md_path") or "",
            }
        )

    data = {
        "report_title": report_title,
        "report_path": report_path,
        "hours": hours,
        "article_count": len(detail_rows),
        "account_count": len(accounts),
        "accounts": list(accounts.values()),
        "articles": articles,
    }
    if include_markdown:
        data["markdown"] = markdown
    return success(data, f"已导出最近 {hours} 小时多公众号合并详情汇总: {report_title}")


def fetch_account_details(
    db: Database,
    fakeid: str = "",
    nickname: str = "",
    article_ids: list[str] | None = None,
    limit: int = 0,
    download_images: bool = True,
    include_html: bool = False,
    force_refresh: bool = False,
    save_files: bool = True,
    export_markdown: bool = False,
    include_report_markdown: bool = False,
    report_title: str = "",
) -> dict[str, Any]:
    account = resolve_account_row(db, fakeid=fakeid, nickname=nickname)
    if not account:
        return failure("未找到公众号")
    fakeid_value = str(account.get("fakeid") or "")
    article_rows = article_rows_for_account(db, fakeid_value, article_ids=article_ids, limit=limit)
    if not article_rows:
        return failure("该公众号暂无可抓取详情的文章")
    succeeded: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    succeeded_ids: list[str] = []
    for row in article_rows:
        result = article_detail(
            db,
            aid=str(row.get("aid") or ""),
            link=str(row.get("link") or ""),
            download_images=download_images,
            include_html=include_html,
            force_refresh=force_refresh,
            save_files=save_files,
        )
        if result.get("success"):
            payload = result.get("data") or {}
            succeeded.append(
                {
                    "article_id": payload.get("article_id") or row.get("id") or "",
                    "title": payload.get("title") or row.get("title") or "",
                    "link": payload.get("link") or row.get("link") or "",
                    "saved_md_path": payload.get("saved_md_path") or "",
                    "cached": bool(payload.get("cached")),
                }
            )
            succeeded_ids.append(str(payload.get("article_id") or row.get("id") or ""))
        else:
            failed.append(
                {
                    "article_id": row.get("id") or "",
                    "title": row.get("title") or "",
                    "link": row.get("link") or "",
                    "error": result.get("error") or "unknown error",
                }
            )
    report_result: dict[str, Any] | None = None
    if export_markdown and succeeded_ids:
        report_result = export_account_report_markdown(
            db,
            fakeid=fakeid_value,
            article_ids=succeeded_ids,
            title=report_title,
            save_file=True,
            include_markdown=include_report_markdown,
        )
    return success(
        {
            "fakeid": fakeid_value,
            "nickname": account.get("nickname") or fakeid_value,
            "requested_count": len(article_rows),
            "success_count": len(succeeded),
            "failed_count": len(failed),
            "details": succeeded,
            "failed": failed,
            "report": report_result.get("data") if report_result and report_result.get("success") else None,
            "report_error": report_result.get("error") if report_result and not report_result.get("success") else "",
        },
        f"已抓取 {len(succeeded)} 篇文章详情",
    )
