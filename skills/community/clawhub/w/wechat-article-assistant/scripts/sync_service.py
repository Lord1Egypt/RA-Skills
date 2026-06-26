#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manual sync and scheduled sync entrypoints."""

from __future__ import annotations

import subprocess
import time

from article_service import export_recent_combined_report_markdown, fetch_account_details, upsert_articles
from database import Database
from log_utils import get_logger
from mp_client import WechatLoginExpiredError, WechatRequestError
from session_store import update_login_validation
from utils import failure, now_ts, success


LOGGER = get_logger(__name__)


def _format_sync_error(message: str) -> tuple[str, str | None]:
    normalized = str(message or "").strip()
    if normalized.lower() == "invalid session":
        return "登录状态已失效，请重新登录后再同步", normalized
    return normalized, None


def _account_name(db: Database, fakeid: str) -> str:
    row = db.row("SELECT nickname FROM account WHERE fakeid = ?", (fakeid,))
    return str((row or {}).get("nickname") or fakeid)


def _account_processing_config(db: Database, fakeid: str) -> dict:
    return db.row(
        "SELECT processing_mode, auto_export_markdown FROM account WHERE fakeid = ?",
        (fakeid,),
    ) or {}


def _log_sync(db: Database, fakeid: str, status: str, message: str, articles_synced: int, started_at: int, finished_at: int) -> None:
    db.execute(
        """
        INSERT INTO sync_log (fakeid, nickname, status, message, articles_synced, started_at, finished_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            fakeid,
            _account_name(db, fakeid),
            status,
            message,
            articles_synced,
            started_at,
            finished_at,
            finished_at,
        ),
    )


def _update_sync_status(db: Database, fakeid: str, status: str, message: str) -> None:
    db.execute(
        """
        UPDATE sync_config
        SET last_sync_at = ?, last_sync_status = ?, last_sync_message = ?, updated_at = ?
        WHERE fakeid = ?
        """,
        (now_ts(), status, message, now_ts(), fakeid),
    )


def _run_post_sync_processing(db: Database, fakeid: str, new_article_ids: list[str]) -> dict | None:
    if not new_article_ids:
        return None
    config = _account_processing_config(db, fakeid)
    processing_mode = str(config.get("processing_mode") or "sync_only").strip().lower()
    if processing_mode != "sync_and_detail":
        return None

    result = fetch_account_details(
        db,
        fakeid=fakeid,
        article_ids=new_article_ids,
        download_images=True,
        include_html=False,
        force_refresh=False,
        save_files=True,
        export_markdown=False,
        include_report_markdown=False,
    )
    if not result.get("success"):
        LOGGER.warning("post_sync_processing failed fakeid=%s error=%s", fakeid, result.get("error"))
    return result


def _should_generate_combined_report(db: Database, fakeid: str, post_process: dict | None) -> bool:
    if not post_process or not post_process.get("success"):
        return False
    payload = post_process.get("data") or {}
    if int(payload.get("success_count") or 0) <= 0:
        return False
    config = _account_processing_config(db, fakeid)
    return bool(int(config.get("auto_export_markdown") or 0))


def _generate_combined_report(db: Database, hours: int = 24) -> dict | None:
    result = export_recent_combined_report_markdown(
        db,
        hours=hours,
        limit=500,
        save_file=True,
        include_markdown=False,
        only_markdown_accounts=True,
    )
    if not result.get("success"):
        LOGGER.warning("combined_report_export failed error=%s", result.get("error"))
    return result


def _notify_enabled(channel: str = "", target: str = "", account: str = "") -> bool:
    return bool(str(channel or "").strip() and str(target or "").strip() and str(account or "").strip())


def _send_progress_message(message: str, channel: str = "", target: str = "", account: str = "") -> bool:
    if not _notify_enabled(channel=channel, target=target, account=account):
        return False
    command = [
        "openclaw",
        "message",
        "send",
        "--channel",
        str(channel).strip(),
        "--target",
        str(target).strip(),
        "--account",
        str(account).strip(),
        "-m",
        str(message or "").strip(),
        "--json",
    ]
    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
    except Exception as exc:
        LOGGER.warning("progress notification failed to start error=%s", exc)
        return False
    if completed.returncode != 0:
        LOGGER.warning(
            "progress notification failed exit=%s stdout=%s stderr=%s",
            completed.returncode,
            (completed.stdout or "").strip(),
            (completed.stderr or "").strip(),
        )
        return False
    LOGGER.info("progress notification sent channel=%s target=%s", channel, target)
    return True


def _build_progress_message(account_name: str, index: int, total: int, result: dict) -> str:
    if result.get("success"):
        payload = result.get("data") or {}
        synced_count = int(payload.get("articles_synced") or 0)
        return f"{account_name}公众号完成，进度{index}/{total}。状态：成功；新增文章 {synced_count} 篇。"
    error = str(result.get("error") or "同步失败").strip()
    return f"{account_name}公众号完成，进度{index}/{total}。状态：失败；原因：{error}。"


def _build_login_expired_message(account_name: str, index: int, total: int) -> str:
    return (
        f"{account_name}公众号同步失败，进度{index}/{total}。"
        "检测到公众号登录已过期，已停止后续同步，请重新扫码登录公众号后台。"
    )


def _validate_login_before_sync(db: Database) -> tuple[bool, str]:
    from mp_client import WechatMPClient

    client = WechatMPClient(db)
    try:
        validated = client.validate_login()
        update_login_validation(
            db,
            True,
            nickname=str(validated.get("nickname") or ""),
            head_img=str(validated.get("head_img") or ""),
        )
        return True, ""
    except WechatLoginExpiredError:
        update_login_validation(db, False)
        return False, "登录状态已过期，请重新登录后再同步"
    except WechatRequestError as exc:
        LOGGER.warning("preflight login validation skipped due to request error=%s", exc)
        return True, ""


def sync_account(db: Database, fakeid: str, max_pages: int | None = None, page_size: int = 5, extra_pages_after_existing: int = 1) -> dict:
    started_at = now_ts()
    from mp_client import WechatMPClient

    LOGGER.info(
        "sync_account start fakeid=%s max_pages=%s page_size=%s extra_pages_after_existing=%s",
        fakeid,
        max_pages,
        page_size,
        extra_pages_after_existing,
    )
    client = WechatMPClient(db)
    known_ids = {row["id"] for row in db.rows("SELECT id FROM article WHERE fakeid = ?", (fakeid,))}
    queued_ids: set[str] = set()

    all_new = []
    total_count = 0
    pages_fetched = 0
    existing_hit_page: int | None = None
    try:
        validated = client.validate_login()
        update_login_validation(
            db,
            True,
            nickname=str(validated.get("nickname") or ""),
            head_img=str(validated.get("head_img") or ""),
        )
        page_index = 0
        while True:
            if max_pages and page_index >= max_pages:
                break
            begin = page_index * page_size
            payload = client.fetch_article_page(fakeid=fakeid, begin=begin, count=page_size)
            total_count = int(payload.get("total_count") or total_count)
            remote_articles = payload.get("articles") or []
            LOGGER.debug(
                "sync_account page fakeid=%s page_index=%s begin=%s remote_articles=%s total_count=%s",
                fakeid,
                page_index,
                begin,
                len(remote_articles),
                total_count,
            )
            if not remote_articles:
                break

            found_existing = False
            for article in remote_articles:
                aid = str(article.get("aid") or f"{article.get('appmsgid', 0)}_{article.get('itemidx', 1)}")
                article_id = f"{fakeid}:{aid}"
                if article_id in known_ids:
                    found_existing = True
                    continue
                if article_id in queued_ids:
                    continue
                queued_ids.add(article_id)
                all_new.append(article)
            pages_fetched += 1
            if found_existing and existing_hit_page is None:
                existing_hit_page = page_index
            if existing_hit_page is not None and page_index - existing_hit_page >= max(0, extra_pages_after_existing):
                break
            if total_count and begin + page_size >= total_count:
                break
            page_index += 1

        saved = upsert_articles(db, fakeid, all_new)
        synced_count = len(saved)
        new_article_ids = [f"{fakeid}:{item['aid']}" for item in saved]
        db.execute(
            """
            UPDATE account
            SET total_count = ?, articles_synced = articles_synced + ?, last_sync_at = ?, updated_at = ?
            WHERE fakeid = ?
            """,
            (total_count, synced_count, now_ts(), now_ts(), fakeid),
        )
        post_process = _run_post_sync_processing(db, fakeid, new_article_ids)
        combined_report = _generate_combined_report(db, hours=24) if _should_generate_combined_report(db, fakeid, post_process) else None
        message = f"同步完成，新增 {synced_count} 篇文章"
        LOGGER.info(
            "sync_account success fakeid=%s synced_count=%s total_count=%s pages_fetched=%s",
            fakeid,
            synced_count,
            total_count,
            pages_fetched,
        )
        _update_sync_status(db, fakeid, "success", message)
        _log_sync(db, fakeid, "success", message, synced_count, started_at, now_ts())
        return success(
            {
                "fakeid": fakeid,
                "articles_synced": synced_count,
                "new_article_ids": new_article_ids,
                "total_count": total_count,
                "pages_fetched": pages_fetched,
                "existing_hit_page": existing_hit_page,
                "extra_pages_after_existing": max(0, extra_pages_after_existing),
                "post_process": post_process.get("data") if post_process and post_process.get("success") else None,
                "post_process_error": post_process.get("error") if post_process and not post_process.get("success") else "",
                "combined_report": combined_report.get("data") if combined_report and combined_report.get("success") else None,
                "combined_report_error": combined_report.get("error") if combined_report and not combined_report.get("success") else "",
                "message": message,
            },
            message,
        )
    except WechatLoginExpiredError as exc:
        message = "登录状态已过期，请重新登录后再同步"
        request_debug = client.get_last_request_debug()
        LOGGER.warning("sync_account login expired fakeid=%s error=%s raw_error=%s", fakeid, message, str(exc))
        update_login_validation(db, False)
        _update_sync_status(db, fakeid, "failed", message)
        _log_sync(db, fakeid, "failed", message, 0, started_at, now_ts())
        data = {
            "fakeid": fakeid,
            "original_error": str(exc),
            "login_expired": True,
        }
        if request_debug:
            data["request_debug"] = request_debug
        return failure(message, data)
    except WechatRequestError as exc:
        raw_message = str(exc)
        message, original_error = _format_sync_error(raw_message)
        request_debug = client.get_last_request_debug()
        LOGGER.warning("sync_account failed fakeid=%s error=%s raw_error=%s", fakeid, message, raw_message)
        _update_sync_status(db, fakeid, "failed", message)
        _log_sync(db, fakeid, "failed", message, 0, started_at, now_ts())
        data = {"fakeid": fakeid}
        if original_error:
            data["original_error"] = original_error
        if request_debug:
            data["request_debug"] = request_debug
        return failure(message, data)


def sync_all(db: Database, interval_seconds: int = 0, channel: str = "", target: str = "", account: str = "") -> dict:
    targets = db.rows("SELECT fakeid FROM sync_config WHERE enabled = 1 ORDER BY fakeid")
    interval_seconds = max(0, int(interval_seconds or 0))
    LOGGER.info(
        "sync_all targets=%s interval_seconds=%s notify=%s",
        len(targets),
        interval_seconds,
        _notify_enabled(channel=channel, target=target, account=account),
    )
    login_valid, login_message = _validate_login_before_sync(db)
    if not login_valid:
        _send_progress_message(login_message, channel=channel, target=target, account=account)
        return failure(
            login_message,
            {
                "total": len(targets),
                "success": 0,
                "failed": 0,
                "interval_seconds": interval_seconds,
                "results": [],
                "login_expired": True,
            },
        )

    results = []
    success_count = 0
    should_generate_combined_report = False
    stopped_due_to_login_expired = False
    for index, item in enumerate(targets, start=1):
        fakeid = str(item["fakeid"])
        account_name = _account_name(db, fakeid)
        result = sync_account(db, fakeid)
        results.append(result)
        if result.get("success"):
            success_count += 1
            payload = result.get("data") or {}
            post_process = payload.get("post_process") or {}
            if int(post_process.get("success_count") or 0) > 0:
                should_generate_combined_report = True
            _send_progress_message(
                _build_progress_message(account_name, index, len(targets), result),
                channel=channel,
                target=target,
                account=account,
            )
        else:
            payload = result.get("data") or {}
            if bool(payload.get("login_expired")):
                stopped_due_to_login_expired = True
                _send_progress_message(
                    _build_login_expired_message(account_name, index, len(targets)),
                    channel=channel,
                    target=target,
                    account=account,
                )
                break
            _send_progress_message(
                _build_progress_message(account_name, index, len(targets), result),
                channel=channel,
                target=target,
                account=account,
            )
        if interval_seconds > 0 and index < len(targets):
            LOGGER.info("sync_all sleep interval_seconds=%s before_next=%s", interval_seconds, targets[index]["fakeid"])
            time.sleep(interval_seconds)
    combined_report = _generate_combined_report(db, hours=24) if should_generate_combined_report else None
    failed_count = len(results) - success_count
    payload = {
        "total": len(targets),
        "success": success_count,
        "failed": failed_count,
        "interval_seconds": interval_seconds,
        "results": results,
        "combined_report": combined_report.get("data") if combined_report and combined_report.get("success") else None,
        "combined_report_error": combined_report.get("error") if combined_report and not combined_report.get("success") else "",
        "stopped_due_to_login_expired": stopped_due_to_login_expired,
        "notify": {
            "channel": channel,
            "target": target,
            "account": account,
        },
    }
    if stopped_due_to_login_expired:
        return failure("同步过程中检测到登录已过期，已停止后续同步", payload)
    return success(
        payload,
        f"批量同步完成，共 {len(targets)} 个公众号，成功 {success_count} 个",
    )


def sync_due(db: Database, grace_minutes: int = 3) -> dict:
    now = now_ts()
    now_struct = time.localtime(now)
    now_minute_of_day = int(now_struct.tm_hour) * 60 + int(now_struct.tm_min)
    grace_minutes = max(0, int(grace_minutes or 0))
    targets = db.rows("SELECT * FROM sync_config WHERE enabled = 1 ORDER BY fakeid")
    due_targets = []
    results = []
    should_generate_combined_report = False
    LOGGER.debug("sync_due checking enabled_targets=%s grace_minutes=%s", len(targets), grace_minutes)

    for item in targets:
        scheduled_minute_of_day = int(item.get("sync_hour") or 0) * 60 + int(item.get("sync_minute") or 0)
        delta = now_minute_of_day - scheduled_minute_of_day
        if delta < 0 or delta > grace_minutes:
            continue

        last_sync_at = item.get("last_sync_at")
        if last_sync_at:
            struct = time.localtime(int(last_sync_at))
            if struct.tm_year == now_struct.tm_year and struct.tm_yday == now_struct.tm_yday:
                last_sync_minute_of_day = int(struct.tm_hour) * 60 + int(struct.tm_min)
                if last_sync_minute_of_day >= scheduled_minute_of_day:
                    continue
        due_targets.append(item)

    for target in due_targets:
        result = sync_account(db, target["fakeid"])
        results.append(result)
        if result.get("success"):
            payload = result.get("data") or {}
            post_process = payload.get("post_process") or {}
            if int(post_process.get("success_count") or 0) > 0:
                should_generate_combined_report = True

    combined_report = _generate_combined_report(db, hours=24) if should_generate_combined_report else None
    return success(
        {
            "checked": len(targets),
            "due": len(due_targets),
            "grace_minutes": grace_minutes,
            "results": results,
            "combined_report": combined_report.get("data") if combined_report and combined_report.get("success") else None,
            "combined_report_error": combined_report.get("error") if combined_report and not combined_report.get("success") else "",
        },
        f"按计划同步完成，本次处理 {len(due_targets)} 个公众号",
    )


def sync_logs(db: Database, fakeid: str = "", limit: int = 50) -> dict:
    LOGGER.debug("sync_logs fakeid=%s limit=%s", fakeid, limit)
    if fakeid:
        rows = db.rows(
            """
            SELECT * FROM sync_log
            WHERE fakeid = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (fakeid, limit),
        )
    else:
        rows = db.rows(
            """
            SELECT * FROM sync_log
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        )
    return success(
        {
            "total": len(rows),
            "logs": rows,
        },
        f"共查询到 {len(rows)} 条同步日志",
    )
