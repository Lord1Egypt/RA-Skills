#!/usr/bin/env python3
"""_platform.py — openclaw-aware helpers.

Centralizes lookups that v1 hardcoded for hermes:
  - load_openrouter_key() — v1 read ~/.hermes/.env; v2 reads openclaw.json
    (~/.openclaw/openclaw.json → models.providers.openrouter.apiKey) with
    .env fallback for transitional setups.
  - resolve_responder(workspace) — v1 walked ~/.review-agent/users/<oid>/...;
    v2 reads the current workspace's owner.json / USER.md.
  - workspace_root() — the peer workspace root. Defaults to cwd (where the
    subagent is running); can be overridden with REVIEW_AGENT_WORKSPACE.

Safe to import from any review-agent script.
"""
import json
import os
from pathlib import Path


def load_openrouter_key():
    """Find an OpenRouter API key. v2 order:
       1. OPENROUTER_API_KEY env
       2. ~/.openclaw/openclaw.json → models.providers.openrouter.apiKey
       3. ~/.hermes/.env (legacy fallback for users mid-migration)
       4. ~/.openclaw/credentials/openrouter.json (if openclaw stored it there)
    Returns None if nothing found."""
    v = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if v:
        return v

    # openclaw.json
    cfg_path = Path.home() / ".openclaw" / "openclaw.json"
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text())
            providers = ((cfg.get("models") or {}).get("providers") or {})
            orout = providers.get("openrouter") or {}
            key = orout.get("apiKey", "")
            # Some installs use ${OPENROUTER_API_KEY} placeholder in the config
            if key.startswith("${") and key.endswith("}"):
                env_var = key[2:-1]
                key = os.environ.get(env_var, "")
            if key and not key.startswith("${"):
                return key
        except Exception:
            pass

    # Legacy .hermes/.env
    hermes_env = Path.home() / ".hermes" / ".env"
    if hermes_env.exists():
        for line in hermes_env.read_text().splitlines():
            if line.startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")

    return None


def workspace_root():
    """Per-peer workspace root. In production this is the subagent's cwd.
    Override with REVIEW_AGENT_WORKSPACE for testing against synthetic
    workspaces on the same machine.
    """
    override = os.environ.get("REVIEW_AGENT_WORKSPACE", "").strip()
    if override:
        return Path(override).resolve()
    return Path.cwd().resolve()


def resolve_responder_name(workspace=None):
    """Return the Responder's display name for prompt templating.
    Reads owner.json in the workspace, falls back to 'the Responder'."""
    ws = workspace or workspace_root()
    owner_file = Path(ws) / "owner.json"
    if owner_file.exists():
        try:
            d = json.loads(owner_file.read_text())
            name = d.get("responder_name") or d.get("admin_display_name")
            if name and name != "__RESPONDER_NAME__":
                return name
        except Exception:
            pass
    return "the Responder"


def session_dir(session_id, workspace=None):
    """Resolve a session dir under the workspace.
       session_id may be bare '<YYYYMMDD-HHMMSS>-<slug>' or a full path."""
    ws = workspace or workspace_root()
    p = Path(session_id)
    if p.is_absolute() and p.is_dir():
        return p
    return ws / "sessions" / session_id


if __name__ == "__main__":
    # Self-tests — purely diagnostic
    print(f"workspace_root()       → {workspace_root()}")
    key = load_openrouter_key()
    print(f"load_openrouter_key()  → {'(found, redacted)' if key else '(missing)'}")
    print(f"resolve_responder_name → {resolve_responder_name()}")
