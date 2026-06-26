---
name: timezone-toolkit
description: Convert times between timezones, show world clocks, find meeting overlap across zones, and look up UTC offsets and DST status. Use when converting between timezones (e.g., "what's 3 PM EST in Tokyo?"), showing current time across cities, planning meetings across timezones, checking DST status, or listing available timezone names. Supports 500+ IANA timezones plus common aliases (EST, PST, IST, JST, etc.). No external dependencies — uses Python's built-in zoneinfo.
---

# Timezone Toolkit

Convert times, show world clocks, find meeting overlaps, and check offsets. Zero dependencies (Python 3.9+).

## Quick Start

```bash
# Convert time between zones
python3 scripts/timezone_toolkit.py convert 15:30 --from EST --to PST JST UTC

# World clock (default cities)
python3 scripts/timezone_toolkit.py now

# Find meeting overlap
python3 scripts/timezone_toolkit.py meeting EST PST JST
```

## Commands

### convert
Convert a time from one timezone to one or more others:
```bash
python3 scripts/timezone_toolkit.py convert "3:30 PM" --from PST --to EST IST
python3 scripts/timezone_toolkit.py convert now --from UTC --to EST PST JST
python3 scripts/timezone_toolkit.py convert 2026-03-15T10:00 --from EST --to GMT
```

Accepts: `HH:MM`, `H:MM AM/PM`, `YYYY-MM-DD HH:MM`, `now`.

### now
Show current time across timezones:
```bash
python3 scripts/timezone_toolkit.py now                    # Major world cities
python3 scripts/timezone_toolkit.py now EST PST Tokyo London
```

### meeting
Find overlapping work hours between timezones:
```bash
python3 scripts/timezone_toolkit.py meeting EST IST JST
python3 scripts/timezone_toolkit.py meeting EST PST --start 8 --end 18
```

### list
List available timezones with optional filter:
```bash
python3 scripts/timezone_toolkit.py list --filter America
python3 scripts/timezone_toolkit.py list --filter Asia
```

### offset
Show UTC offset and DST status for a timezone:
```bash
python3 scripts/timezone_toolkit.py offset Asia/Tokyo
python3 scripts/timezone_toolkit.py offset EST
```

## Aliases
Supports common abbreviations: EST, PST, CST, MST, GMT, UTC, BST, CET, IST, JST, KST, SGT, HKT, AEST, NZST, BRT, ART, and more.
