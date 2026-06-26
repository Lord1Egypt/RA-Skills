#!/usr/bin/env python3
"""
Incremental monitor - 增量监听回复，支持按 campaign 过滤

修复记录：
- P0-1: is_read=0 改为 is_reply=0（未回复判定）+ last_scan_time 增量时间过滤
  原因：只扫未读会漏掉用户已读的未回复邮件；改用 is_reply=0 后配合时间戳增量，
        确保每轮只拉取自上次扫描后新增的回复，不重不漏。
"""
import json
from datetime import datetime, timezone
from typing import Any, Optional

import inbox
from common import get_token, state_file


def get_last_scan_time(campaign_id: str) -> Optional[str]:
    """获取上次扫描时间"""
    scan_log_path = state_file(f"scan_log_{campaign_id}.json")
    if scan_log_path.exists():
        data = json.loads(scan_log_path.read_text())
        return data.get("last_scan_time")
    return None


def save_scan_time(campaign_id: str, timestamp: str):
    """保存扫描时间"""
    scan_log_path = state_file(f"scan_log_{campaign_id}.json")
    data = {"last_scan_time": timestamp}
    scan_log_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def get_processed_reply_ids(campaign_id: str) -> set[str]:
    """获取本 campaign 已处理过的邮件ID集合"""
    processed_path = state_file(f"processed_replies_{campaign_id}.json")
    if processed_path.exists():
        data = json.loads(processed_path.read_text())
        return set(data.get("processed_ids", []))
    return set()


def add_processed_reply_ids(campaign_id: str, reply_ids: list[str]):
    """追加已处理邮件ID"""
    processed_path = state_file(f"processed_replies_{campaign_id}.json")
    existing = get_processed_reply_ids(campaign_id)
    updated = existing | {str(r) for r in reply_ids if r}
    processed_path.write_text(json.dumps({"processed_ids": list(updated)}, ensure_ascii=False, indent=2))


def get_new_replies(
    token: str,
    campaign_id: str,
    contacted_blogger_ids: set[str],
    page_size: int = 50,
) -> list[dict[str, Any]]:
    """获取新回复（只返回来自已邀约达人的、未处理过的增量回复）"""
    last_time = get_last_scan_time(campaign_id)
    processed_ids = get_processed_reply_ids(campaign_id)

    # P0 fix: 改 is_read=0 → is_reply=0（未回复），查到所有未回复邮件
    # 再按时间戳和已处理状态做增量过滤
    inbox_resp = inbox.list_inbox(
        token,
        current_page=1,
        page_size=page_size,
        is_reply=0,   # 未回复（不只是未读）
        time_range=3,  # 全量时间
    )

    records = inbox_resp.get("data", {}).get("records", [])
    if not records:
        return []

    last_ts = None
    if last_time:
        try:
            last_ts = datetime.fromisoformat(last_time.replace("Z", "+00:00"))
        except Exception:
            last_ts = None

    new_replies = []
    new_reply_ids = []
    for mail in records:
        blogger_id = mail.get("bloggerId") or mail.get("bEsId") or ""
        if blogger_id not in contacted_blogger_ids:
            continue

        email_id = str(mail.get("id") or "")
        if email_id in processed_ids:
            continue

        # 时间戳增量过滤
        create_time_str = mail.get("createTime") or ""
        if last_ts and create_time_str:
            try:
                create_ts = datetime.fromisoformat(create_time_str.replace("Z", "+00:00"))
                if create_ts <= last_ts:
                    continue
            except Exception:
                pass

        new_replies.append({
            "emailId": email_id,
            "chatId": mail.get("chatId"),
            "bloggerId": blogger_id,
            "bloggerName": mail.get("bloggerName") or mail.get("nickname") or "",
            "subject": mail.get("subject", ""),
            "content": mail.get("cleanContent") or mail.get("content") or "",
            "createTime": create_time_str,
        })
        if email_id:
            new_reply_ids.append(email_id)

    # 记录本次扫描时间戳和已处理ID
    save_scan_time(campaign_id, datetime.now(timezone.utc).isoformat())
    if new_reply_ids:
        add_processed_reply_ids(campaign_id, new_reply_ids)

    return new_replies


def monitor_campaign_replies(
    token: str,
    campaign_id: str,
    contacted_blogger_ids: set[str],
    page_size: int = 50,
) -> dict[str, Any]:
    """监听 campaign 的回复"""
    replies = get_new_replies(token, campaign_id, contacted_blogger_ids, page_size)

    return {
        "campaign_id": campaign_id,
        "new_replies_count": len(replies),
        "replies": replies,
    }
