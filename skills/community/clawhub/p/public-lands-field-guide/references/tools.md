# The connector tools: what each reads, and the words to keep

These are the davelalande.com MCP connector's tools (`https://davelalande.com/mcp`). `scripts/aa.py` does not call `trip_check`, `rig_math`, `posted_orders`, `road_to_camp`, `land_at`, `changes_since` or `what_we_cover`. Without the connector, say "not read" for what they hold and name the office.

## trip_check

`trip_check` is a whole-trip dry run on given dates (a truck, a van, or your own `tank_gal` and `water_gal`): the gas and water arithmetic in the game's rig numbers, the National Weather Service forecast for the dates that fall inside its window of about a week (a later date says "no forecast yet", never an average), the fire rules the camp records hold as dated records (not today's posting), and camp records near the forest. Anything missing says "unknown: check with <the named office>". It knows nothing of roads, closures or permits, and it refuses a trip with a night in December, January or February and a date that has passed. Give it `start` and a `forest` or a `camp` record id.

Its "today" is the UTC date, so late in a US evening "today" may already be refused: give tomorrow's date and say so.

## posted_orders

`posted_orders` quotes what a national forest has posted on its own alerts page about fire, food storage or closures, word for word: title, order number, dates as posted, the link and the time we read it, with an office to confirm with. It reads only some forests (`what_we_cover` says which). "Nothing posted when we read it on <date>" is not "no fire ban"; "Could not read since <date>" and "not read" are never "none." Only the alerts page is read: an order posted elsewhere, or after our read, is not there. Give it a `forest`.

## road_to_camp

`road_to_camp` gives the Forest Service Motor Vehicle Use Map record of the road nearest a named camp's pin, set against the rig class you give (`car`, `SUV`, `high-clearance`, `van`, `truck`), with an optional `date`: road number and name, the vehicle classes and dates the record lists, maintenance level, recorded surface and the distance from the road to the pin. It covers camps in 20 national forests. BLM roads and other forests answer "unrecorded" plus the office to ask. The record has no SUV, van or truck class, so those are shown against both classes. It is the record, not today's condition: never say a rig can make it.

## changes_since and what_we_cover

Live since November 11, 2026: `changes_since` (what is new since a date for up to three camps: Weather Service alerts quoted as issued, and a season window that flipped; a failed read is never "nothing new") and `what_we_cover` (the coverage table, with who to ask where we hold nothing).

## land_at

`land_at` ("whose land is this point", live since November 11, 2026) answers for **national forests only**: by the record, the Forest Service unit and ranger district at a point. Anywhere else it says the point is not on national forest land and names no manager; then do not name one yourself, and do not call the ground public or private. Point the person to the office that manages that land.

## plan_four_nights

A trip letter: up to four nights at named camps from the records (free first, then unpriced, said so), with a town run on day 3 from the recorded fuel, water and grocery. Give `forest_slug` or `town`. `start_date` defaults to today.

It plans whatever date it is given, a past one too, and it does not refuse winter. So the dates rule in SKILL.md is yours to keep before you call it: pass a `start_date` that is today or later, with the year you told the person, and never a trip with a night in December, January or February. Then run `trip_check` on the same dates.

## rig_math

Plain arithmetic: how many nights the water lasts for a number of people at a stated use per person per day, and how far a tank of gas goes at a stated mileage. Nothing is read from a record. Its defaults (1 gallon per person per day, 13 miles per gallon) are assumptions the answer labels. Use the person's own numbers when they have them. Never claim a fill-up is enough.

## The game tools

`game_leaderboard`, `one_call` and `trip_status` serve the camping game Dispersed 3D, not the records. Use them only if the person asks about the game.
