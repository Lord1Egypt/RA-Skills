# workout-track

OpenClaw skill to log strength training sessions from natural language into a PostgreSQL database.

## What it does

Tell your agent about your gym session — exercises, sets, reps, weights, RPE, rest times, duration, how you felt — and it parses, confirms, and stores everything in a structured `sport` schema.

## Requirements

- PostgreSQL database
- `uv` for running the insert script (`uv run --project ~/.openclaw`)
- Credentials in `~/.openclaw/services/life-db/.env`

## Setup

1. Create the database schema:
   ```bash
   psql -f skills/workout-track/schema.sql
   ```

2. Create your `~/.openclaw/services/life-db/.env`:
   ```env
   PGHOST=localhost
   PGPORT=5432
   PGDATABASE=life_db
   PGUSER=...
   PGPASSWORD=...
   ```

3. Install the skill via clawhub:
   ```bash
   clawhub install workout-track
   ```

## Usage

Just tell your agent what you did:

> "Séance muscu aujourd'hui, 75 min, feeling 8/10. Squat 4×8 à 100kg, bench 3×10 à 80kg, soulevé de terre 3×5 à 130kg."

The agent will show a recap, ask for confirmation, then insert the session.
