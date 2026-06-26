---
name: timezone-helper
description: Time zone conversion, world clock, and meeting planner. Use when the user asks about current time in a city, needs to convert time between zones, wants to schedule a meeting across multiple time zones, or asks about daylight saving time (DST). Built-in IANA timezone data for 200+ cities. No API key, no scripts, no Python required — fully offline.
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "🌍"
---

# Timezone Helper

Convert times between any time zones, plan global meetings, check DST status.
Zero dependencies — all data built-in, works in any environment.

Full city-to-timezone mapping: see `references/cities.md`.

## When to use

- "What time is it in Tokyo right now?"
- "Convert 3pm New York to London time"
- "Schedule a meeting for our team in SF, London and Singapore"
- "Does Germany observe DST? When does it change?"
- "What's the UTC offset for IST?"
- "Find a time that works for NYC, Berlin and Beijing"

---

## Core concepts

### UTC offset
Every timezone is expressed as UTC±HH:MM.
- UTC+9 = 9 hours ahead of UTC (Tokyo, Seoul)
- UTC-5 = 5 hours behind UTC (New York EST, Lima)
- UTC+0 = same as UTC (London GMT, Reykjavik)

### DST (Daylight Saving Time)
Some regions shift clocks ±1 hour seasonally:
- **Northern Hemisphere** (US, Europe, etc.): spring forward, fall back
  - US: second Sunday March → first Sunday November
  - EU: last Sunday March → last Sunday October
- **Southern Hemisphere** (Australia, NZ, etc.): opposite — DST in Oct–Apr
- **No DST**: China, Japan, India, most of Africa, Middle East, Southeast Asia

Always confirm the current date when doing DST-sensitive conversions.

---

## Step 1: Resolve city/region to IANA timezone

Use the table in `references/cities.md` to map user input to an IANA zone.
Common shortcuts to recognize:
```
EST / ET    → America/New_York  (UTC-5 standard, UTC-4 DST)
CST (US)    → America/Chicago   (UTC-6 standard, UTC-5 DST)
MST         → America/Denver    (UTC-7 standard, UTC-6 DST)
PST / PT    → America/Los_Angeles (UTC-8 standard, UTC-7 DST)
GMT / UTC   → UTC               (UTC+0, no DST)
BST         → Europe/London     (UTC+1, summer only)
CET / CEST  → Europe/Paris      (UTC+1 standard, UTC+2 DST)
IST         → Asia/Kolkata      (UTC+5:30, no DST)
CST (China) → Asia/Shanghai     (UTC+8, no DST)
JST         → Asia/Tokyo        (UTC+9, no DST)
AEST / AEDT → Australia/Sydney  (UTC+10 standard, UTC+11 DST)
```

---

## Step 2: Apply UTC offset

Conversion formula:
```
Target time = Source time + (Target UTC offset) - (Source UTC offset)
```

If result crosses midnight: adjust date ±1 day accordingly.

Example:
```
Convert 14:00 New York (EST, UTC-5) → Tokyo (JST, UTC+9)
Difference = +9 - (-5) = +14 hours
14:00 + 14h = 28:00 → 04:00 next day Tokyo
```

---

## Step 3: Check DST status

Before finalizing, verify whether DST is currently active for each zone.
If the user's current date is near a DST transition, note the change.

DST transitions (approximate):
```
US (spring forward):  Second Sunday of March,    02:00 → 03:00
US (fall back):       First Sunday of November,  02:00 → 01:00
EU (spring forward):  Last Sunday of March,      01:00 UTC → 02:00 UTC
EU (fall back):       Last Sunday of October,    01:00 UTC → 00:00 UTC
Australia/Sydney:     First Sunday of October,   02:00 → 03:00
Australia/Sydney:     First Sunday of April,     03:00 → 02:00
```

---

## Output formats

### Single conversion
```
🌍 Time Zone Conversion
━━━━━━━━━━━━━━━━━━━━
Source:  3:00 PM  Wed, Mar 20  —  New York (EST, UTC-5)
Target:  8:00 PM  Wed, Mar 20  —  London (GMT, UTC+0)
         4:00 AM  Thu, Mar 21  —  Tokyo (JST, UTC+9)
         1:00 AM  Thu, Mar 21  —  Singapore (SGT, UTC+8)
```

### World clock (current time)
```
🕐 Current World Time  (based on: 15:00 UTC)
━━━━━━━━━━━━━━━━━━━━
🇺🇸  New York       10:00 AM  Wed  (EST, UTC-5)
🇬🇧  London         15:00     Wed  (GMT, UTC+0)
🇩🇪  Berlin         16:00     Wed  (CET, UTC+1)
🇮🇳  Mumbai         20:30     Wed  (IST, UTC+5:30)
🇨🇳  Beijing        23:00     Wed  (CST, UTC+8)
🇯🇵  Tokyo          00:00     Thu  (JST, UTC+9)
🇦🇺  Sydney         02:00     Thu  (AEDT, UTC+11)
```

### Meeting planner
```
📅 Meeting Planner
━━━━━━━━━━━━━━━━━━━━
Participants:  San Francisco  /  London  /  Singapore

Option A — Best for SF + London:
  San Francisco   09:00 AM  (PST, UTC-8)   ✅ work hours
  London          17:00     (GMT, UTC+0)   ✅ end of day
  Singapore       01:00 AM  (SGT, UTC+8)   ❌ midnight

Option B — Best for London + Singapore:
  San Francisco   01:00 AM  (PST, UTC-8)   ❌ midnight
  London          09:00     (GMT, UTC+0)   ✅ work hours
  Singapore       17:00     (SGT, UTC+8)   ✅ work hours

No perfect overlap exists. Recommended compromise:
  San Francisco   06:00 AM  ⚠️  early
  London          14:00     ✅
  Singapore       22:00     ⚠️  late evening
```

### DST query
```
🕐 DST Information: Germany (Europe/Berlin)
━━━━━━━━━━━━━━━━━━━━
Current offset:    UTC+1  (CET — Central European Time)
DST observed:      Yes
DST offset:        UTC+2  (CEST — Central European Summer Time)
Spring forward:    Last Sunday of March   → clocks +1h at 02:00
Fall back:         Last Sunday of October → clocks -1h at 03:00
2026 transitions:  Mar 29 (→ CEST)  /  Oct 25 (→ CET)
```

---

## Meeting planner logic

When finding meeting overlap across zones:

```
1. Define "work hours" as 09:00–18:00 local time
2. Define "acceptable" as 07:00–21:00 local time
3. Convert each hour of the day to all participants' local times
4. Score each UTC hour:
   - All in work hours  → ✅ ideal
   - All in acceptable  → ⚠️  workable
   - Any outside 07-21  → ❌ avoid
5. Present top 2-3 options with clear local times
6. If no ideal slot exists, say so explicitly and suggest best compromise
```

---

## Notes

- Always ask for or confirm the current date when DST status matters
- "IST" is ambiguous: could be India (UTC+5:30), Israel (UTC+2), or Ireland (UTC+0/+1) — clarify with user if context is unclear
- "CST" is ambiguous: US Central (UTC-6/-5) or China Standard (UTC+8) — resolve from context
- Half-hour and 45-minute offsets exist: India (UTC+5:30), Iran (UTC+3:30), Nepal (UTC+5:45), Australia/Lord Howe (UTC+10:30/+11)
- For precise current-time queries, note that this skill provides static offset data; the actual current time depends on the system clock
