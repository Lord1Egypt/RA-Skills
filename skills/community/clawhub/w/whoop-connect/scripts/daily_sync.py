#!/usr/bin/env python3
"""Daily sync — pull yesterday's data as a webhook safety net.

Run via cron once daily (e.g. 8am). Fetches recovery, sleep, workout,
and cycle for the past 2 days to catch anything webhooks may have missed.
"""

import sys
from whoop_client import WhoopClient
from formatters import format_recovery, format_sleep, format_workout, format_cycle


def main():
    days = 2
    if "--days" in sys.argv:
        idx = sys.argv.index("--days")
        if idx + 1 < len(sys.argv):
            days = int(sys.argv[idx + 1])

    client = WhoopClient()
    synced = {"recovery": 0, "sleep": 0, "workout": 0, "cycle": 0}

    try:
        records = client.get_recovery(days)
        synced["recovery"] = len(records)
        for r in records:
            print(format_recovery(r))
    except Exception as e:
        print(f"[sync] recovery error: {e}")

    try:
        records = client.get_sleep(days)
        synced["sleep"] = len(records)
        for r in records:
            print(format_sleep(r))
    except Exception as e:
        print(f"[sync] sleep error: {e}")

    try:
        records = client.get_workout(days)
        synced["workout"] = len(records)
        for r in records:
            print(format_workout(r))
    except Exception as e:
        print(f"[sync] workout error: {e}")

    try:
        records = client.get_cycle(days)
        synced["cycle"] = len(records)
        for r in records:
            print(format_cycle(r))
    except Exception as e:
        print(f"[sync] cycle error: {e}")

    total = sum(synced.values())
    print(f"\n[sync] done: {total} records ({synced})")


if __name__ == "__main__":
    main()
