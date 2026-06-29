#!/usr/bin/env python3
"""Stage 1: prepare a repository for analysis.

Accepts EITHER:
  * a public GitHub URL  →  shallow-clones it into ./workspace/
  * a local directory path (absolute or relative) → uses it in-place

For local paths, tries to recover GitHub coordinates (owner / repo /
commit_sha / branch) from `.git/`, so downstream renderers can still
emit clickable `path:line#L<n>` permalinks. If the directory is not a
git repo, evidence is rendered as plain code instead of links — the
report still works.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

MAX_SIZE_MB = 500
GITHUB_URL_RE = re.compile(
    r"^https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?(?:/tree/([^/]+))?/?$"
)
# Match GitHub remotes in either HTTPS or SSH form.
GITHUB_REMOTE_RE = re.compile(
    r"(?:git@github\.com:|https?://github\.com/)([^/]+)/([^/.]+?)(?:\.git)?/?$"
)


# ---------------------------------------------------------------------------
# input classification
# ---------------------------------------------------------------------------

def is_github_url(s: str) -> bool:
    return s.startswith(("http://", "https://")) and "github.com" in s


def parse_url(url: str):
    m = GITHUB_URL_RE.match(url.strip())
    if not m:
        sys.exit(f"ERROR: not a github.com URL: {url}")
    owner, repo, branch = m.group(1), m.group(2), m.group(3)
    return owner, repo, branch


# ---------------------------------------------------------------------------
# remote-mode helpers
# ---------------------------------------------------------------------------

def fetch_meta(owner: str, repo: str) -> dict:
    api = f"https://api.github.com/repos/{owner}/{repo}"
    req = urllib.request.Request(api, headers={"User-Agent": "repo-explainer"})
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        return {
            "full_name": data.get("full_name"),
            "description": data.get("description"),
            "stars": data.get("stargazers_count"),
            "language": data.get("language"),
            "default_branch": data.get("default_branch"),
            "size_kb": data.get("size"),
            "topics": data.get("topics", []),
            "html_url": data.get("html_url"),
            "license": (data.get("license") or {}).get("spdx_id"),
        }
    except Exception as e:
        return {"error": str(e), "full_name": f"{owner}/{repo}"}


def clone(owner: str, repo: str, branch: str | None, workdir: Path):
    target = workdir / f"{owner}__{repo}"
    if target.exists():
        subprocess.run(["rm", "-rf", str(target)], check=True)
    cmd = ["git", "clone", "--depth=1"]
    if branch:
        cmd += ["--branch", branch]
    cmd += [f"https://github.com/{owner}/{repo}.git", str(target)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ERROR: git clone failed: {r.stderr}")
    du = subprocess.run(["du", "-sm", str(target)], capture_output=True, text=True)
    size_mb = int(du.stdout.split()[0])
    if size_mb > MAX_SIZE_MB:
        sys.exit(
            f"ERROR: repo size {size_mb}MB exceeds limit {MAX_SIZE_MB}MB. "
            "Re-run with --subpath to focus on a sub-directory."
        )
    sha = subprocess.run(
        ["git", "-C", str(target), "rev-parse", "HEAD"],
        capture_output=True, text=True
    ).stdout.strip()
    return target, sha, size_mb


# ---------------------------------------------------------------------------
# local-mode helpers
# ---------------------------------------------------------------------------

def _git(path: Path, *args: str) -> str | None:
    """Run a git command inside *path*; return stdout (stripped) or None."""
    r = subprocess.run(
        ["git", "-C", str(path), *args],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return None
    return r.stdout.strip() or None


def inspect_local(path: Path) -> dict:
    """Resolve owner / repo / sha / branch from a local directory.

    All four fields are optional. When the directory is not a git repo
    (or has no GitHub remote), the missing fields are returned as None
    and the downstream renderers will degrade gracefully to plain-code
    evidence (no clickable links).
    """
    info: dict[str, str | None] = {
        "owner": None,
        "repo": None,
        "branch": None,
        "commit_sha": None,
        "remote_url": None,
    }
    if not (path / ".git").exists():
        return info

    sha = _git(path, "rev-parse", "HEAD")
    if sha:
        info["commit_sha"] = sha

    branch = _git(path, "rev-parse", "--abbrev-ref", "HEAD")
    if branch and branch != "HEAD":
        info["branch"] = branch

    # Prefer `origin`; fall back to the first available remote.
    remote = _git(path, "remote", "get-url", "origin")
    if not remote:
        remotes = _git(path, "remote") or ""
        for name in remotes.splitlines():
            r = _git(path, "remote", "get-url", name.strip())
            if r:
                remote = r
                break
    if remote:
        info["remote_url"] = remote
        m = GITHUB_REMOTE_RE.search(remote)
        if m:
            info["owner"], info["repo"] = m.group(1), m.group(2)
    return info


def prepare_local(raw_path: str) -> tuple[Path, dict, int]:
    """Validate the local path, enforce size limit, harvest git metadata."""
    path = Path(raw_path).expanduser().resolve()
    if not path.is_dir():
        sys.exit(f"ERROR: not a directory: {path}")

    du = subprocess.run(
        ["du", "-sm", "--exclude=.git", "--exclude=node_modules",
         "--exclude=venv", "--exclude=.venv", "--exclude=__pycache__",
         "--exclude=dist", "--exclude=build", "--exclude=target",
         str(path)],
        capture_output=True, text=True,
    )
    try:
        size_mb = int(du.stdout.split()[0])
    except Exception:
        size_mb = 0
    if size_mb > MAX_SIZE_MB:
        sys.exit(
            f"ERROR: local dir {size_mb}MB exceeds limit {MAX_SIZE_MB}MB. "
            "Re-run with --subpath to focus on a sub-directory."
        )
    return path, inspect_local(path), size_mb


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description=(
            "Stage 1 — fetch a repo for analysis. Accepts a GitHub URL "
            "(shallow-cloned into ./workspace/) OR a local directory "
            "(analyzed in-place; GitHub coordinates auto-detected from "
            ".git/config when present)."
        )
    )
    ap.add_argument(
        "source",
        help="GitHub URL (https://github.com/owner/repo[/tree/branch]) OR "
             "a local directory path (absolute or relative)."
    )
    ap.add_argument("--subpath", default=None)
    ap.add_argument("--workdir", default="./workspace")
    ap.add_argument(
        "--local",
        action="store_true",
        help="Force local-directory mode even if 'source' looks URL-ish. "
             "Auto-detected when omitted."
    )
    args = ap.parse_args()

    # ---- mode detection: explicit flag > URL pattern > path-exists -------
    looks_like_url = is_github_url(args.source)
    use_local = args.local or (not looks_like_url and Path(args.source).expanduser().exists())

    if use_local:
        target, ginfo, size_mb = prepare_local(args.source)
        out = {
            "mode": "local",
            "owner": ginfo["owner"],
            "repo": ginfo["repo"],
            "branch": ginfo["branch"],
            "commit_sha": ginfo["commit_sha"],
            "local_path": str(target),
            "subpath": args.subpath,
            "size_mb": size_mb,
            "github_meta": {
                "remote_url": ginfo["remote_url"],
                "primary_language": None,
            },
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    # ---- remote mode -----------------------------------------------------
    owner, repo, branch = parse_url(args.source)
    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)

    meta = fetch_meta(owner, repo)
    target, sha, size_mb = clone(owner, repo, branch, workdir)

    out = {
        "mode": "remote",
        "owner": owner,
        "repo": repo,
        "branch": branch or meta.get("default_branch"),
        "commit_sha": sha,
        "local_path": str(target),
        "subpath": args.subpath,
        "size_mb": size_mb,
        "github_meta": meta,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
