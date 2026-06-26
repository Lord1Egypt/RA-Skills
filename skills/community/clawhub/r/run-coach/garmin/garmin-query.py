#!/usr/bin/env python3
"""Garmin data query for run-coach bot.
Pure stdlib — no third-party deps.
Reads JSON files written by garmin-sync.py.
"""

import json
import sys
from datetime import date, timedelta
from pathlib import Path

# Workspace is the parent of this script's directory
GARMIN_DIR = Path(__file__).parent
SUMMARY_FILE = GARMIN_DIR / "summary.json"
ACTIVITIES_DIR = GARMIN_DIR / "activities"


def load_summary():
    if not SUMMARY_FILE.exists():
        return None
    with open(SUMMARY_FILE, encoding="utf-8") as f:
        return json.load(f)


def cmd_recent(n=5):
    """Show recent activities."""
    summary = load_summary()
    if not summary:
        print("No Garmin data yet. Run garmin-sync on host first.")
        return

    activities = summary.get("recent_activities", [])[:n]
    if not activities:
        print("No recent running activities found.")
        return

    print(f"=== Recent Runs (last {len(activities)}) ===\n")
    for a in activities:
        print(f"📅 {a['date']}  {a.get('name', '')}")
        print(f"   Distance: {a['distance_km']}km | Time: {a['duration_min']}min | Pace: {a.get('avg_pace', '?')}/km")
        print(f"   HR: avg {a.get('avg_hr', '?')} / max {a.get('max_hr', '?')} | Cadence: {a.get('avg_cadence', '?')}spm")
        print(f"   Calories: {a.get('calories', '?')}")
        print()


def cmd_weekly():
    """Show weekly training summary."""
    summary = load_summary()
    if not summary:
        print("No Garmin data yet.")
        return

    activities = summary.get("recent_activities", [])

    # Filter to last 7 days
    week_ago = (date.today() - timedelta(days=7)).isoformat()
    week_runs = [a for a in activities if a.get("date", "") >= week_ago]

    if not week_runs:
        print("No runs in the past 7 days.")
        return

    total_km = sum(a.get("distance_km", 0) for a in week_runs)
    total_min = sum(a.get("duration_min", 0) for a in week_runs)
    avg_hr = [a["avg_hr"] for a in week_runs if a.get("avg_hr")]
    avg_hr_val = round(sum(avg_hr) / len(avg_hr)) if avg_hr else "?"

    print(f"=== Weekly Summary ({week_ago} ~ {date.today().isoformat()}) ===\n")
    print(f"Runs: {len(week_runs)}")
    print(f"Total distance: {total_km:.1f}km")
    print(f"Total time: {total_min:.0f}min ({total_min/60:.1f}h)")
    print(f"Avg HR: {avg_hr_val}")
    print()

    for a in week_runs:
        print(f"  {a['date']}: {a['distance_km']}km @ {a.get('avg_pace', '?')}/km (HR {a.get('avg_hr', '?')})")


def cmd_stats():
    """Show daily stats and training metrics."""
    summary = load_summary()
    if not summary:
        print("No Garmin data yet.")
        return

    print(f"=== Garmin Stats (synced: {summary.get('last_sync', '?')}) ===\n")

    daily = summary.get("daily_stats")
    if daily:
        print(f"📊 Daily ({daily.get('date', '?')}):")
        print(f"   Steps: {daily.get('steps', '?')}")
        print(f"   Resting HR: {daily.get('resting_hr', '?')}")
        print(f"   HR range: {daily.get('min_hr', '?')} - {daily.get('max_hr', '?')}")
        print(f"   Stress avg: {daily.get('stress_avg', '?')}")
        print(f"   Body Battery: {daily.get('body_battery_low', '?')} - {daily.get('body_battery_high', '?')}")
        print()

    metrics = summary.get("training_metrics", {})
    if metrics:
        print("🏋️ Training Metrics:")
        if metrics.get("vo2max"):
            print(f"   VO2max: {metrics['vo2max']}")
        if metrics.get("fitness_age"):
            print(f"   Fitness Age: {metrics['fitness_age']}")
        if metrics.get("training_status"):
            print(f"   Status: {metrics['training_status']}")
        if metrics.get("training_load"):
            print(f"   Load: {metrics['training_load']}")

        preds = metrics.get("race_predictions", {})
        if preds:
            print("\n🏁 Race Predictions:")
            for dist, time_str in preds.items():
                print(f"   {dist}: {time_str}")


def cmd_activity(activity_date):
    """Show detailed activity by date."""
    if not ACTIVITIES_DIR.exists():
        print("No activity files found.")
        return

    matches = sorted(ACTIVITIES_DIR.glob(f"{activity_date}*.json"))
    if not matches:
        print(f"No activity found for {activity_date}")
        return

    for filepath in matches:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        s = data.get("summary", {})
        print(f"=== {s.get('activityName', 'Activity')} ({s.get('startTimeLocal', '')}) ===\n")
        print(f"Distance: {s.get('distance', 0)/1000:.2f}km")
        print(f"Duration: {s.get('duration', 0)/60:.1f}min")
        print(f"Avg Pace: {format_pace(s.get('distance', 0), s.get('duration', 0))}/km")
        print(f"HR: avg {s.get('averageHR', '?')} / max {s.get('maxHR', '?')}")
        print(f"Cadence: {s.get('averageRunningCadenceInStepsPerMinute', '?')}spm")
        print(f"Elevation: +{s.get('elevationGain', 0):.0f}m / -{s.get('elevationLoss', 0):.0f}m")

        # Splits
        splits = data.get("splits", {})
        laps = splits.get("lapDTOs", [])
        if laps:
            print(f"\n--- Splits ({len(laps)} laps) ---")
            for i, lap in enumerate(laps, 1):
                dist = lap.get("distance", 0) / 1000
                dur = lap.get("duration", 0)
                pace = format_pace(lap.get("distance", 0), dur)
                hr = lap.get("averageHR", "?")
                print(f"  Lap {i}: {dist:.2f}km | {pace}/km | HR {hr}")

        # HR zones
        zones = data.get("hr_zones", [])
        if zones:
            print("\n--- HR Zones ---")
            for z in zones:
                zn = z.get("zoneNumber", "?")
                secs = z.get("secsInZone", 0)
                if secs > 0:
                    print(f"  Zone {zn}: {secs/60:.1f}min")

        print()


def cmd_json():
    """Output raw summary as JSON (for bot parsing)."""
    summary = load_summary()
    if summary:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print("{}")


def format_pace(distance_m, duration_s):
    if not distance_m or distance_m == 0:
        return "?"
    pace_s = duration_s / (distance_m / 1000)
    minutes = int(pace_s // 60)
    seconds = int(pace_s % 60)
    return f"{minutes}:{seconds:02d}"


def main():
    if len(sys.argv) < 2:
        print("Usage: garmin-query.py <command> [args]")
        print()
        print("Commands:")
        print("  recent [n]     - Show recent N activities (default 5)")
        print("  weekly         - Weekly training summary")
        print("  stats          - Daily stats + training metrics")
        print("  activity DATE  - Detailed activity (e.g. 2026-03-18)")
        print("  json           - Raw summary JSON")
        return

    cmd = sys.argv[1]

    if cmd == "recent":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        cmd_recent(n)
    elif cmd == "weekly":
        cmd_weekly()
    elif cmd == "stats":
        cmd_stats()
    elif cmd == "activity":
        if len(sys.argv) < 3:
            print("Usage: garmin-query.py activity YYYY-MM-DD")
            return
        cmd_activity(sys.argv[2])
    elif cmd == "json":
        cmd_json()
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
