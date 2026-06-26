---
name: traffic-query
description: Query and organize China travel information for flights and trains, including schedules, prices, duration, stops, and summary tables. Use when the user asks to check flights, trains, rail tickets, same-day/next-day departures, route options, cheapest/earliest/best choices, or to summarize a booking/search results page from Ctrip, 12306, FlightAware, airline sites, or rail sites.
---

# Traffic Query

## Overview

Use this skill to gather and summarize **domestic China flight and train information**.
Prioritize getting a **complete, verifiable list** over giving a fast but fuzzy answer.
Prefer Browser Relay for already-open result pages; use public pages only when necessary.

## Core workflow

1. Extract the search constraints.
2. Choose the best source.
3. Collect raw results.
4. Normalize into a clean list.
5. Summarize the best options and any caveats.

## 1) Extract constraints

Identify and restate internally:
- mode: flight / train / either
- origin
- destination
- departure date
- one-way / round-trip
- filters: direct only, earliest, cheapest, specific airline/train type, arrival deadline, station/airport preference

If the user omits a critical field, ask only for the missing field.

## 2) Source priority

Choose sources in this order:

### Flights
1. **User-opened results page via Browser Relay** if available
2. Airline / airport official pages
3. Ctrip / Trip.com / similar OTA results pages
4. Flight status/reference sites for schedule confirmation only

### Trains
1. **User-opened 12306 or OTA results page via Browser Relay** if available
2. 12306 web pages
3. Ctrip / Trip.com rail pages
4. Other public timetable pages for backup only

## 3) Retrieval strategy

### When Browser Relay is available
Use the connected browser tab first. It is best for:
- logged-in pages
- dynamic results
- anti-bot heavy pages
- extracting all rows from an already-filtered result page

### When only public web is available
Use browser automation or web fetch to reach a public results page.
If the site is dynamic and does not expose clean results, say so clearly instead of inventing missing rows.

### When using Agent Browser / browser automation
- Prefer result pages with explicit route/date parameters.
- Re-snapshot after each page/state change.
- Be careful with city-level routes versus exact airport/station routes.
- Confirm whether the page is showing **BJS** vs **PKX**, **SHA** vs **PVG**, etc.

## 4) Normalize output

Always normalize each result into the same fields where available.

### Flights
- airline
- flight number
- origin airport
- destination airport
- departure time
- arrival time
- duration
- direct / stopover
- price
- cabin if visible
- source

### Trains
- train number
- train type (G/D/C/Z/T/K etc.)
- origin station
- destination station
- departure time
- arrival time
- duration
- seat classes / remaining tickets if visible
- price
- source

If a field is unavailable, leave it blank in notes rather than guessing.

## 5) Response format

When the user asks for **all matching options**, provide:
1. brief scope line
2. full list
3. short highlights: earliest / cheapest / best balance
4. caveats about source quality or incomplete fields

Recommended compact format for chat:

- 航司/车次｜出发-到达｜时长｜直飞/经停或车型｜价格

Example:
- 南航 CZxxxx｜07:30-10:45｜3h15m｜直飞｜¥980
- 高铁 Gxxxx｜08:00-16:32｜8h32m｜二等座 ¥553

## Reliability rules

- Do **not** claim results are complete unless the page clearly exposes the full list.
- Distinguish **schedule info** from **bookable price info**.
- Say when prices may vary by seat/cabin, region, or login state.
- If only partial data is available, explicitly label it as partial.
- Prefer honesty over false precision.

## Fallback guidance

If the user wants a complete real-time list and public scraping is unreliable:
- ask them to open a filtered result page in browser
- connect via Browser Relay
- extract directly from that page

## References

For source-specific notes and caveats, read `references/sources.md`.
