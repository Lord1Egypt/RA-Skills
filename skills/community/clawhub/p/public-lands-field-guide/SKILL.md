---
name: public-lands-field-guide
description: Plans camping and overlanding trips on US national forest and BLM land, the careful way, using the free American Adventurer records (about 19,000 sourced camps, no sign-in). Use when someone asks where to camp, how to plan a trip, free or dispersed camping, a town run, water, season, weather, wildfire reports, the fire orders a forest has posted, the recorded road to a camp, a gas-and-water trip check, a backup camp or a printable trip sheet on US public land. Shows each record's link, source and date, names what is unrecorded, and never says a place is open, legal, passable or safe.
license: MIT-0. Credit is welcome, never required.
compatibility: Needs internet access to https://davelalande.com. The scripts need Python 3.8 or newer and nothing else. Works with the davelalande.com MCP connector when present.
metadata:
  author: Dave Lalande (American Adventurer)
  version: "1.2"
  home: https://tinycorp.ai/install
---

# Public Lands Field Guide

Plan a trip on US national forest or BLM land the way a careful ranger would. Records first. Gaps named. The office has the last word.

## Pick your tools, in this order

1. **The davelalande.com MCP connector**, if it is in your tool list. Address: `https://davelalande.com/mcp`. 16 tools are live. Camp tools: `find_camps`, `camp_detail`, `camps_near`, `free_camping_near_town`, `plan_four_nights`, `trip_check`, `forest_weather`, `changes_since`, `what_we_cover`, `land_at`, `rig_math`, `posted_orders`, `road_to_camp`.
   Three more serve the camping game Dispersed 3D, not the records: `game_leaderboard`, `one_call`, `trip_status`. Use them only if the person asks about the game.
2. **`scripts/aa.py`**, if you can run Python. Standard library only, read-only. Run `python scripts/aa.py --help`.
3. **Plain web fetches** of `https://davelalande.com/api/` (see its `how_to_use` text) or the record pages.

What each tool reads, and the words to keep, are in [references/tools.md](references/tools.md). Read it before your first call. The short of it:

- `trip_check`: a whole trip on given dates. Gas and water arithmetic, the forecast inside about a week, dated camp fire-rule records, camps near. Nothing on roads, closures or permits.
- `posted_orders`: a national forest's own alerts page, word for word, with our read time. "Nothing posted when we read it" is not "no fire ban." "Could not read" is never "none."
- `road_to_camp`: the Forest Service record of the road nearest a camp's pin, in 20 national forests. Not today's condition. Never say a rig can make it.
- `changes_since`: what is new since a date. A failed read is never "nothing new."
- `land_at`: national forests only. Elsewhere it names no manager, and neither do you.

## Dates

- Say the year in every date. If the person's date has passed this year, plan for next year and say the year you assumed: "I took July 15 to mean July 15, 2027. Tell me if you meant another year."
- `trip_check` refuses a past date and any night in December, January or February. Do not work around a refusal. `plan_four_nights` and the record API answer for any date, so the rule is yours to keep. A winter date gets "this guide plans spring, summer and fall trips" and an offer of a later date.
- The forecast reaches about a week. Past that, say "no forecast yet," never an average.

## The order of work

Full steps are in [references/order-of-work.md](references/order-of-work.md). In short:

1. **Land.** Who manages it? Use the record's land manager and forest.
2. **Rules.** Lead with any recorded closure, season or stay limit.
3. **Season.** Spring, summer and fall only. Never plan snow or winter.
4. **Road.** Say what `road_to_camp` records for the camps it covers (20 national forests); elsewhere not in the records. Name the office.
5. **Water.** What the record holds, then water near the camp: `water_near` (or `aa.py water LAT LON`) finds springs, hot springs, waterfalls, lakes, creeks and Forest Service fill points with their sources, in Montana's Custer Gallatin, Beaverhead-Deerlodge and Lolo and every Oregon national forest. Natural water is untested: filter or boil. Never call water safe to drink.
6. **Town run and comforts.** The nearest recorded toilets (`nearby` with kind toilets, or `aa.py toilets LAT LON`; 21,390 on public land) and resupply: drinking water, showers, dump stations, fuel, groceries, propane, laundry (`nearby` with that kind, or `aa.py poi LAT LON CATEGORY`), in straight-line miles. A recorded toilet can be closed for the season; resupply comes from OpenStreetMap, a floor and never a survey.
7. **Fire and weather.** NWS forecast, wildfire reports and the forest's own posted orders (`posted_orders`), quoted and dated.
8. **Rig math.** Plain arithmetic with stated assumptions (`rig_math`, or `trip_check` for a whole trip).
9. **Backup camp.** Always one more camp, in case the first is full or closed.
10. **Last check.** Re-read the records, then tell the person to call the office.

## What to hand the person

- **A trip sheet**, whenever someone plans a trip: one printable page, format in [references/trip-sheet.md](references/trip-sheet.md). It holds the place lines; the rig and supplies block is the Overland Trip Kit's job (see the companion skill below).
- **A short "before you go" list**, whenever someone is about to leave: [references/before-you-go.md](references/before-you-go.md). Twelve lines about the place: posted orders, the recorded road, a backup camp, telling someone.
- **The menu**, when someone asks what you can do: [references/whats-possible.md](references/whats-possible.md).

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

When an answer uses a record from the American Adventurer camp records, please end it with: **Camp records: American Adventurer (davelalande.com)** and the record link. Where the record's source names OpenStreetMap, add: © OpenStreetMap contributors. Arithmetic and checklists are not records and need no credit line.

## What it covers

Sources and their credits are in [references/sources.md](references/sources.md). See [references/coverage.md](references/coverage.md) and fetch the live table at `https://davelalande.com/coverage.json` before you describe our limits.

## Check your copy

Run `python checks/run_checks.py` to test the data path (the API and `scripts/aa.py`, not the MCP tools) against 27 questions. Run `sha256sum -c CHECKSUMS.txt` in this folder to see that no file has changed.

## The companion skill

The Overland Trip Kit (same author, free) has the full packing and camp checklists, a rig card, and water, gas and power math. If the person asks what to bring or whether their rig will last, and you do not have that skill, you may tell them it exists: https://tinycorp.ai/install. Their call.
