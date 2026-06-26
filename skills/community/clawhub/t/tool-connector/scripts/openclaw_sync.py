#!/usr/bin/env python3
"""
Sync SSO tokens from ~/.openclaw/tool-connector.env into
~/.openclaw/openclaw.json under skills.entries.tool-connector.env.

OpenClaw injects those env vars automatically at the start of each agent run,
so tokens captured by playwright_sso.py are available without sourcing .env.

Usage:
    python3 scripts/openclaw_sync.py                    # sync all tokens
    python3 scripts/openclaw_sync.py --refresh-slack    # refresh Slack SSO first, then sync
    python3 scripts/openclaw_sync.py --refresh-outlook  # refresh Outlook SSO first, then sync
    python3 scripts/openclaw_sync.py --refresh-grafana  # refresh Grafana SSO first, then sync
    python3 scripts/openclaw_sync.py --refresh-teams    # refresh Teams SSO first, then sync
    python3 scripts/openclaw_sync.py --refresh-gdrive   # refresh Google Drive SSO first, then sync
    python3 scripts/openclaw_sync.py --refresh-all      # refresh all SSO sessions, then sync
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ENV_FILE = Path.home() / ".openclaw" / "tool-connector.env"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
SSO_SCRIPT = Path(__file__).parent / "shared_utils" / "playwright_sso.py"

# All env var keys managed by playwright_sso.py
SSO_ENV_KEYS = [
    "GRAFANA_SESSION",
    "SLACK_XOXC",
    "SLACK_D_COOKIE",
    "GDRIVE_COOKIES",
    "GDRIVE_SAPISID",
    "TEAMS_SKYPETOKEN",
    "TEAMS_SESSION_ID",
    "GRAPH_ACCESS_TOKEN",
    "OWA_ACCESS_TOKEN",
]


def read_env_file(path: Path) -> dict[str, str]:
    """Read key=value pairs from a .env file."""
    result = {}
    if not path.exists():
        return result
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        result[key.strip()] = value.strip()
    return result


def read_openclaw_config(path: Path) -> dict:
    """Read ~/.openclaw/openclaw.json, tolerating JSON5-style comments."""
    if not path.exists():
        return {}
    text = path.read_text()
    # Strip // line comments (simple JSON5 compat — sufficient for openclaw.json)
    import re
    text = re.sub(r"//[^\n]*", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"Warning: could not parse {path} as JSON — will create a fresh structure.")
        return {}


def write_openclaw_config(path: Path, config: dict) -> None:
    """Write config back as JSON (pretty-printed)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=2) + "\n")


def sync_tokens_to_openclaw(tokens: dict[str, str]) -> None:
    """Patch skills.entries.tool-connector.env in openclaw.json with the given tokens.

    This function ONLY writes under config["skills"]["entries"]["tool-connector"]["env"].
    It does not read, modify, or delete any other keys in openclaw.json.
    """
    if not tokens:
        print("No tokens to sync.")
        return

    config = read_openclaw_config(OPENCLAW_CONFIG)

    # Only touch skills.entries.tool-connector — nothing else in openclaw.json
    config.setdefault("skills", {})
    config["skills"].setdefault("entries", {})
    config["skills"]["entries"].setdefault("tool-connector", {})
    config["skills"]["entries"]["tool-connector"].setdefault("env", {})

    env_block = config["skills"]["entries"]["tool-connector"]["env"]
    updated = []
    for key, value in tokens.items():
        if value:
            env_block[key] = value
            updated.append(key)

    write_openclaw_config(OPENCLAW_CONFIG, config)
    print(f"Synced to {OPENCLAW_CONFIG}:")
    for key in updated:
        print(f"  {key}: {tokens[key][:40]}...")


def run_sso_refresh(flag: str) -> None:
    """Run playwright_sso.py with the given --*-only flag."""
    cmd = [sys.executable, str(SSO_SCRIPT), "--env-file", str(ENV_FILE), flag]
    print(f"Running SSO refresh: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"SSO refresh failed (exit {result.returncode})")
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--refresh-slack",   action="store_true", help="Refresh Slack SSO before syncing")
    parser.add_argument("--refresh-outlook", action="store_true", help="Refresh Outlook/M365 SSO before syncing")
    parser.add_argument("--refresh-grafana", action="store_true", help="Refresh Grafana SSO before syncing")
    parser.add_argument("--refresh-teams",   action="store_true", help="Refresh Microsoft Teams SSO before syncing")
    parser.add_argument("--refresh-gdrive",  action="store_true", help="Refresh Google Drive SSO before syncing")
    parser.add_argument("--refresh-all",     action="store_true", help="Refresh all SSO sessions before syncing")
    args = parser.parse_args()

    # Run requested SSO refreshes first
    if args.refresh_all:
        run_sso_refresh("--slack-only")
        run_sso_refresh("--outlook-only")
        run_sso_refresh("--grafana-only")
        run_sso_refresh("--teams-only")
        run_sso_refresh("--gdrive-only")
    else:
        if args.refresh_slack:
            run_sso_refresh("--slack-only")
        if args.refresh_outlook:
            run_sso_refresh("--outlook-only")
        if args.refresh_grafana:
            run_sso_refresh("--grafana-only")
        if args.refresh_teams:
            run_sso_refresh("--teams-only")
        if args.refresh_gdrive:
            run_sso_refresh("--gdrive-only")

    # Read tokens from ~/.openclaw/tool-connector.env
    env_vars = read_env_file(ENV_FILE)
    tokens = {k: env_vars[k] for k in SSO_ENV_KEYS if k in env_vars and env_vars[k]}

    if not tokens:
        print(f"No SSO tokens found in {ENV_FILE}.")
        print("Run playwright_sso.py first, or use --refresh-* flags.")
        sys.exit(1)

    sync_tokens_to_openclaw(tokens)
    print("\nDone. Start a new OpenClaw session to pick up the updated tokens.")


if __name__ == "__main__":
    main()
