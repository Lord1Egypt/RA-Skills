#!/usr/bin/env python3
"""
Skill-H reschedule：处理会议改期。

操作：
  1. 旧目录 meta.yaml：status → rescheduled，写入 rescheduled_to 字段
  2. 创建新目录（新时间），继承旧会议 topic/attendees/organizer/category/series_id，
     写入 rescheduled_from 字段，status = scheduled
  3. 在新目录创建 agenda.md（注明改期来源）
  4. 写日志，返回改期通知邮件参数

用法：
    python3 reschedule.py \
      --repo "HKU-AIFusion/dexterous-hand" \
      --old-meeting-dir "2026-04-22-1500" \
      --new-time "2026-04-23T15:00:00+08:00" \
      --new-meeting-id "yyy" \
      --new-meeting-code "987654321" \
      --new-join-url "https://meeting.tencent.com/..." \
      --attendee-emails "email1@163.com,email2@163.com"
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
from gitea_utils import (
    get_file_from_repo,
    update_file_in_repo,
    create_file_in_repo,
)
from log_utils import write_log
from email_utils import build_reschedule_html

GITEA_BASE_URL = os.getenv("GITEA_BASE_URL", "")
GITEA_TOKEN    = os.getenv("GITEA_TOKEN_BOT", "")
META_REPO      = os.getenv("AIFUSION_META_REPO", "")
TZ             = pytz.timezone("Asia/Shanghai")


def parse_time(time_str):
    dt = parse_dt(time_str)
    if dt.tzinfo is None:
        dt = TZ.localize(dt)
    return dt.astimezone(TZ)


def build_new_meta_yaml(old_meta, new_time, new_meeting_id, new_meeting_code,
                        new_join_url, old_dir_name, new_dir_name):
    meta = {
        "meeting_id":       new_meeting_id,
        "meeting_code":     new_meeting_code,
        "join_url":         new_join_url,
        "topic":            old_meta.get("topic", ""),
        "scheduled_time":   new_time.isoformat(),
        "duration_minutes": old_meta.get("duration_minutes", 60),
        "type":             old_meta.get("type", "ad-hoc"),
        "meeting_category": old_meta.get("meeting_category", "single"),
        "repo":             old_meta.get("repo", ""),
        "organizer":        old_meta.get("organizer", ""),
        "attendees":        old_meta.get("attendees", []),
        "status":           "scheduled",
        "rescheduled_from": old_dir_name,
    }
    if old_meta.get("series_id"):
        meta["series_id"] = old_meta["series_id"]
    return yaml.dump(meta, allow_unicode=True, default_flow_style=False, sort_keys=False)


def build_rescheduled_agenda_md(topic, new_time, new_join_url, new_meeting_code,
                                 attendees, organizer, repo, old_dir_name):
    time_str      = new_time.strftime("%Y-%m-%d %H:%M")
    attendees_str = ", ".join(attendees)
    try:
        parts     = old_dir_name.split("-")
        old_label = f"{parts[0]}-{parts[1]}-{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
    except Exception:
        old_label = old_dir_name

    return f"""## 会议基本信息

- 时间：{time_str}（北京时间）
- 腾讯会议链接：{new_join_url}
- 会议号：{new_meeting_code}
- 与会人员：{attendees_str}
- 组织者：{organizer}
- 所属项目：{repo}

## 本次议程

（本次会议由 {old_label} 改期而来，请组织者在此填写新议程）

## 上次会议内容回顾

（改期会议暂无参考记录，请查看原会议目录 meetings/{old_dir_name}/ 的相关文档）
"""


def main():
    parser = argparse.ArgumentParser(description="Skill-H reschedule：处理会议改期")
    parser.add_argument("--repo",            required=True)
    parser.add_argument("--old-meeting-dir", required=True)
    parser.add_argument("--new-time",        required=True, help="ISO8601 新会议时间")
    parser.add_argument("--new-meeting-id",  required=True)
    parser.add_argument("--new-meeting-code",required=True)
    parser.add_argument("--new-join-url",    required=True)
    parser.add_argument("--attendee-emails", default="", help="逗号分隔的参会人邮箱")
    args = parser.parse_args()

    owner, repo_name = args.repo.split("/", 1)
    old_dir  = args.old_meeting_dir
    old_meta_path = f"meetings/{old_dir}/meta.yaml"

    # ── 读取旧 meta.yaml ──────────────────────────────────────────────────────

    raw, sha = get_file_from_repo(owner, repo_name, old_meta_path, GITEA_TOKEN, GITEA_BASE_URL)
    if raw is None:
        _fail(f"旧 meta.yaml 不存在：{old_meta_path}")

    try:
        old_meta = yaml.safe_load(raw) or {}
    except Exception as e:
        _fail(f"旧 meta.yaml 解析失败：{e}")

    # 幂等检查
    if old_meta.get("status") == "rescheduled":
        print(json.dumps({
            "success":    True,
            "idempotent": True,
            "message":    f"{old_dir} 已处于 rescheduled 状态，无需重复操作",
        }, ensure_ascii=False, indent=2))
        return

    # ── 解析新时间 ────────────────────────────────────────────────────────────

    try:
        new_time = parse_time(args.new_time)
    except Exception as e:
        _fail(f"新时间格式解析失败：{e}")

    new_dir = new_time.strftime("%Y-%m-%d-%H%M")

    # ── Step 1：更新旧 meta.yaml → rescheduled ────────────────────────────────

    old_meta["status"]         = "rescheduled"
    old_meta["rescheduled_to"] = new_dir
    old_meta["rescheduled_at"] = datetime.now(TZ).isoformat()

    old_new_content = yaml.dump(old_meta, allow_unicode=True, default_flow_style=False, sort_keys=False)
    try:
        update_file_in_repo(
            owner, repo_name, old_meta_path, old_new_content,
            f"chore(meeting): reschedule {old_dir} → {new_dir}",
            sha, GITEA_TOKEN, GITEA_BASE_URL,
        )
    except Exception as e:
        _fail(f"旧 meta.yaml 更新失败：{e}")

    # ── Step 2：创建新目录 meta.yaml ─────────────────────────────────────────

    new_meta_content = build_new_meta_yaml(
        old_meta, new_time,
        args.new_meeting_id, args.new_meeting_code, args.new_join_url,
        old_dir, new_dir,
    )
    try:
        create_file_in_repo(
            owner, repo_name,
            f"meetings/{new_dir}/meta.yaml",
            new_meta_content,
            f"feat(meeting): create rescheduled meeting {new_dir}",
            GITEA_TOKEN, GITEA_BASE_URL,
        )
    except Exception as e:
        _fail(f"新 meta.yaml 创建失败（旧目录已标记 rescheduled）：{e}")

    # ── Step 3：创建新目录 agenda.md ──────────────────────────────────────────

    attendees  = old_meta.get("attendees", [])
    organizer  = old_meta.get("organizer", "")
    topic      = old_meta.get("topic", "")

    agenda_content = build_rescheduled_agenda_md(
        topic, new_time, args.new_join_url, args.new_meeting_code,
        attendees, organizer, args.repo, old_dir,
    )
    try:
        create_file_in_repo(
            owner, repo_name,
            f"meetings/{new_dir}/agenda.md",
            agenda_content,
            f"feat(meeting): add agenda for rescheduled {new_dir}",
            GITEA_TOKEN, GITEA_BASE_URL,
        )
    except Exception as e:
        # agenda 失败不阻塞主流程，日志记录即可
        pass

    # ── 写日志 ────────────────────────────────────────────────────────────────

    write_log({
        "ts":          datetime.now(TZ).isoformat(),
        "skill":       "skill-h",
        "repo":        args.repo,
        "meeting_dir": old_dir,
        "action":      "meeting-rescheduled",
        "status":      "ok",
        "details": {
            "old_dir": old_dir,
            "new_dir": new_dir,
            "new_meeting_id": args.new_meeting_id,
        },
    }, META_REPO, GITEA_TOKEN, GITEA_BASE_URL)

    # ── 构建改期通知邮件 ──────────────────────────────────────────────────────

    attendee_emails = [e.strip() for e in args.attendee_emails.split(",") if e.strip()]
    old_time        = old_meta.get("scheduled_time", "")

    try:
        parts      = old_dir.split("-")
        old_label  = f"{parts[1]}-{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
        new_label  = new_time.strftime("%m-%d %H:%M")
    except Exception:
        old_label = old_dir
        new_label = new_dir

    agenda_gitea_url = (
        f"{GITEA_BASE_URL.rstrip('/')}/{args.repo}"
        f"/src/branch/main/meetings/{new_dir}/agenda.md"
    )

    html = build_reschedule_html(
        topic, old_time, new_time,
        args.new_meeting_code, args.new_join_url,
        args.repo, organizer, agenda_gitea_url,
    )

    print(json.dumps({
        "success":        True,
        "old_meeting_dir": old_dir,
        "new_meeting_dir": new_dir,
        "reschedule_email": {
            "to":      attendee_emails,
            "subject": f"【会议改期】{topic} · {old_label} → {new_label}",
            "html":    html,
        },
    }, ensure_ascii=False, indent=2))


def _fail(message):
    print(json.dumps({"success": False, "error": message}, ensure_ascii=False))
    sys.exit(1)


if __name__ == "__main__":
    main()
