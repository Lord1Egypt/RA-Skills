#!/usr/bin/env python3
"""Automatically pull, commit, and push a configured personal learning repository."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from learning_workspace_config import (  # noqa: E402
    configured_branch,
    configured_remote,
    load_config,
    scope_has_sensitive_paths,
)
from run_log import Timer, append_run_log, new_run_id  # noqa: E402


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def git(args: list[str], workspace: Path) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], workspace)


def fail(message: str) -> None:
    raise RuntimeError(message)


def detail(result: subprocess.CompletedProcess[str]) -> str:
    return result.stderr.strip() or result.stdout.strip()


def ensure_git_repo(workspace: Path) -> None:
    if shutil.which("git") is None:
        fail("git executable not found")
    inside = git(["rev-parse", "--is-inside-work-tree"], workspace)
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        fail(f"workspace is not a git repository: {workspace}")


def remote_branch_exists(workspace: Path, remote: str, branch: str) -> bool:
    result = git(["rev-parse", "--verify", f"refs/remotes/{remote}/{branch}"], workspace)
    return result.returncode == 0


def pull_rebase_autostash(workspace: Path, remote: str, branch: str) -> None:
    fetch = git(["fetch", remote, branch], workspace)
    if fetch.returncode != 0:
        fail(detail(fetch) or f"git fetch {remote} {branch} failed")
    if not remote_branch_exists(workspace, remote, branch):
        print(f"ok: remote branch {remote}/{branch} does not exist yet; skipping pull")
        return
    pull = git(["pull", "--rebase", "--autostash", remote, branch], workspace)
    if pull.returncode != 0:
        fail(detail(pull) or f"git pull --rebase --autostash {remote} {branch} failed")
    print(pull.stdout.strip() or pull.stderr.strip() or f"ok: pulled {remote}/{branch}")


def staged_changes(workspace: Path) -> bool:
    result = git(["diff", "--cached", "--quiet"], workspace)
    return result.returncode != 0


def stage_scope(workspace: Path, scope: list[str]) -> None:
    if not scope:
        fail("git_sync.commit_scope is empty")
    pathspecs = []
    for item in scope:
        if (workspace / item).exists():
            pathspecs.append(item)
            continue
        tracked = git(["ls-files", "--", item], workspace)
        if tracked.returncode == 0 and tracked.stdout.strip():
            pathspecs.append(item)
    if not pathspecs:
        print("ok: no configured sync paths exist in this workspace")
        return
    result = git(["add", "-A", "--", *pathspecs], workspace)
    if result.returncode != 0:
        fail(detail(result) or "git add failed")


def commit_if_needed(workspace: Path, message: str) -> bool:
    if not staged_changes(workspace):
        print("ok: no configured learning-data changes to commit")
        return False
    result = git(["commit", "-m", message], workspace)
    if result.returncode != 0:
        fail(detail(result) or "git commit failed")
    print(result.stdout.strip())
    return True


def push_with_retry(workspace: Path, remote: str, branch: str) -> None:
    push = git(["push", remote, branch], workspace)
    if push.returncode == 0:
        print(push.stdout.strip() or push.stderr.strip() or f"ok: pushed {remote}/{branch}")
        return

    first_error = detail(push)
    if any(marker in first_error.lower() for marker in ["fetch first", "non-fast-forward", "rejected"]):
        print("wait: push rejected because remote changed; pulling with rebase and retrying")
        pull_rebase_autostash(workspace, remote, branch)
        retry = git(["push", remote, branch], workspace)
        if retry.returncode == 0:
            print(retry.stdout.strip() or retry.stderr.strip() or f"ok: pushed {remote}/{branch}")
            return
        fail(detail(retry) or "git push failed after retry")

    fail(first_error or "git push failed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync a configured zhizhi-math-coach personal learning repository.")
    parser.add_argument("--workspace", type=Path, default=Path("."), help="Personal learning repository root.")
    parser.add_argument("--mode", choices=["before-task", "after-task"], default="after-task")
    parser.add_argument("--message", default="Update learning data", help="Commit message for after-task sync.")
    parser.add_argument("--remote", help="Override configured remote.")
    parser.add_argument("--branch", help="Override configured branch.")
    parser.add_argument("--task-kind", choices=["general", "grading", "worksheet", "publish", "review"], default="general")
    parser.add_argument("--run-id", default="", help="Optional run id for .zhizhi-math-coach/run-log.jsonl.")
    parser.add_argument("--no-log", action="store_true", help="Do not append run-log.jsonl.")
    parser.add_argument("--force", action="store_true", help="Run even when git_sync.enabled is false.")
    parser.add_argument("--no-pull", action="store_true", help="Skip pull/rebase.")
    parser.add_argument("--no-push", action="store_true", help="Commit but do not push.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    timer = Timer()
    workspace = args.workspace.resolve()
    run_id = args.run_id or new_run_id()
    ok = False
    skipped = ""
    committed = False
    pushed = False
    deferred_push = False
    try:
        config = load_config(workspace)
        if not config:
            skipped = "missing-config"
            print("skipped: .zhizhi-math-coach/config.json not found; automatic sync is not configured")
            ok = True
            return 0

        git_sync = config.get("git_sync", {})
        if not args.force and not git_sync.get("enabled"):
            skipped = "git-sync-disabled"
            print("skipped: git_sync.enabled is false")
            ok = True
            return 0

        ensure_git_repo(workspace)
        remote = args.remote or configured_remote(config)
        branch = args.branch or configured_branch(config, workspace)

        if args.mode == "before-task":
            if not args.no_pull and (args.force or git_sync.get("auto_pull_before_task")):
                pull_rebase_autostash(workspace, remote, branch)
            else:
                skipped = "auto-pull-disabled"
                print("skipped: auto_pull_before_task is false")
            ok = True
            return 0

        if not args.no_pull and (args.force or git_sync.get("auto_pull_before_task")):
            pull_rebase_autostash(workspace, remote, branch)

        scope = [str(item) for item in git_sync.get("commit_scope", [])]
        if scope_has_sensitive_paths(scope) and not git_sync.get("sync_full_learning_data"):
            fail("commit_scope includes learning records, but git_sync.sync_full_learning_data is false")
        if scope_has_sensitive_paths(scope) and not git_sync.get("public_repository_accepted"):
            fail("commit_scope includes learning records; set public_repository_accepted true or narrow commit_scope to site-only files")

        if not (args.force or git_sync.get("auto_commit_after_task")):
            skipped = "auto-commit-disabled"
            print("skipped: auto_commit_after_task is false")
            ok = True
            return 0

        stage_scope(workspace, scope)
        committed = commit_if_needed(workspace, args.message)

        if args.no_push:
            skipped = "no-push-arg"
            print("ok: --no-push set; skipping push")
            ok = True
            return 0

        if args.task_kind == "grading" and git_sync.get("defer_push_after_grading"):
            deferred_push = True
            if committed:
                print("ok: defer_push_after_grading is true; grading commit remains local for later sync")
            else:
                print("ok: defer_push_after_grading is true; no push needed because nothing was committed")
            ok = True
            return 0

        if args.force or git_sync.get("auto_push_after_task"):
            push_with_retry(workspace, remote, branch)
            pushed = True
        elif committed:
            skipped = "auto-push-disabled"
            print("skipped: auto_push_after_task is false; commit remains local")
        ok = True
        return 0
    finally:
        if not args.no_log:
            append_run_log(
                workspace,
                {
                    "run_id": run_id,
                    "script": "sync_learning_repo.py",
                    "mode": args.mode,
                    "task_kind": args.task_kind,
                    "ok": ok,
                    "skipped": skipped,
                    "committed": committed,
                    "pushed": pushed,
                    "deferred_push": deferred_push,
                    "duration_ms": timer.elapsed_ms(),
                },
            )


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
