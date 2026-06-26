#!/usr/bin/env python3
"""
Skill-H create-pending：在 aifusion-meta 中为未关联仓库的新腾讯会议
创建占位记录（repo: pending），并返回发给管理员的待确认通知邮件参数。

用法：
    python3 create_pending.py \
      --meeting-id "zzz" \
      --meeting-code "111222333" \
      --topic "未知主题" \
      --time "2026-04-24T10:00:00+08:00" \
      --join-url "https://meeting.tencent.com/..." \
      [--duration 60]
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
from gitea_utils import create_file_in_repo, get_file_from_repo, get_user_email
from log_utils import write_log
from email_utils import build_pending_html

GITEA_BASE_URL        = os.getenv("GITEA_BASE_URL", "")
GITEA_TOKEN           = os.getenv("GITEA_TOKEN_BOT", "")
META_REPO             = os.getenv("AIFUSION_META_REPO", "")
ADVISOR_USERNAME      = os.getenv("ADVISOR_GITEA_USERNAME", "")
TZ                    = pytz.timezone("Asia/Shanghai")


def main():
    parser = argparse.ArgumentParser(description="Skill-H create-pending：创建 repo:pending 占位记录")
    parser.add_argument("--meeting-id",   required=True)
    parser.add_argument("--meeting-code", required=True)
    parser.add_argument("--topic",        required=True)
    parser.add_argument("--time",         required=True, help="ISO8601 会议时间")
    parser.add_argument("--join-url",     required=True)
    parser.add_argument("--duration",     type=int, default=60)
    args = parser.parse_args()

    if not META_REPO:
        _fail("AIFUSION_META_REPO 未配置")

    # ── 解析时间，确定目录名 ──────────────────────────────────────────────────

    try:
        dt = parse_dt(args.time)
        if dt.tzinfo is None:
            dt = TZ.localize(dt)
        dt = dt.astimezone(TZ)
    except Exception as e:
        _fail(f"时间格式解析失败：{e}")

    dir_name = dt.strftime("%Y-%m-%d-%H%M")
    meta_owner, meta_repo_name = META_REPO.split("/", 1)
    meta_path = f"meetings/{dir_name}/meta.yaml"

    # ── 幂等检查：目录是否已存在 ──────────────────────────────────────────────

    existing, _ = get_file_from_repo(
        meta_owner, meta_repo_name, meta_path, GITEA_TOKEN, GITEA_BASE_URL
    )
    if existing:
        try:
            existing_meta = yaml.safe_load(existing) or {}
        except Exception:
            existing_meta = {}
        if existing_meta.get("meeting_id") == args.meeting_id:
            print(json.dumps({
                "success":    True,
                "idempotent": True,
                "meeting_dir": dir_name,
                "message":    f"meeting_id {args.meeting_id} 已存在于 {dir_name}，无需重复创建",
            }, ensure_ascii=False, indent=2))
            return

    # ── 构建 meta.yaml ────────────────────────────────────────────────────────

    meta = {
        "meeting_id":       args.meeting_id,
        "meeting_code":     args.meeting_code,
        "join_url":         args.join_url,
        "topic":            args.topic,
        "scheduled_time":   dt.isoformat(),
        "duration_minutes": args.duration,
        "type":             "ad-hoc",
        "meeting_category": "unknown",
        "repo":             "pending",           # 待组织者确认
        "organizer":        "",
        "attendees":        [],
        "status":           "scheduled",
        "pending_since":    datetime.now(TZ).isoformat(),
    }
    meta_content = yaml.dump(meta, allow_unicode=True, default_flow_style=False, sort_keys=False)

    # ── 写入 aifusion-meta ────────────────────────────────────────────────────

    try:
        create_file_in_repo(
            meta_owner, meta_repo_name, meta_path,
            meta_content,
            f"feat(meeting): pending {dir_name} (meeting_id={args.meeting_id})",
            GITEA_TOKEN, GITEA_BASE_URL,
        )
    except Exception as e:
        _fail(f"创建 pending 目录失败：{e}")

    # ── 写日志 ────────────────────────────────────────────────────────────────

    write_log({
        "ts":          datetime.now(TZ).isoformat(),
        "skill":       "skill-h",
        "repo":        META_REPO,
        "meeting_dir": dir_name,
        "action":      "meeting-pending-created",
        "status":      "ok",
        "details": {
            "meeting_id":   args.meeting_id,
            "meeting_code": args.meeting_code,
            "topic":        args.topic,
        },
    }, META_REPO, GITEA_TOKEN, GITEA_BASE_URL)

    # ── 构建待确认通知邮件 ────────────────────────────────────────────────────

    # 收件人：管理员/导师邮箱
    advisor_email = get_user_email(ADVISOR_USERNAME, GITEA_TOKEN, GITEA_BASE_URL) if ADVISOR_USERNAME else ""
    to_list = [advisor_email] if advisor_email else []

    html = build_pending_html(
        args.topic, dt, args.meeting_code, args.join_url,
        args.meeting_id, META_REPO, dir_name,
    )

    try:
        parts      = dir_name.split("-")
        time_label = f"{parts[1]}-{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
    except Exception:
        time_label = dir_name

    print(json.dumps({
        "success":     True,
        "meeting_dir": dir_name,
        "meta_repo":   META_REPO,
        "notify_email": {
            "to":      to_list,
            "subject": f"【待确认】腾讯会议发现未关联会议 · {args.topic} · {time_label}",
            "html":    html,
        },
    }, ensure_ascii=False, indent=2))


def _fail(message):
    print(json.dumps({"success": False, "error": message}, ensure_ascii=False))
    sys.exit(1)


if __name__ == "__main__":
    main()
