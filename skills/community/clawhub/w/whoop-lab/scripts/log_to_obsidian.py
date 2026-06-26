#!/usr/bin/env python3
"""
Log today's WHOOP stats to the Obsidian daily note.

Usage:
  python3 log_to_obsidian.py
  python3 log_to_obsidian.py --date 2026-03-01   # backfill a specific date
  python3 log_to_obsidian.py --dry-run            # print what would be written
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

# Always resolve so the script works from any cwd
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import config as _cfg

FETCH_SCRIPT = SCRIPT_DIR / "fetch.py"
VAULT_PATH = _cfg.vault_path()
DAILY_NOTES_DIR = _cfg.daily_notes_dir()
ET = ZoneInfo(_cfg.timezone())
LOGGED_BY = _cfg.logged_by()

SECTION_HEADER = "## 🏋️ WHOOP"


def fetch(endpoint, limit=1):
    cmd = [sys.executable, str(FETCH_SCRIPT), endpoint, "--limit", str(limit)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"ERROR fetching {endpoint}: {e.stderr}", file=sys.stderr)
        return {}


def fmt_duration(ms):
    if not ms:
        return "N/A"
    total_min = int(ms / 60000)
    h = total_min // 60
    m = total_min % 60
    return f"{h}h {m:02d}m"


def recovery_emoji(score):
    if score is None:
        return ""
    if score >= 67:
        return " 💚"
    if score >= 34:
        return " 💛"
    return " 🔴"


def build_whoop_section(date_str):
    """Fetch WHOOP data and build the markdown section."""
    now_et = datetime.now(ET)
    time_str = now_et.strftime("%I:%M %p ET").lstrip("0")

    # Fetch latest recovery
    recovery_data = fetch("/recovery", limit=1)
    recovery_records = recovery_data.get("records", [])
    recovery_score = None
    hrv = None
    rhr = None
    if recovery_records:
        score = recovery_records[0].get("score", {})
        recovery_score = score.get("recovery_score")
        hrv = score.get("hrv_rmssd_milli")
        rhr = score.get("resting_heart_rate")

    # Fetch latest sleep
    sleep_data = fetch("/activity/sleep", limit=3)
    sleep_records = [r for r in sleep_data.get("records", []) if not r.get("nap")]
    sleep_perf = None
    sleep_dur_ms = None
    if sleep_records:
        latest = sleep_records[0]
        score = latest.get("score", {})
        sleep_perf = score.get("sleep_performance_percentage")
        stage = score.get("stage_summary", {})
        total_ms = (
            (stage.get("total_slow_wave_sleep_time_milli") or 0)
            + (stage.get("total_rem_sleep_time_milli") or 0)
            + (stage.get("total_light_sleep_time_milli") or 0)
        )
        sleep_dur_ms = total_ms if total_ms > 0 else None

    # Fetch latest cycle for strain
    cycle_data = fetch("/cycle", limit=1)
    cycle_records = cycle_data.get("records", [])
    strain = None
    if cycle_records:
        strain = cycle_records[0].get("score", {}).get("strain")

    # Format values
    rec_str = f"{recovery_score}%{recovery_emoji(recovery_score)}" if recovery_score is not None else "N/A"
    hrv_str = f"{hrv:.0f}ms" if hrv is not None else "N/A"
    rhr_str = f"{rhr:.0f} bpm" if rhr is not None else "N/A"
    perf_str = f"{sleep_perf:.0f}%" if sleep_perf is not None else "N/A"
    dur_str = fmt_duration(sleep_dur_ms)
    strain_str = f"{strain:.1f}" if strain is not None else "N/A"

    section = f"""{SECTION_HEADER}

| Metric | Value |
|--------|-------|
| Recovery | {rec_str} |
| HRV | {hrv_str} |
| Resting HR | {rhr_str} |
| Sleep Performance | {perf_str} |
| Sleep Duration | {dur_str} |
| Day Strain | {strain_str} |

_Logged by {LOGGED_BY} at {time_str}_
"""
    return section


def get_daily_note_path(date_str):
    return DAILY_NOTES_DIR / f"{date_str}.md"


def is_git_repo(vault_path):
    """Check if the vault is a git repository."""
    result = subprocess.run(
        ["git", "-C", str(vault_path), "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True
    )
    return result.returncode == 0


def git_commit_push(vault_path, date_str, dry_run=False):
    if dry_run:
        print(f"[dry-run] Would git add -A && commit && push in {vault_path}")
        return

    if not is_git_repo(vault_path):
        print("  Vault is not a git repository — skipping git sync.", file=sys.stderr)
        return

    cmds = [
        ["git", "-C", str(vault_path), "pull", "--rebase", "--autostash"],
        ["git", "-C", str(vault_path), "add", "-A"],
        ["git", "-C", str(vault_path), "commit", "-m", f"WHOOP log: {date_str}"],
        ["git", "-C", str(vault_path), "push"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, capture_output=True, text=True)
        label = " ".join(cmd[2:])
        if result.returncode != 0 and "nothing to commit" not in result.stdout + result.stderr:
            print(f"  git warning ({label}): {result.stderr.strip()}", file=sys.stderr)
        else:
            print(f"  {label}: ok", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Log WHOOP stats to Obsidian daily note")
    parser.add_argument("--date", help="Date to log (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be written, don't write")
    args = parser.parse_args()

    if args.date:
        date_str = args.date
    else:
        date_str = datetime.now(ET).strftime("%Y-%m-%d")

    # Guard: check vault path exists before writing
    if not VAULT_PATH.exists():
        print(f"ERROR: Vault path does not exist: {VAULT_PATH}", file=sys.stderr)
        print("Configure vault_path in ~/.config/whoop-skill/config.json", file=sys.stderr)
        print("or copy config.example.json and update the path.", file=sys.stderr)
        sys.exit(1)

    # Check vault path is configured and exists
    if not VAULT_PATH or not VAULT_PATH.exists():
        print(f"ERROR: Obsidian vault not found at {VAULT_PATH}", file=sys.stderr)
        print("Set 'vault_path' in ~/.config/whoop-skill/config.json to your vault directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Logging WHOOP stats for {date_str}...", file=sys.stderr)

    section = build_whoop_section(date_str)

    if args.dry_run:
        print("\n--- WHOOP Section (dry-run) ---")
        print(section)
        print("--- end ---")
        return

    note_path = get_daily_note_path(date_str)
    DAILY_NOTES_DIR.mkdir(parents=True, exist_ok=True)

    if note_path.exists():
        content = note_path.read_text(encoding="utf-8")
        if SECTION_HEADER in content:
            print(f"WHOOP section already present in {note_path.name}. Skipping.", file=sys.stderr)
            return
        # Append
        if not content.endswith("\n"):
            content += "\n"
        content += f"\n{section}"
        note_path.write_text(content, encoding="utf-8")
        print(f"Appended WHOOP section to {note_path}", file=sys.stderr)
    else:
        # Create new note
        content = f"# {date_str}\n\n{section}"
        note_path.write_text(content, encoding="utf-8")
        print(f"Created new daily note: {note_path}", file=sys.stderr)

    git_commit_push(VAULT_PATH, date_str)
    print("Done ✓", file=sys.stderr)


if __name__ == "__main__":
    main()
