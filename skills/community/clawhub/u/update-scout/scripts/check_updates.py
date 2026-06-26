#!/usr/bin/env python3
"""
scout - check_updates.py
Polls GitHub releases for watched tools, compares against installed versions,
and outputs a structured update report.

Usage:
  python3 check_updates.py [--json] [--config /path/to/watchlist.json]

Config file: ~/.config/scout/watchlist.json (created on first run)

GitHub API rate limits: 60 req/hour unauthenticated. Set GITHUB_TOKEN env var
for 5,000 req/hour (use your own token — never stored by scout).
"""

import json
import os
import re
import shlex
import subprocess
import sys
import urllib.error
from dataclasses import dataclass, asdict
from typing import Optional

from scout_config import DEFAULT_WATCHLIST_PATH, DEFAULT_SKIP_PATH, github_request

DEFAULT_WATCHLIST = [
    {
        "name": "openclaw",
        "repo": "openclaw/openclaw",
        "detect": {"type": "command", "cmd": ["openclaw", "--version"]},
        "version_prefix": "v",
        "notes": "Core OpenClaw runtime"
    }
]


def load_skip_list(path: str) -> dict:
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def load_config(config_path: str):
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                data = json.load(f)
            if not isinstance(data, list):
                print(f"⚠️  Config at {config_path} is not a list — ignoring.", file=sys.stderr)
                return None
            return data
        except (json.JSONDecodeError, OSError) as e:
            print(f"⚠️  Could not read config {config_path}: {e}", file=sys.stderr)
            return None
    return None


def save_config(config_path: str, watchlist: list):
    dirpath = os.path.dirname(config_path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(watchlist, f, indent=2)


def detect_version_command(cmd: list) -> Optional[str]:
    if not cmd:
        return None
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        output = (result.stdout + result.stderr).strip()
        match = re.search(r'\b(\d+\.\d+[\.\d-]*)\b', output)
        # Return match or None — never return garbage like the first word
        return match.group(1) if match else None
    except FileNotFoundError:
        return None
    except Exception:
        return None


def detect_version_npm(package: str) -> Optional[str]:
    try:
        result = subprocess.run(
            ["npm", "list", "-g", "--depth=0", package],
            capture_output=True, text=True, timeout=10
        )
        match = re.search(rf'{re.escape(package)}@([\d\.\-]+)', result.stdout)
        return match.group(1) if match else None
    except Exception:
        return None


def detect_version_pip(package: str) -> Optional[str]:
    try:
        result = subprocess.run(
            ["pip", "show", package],
            capture_output=True, text=True, timeout=10
        )
        match = re.search(r'Version:\s*([\d\.\-]+)', result.stdout)
        return match.group(1) if match else None
    except Exception:
        return None


def detect_version_file(path: str, key: str = "version") -> Optional[str]:
    try:
        with open(os.path.expanduser(path)) as f:
            data = json.load(f)
        return data.get(key)
    except Exception:
        return None


def get_installed_version(tool: dict) -> Optional[str]:
    detect = tool.get("detect", {})
    dtype = detect.get("type", "command")
    if dtype == "command":
        cmd = detect.get("cmd", [])
        # Support both list and string forms
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)
        return detect_version_command(cmd)
    elif dtype == "npm_global":
        return detect_version_npm(detect.get("package", tool.get("name", "")))
    elif dtype == "pip":
        return detect_version_pip(detect.get("package", tool.get("name", "")))
    elif dtype == "file":
        return detect_version_file(detect.get("path", ""), detect.get("key", "version"))
    return None


def get_latest_release(repo: str) -> dict:
    return github_request(f"https://api.github.com/repos/{repo}/releases/latest")


def normalize_version(v: str, prefix: str) -> str:
    v = (v or "").strip()
    if prefix and v.startswith(prefix):
        v = v[len(prefix):]
    return v


def summarize_notes(body: str, max_chars: int = 500) -> str:
    if not body:
        return ""
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    summary = "\n".join(lines)
    return summary[:max_chars] + "..." if len(summary) > max_chars else summary


@dataclass
class UpdateResult:
    name: str
    installed: Optional[str]
    latest: Optional[str]
    up_to_date: bool
    update_available: bool
    release_url: Optional[str]
    release_notes_summary: Optional[str]
    published_at: Optional[str]
    error: Optional[str]


def check_tool(tool: dict) -> UpdateResult:
    name = tool.get("name", "(unnamed)")
    installed_raw = get_installed_version(tool)
    prefix = tool.get("version_prefix", "v")

    try:
        release = get_latest_release(tool.get("repo", ""))
    except urllib.error.HTTPError as e:
        msg = f"HTTP {e.code}: {tool.get('repo', '')}"
        if e.code == 403:
            msg += " (rate limited — set GITHUB_TOKEN for higher limits)"
        elif e.code == 404:
            msg += " (repo not found)"
        return UpdateResult(name=name, installed=installed_raw, latest=None,
                            up_to_date=False, update_available=False,
                            release_url=None, release_notes_summary=None,
                            published_at=None, error=msg)
    except Exception as e:
        return UpdateResult(name=name, installed=installed_raw, latest=None,
                            up_to_date=False, update_available=False,
                            release_url=None, release_notes_summary=None,
                            published_at=None, error=str(e))

    tag = release.get("tag_name", "")
    latest_norm = normalize_version(tag, prefix)
    installed_norm = normalize_version(installed_raw, prefix) if installed_raw else None
    up_to_date = installed_norm == latest_norm if installed_norm else False

    return UpdateResult(
        name=name,
        installed=installed_raw,
        latest=tag,
        up_to_date=up_to_date,
        update_available=bool(installed_norm) and not up_to_date,
        release_url=release.get("html_url"),
        release_notes_summary=summarize_notes(release.get("body", "")),
        published_at=(release.get("published_at") or "")[:10],
        error=None,
    )


def print_report(results: list):
    updates = [r for r in results if r.update_available]
    current = [r for r in results if r.up_to_date]
    errors = [r for r in results if r.error]

    print("=== Scout Update Report ===\n")

    if updates:
        print(f"🔔 Updates available ({len(updates)}):\n")
        for r in updates:
            print(f"  {r.name}  {r.installed} → {r.latest}  (released {r.published_at})")
            print(f"  Release: {r.release_url}")
            if r.release_notes_summary:
                preview = r.release_notes_summary.replace("\n", "\n    ")
                print(f"  Notes:\n    {preview}")
            print()
    else:
        print("✅ All tools are current.\n")

    if current:
        print(f"✅ Up to date: {', '.join(r.name for r in current)}")

    if errors:
        print(f"\n⚠️  Could not check: {', '.join(r.name + ' (' + (r.error or '') + ')' for r in errors)}")


def main():
    args = sys.argv[1:]
    as_json = "--json" in args
    config_path = DEFAULT_WATCHLIST_PATH
    if "--config" in args:
        idx = args.index("--config")
        if idx + 1 < len(args):
            config_path = args[idx + 1]

    watchlist = load_config(config_path)
    if watchlist is None:
        save_config(config_path, DEFAULT_WATCHLIST)
        watchlist = DEFAULT_WATCHLIST
        if not as_json:
            print(f"Created default config at {config_path}")
            print("Add more tools by editing that file or asking your agent to add them.\n")

    skip_list = load_skip_list(DEFAULT_SKIP_PATH)
    results = [check_tool(t) for t in watchlist]

    def is_skipped(r: UpdateResult) -> bool:
        entry = skip_list.get(r.name)
        if not entry or not isinstance(entry, dict):
            return False
        skipped_ver = normalize_version(entry.get("version", ""), "v")
        latest_ver = normalize_version(r.latest or "", "v")
        return bool(skipped_ver) and skipped_ver == latest_ver

    skipped = [r for r in results if r.update_available and is_skipped(r)]
    results = [r for r in results if not is_skipped(r)]

    if as_json:
        print(json.dumps([asdict(r) for r in results], indent=2))
    else:
        print_report(results)
        if skipped:
            print(f"\n⏭️  Skipped (use skip_release.py --list to review): {', '.join(r.name for r in skipped)}")


if __name__ == "__main__":
    main()
