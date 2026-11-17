---
name: sixflags
description: "Plan a day at a Six Flags theme park with live ride wait times, park hours, show schedules, and next-ride suggestions. Use when the user asks about Carowinds or any Six Flags / Cedar Fair park (Cedar Point, Canada's Wonderland, Magic Mountain, the Hurricane Harbor water parks, etc.) — current waits, what to ride next, what time the park opens/closes, or what shows are on. Backed by the sixflags-mcp server over the public themeparks.wiki API (no login)."
---

# Six Flags trip planning

Live wait times, park hours, shows, and day-planning for the combined Six Flags / Cedar Fair chain. Every tool defaults to the user's **home park** (Carowinds unless `SIXFLAGS_HOME_PARK` is set), so most calls need no `park` argument. Data comes from the public themeparks.wiki API — no account or key.

## Tools

- **`sixflags_get_wait_times`** — every ride's current standby + single-rider wait and status (operating / closed / down), sorted longest-first, plus a crowd summary (open count, average/longest/shortest wait). Start here.
- **`sixflags_suggest_next`** — the "what should we ride next?" tool. Ranks currently-open rides by shortest standby wait. Pass `exclude` (rides already ridden), `maxWaitMinutes`, and `limit`. Re-run through the day, adding each finished ride to `exclude`, to keep hopping to the lowest wait.
- **`sixflags_get_park_schedule`** — operating hours from today forward (`days` to widen the window). Use it to decide when to arrive and how long you've got.
- **`sixflags_get_shows`** — today's live show schedule (parades, stunt shows, character meets) with showtimes.
- **`sixflags_list_attractions`** — the full directory of a park's rides (or `type: SHOW`/`RESTAURANT`) with map coordinates. Static metadata; use `get_wait_times` for live status.
- **`sixflags_list_parks`** — every Six Flags park with its id; `search` to filter. Use when the user names a park other than home, or to look up an id.
- **`sixflags_healthcheck`** — confirm the upstream is reachable.

## The `park` argument

Optional on every data tool; omit it for the home park. When present it accepts a park **name** ("Cedar Point"), a **slug** ("sixflags_destination_CP"), a unique **name substring** ("magic"), or a park **id**. An ambiguous substring or an unknown park returns an error listing how to disambiguate (run `sixflags_list_parks`).

## Planning a day — the loop

1. `sixflags_get_park_schedule` → know the operating window.
2. `sixflags_get_wait_times` → read the crowd; note the marquee coasters and their waits.
3. `sixflags_suggest_next` → pick the next ride. After riding it, call again with that ride added to `exclude`. Repeat.
4. `sixflags_get_shows` → slot shows into the gaps between rides.

## In context groups

This server joins the **travel** group (mcp-host context groups; the tools carry `_meta.mint` hints).

- **Canonical read:** `sixflags_get_park_schedule` answers the group's *what's on* ask — the home park's operating days and hours, with `view: "brief"` giving one line per day (`Carowinds — 2026-07-18 — open 10:00–22:00`) inside the untrusted-data envelope's `data` (park names and descriptions are the operator's text), or the single note line `-- none` when nothing is scheduled. It takes no subject: the chain's parks are a public directory, not the person's own, so the group reads the configured home park. `sixflags_get_shows` is a non-canonical *what's on* (today's showtimes); everything else is a lookup.
- **No what's-new or what's-due:** nothing here is news or a deadline.
- **A compound ask** looks like "is the park open this weekend, and anything else on our trip?" — the group answers the park's days and hours alongside the other travel sources.
- **No browser needed:** the upstream is a public keyless API, so this source never answers "needs your browser open".

## Notes

- Waits and show times only populate during operating hours — off-hours every ride reads CLOSED with no wait. Check `parkOpen` in the wait-times/suggest responses and the schedule before assuming the park is dark.
- "Six Flags" here means the post-merger chain: it includes the former Cedar Fair parks (Carowinds, Cedar Point, Kings Island, Canada's Wonderland, …) alongside the historically Six-Flags-branded parks.
