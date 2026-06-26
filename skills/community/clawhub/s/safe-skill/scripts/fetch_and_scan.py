#!/usr/bin/env python3
"""
fetch_and_scan.py — Download an AI agent skill and run security analysis.

Supports:
  - GitHub repo/directory URLs
  - ClawHub skill slugs (author/skill-name)
  - GitHub API paths (repos/owner/repo/contents/path)
  - Local directories or files (passthrough)

Usage:
    python3 fetch_and_scan.py <source> [scan.py options...]

Examples:
    # GitHub tree URL
    python3 fetch_and_scan.py https://github.com/openclaw/skills/tree/main/skills/spclaudehome/skill-vetter

    # ClawHub slug
    python3 fetch_and_scan.py clawhub:spclaudehome/skill-vetter

    # GitHub shorthand (owner/repo/path)
    python3 fetch_and_scan.py github:openclaw/skills/skills/spclaudehome/skill-vetter

    # JSON output
    python3 fetch_and_scan.py clawhub:spclaudehome/skill-vetter --json

    # With explicit whitelist
    python3 fetch_and_scan.py clawhub:spclaudehome/skill-vetter -w my_whitelist.json

Zero external dependencies. Python 3.8+ stdlib only.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional, Tuple, List


# ============================================================
# Source Parsing
# ============================================================

def parse_source(source: str) -> Tuple[str, dict]:
    """
    Parse a source string into (type, params).
    Returns: ("github_tree", {"owner": ..., "repo": ..., "branch": ..., "path": ...})
             ("github_api",  {"owner": ..., "repo": ..., "path": ...})
             ("clawhub",     {"author": ..., "skill": ...})
             ("local",       {"path": ...})
    """
    # ClawHub slug: clawhub:author/skill-name
    if source.startswith("clawhub:"):
        slug = source[len("clawhub:"):]
        parts = slug.strip("/").split("/")
        if len(parts) == 2:
            return "clawhub", {"author": parts[0], "skill": parts[1]}
        raise ValueError(f"Invalid ClawHub slug: {slug} (expected author/skill-name)")

    # GitHub shorthand: github:owner/repo/path/to/skill
    if source.startswith("github:"):
        rest = source[len("github:"):]
        parts = rest.strip("/").split("/")
        if len(parts) < 2:
            raise ValueError(f"Invalid GitHub shorthand: {rest} (need at least owner/repo)")
        owner, repo = parts[0], parts[1]
        path = "/".join(parts[2:]) if len(parts) > 2 else ""
        return "github_api", {"owner": owner, "repo": repo, "path": path}

    # GitHub tree URL: https://github.com/owner/repo/tree/branch/path
    gh_tree = re.match(
        r'https?://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.*)',
        source
    )
    if gh_tree:
        return "github_tree", {
            "owner": gh_tree.group(1),
            "repo": gh_tree.group(2),
            "branch": gh_tree.group(3),
            "path": gh_tree.group(4).rstrip("/"),
        }

    # GitHub blob URL: https://github.com/owner/repo/blob/branch/path
    gh_blob = re.match(
        r'https?://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.*)',
        source
    )
    if gh_blob:
        return "github_tree", {
            "owner": gh_blob.group(1),
            "repo": gh_blob.group(2),
            "branch": gh_blob.group(3),
            "path": gh_blob.group(4).rstrip("/"),
        }

    # Raw GitHub URL
    gh_raw = re.match(
        r'https?://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)/(.*)',
        source
    )
    if gh_raw:
        return "github_tree", {
            "owner": gh_raw.group(1),
            "repo": gh_raw.group(2),
            "branch": gh_raw.group(3),
            "path": gh_raw.group(4).rstrip("/"),
        }

    # Local path
    if os.path.exists(source):
        return "local", {"path": source}

    # Try as GitHub URL without /tree/
    gh_repo = re.match(r'https?://github\.com/([^/]+)/([^/]+)/?$', source)
    if gh_repo:
        return "github_api", {
            "owner": gh_repo.group(1),
            "repo": gh_repo.group(2),
            "path": "",
        }

    raise ValueError(
        f"Cannot parse source: {source}\n"
        f"Expected: GitHub URL, clawhub:author/skill, github:owner/repo/path, or local path"
    )


# ============================================================
# GitHub API Fetcher
# ============================================================

def github_api_get(url: str) -> dict:
    """Make a GitHub API request. Returns parsed JSON."""
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "skill-vetter-pro/0.3.0")

    # Use GITHUB_TOKEN if available
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        req.add_header("Authorization", f"token {token}")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("Error: GitHub API rate limit exceeded. Set GITHUB_TOKEN env var.", file=sys.stderr)
        elif e.code == 404:
            print(f"Error: Not found: {url}", file=sys.stderr)
        else:
            print(f"Error: GitHub API returned {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Network error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def download_raw(url: str) -> bytes:
    """Download raw file content."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "skill-vetter-pro/0.3.0")
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        req.add_header("Authorization", f"token {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except Exception as e:
        print(f"Warning: Failed to download {url}: {e}", file=sys.stderr)
        return b""


def fetch_github_directory(owner: str, repo: str, path: str, branch: str = "main",
                           dest_dir: str = ".") -> str:
    """
    Recursively download a GitHub directory using the Contents API.
    Returns the local path where files were saved.
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    if branch:
        api_url += f"?ref={branch}"

    data = github_api_get(api_url)

    # Single file
    if isinstance(data, dict):
        if data.get("type") == "file":
            content = download_raw(data["download_url"])
            filepath = os.path.join(dest_dir, data["name"])
            os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(content)
            return filepath
        return dest_dir

    # Directory listing
    if isinstance(data, list):
        for item in data:
            if item["type"] == "file":
                content = download_raw(item["download_url"])
                filepath = os.path.join(dest_dir, item["name"])
                with open(filepath, 'wb') as f:
                    f.write(content)
                print(f"  ↓ {item['path']}", file=sys.stderr)
            elif item["type"] == "dir":
                subdir = os.path.join(dest_dir, item["name"])
                os.makedirs(subdir, exist_ok=True)
                fetch_github_directory(
                    owner, repo, item["path"], branch=branch, dest_dir=subdir
                )
    return dest_dir


# ============================================================
# ClawHub Fetcher
# ============================================================

def fetch_clawhub(author: str, skill: str, dest_dir: str) -> str:
    """
    Fetch a skill from ClawHub via the openclaw/skills GitHub repo.
    ClawHub skills are stored at: skills/{author}/{skill}/SKILL.md
    """
    print(f"  Fetching from ClawHub: {author}/{skill}", file=sys.stderr)
    return fetch_github_directory(
        owner="openclaw",
        repo="skills",
        path=f"skills/{author}/{skill}",
        branch="main",
        dest_dir=dest_dir,
    )


# ============================================================
# Main Orchestrator
# ============================================================

def fetch_skill(source: str) -> Tuple[str, bool]:
    """
    Fetch a skill from the given source.
    Returns: (local_path, is_temp) — is_temp=True means caller should cleanup.
    """
    source_type, params = parse_source(source)

    if source_type == "local":
        return params["path"], False

    # Create temp directory
    tmp_dir = tempfile.mkdtemp(prefix="skill-vetter-")

    if source_type == "clawhub":
        print(f"Fetching skill from ClawHub: {params['author']}/{params['skill']}", file=sys.stderr)
        fetch_clawhub(params["author"], params["skill"], tmp_dir)
        return tmp_dir, True

    if source_type in ("github_tree", "github_api"):
        owner = params["owner"]
        repo = params["repo"]
        path = params.get("path", "")
        branch = params.get("branch", "main")
        print(f"Fetching from GitHub: {owner}/{repo}/{path} (branch: {branch})", file=sys.stderr)
        fetch_github_directory(owner, repo, path, branch=branch, dest_dir=tmp_dir)
        return tmp_dir, True

    raise ValueError(f"Unknown source type: {source_type}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    source = sys.argv[1]
    extra_args = sys.argv[2:]

    # Determine scanner script path
    script_dir = Path(__file__).parent
    scanner = script_dir / "scan.py"
    if not scanner.exists():
        print(f"Error: scan.py not found at {scanner}", file=sys.stderr)
        sys.exit(1)

    # Fetch
    try:
        local_path, is_temp = fetch_skill(source)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning: {local_path}", file=sys.stderr)
    print("", file=sys.stderr)

    # List fetched files
    local_p = Path(local_path)
    if local_p.is_dir():
        files = list(local_p.rglob('*'))
        file_count = sum(1 for f in files if f.is_file())
        print(f"Downloaded {file_count} files to {local_path}", file=sys.stderr)
        print("", file=sys.stderr)

    # Run scanner
    try:
        cmd = [sys.executable, str(scanner), local_path] + extra_args
        result = subprocess.run(cmd, capture_output=False)
        exit_code = result.returncode
    except Exception as e:
        print(f"Error running scanner: {e}", file=sys.stderr)
        exit_code = 1
    finally:
        # Cleanup temp directory
        if is_temp:
            shutil.rmtree(local_path, ignore_errors=True)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
