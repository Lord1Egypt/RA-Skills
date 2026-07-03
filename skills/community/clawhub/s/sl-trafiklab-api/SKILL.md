---
name: sl-trafiklab-api
description: "Fetch real-time SL (Stockholm public transport) departures and deviation information using a Python CLI tool. Use when checking upcoming departures, querying transit delays, or configuring favourite sites/routes for autonomous monitoring. Note: The skill can query ANY site or line on demand; favorites are solely for autonomous background monitoring."
metadata: {"openclaw": {"requires": {"bins": ["python"]}}}
---

# SL Trafiklab API Skill

This skill retrieves real-time departure and deviation information from SL (Stockholm public transport) via a Python CLI client. It **does NOT require registration** of sites to make queries—you can query departures and deviations for any site or line on demand. The favorites configuration is **only for autonomous background monitoring** (e.g., heartbeat checks, cron jobs that proactively notify about disruptions).

The most critical task when handling background monitoring is to **filter out noise**. The user should not be notified about disruptions at sites/lines they're not actually using on that specific route.

## Preferences Storage
Preferences for **autonomous monitoring** are stored in your workspace at `.sl/preferences.json`.
You must interact with this configuration exclusively via the `site save/remove` and `route save/remove` subcommands, which handle validation.

## Core Actions
All actions are performed by invoking `python scripts/cli.py`. For detailed command arguments and response layouts, refer to **`references/api.md`**.

1. **site list**: Search for a transit site's numeric ID by name.
   - Command: `python scripts/cli.py site list "<query>"`
2. **site departures**: Fetch upcoming real-time departures.
   - Command: `python scripts/cli.py site departures <site_id> [--line <line>] [--transport <mode>] [--direction <dir>] [--forecast <forecast>]`
3. **site check**: Check departures/disruptions for a single site or all favorite stops.
   - Command: `python scripts/cli.py site check [<site_id>] [-v]`
4. **site save / remove**: Save or remove favorite stops in preferences for background monitoring.
   - Commands: `python scripts/cli.py site save <site_id> "<display_name>" [--lines <lines>] [--modes <modes>]` / `python scripts/cli.py site remove <site_id>`
5. **route check**: Print upcoming departures, show active/planned transit deviations, and check connection safety buffers for one or all favorite routes.
   - Command: `python scripts/cli.py route check [<alias>] [-v]`
6. **route find**: Search travel proposals dynamically using SL's transit router, supporting alias inputs, custom departure times/dates, leg preference matching, via stop details, and exclusions.
   - Command: `python scripts/cli.py route find <origin_or_alias> [<destination>] [--time <HH:MM>] [--date <YYYY-MM-DD>] [--number <1-3>] [--all] [--via <via_stop>] [--dwell-time <HH:MM>] [--not-via <avoid_stop>]`
7. **route save / remove**: Save or remove favorite routes in preferences. Supports three modes:
   - **Default / Unconstrained (3-argument syntax or index 0)**: Saves a direct start-to-destination connection. Queries the Journey Planner under the hood to automatically configure travel duration, direct lines, and direction filters. Used to monitor all options between two points.
     - Command: `python scripts/cli.py route save <origin> <destination> <alias> [--time <HH:MM>] [--date <YYYY-MM-DD>]`
   - **Specific Journey Proposal (4-argument syntax)**: Saves the exact legs and transfers of a specific journey proposal (indices 1-3). Used to monitor transfer connection safety buffers at specific steps.
     - Command: `python scripts/cli.py route save <origin> <destination> <proposal_index> <alias> [--time <HH:MM>] [--date <YYYY-MM-DD>]`
   - **Manual Legs Array (2-argument syntax)**: Saves a custom leg sequence manually using a JSON array of leg objects. Refer to [api.md](file:///c:/Users/patrk/Documents/antigravity/sl-trafiklab-api/references/api.md#L36-L57) for the required JSON schema format.
     - Command: `python scripts/cli.py route save <alias> '<legs_json>'`
   - **Route Removal**: `python scripts/cli.py route remove <alias>`
8. **deviations**: Fetch active or planned transit disruptions.
   - Command: `python scripts/cli.py deviations [--site <site_id>] [--line <line>] [--future]`
