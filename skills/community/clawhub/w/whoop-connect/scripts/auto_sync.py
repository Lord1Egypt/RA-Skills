#!/usr/bin/env python3
"""Smart auto-sync daemon for WHOOP Connect.

Adaptive polling:
- If webhook is enabled and healthy → poll every sync_interval_webhook minutes (default 20)
- If webhook is off or unhealthy   → poll every sync_interval minutes (default 5)

Respects daily API call limit (default 10,000). Logs new data only.
"""

import json
import os
import signal
import sys
import time
from datetime import datetime, timezone

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)

from whoop_client import WhoopClient, DailyLimitExceeded
from db import get_db, get_daily_api_calls
from formatters import format_recovery, format_sleep, format_workout, format_cycle

CONFIG_PATH = os.path.expanduser("~/.whoop/config.json")
WEBHOOK_HEARTBEAT_PATH = os.path.expanduser("~/.whoop/webhook_heartbeat")


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}


def is_webhook_healthy(config, max_age_seconds=None):
    """Check if webhook is enabled and has received a recent event."""
    if not config.get("webhook_enabled", False):
        return False
    if not os.path.exists(WEBHOOK_HEARTBEAT_PATH):
        return False
    try:
        mtime = os.path.getmtime(WEBHOOK_HEARTBEAT_PATH)
        if max_age_seconds is None:
            # Consider healthy if heartbeat within 3x the webhook sync interval
            interval = config.get("sync_interval_webhook", 20)
            max_age_seconds = interval * 60 * 3
        return (time.time() - mtime) < max_age_seconds
    except OSError:
        return False


def get_effective_interval(config):
    """Return the polling interval in seconds based on webhook status."""
    if is_webhook_healthy(config):
        minutes = config.get("sync_interval_webhook", 20)
        mode = "webhook-fallback"
    else:
        minutes = config.get("sync_interval", 5)
        mode = "primary"
    return minutes * 60, mode


def estimate_daily_calls(interval_seconds):
    """Estimate how many API calls per day at this interval.
    Each sync cycle hits ~4 endpoints, each may paginate once = ~8 calls.
    """
    syncs_per_day = 86400 / interval_seconds
    calls_per_sync = 8  # 4 endpoints × ~2 pages avg
    return int(syncs_per_day * calls_per_sync)


def get_known_ids(conn):
    """Get sets of known IDs from DB to detect new data."""
    recovery_ids = set()
    sleep_ids = set()
    workout_ids = set()

    for row in conn.execute("SELECT cycle_id FROM recovery").fetchall():
        recovery_ids.add(row["cycle_id"])
    for row in conn.execute("SELECT id FROM sleep").fetchall():
        sleep_ids.add(row["id"])
    for row in conn.execute("SELECT id FROM workout").fetchall():
        workout_ids.add(row["id"])

    return recovery_ids, sleep_ids, workout_ids


def sync_once(client, config, known_recovery, known_sleep, known_workout):
    """Run one sync cycle. Returns (new_items_list, updated_known_sets)."""
    new_items = []
    days = 2  # look back 2 days to catch delayed scoring

    push_recovery = config.get("push_recovery", True)
    push_sleep = config.get("push_sleep", True)
    push_workout = config.get("push_workout", True)

    try:
        records = client.get_recovery(days)
        for r in records:
            rid = r.get("cycle_id")
            if rid and rid not in known_recovery and r.get("score_state") == "SCORED":
                known_recovery.add(rid)
                if push_recovery:
                    new_items.append(("recovery", format_recovery(r)))
    except DailyLimitExceeded:
        raise
    except Exception as e:
        print(f"[auto_sync] recovery error: {e}", flush=True)

    try:
        records = client.get_sleep(days)
        for r in records:
            sid = r.get("id")
            if sid and sid not in known_sleep and r.get("score_state") == "SCORED":
                known_sleep.add(sid)
                if push_sleep:
                    new_items.append(("sleep", format_sleep(r)))
    except DailyLimitExceeded:
        raise
    except Exception as e:
        print(f"[auto_sync] sleep error: {e}", flush=True)

    try:
        records = client.get_workout(days)
        for r in records:
            wid = r.get("id")
            if wid and wid not in known_workout and r.get("score_state") == "SCORED":
                known_workout.add(wid)
                if push_workout:
                    new_items.append(("workout", format_workout(r)))
    except DailyLimitExceeded:
        raise
    except Exception as e:
        print(f"[auto_sync] workout error: {e}", flush=True)

    return new_items


def main():
    config = load_config()
    client = WhoopClient()

    # Parse CLI overrides
    args = sys.argv[1:]
    once = "--once" in args
    for i, a in enumerate(args):
        if a == "--interval" and i + 1 < len(args):
            override_min = int(args[i + 1])
            config["sync_interval"] = override_min
            config["sync_interval_webhook"] = override_min

    # Pre-flight: check estimated daily usage
    interval_secs, mode = get_effective_interval(config)
    estimated = estimate_daily_calls(interval_secs)
    limit = config.get("daily_api_limit", 10000)

    print(f"[auto_sync] mode={mode} interval={interval_secs // 60}m "
          f"estimated_daily_calls={estimated} limit={limit}", flush=True)

    if estimated > limit * 0.8:
        print(f"[auto_sync] WARNING: estimated daily calls ({estimated}) "
              f"exceeds 80% of limit ({limit}). Consider increasing interval.", flush=True)

    # Build initial known-ID sets from DB
    conn = get_db()
    known_recovery, known_sleep, known_workout = get_known_ids(conn)
    conn.close()

    print(f"[auto_sync] known records: recovery={len(known_recovery)} "
          f"sleep={len(known_sleep)} workout={len(known_workout)}", flush=True)

    # Graceful shutdown
    running = True

    def handle_signal(sig, frame):
        nonlocal running
        print(f"\n[auto_sync] shutting down (signal {sig})", flush=True)
        running = False

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    while running:
        config = load_config()  # reload config each cycle for hot-update
        interval_secs, mode = get_effective_interval(config)

        try:
            usage = client.get_api_usage()
            print(f"[auto_sync] {datetime.now(tz=timezone.utc).strftime('%H:%M:%S')} "
                  f"mode={mode} api={usage['used']}/{usage['limit']}", flush=True)

            new_items = sync_once(client, config, known_recovery, known_sleep, known_workout)

            if new_items:
                print(f"\n[auto_sync] === {len(new_items)} new event(s) ===", flush=True)
                for event_type, formatted in new_items:
                    print(f"\n[{event_type}] {formatted}", flush=True)
                print("", flush=True)

        except DailyLimitExceeded as e:
            print(f"[auto_sync] {e}", flush=True)
            print("[auto_sync] pausing until next UTC day", flush=True)
            # Sleep until UTC midnight
            now = datetime.now(tz=timezone.utc)
            tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0)
            tomorrow = tomorrow.__class__(
                tomorrow.year, tomorrow.month, tomorrow.day,
                tzinfo=timezone.utc
            )
            from datetime import timedelta
            tomorrow += timedelta(days=1)
            sleep_secs = (tomorrow - now).total_seconds()
            print(f"[auto_sync] sleeping {sleep_secs / 3600:.1f}h until UTC midnight", flush=True)
            time.sleep(min(sleep_secs, 86400))
            continue
        except Exception as e:
            print(f"[auto_sync] unexpected error: {e}", flush=True)

        if once:
            break

        # Sleep in small increments for responsive shutdown
        sleep_until = time.time() + interval_secs
        while running and time.time() < sleep_until:
            time.sleep(min(5, sleep_until - time.time()))

    print("[auto_sync] stopped", flush=True)


if __name__ == "__main__":
    main()
