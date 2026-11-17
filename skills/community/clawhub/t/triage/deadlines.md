# Deadlines — Slack Math, Real vs Stated, Negotiation

The slack formula lives in SKILL.md (Core Rules #2): slack = working time until deadline − remaining work, counted in `working_hours` from config. This file is everything around the formula: the cases that break naive calendar math, telling real deadlines from stated ones, and what to do when slack goes negative.

## Slack Cases That Break Calendar Math

- **Timezones**: "EOD" means the SENDER's end of day. A requester 6 hours ahead turns "EOD Friday" into your Friday morning — resolve the timezone before computing slack, not after missing it.
- **Dependency chains**: your real due date = stated deadline − downstream lead time. A deliverable due Monday 9am that needs a reviewer is due before that reviewer's Friday ends; backward-schedule through every dependent step and triage against the earliest resulting date.
- **Scope growth**: calendar distance to a deadline is constant; slack is not — it shrinks when time passes AND when remaining work grows. Recompute on every scope change (SKILL.md, Core Rules #7), not on a timer.
- **Partial availability**: slack counts YOUR available working hours, not all working hours. Two days of meetings between now and Friday can turn comfortable slack negative without anything else changing.

## Real vs Stated Deadlines

Ask what consumes the output. The meeting, decision, launch, or dependent person behind the deadline is the real one; the stated date is often that minus someone's buffer.

Soft-deadline tells (each lowers confidence in the date; none abolishes it without checking):

- Round dates with no named consumer ("by the 1st", "end of month").
- Habitual "EOD" from a sender whose EODs never had consequences — sender calibration applies (signals.md).
- A date set by a middleman, not the consumer — buffers stack per hop; ask the middleman what THEIR deadline is.
- A deadline nobody can trace to a consequence is a preference, not a deadline: triage it on value, schedule it as a dated P2, and say which date you are treating as real.

**Urgency laundering** ("need it in an hour" for a task known for weeks — signals.md): the deadline may still be genuine. Honor the slack math, flag the pattern to the user separately. Slack and blame are separate ledgers.

## Negotiating When Slack Is Negative

Three moves, tried in this order — each preserves more trust than the next:

1. **Scope**: "What part do you need by then — a draft, the number, the decision?" Most deadline consumers need one slice, not the artifact.
2. **Sequence**: when two items both claim the same hours, force the ranking: "I can finish X by the deadline or Y — which first?" Never promise both.
3. **Time**: a new date, once, with buffer you will actually keep. A second slip on the same item converts every future estimate you give into noise.

Offer options, not alarm. "This doesn't fit" is a status report; "X by Friday or all of it Monday — pick" is triage.

## When a Deadline Moves

Re-triage the whole queue, not just the moved item (SKILL.md, Core Rules #7) — one moved deadline changes other items' relative slack and can flip their order. Announce the delta, not the whole queue: "Y moved to Thursday, so it now runs before X."

## The Missed-Deadline Protocol

- Report negative slack the moment it is detected, not at the deadline. Discovered today, it is a negotiation (moves above); discovered at the deadline, it is an incident plus a trust debit.
- When the miss is already certain: state the new realistic date and what changed, in one message, before being asked. The user learning it from you beats the user learning it from the consumer.
- Log it: a miss with no external cause is a triage failure — Override Log with reason (patterns.md), so the pattern can surface.
