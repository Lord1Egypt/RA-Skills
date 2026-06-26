#!/usr/bin/env python3
"""Check if a newer version of the skill is available.

Works in two modes:
1. Git repo: compare local HEAD with remote via git fetch / ls-remote
2. Non-git install: read commit_hash from SKILL.md and compare with GitHub API

Usage:
    python3 check_update.py --skill-dir /path/to/skill
"""

import argparse
import json
import os
import re
import sys
import subprocess
import urllib.request
import urllib.error

GITHUB_REPO = "Atlas-Of-Imagination/virse-skill"
GITHUB_BRANCH = "main"


def read_local_hash_from_skill_md(skill_dir: str) -> str | None:
    """Read commit_hash from SKILL.md frontmatter."""
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return None
    try:
        with open(skill_md, "r") as f:
            content = f.read(2048)  # frontmatter is near the top
        m = re.search(r"^commit_hash:\s*(\S+)", content, re.MULTILINE)
        if m:
            h = m.group(1)
            # Ignore placeholder values
            if h in ("old", "unknown", "none", ""):
                return None
            return h
        return None
    except Exception:
        return None


def get_remote_hash_github() -> str | None:
    """Get latest commit hash from GitHub API (no git required)."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/commits/{GITHUB_BRANCH}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "virse-skill-updater",
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("sha")
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, OSError):
        return None


def get_remote_hash_git(skill_dir: str) -> str | None:
    """Get latest remote hash via git (fetch then rev-parse, fallback to ls-remote)."""
    # Try fetch + rev-parse
    try:
        fetch = subprocess.run(
            ["git", "-C", skill_dir, "fetch", "origin", GITHUB_BRANCH, "--quiet"],
            capture_output=True, text=True, timeout=30,
        )
        if fetch.returncode == 0:
            rev = subprocess.run(
                ["git", "-C", skill_dir, "rev-parse", f"origin/{GITHUB_BRANCH}"],
                capture_output=True, text=True, timeout=5,
            )
            if rev.returncode == 0:
                return rev.stdout.strip()
    except (subprocess.TimeoutExpired, OSError):
        pass

    # Fallback: ls-remote
    try:
        ls = subprocess.run(
            ["git", "-C", skill_dir, "ls-remote", "origin", f"refs/heads/{GITHUB_BRANCH}"],
            capture_output=True, text=True, timeout=15,
        )
        if ls.returncode == 0 and ls.stdout.strip():
            return ls.stdout.strip().split()[0]
    except (subprocess.TimeoutExpired, OSError):
        pass

    return None


def get_local_hash_git(skill_dir: str) -> str | None:
    """Get local HEAD hash via git."""
    try:
        result = subprocess.run(
            ["git", "-C", skill_dir, "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, OSError):
        pass
    return None


def main():
    parser = argparse.ArgumentParser(description="Check for skill updates")
    parser.add_argument("--skill-dir", required=True, help="Path to the skill directory")
    args = parser.parse_args()

    skill_dir = args.skill_dir

    if not skill_dir or not os.path.isdir(skill_dir):
        print("check_failed")
        print(f"[update-check] skill-dir does not exist: {skill_dir!r}", file=sys.stderr)
        return

    is_git_repo = os.path.isdir(os.path.join(skill_dir, ".git"))

    try:
        # --- Determine local version ---
        local_hash = None
        if is_git_repo:
            local_hash = get_local_hash_git(skill_dir)

        if local_hash is None:
            # Non-git install or git failed: read from SKILL.md frontmatter
            local_hash = read_local_hash_from_skill_md(skill_dir)

        if local_hash is None:
            print("check_failed")
            print("[update-check] cannot determine local version (no .git and no commit_hash in SKILL.md)", file=sys.stderr)
            return

        # --- Determine remote version ---
        remote_hash = None
        if is_git_repo:
            remote_hash = get_remote_hash_git(skill_dir)

        if remote_hash is None:
            # Fallback to GitHub API (works without git)
            remote_hash = get_remote_hash_github()

        if remote_hash is None:
            print("check_failed")
            print("[update-check] cannot reach remote (both git and GitHub API failed)", file=sys.stderr)
            return

        # --- Compare ---
        # Normalize: compare short hashes if local is short (from SKILL.md)
        if len(local_hash) < 12:
            # local_hash is short, compare prefixes
            match = remote_hash[:len(local_hash)] == local_hash
        else:
            match = remote_hash == local_hash

        if not match:
            short_remote = remote_hash[:7]
            print(f"update_available|{short_remote}")
        else:
            print("up_to_date")

    except Exception as e:
        print("check_failed")
        print(f"[update-check] unexpected error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
