#!/usr/bin/env python3
"""
setup.py — Interactive onboarding for skill-regression.

Usage:
  python3 scripts/setup.py              # Interactive setup
  python3 scripts/setup.py --show       # Show current config (no edit)
  python3 scripts/setup.py --reset      # Wipe and re-onboard
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running from any cwd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib_config import (  # noqa: E402
    GLOBAL_CONFIG_DIR,
    GLOBAL_ENV_FILE,
    REQUIRED_KEYS,
    detect_default_backend,
    is_tty,
    load_env_layers,
    resolve_config,
    run_onboarding,
)


def cmd_show(cfg: dict):
    print(f"\n📋 skill-regression config:")
    print(f"   Config file: {GLOBAL_ENV_FILE}")
    print(f"   Auto-detected backend: {detect_default_backend()}\n")
    for k in sorted(cfg.keys()):
        v = cfg[k]
        if "KEY" in k and v:
            v = v[:6] + "***" + v[-2:] if len(v) > 8 else "***"
        print(f"   {k} = {v}")
    print()


def cmd_reset():
    if GLOBAL_ENV_FILE.exists():
        confirm = input(f"⚠️  Delete {GLOBAL_ENV_FILE}? [y/N]: ").strip().lower()
        if confirm in ("y", "yes"):
            GLOBAL_ENV_FILE.unlink()
            print(f"✅ Removed {GLOBAL_ENV_FILE}")
        else:
            print("Aborted.")
            return
    cmd_setup({})


def cmd_setup(cfg: dict):
    if not is_tty():
        print("❌ setup.py requires an interactive terminal (TTY).", file=sys.stderr)
        print("   Or set SR_* env vars / create ~/.config/skill-regression/.env directly.", file=sys.stderr)
        sys.exit(2)

    # Force onboarding for ALL required keys (even if some are set)
    backend = cfg.get("SR_BACKEND") or detect_default_backend()
    cfg["SR_BACKEND"] = backend
    required = ["SR_BACKEND"] + REQUIRED_KEYS.get(backend, REQUIRED_KEYS["api"])
    # Onboard prompts only for missing — for full reset, missing = all required
    print("Re-run onboarding (existing values shown as defaults):")
    run_onboarding(cfg, missing=required)
    print("\n✅ Setup complete. You can now run `bash scripts/run_regression.sh <skill>`.")


def main():
    ap = argparse.ArgumentParser(description="skill-regression onboarding")
    ap.add_argument("--show", action="store_true", help="Show current config (masked)")
    ap.add_argument("--reset", action="store_true", help="Wipe config and re-onboard")
    args = ap.parse_args()

    cfg = resolve_config(project_dir=Path.cwd())

    if args.show:
        cmd_show(cfg)
    elif args.reset:
        cmd_reset()
    else:
        cmd_setup(cfg)


if __name__ == "__main__":
    main()
