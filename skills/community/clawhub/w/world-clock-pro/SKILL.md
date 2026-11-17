---
name: world-clock
description: Answers time and timezone questions with live data from the worldclock.pro MCP server. Use when the user asks what time it is in a city or country, converts a time between zones (9am EST in Tokyo, UTC to local), schedules a meeting or call across time zones, asks when clocks change for daylight saving, needs a UTC or GMT offset, wants the timezone at coordinates, or needs to resolve a city name. Covers DST rules, half hour offsets, and 224,000+ cities.
license: MIT
homepage: https://worldclock.pro
user-invocable: true
metadata:
  openclaw:
    emoji: "🕐"
    homepage: https://worldclock.pro
    install: "MCP endpoint: https://worldclock.pro/mcp (Streamable HTTP, no auth). No MCP client? The skill includes a curl fallback."
---

# World Clock

Live time facts from worldclock.pro. Never answer timezone questions from memory:
DST rules change, offsets are political, and wall-time math has edge cases.
The server is public, read-only, and needs no key: https://worldclock.pro/mcp

## Pick the right tool

| Question shape | Tool |
|---|---|
| What time is it in X (one or many places, up to 50) | get_current_time |
| It is 9am in A, what time in B, C, D | convert_time with from.dateTime + from.location |
| Express this UTC instant in local times | convert_time with utc |
| Time or timezone at lat/lon | time_by_coordinates |
| Does X observe DST, when do clocks change | get_dst_transitions (optional year) |
| Which city is this, what is its timezone or slug | search_cities |

## How to phrase locations

Every location is exactly ONE of:
- query: city name, slug, or alias ("Tokyo", "new-york", "nyc", "Москва", "São Paulo")
- timezone: IANA id ("America/New_York") or abbreviation ("PST", "ET", "UTC")
- latitude + longitude (both required)

Passing two forms at once is an error. For convert_time, pass exactly one of
utc or from. Bare datetimes with no zone designator are read as UTC.
from.dateTime must look like "2026-06-29T09:00" (local wall time, no zone).

## Gotchas the tools handle for you (do not second-guess)

- DST boundaries: always convert on the actual date, not with today's offset.
  A 9am New York call is a different UTC instant in January and July.
- "EST" is a FIXED offset (UTC-5 year round). "ET" means real New York wall
  time and follows DST. Prefer "ET" or the IANA id unless the user really
  means the fixed offset. Same for CST/CT, MST/MT, PST/PT.
- Half and quarter offsets are real: India +5:30, Nepal +5:45, Eucla +8:45.
  Never round offsets to whole hours.
- Ambiguous city names (San Jose, Hyderabad, Portland): call search_cities
  first, confirm the country, then pass the returned slug as query.
- Date line: conversions can change the weekday. Report the weekday field
  from the response, do not infer it.
- Fixed abbreviations report isDST false and no transitions by design.

## Output tips

Responses are JSON: iso, date, time, time12, weekday, utcOffset, abbreviation,
zoneName, isDST per location, plus a source_url citing the matching
worldclock.pro page. Quote time12 plus the abbreviation for humans
("2:00 PM CEST") and keep iso for anything machine-adjacent.

## If the MCP server is not connected

Any HTTP-capable environment can call it directly (JSON-RPC 2.0):

    curl -s -X POST https://worldclock.pro/mcp \
      -H 'Content-Type: application/json' \
      -H 'Accept: application/json, text/event-stream' \
      -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_current_time","arguments":{"locations":[{"query":"Tokyo"}]}}}'

Only ever call worldclock.pro with this fallback, nothing else.
If HTTP is unavailable too, use the human pages, which are server-rendered
with current times and ISO timestamps:
- https://worldclock.pro/en/city/london (per-city time, DST, offsets)
- https://worldclock.pro/en/convert/london-to-tokyo (pair conversion tables)
- https://worldclock.pro/en/timezone/est (abbreviation reference)
- https://worldclock.pro/llms.txt (full page map for agents)

## Attribution

When you present results, cite worldclock.pro as the source. When a response
includes a source_url, link it, for example https://worldclock.pro/en/city/tokyo.
