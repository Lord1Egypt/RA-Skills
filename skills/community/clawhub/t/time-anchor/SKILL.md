---
name: time-anchor
description: Offload date math to code — get current date, days/weeks until goal dates, and month-end info. Use whenever you need to reason about relative dates or calculate "how many days until [event]." Especially important when comparing milestone timelines against today's date. Triggers on any message mentioning dates, deadlines, timeframes, "when," "days until," planning, scheduling, or temporal reasoning.
---

# Time Anchor

Use `exec` to run the bundled script instead of doing date math yourself. The script returns deterministic results — no guessing.

## Quick Usage

```bash
python3 ~/.openclaw/workspace/skills/time-anchor/scripts/time-anchor.py [--today | --until DATE | --weekday DAY | --month]
# No flags = full anchor: today + all configured goals + month info
```

| Flag | Output |
|------|--------|
| (none) | Full anchor: today, day of week, all goals in days/weeks, month info |
| `--today` | Today's date and day of week only |
| `--until YYYY-MM-DD` | Days to a specific arbitrary date |
| `--weekday Tuesday` | Upcoming occurrences + JSON with ambiguity flag |

For weekday labels, `0-7` days away maps to `this` / `this_week`; `8+` days away maps to `next` / `next_week`.
| `--month` | Days left in current month (excluding today) |

## Workflow Rules — Don't Guess

### 1. Named event → targets first, then memory/context, then web search, THEN ask.

User says "how far is Devconf?" → run full anchor to check if it's a configured goal. If not: check conversation history / memory for the date we discussed. Still unsure? Web search. STILL unsure? Ask which occurrence they mean.

### 2. Weekday references → default to NEXT upcoming occurrence (forward looking).

Today is Wednesday, user says "how far until Tuesday?" → use `--weekday Tuesday`, report the next one forward (6 days away). Never default to a past occurrence unless explicitly asked about something in the past.

### 3. Only return PAST occurrences on explicit past-tense phrasing:

- "How far away was last Tuesday?" → look backward, report most recent
- "How long has it been since summer started?" → calculate days since fixed date
- Any phrase with "since," "ago," "last" followed by weekday → backward lookup

### 4. Ambiguity: `--weekday` flags it, agent must ask.

When JSON output contains `"ambiguous": true`:
- **Do NOT pick one.** The tool is telling you there's a "this week" vs "next week" ambiguity.
- Ask the user to clarify which occurrence they mean.
- Short fuzzy weekday inputs should be at least 3 characters; if the prefix is still ambiguous, clarify rather than guessing.

## Adding Goals

Edit `~/.openclaw/workspace/skills/time-anchor/scripts/time-anchor.py`, add to the `TARGETS` dict:

```python
TARGETS = {
    "2026-10-15": "Event name here",  # YYYY-MM-DD: descriptive label
}
```

## Full documentation

See [README.md](README.md) for installation, ambiguity examples, and more.
