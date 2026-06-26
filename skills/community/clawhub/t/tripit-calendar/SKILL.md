---
name: tripit_calendar
description: Read upcoming TripIt travel plans from a TripIt iCal feed; use for next trip, upcoming travel, itinerary, flight or hotel bookings already in TripIt; do not use for live flight status, delays, check-in, or general travel research.
metadata: {"openclaw":{"emoji":"✈️","os":["linux","darwin"],"skillKey":"tripit_calendar","requires":{"anyBins":["python3","python"],"env":["TRIPIT_ICAL_URL"]}}}
---

# TripIt Calendar

Use this skill to retrieve the user's upcoming travel plans from a TripIt iCal feed.

## Routing

Use this skill when the user asks about:
- their next trip
- upcoming trips this week or this month
- flight, hotel, train, or car bookings that are already in TripIt
- travel itinerary details already saved in TripIt
- whether they have any travel coming up

Do not use this skill when the user asks about:
- live flight status, delays, gates, baggage belts, or airport operations
- finding new flights or hotels on the web
- visa rules, weather, or destination advice
- anything that is not based on the user's TripIt itinerary

## What this skill needs

- `TRIPIT_ICAL_URL` must be available
- Python with `requests` and `icalendar` installed

OpenClaw can load environment variables from `~/.openclaw/.env`. This script also falls back to reading `~/.openclaw/.env` directly if `TRIPIT_ICAL_URL` is not already present in the process environment.

Expected entry in `~/.openclaw/.env`:

```bash
TRIPIT_ICAL_URL=https://www.tripit.com/feed/ical/private/.../tripit.ics
```

## Execution

Prefer the OpenClaw virtual environment Python when it exists:

```bash
/home/picoclaw/.openclaw/workspace/openclaw_venv/bin/python {baseDir}/final_tripit_ical.py
```

If that exact path is not available, use:

```bash
python3 {baseDir}/final_tripit_ical.py
```

Use `--pretty` only when a human-readable terminal view is explicitly needed.

## Output

The script returns JSON with:
- `next_trip`: the next detected trip group
- `upcoming_events`: up to 20 future itinerary items
- `counts`: number of upcoming events and detected trips
- `generated_at`: timestamp of the lookup

Each event may include:
- summary
- start and end time
- location
- status
- short description

## How to respond

1. Run the script.
2. Read `next_trip` first.
3. Give the user a concise summary of the next trip.
4. If useful, list the most relevant itinerary items in chronological order.
5. If there are no upcoming events, clearly say there is no upcoming TripIt itinerary.
6. Never invent flight numbers, hotels, dates, or locations that are not in the JSON.

## Examples

User requests that should trigger this skill:
- What is my next trip?
- Do I have any travel coming up?
- Show my upcoming TripIt itinerary.
- Any flights or hotels this month?
- What bookings do I have in TripIt next week?

Example commands:

```bash
/home/picoclaw/.openclaw/workspace/openclaw_venv/bin/python {baseDir}/final_tripit_ical.py
/home/picoclaw/.openclaw/workspace/openclaw_venv/bin/python {baseDir}/final_tripit_ical.py --pretty
python3 {baseDir}/final_tripit_ical.py
```

## Troubleshooting

- If the skill does not appear, confirm `TRIPIT_ICAL_URL` is available to OpenClaw.
- If the agent is running in a sandboxed Docker session, the environment variable must also be passed into the sandbox.
- If Python packages are missing, install them into the same Python environment used for the command.
