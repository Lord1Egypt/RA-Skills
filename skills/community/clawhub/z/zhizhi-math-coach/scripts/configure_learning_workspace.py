#!/usr/bin/env python3
"""Create or update the machine-readable zhizhi-math-coach workspace config."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from learning_workspace_config import (  # noqa: E402
    DEFAULT_SYNC_SCOPE,
    default_base_url,
    infer_owner_repo,
    update_config,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Configure a zhizhi-math-coach personal learning workspace.")
    parser.add_argument("--workspace", type=Path, default=Path("."), help="Personal learning repository root.")
    parser.add_argument("--student-name", default="孩子", help="Display name stored in the workspace config.")
    parser.add_argument("--github-owner", help="GitHub owner. Inferred from origin when omitted.")
    parser.add_argument("--repo", help="GitHub repository. Inferred from origin when omitted.")
    parser.add_argument("--remote", default="origin", help="Git remote name. Defaults to origin.")
    parser.add_argument("--branch", default="main", help="Git branch used for sync. Defaults to main.")
    parser.add_argument("--base-url", help="GitHub Pages base URL. Defaults to https://<owner>.github.io/<repo>.")
    parser.add_argument("--enable-git-sync", action="store_true", help="Mark Git sync as enabled.")
    parser.add_argument("--auto-sync", action="store_true", help="Enable automatic pull, commit, and push.")
    parser.add_argument("--defer-push-after-grading", action="store_true", help="For grading tasks, commit locally but skip push until a later sync.")
    parser.add_argument("--sync-full-learning-data", action="store_true", help="Allow the configured commit scope to include learning records.")
    parser.add_argument("--public-repository-accepted", action="store_true", help="Parent accepts the visibility of committed files in a public repository.")
    parser.add_argument("--enable-pages", action="store_true", help="Mark GitHub Pages publishing as enabled.")
    parser.add_argument("--auto-publish-pages", action="store_true", help="Automatically publish generated worksheets to Pages.")
    parser.add_argument("--enable-scheduled-tasks", action="store_true", help="Mark OpenClaw scheduled reminders as enabled.")
    parser.add_argument("--auto-register-scheduled-tasks", action="store_true", help="Automatically register OpenClaw cron jobs when supported.")
    parser.add_argument("--timezone", default="Asia/Shanghai", help="IANA timezone for scheduled reminders, for example Asia/Shanghai.")
    parser.add_argument("--allow-scheduled-record-writes", action="store_true", help="Allow scheduled jobs to write learning records.")
    parser.add_argument("--allow-scheduled-worksheet-generation", action="store_true", help="Allow scheduled jobs to generate worksheets.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = args.workspace.resolve()
    if not workspace.exists():
        print(f"error: workspace does not exist: {workspace}", file=sys.stderr)
        return 2

    inferred = infer_owner_repo(workspace, args.remote)
    owner = args.github_owner or (inferred[0] if inferred else "")
    repo = args.repo or (inferred[1] if inferred else workspace.name)
    base_url = (args.base_url or default_base_url(owner, repo)).rstrip("/")

    patch = {
        "workspace_role": "personal-learning-data",
        "student": {
            "display_name": args.student_name,
        },
        "github": {
            "owner": owner,
            "repo": repo,
        },
        "git_sync": {
            "remote": args.remote,
            "branch": args.branch,
            "commit_scope": DEFAULT_SYNC_SCOPE,
        },
        "pages": {
            "source": "github-actions",
            "base_url": base_url,
        },
    }

    if args.enable_git_sync or args.auto_sync:
        patch["git_sync"].update(
            {
                "enabled": True,
                "auto_pull_before_task": args.auto_sync,
                "auto_commit_after_task": args.auto_sync,
                "auto_push_after_task": args.auto_sync,
                "defer_push_after_grading": args.defer_push_after_grading,
                "sync_full_learning_data": args.sync_full_learning_data or args.auto_sync,
                "public_repository_accepted": args.public_repository_accepted,
            }
        )

    if args.enable_pages or args.auto_publish_pages:
        patch["pages"].update(
            {
                "enabled": True,
                "auto_publish_worksheets": args.auto_publish_pages,
            }
        )

    if args.enable_scheduled_tasks or args.auto_register_scheduled_tasks:
        patch["automation"] = {
            "enabled": True,
            "scheduler": "openclaw-cron",
            "auto_register_when_supported": args.auto_register_scheduled_tasks,
            "timezone": args.timezone,
            "allow_record_writes": args.allow_scheduled_record_writes,
            "allow_auto_worksheet_generation": args.allow_scheduled_worksheet_generation,
        }

    config = update_config(
        workspace,
        patch,
        student_name=args.student_name,
        remote=args.remote,
        branch=args.branch,
        owner=owner,
        repo=repo,
        timezone=args.timezone,
    )

    print(f"written: {workspace / '.zhizhi-math-coach' / 'config.json'}")
    print(f"workspace_role: {config.get('workspace_role')}")
    print(f"git_sync.enabled: {config.get('git_sync', {}).get('enabled')}")
    print(f"git_sync.auto_pull_before_task: {config.get('git_sync', {}).get('auto_pull_before_task')}")
    print(f"git_sync.auto_push_after_task: {config.get('git_sync', {}).get('auto_push_after_task')}")
    print(f"git_sync.defer_push_after_grading: {config.get('git_sync', {}).get('defer_push_after_grading')}")
    print(f"pages.enabled: {config.get('pages', {}).get('enabled')}")
    print(f"pages.auto_publish_worksheets: {config.get('pages', {}).get('auto_publish_worksheets')}")
    print(f"pages.base_url: {config.get('pages', {}).get('base_url')}")
    print(f"automation.enabled: {config.get('automation', {}).get('enabled')}")
    print(f"automation.auto_register_when_supported: {config.get('automation', {}).get('auto_register_when_supported')}")
    print(f"automation.timezone: {config.get('automation', {}).get('timezone')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
