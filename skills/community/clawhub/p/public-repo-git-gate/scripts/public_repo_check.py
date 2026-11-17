#!/usr/bin/env python3
"""Check Git content and branch state before a public commit, push, or PR."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


DEFAULT_FORBIDDEN_PATHS = [
    r"(^|/)(?:internal|private|legal|commercial|finance|billing|entitlement|secrets?)(?:/|$)",
    r"(^|/)(?:\.env|\.vercel|\.supabase|\.codex|\.agents|\.claude)(?:[/.]|$)",
    r"(^|/)(?:production|prod|customer|user-data|exports?)(?:[-_][^/]*)?\.(?:csv|json|sql|dump|db|sqlite|zip)$",
    r"(^|/)(?:ROADMAP|TODO)(?:\.[^/]*)?$",
]
_PRIVATE_KEY_HEADER_PATTERN = "".join(
    (
        r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE ",
        r"KEY-----",
    )
)
DEFAULT_SECRET_PATTERNS = [
    _PRIVATE_KEY_HEADER_PATTERN,
    r"(?:sk-(?:proj-)?|gh[pousr]_)[A-Za-z0-9_-]{12,}",
    r"sb_secret_[A-Za-z0-9_-]{8,}",
    r"postgres(?:ql)?://[^\s:'\"]+:[^\s@'\"]+@",
]


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", "replace").strip() or f"git {' '.join(args)} failed")
    return result.stdout.decode("utf-8", "replace")


def git_paths(repo: Path, staged: bool, changed_since: str | None) -> list[str]:
    if changed_since:
        args = ["diff", "--name-only", "--diff-filter=ACMRTUXB", "-z", f"{changed_since}...HEAD"]
    elif staged:
        args = ["diff", "--cached", "--name-only", "--diff-filter=ACMRTUXB", "-z"]
    else:
        args = ["ls-files", "--cached", "--others", "--exclude-standard", "-z"]
    return [path for path in git(repo, *args).split("\0") if path]


def read_content(repo: Path, path: str, staged: bool) -> bytes:
    if staged:
        result = subprocess.run(
            ["git", "-C", str(repo), "show", f":{path}"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode:
            return b""
        return result.stdout
    return (repo / path).read_bytes()


def load_config(path: Path | None) -> dict:
    if not path:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def scan_paths(repo: Path, paths: Iterable[str], staged: bool, config: dict) -> list[str]:
    forbidden_paths = [*DEFAULT_FORBIDDEN_PATHS, *config.get("forbidden_paths", [])]
    secret_patterns = [*DEFAULT_SECRET_PATTERNS, *config.get("forbidden_terms", [])]
    path_rules = [re.compile(rule, re.IGNORECASE) for rule in forbidden_paths]
    secret_rules = [re.compile(rule, re.IGNORECASE) for rule in secret_patterns]
    findings: list[str] = []

    for raw_path in paths:
        path = raw_path.replace("\\", "/")
        if any(rule.search(path) for rule in path_rules):
            findings.append(f"{path}: forbidden public-repository path")
            continue
        try:
            data = read_content(repo, raw_path, staged)
        except OSError as error:
            findings.append(f"{path}: cannot read candidate ({error})")
            continue
        if b"\0" in data:
            continue
        text = data.decode("utf-8", "replace")
        if any(rule.search(text) for rule in secret_rules):
            findings.append(f"{path}: possible secret or credential")

    return findings


def check_remote(repo: Path) -> list[str]:
    findings: list[str] = []
    remotes = git(repo, "remote", check=False).split()
    for remote in remotes:
        url = git(repo, "remote", "get-url", remote, check=False).strip()
        if re.search(r"https?://[^/\s:]+:[^@\s]+@", url):
            findings.append(f"remote {remote}: URL contains embedded credentials")
        print(f"remote {remote}: {url}")
    if not remotes:
        findings.append("repository has no configured remote")
    return findings


def check_repo(repo: Path, staged: bool, changed_since: str | None, require_feature_branch: bool,
               check_remote_flag: bool, config: dict) -> list[str]:
    findings: list[str] = []
    branch = git(repo, "branch", "--show-current").strip()
    if not branch:
        findings.append("repository is in detached HEAD state")
    if require_feature_branch and branch in {"main", "master"}:
        findings.append(f"current branch {branch} is protected; use a feature branch and PR")

    if staged and not changed_since:
        diff_check = subprocess.run(
            ["git", "-C", str(repo), "diff", "--cached", "--check"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if diff_check.returncode:
            findings.append("staged diff has whitespace errors:\n" + diff_check.stdout.decode("utf-8", "replace").strip())

    paths = git_paths(repo, staged, changed_since)
    print(f"branch: {branch or '(detached)'}")
    scope = "staged" if staged else (f"changed since {changed_since}" if changed_since else "tracked/untracked")
    print(f"checking {len(paths)} {scope} candidate paths")
    findings.extend(scan_paths(repo, paths, staged, config))
    if check_remote_flag:
        findings.extend(check_remote(repo))
    return sorted(set(findings))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--staged", action="store_true", help="scan only the current index")
    scope.add_argument("--all", action="store_true", help="scan tracked and non-ignored untracked candidates")
    scope.add_argument("--changed-since", metavar="REF", help="scan paths changed between REF and HEAD")
    parser.add_argument("--require-feature-branch", action="store_true")
    parser.add_argument("--check-remote", action="store_true")
    parser.add_argument("--config", type=Path)
    args = parser.parse_args()

    repo = args.repo.resolve()
    if not (repo / ".git").exists() and not (repo / ".git").is_file():
        print(f"not a Git repository: {repo}", file=sys.stderr)
        return 2
    try:
        findings = check_repo(repo, staged=args.staged, changed_since=args.changed_since,
                              require_feature_branch=args.require_feature_branch,
                              check_remote_flag=args.check_remote, config=load_config(args.config))
    except (OSError, RuntimeError, json.JSONDecodeError) as error:
        print(f"public repository check could not run: {error}", file=sys.stderr)
        return 2
    if findings:
        print("Public repository Git gate failed:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1
    print("Public repository Git gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
