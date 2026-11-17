# SL Trafiklab CLI & API References

The `sl-trafiklab-api` skill wraps the SL Integration and Deviations APIs using a standalone, zero-dependency Python script at `skills/sl-trafiklab-api/scripts/cli.py`.

---

## Favorites Storage (`.sl/preferences.json`)

The preferences file stores favorite stops and multi-leg routes. It is loaded and modified using the favorite commands.

### Format Example

> [!NOTE]
> - **`id`**: The short numeric **parent site ID** (e.g. `1386`, `9530`). This is required by the departures API and is used by `route check`.
> - **`stop_id`** (optional): The platform/stop-point level ID (e.g. `18010957`). If present, it is used by `route find` to filter matching travel proposals.

```json
{
  "favourite_stops": [
    { 
      "id": 9001, 
      "name": "T-Centralen" 
    },
    { 
      "id": 9117, 
      "name": "Odenplan",
      "transport_modes": ["METRO"]
    },
    { 
      "id": 9192, 
      "name": "Gullmarsplan",
      "lines": ["4", "66"],
      "transport_modes": ["BUS", "METRO"]
    }
  ],
  "favourite_routes": [
    {
      "name": "Daily Commute",
      "legs": [
        { 
          "lines": ["66"], 
          "from": { "id": 1001, "name": "Generic Stop A" }, 
          "to": { "id": 1002, "name": "Generic Stop B" },
          "travel_time_minutes": 15
        },
        { 
          "lines": ["40", "41"], 
          "from": { "id": 9002, "name": "Generic Station B" }, 
          "to": { "id": 9003, "name": "Generic Station C" },
          "travel_time_minutes": 20,
          "direction": ["Generic Terminus C", "Generic Terminus D"]
        }
      ]
    }
  ]
}
```

---

## CLI Reference

All commands are run using Python:

### 1. `site` Core Commands

- **Search Sites:** Search for a transit stop's numeric Site ID by name.
  ```bash
  python3 skills/sl-trafiklab-api/scripts/cli.py site list "Odenplan"
  ```
- **Fetch Departures:** Get live upcoming departures for a site.
  ```bash
  python3 skills/sl-trafiklab-api/scripts/cli.py site departures 9117 --line 4 --transport BUS
  ```

  > **Note — lookahead window and line filtering:** `site departures` returns a live
  > subset of upcoming departures, roughly the next hour (the SL transport API's
  > lookahead window). When you filter with `--line` and/or `--direction`, the CLI
  > fetches the full board and filters **locally** to avoid the API's server-side
  > cap (filtered requests return only a small subset, ~3 rows, regardless of any
  > limit parameter). It still returns at most the API's ~1-hour window, so for a
  > complete schedule — or departures beyond the immediate lookahead — use
  > `route find` (journey planner) instead.
  >
  > `--direction` filters by numeric code (`1`/`2`); departures heading toward the
  > destination of interest are the relevant ones.

### 2. `site` Favorite & Check Commands

- **Check Stations:** Verify departures and disruptions for one or all saved favorite sites.
  ```bash
  # Check all favorite sites
  python3 skills/sl-trafiklab-api/scripts/cli.py site check

  # Check only site ID 9117 (with verbose details)
  python3 skills/sl-trafiklab-api/scripts/cli.py site check 9117 -v
  ```
- **Save Favorite Site:** Add or update a station/stop site in preferences.
  ```bash
  python3 skills/sl-trafiklab-api/scripts/cli.py site save 9001 "T-Centralen" --lines "17,18,19" --modes METRO
  ```
- **Remove Favorite Site:** Remove a site from preferences.
  ```bash
  python3 skills/sl-trafiklab-api/scripts/cli.py site remove 9001
  ```
### 3. `route` Commands

- **Check Routes:** Evaluate departures, show upcoming departures for each leg, and evaluate connection safety buffers for one or all favorite routes.
  ```bash
  # Check all favorite routes
  python3 skills/sl-trafiklab-api/scripts/cli.py route check

  # Check only the "Daily Commute" route
  python3 skills/sl-trafiklab-api/scripts/cli.py route check "Daily Commute" -v
  ```

- **Find Travel Proposals:** Search dynamically for travel proposals using SL's routing engine. Supports alias resolving, future times, leg-preference matching, via routing, and stop exclusions.
  ```bash
  # Search travel options between two stops
  python3 skills/sl-trafiklab-api/scripts/cli.py route find "Generic Stop A" "Generic Stop B"

  # Search future options
  python3 skills/sl-trafiklab-api/scripts/cli.py route find "Generic Stop A" "Generic Stop B" --time "08:00" --date "2026-07-02"

  # Search via an intermediate stop with an optional dwell time
  python3 skills/sl-trafiklab-api/scripts/cli.py route find "Generic Stop A" "Generic Stop B" --via "Generic Via Stop" --dwell-time "00:10"

  # Search excluding/avoiding a specific station
  python3 skills/sl-trafiklab-api/scripts/cli.py route find "Generic Stop A" "Generic Stop B" --not-via "Avoided Stop"

  # Search by alias, filtering options against saved leg constraints
  python3 skills/sl-trafiklab-api/scripts/cli.py route find "Daily Commute"

  # Bypass leg constraints to see all transit alternatives between alias terminals
  python3 skills/sl-trafiklab-api/scripts/cli.py route find "Daily Commute" --all
  ```

The `--time` and `--date` inputs are **Stockholm local time** (e.g. `--time "08:00"` = 08:00 local departure), but the returned leg times are **UTC**. During summer time (CEST, UTC+2) a `--time "08:00"` request therefore surfaces legs around 06:00 UTC on screen — that is expected. Always convert returned times to the user's local timezone (Europe/Stockholm) before presenting.
- **Save Favorite Route:** Add or update a route using either manual legs JSON, selecting a specific journey proposal, or saving a start-to-destination connection.
  ```bash
  # Format A: Save using manual legs JSON
  python3 skills/sl-trafiklab-api/scripts/cli.py route save "Daily Commute" '[{"lines":["10"],"from":{"id":1001,"name":"Generic Stop A"},"to":{"id":1002,"name":"Generic Stop B"},"travel_time_minutes":15}]'

  # Format B: Save transit legs dynamically from proposal option 1 (optionally specifying typical travel time/date)
  python3 skills/sl-trafiklab-api/scripts/cli.py route save "Generic Stop A" "Generic Stop B" 1 "Daily Commute" --time "07:30" --date "2026-07-02"

  # Format C: Save direct start/stop connection without line constraints (proposal index 0)
  python3 skills/sl-trafiklab-api/scripts/cli.py route save "Generic Stop A" "Generic Stop B" 0 "Daily Commute"

  # Format D: Save start/stop connection using the default signature (origin, destination, and alias) (equivalent to index 0)
  python3 skills/sl-trafiklab-api/scripts/cli.py route save "Generic Stop A" "Generic Stop B" "Daily Commute"
  ```

  > [!TIP]
  > Saving via Format C/D (default/index 0) queries the Journey Planner under the hood. It automatically configures typical travel duration (from the first option), collects and consolidates direct line numbers, and configures direction filters to avoid noise. If no travel options are found, it falls back to saving with empty line lists and 0 travel time.

  > [!IMPORTANT]
  > **Workflow for saving a route with specific constraints (like a line number or transfer path):**
  > To save a route that satisfies specific constraints (e.g., must use Line 10, or must follow a specific transfer path), use `route find` followed by `route save`:
  > 1. Run `python3 skills/sl-trafiklab-api/scripts/cli.py route find "<origin>" "<destination>" [--time <HH:MM>] [--date <YYYY-MM-DD>]` to list travel proposals.
  > 2. Look at the output options and choose the one that matches your requirements (e.g., Option 2 uses Line 10).
  > 3. Save using that option index (Format B, passing the option index along with the exact same time/date parameters to ensure option alignment): `python3 skills/sl-trafiklab-api/scripts/cli.py route save "<origin>" "<destination>" <option_index> "<alias>" [--time <HH:MM>] [--date <YYYY-MM-DD>]` (e.g., `python3 skills/sl-trafiklab-api/scripts/cli.py route save "Generic Stop A" "Generic Stop B" 2 "Daily Commute" --time "07:30" --date "2026-07-02"`).
- **Remove Favorite Route:** Remove a route by alias.
  ```bash
  # Remove favorite route by name
  python3 skills/sl-trafiklab-api/scripts/cli.py route remove "Daily Commute"
  ```

### 4. `deviations` Command

- **Fetch Transit Disruptions:** Check active deviations affecting specific lines or stop sites.
  ```bash
  python3 skills/sl-trafiklab-api/scripts/cli.py deviations --site 9001 --line 40 -v
  ```


---

## Running the Test Suite

The skill includes a built-in test suite using **pytest** to verify CLI and API functionality:

- **Run all tests (both offline unit tests and live integration checks):**
  ```bash
  pytest
  ```
- **Run only unit tests (offline mock testing):**
  ```bash
  pytest -m "not integration"
  ```
- **Run only integration tests (live network testing):**
  ```bash
  pytest -m integration
  ```

