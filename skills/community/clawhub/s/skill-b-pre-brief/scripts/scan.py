#!/usr/bin/env python3
"""
Skill-B scan：遍历所有受管仓库，找出需要在 [now+15min, now+6h] 内发送会前简报的会议。

对每场命中会议：
  - 计算 Gitea 活动时间窗口（since / until）
  - 解析参会人邮箱
  - 返回 report_params 供 OpenClaw 调用 gitea-routine-report

时间窗口规则：
  - 循环会议（recurring）：找同 series_id 的上次会议时间 → 现在
  - 临时会议（ad-hoc）：找同仓库最近一次任意会议时间 → 现在
  - 找不到历史记录：now - 7天 → 现在（fallback）

改期会议（含 rescheduled_from 字段）：action=mark_only，不生成简报。

用法：
    python3 scan.py
"""

import os
import sys
import json
from datetime import datetime, timedelta

import pytz
import yaml
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.config/skill-b-pre-brief/.env"))

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

# 简报发送时间窗口：会议开始前 15 分钟至 6 小时内
WINDOW_MIN = timedelta(minutes=15)
WINDOW_MAX = timedelta(hours=6)

# 找不到历史会议时的默认回溯时间
FALLBACK_DAYS = 7


# ──────────────────────────────────────────────────────────────────────────────

def parse_meeting_time(time_str):
    """解析 meta.yaml 中的 scheduled_time，返回带时区的 datetime。"""
    from dateutil.parser import parse as parse_dt
    dt = parse_dt(time_str)
    if dt.tzinfo is None:
        dt = TZ.localize(dt)
    return dt.astimezone(TZ)


def dir_name_to_time(dir_name):
    """
    将会议目录名 YYYY-MM-DD-HHMM 转换为 datetime。
    解析失败返回 None。
    """
    try:
        parts = dir_name.split("-")
        # 格式：2026-04-22-1500 → parts = ['2026', '04', '22', '1500']
        date_str = f"{parts[0]}-{parts[1]}-{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        return TZ.localize(dt)
    except Exception:
        return None


def find_last_meeting_time(owner, repo_name, current_dir, meeting_type, series_id):
    """
    在同仓库历史会议中，找到最近一次满足条件的会议结束时间（或开始时间）。
    用于确定本次 Gitea 活动统计的 since 时间。

    循环会议：找同 series_id 的上次会议。
    临时会议：找同仓库最近一次任意会议（不含当前）。

    返回 datetime（带时区），找不到返回 None。
    """
    dirs = sorted(
        list_meetings_in_repo(owner, repo_name, GITEA_TOKEN, GITEA_BASE_URL),
        reverse=True,  # 从最新到最旧
    )

    for dir_name in dirs:
        # 跳过当前会议自身
        if dir_name == current_dir:
            continue
        # 跳过改期存档目录
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

        # 循环会议：必须同 series_id
        if meeting_type == "recurring" and series_id:
            if meta.get("series_id") != series_id:
                continue

        # 取会议时间
        sched = meta.get("scheduled_time")
        if not sched:
            # 从目录名推断
            dt = dir_name_to_time(dir_name)
        else:
            try:
                dt = parse_meeting_time(sched)
            except Exception:
                dt = dir_name_to_time(dir_name)

        if dt:
            return dt

    return None


def get_attendee_emails(attendees, owner, repo_name):
    """
    解析参会人邮箱列表。
    attendees 若为空，则自动取仓库成员。
    """
    if not attendees:
        attendees = get_repo_member_usernames(owner, repo_name, GITEA_TOKEN, GITEA_BASE_URL)

    emails = []
    for username in attendees:
        email = get_user_email(username, GITEA_TOKEN, GITEA_BASE_URL)
        if email:
            emails.append(email)

    return emails


def format_date(dt):
    """格式化为 YYYY-MM-DD（供 gitea-routine-report 使用）。"""
    return dt.strftime("%Y-%m-%d")


# ──────────────────────────────────────────────────────────────────────────────

def scan_repo(full_name):
    """
    扫描单个仓库，返回命中的会议列表（可能为空）。
    """
    owner, repo_name = full_name.split("/", 1)
    now = datetime.now(TZ)
    window_start = now + WINDOW_MIN   # 15 分钟后
    window_end   = now + WINDOW_MAX   # 6 小时后

    dirs = list_meetings_in_repo(owner, repo_name, GITEA_TOKEN, GITEA_BASE_URL)
    results = []

    for dir_name in dirs:
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

        # 只处理 scheduled 状态
        if meta.get("status") != "scheduled":
            continue

        # 解析会议时间
        sched_str = meta.get("scheduled_time")
        if not sched_str:
            continue
        try:
            meeting_time = parse_meeting_time(sched_str)
        except Exception:
            continue

        # 检查是否在发送窗口内 [now+15min, now+6h]
        if not (window_start <= meeting_time <= window_end):
            continue

        # 改期会议（含 rescheduled_from）：只更新状态，不发简报
        if meta.get("rescheduled_from"):
            results.append({
                "action":         "mark_only",
                "repo":           full_name,
                "meeting_dir":    dir_name,
                "topic":          meta.get("topic", ""),
                "scheduled_time": meeting_time.isoformat(),
                "reason":         "rescheduled_from present, skip brief",
            })
            continue

        # ── 计算 Gitea 活动时间窗口 ─────────────────────────────────────────

        meeting_type = meta.get("type", "ad-hoc")
        series_id    = meta.get("series_id")
        attendees    = meta.get("attendees", [])
        organizer    = meta.get("organizer", "")

        last_meeting_time = find_last_meeting_time(
            owner, repo_name, dir_name, meeting_type, series_id
        )

        if last_meeting_time:
            since_dt = last_meeting_time
        else:
            # 没有历史会议，fallback：最近 7 天
            since_dt = now - timedelta(days=FALLBACK_DAYS)

        until_dt = now  # 统计到现在

        # ── 参会人邮箱 ───────────────────────────────────────────────────────

        attendee_emails = get_attendee_emails(attendees, owner, repo_name)

        # 如果 attendees 为空，补充回成员列表
        if not attendees:
            attendees = get_repo_member_usernames(
                owner, repo_name, GITEA_TOKEN, GITEA_BASE_URL
            )

        results.append({
            "action":          "generate_brief",
            "repo":            full_name,
            "meeting_dir":     dir_name,
            "topic":           meta.get("topic", ""),
            "scheduled_time":  meeting_time.isoformat(),
            "organizer":       organizer,
            "attendees":       attendees,
            "attendee_emails": attendee_emails,
            "since":           since_dt.isoformat(),
            "until":           until_dt.isoformat(),
            # gitea-routine-report 使用 YYYY-MM-DD 格式
            "report_params": {
                "repo":  full_name,
                "since": format_date(since_dt),
                "until": format_date(until_dt),
            },
            "window_source": (
                "last_meeting" if last_meeting_time else f"fallback_{FALLBACK_DAYS}d"
            ),
        })

    return results


def main():
    if not GITEA_BASE_URL or not GITEA_TOKEN:
        print(json.dumps({
            "error": "缺少 Gitea 配置，请检查 ~/.config/skill-b-pre-brief/.env",
            "meetings": [],
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
        "scanned_repos": len(repos),
        "meetings":      all_meetings,
        "count":         len(all_meetings),
        "errors":        errors,
        "scan_time":     datetime.now(TZ).isoformat(),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
