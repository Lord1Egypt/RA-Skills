#!/usr/bin/env python3
"""Insert a strength training session into sport schema.

Usage:
    python insert_workout.py '<json>'

JSON format:
{
  "session_date": "2026-03-02",
  "duration_min": 75,
  "feeling": 8,
  "notes": "...",
  "exercises": [
    {
      "exercise_name": "Squat",
      "sets": 4,
      "reps": 8,
      "weight_kg": 100.0,
      "rpe": 8.5,
      "rest_sec": 120,
      "order_in_session": 1,
      "notes": null
    }
  ]
}
"""

import json
import os
import sys
from datetime import date

import psycopg2


def get_conn():
    url = os.environ.get("DATABASE_URL")
    if url:
        return psycopg2.connect(url)
    return psycopg2.connect(
        host=os.environ.get("PGHOST", ""),
        port=os.environ.get("PGPORT", ""),
        dbname=os.environ.get("PGDATABASE", ""),
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
    )


def insert(data: dict):
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sport.sessions
                    (session_date, session_type, duration_min, feeling, notes)
                VALUES (%s, 'strength', %s, %s, %s)
                RETURNING id
                """,
                (
                    data.get("session_date", date.today().isoformat()),
                    data.get("duration_min"),
                    data.get("feeling"),
                    data.get("notes"),
                ),
            )
            session_id = cur.fetchone()[0]

            for i, ex in enumerate(data.get("exercises", []), start=1):
                cur.execute(
                    """
                    INSERT INTO sport.exercises
                        (session_id, exercise_name, sets, reps, weight_kg,
                         rpe, rest_sec, order_in_session, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        session_id,
                        ex["exercise_name"],
                        ex.get("sets"),
                        ex.get("reps"),
                        ex.get("weight_kg"),
                        ex.get("rpe"),
                        ex.get("rest_sec"),
                        ex.get("order_in_session", i),
                        ex.get("notes"),
                    ),
                )

        print(f"OK session_id={session_id}")
    finally:
        conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: insert_workout.py '<json>'", file=sys.stderr)
        sys.exit(1)

    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"ERROR invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    insert(payload)
