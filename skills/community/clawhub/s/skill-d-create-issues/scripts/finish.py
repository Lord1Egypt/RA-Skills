#!/usr/bin/env python3
"""
Skill-D finish：收尾步骤。
  1. meta.yaml status → minutes-published，写入 created_issues 字段
  2. 写日志
  3. 生成并返回三种邮件参数，供 OpenClaw 调用 imap-smtp-email 发送

用法（单项目会议，有 issue）：
    python3 finish.py \
      --repo "HKU-AIFusion/dexterous-hand" \
      --meeting-dir "2026-04-22-1500" \
      --topic "v2 设计评审" \
      --category "single" \
      --organizer-email "organizer@163.com" \
      --attendee-emails "email1@163.com,email2@163.com" \
      --created-issues-json '[{"local_id":"1","issue_number":42,"issue_url":"...","assignee":"sujinze","task":"...","due_date":"...","quote":"..."}]' \
      --failed-issues-json '[]'

用法（跨项目会议，无 issue）：
    python3 finish.py \
      --repo "HKU-AIFusion/aifusion-meta" \
      --meeting-dir "2026-04-22-1500" \
      --topic "跨组全员会议" \
      --category "cross-project" \
      --organizer-email "organizer@163.com" \
      --attendee-emails "" \
      --confirmed-issue-content "（confirmed_issue.md 完整文本）"
"""

import os
import sys
import json
import argparse
from datetime import datetime
from collections import defaultdict

import pytz
import yaml
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.config/skill-d-create-issues/.env"))

sys.path.insert(0, os.path.dirname(__file__))
from gitea_utils import get_file_from_repo, update_file_in_repo
from log_utils import write_log
from email_utils import (
    build_minutes_html,
    build_assignee_html,
    build_cross_project_html,
)

GITEA_BASE_URL = os.getenv("GITEA_BASE_URL", "")
GITEA_TOKEN    = os.getenv("GITEA_TOKEN_BOT", "")
META_REPO      = os.getenv("AIFUSION_META_REPO", "")
TZ             = pytz.timezone("Asia/Shanghai")


def _time_label(meeting_dir):
    try:
        parts = meeting_dir.split("-")
        return f"{parts[1]}-{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
    except Exception:
        return meeting_dir


def main():
    parser = argparse.ArgumentParser(description="Skill-D finish：收尾，返回邮件参数")
    parser.add_argument("--repo",                    required=True)
    parser.add_argument("--meeting-dir",             required=True)
    parser.add_argument("--topic",                   required=True)
    parser.add_argument("--category",                default="single",
                        choices=["single", "cross-project"])
    parser.add_argument("--organizer-email",         required=True)
    parser.add_argument("--attendee-emails",         default="",
                        help="逗号分隔的全员邮箱")
    parser.add_argument("--created-issues-json",     default="[]")
    parser.add_argument("--failed-issues-json",      default="[]")
    parser.add_argument("--confirmed-issue-content", default="",
                        help="跨项目会议时传入 confirmed_issue.md 全文")
    parser.add_argument("--minutes-summary",         default="",
                        help="minutes.md 的摘要文本（OpenClaw 提取，用于正式纪要邮件）")
    args = parser.parse_args()

    if not GITEA_BASE_URL or not GITEA_TOKEN:
        _fail("缺少 Gitea 配置，请检查 ~/.config/skill-d-create-issues/.env")

    try:
        created_issues = json.loads(args.created_issues_json) if args.created_issues_json else []
    except Exception as e:
        _fail(f"created-issues-json 解析失败：{e}")

    try:
        failed_issues = json.loads(args.failed_issues_json) if args.failed_issues_json else []
    except Exception as e:
        _fail(f"failed-issues-json 解析失败：{e}")

    owner, repo_name = args.repo.split("/", 1)
    d         = args.meeting_dir
    meta_path = f"meetings/{d}/meta.yaml"

    # ── 读取 meta.yaml ────────────────────────────────────────────────────────

    raw, sha = get_file_from_repo(owner, repo_name, meta_path, GITEA_TOKEN, GITEA_BASE_URL)
    if raw is None:
        _fail(f"meta.yaml 不存在：{meta_path}")

    try:
        meta = yaml.safe_load(raw) or {}
    except Exception as e:
        _fail(f"meta.yaml 解析失败：{e}")

    old_status = meta.get("status", "")

    # 幂等检查
    if old_status == "minutes-published":
        print(json.dumps({
            "success":    True,
            "idempotent": True,
            "message":    "已处于 minutes-published 状态",
        }, ensure_ascii=False, indent=2))
        return

    # ── 更新 meta.yaml ────────────────────────────────────────────────────────

    meta["status"]          = "minutes-published"
    meta["published_at"]    = datetime.now(TZ).isoformat()
    meta["created_issues"]  = [i["issue_number"] for i in created_issues]

    new_content = yaml.dump(meta, allow_unicode=True, default_flow_style=False, sort_keys=False)
    try:
        update_file_in_repo(
            owner, repo_name, meta_path, new_content,
            f"chore(meeting): {old_status} → minutes-published [{d}]",
            sha, GITEA_TOKEN, GITEA_BASE_URL,
        )
    except Exception as e:
        _fail(f"meta.yaml 更新失败：{e}")

    # ── 写日志 ────────────────────────────────────────────────────────────────

    write_log({
        "ts":          datetime.now(TZ).isoformat(),
        "skill":       "skill-d",
        "repo":        args.repo,
        "meeting_dir": d,
        "action":      "minutes-published",
        "status":      "ok",
        "details": {
            "category":          args.category,
            "old_status":        old_status,
            "created_issues":    [i["issue_number"] for i in created_issues],
            "failed_count":      len(failed_issues),
        },
    }, META_REPO, GITEA_TOKEN, GITEA_BASE_URL)

    # ── 构建邮件参数 ──────────────────────────────────────────────────────────

    attendee_emails = [e.strip() for e in args.attendee_emails.split(",") if e.strip()]
    organizer       = meta.get("organizer", "")
    time_label      = _time_label(d)

    result = {
        "success":     True,
        "meeting_dir": d,
        "new_status":  "minutes-published",
        "created_count": len(created_issues),
        "failed_count":  len(failed_issues),
        # 三种邮件（按 category 使用不同的）
        "minutes_email":   None,
        "assignee_emails": [],
        "cross_email":     None,
    }

    if args.category == "single":

        # ── 正式纪要邮件（全员）────────────────────────────────────────────────

        minutes_html = build_minutes_html(
            topic=args.topic,
            meeting_dir=d,
            repo=args.repo,
            organizer=organizer,
            join_url=meta.get("join_url", ""),
            created_issues=created_issues,
            failed_issues=failed_issues,
            gitea_base_url=GITEA_BASE_URL,
            minutes_content_summary=args.minutes_summary,
        )
        result["minutes_email"] = {
            "to":      attendee_emails,
            "subject": f"【会议纪要】{args.topic} · {time_label}",
            "html":    minutes_html,
        }

        # ── 个人任务通知邮件（按 assignee 分组）──────────────────────────────

        # assignee → [task_dict]
        assignee_tasks: dict[str, list] = defaultdict(list)
        for issue in created_issues:
            a = issue.get("assignee", "")
            if a:
                assignee_tasks[a].append({
                    "issue_number": issue["issue_number"],
                    "issue_url":    issue["issue_url"],
                    "task":         issue["task"],
                    "due_date":     issue.get("due_date", ""),
                    "quote":        issue.get("quote", ""),
                    "depends_on_str": "",   # 依赖描述可由 OpenClaw 在 finish 前补充
                })

        for assignee_username, tasks in assignee_tasks.items():
            # 尝试从 attendee_emails 中匹配（根据顺序）；
            # 更精确的方式是 check 时返回 email_map，这里用简化方案：
            # OpenClaw 可以在调用 finish 时额外传入 assignee email map，
            # 或者此处直接用 Gitea API 查询（因为 token 在环境里）。
            from gitea_utils import get_user_email
            a_email = get_user_email(assignee_username, GITEA_TOKEN, GITEA_BASE_URL)
            if not a_email:
                continue

            a_html = build_assignee_html(
                assignee_username=assignee_username,
                tasks=tasks,
                topic=args.topic,
                meeting_dir=d,
                repo=args.repo,
                gitea_base_url=GITEA_BASE_URL,
            )
            result["assignee_emails"].append({
                "to":      [a_email],
                "subject": f"【任务分配】您在 "{args.topic}" 中有 {len(tasks)} 项待办 · {time_label}",
                "html":    a_html,
            })

    else:
        # ── 跨项目会议：仅发组织者建议邮件 ───────────────────────────────────

        cross_html = build_cross_project_html(
            topic=args.topic,
            meeting_dir=d,
            repo=args.repo,
            confirmed_issue_content=args.confirmed_issue_content,
            gitea_base_url=GITEA_BASE_URL,
        )
        result["cross_email"] = {
            "to":      [args.organizer_email] if args.organizer_email else [],
            "subject": f"【跨项目会议 issue 建议】{args.topic} · {time_label}",
            "html":    cross_html,
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))


def _fail(message):
    print(json.dumps({"success": False, "error": message}, ensure_ascii=False))
    sys.exit(1)


if __name__ == "__main__":
    main()
