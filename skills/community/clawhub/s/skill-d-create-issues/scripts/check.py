#!/usr/bin/env python3
"""
Skill-D check：校验前置条件，返回 confirmed_issue.md 内容和会议元信息。

校验项：
  1. meta.yaml status == draft-pending-review
  2. confirmed_issue.md 存在

用法：
    python3 check.py \
      --repo "HKU-AIFusion/dexterous-hand" \
      --meeting-dir "2026-04-22-1500"
"""

import os
import sys
import json
import argparse

import yaml
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.config/skill-d-create-issues/.env"))

sys.path.insert(0, os.path.dirname(__file__))
from gitea_utils import (
    get_file_from_repo,
    file_exists_in_repo,
    get_user_email,
    get_repo_member_usernames,
)

GITEA_BASE_URL = os.getenv("GITEA_BASE_URL", "")
GITEA_TOKEN    = os.getenv("GITEA_TOKEN_BOT", "")


def main():
    parser = argparse.ArgumentParser(description="Skill-D check：校验前置条件")
    parser.add_argument("--repo",        required=True)
    parser.add_argument("--meeting-dir", required=True)
    args = parser.parse_args()

    if not GITEA_BASE_URL or not GITEA_TOKEN:
        _invalid("缺少 Gitea 配置，请检查 ~/.config/skill-d-create-issues/.env")

    owner, repo_name = args.repo.split("/", 1)
    d = args.meeting_dir
    meta_path = f"meetings/{d}/meta.yaml"

    # ── 1. 读取 meta.yaml ─────────────────────────────────────────────────────

    raw, _ = get_file_from_repo(owner, repo_name, meta_path, GITEA_TOKEN, GITEA_BASE_URL)
    if raw is None:
        _invalid(f"meta.yaml 不存在，请确认会议目录正确：meetings/{d}/")

    try:
        meta = yaml.safe_load(raw) or {}
    except Exception as e:
        _invalid(f"meta.yaml 解析失败：{e}")

    status = meta.get("status", "")
    if status != "draft-pending-review":
        _invalid(
            f"当前状态为 '{status}'，不是 draft-pending-review。"
            + ("（已完成，无需重复操作）" if status == "minutes-published" else "")
        )

    # ── 2. 确认 confirmed_issue.md 存在 ──────────────────────────────────────

    confirmed_path = f"meetings/{d}/confirmed_issue.md"
    if not file_exists_in_repo(owner, repo_name, confirmed_path, GITEA_TOKEN, GITEA_BASE_URL):
        _invalid(
            "confirmed_issue.md 不存在。\n"
            "请在 Gitea 中将 draft_issue.md 改名为 confirmed_issue.md，"
            "或在 OpenClaw 中说"确认该会议的 issue"。"
        )

    # ── 3. 读取 confirmed_issue.md ────────────────────────────────────────────

    confirmed_content, _ = get_file_from_repo(
        owner, repo_name, confirmed_path, GITEA_TOKEN, GITEA_BASE_URL
    )
    if not confirmed_content:
        _invalid("confirmed_issue.md 内容为空，请检查文件是否正确上传。")

    # ── 4. 读取 minutes.md（可能不存在）──────────────────────────────────────

    minutes_content, _ = get_file_from_repo(
        owner, repo_name, f"meetings/{d}/minutes.md", GITEA_TOKEN, GITEA_BASE_URL
    )

    # ── 5. 解析参会人信息 ─────────────────────────────────────────────────────

    attendees = meta.get("attendees") or get_repo_member_usernames(
        owner, repo_name, GITEA_TOKEN, GITEA_BASE_URL
    )

    attendee_emails = [
        e for e in (get_user_email(u, GITEA_TOKEN, GITEA_BASE_URL) for u in attendees)
        if e
    ]

    organizer       = meta.get("organizer", "")
    organizer_email = get_user_email(organizer, GITEA_TOKEN, GITEA_BASE_URL) if organizer else ""
    if not organizer_email and owner:
        organizer_email = get_user_email(owner, GITEA_TOKEN, GITEA_BASE_URL)

    print(json.dumps({
        "valid":                    True,
        "repo":                     args.repo,
        "meeting_dir":              d,
        "category":                 meta.get("meeting_category", "single"),
        "topic":                    meta.get("topic", ""),
        "scheduled_time":           meta.get("scheduled_time", ""),
        "join_url":                 meta.get("join_url", ""),
        "organizer":                organizer,
        "organizer_email":          organizer_email,
        "attendees":                attendees,
        "attendee_emails":          attendee_emails,
        "confirmed_issue_content":  confirmed_content,
        "minutes_content":          minutes_content or "",
    }, ensure_ascii=False, indent=2))


def _invalid(reason):
    print(json.dumps({"valid": False, "reason": reason}, ensure_ascii=False))
    sys.exit(0)   # 校验失败不是脚本错误，正常退出让 OpenClaw 读 valid=false


if __name__ == "__main__":
    main()
