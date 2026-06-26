#!/usr/bin/env python3
"""
Skill-C set-failed：将会议状态 waiting-transcript → transcript-failed。
写日志，返回发给组织者的手动上传通知邮件参数。

用法：
    python3 set_failed.py \
      --repo "HKU-AIFusion/dexterous-hand" \
      --meeting-dir "2026-04-22-1500" \
      --organizer-email "organizer@163.com"
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
from gitea_utils import get_file_from_repo, update_file_in_repo
from log_utils import write_log

GITEA_BASE_URL = os.getenv("GITEA_BASE_URL", "")
GITEA_TOKEN    = os.getenv("GITEA_TOKEN_BOT", "")
META_REPO      = os.getenv("AIFUSION_META_REPO", "")
TZ             = pytz.timezone("Asia/Shanghai")


def build_manual_upload_html(topic, meeting_dir, repo, gitea_base_url, organizer):
    """生成手动上传指引邮件 HTML。"""
    try:
        parts      = meeting_dir.split("-")
        time_label = f"{parts[0]}-{parts[1]}-{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
    except Exception:
        time_label = meeting_dir

    transcript_url = (
        f"{gitea_base_url.rstrip('/')}/{repo}"
        f"/src/branch/main/meetings/{meeting_dir}/"
    )

    return f"""<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, 'PingFang SC', sans-serif; max-width: 600px;
             margin: 0 auto; padding: 24px; color: #333;">

  <h2 style="color:#e65100;margin-bottom:4px;">⚠️ 会议转录拉取超时，需要手动上传</h2>
  <p style="color:#666;margin-top:0;">
    以下会议的转录内容超过 60 分钟仍未成功从腾讯会议拉取，请手动上传转录文件。
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
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;border:1px solid #e0e0e0;">组织者</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{organizer}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;border:1px solid #e0e0e0;">所属项目</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{repo}</td>
    </tr>
  </table>

  <div style="background:#fff3e0;border-left:4px solid #e65100;padding:16px;
              margin:20px 0;border-radius:4px;">
    <p style="margin:0 0 10px;font-weight:bold;">📋 操作步骤</p>
    <ol style="margin:0;padding-left:20px;">
      <li style="margin-bottom:8px;">
        从腾讯会议客户端手动导出本场会议的转录文本
      </li>
      <li style="margin-bottom:8px;">
        将内容整理后，以 <code>transcript.md</code> 为文件名，
        上传到以下 Gitea 目录：<br>
        <a href="{transcript_url}" style="color:#1a73e8;">{transcript_url}</a>
      </li>
      <li>
        上传完成后，系统将在下次轮询时（约 10 分钟）自动继续处理
      </li>
    </ol>
  </div>

  <hr style="border:none;border-top:1px solid #e8e8e8;margin:24px 0;">
  <p style="color:#999;font-size:12px;margin:0;">本邮件由 AIFusion Bot 自动发送，请勿直接回复。</p>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Skill-C set-failed")
    parser.add_argument("--repo",            required=True)
    parser.add_argument("--meeting-dir",     required=True)
    parser.add_argument("--organizer-email", required=True)
    args = parser.parse_args()

    owner, repo_name = args.repo.split("/", 1)
    meta_path = f"meetings/{args.meeting_dir}/meta.yaml"

    raw, sha = get_file_from_repo(owner, repo_name, meta_path, GITEA_TOKEN, GITEA_BASE_URL)
    if raw is None:
        _fail(f"meta.yaml 不存在：{meta_path}")

    try:
        meta = yaml.safe_load(raw) or {}
    except Exception as e:
        _fail(f"meta.yaml 解析失败：{e}")

    old_status = meta.get("status", "")

    # 幂等检查
    if old_status == "transcript-failed":
        print(json.dumps({
            "success":    True,
            "idempotent": True,
            "message":    "已处于 transcript-failed 状态",
        }, ensure_ascii=False, indent=2))
        return

    if old_status != "waiting-transcript":
        _fail(f"状态不符：期望 waiting-transcript，实际 {old_status}")

    meta["status"]      = "transcript-failed"
    meta["failed_at"]   = datetime.now(TZ).isoformat()

    new_content = yaml.dump(meta, allow_unicode=True, default_flow_style=False, sort_keys=False)
    try:
        update_file_in_repo(
            owner, repo_name, meta_path, new_content,
            f"chore(meeting): waiting-transcript → transcript-failed [{args.meeting_dir}]",
            sha, GITEA_TOKEN, GITEA_BASE_URL,
        )
    except Exception as e:
        _fail(f"meta.yaml 更新失败：{e}")

    write_log({
        "ts":          datetime.now(TZ).isoformat(),
        "skill":       "skill-c",
        "repo":        args.repo,
        "meeting_dir": args.meeting_dir,
        "action":      "transcript-failed",
        "status":      "ok",
        "details": {
            "old_status":            old_status,
            "transcript_started_at": meta.get("transcript_started_at", ""),
        },
    }, META_REPO, GITEA_TOKEN, GITEA_BASE_URL)

    topic     = meta.get("topic", args.meeting_dir)
    organizer = meta.get("organizer", "")

    try:
        parts      = args.meeting_dir.split("-")
        time_label = f"{parts[1]}-{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
    except Exception:
        time_label = args.meeting_dir

    html = build_manual_upload_html(
        topic, args.meeting_dir, args.repo, GITEA_BASE_URL, organizer,
    )

    print(json.dumps({
        "success":     True,
        "meeting_dir": args.meeting_dir,
        "new_status":  "transcript-failed",
        "fail_email": {
            "to":      [args.organizer_email] if args.organizer_email else [],
            "subject": f"【需要操作】{topic} 转录拉取超时，请手动上传 · {time_label}",
            "html":    html,
        },
    }, ensure_ascii=False, indent=2))


def _fail(message):
    print(json.dumps({"success": False, "error": message}, ensure_ascii=False))
    sys.exit(1)


if __name__ == "__main__":
    main()
