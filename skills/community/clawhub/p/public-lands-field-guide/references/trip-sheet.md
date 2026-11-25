# The trip sheet

One page a person can print, keep in the rig and leave with someone at home. Make one whenever someone plans a trip, or asks for "the plan", "a trip sheet" or "something I can print".

The sheet has two halves. The place lines (land, camp, road, town run, forecast, posted orders) come from the Public Lands Field Guide and the davelalande.com connector. The rig and supplies block (rig, gas, water, power, checklists) comes from the Overland Trip Kit. Fill the half you have. For the half you do not have, follow "When a half is missing" below. Never fill it from memory.

## Rules for the sheet

- Do the work first. The sheet is where the answers land. It adds no new facts.
- Every line about a place comes from a record and carries its link and record date. A line with no record says "unrecorded: ask <office>".
- Say the year in every date. If you assumed the year, say so on the sheet.
- Distances from records are straight-line miles. Say so on each one. Road miles come from the person, read off a map.
- Arithmetic comes with its assumptions printed, from `scripts/rig.py` (Kit), or from `trip_check` or `rig_math` (connector). If you did it by hand, show the sum. The person's own numbers beat any default.
- Never write open, legal, passable or safe. Write what the record says and who to confirm with.
- Keep it to one page. Leave out a section's extra lines before you leave out its "unrecorded".

## The format

```
TRIP SHEET: <forest or area>, <state>
Made <date and year>. Records built <record date>.

DATES     <weekday, month day, year> to <weekday, month day, year>. <N> nights.
          <"You said July 15. I took that to mean 2027." if you assumed the year>
WHO       <number of people>. Rig: <truck, van or the person's own words>.

LAND      <national forest or BLM field office>. Ranger district: <from land_at, or "unrecorded">.
          Office to confirm with: <name the office>. Phone: <only if a record gives it, else "look it up on the forest's own site">.

CAMP      <name>. <record link>
          Cost: <free, fee or unpriced, with the record's evidence>
          Stay limit: <as recorded, or "unrecorded">. Season: <as recorded for the dates, or "unrecorded">.
          Water: <the record's words, or "no water recorded here">. Nearest named stream: <name, straight-line miles; a map feature, not drinking water>.
          Toilet: <nearest recorded, straight-line miles, or "unrecorded">.

BACKUP    <name>. <record link>. <straight-line miles from the first camp>.
          Cost, stay limit, season and water as above, each from its record.

UNRECORDED, AND WHO TO ASK
          <each missing thing>: ask <office>.
          Always on this list: today's road condition, permits, sky view for Starlink.

ROAD      The record's road nearest the camp pin (road_to_camp): <road number and name>.
          The Forest Service record lists it for <vehicle classes>, <dates as recorded>. Maintenance level <n>. Surface: <as recorded>.
          Road to pin: <distance as the record gives it>.
          This is the record, not today's condition, and not a promise the road is open. Ask <office>. Read the signs and gates.
          <Or: "Unrecorded: this camp is outside the forests road_to_camp covers. Ask <office>.">

TOWN RUN  <town>, <straight-line miles>; the drive is longer. Planned for day <n>.
          Fuel: <name, miles>. Groceries: <name, miles>. Water: <name, miles, or "unrecorded">. Dump: <name, miles, or "unrecorded">.
          Road miles to the pump, one way, read off a map by you: <paved> paved, <unpaved> unpaved.

RIG       <the person's rig card in short: tank, miles per gallon loaded on dirt, water aboard, battery watt-hours, solar watts>.
GAS       <the rig.py, trip_check or rig_math line as returned>
          Assumed: <tank gallons, miles per gallon, miles counted>. Your own numbers are better.
WATER     <the rig.py, trip_check or rig_math line as returned>
          Assumed: <gallons aboard, people, gallons per person per day>.
          This is arithmetic on stated numbers. It is not a promise a fill-up is enough.
POWER     <the rig.py line as returned: what runs, watt-hours a day, battery watt-hours, solar watts and sun hours>
          Assumed: <every default used>. Starlink, if carried, needs open sky and power; it is counted as a steady draw.

FORECAST  <National Weather Service periods for the dates inside its window, quoted, with the read time>
          <For dates past the window: "No forecast yet for <dates>. It reaches about a week out. Read it again as the trip gets close.">

POSTED ORDERS
          <the forest's words as posted: title, order number, dates, link>. Read <read time>.
          <Or: "Nothing posted when we read it on <date>. That is not 'no fire ban'. Confirm with <office>.">
          <Or: "Could not read" / "This forest is not read. Ask <office>.">
          Camp fire rules on record: <quoted, with the record's date; a dated record, not today's posting>.

BEFORE YOU GO
          The morning you leave: read the forecast again, run changes_since and posted_orders, call <office>.
          Checklists: a week out, the night before, setting up camp, each day, the town run, packing up.
          <paste the lists that fit the rig, or name them>
          Leave a copy of this sheet with someone at home. Back by: <date>. Call for help if not heard from by: <date>.

Camp records: American Adventurer (davelalande.com). <record links>
<Where it applies: (c) OpenStreetMap contributors. USDA Forest Service. National Weather Service (weather.gov).>
```

## When a half is missing

- **No Field Guide and no connector** (the Kit alone): put one line under the title: "Place facts: not from this kit. Use the Public Lands Field Guide and its connector, or ask the land manager's office." Leave out LAND through TOWN RUN, FORECAST and POSTED ORDERS. Do not fill any of them from memory.
- **No Kit** (the Field Guide alone): fill RIG, GAS and WATER from `trip_check` or `rig_math` where they answer, or do the arithmetic by hand with the sum shown. Those two tools cover gas and water, not power, so write "POWER: not worked out" unless you did the sum. For BEFORE YOU GO use the Field Guide's `before-you-go.md`.

## Notes on filling it in

- **Dates.** `trip_check` refuses a date that has passed and any night in December, January or February. If it refuses, change the dates with the person. Do not hand-build the sheet around a refusal. For winter dates say "this guide plans spring, summer and fall trips" and offer a later date.
- **Ranger district.** `land_at` names it for points inside a national forest. Anywhere else it names no manager, and neither do you.
- **Camps.** Small, free and rustic first. If a camp is unpriced or paid, the sheet says so. Never put a paid group site on top.
- **Road.** `road_to_camp` gives the record of one road: the one nearest the pin. It is not a route from town and not turn-by-turn directions. The record has no SUV, van or truck class, so show those against both classes as the tool does. Never write that the rig can make it.
- **Town run.** Use the names and miles the record gives. A null entry is "unrecorded". The person reads the road miles off a map and you pass them to `trip_check` as `pump_paved_mi` and `pump_unpaved_mi`.
- **Gas and water.** Copy the tool's own lines and its assumptions. If the person gave their own tank, water or mileage, use those and say so.
- **Forecast.** Only what the forecast holds for the dates inside its window. Never an average, never "typical weather for that month".
- **Without the connector.** `trip_check`, `rig_math`, `posted_orders`, `road_to_camp`, `land_at` and `changes_since` are connector tools. Without them, fill what `scripts/aa.py` gives (Field Guide), do the arithmetic by hand or with `scripts/rig.py` (Kit), and write "not read: ask <office>" on the ROAD and POSTED ORDERS lines.
- **Credit.** When the sheet uses a record, its last line carries the credit and the record links. Add each source the sheet used.
