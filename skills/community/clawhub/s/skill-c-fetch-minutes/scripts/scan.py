#!/usr/bin/env python3
"""
Skill-C scan：遍历所有受管仓库，返回三类待处理会议。

A 类：status in {scheduled, brief-sent} 且“已结束超过 20 分钟”
  → 只有满足 end_time + 20min < now，才允许进入会后流程
  → 这样即使会前简报漏发，会议结束后也不会卡住整个会后流程
  → 同时避免未开始/刚结束会议被误判

B 类：status == waiting-transcript
  → OpenClaw 判断是否超时（>60分钟），超时则 set-failed；
    否则三层降级拉取转录，成功则 AI 抽取 + commit-content

C 类：status == transcript-failed 且 transcript.md 已存在
  → 组织者已手动上传，OpenClaw 直接读取内容做 AI 抽取 + commit-content

用法：
    python3 scan.py
"""

import os
import sys
import json
from datetime import datetime, timedelta

import pytz
import yaml
from dateutil.parser import parse as parse_dt
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.config/skill-c-fetch-minutes/.env"))

sys.path.insert(0, os.path.dirname(__file__))
from gitea_utils import (
    get_managed_repos,
    list_meetings_in_repo,
    get_file_from_repo,
    file_exists_in_repo,
    get_user_email,
    get_repo_member_usernames,
)

GITEA_BASE_URL = os.getenv("GITEA_BASE_URL", "")
GITEA_TOKEN    = os.getenv("GITEA_TOKEN_BOT", "")
TZ             = pytz.timezone("Asia/Shanghai")

# 会议结束后再额外等待 20 分钟，才允许进入会后流程
POST_MEETING_GRACE_MINUTES = 20


def parse_time_or_none(time_str):
    """解析 ISO8601 时间，失败返回 None。"""
    if not time_str:
        return None
    try:
        dt = parse_dt(time_str)
        if dt.tzinfo is None:
            dt = TZ.localize(dt)
        return dt.astimezone(TZ)
    except Exception:
        return None


def get_organizer_email(meta, owner, repo_name):
    """获取组织者邮箱；找不到时 fallback 到 owner 邮箱。"""
    organizer = meta.get("organizer", "")
    if organizer:
        email = get_user_email(organizer, GITEA_TOKEN, GITEA_BASE_URL)
        if email:
            return email
    return get_user_email(owner, GITEA_TOKEN, GITEA_BASE_URL)


def get_attendee_emails(attendees, owner, repo_name):
    if not attendees:
        attendees = get_repo_member_usernames(owner, repo_name, GITEA_TOKEN, GITEA_BASE_URL)
    return [
        e for e in (
            get_user_email(u, GITEA_TOKEN, GITEA_BASE_URL) for u in attendees
        ) if e
    ]


def build_postprocess_timing(meta):
    """
    计算会议结束与是否允许进入会后流程。
    返回：
      {
        "scheduled_dt": datetime|None,
        "duration_minutes": int,
        "end_dt": datetime|None,
        "ready_after_dt": datetime|None,
        "ready_for_postprocess": bool,
      }
    """
    scheduled_dt = parse_time_or_none(meta.get("scheduled_time", ""))
    try:
        duration_minutes = int(meta.get("duration_minutes", 60) or 60)
    except Exception:
        duration_minutes = 60

    if scheduled_dt is None:
        return {
            "scheduled_dt": None,
            "duration_minutes": duration_minutes,
            "end_dt": None,
            "ready_after_dt": None,
            "ready_for_postprocess": False,
        }

    end_dt = scheduled_dt + timedelta(minutes=duration_minutes)
    ready_after_dt = end_dt + timedelta(minutes=POST_MEETING_GRACE_MINUTES)
    now = datetime.now(TZ)

    return {
        "scheduled_dt": scheduled_dt,
        "duration_minutes": duration_minutes,
        "end_dt": end_dt,
        "ready_after_dt": ready_after_dt,
        "ready_for_postprocess": now > ready_after_dt,
    }


def make_meeting_record(full_name, dir_name, meta, owner, repo_name, extra=None):
    """构造统一格式的会议记录供 OpenClaw 使用。"""
    attendees = meta.get("attendees") or get_repo_member_usernames(
        owner, repo_name, GITEA_TOKEN, GITEA_BASE_URL
    )

    timing = build_postprocess_timing(meta)

    record = {
        "repo":              full_name,
        "meeting_dir":       dir_name,
        "topic":             meta.get("topic", ""),
        "scheduled_time":    meta.get("scheduled_time", ""),
        "duration_minutes":  timing["duration_minutes"],
        "meeting_id":        meta.get("meeting_id", ""),
        "meeting_code":      meta.get("meeting_code", ""),
        "join_url":          meta.get("join_url", ""),
        "organizer":         meta.get("organizer", ""),
        "organizer_email":   get_organizer_email(meta, owner, repo_name),
        "attendees":         attendees,
        "attendee_emails":   get_attendee_emails(attendees, owner, repo_name),
        "category":          meta.get("meeting_category", "single"),
        "status":            meta.get("status", ""),
        "meeting_end_time":  timing["end_dt"].isoformat() if timing["end_dt"] else "",
        "ready_after_time":  timing["ready_after_dt"].isoformat() if timing["ready_after_dt"] else "",
        "ready_for_postprocess": timing["ready_for_postprocess"],
        "postprocess_grace_minutes": POST_MEETING_GRACE_MINUTES,
    }
    if extra:
        record.update(extra)
    return record


def scan_repo(full_name):
    owner, repo_name = full_name.split("/", 1)
    dirs = list_meetings_in_repo(owner, repo_name, GITEA_TOKEN, GITEA_BASE_URL)

    class_a, class_b, class_c = [], [], []

    for dir_name in dirs:
        if "__rescheduled" in dir_name:
            continue

        raw, _ = get_file_from_repo(
            owner, repo_name, f"meetings/{dir_name}/meta.yaml",
            GITEA_TOKEN, GITEA_BASE_URL,
        )
        if not raw:
            continue

        try:
            meta = yaml.safe_load(raw) or {}
        except Exception:
            continue

        status = meta.get("status", "")
        timing = build_postprocess_timing(meta)

        # ── A 类：scheduled / brief-sent，但必须已经结束超过 20 分钟 ─────────
        if status in {"scheduled", "brief-sent"}:
            if not timing["ready_for_postprocess"]:
                continue
            class_a.append(make_meeting_record(full_name, dir_name, meta, owner, repo_name))

        # ── B 类：waiting-transcript ──────────────────────────────────────────
        elif status == "waiting-transcript":
            class_b.append(make_meeting_record(
                full_name, dir_name, meta, owner, repo_name,
                extra={
                    "transcript_started_at": meta.get("transcript_started_at", ""),
                    "transcript_poll_count": meta.get("transcript_poll_count", 0),
                },
            ))

        # ── C 类：transcript-failed + transcript.md 已存在 ─────────────────────
        elif status == "transcript-failed":
            transcript_exists = file_exists_in_repo(
                owner, repo_name,
                f"meetings/{dir_name}/transcript.md",
                GITEA_TOKEN, GITEA_BASE_URL,
            )
            if transcript_exists:
                transcript_content, _ = get_file_from_repo(
                    owner, repo_name,
                    f"meetings/{dir_name}/transcript.md",
                    GITEA_TOKEN, GITEA_BASE_URL,
                )
                class_c.append(make_meeting_record(
                    full_name, dir_name, meta, owner, repo_name,
                    extra={"transcript_content": transcript_content or ""},
                ))

    return class_a, class_b, class_c


def main():
    if not GITEA_BASE_URL or not GITEA_TOKEN:
        print(json.dumps({
            "error": "缺少 Gitea 配置，请检查 ~/.config/skill-c-fetch-minutes/.env",
            "class_a": [], "class_b": [], "class_c": [],
        }, ensure_ascii=False))
        sys.exit(1)

    repos = get_managed_repos(GITEA_TOKEN, GITEA_BASE_URL)
    all_a, all_b, all_c = [], [], []
    errors = []

    for full_name in repos:
        try:
            a, b, c = scan_repo(full_name)
            all_a.extend(a)
            all_b.extend(b)
            all_c.extend(c)
        except Exception as e:
            errors.append({"repo": full_name, "error": str(e)})

    print(json.dumps({
        "class_a":       all_a,
        "class_b":       all_b,
        "class_c":       all_c,
        "count_a":       len(all_a),
        "count_b":       len(all_b),
        "count_c":       len(all_c),
        "scanned_repos": len(repos),
        "errors":        errors,
        "scan_time":     datetime.now(TZ).isoformat(),
        "postprocess_grace_minutes": POST_MEETING_GRACE_MINUTES,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()