#!/usr/bin/env python3
"""Publish worksheet HTML/PDF to GitHub Pages, push, then wait for the Pages action."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PUBLISH_SCRIPT = SCRIPT_DIR / "publish_html_site.py"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from learning_workspace_config import (  # noqa: E402
    configured_branch,
    configured_remote,
    load_config,
    pages_base_url,
)


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def fail(message: str) -> None:
    raise RuntimeError(message)


def git(args: list[str], workspace: Path) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], workspace)


def parse_remote_url(url: str) -> tuple[str, str] | None:
    patterns = [
        r"^git@github\.com:([^/]+)/(.+?)(?:\.git)?$",
        r"^git@([^:]+):([^/]+)/(.+?)(?:\.git)?$",
        r"^https://github\.com/([^/]+)/(.+?)(?:\.git)?$",
    ]
    for pattern in patterns:
        match = re.match(pattern, url.strip())
        if not match:
            continue
        groups = match.groups()
        if len(groups) == 2:
            return groups[0], groups[1]
        return groups[1], groups[2]
    return None


def infer_owner_repo(workspace: Path, remote: str) -> tuple[str, str]:
    result = git(["remote", "get-url", remote], workspace)
    if result.returncode != 0:
        fail(f"cannot infer GitHub repository because remote {remote!r} is not configured")
    parsed = parse_remote_url(result.stdout.strip())
    if parsed is None:
        fail(f"cannot parse GitHub remote URL: {result.stdout.strip()}")
    return parsed


def current_branch(workspace: Path) -> str:
    result = git(["branch", "--show-current"], workspace)
    if result.returncode != 0 or not result.stdout.strip():
        fail("cannot determine current git branch")
    return result.stdout.strip()


def remote_branch_exists(workspace: Path, remote: str, branch: str) -> bool:
    result = git(["rev-parse", "--verify", f"refs/remotes/{remote}/{branch}"], workspace)
    return result.returncode == 0


def pull_rebase_autostash(workspace: Path, remote: str, branch: str) -> None:
    fetch = git(["fetch", remote, branch], workspace)
    if fetch.returncode != 0:
        fail(fetch.stderr.strip() or fetch.stdout.strip() or f"git fetch {remote} {branch} failed")
    if not remote_branch_exists(workspace, remote, branch):
        print(f"ok: remote branch {remote}/{branch} does not exist yet; skipping pull")
        return
    pull = git(["pull", "--rebase", "--autostash", remote, branch], workspace)
    if pull.returncode != 0:
        fail(pull.stderr.strip() or pull.stdout.strip() or f"git pull --rebase --autostash {remote} {branch} failed")
    print(pull.stdout.strip() or pull.stderr.strip() or f"ok: pulled {remote}/{branch}")


def head_sha(workspace: Path) -> str:
    result = git(["rev-parse", "HEAD"], workspace)
    if result.returncode != 0:
        fail("cannot determine HEAD commit")
    return result.stdout.strip()


def staged_changes(workspace: Path) -> bool:
    result = git(["diff", "--cached", "--quiet"], workspace)
    return result.returncode != 0


def rel_paths(paths: list[Path], workspace: Path) -> list[str]:
    result = []
    for path in paths:
        if path.exists():
            result.append(path.resolve().relative_to(workspace.resolve()).as_posix())
    return result


def changed_publish_json_paths(workspace: Path) -> list[Path]:
    return sorted((workspace / "worksheets").glob("*/publish.json"))


def run_publish(workspace: Path, paths: list[str], base_url: str) -> list[str]:
    cmd = [
        sys.executable,
        str(PUBLISH_SCRIPT),
        *(paths or ["worksheets"]),
        "--workspace",
        str(workspace),
        "--base-url",
        base_url,
    ]
    result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        fail(f"publish_html_site.py failed: {detail}")

    links: list[str] = []
    for line in result.stdout.splitlines():
        if line.startswith("- ") and "http" in line:
            links.append(line.split(": ", 1)[-1].strip())
    return links


def http_json(url: str, timeout: int = 15) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "zhizhi-math-coach",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def url_ok(url: str, timeout: int = 15) -> bool:
    target = url + ("&" if "?" in url else "?") + f"t={int(time.time())}"
    request = urllib.request.Request(target, headers={"User-Agent": "zhizhi-math-coach"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return 200 <= response.status < 400
    except (urllib.error.URLError, TimeoutError):
        return False


def find_workflow_run(owner: str, repo: str, workflow: str, branch: str, sha: str) -> dict | None:
    workflow_q = urllib.parse.quote(workflow, safe="")
    url = (
        f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_q}/runs"
        f"?branch={urllib.parse.quote(branch)}&event=push&per_page=10"
    )
    data = http_json(url)
    for run_info in data.get("workflow_runs", []):
        if run_info.get("head_sha") == sha:
            return run_info
    return None


def wait_for_action(owner: str, repo: str, workflow: str, branch: str, sha: str, timeout_seconds: int, interval_seconds: int) -> dict:
    deadline = time.time() + timeout_seconds
    last_run: dict | None = None
    while time.time() < deadline:
        try:
            run_info = find_workflow_run(owner, repo, workflow, branch, sha)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            print(f"wait: GitHub Actions API not ready: {exc}")
            run_info = None
        if run_info:
            last_run = run_info
            status = run_info.get("status")
            conclusion = run_info.get("conclusion")
            html_url = run_info.get("html_url", "")
            print(f"wait: actions run {status}/{conclusion or 'pending'} {html_url}")
            if status == "completed":
                if conclusion == "success":
                    return run_info
                fail(f"GitHub Actions completed with conclusion={conclusion}: {html_url}")
        else:
            print("wait: actions run not visible yet")
        time.sleep(interval_seconds)
    if last_run:
        fail(f"timed out waiting for GitHub Actions: {last_run.get('html_url', '')}")
    fail("timed out waiting for GitHub Actions run to appear")


def wait_for_urls(urls: list[str], timeout_seconds: int, interval_seconds: int) -> None:
    if not urls:
        return
    deadline = time.time() + timeout_seconds
    pending = list(dict.fromkeys(urls))
    while pending and time.time() < deadline:
        still_pending = []
        for url in pending:
            if url_ok(url):
                print(f"ready: {url}")
            else:
                still_pending.append(url)
        pending = still_pending
        if pending:
            print(f"wait: pages URLs not ready yet: {len(pending)}")
            time.sleep(interval_seconds)
    if pending:
        fail(f"timed out waiting for Pages URLs: {', '.join(pending)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish child-facing worksheets to GitHub Pages and wait for deployment.")
    parser.add_argument("paths", nargs="*", help="Worksheet directories/files or roots to publish. Defaults to worksheets.")
    parser.add_argument("--workspace", type=Path, default=Path("."), help="Personal learning repository root.")
    parser.add_argument("--base-url", help="GitHub Pages base URL. Defaults to https://<owner>.github.io/<repo>.")
    parser.add_argument("--remote", help="Git remote name. Defaults to config git_sync.remote or origin.")
    parser.add_argument("--branch", help="Git branch. Defaults to config git_sync.branch or current branch.")
    parser.add_argument("--workflow", default="pages.yml", help="Workflow filename. Defaults to pages.yml.")
    parser.add_argument("--message", default="Publish worksheet pages", help="Commit message.")
    parser.add_argument("--timeout", type=int, default=360, help="Seconds to wait for GitHub Actions and Pages URLs.")
    parser.add_argument("--interval", type=int, default=10, help="Polling interval in seconds.")
    parser.add_argument("--no-push", action="store_true", help="Publish local files and commit, but do not push/wait.")
    parser.add_argument("--no-pull", action="store_true", help="Skip git pull --rebase --autostash before publishing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = args.workspace.resolve()
    if not workspace.exists():
        fail(f"workspace does not exist: {workspace}")

    config = load_config(workspace)
    remote = args.remote or configured_remote(config)
    owner, repo = infer_owner_repo(workspace, remote)
    branch = args.branch or configured_branch(config, workspace) or current_branch(workspace)
    base_url = args.base_url or pages_base_url(config) or f"https://{owner}.github.io/{repo}"

    if not args.no_pull:
        pull_rebase_autostash(workspace, remote, branch)

    links = run_publish(workspace, args.paths, base_url)
    add_paths = rel_paths(
        [
            workspace / "site",
            workspace / ".github" / "workflows" / args.workflow,
            *changed_publish_json_paths(workspace),
        ],
        workspace,
    )
    if not add_paths:
        fail("nothing public-safe to add; site/ was not generated")
    add_result = git(["add", *add_paths], workspace)
    if add_result.returncode != 0:
        fail(add_result.stderr.strip() or add_result.stdout.strip() or "git add failed")

    committed = False
    if staged_changes(workspace):
        commit_result = git(["commit", "-m", args.message], workspace)
        if commit_result.returncode != 0:
            fail(commit_result.stderr.strip() or commit_result.stdout.strip() or "git commit failed")
        committed = True
        print(commit_result.stdout.strip())
    else:
        print("ok: no public site changes to commit")

    sha = head_sha(workspace)
    if args.no_push:
        print("ok: --no-push set; skipping push and deployment wait")
        return 0

    push_result = git(["push", remote, branch], workspace)
    if push_result.returncode != 0:
        first_error = push_result.stderr.strip() or push_result.stdout.strip()
        if any(marker in first_error.lower() for marker in ["fetch first", "non-fast-forward", "rejected"]):
            print("wait: push rejected because remote changed; pulling with rebase and retrying")
            pull_rebase_autostash(workspace, remote, branch)
            push_result = git(["push", remote, branch], workspace)
        if push_result.returncode != 0:
            fail(push_result.stderr.strip() or push_result.stdout.strip() or "git push failed")
    print(push_result.stdout.strip() or push_result.stderr.strip())

    if committed:
        wait_for_action(owner, repo, args.workflow, branch, sha, args.timeout, args.interval)
    else:
        print("ok: no new commit; checking existing Pages URLs")

    urls = [base_url.rstrip("/") + "/", *links]
    wait_for_urls(urls, args.timeout, args.interval)

    print("pages-ready")
    print(base_url.rstrip("/") + "/")
    for link in links:
        print(link)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
