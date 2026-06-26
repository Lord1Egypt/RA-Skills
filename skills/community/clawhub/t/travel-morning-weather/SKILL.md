---
name: Travel Morning Weather
version: 1.0.0
description: Adjust morning weather briefing location based on travel plans captured from conversation.
metadata:
  openclaw:
    requires:
      bins: [python3, curl]
    emoji: "\U0001F30D"
    homepage: https://github.com/Suidge/travel-morning-weather
    os: [darwin, linux]
---

# 🌍 Travel Morning Weather

## Setup

On first activation, check if `memory/travel-plan.json` exists.
If **not found** → ask the user for their home city, then create it:

```json
{ "default_location": "<User's City>, <Country>", "daily_locations": {} }
```

If **found** → confirm `default_location` with the user before first use.

## When to Use

- Morning Briefing cron runs at 07:00 Asia/Shanghai
- User mentions travel plans in conversation (dates + location)

## Core Rules

### 1. Morning Weather Location Resolution

Read `memory/travel-plan.json`. Use today's date (Asia/Shanghai) to look up `daily_locations`:
- **Match found** → use that city for weather query
- **No match** → use `default_location`

### 2. Capture Travel Plans from Conversation

When user mentions travel (dates + location), update `travel-plan.json` proactively:

```bash
python3 skills/travel-morning-weather/scripts/update-travel-plan.py \
  --start YYYY-MM-DD --end YYYY-MM-DD --location "City, Country"
```

For detailed trigger conditions, see `references/capture-triggers.md`.

### 3. Auto-Expire Old Entries

Before morning briefing, run cleanup to remove past dates:

```bash
python3 skills/travel-morning-weather/scripts/travel-cleaner.py
```

## Quick Reference

| Task | Reference |
|------|-----------|
| JSON schema + fields | `references/data-format.md` |
| Capture triggers + flow | `references/capture-triggers.md` |
| Morning cron integration | `references/morning-briefing.md` |
| Clean expired entries | `scripts/travel-cleaner.py` |
| Update travel data | `scripts/update-travel-plan.py` |
| Example data | `examples/travel-plan.json` |
