"""
Shared config loader for OpenClaw snapshot scripts.

Resolution order for config values:
  1. os.environ (set by OpenClaw via ~/.openclaw/.env or skills.entries.*.env)
  2. Skill-local .env file (one level up from scripts/)

This means users can provide credentials through either:
  - OpenClaw's ~/.openclaw/.env (recommended — single place for all secrets)
  - The skill's own .env file (standalone usage outside OpenClaw)
  - Shell environment variables
"""

import os
import stat
import sys
import tempfile
from pathlib import Path

# Skill root is the parent of the scripts/ directory
SKILL_DIR = Path(__file__).parent.parent
ENV_FILE = SKILL_DIR / ".env"


def load_env_file() -> dict:
    """Read the skill-local .env file if it exists. Returns empty dict if not found."""
    if not ENV_FILE.is_file():
        return {}

    config = {}
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()
    return config


def get_config() -> dict:
    """
    Load and validate the config.
    Checks os.environ first (populated by OpenClaw from ~/.openclaw/.env),
    then falls back to the skill's local .env file.
    """
    # Start with values from the skill-local .env (if it exists)
    config = load_env_file()

    # Environment variables take precedence (set by OpenClaw or shell)
    required = ["BACKUP_PASSWORD", "GITHUB_PAT", "GITHUB_USERNAME"]
    for key in required + ["REPO_NAME"]:
        env_val = os.environ.get(key)
        if env_val:
            config[key] = env_val.rstrip(",")

    # Validate
    missing = [k for k in required if not config.get(k)]
    if missing:
        print("Error: Missing credentials. Provide them via either:")
        print(f"  1. OpenClaw env:  ~/.openclaw/.env")
        print(f"  2. Skill env:     {ENV_FILE}")
        print(f"  3. Shell:         export VARIABLE=value")
        print()
        print("  Missing:")
        for k in missing:
            print(f"    - {k}")
        sys.exit(1)

    config.setdefault("REPO_NAME", "openclaw-transport")

    # Clean URL without PAT — auth is handled via GIT_ASKPASS at runtime
    config["REPO_URL"] = (
        f"https://github.com/"
        f"{config['GITHUB_USERNAME']}/{config['REPO_NAME']}.git"
    )

    return config


def git_env(config: dict) -> dict:
    """
    Return an environment dict for subprocess calls to git.
    Uses GIT_ASKPASS with a temp script that provides the PAT,
    so the token never appears in .git/config or process listings.
    """
    askpass = tempfile.NamedTemporaryFile(
        mode="w", suffix=".sh", delete=False, prefix="git-askpass-"
    )
    askpass.write(f"#!/bin/sh\necho {config['GITHUB_PAT']}\n")
    askpass.close()
    os.chmod(askpass.name, stat.S_IRWXU)  # 700 — owner only

    env = os.environ.copy()
    env["GIT_ASKPASS"] = askpass.name
    env["GIT_TERMINAL_PROMPT"] = "0"  # never prompt interactively

    # Store path so callers can clean up
    env["_ASKPASS_TMP"] = askpass.name
    return env


def cleanup_git_env(env: dict):
    """Remove the temporary askpass script."""
    tmp = env.get("_ASKPASS_TMP")
    if tmp:
        try:
            os.unlink(tmp)
        except OSError:
            pass