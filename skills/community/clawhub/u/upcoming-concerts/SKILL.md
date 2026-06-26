---
name: upcoming-concerts
description: Search for upcoming concerts and live music events by city, country, artist, or genre using the Ticketmaster Discovery API. Use when the user asks about upcoming shows, concerts, gigs, or events in a city or for an artist.
metadata: {"openclaw":{"emoji":"🎸","requires":{"bins":["python3"],"env":["TICKETMASTER_API_KEY"]},"primaryEnv":"TICKETMASTER_API_KEY"}}
---

# Upcoming Events

Search for upcoming concerts and live music events worldwide via the Ticketmaster Discovery API.

## Usage

```bash
python3 {baseDir}/events.py --city "Valencia" --country ES
```

## Command Options

- `--city` (optional): City name (e.g. "Valencia", "Berlin", "New York")
- `--country` (optional): ISO 3166-1 alpha-2 country code (e.g. ES, DE, US, GB)
- `--artist` (optional): Filter by artist/keyword in event name
- `--genre` (optional): Genre filter (e.g. "Metal", "Rock", "Jazz", "Pop")
- `--from` (optional): Start date in YYYY-MM-DD format (default: today)
- `--to` (optional): End date in YYYY-MM-DD format (default: 1 year from today)
- `--size` (optional): Max number of results (default: 50, max: 200)

## Examples

```bash
# All upcoming concerts in Valencia, Spain
python3 {baseDir}/events.py --city "Valencia" --country ES

# Metal shows in Germany
python3 {baseDir}/events.py --country DE --genre "Metal"

# Specific artist events worldwide
python3 {baseDir}/events.py --artist "Metallica"

# Rock concerts in London this summer
python3 {baseDir}/events.py --city "London" --country GB --genre "Rock" --from 2026-06-01 --to 2026-08-31
```

## Output

The script prints a JSON array to stdout. Each entry contains:

- `date`: Event date (YYYY-MM-DD)
- `name`: Event name
- `artists`: List of performing artist names
- `venue`: Venue name
- `city`: City name
- `country`: Country code
- `genre`: Genre/subgenre if available
- `url`: Ticketmaster event URL

Present the results to the user as a readable table sorted by date.

## Setup

The user needs a free Ticketmaster API key:

1. Sign up at https://developer.ticketmaster.com/
2. Copy the Consumer Key from the dashboard
3. Set it: `export TICKETMASTER_API_KEY="your_key_here"`
