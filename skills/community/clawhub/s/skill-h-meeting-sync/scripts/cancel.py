#!/usr/bin/env python3
"""
Skill-H cancel：将指定会议的 meta.yaml status 更新为 cancelled。
写日志，返回取消通知邮件参数供 OpenClaw 调用 imap-smtp-email 发送。

重要安全规则：
- 只有“会议时间尚未到达”的会议，才允许自动标记为 cancelled
- 如果 scheduled_time 已经 <= now，则不自动取消
  因为腾讯会议中不存在这场会，也可能只是会议已经正常结束

用法：
    python3 cancel.py       --repo "HKU-AIFusion/dexterous-hand"       --meeting-dir "2026-04-22-1500"       --attendee-emails "email1@163.com,email2@163.com"       [--cancel-reason "腾讯会议中已不存在，且会议时间尚未到达"]
"""

import os
import sys
import json
import argparse
from datetime import datetime

import pytz
import yaml
from dateutil.parser import parse as parse_dt
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.config/skill-h-meeting-sync/.env"))

sys.path.insert(0, os.path.dirname(__file__))
from gitea_utils import get_file_from_repo, update_file_in_repo
from log_utils import write_log
from email_utils import build_cancel_html

GITEA_BASE_URL = os.getenv("GITEA_BASE_URL", "")
GITEA_TOKEN    = os.getenv("GITEA_TOKEN_BOT", "")
META_REPO      = os.getenv("AIFUSION_META_REPO", "")
TZ             = pytz.timezone("Asia/Shanghai")


def parse_time_or_none(time_str):
    """解析 ISO8601 时间；失败返回 None。"""
    if not time_str:
        return None
    try:
        dt = parse_dt(time_str)
        if dt.tzinfo is None:
            dt = TZ.localize(dt)
        return dt.astimezone(TZ)
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(description="Skill-H cancel：标记会议为已取消")
    parser.add_argument("--repo",            required=True, help="仓库全名")
    parser.add_argument("--meeting-dir",     required=True, help="会议目录名")
    parser.add_argument("--attendee-emails", default="",    help="逗号分隔的参会人邮箱")
    parser.add_argument("--cancel-reason",   default="腾讯会议中已不存在，且会议时间尚未到达", help="取消原因")
    args = parser.parse_args()

    owner, repo_name = args.repo.split("/", 1)
    meta_path = f"meetings/{args.meeting_dir}/meta.yaml"

    # ── 读取 meta.yaml ────────────────────────────────────────────────────────

    raw, sha = get_file_from_repo(owner, repo_name, meta_path, GITEA_TOKEN, GITEA_BASE_URL)
    if raw is None:
        _fail(f"meta.yaml 不存在：{args.repo}/{meta_path}")

    try:
        meta = yaml.safe_load(raw) or {}
    except Exception as e:
        _fail(f"meta.yaml 解析失败：{e}")

    old_status = meta.get("status", "")

    # 幂等检查：已是终态则直接返回成功
    if old_status == "cancelled":
        print(json.dumps({
            "success": True,
            "idempotent": True,
            "message": "会议已处于 cancelled 状态，无需重复操作",
        }, ensure_ascii=False, indent=2))
        return

    # ── 安全检查：会议时间已过，不自动取消 ────────────────────────────────────

    scheduled_time_str = meta.get("scheduled_time", "")
    scheduled_dt = parse_time_or_none(scheduled_time_str)
    now = datetime.now(TZ)

    if scheduled_dt and scheduled_dt <= now:
        write_log({
            "ts":          now.isoformat(),
            "skill":       "skill-h",
            "repo":        args.repo,
            "meeting_dir": args.meeting_dir,
            "action":      "meeting-cancel-skipped",
            "status":      "skipped",
            "details": {
                "old_status":      old_status,
                "scheduled_time":  scheduled_dt.isoformat(),
                "now":             now.isoformat(),
                "skip_reason":     "meeting_time_passed",
                "cancel_reason":   args.cancel_reason,
            },
        }, META_REPO, GITEA_TOKEN, GITEA_BASE_URL)

        print(json.dumps({
            "success":      True,
            "skipped":      True,
            "skip_reason":  "meeting_time_passed",
            "meeting_dir":  args.meeting_dir,
            "current_status": old_status,
            "message":      "会议时间已过，可能已正常结束；Skill-H 不自动将其标记为 cancelled",
        }, ensure_ascii=False, indent=2))
        return

    # ── 更新 meta.yaml ────────────────────────────────────────────────────────

    meta["status"]        = "cancelled"
    meta["cancel_reason"] = args.cancel_reason
    meta["cancelled_at"]  = now.isoformat()

    new_content = yaml.dump(meta, allow_unicode=True, default_flow_style=False, sort_keys=False)
    try:
        update_file_in_repo(
            owner, repo_name, meta_path, new_content,
            f"chore(meeting): cancel {args.meeting_dir}",
            sha, GITEA_TOKEN, GITEA_BASE_URL,
        )
    except Exception as e:
        _fail(f"meta.yaml 更新失败：{e}")

    # ── 写日志 ────────────────────────────────────────────────────────────────

    write_log({
        "ts":          now.isoformat(),
        "skill":       "skill-h",
        "repo":        args.repo,
        "meeting_dir": args.meeting_dir,
        "action":      "meeting-cancelled",
        "status":      "ok",
        "details": {
            "old_status":    old_status,
            "cancel_reason": args.cancel_reason,
        },
    }, META_REPO, GITEA_TOKEN, GITEA_BASE_URL)

    # ── 构建取消通知邮件 ──────────────────────────────────────────────────────

    attendee_emails = [e.strip() for e in args.attendee_emails.split(",") if e.strip()]

    topic          = meta.get("topic", args.meeting_dir)
    meeting_code   = meta.get("meeting_code", "")
    organizer      = meta.get("organizer", "")

    try:
        parts      = args.meeting_dir.split("-")
        time_label = f"{parts[1]}-{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
    except Exception:
        time_label = args.meeting_dir

    html = build_cancel_html(
        topic, scheduled_time_str, meeting_code,
        args.repo, organizer, args.cancel_reason,
    )

    print(json.dumps({
        "success":     True,
        "meeting_dir": args.meeting_dir,
        "new_status":  "cancelled",
        "cancel_email": {
            "to":      attendee_emails,
            "subject": f"【会议取消】{topic} · {time_label}",
            "html":    html,
        },
    }, ensure_ascii=False, indent=2))


def _fail(message):
    print(json.dumps({"success": False, "error": message}, ensure_ascii=False))
    sys.exit(1)


if __name__ == "__main__":
    main()
