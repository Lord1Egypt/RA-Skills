---
name: Remind
slug: remind
version: 1.0.4
changelog: "Display name shown correctly"
description: >-
  Reminds the user of commitments they already know — meetings, deadlines, bills,
  promises, follow-ups — at the right lead time, in their style. Use when the user
  says remind me, nudge me, ping me, or don't let me forget, mentions a deadline,
  appointment, flight, renewal, birthday, or a promise they made, wants a recurring
  reminder, snoozes or reschedules one, needs to chase something a colleague promised,
  or reacts to reminder timing (too early, too late, I forgot). Not for announcing
  new information the user doesn't know yet (alerting) or executing tasks on a schedule.
homepage: https://clawic.com/skills/remind
metadata:
  clawdbot:
    emoji: ⏰
    displayName: Remind
    configPaths:
    - ~/Clawic/data/remind/
---

User preferences, learned lead times, and the active reminder list live in `~/Clawic/data/remind/` (see `setup.md` on first use, `memory-template.md` for file formats). If you have data at an old location (`~/remind/`, `~/clawic/remind/`, or preferences stored inside this file's sections), move it to `~/Clawic/data/remind/`.

## When To Use

**Remind = "Just a reminder that..."** — surfacing something the human already knows, at the moment it becomes actionable.

- Planned events, deadlines, and commitments they set themselves
- Promises they made to other people — and other people's promises they must chase
- Recurring obligations easy to lose track of: taxes, renewals, bills, reviews
- Things they told you they were afraid to forget
- Not for new information (news, outages, price moves — that is alerting) and not for executing tasks on a schedule (that is scheduling)

**The litmus test:** could they have written it in their own calendar? Then it's a reminder. Did the world just change? That's an alert. If "just a reminder that..." reads unnaturally in front of the message, don't send it as one.

## Quick Reference

| Situation | Play |
|---|---|
| "Remind me to X at/in Y" | Create exactly as stated; explicit override beats every learned preference and default |
| "Don't let me forget X" | Create with an extra earlier stage — the phrase signals stakes, not timing (`timing.md`, Adjustment Factors) |
| Commitment mentioned, no ask ("I'll send it Friday") | First 2 in a category: offer ("Want a nudge Friday morning?"); after 2 acceptances, create silently (`triggers.md`) |
| Recurring obligation (taxes, renewals, dentist) | `recurring.md` — cadence defaults, anchor drift, end conditions |
| "Later" / "not now" / no reaction to a reminder | `followup.md` — snooze, silence, re-ping rules |
| Reaction to a past reminder ("too early", "I forgot") | `learning.md` maps the phrase to a signal; adjust via the ladder in `timing.md` |
| They acknowledged the reminder | Done — no repeat unless the entry is under **Always** (`followup.md`) |
| Window missed (offline, late detection, quiet hours) | `followup.md` late delivery — lead with what is still possible |
| Several reminders due at once | Stack up to 3 in one message, hard deadlines first; more → digest (`phrasing.md`) |
| **Default: unsure if remindable** | High stakes → create and say so; low stakes → skip and watch what happens |

Depth on demand: `triggers.md` what qualifies · `timing.md` lead times, ladder, quiet hours, timezones · `phrasing.md` writing the message · `recurring.md` repeating obligations · `followup.md` after it fires: acks, snooze, escalation, misses · `learning.md` reactions → preferences · `setup.md` first use · `memory-template.md` storage formats.

## Core Rules

1. **Only remind about what they already know.** New information is an alert; the litmus test above decides. Misclassifying erodes trust in both channels.
2. **Explicit beats learned beats default.** "Remind me at 3pm" overrides every stored preference; a stored preference overrides `timing.md`; the defaults catch the rest. A one-off override never rewrites the category preference (`learning.md`).
3. **The loop: detect → evaluate → remind → observe → confirm → store.** Detect (`triggers.md`), evaluate against `~/Clawic/data/remind/preferences.md`, remind while they can still act, observe the reaction, confirm before storing.
4. **Signal ladder** (canonical — every other file points here): explicit instruction → store `(confirmed)` immediately · 2 consistent observed reactions → store `(pattern)`, propose the change · accepted proposal, or a 3rd consistent reaction → upgrade to `(confirmed)` · 1 contradicting reaction on a `(confirmed)` entry → downgrade to `(pattern)`, re-observe.
5. **Remind while acting is still possible.** Lead counts back from when the *action* must start, not from the event: `remind at = event time − process − transition − prep` (worked example in `timing.md`).
6. **One acknowledgment = done.** Repeats read as nagging; **Always** entries are the only exception, and silence is not an acknowledgment (`followup.md`).
7. **Never store without comment.** Wrong guesses compound invisibly; propose in one line before writing anything `(confirmed)`.
8. **A working system sends fewer reminders each month, not more.** Correct Skips are wins; let reactions promote categories, never your own eagerness.

## Reminder Components

- **What** — the commitment, phrased as the *action*, not the event: "Leave by 2:15 for the 5pm flight", never "Flight at 5pm". If the reminder arrives when the action is no longer possible, the timing was wrong regardless of the event time.
- **When** — lead time before the action must start (`timing.md`)
- **How** — tone, length, and stage wording (`phrasing.md`); default: one line, what + when + the single next step

## Output Gates

Run before every reminder goes out:

- [ ] Do they already know this? (No → it's an alert, not a reminder)
- [ ] Can they still act on it after this arrives? (No → apply `followup.md` late delivery; log the missed lead)
- [ ] Has this exact reminder — this occurrence, for recurring — been acknowledged? (Yes → drop unless in **Always**)
- [ ] Does a **Skip** entry, a stated exclusion, or `quiet_hours` cover it? (`timing.md`)
- [ ] Is it phrased as the action, not the event, with wording distinct from the previous stage? (`phrasing.md`)

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/remind/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| quiet_hours | text (HH:MM–HH:MM local) | 22:00–07:00 | Suppresses delivery inside the window unless the action itself must start there (`timing.md`, Time-of-Day Rules) |
| morning_slot | text (HH:MM–HH:MM local) | 07:00–08:00 | Where morning-of, daily-habit, and "tomorrow morning" reminders land |
| digest_slot | text (HH:MM) | none | When set, low-priority reminders batch into one daily digest at this time instead of arriving one by one (`phrasing.md`) |
| lead_bias | earlier \| standard \| later | standard | Shifts the default lead of every *unlearned* category one ladder step in that direction; learned preferences are untouched |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Delivery & tone** — register (casual/formal), length, emoji, language of reminders — affects `phrasing.md` defaults
- **Proactivity** — appetite for unprompted reminders from implicit detection — affects the offer-first rule in `triggers.md`
- **Schedule shape** — workday start/end, weekend policy for work items — affects Time-of-Day Rules in `timing.md`
- **Exclusions** — topics, projects, or blocks (focus time, meetings) where reminders never fire — feeds **Skip** and the Output Gates
- **Adjacent systems** — calendars or task apps already alerting them — categories those cover default to **Skip** (their alarm plus yours = double nag)

Per-category lead times are learned data, not config: they live in `~/Clawic/data/remind/preferences.md` (`memory-template.md` for the format).

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Reminding about everything detected | Fatigue: they tune out, and the one critical reminder dies with the noise | Skip low stakes by default; let reactions promote categories |
| Reminding at event time | Awareness without agency — nothing left to do but feel bad | Lead counts back from when the *action* starts (`timing.md` formula) |
| Repeating after an acknowledgment | Reads as nagging; erodes the trust the whole skill runs on | One ack = done; **Always** is the only exception (`followup.md`) |
| Treating "thanks" as "send more" | Politeness is not preference | Only timing words and actual misses move the ladder (`learning.md`) |
| Storing preferences silently | Wrong guesses compound invisibly; they can't correct what they can't see | Propose in one line before writing anything `(confirmed)` |
| Stretching lead time after one miss | One miss may be a bad day; overcorrection breeds "too early" complaints | Move one ladder step per 2 signals, never multiply |
| Same wording on every stage | Identical repeats read as a stuck bot, and get filtered like one | Each stage carries a different action verb (`phrasing.md`) |
| "You missed X" with nothing to do | Guilt without agency; the worst message this skill can send | Deliver a miss only when a recovery action exists, and lead with it (`followup.md`) |

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/remind (install if the user confirms):
- `alerts` - New or urgent events they don't know about yet
- `notify` - Delivery mechanics: channels, batching, fatigue control
- `schedule` - Executing recurring tasks, not recalling them
- `memory` - Long-term storage beyond reminder preferences

## Feedback

- If useful, star it: https://clawic.com/skills/remind
- Latest version: https://clawic.com/skills/remind

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/remind.
