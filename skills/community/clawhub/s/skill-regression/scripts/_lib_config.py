#!/usr/bin/env python3
"""
_lib_config.py — Shared config loader with .env support + onboarding.

Resolution priority (high -> low):
  1. CLI args
  2. Process env vars (SR_*)
  3. Project-local `./.env`
  4. Global `~/.config/skill-regression/.env`
  5. Missing required key -> trigger onboarding (interactive)

All SR_* vars (skill-regression private namespace):
  SR_BACKEND          openclaw | api  (auto-detect default: openclaw if CLI found, else api)
  SR_LLM_API_KEY      OpenAI-compatible API key (required for api backend)
  SR_LLM_BASE_URL     LLM endpoint (default https://api.openai.com/v1)
  SR_LLM_MODEL        Model name (default gpt-4o-mini)
  SR_TARGET_AGENT     OpenClaw target agent name for cron mode (default: main)
"""
from __future__ import annotations

import os
import shutil
import stat
import sys
from pathlib import Path
from typing import Optional


GLOBAL_CONFIG_DIR = Path.home() / ".config" / "skill-regression"
GLOBAL_ENV_FILE = GLOBAL_CONFIG_DIR / ".env"

# Required keys per backend
REQUIRED_KEYS = {
    "api": ["SR_LLM_API_KEY", "SR_LLM_BASE_URL", "SR_LLM_MODEL"],
    "openclaw": ["SR_TARGET_AGENT", "SR_LLM_API_KEY", "SR_LLM_BASE_URL", "SR_LLM_MODEL"],
    # openclaw still needs LLM API for the semantic-scoring layer (Step 3 scoring),
    # only the agent-trigger layer differs.
}

DEFAULTS = {
    "SR_BACKEND": None,  # auto-detect
    "SR_LLM_BASE_URL": "https://api.openai.com/v1",
    "SR_LLM_MODEL": "gpt-4o-mini",
    "SR_TARGET_AGENT": "main",
}


# ── .env loading ──────────────────────────────────────────────────────────

def _parse_env_file(path: Path) -> dict:
    """Parse simple .env file (KEY=VALUE per line, # comments, no shell expansion)."""
    out = {}
    if not path.exists():
        return out
    try:
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key:
                out[key] = val
    except Exception:
        return {}
    return out


def load_env_layers(project_dir: Optional[Path] = None) -> dict:
    """
    Load env layers in resolution-priority order. Returns merged dict
    of SR_* keys only (process env wins over .env files).
    """
    layers = {}

    # Layer 4: global .env (lowest)
    if GLOBAL_ENV_FILE.exists():
        layers.update(_parse_env_file(GLOBAL_ENV_FILE))

    # Layer 3: project-local .env
    if project_dir:
        local_env = Path(project_dir) / ".env"
        if local_env.exists():
            layers.update(_parse_env_file(local_env))

    # Layer 2: process env (highest before CLI)
    for k in list(REQUIRED_KEYS["api"]) + list(REQUIRED_KEYS["openclaw"]) + ["SR_BACKEND"]:
        if k in os.environ:
            layers[k] = os.environ[k]

    # Apply defaults for unset values
    for k, default in DEFAULTS.items():
        if default is not None and k not in layers:
            layers[k] = default

    return layers


def detect_default_backend() -> str:
    """Auto-detect default backend: 'openclaw' if openclaw CLI available, else 'api'."""
    if shutil.which("openclaw"):
        return "openclaw"
    return "api"


def resolve_config(
    cli_args: Optional[dict] = None,
    project_dir: Optional[Path] = None,
) -> dict:
    """
    Resolve final config. CLI args > env > .env files > defaults.
    Backend auto-detected if not set.
    Does NOT trigger onboarding; caller responsible for `require_config_ready()`.
    """
    cli_args = cli_args or {}
    cfg = load_env_layers(project_dir=project_dir)

    # CLI overrides
    for k, v in cli_args.items():
        if v is not None:
            cfg[k] = v

    # Backend auto-detect
    if not cfg.get("SR_BACKEND"):
        cfg["SR_BACKEND"] = detect_default_backend()

    return cfg


def missing_required(cfg: dict) -> list:
    """Return list of missing required keys for the resolved backend."""
    backend = cfg.get("SR_BACKEND", "api")
    required = REQUIRED_KEYS.get(backend, REQUIRED_KEYS["api"])
    return [k for k in required if not cfg.get(k)]


# ── Onboarding ────────────────────────────────────────────────────────────

def is_tty() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def run_onboarding(cfg: dict, missing: list, save_path: Optional[Path] = None) -> dict:
    """
    Interactive onboarding (Style A). Prompts only for missing keys.
    Writes result to save_path (default: global .env), chmod 600.
    """
    if not is_tty():
        # Non-interactive: print Style B fallback and exit
        print_setup_hint(missing)
        sys.exit(2)

    print("\n🔧 skill-regression first-time setup", file=sys.stderr)
    print(f"   Missing config: {', '.join(missing)}", file=sys.stderr)
    print(f"   Backend: {cfg.get('SR_BACKEND', 'auto')}\n", file=sys.stderr)

    updates = {}

    if "SR_BACKEND" in missing:
        default_be = detect_default_backend()
        val = _prompt(f"Backend [openclaw/api] (default: {default_be})", default_be)
        if val not in ("openclaw", "api"):
            print(f"❌ Invalid backend '{val}'. Must be 'openclaw' or 'api'.", file=sys.stderr)
            sys.exit(2)
        updates["SR_BACKEND"] = val
        cfg["SR_BACKEND"] = val

    if "SR_TARGET_AGENT" in missing:
        val = _prompt("OpenClaw target agent name", DEFAULTS["SR_TARGET_AGENT"])
        if not val:
            print("❌ SR_TARGET_AGENT cannot be empty.", file=sys.stderr)
            sys.exit(2)
        updates["SR_TARGET_AGENT"] = val

    if "SR_LLM_API_KEY" in missing:
        val = _prompt_secret("LLM API key (e.g. sk-...)")
        if not val:
            print("❌ SR_LLM_API_KEY cannot be empty.", file=sys.stderr)
            sys.exit(2)
        updates["SR_LLM_API_KEY"] = val

    if "SR_LLM_BASE_URL" in missing:
        val = _prompt("LLM base URL", DEFAULTS["SR_LLM_BASE_URL"])
        updates["SR_LLM_BASE_URL"] = val

    if "SR_LLM_MODEL" in missing:
        val = _prompt("Model name", DEFAULTS["SR_LLM_MODEL"])
        updates["SR_LLM_MODEL"] = val

    # Save
    target = save_path or GLOBAL_ENV_FILE
    save_choice = _prompt(f"\nSave to {target}? [Y/n]", "y")
    if save_choice.lower() in ("y", "yes", ""):
        write_env_file(target, updates, merge_existing=True)
        print(f"✅ Saved to {target} (chmod 600)", file=sys.stderr)

    cfg.update(updates)
    return cfg


def _prompt(prompt: str, default: Optional[str] = None) -> str:
    suffix = f" [{default}]: " if default else ": "
    try:
        val = input(f"   {prompt}{suffix}").strip()
    except EOFError:
        val = ""
    return val or (default or "")


def _prompt_secret(prompt: str) -> str:
    """Hidden input for secrets (no terminal echo)."""
    import getpass
    try:
        return getpass.getpass(f"   {prompt}: ").strip()
    except (EOFError, KeyboardInterrupt):
        return ""


def write_env_file(path: Path, kv: dict, merge_existing: bool = True):
    """Write .env file with chmod 600; merge with existing if requested."""
    path = Path(path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(path.parent, 0o700)
    except OSError:
        pass

    existing = _parse_env_file(path) if (merge_existing and path.exists()) else {}
    existing.update(kv)

    lines = ["# skill-regression config (chmod 600, do not commit)"]
    for k in sorted(existing.keys()):
        v = existing[k]
        # Quote if contains spaces
        if " " in v or "\t" in v:
            v = f'"{v}"'
        lines.append(f"{k}={v}")
    lines.append("")  # trailing newline

    path.write_text("\n".join(lines), encoding="utf-8")
    os.chmod(path, 0o600)

    # Append to .gitignore if writing project-local .env
    if path.name == ".env" and path.parent.name != "skill-regression":
        gitignore = path.parent / ".gitignore"
        existing_lines = gitignore.read_text(encoding="utf-8").splitlines() if gitignore.exists() else []
        if ".env" not in existing_lines:
            existing_lines.append(".env")
            gitignore.write_text("\n".join(existing_lines) + "\n", encoding="utf-8")


def print_setup_hint(missing: list):
    """Style B: print Onboarding hint when stdin is not a TTY."""
    print("\n❌ skill-regression not configured.", file=sys.stderr)
    print(f"   Missing required config: {', '.join(missing)}\n", file=sys.stderr)
    print("   To set up interactively:", file=sys.stderr)
    print("     python3 scripts/setup.py\n", file=sys.stderr)
    print("   Or set env vars directly (then re-run):", file=sys.stderr)
    for k in missing:
        default = DEFAULTS.get(k, "<your-value>")
        if k == "SR_LLM_API_KEY":
            default = "sk-..."
        print(f"     export {k}='{default}'", file=sys.stderr)
    print("\n   Or create ~/.config/skill-regression/.env\n", file=sys.stderr)


def require_config_ready(cfg: dict, allow_onboarding: bool = True) -> dict:
    """
    Verify cfg has all required keys for its backend.
    If missing and TTY, trigger onboarding (Style A).
    If missing and non-TTY, print hint and exit 2 (Style B).
    """
    missing = missing_required(cfg)
    if not missing:
        return cfg

    if allow_onboarding and is_tty():
        return run_onboarding(cfg, missing)
    else:
        print_setup_hint(missing)
        sys.exit(2)


if __name__ == "__main__":
    # CLI: `python3 _lib_config.py` prints resolved config (debug)
    cfg = resolve_config(project_dir=Path.cwd())
    for k in sorted(cfg.keys()):
        v = cfg[k]
        if "KEY" in k and v:
            v = v[:6] + "***"  # mask secrets
        print(f"{k}={v}")
