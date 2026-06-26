#!/usr/bin/env python3
"""
Skill-C set-waiting：将会议状态 scheduled / brief-sent → waiting-transcript。
记录 transcript_started_at 时间戳，初始化 transcript_poll_count = 0。

重要安全规则：
- 只有会议真正结束后，并额外等待 20 分钟，才允许自动进入 waiting-transcript
- 如果条件未满足，本脚本返回 skipped=true，不推进状态
- 即使 OpenClaw 误调用，本脚本也会拦截未满足条件的会议

用法：
    python3 set_waiting.py \
      --repo "HKU-AIFusion/dexterous-hand" \
      --meeting-dir "2026-04-22-1500"
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

load_dotenv(os.path.expanduser("~/.config/skill-c-fetch-minutes/.env"))

sys.path.insert(0, os.path.dirname(__file__))
from gitea_utils import get_file_from_repo, update_file_in_repo
from log_utils import write_log

GITEA_BASE_URL = os.getenv("GITEA_BASE_URL", "")
GITEA_TOKEN    = os.getenv("GITEA_TOKEN_BOT", "")
META_REPO      = os.getenv("AIFUSION_META_REPO", "")
TZ             = pytz.timezone("Asia/Shanghai")

POST_MEETING_GRACE_MINUTES = 20


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
    parser = argparse.ArgumentParser(description="Skill-C set-waiting")
    parser.add_argument("--repo",         required=True)
    parser.add_argument("--meeting-dir",  required=True)
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
    if old_status == "waiting-transcript":
        started_at = meta.get("transcript_started_at", datetime.now(TZ).isoformat())
        print(json.dumps({
            "success":               True,
            "idempotent":            True,
            "transcript_started_at": started_at,
            "message":               "已处于 waiting-transcript 状态",
        }, ensure_ascii=False, indent=2))
        return

    if old_status not in {"brief-sent", "scheduled"}:
        _fail(f"状态不符：期望 brief-sent 或 scheduled，实际 {old_status}")

    # ── 安全检查：必须“会议结束 + 20 分钟缓冲”后才能进入 waiting-transcript ──

    scheduled_dt = parse_time_or_none(meta.get("scheduled_time", ""))
    if scheduled_dt is None:
        _fail("scheduled_time 缺失或解析失败，拒绝进入 waiting-transcript")

    try:
        duration_minutes = int(meta.get("duration_minutes", 60) or 60)
    except Exception:
        duration_minutes = 60

    end_dt = scheduled_dt + timedelta(minutes=duration_minutes)
    ready_after_dt = end_dt + timedelta(minutes=POST_MEETING_GRACE_MINUTES)
    now = datetime.now(TZ)

    if now <= ready_after_dt:
        write_log({
            "ts":          now.isoformat(),
            "skill":       "skill-c",
            "repo":        args.repo,
            "meeting_dir": args.meeting_dir,
            "action":      "set-waiting-transcript-skipped",
            "status":      "skipped",
            "details": {
                "old_status":                old_status,
                "scheduled_time":            scheduled_dt.isoformat(),
                "duration_minutes":          duration_minutes,
                "meeting_end_time":          end_dt.isoformat(),
                "ready_after_time":          ready_after_dt.isoformat(),
                "postprocess_grace_minutes": POST_MEETING_GRACE_MINUTES,
                "now":                       now.isoformat(),
                "skip_reason":               "meeting_not_finished_long_enough",
            },
        }, META_REPO, GITEA_TOKEN, GITEA_BASE_URL)

        print(json.dumps({
            "success":                    True,
            "skipped":                    True,
            "skip_reason":                "meeting_not_finished_long_enough",
            "meeting_dir":                args.meeting_dir,
            "current_status":             old_status,
            "scheduled_time":             scheduled_dt.isoformat(),
            "meeting_end_time":           end_dt.isoformat(),
            "ready_after_time":           ready_after_dt.isoformat(),
            "postprocess_grace_minutes":  POST_MEETING_GRACE_MINUTES,
            "message":                    "会议尚未结束超过 20 分钟，Skill-C 不进入 waiting-transcript",
        }, ensure_ascii=False, indent=2))
        return

    # ── 正常推进状态 ─────────────────────────────────────────────────────────

    now_str = now.isoformat()
    meta["status"]                = "waiting-transcript"
    meta["transcript_started_at"] = now_str
    meta["transcript_poll_count"] = 0

    new_content = yaml.dump(meta, allow_unicode=True, default_flow_style=False, sort_keys=False)
    try:
        update_file_in_repo(
            owner, repo_name, meta_path, new_content,
            f"chore(meeting): {old_status} → waiting-transcript [{args.meeting_dir}]",
            sha, GITEA_TOKEN, GITEA_BASE_URL,
        )
    except Exception as e:
        _fail(f"meta.yaml 更新失败：{e}")

    write_log({
        "ts":          now.isoformat(),
        "skill":       "skill-c",
        "repo":        args.repo,
        "meeting_dir": args.meeting_dir,
        "action":      "set-waiting-transcript",
        "status":      "ok",
        "details": {
            "old_status":                old_status,
            "scheduled_time":            scheduled_dt.isoformat(),
            "duration_minutes":          duration_minutes,
            "meeting_end_time":          end_dt.isoformat(),
            "ready_after_time":          ready_after_dt.isoformat(),
            "postprocess_grace_minutes": POST_MEETING_GRACE_MINUTES,
        },
    }, META_REPO, GITEA_TOKEN, GITEA_BASE_URL)

    print(json.dumps({
        "success":               True,
        "meeting_dir":           args.meeting_dir,
        "new_status":            "waiting-transcript",
        "old_status":            old_status,
        "transcript_started_at": now_str,
        "meeting_end_time":      end_dt.isoformat(),
        "ready_after_time":      ready_after_dt.isoformat(),
        "postprocess_grace_minutes": POST_MEETING_GRACE_MINUTES,
    }, ensure_ascii=False, indent=2))


def _fail(message):
    print(json.dumps({"success": False, "error": message}, ensure_ascii=False))
    sys.exit(1)


if __name__ == "__main__":
    main()