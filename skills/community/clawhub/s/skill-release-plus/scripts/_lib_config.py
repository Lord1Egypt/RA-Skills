#!/usr/bin/env python3
"""
_lib_config.py — Shared config loader with .env support + onboarding.

Resolution priority (high -> low):
  1. CLI args
  2. Process env vars (SRP_*)
  3. Project-local `./.env`
  4. Global `~/.config/skill-release-plus/.env`
  5. Missing required key -> trigger onboarding (interactive TTY) or exit 2 (non-TTY)

All SRP_* vars (skill-release-plus private namespace):
  Targets:
    SRP_DEFAULT_TARGETS       comma-separated default targets (default "clawhub")
                              valid: clawhub, skillhub-cn, github-release,
                                     user-hook:<path>
  Per-target tokens:
    SRP_CLAWHUB_TOKEN         clawhub.com API token (clh_xxx)
                              -> cn.clawhub-mirror.com auto-mirrors clawhub
    SRP_SKILLHUB_CN_TOKEN     Tencent SkillHub token (skh_xxx)
    SRP_GITHUB_TOKEN          GitHub PAT (ghp_xxx or github_pat_xxx) for github-release

  Behavior:
    SRP_SIGN_OPTIONAL         if "true", skip skill-sign dependency if not installed
    SRP_OUTPUT_DIR            override package output dir (default: ./output/skill-release)

Exit codes:
  0 success
  1 business failure (publish failed, package error, etc.)
  2 config missing (no token / no valid target / onboarding needed in non-TTY)
"""
from __future__ import annotations

import os
import stat
import sys
from pathlib import Path
from typing import Optional


GLOBAL_CONFIG_DIR = Path.home() / ".config" / "skill-release-plus"
GLOBAL_ENV_FILE = GLOBAL_CONFIG_DIR / ".env"
PROJECT_ENV_FILE = Path.cwd() / ".env"

# Valid target names (user-hook:<path> is dynamic so not listed here)
#
# Note on cn.clawhub-mirror.com (ByteDance Volcano Engine):
#   verified 2026-06-22 to be a READ-ONLY mirror of clawhub.com — no publish API.
#   Publishing to clawhub causes the cn mirror to auto-sync. Therefore no
#   independent 'clawhub-cn' target exists; users in China simply install via
#   the cn.clawhub-mirror.com URL.
VALID_TARGETS = {"clawhub", "skillhub-cn", "github-release"}

# Per-target required env var (token name)
TARGET_TOKEN_ENV = {
    "clawhub":        "SRP_CLAWHUB_TOKEN",
    "skillhub-cn":    "SRP_SKILLHUB_CN_TOKEN",
    "github-release": "SRP_GITHUB_TOKEN",
}

DEFAULTS = {
    "SRP_DEFAULT_TARGETS": "clawhub",
    "SRP_OUTPUT_DIR": str(Path.cwd() / "output" / "skill-release"),
    "SRP_SIGN_OPTIONAL": "true",
}


# ── .env loading ──────────────────────────────────────────────────────────

def _parse_env_file(path: Path) -> dict:
    """Parse a simple KEY=VALUE .env file. Ignores blank lines and #-comments.
    Strips surrounding double quotes from values."""
    out: dict = {}
    if not path.is_file():
        return out
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip()
            if v.startswith('"') and v.endswith('"'):
                v = v[1:-1]
            elif v.startswith("'") and v.endswith("'"):
                v = v[1:-1]
            out[k] = v
    except Exception as e:
        print(f"WARN: failed to parse {path}: {e}", file=sys.stderr)
    return out


# ── Resolution layer ──────────────────────────────────────────────────────

def resolve_config(cli_overrides: dict = None) -> dict:
    """
    Resolve SRP_* config with 4-layer priority.
    Returns dict with all SRP_* keys (None if missing).
    """
    cli_overrides = cli_overrides or {}

    # Layer 4: global ~/.config/skill-release-plus/.env
    cfg = dict(DEFAULTS)
    cfg.update(_parse_env_file(GLOBAL_ENV_FILE))

    # Layer 3: project ./.env
    cfg.update(_parse_env_file(PROJECT_ENV_FILE))

    # Layer 2: process env vars (only SRP_* prefix)
    for k, v in os.environ.items():
        if k.startswith("SRP_") and v:
            cfg[k] = v

    # Layer 1: CLI overrides
    for k, v in cli_overrides.items():
        if v is not None and v != "":
            cfg[k] = v

    return cfg


def parse_targets(targets_str: str) -> list:
    """Parse comma-separated target list and validate.
    Returns list of target names. Raises ValueError on unknown target.

    Special values:
      "all" (alone or as one of the comma items) expands to all VALID_TARGETS.
      "user-hook:<path>" is dynamic and always accepted.
    """
    if not targets_str:
        return ["clawhub"]
    raw_items = [t.strip() for t in targets_str.split(",") if t.strip()]
    result = []
    for t in raw_items:
        if t.lower() == "all":
            # Expand to all built-in targets (preserves order; dedup later)
            result.extend(sorted(VALID_TARGETS))
            continue
        if t.startswith("user-hook:"):
            result.append(t)
            continue
        if t not in VALID_TARGETS:
            valid_list = ", ".join(sorted(VALID_TARGETS)) + ", user-hook:<path>, all"
            raise ValueError(
                f"unknown target '{t}'. Valid targets: {valid_list}"
            )
        result.append(t)
    # Dedup preserving first occurrence
    seen = set()
    out = []
    for t in result:
        if t not in seen:
            out.append(t)
            seen.add(t)
    return out


def ensure_token_for_target(target: str, cfg: dict) -> Optional[str]:
    """Get token for a target. Returns token string or None if missing."""
    if target.startswith("user-hook:"):
        return ""  # user-hook does not need a token
    env_key = TARGET_TOKEN_ENV.get(target)
    if not env_key:
        return None
    return cfg.get(env_key)


def check_targets_ready(targets: list, cfg: dict) -> dict:
    """Check token readiness for each target.
    Returns {target: {"ready": bool, "missing_env": str|None}}."""
    result = {}
    for t in targets:
        token = ensure_token_for_target(t, cfg)
        if t.startswith("user-hook:"):
            result[t] = {"ready": True, "missing_env": None}
            continue
        env_key = TARGET_TOKEN_ENV.get(t, "?")
        if token:
            result[t] = {"ready": True, "missing_env": None}
        else:
            result[t] = {"ready": False, "missing_env": env_key}
    return result


# ── Onboarding (Style A: per-target prompt) ───────────────────────────────

def is_tty() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def onboard_token(target: str) -> Optional[str]:
    """Interactive token prompt for a single target. TTY only.
    Returns the entered token (also writes to global .env) or None if user skips."""
    if not is_tty():
        return None

    env_key = TARGET_TOKEN_ENV.get(target)
    if not env_key:
        return None

    hub_hint = {
        "clawhub":        "Get from https://clawhub.com  (Settings -> API Tokens)",
        "skillhub-cn":    "Get from https://skillhub.cn  (Profile -> API Tokens)",
        "github-release": "Create a PAT at https://github.com/settings/tokens  (repo scope)",
    }.get(target, "")

    print(f"\n=== Onboarding: missing token for target '{target}' ===", file=sys.stderr)
    print(f"  required env var: {env_key}", file=sys.stderr)
    if hub_hint:
        print(f"  {hub_hint}", file=sys.stderr)
    print(f"  Skip with empty input. Will not save to global config if skipped.", file=sys.stderr)

    try:
        token = input(f"  {env_key}= ").strip()
    except (EOFError, KeyboardInterrupt):
        return None

    if not token:
        return None

    # Save to global .env
    save = input(f"  Save to {GLOBAL_ENV_FILE} for future use? [Y/n] ").strip().lower()
    if save in ("", "y", "yes"):
        _save_global_env({env_key: token})
        print(f"  ✓ saved to {GLOBAL_ENV_FILE}", file=sys.stderr)
    return token


def _save_global_env(kv: dict) -> None:
    """Append (or overwrite) keys to global .env with chmod 600."""
    GLOBAL_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    # chmod 700 on parent
    try:
        os.chmod(GLOBAL_CONFIG_DIR, stat.S_IRWXU)
    except Exception:
        pass

    existing = _parse_env_file(GLOBAL_ENV_FILE)
    existing.update(kv)

    lines = []
    for k in sorted(existing.keys()):
        v = existing[k]
        # Quote value if contains spaces or special chars
        if any(c in v for c in ' "#$'):
            v = '"' + v.replace('"', '\\"') + '"'
        lines.append(f"{k}={v}")
    GLOBAL_ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        os.chmod(GLOBAL_ENV_FILE, stat.S_IRUSR | stat.S_IWUSR)  # 600
    except Exception:
        pass


# ── Non-TTY hint ─────────────────────────────────────────────────────────

def emit_missing_token_hint(target: str, env_key: str) -> None:
    """Print a friendly hint about how to set the missing token (non-TTY path)."""
    print(
        f"ERROR: target '{target}' requires {env_key} but it is not set.\n"
        f"  Set one of the following (priority high -> low):\n"
        f"    1. CLI arg (see --help)\n"
        f"    2. shell:   export {env_key}=<your-token>\n"
        f"    3. project: echo '{env_key}=<token>' >> ./.env\n"
        f"    4. global:  echo '{env_key}=<token>' >> {GLOBAL_ENV_FILE}\n"
        f"  Then re-run. Or run with --target <other-target> to skip this one.\n",
        file=sys.stderr,
    )


# ── Public API ────────────────────────────────────────────────────────────

__all__ = [
    "GLOBAL_CONFIG_DIR",
    "GLOBAL_ENV_FILE",
    "VALID_TARGETS",
    "TARGET_TOKEN_ENV",
    "DEFAULTS",
    "resolve_config",
    "parse_targets",
    "ensure_token_for_target",
    "check_targets_ready",
    "is_tty",
    "onboard_token",
    "emit_missing_token_hint",
]
