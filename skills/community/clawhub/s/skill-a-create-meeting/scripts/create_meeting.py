#!/usr/bin/env python3
"""
Skill-A 主执行脚本（执行型版本）。

本脚本不负责：
- LLM 解析
- 腾讯会议创建
- SMTP 发信

本脚本只负责：
- Gitea 侧会议目录 / meta.yaml / agenda.md
- 自动获取仓库成员和邮箱
- 查询仓库 owner 邮箱
- 生成邀请邮件 HTML 内容
- 写统一日志
- 返回给 OpenClaw 供后续调用 imap-smtp-email
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta

import pytz
import yaml
from dateutil.parser import parse as parse_dt
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.config/skill-a-create-meeting/.env"))

sys.path.insert(0, os.path.dirname(__file__))
from gitea_utils import (
    get_user_email,
    get_repo_member_usernames,
    get_repo_owner_email,
    create_file_in_repo,
    get_file_from_repo,
    list_meetings_in_repo,
)
from email_utils import build_invitation_html
from log_utils import write_log

GITEA_BASE_URL = os.getenv("GITEA_BASE_URL", "")
GITEA_TOKEN = os.getenv("GITEA_TOKEN_BOT", "")
META_REPO = os.getenv("AIFUSION_META_REPO", "")
TZ = pytz.timezone("Asia/Shanghai")


def get_previous_meeting_info(repo, meeting_type, series_id, token, base_url):
    """
    读取上次同类会议 minutes.md 的存在情况。
    当前版本不在 skill 内做 LLM 摘要，只做保守降级。
    有内容也只给出来源标签，agenda 中仍提示去查看原文。
    """
    try:
        owner, repo_name = repo.split("/", 1)
        dirs = sorted(list_meetings_in_repo(owner, repo_name, token, base_url), reverse=True)

        for dir_name in dirs:
            if "__rescheduled" in dir_name:
                continue

            meta_raw, _ = get_file_from_repo(
                owner, repo_name, f"meetings/{dir_name}/meta.yaml", token, base_url
            )
            if not meta_raw:
                continue

            meta = yaml.safe_load(meta_raw) or {}
            if meeting_type == "recurring" and series_id:
                if meta.get("series_id") != series_id:
                    continue

            minutes_content, _ = get_file_from_repo(
                owner, repo_name, f"meetings/{dir_name}/minutes.md", token, base_url
            )
            if not minutes_content or len(minutes_content.strip()) < 20:
                continue

            try:
                parts = dir_name.split("-")
                label = f"{parts[0]}-{parts[1]}-{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
            except Exception:
                label = dir_name

            return (
                "- 已检测到上次同类会议纪要，请打开对应 minutes.md 查看原文要点。",
                label,
            )
    except Exception:
        pass

    return None, None


def build_meta_yaml(meeting_id, meeting_code, join_url, topic, scheduled_time,
                    duration_minutes, meeting_type, series_id, category, repo,
                    organizer, attendees):
    meta = {
        "meeting_id": meeting_id,
        "meeting_code": meeting_code,
        "join_url": join_url,
        "topic": topic,
        "scheduled_time": scheduled_time.isoformat(),
        "duration_minutes": duration_minutes,
        "type": meeting_type,
        "meeting_category": category,
        "repo": repo,
        "organizer": organizer,
        "attendees": attendees,
        "status": "scheduled",
    }
    if series_id:
        meta["series_id"] = series_id

    return yaml.dump(meta, allow_unicode=True, default_flow_style=False, sort_keys=False)


def build_agenda_md(topic, scheduled_time, join_url, meeting_code,
                    attendees, organizer, repo, prev_summary, prev_label):
    time_str = scheduled_time.strftime("%Y-%m-%d %H:%M")
    attendees_str = ", ".join(attendees)

    if prev_summary and prev_label:
        prev_section = f"""## 上次会议内容回顾

（来源：{prev_label} 会议 minutes.md）

{prev_summary}"""
    else:
        prev_section = "## 上次会议内容回顾\n\n暂无参考记录"

    return f"""## 会议基本信息

- 时间：{time_str}（北京时间）
- 腾讯会议链接：{join_url}
- 会议号：{meeting_code}
- 与会人员：{attendees_str}
- 组织者：{organizer}
- 所属项目：{repo}

## 本次议程

（请组织者在此填写）

{prev_section}
"""


def main():
    parser = argparse.ArgumentParser(description="Skill-A: 会议准备执行器")
    parser.add_argument("--time", required=True, help="ISO 8601 时间（含时区）")
    parser.add_argument("--topic", required=True, help="会议主题")
    parser.add_argument("--repo", required=True, help="目标仓库全名，如 owner/repo")
    parser.add_argument("--category", default="single", choices=["single", "cross-project"])
    parser.add_argument("--organizer", required=True, help="组织者 Gitea 用户名")
    parser.add_argument("--meeting-id", required=True, help="腾讯会议 meeting_id")
    parser.add_argument("--meeting-code", required=True, help="腾讯会议会议号")
    parser.add_argument("--join-url", required=True, help="腾讯会议加入链接")
    parser.add_argument("--attendees", default="", help="逗号分隔的 Gitea 用户名列表；不传则自动取仓库成员")
    parser.add_argument("--duration", type=int, default=60, help="会议时长（分钟）")
    parser.add_argument("--meeting-type", default="ad-hoc", choices=["ad-hoc", "recurring"])
    parser.add_argument("--series-id", default=None, help="循环会议系列 ID")
    args = parser.parse_args()

    try:
        scheduled_time = parse_dt(args.time)
        if scheduled_time.tzinfo is None:
            scheduled_time = TZ.localize(scheduled_time)
        scheduled_time = scheduled_time.astimezone(TZ)
    except Exception as e:
        _fail(f"时间格式解析失败：{e}")

    if not GITEA_BASE_URL or not GITEA_TOKEN or not META_REPO:
        _fail("缺少 Gitea 配置，请检查 ~/.config/skill-a-create-meeting/.env")

    owner, repo_name = args.repo.split("/", 1)

    if args.attendees.strip():
        attendees = [a.strip() for a in args.attendees.split(",") if a.strip()]
    else:
        attendees = get_repo_member_usernames(owner, repo_name, GITEA_TOKEN, GITEA_BASE_URL)
        if args.organizer and args.organizer not in attendees:
            attendees.insert(0, args.organizer)

    # 去重保序
    deduped = []
    seen = set()
    for u in attendees:
        if u and u not in seen:
            deduped.append(u)
            seen.add(u)
    attendees = deduped

    dir_name = scheduled_time.strftime("%Y-%m-%d-%H%M")
    repo_owner_email = get_repo_owner_email(owner, repo_name, GITEA_TOKEN, GITEA_BASE_URL)

    attendee_emails = []
    attendee_email_map = {}
    for username in attendees:
        email = get_user_email(username, GITEA_TOKEN, GITEA_BASE_URL)
        if email:
            attendee_emails.append(email)
            attendee_email_map[username] = email

    prev_summary, prev_label = get_previous_meeting_info(
        args.repo, args.meeting_type, args.series_id, GITEA_TOKEN, GITEA_BASE_URL
    )

    agenda_gitea_url = (
        f"{GITEA_BASE_URL.rstrip('/')}/{args.repo}"
        f"/src/branch/main/meetings/{dir_name}/agenda.md"
    )

    meta_content = build_meta_yaml(
        args.meeting_id, args.meeting_code, args.join_url, args.topic, scheduled_time,
        args.duration, args.meeting_type, args.series_id, args.category,
        args.repo, args.organizer, attendees,
    )
    agenda_content = build_agenda_md(
        args.topic, scheduled_time, args.join_url, args.meeting_code,
        attendees, args.organizer, args.repo, prev_summary, prev_label,
    )

    try:
        create_file_in_repo(
            owner, repo_name,
            f"meetings/{dir_name}/meta.yaml",
            meta_content,
            f"feat(meeting): create {dir_name}",
            GITEA_TOKEN, GITEA_BASE_URL,
        )
        create_file_in_repo(
            owner, repo_name,
            f"meetings/{dir_name}/agenda.md",
            agenda_content,
            f"feat(meeting): add agenda for {dir_name}",
            GITEA_TOKEN, GITEA_BASE_URL,
        )
    except Exception as e:
        _fail(f"Gitea 文件创建失败：{e}")

    html_body = build_invitation_html(
        args.topic, scheduled_time, args.join_url,
        args.meeting_code, args.organizer, args.repo, agenda_gitea_url,
    )
    email_subject = f"【会议邀请】{args.topic} · {scheduled_time.strftime('%m-%d %H:%M')}"

    log_entry = {
        "ts": datetime.now(TZ).isoformat(),
        "skill": "skill-a",
        "repo": args.repo,
        "meeting_dir": dir_name,
        "action": "meeting-prepared",
        "status": "ok",
        "details": {
            "meeting_id": args.meeting_id,
            "meeting_code": args.meeting_code,
            "repo_member_count": len(attendees),
            "resolved_email_count": len(attendee_emails),
        },
    }
    write_log(log_entry, META_REPO, GITEA_TOKEN, GITEA_BASE_URL)

    time_str = scheduled_time.strftime("%Y-%m-%d %H:%M")
    email_note = (
        f"请继续用 imap-smtp-email 向 {len(attendee_emails)} 个邮箱发送会议邀请。"
        if attendee_emails else
        "⚠️ 未解析到任何成员邮箱，请手动通知与会人员。"
    )

    user_message = (
        f"✅ 会议准备已完成！\n\n"
        f"📅 **{args.topic}**\n"
        f"🕐 {time_str}（北京时间）\n"
        f"🎥 会议号：{args.meeting_code}\n"
        f"🔗 加入链接：{args.join_url}\n"
        f"📝 议程文档：{agenda_gitea_url}\n\n"
        f"{email_note}"
    )

    print(json.dumps({
        "success": True,
        "user_message": user_message,
        "meeting_id": args.meeting_id,
        "meeting_code": args.meeting_code,
        "join_url": args.join_url,
        "agenda_gitea_url": agenda_gitea_url,
        "meeting_dir": dir_name,
        "repo_member_usernames": attendees,
        "repo_member_emails": attendee_emails,
        "repo_member_email_map": attendee_email_map,
        "repo_owner_email": repo_owner_email,
        "invite_email": {
            "to": attendee_emails,
            "subject": email_subject,
            "html": html_body,
        },
    }, ensure_ascii=False, indent=2))


def _fail(message):
    print(json.dumps({"success": False, "error": message}, ensure_ascii=False))
    sys.exit(1)


if __name__ == "__main__":
    main()
