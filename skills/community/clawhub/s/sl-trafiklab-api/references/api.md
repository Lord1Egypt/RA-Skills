# SL Trafiklab CLI & API References

The `sl-trafiklab-api` skill wraps the SL Integration and Deviations APIs using a standalone, zero-dependency Python script at `scripts/cli.py`.

---

## State Storage (`.sl/preferences.json`)

The monitoring preferences file stores sites and multi-leg routes configured for autonomous background check notifications. It is loaded and modified using the `favorite` namespace commands.

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
  python scripts/cli.py site list "Odenplan"
  ```
- **Fetch Departures:** Get live upcoming departures for a site.
  ```bash
  python scripts/cli.py site departures 9117 --line 4 --transport BUS
  ```

### 2. `site` Favorite & Check Commands

- **Check Stations:** Verify departures and disruptions for one or all saved favorite sites.
  ```bash
  # Check all favorite sites
  python scripts/cli.py site check

  # Check only site ID 9117 (with verbose details)
  python scripts/cli.py site check 9117 -v
  ```
- **Save Favorite Site:** Add or update a station/stop site in preferences.
  ```bash
  python scripts/cli.py site save 9001 "T-Centralen" --lines "17,18,19" --modes METRO
  ```
- **Remove Favorite Site:** Remove a site from preferences.
  ```bash
  python scripts/cli.py site remove 9001
  ```
### 3. `route` Commands

- **Check Routes:** Evaluate departures, show upcoming departures for each leg, and evaluate connection safety buffers for one or all favorite routes.
  ```bash
  # Check all favorite routes
  python scripts/cli.py route check

  # Check only the "Daily Commute" route
  python scripts/cli.py route check "Daily Commute" -v
  ```

- **Find Travel Proposals:** Search dynamically for travel proposals using SL's routing engine. Supports alias resolving, future times, leg-preference matching, via routing, and stop exclusions.
  ```bash
  # Search travel options between two stops
  python scripts/cli.py route find "Generic Stop A" "Generic Stop B"

  # Search future options
  python scripts/cli.py route find "Generic Stop A" "Generic Stop B" --time "08:00" --date "2026-07-02"

  # Search via an intermediate stop with an optional dwell time
  python scripts/cli.py route find "Generic Stop A" "Generic Stop B" --via "Generic Via Stop" --dwell-time "00:10"

  # Search excluding/avoiding a specific station
  python scripts/cli.py route find "Generic Stop A" "Generic Stop B" --not-via "Avoided Stop"

  # Search by alias, filtering options against saved leg constraints
  python scripts/cli.py route find "Daily Commute"

  # Bypass leg constraints to see all transit alternatives between alias terminals
  python scripts/cli.py route find "Daily Commute" --all
  ```
- **Save Favorite Route:** Add or update a route using either manual legs JSON, selecting a specific journey proposal, or saving a start-to-destination connection.
  ```bash
  # Format A: Save using manual legs JSON
  python scripts/cli.py route save "Daily Commute" '[{"lines":["10"],"from":{"id":1001,"name":"Generic Stop A"},"to":{"id":1002,"name":"Generic Stop B"},"travel_time_minutes":15}]'

  # Format B: Save transit legs dynamically from proposal option 1 (optionally specifying typical travel time/date)
  python scripts/cli.py route save "Generic Stop A" "Generic Stop B" 1 "Daily Commute" --time "07:30" --date "2026-07-02"

  # Format C: Save direct start/stop connection without line constraints (proposal index 0)
  python scripts/cli.py route save "Generic Stop A" "Generic Stop B" 0 "Daily Commute"

  # Format D: Save start/stop connection using the new default 3-argument syntax (equivalent to index 0)
  python scripts/cli.py route save "Generic Stop A" "Generic Stop B" "Daily Commute"

  > [!TIP]
  > Saving via Format C/D (default/index 0) queries the Journey Planner under the hood. It automatically configures typical travel duration (from the first option), collects and consolidates direct line numbers, and configures direction filters to avoid noise. If no travel options are found, it falls back to saving with empty line lists and 0 travel time.
  ```
- **Remove Favorite Route:** Remove a route by alias.
  ```bash
  # Remove favorite route by name
  python scripts/cli.py route remove "Daily Commute"
  ```

### 4. `deviations` Command

- **Fetch Transit Disruptions:** Check active deviations affecting specific lines or stop sites.
  ```bash
  python scripts/cli.py deviations --site 9001 --line 40 -v
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

