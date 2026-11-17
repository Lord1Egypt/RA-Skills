# The order of work

Do the steps in this order. Each step says what to fetch, what to say, and what to hand off. Every claim carries the record's link, source and date (see honesty.md).

Commands below use `scripts/aa.py`. With the MCP connector, the matching tool is named in brackets.

## 1. Land: whose ground is this?

- Start from a camp record: `aa.py find "<place>" --state XX` [`find_camps`], or a town: `aa.py town "<town>" --state XX` [`free_camping_near_town`].
- Read `land_manager` (USFS, BLM, a state or county agency) and `forest` (name and link).
- For a point that is not a camp record, call `land_at`. It answers inside national forests only. If it says the point is not on national forest land, say so, name no manager, and name an office only if a record names it.
- National parks are outside the records by design. State and other named lands are in `aa.py land "<name>"`.

## 2. Rules: lead with them

- Read `rules` on the camp (`aa.py camp SLUG`) [`camp_detail`]. Keys that may appear: `stay_limit_days`, `stay_limit_text`, `stay_limit_status`, `open_season`, `fee_note`, `max_vehicle_length_ft`.
- A closure, season or stay limit decides whether the trip happens, so say it first.
- No `rules` object means unrecorded. It never means "no limit" and never means "open."
- `stay_limit_status: "None published"` means the source page published no number. Quote that. It is still not permission to stay longer.
- Permit prices are not in the records, and neither are today's fire orders. Camp records may hold fire rules as a dated snapshot (`trip_check` quotes them as dated records, not today's posting). Name the office.

## 3. Season: spring, summer and fall only

- We plan trips for spring, summer and fall. Never plan snow or winter. If the dates fall in winter, say "this guide plans spring, summer and fall trips" and offer a later date.
- `aa.py camp SLUG --date YYYY-MM-DD` returns `season.state` (open, closed, or check) with `why`, for that date. The `check` state means the agency text did not parse to a date. Say that.
- No `season` block means the season is unrecorded. Say so. Do not assume a road or camp is open.
- `aa.py find "" --open YYYY-MM-DD` lists camps whose season window reads open that day. A camp that is not listed is "no record," not "closed."

## 4. Road: the record does not hold it

- Road conditions, passability and road class are not in the records. Do not say a rig "can make it."
- Say what is recorded: `camp_type` (for example drive), whether the land record classes it 4x4 (`aa.py find ... ` with `access` filter on the API), `terrain.slope_pct` (the hillside, not the pad: never call a site level).
- Name the office (the land manager) for current road status. Tell the person to look at signs and gates.

## 5. Water

- `water` on the camp holds the source's own words, or null. Null means "no water recorded here." That is a correct answer.
- `surface_water` names the nearest named stream and its distance. It is a map feature, not a drinking source and not a flow reading.
- Treat all natural water as needing treatment. Say that plainly. Do not rate it safe.
- Stream gauges exist for very few camps. If none is paired, say so.

## 6. Town run

- `services_mi` lists the nearest fuel, groceries, water, dump, propane, pharmacy, hospital and hardware with names and straight-line miles. Null entries are unrecorded.
- `town_name` and `town_mi` give the nearest town. Say straight-line, and that the drive is longer.
- More points: `aa.py poi LAT LON fuel --radius 25`. Those come from OpenStreetMap: floor, never a survey, and they need the OpenStreetMap credit.

## 7. Fire and weather

- Weather: `aa.py weather LAT LON` [`forest_weather`]. This is the National Weather Service forecast, quoted as written, with its read time. If the forecast shows snow, say "this forecast is outside the seasons we plan for."
- Wildfire reports: `aa.py fire LAT LON`. These are reports of incidents and planned burns within about 100 miles. They are not perimeters, closures or restrictions. A failed read means "could not read," never "none nearby."
- Current fire restrictions are not in the records. A camp's recorded fire rules are a dated snapshot, not today's posting. Name the forest or field office.

## 8. Rig math

- For a whole trip on given dates, call `trip_check` (connector only): gas and water in the game's rig numbers or your own tank, the forecast inside its window, dated camp fire-rule records and camps near. Give `start` and a `forest` or `camp`; add `pump_paved_mi` and `pump_unpaved_mi` (one way, read off a map) for the gas. A date past the forecast says "no forecast yet". It refuses winter nights and past dates. It never says a road or camp can be used.
- Use `rig_math` if the connector is present. Otherwise do the arithmetic yourself and print your assumptions.
- Water: gallons divided by (people times gallons per person per day). State the rate you used. The site's own default is 1 gallon per person per day, an assumption, not a rule.
- Gas: gallons times miles per gallon. State the mpg you used. Count the drive out and back. Straight-line miles understate the road.
- Never claim a fill-up is enough. Say what the arithmetic gives and what it assumed.

## 9. Backup camp

- Every plan has a second camp. `aa.py near LAT LON --cost free --radius 25` gives the nearest camps (the script filters free ones itself).
- Pick one that is small, free and rustic, 5 to 25 straight-line miles away, with its own record link.
- Never use a paid group site as the showcase. If a camp is a paid site, say it is paid.

## 10. Last check

Before you finish:

1. Does every camp have its link, source and record date?
2. Is every unrecorded thing named as unrecorded?
3. Is each distance labeled straight-line?
4. Did you avoid "open," "legal," "passable" and "safe"?
5. Did you name the office to confirm with (the camp's land manager)?
6. Did you add the credit line?
7. On the morning of the trip, run `changes_since` for the camps (MCP) to see what is new since the plan, then tell the person to re-check the forecast and call the office. "Nothing new in what we watch" is not the same as nothing changed. `changes_since` does not read fire orders or closure orders.
