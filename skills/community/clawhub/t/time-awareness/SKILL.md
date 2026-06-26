# SKILL.md - Time Awareness

## Description
Never make time-sensitive mistakes again. Forces time verification before claims, prevents stale data, handles timezones correctly.

## Price
Free

## Commands
- "What time is it?" â Current time in multiple zones
- "Is the market open?" â Check market hours (ES, NQ, etc.)
- "When does the market open?" â Next market open time
- "Convert [time] to [timezone]" â Timezone conversion
- "Set my timezone to [zone]" â Configure your timezone

## Quick Start
1. Set your timezone: "Set my timezone to America/Denver"
2. Check market status: "Is ES open?"
3. Get current time: "What time is it?"

## Core Features

### Time Verification
- Always verifies current time before claims
- Prevents stale data (configurable max age)
- Handles DST transitions correctly

### Market Hours
- Supports ES, NQ, YM, CL, GC, and more
- Knows holidays and early closes
- RTH (Regular Trading Hours) and ETH (Extended)

### Timezone Handling
- 500+ timezone database
- Automatic conversion
- UTC as reference

## Examples

```
You: "Is the market open?"
Agent: "ES is currently CLOSED. Opens Monday at 6:00 PM MT (pre-market)."

You: "What time is it in Tokyo?"
Agent: "It's 8:15 AM JST (Tuesday) in Tokyo."

You: "When does NQ open?"
Agent: "NQ opens in 2 hours 15 minutes (6:00 PM MT)."
```

## Implementation

This skill uses Python's `zoneinfo` and `datetime` modules. No external API keys required.

---
*Time is money. Know it precisely.*
