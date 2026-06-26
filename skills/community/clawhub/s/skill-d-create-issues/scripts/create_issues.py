#!/usr/bin/env python3
"""
Skill-D create-issues：接收 OpenClaw 解析好的 action items JSON，
批量在 Gitea 仓库建 issue，完成依赖关系回填。

OpenClaw 负责：解析 confirmed_issue.md，提取结构化 action items
本脚本负责：调用 Gitea API 创建 issue，管理 label，回填 Depends-on

输入 issues-json 格式：
[
  {
    "local_id": "1",
    "task": "任务描述",
    "assignee": "sujinze",
    "due_date": "2026-04-29",
    "depends_on_local_ids": [],
    "quote": "原话引用"
  }
]

用法：
    python3 create_issues.py \
      --repo "HKU-AIFusion/dexterous-hand" \
      --meeting-dir "2026-04-22-1500" \
      --topic "v2 设计评审" \
      --issues-json '[...]'
"""

import os
import sys
import json
import argparse
from datetime import datetime

import pytz
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.config/skill-d-create-issues/.env"))

sys.path.insert(0, os.path.dirname(__file__))
from gitea_utils import (
    ensure_label,
    create_issue,
    update_issue_body,
)

GITEA_BASE_URL = os.getenv("GITEA_BASE_URL", "")
GITEA_TOKEN    = os.getenv("GITEA_TOKEN_BOT", "")
TZ             = pytz.timezone("Asia/Shanghai")

# issue label 颜色
LABEL_MEETING_ACTION_COLOR = "#e11d48"   # 红色：需要行动
LABEL_MEETING_REF_COLOR    = "#6366f1"   # 紫色：来源标记


def build_issue_body(task, assignee, due_date, quote, meeting_dir,
                     repo, gitea_base_url, depends_placeholder=""):
    """构建 Gitea issue 正文 Markdown。"""
    dir_url = f"{gitea_base_url.rstrip('/')}/{repo}/src/branch/main/meetings/{meeting_dir}/"
    try:
        parts      = meeting_dir.split("-")
        time_label = f"{parts[0]}-{parts[1]}-{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
    except Exception:
        time_label = meeting_dir

    lines = [
        f"## 任务描述",
        f"",
        f"{task}",
        f"",
    ]

    if due_date:
        lines += [f"**截止日期**：{due_date}", ""]

    if depends_placeholder:
        lines += [depends_placeholder, ""]

    if quote:
        lines += [
            f"## 原话引用",
            f"",
            f"> {quote}",
            f"",
        ]

    lines += [
        f"## 来源",
        f"",
        f"- 会议：[{time_label}]({dir_url})",
        f"- 负责人：@{assignee}" if assignee else "",
        f"",
        f"---",
        f"*本 issue 由 AIFusion Bot 根据会议决议自动创建*",
    ]

    return "\n".join(line for line in lines)


def main():
    parser = argparse.ArgumentParser(description="Skill-D create-issues：批量建 Gitea issue")
    parser.add_argument("--repo",         required=True)
    parser.add_argument("--meeting-dir",  required=True)
    parser.add_argument("--topic",        required=True)
    parser.add_argument("--issues-json",  required=True, help="JSON 数组字符串")
    args = parser.parse_args()

    if not GITEA_BASE_URL or not GITEA_TOKEN:
        _fail("缺少 Gitea 配置，请检查 ~/.config/skill-d-create-issues/.env")

    try:
        items = json.loads(args.issues_json)
    except Exception as e:
        _fail(f"issues-json 解析失败：{e}")

    if not items:
        print(json.dumps({
            "success": True,
            "created": [],
            "failed":  [],
            "message": "issues-json 为空，无需建 issue",
        }, ensure_ascii=False, indent=2))
        return

    owner, repo_name = args.repo.split("/", 1)
    d = args.meeting_dir

    # ── 确保 label 存在 ───────────────────────────────────────────────────────

    label_action_id = ensure_label(
        owner, repo_name, "meeting-action",
        GITEA_TOKEN, GITEA_BASE_URL,
        color=LABEL_MEETING_ACTION_COLOR,
    )
    label_ref_id = ensure_label(
        owner, repo_name, f"meeting:{d}",
        GITEA_TOKEN, GITEA_BASE_URL,
        color=LABEL_MEETING_REF_COLOR,
    )
    label_ids = [lid for lid in [label_action_id, label_ref_id] if lid is not None]

    # ── 第一轮：创建所有 issue ────────────────────────────────────────────────

    # local_id → {issue_number, issue_url, assignee, task}
    created_map: dict[str, dict] = {}
    created = []
    failed  = []

    for item in items:
        local_id = str(item.get("local_id", ""))
        task     = item.get("task", "（无标题）")
        assignee = item.get("assignee", "")
        due_date = item.get("due_date", "")
        quote    = item.get("quote", "")

        body = build_issue_body(
            task, assignee, due_date, quote,
            d, args.repo, GITEA_BASE_URL,
        )

        assignees = [assignee] if assignee else []

        try:
            issue_number, issue_url = create_issue(
                owner, repo_name,
                title=task,
                body=body,
                assignees=assignees,
                label_ids=label_ids,
                token=GITEA_TOKEN,
                base_url=GITEA_BASE_URL,
            )
            created_map[local_id] = {
                "local_id":    local_id,
                "issue_number": issue_number,
                "issue_url":   issue_url,
                "assignee":    assignee,
                "task":        task,
                "due_date":    due_date,
                "quote":       quote,
            }
            created.append(created_map[local_id])
        except Exception as e:
            failed.append({"local_id": local_id, "task": task, "error": str(e)})

    # ── 第二轮：回填依赖关系 ──────────────────────────────────────────────────

    for item in items:
        local_id      = str(item.get("local_id", ""))
        dep_local_ids = [str(x) for x in item.get("depends_on_local_ids", [])]

        if not dep_local_ids:
            continue

        # 本条或依赖项若有任一创建失败则跳过
        if local_id not in created_map:
            continue
        dep_issue_numbers = []
        for dep_id in dep_local_ids:
            if dep_id in created_map:
                dep_issue_numbers.append(created_map[dep_id]["issue_number"])

        if not dep_issue_numbers:
            continue

        this = created_map[local_id]
        depends_line = "**依赖**：" + ", ".join(f"#{n}" for n in dep_issue_numbers)

        # 重新构建正文（带依赖行）
        new_body = build_issue_body(
            this["task"], this["assignee"], this["due_date"], this["quote"],
            d, args.repo, GITEA_BASE_URL,
            depends_placeholder=depends_line,
        )

        try:
            update_issue_body(
                owner, repo_name, this["issue_number"],
                new_body, GITEA_TOKEN, GITEA_BASE_URL,
            )
        except Exception:
            # 依赖回填失败不影响 issue 本身，静默忽略
            pass

    print(json.dumps({
        "success": True,
        "created": created,
        "failed":  failed,
    }, ensure_ascii=False, indent=2))


def _fail(message):
    print(json.dumps({"success": False, "error": message}, ensure_ascii=False))
    sys.exit(1)


if __name__ == "__main__":
    main()
