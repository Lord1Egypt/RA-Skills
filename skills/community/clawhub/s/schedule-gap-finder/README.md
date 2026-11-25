# schedule-gap-finder (OpenClaw / AgentSkills skill)

Finds **schedule conflicts** and **free time slots** for one day from calendar events given as JSON or an `.ics` file, within configurable working hours. Pure Node.js: no dependencies, no network, read-only.

Original work for CSCI 599 Assignment 3 (advanced integration: custom skill published to ClawHub).

```bash
node scripts/gaps.mjs --day 2026-11-18 --tz America/Los_Angeles < events.json
node scripts/gaps.mjs --ics calendar.ics --day 2026-11-18 --tz America/Los_Angeles --json
node --test scripts/gaps.test.mjs   # unit tests (8)
```

Example output:
```
Schedule for 2026-11-18 (America/Los_Angeles), working window 08:00-18:00
- 9:00 AM-9:30 AM: Advisor 1:1
- 11:00 AM-12:00 PM: Lab sync
- 11:30 AM-12:30 PM: TA office hours
Conflicts (1):
- "Lab sync" overlaps "TA office hours" 11:30 AM-12:00 PM (30 min)
Free slots >= 30 min:
- 8:00 AM-9:00 AM (60 min)
- 9:30 AM-11:00 AM (90 min)
- 12:30 PM-6:00 PM (330 min)
Best block for focused work: 12:30 PM-6:00 PM (330 min)
```
