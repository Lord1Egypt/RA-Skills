---
name: public-lands-field-guide
description: Plans camping and overlanding trips on US national forest and BLM land, the careful way, using the free American Adventurer records (about 19,000 sourced camps, no sign-in). Use when someone asks where to camp, how to plan a trip, free or dispersed camping, a town run, water, season, weather, wildfire reports, a gas-and-water trip check or a backup camp on US public land. Shows each record's link, source and date, names what is unrecorded, and never says a place is open, legal, passable or safe.
license: Free to use and copy unchanged, with the credit line "Camp records: American Adventurer (davelalande.com)" and a link to the record.
compatibility: Needs internet access to https://davelalande.com. The scripts need Python 3.8 or newer and nothing else. Works with the davelalande.com MCP connector when present.
metadata:
  author: Dave Lalande (American Adventurer)
  version: "1.1"
  home: https://davelalande.com/skill/
---

# Public Lands Field Guide

Plan a trip on US national forest or BLM land the way a careful ranger would. Records first. Gaps named. The office has the last word.

## Pick your tools, in this order

1. **The davelalande.com MCP connector**, if it is in your tool list. Address: `https://davelalande.com/mcp`. 14 tools are live. Camp tools: `find_camps`, `camp_detail`, `camps_near`, `free_camping_near_town`, `plan_four_nights`, `trip_check`, `forest_weather`, `changes_since`, `what_we_cover`, `land_at`, `rig_math`.
   Three more serve the camping game Dispersed 3D, not the records: `game_leaderboard`, `one_call`, `trip_status`. Use them only if the person asks about the game.
2. **`scripts/aa.py`**, if you can run Python. Standard library only, read-only. Run `python scripts/aa.py --help`.
3. **Plain web fetches** of `https://davelalande.com/api/` (see its `how_to_use` text) or the record pages.

`trip_check` is a whole-trip dry run on given dates (a truck, a van, or your own `tank_gal` and `water_gal`): the gas and water arithmetic in the game's rig numbers, the National Weather Service forecast for the dates that fall inside its window of about a week (a later date says "no forecast yet", never an average), the fire rules the camp records hold as dated records (not today's posting), and camp records near the forest. Anything missing says "unknown: check with <the named office>". It knows nothing of roads, closures or permits, and it refuses a trip with a night in December, January or February and a date that has passed. Give it `start` and a `forest` or a `camp` record id.

Live since November 11, 2026: `changes_since` (what is new since a date for up to three camps: Weather Service alerts quoted as issued, and a season window that flipped; a failed read is never "nothing new") and `what_we_cover` (the coverage table, with who to ask where we hold nothing).

`land_at` ("whose land is this point", live since November 11, 2026) answers for **national forests only**: by the record, the Forest Service unit and ranger district at a point. Anywhere else it says the point is not on national forest land and names no manager; then do not name one yourself, and do not call the ground public or private. Point the person to the office that manages that land.

## The order of work

Full steps are in [references/order-of-work.md](references/order-of-work.md). In short:

1. **Land.** Who manages it? Use the record's land manager and forest.
2. **Rules.** Lead with any recorded closure, season or stay limit.
3. **Season.** Spring, summer and fall only. Never plan snow or winter.
4. **Road.** Not in the records. Name the office.
5. **Water.** What the record holds, nothing more.
6. **Town run.** Fuel, groceries, water, dump from the record, in straight-line miles.
7. **Fire and weather.** NWS forecast and wildfire reports, quoted and dated.
8. **Rig math.** Plain arithmetic with stated assumptions (`rig_math`, or `trip_check` for a whole trip).
9. **Backup camp.** Always one more camp, in case the first is full or closed.
10. **Last check.** Re-read the records, then tell the person to call the office.

## The manners

Details in [references/honesty.md](references/honesty.md).

- **Show every record's link, source and record date.** No link, no claim.
- **Say what is unrecorded. Never estimate it.** A missing field means unrecorded, not "none."
- **Distances are straight-line miles.** Roads run longer.
- **Never say a place is open, legal, passable or safe.** Say what the record says. Name the office to confirm with. Signs on the ground and the office win.
- **Free camps first**, then unpriced (say so). Do not showcase paid group sites. Small, free, rustic sites for one or two rigs are the heart of it.
- **Leave No Trace.** Pack it out. Keep to the stay limit as recorded.
- **Send no personal data to the API.** It needs none.

## Credit

End any answer that uses a record with: **Camp records: American Adventurer (davelalande.com)** and the record link. Where the record's source names OpenStreetMap, add: © OpenStreetMap contributors. See [references/sources.md](references/sources.md).

## What it covers

See [references/coverage.md](references/coverage.md) and fetch the live table at `https://davelalande.com/coverage.json` before you describe our limits.

## Check your copy

Run `python checks/run_checks.py` to test the data path (the API and `scripts/aa.py`, not the MCP tools) against 20 questions. Compare `CHECKSUMS.txt` with the copy at `https://davelalande.com/skill/`.
