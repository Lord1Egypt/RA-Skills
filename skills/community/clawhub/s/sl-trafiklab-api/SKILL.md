---
name: sl-trafiklab-api
description: "Fetch real-time SL (Stockholm public transport) departures and deviation information using a Python CLI tool. Use when checking departures, querying transit delays, or saving favorite sites and routes for quick status checks."
metadata: {"openclaw": {"requires": {"bins": ["python3"]}}}
---

# SL Trafiklab API Skill

This skill retrieves real-time departure and deviation information from SL (Stockholm public transport) via a Python CLI client. It **does NOT require registration** of sites to make queries—you can query departures and deviations for any site or line on demand. The favorites configuration allows you to **save frequently used stops and routes** to run quick status checks (e.g., departures, disruptions, and safety buffers) without re-entering names or IDs.

The most critical task when checking saved routes is to **filter out noise**. The user should not be notified about disruptions at sites or lines they are not actually using on that specific route.

## Favorites Storage
Your favorite stops and routes are stored in your workspace at `.sl/preferences.json`.
You must interact with this configuration exclusively via the `site save/remove` and `route save/remove` subcommands, which handle validation.

## CLI Execution Context

The skill is written for the **ClawHub-installed layout**: it lives in the agent workspace under `skills/sl-trafiklab-api/` and all commands are invoked as `python3 skills/sl-trafiklab-api/scripts/cli.py` **from the agent workspace root** (e.g. `~/.openclaw/workspace-assistant`).

**Always run the CLI from the agent workspace root**, not from inside the skill directory. The `preferences.json` path is resolved relative to the current working directory, not the skill directory. Running from any other directory will cause `route check`, `site check`, and other preference-dependent commands to silently report "not found."

Use `python3` (not `python`) as the invocation command on systems where Python 3 is installed without a `python` symlink.

### `--direction` Flag
The `--direction` flag on `site departures` accepts **numeric codes only** (`1` or `2`), not destination names. Passing destination name strings (e.g. `"Märsta"`) will be rejected with a helpful error message.

### `route find` Time Output
`route find` returns departure and arrival times in **UTC**. Always convert to the user's local timezone (Europe/Stockholm) before presenting results.

The `--time` and `--date` **inputs** are interpreted as **Stockholm local time** (i.e. `--time 15:00` means a 15:00 local departure), while the returned leg times are UTC. Do not confuse the two: with summer time (CEST, UTC+2), a `--time 12:00` request may show first legs around 10:00 UTC on screen — that is correct, not a bug.

## Core Actions
All actions are performed by invoking `python3 skills/sl-trafiklab-api/scripts/cli.py`. For detailed command arguments and response layouts, refer to **`references/api.md`**.

1. **site list**: Search for a transit site's numeric ID by name.
   - Command: `python3 skills/sl-trafiklab-api/scripts/cli.py site list "<query>"`
2. **site departures**: Fetch upcoming real-time departures.
   - Command: `python3 skills/sl-trafiklab-api/scripts/cli.py site departures <site_id> [--line <line>] [--transport <mode>] [--direction <dir>] [--forecast <forecast>]`
   - `--direction` filters by numeric code (`1`/`2`). Line/direction filters are applied **locally** so the response is not truncated to the API's server-side cap (filtered requests return only a small subset, ~3 rows). The board still covers roughly the next hour; for a fuller schedule or planning use `route find`.
3. **site check**: Check departures/disruptions for a single site or all favorite stops.
   - Command: `python3 skills/sl-trafiklab-api/scripts/cli.py site check [<site_id>] [-v]`
4. **site save / remove**: Save or remove favorite stops in preferences for background monitoring.
   - Commands: `python3 skills/sl-trafiklab-api/scripts/cli.py site save <site_id> "<display_name>" [--lines <lines>] [--modes <modes>]` / `python3 skills/sl-trafiklab-api/scripts/cli.py site remove <site_id>`
5. **route check**: Print upcoming departures, show active/planned transit deviations, and check connection safety buffers for one or all favorite routes.
   - Command: `python3 skills/sl-trafiklab-api/scripts/cli.py route check [<alias>] [-v]`
6. **route find**: Search travel proposals dynamically using SL's transit router, supporting alias inputs, custom departure times/dates, leg preference matching, via stop details, and exclusions.
   - Command: `python3 skills/sl-trafiklab-api/scripts/cli.py route find <origin_or_alias> [<destination>] [--time <HH:MM>] [--date <YYYY-MM-DD>] [--number <1-3>] [--all] [--via <via_stop>] [--dwell-time <HH:MM>] [--not-via <avoid_stop>]`
7. **route save / remove**: Save or remove favorite routes in preferences. Supports three modes:
   - **Default / Unconstrained (Origin & Destination)**: Saves a direct start-to-destination connection. Queries the Journey Planner under the hood to automatically configure travel duration, direct lines, and direction filters. Used to monitor all options between two points.
     - Command: `python3 skills/sl-trafiklab-api/scripts/cli.py route save <origin> <destination> <alias> [--time <HH:MM>] [--date <YYYY-MM-DD>]`
   - **Specific Route Proposal (with Option Index)**: Saves the exact legs and transfers of a specific travel proposal matching the option index (typically 1, 2, or 3) returned from a prior `route find` query (run with the exact same origin, destination, time, and date parameters to ensure option alignment). Used to monitor transfer connection safety buffers at specific steps.
     - Command: `python3 skills/sl-trafiklab-api/scripts/cli.py route save <origin> <destination> <proposal_index> <alias> [--time <HH:MM>] [--date <YYYY-MM-DD>]`
   - **Manual Legs Array (with JSON)**: Saves a custom leg sequence manually using a JSON array of leg objects. Refer to [api.md](file:///c:/Users/patrk/Documents/antigravity/sl-trafiklab-api/references/api.md#L36-L57) for the required JSON schema format.
     - Command: `python3 skills/sl-trafiklab-api/scripts/cli.py route save <alias> '<legs_json>'`
   - **Route Removal**: `python3 skills/sl-trafiklab-api/scripts/cli.py route remove <alias>`

> [!TIP]
> **Workflow: Saving a Route with Specific Constraints (e.g., specific line or transfer points)**
> To save a route with specific constraints (for example, to restrict a connection to a specific bus/train line or path):
> 1. Run `python3 skills/sl-trafiklab-api/scripts/cli.py route find "<origin>" "<destination>" [--time <HH:MM>] [--date <YYYY-MM-DD>]` to list travel proposals.
> 2. Identify the option index (e.g., Option 1, Option 2) from the search output that meets the constraints.
> 3. Save using the option index, passing the exact same time/date parameters to ensure option alignment: `python3 skills/sl-trafiklab-api/scripts/cli.py route save "<origin>" "<destination>" <option_index> "<alias>" [--time <HH:MM>] [--date <YYYY-MM-DD>]`.
8. **deviations**: Fetch active or planned transit disruptions.
   - Command: `python3 skills/sl-trafiklab-api/scripts/cli.py deviations [--site <site_id>] [--line <line>] [--future]`
