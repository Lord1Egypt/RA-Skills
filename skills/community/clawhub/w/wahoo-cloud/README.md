# Wahoo Skill

An agentic skill for synchronizing Wahoo fitness data into a local SQLite database. Designed to be high-signal for LLM agents and comprehensive for human developers.

## 🚀 Agent Quickstart (High-Signal)

Use these commands to interact with Wahoo data.

### Core Capabilities
- **Sync Data**: `python3 scripts/fetch_workouts.py [--limit N]`
  - Fetches workout metadata and downloads/parses FIT files.
  - `--limit N`: Only process the N most recent workouts (useful for testing/rate-limit avoidance).
- **Auth Setup**: `python3 scripts/oauth_setup.py`
  - Interactive OAuth2 flow to generate access and refresh tokens.

### Environment Variables
| Variable | Description | Default |
| :--- | :--- | :--- |
| `WAHOO_BASE_DIR` | Base directory for all Wahoo files (secrets, DB, FITs) | `~/.wahoo` |
| `WAHOO_CLIENT_ID` | Wahoo API Client ID | *Required* |
| `WAHOO_CLIENT_SECRET` | Wahoo API Client Secret | *Required* |

### Data Schema (SQLite)
The data is stored in `[WAHOO_BASE_DIR]/wahoo.db`.

**Key Tables:**
- `workouts`: Metadata (name, starts, distance, duration, power, heart rate, etc.)
- `laps`: Detailed lap-by-lap breakdown of each workout.
- `records`: High-resolution sensor data (power, heart rate, cadence, GPS).
- `device_info`: Hardware details used during the workout.
- `zones`: Heart rate and power zone data.
- `sync_log`: History of synchronization runs.

---

## 🛠 Developer Guide (Human-Centric)

## Overview
This skill provides a bridge between the Wahoo API and a local, structured SQLite database. It handles the complexities of OAuth2 token refreshing, paginated API requests, FIT file downloading, and intensive data parsing.

## Architecture

### 1. Authentication Flow
The skill uses the OAuth2 Authorization Code flow.
- **Tokens Location**: `[WAHOO_BASE_DIR]/secrets/wahoo_tokens.json`
- **Environment File**: `[WAHOO_BASE_DIR]/secrets/wahoo.env` (Optional, used to load credentials).

### 2. Sync Workflow
The `fetch_workouts.py` script follows this pipeline:
1. **Auth**: Ensures a valid access token is available (refreshes if necessary).
2. **Discovery**: Iterates through `/v1/workouts` to find new or updated metadata.
3. **Metadata Upsert**: Updates the `workouts` table with the latest summary data.
4. **FIT Processing**: 
   - If a workout lacks a local FIT file or parsed data:
   - Downloads the `.fit` file from the `fit_url` provided by Wahoo.
   - Uses `fit_parser` to extract high-resolution metrics.
   - Populates `laps`, `records`, `device_info`, and `zones` tables.

### 3. Database Schema
The schema is managed via `schema/wahoo_db_schema.sql` and incremental migrations defined in `scripts/fetch_workouts.py`.

## Installation & Setup

1. **Clone the repository.**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Credentials**:
   Create a `.env` file in your `WAHOO_BASE_DIR` or set them in your shell:
   ```bash
   export WAHOO_CLIENT_ID='your_id'
   export WAHOO_CLIENT_SECRET='your_secret'
   ```
4. **Run OAuth Setup**:
   ```bash
   python3 scripts/oauth_setup.py
   ```

## Troubleshooting

### Rate Limiting (429 Errors)
The `wahoo_api` library includes built-in exponential backoff. If you encounter persistent 429s, use the `--limit` flag in the sync script to reduce the payload size per run.

### Database Errors
If you encounter "no such column" errors, ensure you have run a full sync recently to allow the migration logic in `fetch_workouts.py` to update your schema.

## License
MIT
