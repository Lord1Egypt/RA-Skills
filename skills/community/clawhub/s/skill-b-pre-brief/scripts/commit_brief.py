#!/usr/bin/env python3
"""
Skill-B commit：将渲染好的简报 HTML 存入 Gitea 会议目录，
更新 meta.yaml 状态为 brief-sent，写日志，返回邮件参数。

用法（正常简报）：
    python3 commit_brief.py \
      --repo "HKU-AIFusion/dexterous-hand" \
      --meeting-dir "2026-04-22-1500" \
      --topic "v2 设计评审" \
      --html-file "/tmp/brief_body_2026-04-22-1500.html" \
      --attendee-emails "email1@163.com,email2@163.com" \
      --since "2026-04-15" \
      --until "2026-04-22"

用法（改期会议，只更新状态）：
    python3 commit_brief.py \
      --repo "HKU-AIFusion/dexterous-hand" \
      --meeting-dir "2026-04-22-1500" \
      --mark-only
"""

import os
import sys
import json
import argparse
from datetime import datetime

import pytz
import yaml
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.config/skill-b-pre-brief/.env"))

sys.path.insert(0, os.path.dirname(__file__))
from gitea_utils import (
    create_file_in_repo,
    get_file_from_repo,
    update_file_in_repo,
)
from log_utils import write_log

GITEA_BASE_URL = os.getenv("GITEA_BASE_URL", "")
GITEA_TOKEN    = os.getenv("GITEA_TOKEN_BOT", "")
META_REPO      = os.getenv("AIFUSION_META_REPO", "")
TZ             = pytz.timezone("Asia/Shanghai")


# ──────────────────────────────────────────────────────────────────────────────

def update_meta_status(owner, repo_name, meeting_dir, new_status):
    """
    将 meetings/<meeting_dir>/meta.yaml 的 status 字段更新为 new_status。
    抛出异常时向上传递。
    """
    meta_path = f"meetings/{meeting_dir}/meta.yaml"
    raw, sha = get_file_from_repo(owner, repo_name, meta_path, GITEA_TOKEN, GITEA_BASE_URL)

    if raw is None:
        raise FileNotFoundError(f"meta.yaml 不存在：{meta_path}")

    meta = yaml.safe_load(raw) or {}
    old_status = meta.get("status", "")
    meta["status"] = new_status

    new_content = yaml.dump(meta, allow_unicode=True, default_flow_style=False, sort_keys=False)
    update_file_in_repo(
        owner, repo_name, meta_path, new_content,
        f"chore(meeting): status {old_status} → {new_status} [{meeting_dir}]",
        sha, GITEA_TOKEN, GITEA_BASE_URL,
    )

    return old_status


def build_pre_brief_md(topic, meeting_dir, since, until, sent_at, attendee_emails):
    """
    生成存入 Gitea 的 pre_brief.md（轻量索引文件，HTML 完整版由邮件发送）。
    """
    try:
        parts = meeting_dir.split("-")
        time_str = f"{parts[0]}-{parts[1]}-{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
    except Exception:
        time_str = meeting_dir

    recipients = ", ".join(attendee_emails) if attendee_emails else "（无）"

    return f"""# 会前简报 — {topic}

**会议时间**：{time_str}（北京时间）
**统计时间段**：{since} ~ {until}
**发送时间**：{sent_at}
**发送对象**：{recipients}

> 完整 HTML 版简报已通过邮件发送给全体参会人。
> 若需查阅详细内容，请在邮件客户端中查找主题包含"【会前简报】"的邮件。
"""


# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Skill-B commit：保存简报并更新状态")
    parser.add_argument("--repo",            required=True, help="仓库全名，如 owner/repo")
    parser.add_argument("--meeting-dir",     required=True, help="会议目录名，如 2026-04-22-1500")
    parser.add_argument("--topic",           default="",    help="会议主题（mark-only 时可省略）")
    parser.add_argument("--html-file",       default="",    help="渲染好的 HTML 简报文件路径")
    parser.add_argument("--attendee-emails", default="",    help="逗号分隔的参会人邮箱")
    parser.add_argument("--since",           default="",    help="活动统计开始日期 YYYY-MM-DD")
    parser.add_argument("--until",           default="",    help="活动统计结束日期 YYYY-MM-DD")
    parser.add_argument("--mark-only",       action="store_true",
                        help="只更新 meta.yaml 状态，不保存简报文件，不返回邮件参数（改期会议用）")
    args = parser.parse_args()

    if not GITEA_BASE_URL or not GITEA_TOKEN:
        _fail("缺少 Gitea 配置，请检查 ~/.config/skill-b-pre-brief/.env")

    owner, repo_name = args.repo.split("/", 1)
    now_str = datetime.now(TZ).strftime("%Y-%m-%d %H:%M")

    # ── mark-only 模式（改期会议）────────────────────────────────────────────

    if args.mark_only:
        try:
            old_status = update_meta_status(owner, repo_name, args.meeting_dir, "brief-sent")
        except Exception as e:
            _fail(f"更新 meta.yaml 失败：{e}")

        write_log({
            "ts":          datetime.now(TZ).isoformat(),
            "skill":       "skill-b",
            "repo":        args.repo,
            "meeting_dir": args.meeting_dir,
            "action":      "mark-only-brief-sent",
            "status":      "ok",
            "details":     {"old_status": old_status, "reason": "rescheduled_from"},
        }, META_REPO, GITEA_TOKEN, GITEA_BASE_URL)

        print(json.dumps({
            "success":     True,
            "action":      "mark_only",
            "meeting_dir": args.meeting_dir,
            "new_status":  "brief-sent",
        }, ensure_ascii=False, indent=2))
        return

    # ── 正常简报模式 ──────────────────────────────────────────────────────────

    if not args.html_file:
        _fail("--html-file 为必填项（非 mark-only 模式）")

    if not os.path.isfile(args.html_file):
        _fail(f"HTML 文件不存在：{args.html_file}")

    with open(args.html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    if not html_content.strip():
        _fail(f"HTML 文件内容为空：{args.html_file}")

    attendee_emails = [
        e.strip() for e in args.attendee_emails.split(",") if e.strip()
    ]

    # ── 1. 保存 pre_brief.md 到 Gitea ────────────────────────────────────────

    brief_md = build_pre_brief_md(
        args.topic, args.meeting_dir,
        args.since, args.until,
        now_str, attendee_emails,
    )

    try:
        create_file_in_repo(
            owner, repo_name,
            f"meetings/{args.meeting_dir}/pre_brief.md",
            brief_md,
            f"feat(meeting): add pre_brief for {args.meeting_dir}",
            GITEA_TOKEN, GITEA_BASE_URL,
        )
    except Exception as e:
        # pre_brief.md 写入失败，阻止状态更新（下次 cron 可重试）
        _fail(f"pre_brief.md 写入 Gitea 失败：{e}")

    # ── 2. 更新 meta.yaml status → brief-sent ────────────────────────────────

    try:
        old_status = update_meta_status(owner, repo_name, args.meeting_dir, "brief-sent")
    except Exception as e:
        _fail(f"meta.yaml 状态更新失败：{e}")

    # ── 3. 写日志 ─────────────────────────────────────────────────────────────

    write_log({
        "ts":          datetime.now(TZ).isoformat(),
        "skill":       "skill-b",
        "repo":        args.repo,
        "meeting_dir": args.meeting_dir,
        "action":      "brief-sent",
        "status":      "ok",
        "details": {
            "old_status":       old_status,
            "recipients":       len(attendee_emails),
            "since":            args.since,
            "until":            args.until,
        },
    }, META_REPO, GITEA_TOKEN, GITEA_BASE_URL)

    # ── 4. 构建邮件主题 ───────────────────────────────────────────────────────

    try:
        parts = args.meeting_dir.split("-")
        time_label = f"{parts[1]}-{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
    except Exception:
        time_label = args.meeting_dir

    email_subject = f"【会前简报】{args.topic} · {time_label}"

    # ── 5. 返回结果 ───────────────────────────────────────────────────────────

    print(json.dumps({
        "success":     True,
        "meeting_dir": args.meeting_dir,
        "new_status":  "brief-sent",
        "brief_email": {
            "to":      attendee_emails,
            "subject": email_subject,
            "html":    html_content,
        },
    }, ensure_ascii=False, indent=2))


def _fail(message):
    print(json.dumps({"success": False, "error": message}, ensure_ascii=False))
    sys.exit(1)


if __name__ == "__main__":
    main()
