#!/usr/bin/env python3
"""
Skill-H archive：将 status ∈ {cancelled, rescheduled} 且超过 30 天的会议目录
迁移到同仓库的 meetings/archive/ 子目录。

迁移策略（Gitea 不支持目录重命名，逐文件操作）：
  1. 读取旧目录下所有文件内容
  2. 在 meetings/archive/<dir_name>/ 下逐一创建
  3. 逐一删除旧目录下的文件

任一文件迁移失败时：记录警告，跳过该文件，继续处理其他文件。
最终输出归档摘要。

用法：
    python3 archive.py
"""

import os
import sys
import json
from datetime import datetime, timedelta, timezone

import pytz
import yaml
from dateutil.parser import parse as parse_dt
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.config/skill-h-meeting-sync/.env"))

sys.path.insert(0, os.path.dirname(__file__))
from gitea_utils import (
    get_managed_repos,
    list_meetings_in_repo,
    get_file_from_repo,
    list_dir_in_repo,
    create_file_in_repo,
    delete_file_in_repo,
)
from log_utils import write_log

GITEA_BASE_URL    = os.getenv("GITEA_BASE_URL", "")
GITEA_TOKEN       = os.getenv("GITEA_TOKEN_BOT", "")
META_REPO         = os.getenv("AIFUSION_META_REPO", "")
TZ                = pytz.timezone("Asia/Shanghai")

ARCHIVE_STATUSES  = {"cancelled", "rescheduled"}
ARCHIVE_DAYS      = 30


# ─────────────────────────────────────────────────────────────────────────────

def is_older_than(scheduled_time_str, days):
    """判断会议时间是否超过 days 天前。"""
    try:
        dt = parse_dt(scheduled_time_str)
        if dt.tzinfo is None:
            dt = TZ.localize(dt)
        threshold = datetime.now(TZ) - timedelta(days=days)
        return dt < threshold
    except Exception:
        return False


def migrate_dir(owner, repo_name, src_dir, dst_dir):
    """
    将 meetings/<src_dir>/ 下所有文件迁移到 meetings/<dst_dir>/。
    返回 (migrated_files, failed_files)。
    """
    items = list_dir_in_repo(
        owner, repo_name, f"meetings/{src_dir}",
        GITEA_TOKEN, GITEA_BASE_URL,
    )

    migrated = []
    failed   = []

    for item in items:
        if item.get("type") != "file":
            continue

        filename = item["name"]
        src_path = f"meetings/{src_dir}/{filename}"
        dst_path = f"meetings/{dst_dir}/{filename}"

        # 读取源文件
        content, sha = get_file_from_repo(
            owner, repo_name, src_path, GITEA_TOKEN, GITEA_BASE_URL
        )
        if content is None:
            failed.append({"file": filename, "reason": "读取源文件失败"})
            continue

        # 在目标路径创建
        try:
            create_file_in_repo(
                owner, repo_name, dst_path, content,
                f"chore(archive): move {src_dir}/{filename} to archive",
                GITEA_TOKEN, GITEA_BASE_URL,
            )
        except Exception as e:
            failed.append({"file": filename, "reason": f"创建目标文件失败：{e}"})
            continue

        # 删除源文件
        try:
            delete_file_in_repo(
                owner, repo_name, src_path, sha,
                f"chore(archive): delete {src_dir}/{filename}",
                GITEA_TOKEN, GITEA_BASE_URL,
            )
        except Exception as e:
            # 删除失败不影响归档结果（目标已创建），仅记录警告
            failed.append({"file": filename, "reason": f"删除源文件失败（目标已创建）：{e}"})
            continue

        migrated.append(filename)

    return migrated, failed


def archive_repo(full_name):
    """归档单个仓库中符合条件的会议目录。"""
    owner, repo_name = full_name.split("/", 1)
    dirs = list_meetings_in_repo(owner, repo_name, GITEA_TOKEN, GITEA_BASE_URL)

    repo_result = []

    for dir_name in dirs:
        # 读 meta.yaml
        raw, _ = get_file_from_repo(
            owner, repo_name, f"meetings/{dir_name}/meta.yaml",
            GITEA_TOKEN, GITEA_BASE_URL,
        )
        if not raw:
            continue

        try:
            meta = yaml.safe_load(raw) or {}
        except Exception:
            continue

        status = meta.get("status", "")
        if status not in ARCHIVE_STATUSES:
            continue

        scheduled_time = meta.get("scheduled_time", "")
        if not is_older_than(scheduled_time, ARCHIVE_DAYS):
            continue

        # ── 开始迁移 ──────────────────────────────────────────────────────────

        dst_dir = f"archive/{dir_name}"
        migrated, failed = migrate_dir(owner, repo_name, dir_name, dst_dir)

        repo_result.append({
            "dir":      dir_name,
            "status":   status,
            "migrated": migrated,
            "failed":   failed,
            "ok":       len(failed) == 0,
        })

        write_log({
            "ts":          datetime.now(TZ).isoformat(),
            "skill":       "skill-h",
            "repo":        full_name,
            "meeting_dir": dir_name,
            "action":      "meeting-archived",
            "status":      "ok" if not failed else "partial",
            "details": {
                "dst_dir":        dst_dir,
                "migrated_count": len(migrated),
                "failed_count":   len(failed),
                "failed_files":   failed,
            },
        }, META_REPO, GITEA_TOKEN, GITEA_BASE_URL)

    return repo_result


# ─────────────────────────────────────────────────────────────────────────────

def main():
    if not GITEA_BASE_URL or not GITEA_TOKEN:
        print(json.dumps({
            "error": "缺少 Gitea 配置，请检查 ~/.config/skill-h-meeting-sync/.env",
        }, ensure_ascii=False))
        sys.exit(1)

    repos   = get_managed_repos(GITEA_TOKEN, GITEA_BASE_URL)
    summary = []
    errors  = []

    for full_name in repos:
        try:
            results = archive_repo(full_name)
            if results:
                summary.append({"repo": full_name, "archived": results})
        except Exception as e:
            errors.append({"repo": full_name, "error": str(e)})

    total_dirs    = sum(len(r["archived"]) for r in summary)
    total_files   = sum(
        sum(len(d["migrated"]) for d in r["archived"])
        for r in summary
    )
    total_failed  = sum(
        sum(len(d["failed"]) for d in r["archived"])
        for r in summary
    )

    print(json.dumps({
        "success":       True,
        "scanned_repos": len(repos),
        "archived_dirs": total_dirs,
        "migrated_files":total_files,
        "failed_files":  total_failed,
        "errors":        errors,
        "summary":       summary,
        "archive_time":  datetime.now(TZ).isoformat(),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
