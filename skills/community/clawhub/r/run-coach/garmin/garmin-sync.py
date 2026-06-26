#!/usr/bin/env python3
"""Garmin Connect data sync for run-coach bot.
Reads credentials from environment variables GARMIN_EMAIL and GARMIN_PASSWORD.
Writes JSON activity data to the garmin/ directory for the bot to query.
"""

import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

# Workspace is always the directory containing this script's parent
_WORKSPACE = Path(__file__).parent.parent

GARTH_HOME = str(_WORKSPACE / "garmin" / ".garth")
GARMIN_DIR = _WORKSPACE / "garmin"
ACTIVITIES_DIR = GARMIN_DIR / "activities"
SUMMARY_FILE = GARMIN_DIR / "summary.json"


def load_credentials():
    """Load Garmin credentials from environment variables."""
    email = os.environ.get("GARMIN_EMAIL", "").strip()
    password = os.environ.get("GARMIN_PASSWORD", "").strip()

    if not email or not password:
        print("Error: GARMIN_EMAIL and GARMIN_PASSWORD environment variables must be set.")
        print("Add them to your OpenClaw config or .env file:")
        print("  GARMIN_EMAIL=your@email.com")
        print("  GARMIN_PASSWORD=your_password")
        sys.exit(1)

    return email, password


def get_client():
    """Authenticate with Garmin Connect, using cached tokens when possible."""
    email, password = load_credentials()

    client = Garmin(email=email, password=password)

    # Try token-based login first
    if Path(GARTH_HOME).exists():
        try:
            client.login(GARTH_HOME)
            print("Logged in with cached token.")
            return client
        except Exception:
            print("Cached token expired, re-authenticating...")

    # Fresh login
    try:
        client.login()
        client.garth.dump(GARTH_HOME)
        print("Fresh login successful, token cached.")
        return client
    except GarminConnectAuthenticationError as e:
        print(f"Auth failed: {e}")
        sys.exit(1)
    except GarminConnectConnectionError as e:
        print(f"Connection error: {e}")
        sys.exit(1)
    except GarminConnectTooManyRequestsError as e:
        print(f"Rate limited: {e}")
        sys.exit(1)


def sync_activities(client, days=7):
    """Fetch recent running activities and save as JSON."""
    end_date = date.today().isoformat()
    start_date = (date.today() - timedelta(days=days)).isoformat()

    print(f"Fetching activities from {start_date} to {end_date}...")

    activities = client.get_activities_by_date(
        startdate=start_date,
        enddate=end_date,
        activitytype="running",
    )

    print(f"Found {len(activities)} running activities.")

    saved = []
    for activity in activities:
        activity_id = activity.get("activityId")
        activity_date = activity.get("startTimeLocal", "")[:10]

        # Fetch detailed data
        detail = {}
        try:
            detail["summary"] = activity
            detail["splits"] = client.get_activity_splits(activity_id)
            detail["hr_zones"] = client.get_activity_hr_in_timezones(activity_id)
        except Exception as e:
            print(f"  Warning: couldn't fetch details for {activity_id}: {e}")
            detail["summary"] = activity

        # Save individual activity file
        filename = f"{activity_date}_{activity_id}.json"
        filepath = ACTIVITIES_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(detail, f, ensure_ascii=False, indent=2, default=str)

        saved.append({
            "date": activity_date,
            "id": activity_id,
            "name": activity.get("activityName", ""),
            "distance_km": round(activity.get("distance", 0) / 1000, 2),
            "duration_min": round(activity.get("duration", 0) / 60, 1),
            "avg_hr": activity.get("averageHR"),
            "max_hr": activity.get("maxHR"),
            "avg_pace": format_pace(activity.get("distance", 0), activity.get("duration", 0)),
            "calories": activity.get("calories"),
            "avg_cadence": activity.get("averageRunningCadenceInStepsPerMinute"),
            "file": filename,
        })
        print(f"  Saved: {filename}")

    return saved


def sync_daily_stats(client):
    """Fetch today's daily stats."""
    today = date.today().isoformat()
    try:
        stats = client.get_stats_and_body(today)
        return {
            "date": today,
            "steps": stats.get("totalSteps"),
            "distance_km": round((stats.get("totalDistanceMeters") or 0) / 1000, 2),
            "calories_total": stats.get("totalKilocalories"),
            "calories_active": stats.get("activeKilocalories"),
            "resting_hr": stats.get("restingHeartRate"),
            "min_hr": stats.get("minHeartRate"),
            "max_hr": stats.get("maxHeartRate"),
            "stress_avg": stats.get("averageStressLevel"),
            "body_battery_high": stats.get("bodyBatteryChargedValue"),
            "body_battery_low": stats.get("bodyBatteryDrainedValue"),
        }
    except Exception as e:
        print(f"Warning: couldn't fetch daily stats: {e}")
        return None


def sync_training_metrics(client):
    """Fetch training status, VO2max, race predictions."""
    today = date.today().isoformat()
    metrics = {}

    try:
        max_metrics = client.get_max_metrics(today)
        # Returns a list, take first element
        if isinstance(max_metrics, list) and max_metrics:
            max_metrics = max_metrics[0]
        generic = max_metrics.get("generic", {}) if max_metrics else {}
        metrics["vo2max"] = generic.get("vo2MaxPreciseValue")
        metrics["fitness_age"] = generic.get("fitnessAge")
    except Exception as e:
        print(f"Warning: VO2max not available (FR235 may not support): {e}")

    try:
        training = client.get_training_status(today)
        if training:
            metrics["training_status"] = training.get("trainingStatusKey")
            metrics["training_load"] = training.get("trainingLoad")
    except Exception as e:
        print(f"Warning: training status not available: {e}")

    try:
        preds = client.get_race_predictions()
        if preds:
            race_predictions = {}
            for race in preds:
                dist_km = race.get("raceDistanceInMeters", 0) / 1000
                time_s = race.get("raceTimeinSeconds", 0)
                if dist_km > 0 and time_s > 0:
                    h = int(time_s // 3600)
                    m = int((time_s % 3600) // 60)
                    s = int(time_s % 60)
                    label = f"{dist_km:.0f}km"
                    race_predictions[label] = f"{h}:{m:02d}:{s:02d}"
            metrics["race_predictions"] = race_predictions
    except Exception as e:
        print(f"Warning: race predictions not available: {e}")

    return metrics


def format_pace(distance_m, duration_s):
    """Calculate pace in min/km format."""
    if not distance_m or distance_m == 0:
        return None
    pace_s = duration_s / (distance_m / 1000)
    minutes = int(pace_s // 60)
    seconds = int(pace_s % 60)
    return f"{minutes}:{seconds:02d}"


def build_summary(recent_activities, daily_stats, training_metrics):
    """Build summary JSON combining all data."""
    summary = {
        "last_sync": date.today().isoformat(),
        "recent_activities": recent_activities,
        "daily_stats": daily_stats,
        "training_metrics": training_metrics,
    }
    return summary


def main():
    days = 14
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except ValueError:
            pass

    # Ensure directories exist
    ACTIVITIES_DIR.mkdir(parents=True, exist_ok=True)

    print(f"=== Garmin Sync ({date.today().isoformat()}) ===")

    client = get_client()

    # Save token after successful operations
    recent = sync_activities(client, days=days)
    daily = sync_daily_stats(client)
    training = sync_training_metrics(client)

    # Persist token
    client.garth.dump(GARTH_HOME)

    # Write summary
    summary = build_summary(recent, daily, training)
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=str)

    print(f"\nSummary written to {SUMMARY_FILE}")
    print(f"Activities: {len(recent)}")
    if daily:
        print(f"Resting HR: {daily.get('resting_hr')}")
    if training.get("vo2max"):
        print(f"VO2max: {training['vo2max']}")
    print("=== Done ===")


if __name__ == "__main__":
    main()
