#!/usr/bin/env python3
"""
subagent-timeout-config: one-click subagent timeout configurator for OpenClaw.

Configures three related timeout fields in OpenClaw's config JSON:
  - agents.defaults.timeoutSeconds          (per-tool-call wait)
  - agents.defaults.subagents.runTimeoutSeconds  (per-subagent task budget)
  - acp.runtime.ttlMinutes                  (ACP session lifetime)

Constraint enforced: ttlMinutes * 60 >= runTimeoutSeconds.

Preset profiles (CLI key + display label):
  quick     "Quick"     —  60s / 1h / 1h    quick iteration, fast feedback
  normal    "Normal"    — 180s / 2h / 2h    everyday development
  patient   "Patient"   — 300s / 3h / 3h    long-running tasks, big codebases

Safety:
  - Auto-backup of the config file to <config>.bak.<YYYYMMDD-HHMMSS> before write
  - Default: triggers `openclaw gateway restart` after a successful write.
    Pass `--no-restart` if you want to restart manually later.
  - `--dry-run` previews diffs without writing anything.

Usage:
  python3 set_timeout.py --profile quick
  python3 set_timeout.py --profile normal --no-restart
  python3 set_timeout.py --custom 180,7200,120
  python3 set_timeout.py --status
  python3 set_timeout.py --list
  python3 set_timeout.py --profile quick --config /custom/path/openclaw.json

Exit codes:
  0 = success
  1 = error (bad args, IO error, validation failure)
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

# ── Defaults & constants ────────────────────────────────────────────────────

DEFAULT_CONFIG_PATH = "~/.openclaw/openclaw.json"

# Preset profiles. Order matters for --list display.
PROFILES = {
    "quick": {
        "label": "Quick",
        "timeout_seconds": 60,
        "run_timeout_seconds": 3600,
        "ttl_minutes": 60,
        "use_case": "Quick iteration, fast feedback loops, interactive debugging",
    },
    "normal": {
        "label": "Normal",
        "timeout_seconds": 180,
        "run_timeout_seconds": 7200,
        "ttl_minutes": 120,
        "use_case": "Everyday development tasks, moderate complexity",
    },
    "patient": {
        "label": "Patient",
        "timeout_seconds": 300,
        "run_timeout_seconds": 10800,
        "ttl_minutes": 180,
        "use_case": "Long-running tasks, big codebases, complex analysis",
    },
}

# Backward-compat alias mapping (kept for users who learnt the old names).
PROFILE_ALIASES = {
    "impatient": "quick",
    "fast":      "quick",
    "slow":      "patient",
}


# ── Config IO ──────────────────────────────────────────────────────────────

def resolve_config_path(cli_path: Optional[str]) -> Path:
    """Priority: --config CLI > OPENCLAW_CONFIG env > ~/.openclaw/openclaw.json."""
    raw = cli_path or os.environ.get("OPENCLAW_CONFIG") or DEFAULT_CONFIG_PATH
    return Path(raw).expanduser()


def load_config(path: Path) -> Optional[Dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Config file not found: {path}", file=sys.stderr)
        print(f"   Hint: install OpenClaw or pass --config <path> to target a different runtime.",
              file=sys.stderr)
    except json.JSONDecodeError as e:
        print(f"❌ Config file is not valid JSON: {e}", file=sys.stderr)
    except Exception as e:
        print(f"❌ Cannot read config file: {e}", file=sys.stderr)
    return None


def backup_config(path: Path) -> Optional[Path]:
    """Make a timestamped backup of the config file. Returns the backup path."""
    if not path.exists():
        return None
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = path.with_suffix(path.suffix + f".bak.{ts}")
    try:
        shutil.copy2(path, bak)
        return bak
    except Exception as e:
        print(f"⚠️  Backup failed ({e}); proceeding without backup.", file=sys.stderr)
        return None


def write_config(path: Path, config: Dict) -> bool:
    try:
        # Atomic write: temp file + rename
        tmp = path.with_suffix(path.suffix + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, path)
        return True
    except Exception as e:
        print(f"❌ Failed to write config: {e}", file=sys.stderr)
        return False


def gateway_restart() -> bool:
    """Trigger `openclaw gateway restart`. Returns True on success."""
    try:
        result = subprocess.run(
            ["openclaw", "gateway", "restart"],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode == 0:
            return True
        print(f"⚠️  gateway restart returned {result.returncode}: "
              f"{result.stderr.strip()[-200:]}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("⚠️  `openclaw` CLI not found on PATH; please restart Gateway manually.",
              file=sys.stderr)
        return False
    except subprocess.TimeoutExpired:
        print("⚠️  gateway restart timed out after 60s.", file=sys.stderr)
        return False


# ── Mutation core ───────────────────────────────────────────────────────────

def apply_timeout_values(config: Dict, timeout_seconds: int,
                         run_timeout_seconds: int, ttl_minutes: int) -> Dict:
    """Pure function: return a new dict with timeout fields applied."""
    config.setdefault("agents", {}).setdefault("defaults", {})
    config["agents"]["defaults"].setdefault("subagents", {})
    config.setdefault("acp", {}).setdefault("runtime", {})

    config["agents"]["defaults"]["timeoutSeconds"] = timeout_seconds
    config["agents"]["defaults"]["subagents"]["runTimeoutSeconds"] = run_timeout_seconds
    config["acp"]["runtime"]["ttlMinutes"] = ttl_minutes
    return config


def validate(timeout_seconds: int, run_timeout_seconds: int,
             ttl_minutes: int) -> Tuple[bool, Optional[str]]:
    """Return (ok, error_message)."""
    if timeout_seconds <= 0 or run_timeout_seconds <= 0 or ttl_minutes <= 0:
        return False, "all timeout values must be positive integers"
    if run_timeout_seconds < timeout_seconds:
        return False, (f"runTimeoutSeconds ({run_timeout_seconds}) should be ≥ "
                       f"timeoutSeconds ({timeout_seconds})")
    if ttl_minutes * 60 < run_timeout_seconds:
        return False, (f"ttlMinutes ({ttl_minutes}min = {ttl_minutes * 60}s) must be "
                       f"≥ runTimeoutSeconds ({run_timeout_seconds}s). Increase "
                       f"--ttl or lower --run-timeout.")
    return True, None


# ── Display ─────────────────────────────────────────────────────────────────

def format_time(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}min"
    hours = seconds // 3600
    mins = (seconds % 3600) // 60
    return f"{hours}h{mins}min" if mins else f"{hours}h"


def show_status(config: Optional[Dict]) -> None:
    if config is None:
        print("❌ No config loaded.")
        return
    defaults = config.get("agents", {}).get("defaults", {})
    runtime = config.get("acp", {}).get("runtime", {})
    t = defaults.get("timeoutSeconds", "(unset)")
    r = defaults.get("subagents", {}).get("runTimeoutSeconds", "(unset)")
    ttl = runtime.get("ttlMinutes", "(unset)")

    print("\n📊 Current Subagent Timeout Configuration")
    print("=" * 60)
    print(f"  timeoutSeconds        (per-tool-call wait)    : {t}"
          f"{f'  ({format_time(t)})' if isinstance(t, int) else ''}")
    print(f"  runTimeoutSeconds     (per-subagent budget)   : {r}"
          f"{f'  ({format_time(r)})' if isinstance(r, int) else ''}")
    print(f"  ttlMinutes            (ACP session lifetime)  : {ttl}"
          f"{f'  ({format_time(ttl * 60)})' if isinstance(ttl, int) else ''}")
    print("=" * 60)


def show_profiles() -> None:
    print("\n📋 Available Profiles")
    print("=" * 70)
    for key, p in PROFILES.items():
        print(f"\n  --profile {key}    ({p['label']})")
        print(f"    timeoutSeconds      : {p['timeout_seconds']:>5}s   ({format_time(p['timeout_seconds'])})")
        print(f"    runTimeoutSeconds   : {p['run_timeout_seconds']:>5}s   ({format_time(p['run_timeout_seconds'])})")
        print(f"    ttlMinutes          : {p['ttl_minutes']:>5}min ({format_time(p['ttl_minutes'] * 60)})")
        print(f"    use case            : {p['use_case']}")
    aliases = ", ".join(f"{a}→{c}" for a, c in PROFILE_ALIASES.items())
    print(f"\n  Aliases: {aliases}")
    print("=" * 70)


def diff_summary(old: Dict, t: int, r: int, ttl: int) -> str:
    """Render a human-readable diff for dry-run / pre-apply preview."""
    o_t = old.get("agents", {}).get("defaults", {}).get("timeoutSeconds", "(unset)")
    o_r = old.get("agents", {}).get("defaults", {}).get("subagents", {}).get("runTimeoutSeconds", "(unset)")
    o_ttl = old.get("acp", {}).get("runtime", {}).get("ttlMinutes", "(unset)")
    lines = [
        "  Field                  Old         →  New",
        "  ─────────────────────  ──────────  ─  ──────────",
        f"  timeoutSeconds         {str(o_t):>10}  →  {t:>10}",
        f"  runTimeoutSeconds      {str(o_r):>10}  →  {r:>10}",
        f"  ttlMinutes             {str(o_ttl):>10}  →  {ttl:>10}",
    ]
    return "\n".join(lines)


# ── Apply orchestration ────────────────────────────────────────────────────

def do_apply(config_path: Path, timeout_seconds: int, run_timeout_seconds: int,
             ttl_minutes: int, *, label: str, dry_run: bool, no_restart: bool) -> int:
    config = load_config(config_path)
    if config is None:
        return 1

    ok, err = validate(timeout_seconds, run_timeout_seconds, ttl_minutes)
    if not ok:
        print(f"❌ Validation failed: {err}", file=sys.stderr)
        return 1

    print(f"\n🔄 Applying [{label}] to {config_path}")
    print(diff_summary(config, timeout_seconds, run_timeout_seconds, ttl_minutes))

    if dry_run:
        print("\n[DRY-RUN] No file written. Re-run without --dry-run to apply.")
        return 0

    bak = backup_config(config_path)
    if bak:
        print(f"💾 Backup saved → {bak}")

    new_config = apply_timeout_values(config, timeout_seconds, run_timeout_seconds, ttl_minutes)
    if not write_config(config_path, new_config):
        return 1

    print(f"✅ Configuration written to {config_path}")

    if no_restart:
        print("ℹ️  Gateway NOT restarted (--no-restart). Run `openclaw gateway restart` "
              "manually for changes to take effect.")
    else:
        print("🔁 Restarting Gateway ...")
        if gateway_restart():
            print("✅ Gateway restarted; new timeouts are active.")
        else:
            print("⚠️  Gateway restart failed; new timeouts will activate on next restart.")

    show_status(new_config)
    return 0


def resolve_profile_key(name: str) -> Optional[str]:
    name = name.lower().strip()
    if name in PROFILES:
        return name
    if name in PROFILE_ALIASES:
        canonical = PROFILE_ALIASES[name]
        print(f"ℹ️  Alias '{name}' → using '{canonical}'.", file=sys.stderr)
        return canonical
    return None


# ── Entry point ────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="One-click subagent timeout configurator for OpenClaw.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --profile quick                # Quick: 1min/1h/1h\n"
            "  %(prog)s --profile normal --no-restart  # Apply, skip gateway restart\n"
            "  %(prog)s --custom 180,7200,120          # Custom values\n"
            "  %(prog)s --status                       # Show current settings\n"
            "  %(prog)s --list                         # List preset profiles\n"
            "  %(prog)s --profile patient --dry-run    # Preview without writing\n"
        ),
    )
    parser.add_argument("--profile",
                        help="Apply preset profile: quick | normal | patient "
                             "(aliases: impatient→quick, fast→quick, slow→patient)")
    parser.add_argument("--custom", metavar="T,R,TTL",
                        help="Custom values: timeoutSeconds,runTimeoutSeconds,ttlMinutes")
    parser.add_argument("--status", action="store_true",
                        help="Show current timeout configuration")
    parser.add_argument("--list", action="store_true",
                        help="List all available preset profiles")
    parser.add_argument("--config", metavar="PATH",
                        help=f"Path to OpenClaw config JSON "
                             f"(default: $OPENCLAW_CONFIG or {DEFAULT_CONFIG_PATH})")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes; do not write file or restart Gateway")
    parser.add_argument("--no-restart", action="store_true",
                        help="Skip `openclaw gateway restart` after writing")
    args = parser.parse_args()

    config_path = resolve_config_path(args.config)

    if args.list:
        show_profiles()
        return 0

    if args.status:
        show_status(load_config(config_path))
        return 0

    if args.profile:
        key = resolve_profile_key(args.profile)
        if key is None:
            print(f"❌ Unknown profile: {args.profile}", file=sys.stderr)
            print(f"   Available: {', '.join(PROFILES.keys())}", file=sys.stderr)
            return 1
        p = PROFILES[key]
        return do_apply(config_path,
                        p["timeout_seconds"], p["run_timeout_seconds"], p["ttl_minutes"],
                        label=p["label"], dry_run=args.dry_run, no_restart=args.no_restart)

    if args.custom:
        parts = [s.strip() for s in args.custom.split(",")]
        if len(parts) != 3:
            print("❌ --custom requires 3 comma-separated integers: T,R,TTL", file=sys.stderr)
            return 1
        try:
            t, r, ttl = int(parts[0]), int(parts[1]), int(parts[2])
        except ValueError:
            print("❌ --custom values must be integers (seconds, seconds, minutes)",
                  file=sys.stderr)
            return 1
        return do_apply(config_path, t, r, ttl,
                        label="Custom", dry_run=args.dry_run, no_restart=args.no_restart)

    # No action specified — show help + current status
    parser.print_help()
    print()
    show_status(load_config(config_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
