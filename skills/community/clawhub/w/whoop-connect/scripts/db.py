#!/usr/bin/env python3
"""SQLite persistence layer for WHOOP Connect."""

import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta, timezone

DB_DIR = os.path.expanduser("~/.whoop")
DB_PATH = os.path.join(DB_DIR, "whoop.db")


def get_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    _init_tables(conn)
    return conn


def _init_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS recovery (
            cycle_id INTEGER PRIMARY KEY,
            sleep_id TEXT,
            user_id INTEGER,
            created_at TEXT,
            updated_at TEXT,
            score_state TEXT,
            recovery_score REAL,
            hrv_rmssd_milli REAL,
            resting_heart_rate REAL,
            spo2_percentage REAL,
            skin_temp_celsius REAL,
            user_calibrating INTEGER,
            fetched_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS sleep (
            id TEXT PRIMARY KEY,
            cycle_id INTEGER,
            user_id INTEGER,
            created_at TEXT,
            updated_at TEXT,
            start TEXT,
            end TEXT,
            timezone_offset TEXT,
            nap INTEGER,
            score_state TEXT,
            total_in_bed_time_milli INTEGER,
            total_awake_time_milli INTEGER,
            total_light_sleep_time_milli INTEGER,
            total_slow_wave_sleep_time_milli INTEGER,
            total_rem_sleep_time_milli INTEGER,
            total_no_data_time_milli INTEGER,
            sleep_cycle_count INTEGER,
            disturbance_count INTEGER,
            respiratory_rate REAL,
            sleep_performance_percentage REAL,
            sleep_efficiency_percentage REAL,
            sleep_consistency_percentage REAL,
            baseline_milli INTEGER,
            need_from_sleep_debt_milli INTEGER,
            need_from_recent_strain_milli INTEGER,
            need_from_recent_nap_milli INTEGER,
            fetched_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS workout (
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            created_at TEXT,
            updated_at TEXT,
            start TEXT,
            end TEXT,
            timezone_offset TEXT,
            sport_name TEXT,
            score_state TEXT,
            strain REAL,
            average_heart_rate INTEGER,
            max_heart_rate INTEGER,
            kilojoule REAL,
            distance_meter REAL,
            altitude_gain_meter REAL,
            altitude_change_meter REAL,
            percent_recorded REAL,
            zone_zero_milli INTEGER,
            zone_one_milli INTEGER,
            zone_two_milli INTEGER,
            zone_three_milli INTEGER,
            zone_four_milli INTEGER,
            zone_five_milli INTEGER,
            fetched_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS cycle (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            created_at TEXT,
            updated_at TEXT,
            start TEXT,
            end TEXT,
            timezone_offset TEXT,
            score_state TEXT,
            strain REAL,
            kilojoule REAL,
            average_heart_rate INTEGER,
            max_heart_rate INTEGER,
            fetched_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS profile (
            user_id INTEGER PRIMARY KEY,
            email TEXT,
            first_name TEXT,
            last_name TEXT,
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS body_measurement (
            user_id INTEGER PRIMARY KEY,
            height_meter REAL,
            weight_kilogram REAL,
            max_heart_rate INTEGER,
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS api_call_log (
            date TEXT PRIMARY KEY,
            call_count INTEGER DEFAULT 0
        );

        CREATE INDEX IF NOT EXISTS idx_recovery_created ON recovery(created_at);
        CREATE INDEX IF NOT EXISTS idx_sleep_start ON sleep(start);
        CREATE INDEX IF NOT EXISTS idx_workout_start ON workout(start);
        CREATE INDEX IF NOT EXISTS idx_cycle_start ON cycle(start);
    """)
    conn.commit()


def upsert_recovery(conn, data):
    score = data.get("score") or {}
    conn.execute("""
        INSERT OR REPLACE INTO recovery
        (cycle_id, sleep_id, user_id, created_at, updated_at, score_state,
         recovery_score, hrv_rmssd_milli, resting_heart_rate,
         spo2_percentage, skin_temp_celsius, user_calibrating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["cycle_id"], data.get("sleep_id"), data["user_id"],
        data["created_at"], data["updated_at"], data["score_state"],
        score.get("recovery_score"), score.get("hrv_rmssd_milli"),
        score.get("resting_heart_rate"), score.get("spo2_percentage"),
        score.get("skin_temp_celsius"),
        1 if score.get("user_calibrating") else 0,
    ))
    conn.commit()


def upsert_sleep(conn, data):
    score = data.get("score") or {}
    stage = score.get("stage_summary") or {}
    needed = score.get("sleep_needed") or {}
    conn.execute("""
        INSERT OR REPLACE INTO sleep
        (id, cycle_id, user_id, created_at, updated_at, start, end,
         timezone_offset, nap, score_state,
         total_in_bed_time_milli, total_awake_time_milli,
         total_light_sleep_time_milli, total_slow_wave_sleep_time_milli,
         total_rem_sleep_time_milli, total_no_data_time_milli,
         sleep_cycle_count, disturbance_count, respiratory_rate,
         sleep_performance_percentage, sleep_efficiency_percentage,
         sleep_consistency_percentage,
         baseline_milli, need_from_sleep_debt_milli,
         need_from_recent_strain_milli, need_from_recent_nap_milli)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["id"], data.get("cycle_id"), data["user_id"],
        data["created_at"], data["updated_at"], data["start"], data["end"],
        data["timezone_offset"], 1 if data.get("nap") else 0, data["score_state"],
        stage.get("total_in_bed_time_milli"), stage.get("total_awake_time_milli"),
        stage.get("total_light_sleep_time_milli"), stage.get("total_slow_wave_sleep_time_milli"),
        stage.get("total_rem_sleep_time_milli"), stage.get("total_no_data_time_milli"),
        stage.get("sleep_cycle_count"), stage.get("disturbance_count"),
        score.get("respiratory_rate"),
        score.get("sleep_performance_percentage"), score.get("sleep_efficiency_percentage"),
        score.get("sleep_consistency_percentage"),
        needed.get("baseline_milli"), needed.get("need_from_sleep_debt_milli"),
        needed.get("need_from_recent_strain_milli"), needed.get("need_from_recent_nap_milli"),
    ))
    conn.commit()


def upsert_workout(conn, data):
    score = data.get("score") or {}
    zones = score.get("zone_durations") or {}
    conn.execute("""
        INSERT OR REPLACE INTO workout
        (id, user_id, created_at, updated_at, start, end,
         timezone_offset, sport_name, score_state,
         strain, average_heart_rate, max_heart_rate, kilojoule,
         distance_meter, altitude_gain_meter, altitude_change_meter,
         percent_recorded,
         zone_zero_milli, zone_one_milli, zone_two_milli,
         zone_three_milli, zone_four_milli, zone_five_milli)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["id"], data["user_id"], data["created_at"], data["updated_at"],
        data["start"], data["end"], data["timezone_offset"],
        data.get("sport_name"), data["score_state"],
        score.get("strain"), score.get("average_heart_rate"),
        score.get("max_heart_rate"), score.get("kilojoule"),
        score.get("distance_meter"), score.get("altitude_gain_meter"),
        score.get("altitude_change_meter"), score.get("percent_recorded"),
        zones.get("zone_zero_milli"), zones.get("zone_one_milli"),
        zones.get("zone_two_milli"), zones.get("zone_three_milli"),
        zones.get("zone_four_milli"), zones.get("zone_five_milli"),
    ))
    conn.commit()


def upsert_cycle(conn, data):
    score = data.get("score") or {}
    conn.execute("""
        INSERT OR REPLACE INTO cycle
        (id, user_id, created_at, updated_at, start, end,
         timezone_offset, score_state,
         strain, kilojoule, average_heart_rate, max_heart_rate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["id"], data["user_id"], data["created_at"], data["updated_at"],
        data["start"], data.get("end"), data["timezone_offset"], data["score_state"],
        score.get("strain"), score.get("kilojoule"),
        score.get("average_heart_rate"), score.get("max_heart_rate"),
    ))
    conn.commit()


def upsert_profile(conn, data):
    conn.execute("""
        INSERT OR REPLACE INTO profile (user_id, email, first_name, last_name)
        VALUES (?, ?, ?, ?)
    """, (data["user_id"], data["email"], data["first_name"], data["last_name"]))
    conn.commit()


def upsert_body(conn, data):
    conn.execute("""
        INSERT OR REPLACE INTO body_measurement
        (user_id, height_meter, weight_kilogram, max_heart_rate)
        VALUES (?, ?, ?, ?)
    """, (data.get("user_id", 0), data["height_meter"],
          data["weight_kilogram"], data["max_heart_rate"]))
    conn.commit()


# --- API call tracking ---

def get_daily_api_calls(conn, date_str=None):
    """Get the number of API calls made today."""
    if date_str is None:
        date_str = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    row = conn.execute(
        "SELECT call_count FROM api_call_log WHERE date = ?", (date_str,)
    ).fetchone()
    return row["call_count"] if row else 0


def increment_api_calls(conn, count=1, date_str=None):
    """Increment the daily API call counter. Returns new total."""
    if date_str is None:
        date_str = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    conn.execute("""
        INSERT INTO api_call_log (date, call_count) VALUES (?, ?)
        ON CONFLICT(date) DO UPDATE SET call_count = call_count + ?
    """, (date_str, count, count))
    conn.commit()
    return get_daily_api_calls(conn, date_str)


# --- Trend queries ---

METRIC_QUERIES = {
    "recovery_score": ("recovery", "recovery_score", "created_at"),
    "hrv": ("recovery", "hrv_rmssd_milli", "created_at"),
    "resting_hr": ("recovery", "resting_heart_rate", "created_at"),
    "spo2": ("recovery", "spo2_percentage", "created_at"),
    "skin_temp": ("recovery", "skin_temp_celsius", "created_at"),
    "strain": ("cycle", "strain", "start"),
    "sleep_duration": ("sleep", "total_in_bed_time_milli", "start"),
    "sleep_efficiency": ("sleep", "sleep_efficiency_percentage", "start"),
    "sleep_performance": ("sleep", "sleep_performance_percentage", "start"),
    "respiratory_rate": ("sleep", "respiratory_rate", "start"),
}


def query_trends(conn, metric, days=7):
    if metric not in METRIC_QUERIES:
        return {"error": f"Unknown metric: {metric}. Valid: {', '.join(METRIC_QUERIES)}"}

    table, column, date_col = METRIC_QUERIES[metric]
    cutoff = (datetime.now(tz=timezone.utc) - timedelta(days=days)).isoformat()

    rows = conn.execute(f"""
        SELECT {date_col} as date, {column} as value
        FROM {table}
        WHERE {date_col} >= ? AND {column} IS NOT NULL
        ORDER BY {date_col}
    """, (cutoff,)).fetchall()

    if not rows:
        return {"metric": metric, "days": days, "count": 0, "data": []}

    values = [r["value"] for r in rows]
    mean_val = sum(values) / len(values)
    min_val = min(values)
    max_val = max(values)

    variance = sum((v - mean_val) ** 2 for v in values) / len(values)
    std_val = variance ** 0.5

    # Trend direction: compare first half avg vs second half avg
    mid = len(values) // 2
    if mid > 0:
        first_half = sum(values[:mid]) / mid
        second_half = sum(values[mid:]) / (len(values) - mid)
        delta = second_half - first_half
        if abs(delta) < std_val * 0.1:
            trend = "stable"
        elif delta > 0:
            trend = "improving" if metric != "resting_hr" else "declining"
        else:
            trend = "declining" if metric != "resting_hr" else "improving"
    else:
        trend = "insufficient_data"

    return {
        "metric": metric,
        "days": days,
        "count": len(values),
        "mean": round(mean_val, 2),
        "std": round(std_val, 2),
        "min": round(min_val, 2),
        "max": round(max_val, 2),
        "trend": trend,
        "data": [{"date": r["date"], "value": r["value"]} for r in rows],
    }


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  db.py trends --metric <name> [--days N]")
        print(f"  Metrics: {', '.join(METRIC_QUERIES)}")
        sys.exit(0)

    if sys.argv[1] == "trends":
        metric = None
        days = 7
        args = sys.argv[2:]
        i = 0
        while i < len(args):
            if args[i] == "--metric" and i + 1 < len(args):
                metric = args[i + 1]
                i += 2
            elif args[i] == "--days" and i + 1 < len(args):
                days = int(args[i + 1])
                i += 2
            else:
                i += 1

        if not metric:
            print("Error: --metric required")
            sys.exit(1)

        conn = get_db()
        result = query_trends(conn, metric, days)
        print(json.dumps(result, indent=2))
        conn.close()
    else:
        print(f"Unknown command: {sys.argv[1]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
