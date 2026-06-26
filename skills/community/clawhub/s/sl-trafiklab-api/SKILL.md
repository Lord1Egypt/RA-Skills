---
name: sl-trafiklab-api
description: "Fetch real-time SL (Stockholm public transport) departures and deviation information. Use when checking upcoming departures from stops, querying active train/bus delays, or configuring favourite stops/routes for autonomous monitoring. Note: The skill can query ANY stop or route on demand without registration; favourite_stops and favourite_routes are solely for autonomous background monitoring."
metadata: {"openclaw": {"requires": {"bins": ["curl", "jq"]}}}
---

# SL Trafiklab API Skill

This skill retrieves real-time departure and deviation information from SL (Stockholm public transport). It **does NOT require registration** of stops or routes to make queries—you can query any stop or route on demand. The `favourite_stops` and `favourite_routes` configuration is **only for autonomous background monitoring** (e.g., heartbeat checks, cron jobs that proactively notify about disruptions).

The most critical task when handling background routes is to **filter out noise**. The user should not be notified about disruptions at stops/lines they're not actually using on that specific route.

## State Storage
Preferences for **autonomous monitoring** are maintained in your workspace at `.sl/preferences.json`.
Initialize this file with empty arrays if it does not exist.
See `references/api.md` for the exact JSON format, which includes `favourite_stops` and `favourite_routes`.

To save updates to the user's monitoring preferences, simply write valid JSON to `.sl/preferences.json`.

## Core Actions
For all specific API endpoints (`curl` commands), strict payload formats, and data extraction instructions, you must refer to **`references/api.md`**.

1. **search_sl_sites**: Finds the numeric Site ID for a given stop name. The Departures and Deviations APIs require numeric IDs. **Warning**: Large payload, see `references/api.md` for safe filtering via `jq`.
2. **fetch_departures**: Fetch real-time departures from ANY site (does not need to be in favourites). Returns upcoming departures with scheduled/expected times, destinations, and deviations. Optional filters: line, transport_mode, direction, forecast window.
3. **fetch_deviations**: Fetch disruption info for ANY site/line (does not need to be in favourites). You **must** utilize the strict assessment logic defined in `references/api.md` when filtering for autonomous notifications.
4. **manage_preferences**: Overwrite `.sl/preferences.json` to configure `favourite_stops` and `favourite_routes` for autonomous monitoring only.

## Autonomous Directives (Background Monitoring)
During autonomous execution (e.g., background heartbeat or cron job):
1. Load `.sl/preferences.json`.
2. Check `favourite_stops`:
   - For each stop, optionally filter by its registered `lines` and/or `transport_modes` when fetching departures
   - Fetch deviations affecting these stops
3. Check `favourite_routes`:
   - Execute detailed deviation checking using the strict assessment logic from `references/api.md`
   - For each leg of the route, verify disruptions actually affect the user's specific boarding/alighting stops
4. Compare returned deviation IDs against context memory.
5. Only send a notification if a new, relevant disruption is detected.
6. Adhere to Trafiklab's limit of maximum 1 request per minute.
