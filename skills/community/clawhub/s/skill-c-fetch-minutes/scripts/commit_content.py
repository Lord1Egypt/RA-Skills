#!/usr/bin/env python3
"""
Skill-C commit-content：将 OpenClaw 生成的四个文件提交到 Gitea 会议目录，
将 meta.yaml status 更新为 draft-pending-review，写日志，
返回发给组织者的审核通知邮件参数。

OpenClaw 负责：
  - 生成四个文件的内容并写入 /tmp
  - 调用本脚本

本脚本负责：
  - 逐一将文件 upsert 到 Gitea（自动处理创建 or 更新）
  - 更新 meta.yaml status
  - 写日志
  - 返回邮件参数（供 OpenClaw 调用 imap-smtp-email）

用法：
    python3 commit_content.py \
      --repo "HKU-AIFusion/dexterous-hand" \
      --meeting-dir "2026-04-22-1500" \
      --topic "v2 设计评审" \
      --organizer-email "organizer@163.com" \
      --transcript-file "/tmp/transcript_2026-04-22-1500.md" \
      --minutes-file "/tmp/minutes_2026-04-22-1500.md" \
      --draft-issue-file "/tmp/draft_issue_2026-04-22-1500.md" \
      [--ai-summary-file "/tmp/ai_summary_2026-04-22-1500.md"] \
      [--source "ai_summary"]
"""

import os
import sys
import json
import argparse
from datetime import datetime

import pytz
import yaml
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.config/skill-c-fetch-minutes/.env"))

sys.path.insert(0, os.path.dirname(__file__))
from gitea_utils import (
    get_file_from_repo,
    update_file_in_repo,
    upsert_file_in_repo,
)
from log_utils import write_log

GITEA_BASE_URL = os.getenv("GITEA_BASE_URL", "")
GITEA_TOKEN    = os.getenv("GITEA_TOKEN_BOT", "")
META_REPO      = os.getenv("AIFUSION_META_REPO", "")
TZ             = pytz.timezone("Asia/Shanghai")

# 有效的来源标识
VALID_SOURCES = {"ai_summary", "transcript_only", "manual_upload"}


def build_review_html(topic, meeting_dir, repo, organizer, source,
                      gitea_base_url, has_action_items):
    """生成发给组织者的 draft 审核通知邮件 HTML。"""
    try:
        parts      = meeting_dir.split("-")
        time_label = f"{parts[0]}-{parts[1]}-{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
    except Exception:
        time_label = meeting_dir

    dir_url          = f"{gitea_base_url.rstrip('/')}/{repo}/src/branch/main/meetings/{meeting_dir}/"
    draft_url        = f"{dir_url}draft_issue.md"
    minutes_url      = f"{dir_url}minutes.md"

    source_label = {
        "ai_summary":      "腾讯会议 AI 智能纪要 + 转录全文",
        "transcript_only": "腾讯会议转录全文",
        "manual_upload":   "手动上传的转录文件",
    }.get(source, source)

    action_items_note = (
        "<p>本次会议提取到待办任务，请重点审核 <strong>draft_issue.md</strong> 中各条任务的负责人和截止日期是否正确。</p>"
        if has_action_items else
        "<p>本次会议 <strong>未提取到明确的待办任务</strong>，draft_issue.md 已说明情况，请确认后处理。</p>"
    )

    return f"""<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, 'PingFang SC', sans-serif; max-width: 600px;
             margin: 0 auto; padding: 24px; color: #333;">

  <h2 style="color:#1a73e8;margin-bottom:4px;">📋 会议 issue 草稿待审核</h2>
  <p style="color:#666;margin-top:0;">
    系统已完成会议纪要生成，请审核 issue 草稿后确认。
  </p>

  <table style="border-collapse:collapse;width:100%;margin:20px 0;font-size:14px;">
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;width:110px;border:1px solid #e0e0e0;">会议主题</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{topic}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;border:1px solid #e0e0e0;">会议时间</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{time_label}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;border:1px solid #e0e0e0;">所属项目</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{repo}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;border:1px solid #e0e0e0;">内容来源</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{source_label}</td>
    </tr>
  </table>

  {action_items_note}

  <div style="background:#e8f5e9;border-left:4px solid #34a853;padding:16px;
              margin:20px 0;border-radius:4px;">
    <p style="margin:0 0 10px;font-weight:bold;">✅ 审核确认方式（二选一）</p>
    <ol style="margin:0;padding-left:20px;">
      <li style="margin-bottom:8px;">
        在 Gitea 中将
        <a href="{draft_url}" style="color:#1a73e8;"><code>draft_issue.md</code></a>
        改名为 <code>confirmed_issue.md</code>
      </li>
      <li>
        在 OpenClaw 中说：<strong>"确认 {meeting_dir} 的 issue"</strong>
      </li>
    </ol>
  </div>

  <div style="margin:24px 0;">
    <a href="{draft_url}"
       style="background:#1a73e8;color:white;padding:11px 22px;text-decoration:none;
              border-radius:5px;display:inline-block;font-size:14px;margin-right:10px;">
      📄 查看 issue 草稿
    </a>
    <a href="{minutes_url}"
       style="background:#34a853;color:white;padding:11px 22px;text-decoration:none;
              border-radius:5px;display:inline-block;font-size:14px;">
      📝 查看会议纪要
    </a>
  </div>

  <hr style="border:none;border-top:1px solid #e8e8e8;margin:24px 0;">
  <p style="color:#999;font-size:12px;margin:0;">本邮件由 AIFusion Bot 自动发送，请勿直接回复。</p>
</body>
</html>"""


def read_file_arg(path, label):
    """读取文件内容，失败则 _fail。"""
    if not path:
        return None
    if not os.path.isfile(path):
        _fail(f"{label} 文件不存在：{path}")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.strip():
        _fail(f"{label} 文件内容为空：{path}")
    return content


def main():
    parser = argparse.ArgumentParser(description="Skill-C commit-content")
    parser.add_argument("--repo",             required=True)
    parser.add_argument("--meeting-dir",      required=True)
    parser.add_argument("--topic",            required=True)
    parser.add_argument("--organizer-email",  required=True)
    parser.add_argument("--transcript-file",  required=True)
    parser.add_argument("--minutes-file",     required=True)
    parser.add_argument("--draft-issue-file", required=True)
    parser.add_argument("--ai-summary-file",  default="")
    parser.add_argument("--source",           default="transcript_only",
                        choices=list(VALID_SOURCES))
    args = parser.parse_args()

    if not GITEA_BASE_URL or not GITEA_TOKEN:
        _fail("缺少 Gitea 配置，请检查 ~/.config/skill-c-fetch-minutes/.env")

    owner, repo_name = args.repo.split("/", 1)
    d = args.meeting_dir
    meta_path = f"meetings/{d}/meta.yaml"

    # ── 读取所有文件内容 ──────────────────────────────────────────────────────

    transcript_content  = read_file_arg(args.transcript_file,  "transcript-file")
    minutes_content     = read_file_arg(args.minutes_file,     "minutes-file")
    draft_issue_content = read_file_arg(args.draft_issue_file, "draft-issue-file")
    ai_summary_content  = read_file_arg(args.ai_summary_file,  "ai-summary-file") \
                          if args.ai_summary_file else None

    # draft_issue 是否含有实际待办（简单判断有无 "- [ ]"）
    has_action_items = "- [ ]" in draft_issue_content

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
    if old_status == "draft-pending-review":
        print(json.dumps({
            "success":    True,
            "idempotent": True,
            "message":    "已处于 draft-pending-review 状态",
        }, ensure_ascii=False, indent=2))
        return

    # ── 逐文件 upsert 到 Gitea ────────────────────────────────────────────────

    files_to_commit = [
        (f"meetings/{d}/transcript.md",  transcript_content,  "feat(meeting): add transcript"),
        (f"meetings/{d}/minutes.md",     minutes_content,     "feat(meeting): add minutes"),
        (f"meetings/{d}/draft_issue.md", draft_issue_content, "feat(meeting): add draft_issue"),
    ]
    if ai_summary_content:
        files_to_commit.insert(1, (
            f"meetings/{d}/ai_summary.md", ai_summary_content, "feat(meeting): add ai_summary"
        ))

    for filepath, content, commit_msg in files_to_commit:
        try:
            upsert_file_in_repo(
                owner, repo_name, filepath, content,
                f"{commit_msg} [{d}]",
                GITEA_TOKEN, GITEA_BASE_URL,
            )
        except Exception as e:
            _fail(f"文件提交失败（{filepath}）：{e}")

    # ── 更新 meta.yaml status → draft-pending-review ──────────────────────────

    meta["status"]      = "draft-pending-review"
    meta["reviewed_at"] = None            # 占位，Skill-D 确认后填写
    meta["transcript_source"] = args.source

    new_meta = yaml.dump(meta, allow_unicode=True, default_flow_style=False, sort_keys=False)
    try:
        update_file_in_repo(
            owner, repo_name, meta_path, new_meta,
            f"chore(meeting): {old_status} → draft-pending-review [{d}]",
            sha, GITEA_TOKEN, GITEA_BASE_URL,
        )
    except Exception as e:
        _fail(f"meta.yaml 状态更新失败：{e}")

    # ── 写日志 ────────────────────────────────────────────────────────────────

    write_log({
        "ts":          datetime.now(TZ).isoformat(),
        "skill":       "skill-c",
        "repo":        args.repo,
        "meeting_dir": d,
        "action":      "draft-pending-review",
        "status":      "ok",
        "details": {
            "old_status":       old_status,
            "source":           args.source,
            "has_action_items": has_action_items,
        },
    }, META_REPO, GITEA_TOKEN, GITEA_BASE_URL)

    # ── 构建审核通知邮件 ──────────────────────────────────────────────────────

    try:
        parts      = d.split("-")
        time_label = f"{parts[1]}-{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
    except Exception:
        time_label = d

    html = build_review_html(
        args.topic, d, args.repo,
        meta.get("organizer", ""),
        args.source,
        GITEA_BASE_URL,
        has_action_items,
    )

    gitea_dir_url = f"{GITEA_BASE_URL.rstrip('/')}/{args.repo}/src/branch/main/meetings/{d}/"

    print(json.dumps({
        "success":       True,
        "meeting_dir":   d,
        "new_status":    "draft-pending-review",
        "has_action_items": has_action_items,
        "gitea_dir_url": gitea_dir_url,
        "review_email": {
            "to":      [args.organizer_email] if args.organizer_email else [],
            "subject": f"【请审核】{args.topic} 会议 issue 草稿已生成 · {time_label}",
            "html":    html,
        },
    }, ensure_ascii=False, indent=2))


def _fail(message):
    print(json.dumps({"success": False, "error": message}, ensure_ascii=False))
    sys.exit(1)


if __name__ == "__main__":
    main()
