# Urgency Signals

Signals raise suspicion; the level tests in SKILL.md decide. A signal never assigns a level by itself — it tells you which test to run first.

## Language Signals

**State-words outrank feeling-words.** "Prod is down" describes a verifiable state — run the P0 damage test immediately. "This is critical" describes a feeling — it earns a check, not a level.

- P0 candidates (state): "down", "outage", "breach", "data loss", "can't ship", "customers seeing errors", "meeting in N minutes" + missing deliverable
- P0 claims (feeling — verify before honoring): "urgent", "ASAP", "emergency", "critical"
- P1: "today", "by EOD", "blocking me", "client is waiting", named external stakeholder plus a date
- P2: "this week", "when possible", "should probably", internal improvement with no date
- P3: "no rush", "when you have time", "idea:", "someday", "nice to have", "FYI"

## Sender Calibration

Urgency words carry information relative to the sender's baseline, not the dictionary:

- A sender who marks most requests urgent → their "urgent" is noise; run the level tests as if the word were absent, and record the calibration (`patterns.md`, By Source).
- A sender who almost never escalates → their first "ASAP" is loud; treat as P1 minimum and verify for P0.
- Calibration is per sender, learned like any other rule: observe → propose → confirm.

## Context Signals

**Escalate suspicion when:** external deadline named; multiple people affected; revenue or customer impact; security or safety implications; follow-up to a previously urgent item.

**De-escalate suspicion when:** exploratory or brainstorming framing; no dependency named; the requester themselves is not planning to act on the result soon.

**Urgency laundering:** someone else's missed planning arriving as your emergency — "need this in an hour" for a task they've known about for weeks. The deadline may still be real (often genuine P1), but flag it to the user and record who launders; chronic launderers get sender calibration, not automatic escalation. Telling the real deadline from the stated one: `deadlines.md`.

## Source Defaults

Starting points before any learned rule; a confirmed rule in `patterns.md` always overrides this table.

| Source | Default | Why |
|--------|---------|-----|
| Direct real-time message | P1 | The sender chose the interruptive channel |
| Paging / on-call alert | P0 until disproven | Built to fire only on damage — verify fast, then downgrade if false |
| Repeated identical alert | Recalibrate, don't re-page | The Nth identical alert adds no information; noisy alerts need fixing, not honoring (`bugs.md`, Alerts) |
| Monitoring digest, dashboard | P2 | Batched by design |
| Forwarded email | P2 | If it were burning, they would have messaged |
| Anything prefixed "FYI" | P3 | Informational by declaration |
| Unknown / anything else | P2, then run level tests | Safe default; the tests correct it |

## Time Modifiers

- **Compute slack in working hours, not clock hours** — formula and worked weekend example: SKILL.md Core Rules #2.
- **User's focus time** — hold P2/P3 entirely; P1 waits for the current unit of work to finish; only P0 interrupts.
- **Before the user's known meetings** — items needed *for* the meeting inherit the meeting's start time as their deadline.
- **Friday afternoon** — don't start non-urgent multi-day work that will sit half-done over the weekend; queue it for Monday.

## Anti-Patterns

**Don't auto-elevate on:**
- Repetition — a third mention of the same task is frustration, not new urgency; answer with queue position
- Message length — verbosity correlates with thinking out loud, not with impact
- ALL CAPS or exclamation marks alone — style, not priority; look for a state-word or a date
- Sender seniority — rank predicts importance, not cost of delay (SKILL.md Traps)

**Don't auto-lower on:**
- Polite phrasing ("would you mind...") — some users soften everything; check for a date first
- Casual tone or humor — friendliness and urgency coexist
