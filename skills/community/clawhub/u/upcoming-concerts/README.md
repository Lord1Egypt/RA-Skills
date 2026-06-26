# upcoming-events

OpenClaw skill to search for upcoming concerts and live music events worldwide using the Ticketmaster Discovery API.

## Setup

1. Get a free API key at https://developer.ticketmaster.com/
2. Set the environment variable:
   ```bash
   export TICKETMASTER_API_KEY="your_key_here"
   ```

## Install

Copy this directory into `~/.openclaw/skills/upcoming-events/` or your workspace `skills/` folder.

## Standalone usage

```bash
python3 events.py --city "Valencia" --country ES
python3 events.py --country DE --genre "Metal"
python3 events.py --artist "Metallica"
```
