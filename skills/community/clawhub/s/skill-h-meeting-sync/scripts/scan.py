#!/usr/bin/env python3
"""
Skill-H scan：遍历所有受管仓库，汇总 status ∈ {scheduled, brief-sent} 的活跃会议。
返回供 OpenClaw 与腾讯会议列表做三向对比的数据。

用法：
    python3 scan.py
"""

import os
import sys
import json
from datetime import datetime

import pytz
import yaml
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.config/skill-h-meeting-sync/.env"))

sys.path.insert(0, os.path.dirname(__file__))
from gitea_utils import (
    get_managed_repos,
    list_meetings_in_repo,
    get_file_from_repo,
    get_user_email,
    get_repo_member_usernames,
)

GITEA_BASE_URL = os.getenv("GITEA_BASE_URL", "")
GITEA_TOKEN    = os.getenv("GITEA_TOKEN_BOT", "")
TZ             = pytz.timezone("Asia/Shanghai")

ACTIVE_STATUSES = {"scheduled", "brief-sent"}


def get_attendee_emails(attendees, owner, repo_name):
    emails = []
    for username in (attendees or []):
        email = get_user_email(username, GITEA_TOKEN, GITEA_BASE_URL)
        if email:
            emails.append(email)
    return emails


def scan_repo(full_name):
    owner, repo_name = full_name.split("/", 1)
    dirs = list_meetings_in_repo(owner, repo_name, GITEA_TOKEN, GITEA_BASE_URL)
    results = []

    for dir_name in dirs:
        # 已归档或改期存档目录跳过（状态不是 active）
        if "__rescheduled" in dir_name:
            continue

        meta_raw, _ = get_file_from_repo(
            owner, repo_name, f"meetings/{dir_name}/meta.yaml",
            GITEA_TOKEN, GITEA_BASE_URL,
        )
        if not meta_raw:
            continue

        try:
            meta = yaml.safe_load(meta_raw) or {}
        except Exception:
            continue

        status = meta.get("status", "")
        if status not in ACTIVE_STATUSES:
            continue

        attendees = meta.get("attendees") or get_repo_member_usernames(
            owner, repo_name, GITEA_TOKEN, GITEA_BASE_URL
        )
        attendee_emails = get_attendee_emails(attendees, owner, repo_name)

        results.append({
            "repo":            full_name,
            "meeting_dir":     dir_name,
            "meeting_id":      meta.get("meeting_id", ""),
            "meeting_code":    meta.get("meeting_code", ""),
            "topic":           meta.get("topic", ""),
            "scheduled_time":  meta.get("scheduled_time", ""),
            "duration_minutes":meta.get("duration_minutes", 60),
            "status":          status,
            "type":            meta.get("type", "ad-hoc"),
            "meeting_category":meta.get("meeting_category", "single"),
            "series_id":       meta.get("series_id"),
            "organizer":       meta.get("organizer", ""),
            "attendees":       attendees,
            "attendee_emails": attendee_emails,
            "join_url":        meta.get("join_url", ""),
        })

    return results


def main():
    if not GITEA_BASE_URL or not GITEA_TOKEN:
        print(json.dumps({
            "error": "缺少 Gitea 配置，请检查 ~/.config/skill-h-meeting-sync/.env",
            "gitea_meetings": [],
        }, ensure_ascii=False))
        sys.exit(1)

    repos = get_managed_repos(GITEA_TOKEN, GITEA_BASE_URL)
    all_meetings = []
    errors = []

    for full_name in repos:
        try:
            hits = scan_repo(full_name)
            all_meetings.extend(hits)
        except Exception as e:
            errors.append({"repo": full_name, "error": str(e)})

    print(json.dumps({
        "scanned_repos":  len(repos),
        "gitea_meetings": all_meetings,
        "count":          len(all_meetings),
        "errors":         errors,
        "scan_time":      datetime.now(TZ).isoformat(),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
