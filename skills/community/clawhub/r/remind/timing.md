# Timing Defaults

Defaults, not measurements: every row is a starting point that a learned preference in `~/Clawic/data/remind/preferences.md` overrides. Precedence: explicit user instruction > learned preference > this file.

## The Lead Formula

Lead time counts back from when the **action** must start, not from the event:

`remind at = event time − process − transition − prep`

Worked example — flight at 17:00: airport process 90 min → be there 15:30; drive 45 min → leave 14:45; pack 30 min → action starts 14:15. Remind at ~14:15, not "flight at 5pm" sent at 16:00. The 3-hour travel default below is this formula with typical values; recompute when the user gives real ones.

## Standard Lead Times

With `lead_bias` set in config, shift every *unlearned* category default one ladder step in that direction; learned preferences are untouched.

| Category | Default Lead | Action it protects |
|----------|-------------|--------------------|
| Meeting/Call | 15 min | Wrap current task, open the link, scan the agenda |
| Deadline | 1 day + morning-of | A working session, then a final check |
| Flight/Travel | 3 hours | Pack + leave + airport process (formula above) |
| Birthday/Event | 1 week + day-of | Buy the gift; then say the words |
| Bill/Payment | 3 days | Transfer clearing time |
| Appointment | 1 hour | Travel there |
| Daily habit | `morning_slot` | Start-of-day intention |
| Renewal with notice period | Standard lead before the *decision* date (`recurring.md`) | Decide before the cancellation window closes |
| **Default: unlisted category** | 1 day, then learn | Safe first guess; one reaction cycle calibrates it |

## The Lead Ladder

All adjustments move **one step at a time** on this ladder — never multiply, never jump:

`5 min · 15 min · 30 min · 1 h · 3 h · morning-of · 1 day · 3 days · 1 week`

- "Too early" → one step shorter for that category
- "I forgot" / missed it → one step longer, and consider adding a stage (below)
- "Perfect timing" → lock the current step; stop adjusting
- Late twice in a category → one step longer even without a complaint

Move only after the 2-signal threshold (signal ladder, SKILL.md) — one reaction may be a bad day. `learning.md` maps reaction phrases to these moves.

## Adjustment Factors

| Situation | Adjustment |
|-----------|------------|
| High stakes ("don't let me forget") | Add an earlier stage; do NOT stretch the final lead — the last reminder still fires when the action starts |
| Requires prep work | Add a stage sized to the prep: "book the restaurant" needs days, "join the call" needs minutes |
| User voiced concern | Add one extra stage; concern is a stakes signal, not a timing signal |
| Consistently on time without help | One step shorter, or propose moving the category to **Skip** |

## Multi-Reminder Patterns

**Every stage carries a different action.** If two stages would say the same thing, delete one — identical repeats read as nagging (SKILL.md, Traps); stage-specific wording lives in `phrasing.md`.

```
Important deadline:
  1 week before  → start (block a working session)
  1 day before   → finish (the work happens here)
  morning of     → verify + submit
```

```
Travel:
  1 week    → book/confirm, start the packing list
  1 day     → pack, check in online
  ~3 hours  → leave (formula above gives the exact time)
```

Recurring obligations reuse these patterns on every cycle (`recurring.md`).

## Time-of-Day Rules

| Reminder Type | Delivery |
|---------------|----------|
| Morning tasks | `morning_slot` (default 07:00–08:00) |
| Work items | Start of their workday (Schedule shape area in config) |
| Work item landing on a weekend | Hold to Monday's workday start — unless the deadline arrives first |
| Personal | Evening before, or morning of |
| Same-day urgent | Immediately |
| Low priority | Batch into the next natural delivery, or the `digest_slot` if set (`phrasing.md`) |
| **Default** | Their next active hours, never mid-night |

**Quiet hours: no reminders inside `quiet_hours` (default 22:00–07:00 local)**, unless the action itself must start inside the window — a 6 AM flight beats quiet hours; a birthday card does not.

## Timezones, DST, Travel

- Store event-anchored reminders (flights, calls, appointments) in the **event's** local time; compute delivery against the user's *current* timezone at fire time, not at creation time.
- Travel day = the transition term of the lead formula grows. Recompute with real numbers; never reuse the home-city default drive time.
- Recurring local routines (`morning_slot`, daily habits) follow the wall clock through DST and travel; fixed external events follow the event's zone. The two drift apart exactly on travel days — which is when the reminder earns its keep.
- "Tomorrow" spoken between midnight and 04:00 is ambiguous: confirm the date once ("Friday the 26th?"). This is the one clarifying question worth its cost (SKILL.md caps you at one).

## Override Syntax

Explicit phrasing beats everything stored:

| Phrase | Interpretation |
|--------|----------------|
| "Remind me at 3pm" | Exact time; no adjustment, no learning applied |
| "Remind me in 2 hours" | Relative offset from now |
| "Remind me tomorrow morning" | Next day, `morning_slot` |
| "The day before" | 1 day lead |
| "Give me plenty of warning" | One ladder step earlier than the learned/default lead, plus an extra stage |
| "Remind me later" (no time) | Ask "when?" once; if unanswered, next natural delivery slot (`followup.md`, Snooze) |
